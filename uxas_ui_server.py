#!/usr/bin/env python3
"""
OpenUxAS Web UI Server
- Launches a web-based UI for configuring, running, and analyzing OpenUxAS
- No external dependencies required (uses Python standard library only)
- Usage: python3 uxas_ui_server.py [--port 8080]
"""

import http.server
import socketserver
import json
import os
import sys
import subprocess
import threading
import signal
import sqlite3
import xml.etree.ElementTree as ET
import glob
import time
import shutil
import re
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
UXAS_ROOT = os.path.dirname(os.path.abspath(__file__))
UXAS_BIN = os.path.join(UXAS_ROOT, "obj", "cpp", "uxas")
EXAMPLES_DIR = os.path.join(UXAS_ROOT, "examples")
DEFAULT_PORT = 8080

# ── Global State ───────────────────────────────────────────────────────────
uxas_process = None
uxas_output_lines = []
uxas_lock = threading.Lock()
uxas_running = False


# ── Helper Functions ───────────────────────────────────────────────────────

def list_examples():
    """List available example directories."""
    examples = []
    if os.path.isdir(EXAMPLES_DIR):
        for name in sorted(os.listdir(EXAMPLES_DIR)):
            path = os.path.join(EXAMPLES_DIR, name)
            if os.path.isdir(path) and not name.startswith('.'):
                cfg_files = glob.glob(os.path.join(path, "cfg_*.xml")) + \
                            glob.glob(os.path.join(path, "*_cfg.xml"))
                yaml_file = os.path.join(path, "config.yaml")
                has_yaml = os.path.isfile(yaml_file)
                examples.append({
                    "name": name,
                    "path": name,
                    "cfg_files": [os.path.basename(f) for f in cfg_files],
                    "has_yaml": has_yaml
                })
    return examples


def parse_xml_config(filepath):
    """Parse a UxAS XML configuration file and return structured data."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        config = {
            "entityId": root.get("EntityID", "100"),
            "entityType": root.get("EntityType", "Aircraft"),
            "runDuration": root.get("RunDuration_s", ""),
            "formatVersion": root.get("FormatVersion", "1.0"),
            "services": [],
            "bridges": []
        }
        for svc in root.findall("Service"):
            svc_data = {"type": svc.get("Type", ""), "attributes": {}}
            for k, v in svc.attrib.items():
                if k != "Type":
                    svc_data["attributes"][k] = v
            # Parse sub-elements (e.g., Message entries)
            messages = []
            for msg in svc.findall("Message"):
                messages.append(dict(msg.attrib))
            if messages:
                svc_data["messages"] = messages
            # Parse LogMessage entries
            log_messages = []
            for lm in svc.findall("LogMessage"):
                log_messages.append(dict(lm.attrib))
            if log_messages:
                svc_data["logMessages"] = log_messages
            config["services"].append(svc_data)
        for br in root.findall("Bridge"):
            br_data = {"type": br.get("Type", ""), "attributes": {}, "subscriptions": []}
            for k, v in br.attrib.items():
                if k != "Type":
                    br_data["attributes"][k] = v
            for sub in br.findall("SubscribeToMessage"):
                br_data["subscriptions"].append(sub.get("MessageType", ""))
            config["bridges"].append(br_data)
        return config
    except Exception as e:
        return {"error": str(e)}


def parse_message_xml(filepath):
    """Parse a LMCP message XML file."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        return _element_to_dict(root)
    except Exception as e:
        return {"error": str(e)}


def _element_to_dict(elem):
    """Recursively convert XML element to dictionary."""
    result = {"_tag": elem.tag, "_attrib": dict(elem.attrib)}
    children = list(elem)
    if children:
        child_list = []
        for child in children:
            child_list.append(_element_to_dict(child))
        result["_children"] = child_list
    else:
        result["_text"] = (elem.text or "").strip()
    return result


def list_message_files(example_path):
    """List all message XML files for an example."""
    messages = []
    msg_dir = os.path.join(example_path, "MessagesToSend")
    if os.path.isdir(msg_dir):
        for root_dir, dirs, files in os.walk(msg_dir):
            for f in sorted(files):
                if f.endswith('.xml'):
                    rel = os.path.relpath(os.path.join(root_dir, f), msg_dir)
                    messages.append(rel)
    return messages


def _build_services_from_ui_config(config_data):
    """Convert UI buildConfig() format to services list."""
    services = []
    algo = config_data.get("algorithm", {})
    svc_settings = algo.get("services", {})

    # Map of UI key -> (ServiceType, attributes builder)
    svc_map = {
        "arv": ("AutomationRequestValidatorService",
                lambda s: {"MaxResponseTime_ms": str(
                    s.get("maxResponseTime", 5000))}),
        "taskManager": ("TaskManagerService", lambda s: {}),
        "routePlanner": ("RoutePlannerVisibilityService",
                         lambda s: {
                             k: str(v) for k, v in {
                                 "TurnRadiusOffset_m":
                                     s.get("turnRadiusOffset"),
                                 "MinWaypointSeparation_m":
                                     s.get("minWaypointSeparation"),
                             }.items() if v}),
        "routeAggregator": ("RouteAggregatorService", lambda s: {}),
        "atbb": ("AssignmentTreeBranchBoundService",
                 lambda s: {
                     k: str(v) for k, v in {
                         "NumberNodesMaximum": s.get("maxNodes"),
                         "CostFunction": s.get("costFunction"),
                     }.items() if v}),
        "planBuilder": ("PlanBuilderService",
                        lambda s: {
                            k: str(v) for k, v in {
                                "AssignmentStartPointLead_m":
                                    s.get("assignmentStartPointLead"),
                            }.items() if v}),
        "sensorManager": ("SensorManagerService", lambda s: {}),
        "batchSummary": ("BatchSummaryService", lambda s: {}),
    }

    for key, (svc_type, attr_fn) in svc_map.items():
        settings = svc_settings.get(key, {})
        if settings.get("enabled", True):
            attrs = attr_fn(settings)
            services.append({"type": svc_type, "attributes": attrs})

    # WaypointPlanManager
    wp = algo.get("waypointManager", {})
    if wp:
        wp_attrs = {}
        if wp.get("numServe"):
            wp_attrs["NumberWaypointsToServe"] = str(wp["numServe"])
        if wp.get("numOverlap"):
            wp_attrs["NumberWaypointsOverlap"] = str(wp["numOverlap"])
        if wp.get("loiterRadius"):
            wp_attrs["DefaultLoiterRadius_m"] = str(wp["loiterRadius"])
        if wp.get("turnType"):
            wp_attrs["TurnType"] = wp["turnType"]
        if wp.get("gimbalPayloadId"):
            wp_attrs["GimbalPayloadId"] = str(wp["gimbalPayloadId"])
        vid = config_data.get("entityId", 100)
        wp_attrs["VehicleID"] = str(vid)
        services.append({
            "type": "WaypointPlanManagerService",
            "attributes": wp_attrs
        })

    # Logging
    logging = algo.get("logging", {})
    if logging.get("enabled", True):
        log_attrs = {}
        if logging.get("messageCountLimit"):
            log_attrs["MessageCountLimit"] = str(
                logging["messageCountLimit"])
        if logging.get("filesPerSubDir"):
            log_attrs["FilesPerSubDirectory"] = str(
                logging["filesPerSubDir"])
        services.append({
            "type": "MessageLoggerDataService",
            "attributes": log_attrs
        })

    return services


def generate_xml_config(config_data):
    """Generate UxAS XML configuration from structured data."""
    root = ET.Element("UxAS")
    root.set("FormatVersion", config_data.get("formatVersion", "1.0"))
    root.set("EntityID", str(config_data.get("entityId", "100")))
    root.set("EntityType", config_data.get("entityType", "Aircraft"))
    if config_data.get("runDuration"):
        root.set("RunDuration_s", str(config_data["runDuration"]))

    # If config has 'algorithm' key, it's from the UI buildConfig()
    # Convert to services list
    services = config_data.get("services", [])
    if not services and config_data.get("algorithm"):
        services = _build_services_from_ui_config(config_data)

    for br in config_data.get("bridges", []):
        br_elem = ET.SubElement(root, "Bridge")
        br_elem.set("Type", br["type"])
        for k, v in br.get("attributes", {}).items():
            br_elem.set(k, str(v))
        for sub in br.get("subscriptions", []):
            sub_elem = ET.SubElement(br_elem, "SubscribeToMessage")
            sub_elem.set("MessageType", sub)

    for svc in services:
        svc_elem = ET.SubElement(root, "Service")
        svc_elem.set("Type", svc["type"])
        for k, v in svc.get("attributes", {}).items():
            svc_elem.set(k, str(v))
        for msg in svc.get("messages", []):
            msg_elem = ET.SubElement(svc_elem, "Message")
            for k, v in msg.items():
                msg_elem.set(k, str(v))
        for lm in svc.get("logMessages", []):
            lm_elem = ET.SubElement(svc_elem, "LogMessage")
            for k, v in lm.items():
                lm_elem.set(k, str(v))

    ET.indent(root, space="    ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def generate_vehicle_xml(vehicle_data):
    """Generate AirVehicleConfiguration XML from structured data."""
    root = ET.Element("AirVehicleConfiguration")
    root.set("Series", "CMASI")
    root.set("Time", "1.0")

    for field in ["ID", "Label", "MinimumSpeed", "MaximumSpeed",
                  "NominalSpeed", "NominalAltitude", "NominalAltitudeType"]:
        if field in vehicle_data:
            el = ET.SubElement(root, field)
            el.text = str(vehicle_data[field])

    # Flight profile
    fp_data = vehicle_data.get("flightProfile", {})
    nfp = ET.SubElement(root, "NominalFlightProfile")
    fp = ET.SubElement(nfp, "FlightProfile")
    fp.set("Series", "CMASI")
    for fld in ["Airspeed", "PitchAngle", "VerticalSpeed", "MaxBankAngle", "EnergyRate"]:
        el = ET.SubElement(fp, fld)
        el.text = str(fp_data.get(fld, "0"))

    ET.SubElement(root, "AlternateFlightProfiles")
    ET.SubElement(root, "PayloadConfigurationList")

    ET.indent(root, space="    ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def generate_vehicle_state_xml(state_data):
    """Generate AirVehicleState XML from structured data."""
    root = ET.Element("AirVehicleState")
    root.set("Series", "CMASI")

    for field in ["ID"]:
        el = ET.SubElement(root, field)
        el.text = str(state_data.get(field, "400"))

    loc = ET.SubElement(root, "Location")
    loc3d = ET.SubElement(loc, "Location3D")
    loc3d.set("Series", "CMASI")
    for fld in ["Latitude", "Longitude", "Altitude"]:
        el = ET.SubElement(loc3d, fld)
        el.text = str(state_data.get(fld, "0"))
    el = ET.SubElement(loc3d, "AltitudeType")
    el.text = state_data.get("AltitudeType", "MSL")

    for fld in ["Heading", "Airspeed", "EnergyAvailable", "Time"]:
        el = ET.SubElement(root, fld)
        el.text = str(state_data.get(fld, "0"))

    el = ET.SubElement(root, "Mode")
    el.text = "Waypoint"

    ET.indent(root, space="    ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def generate_task_xml(task_data):
    """Generate task XML from structured data."""
    task_type = task_data.get("taskType", "LineSearchTask")
    root = ET.Element(task_type)
    root.set("Series", "CMASI")

    if task_type == "LineSearchTask":
        pl = ET.SubElement(root, "PointList")
        for pt in task_data.get("points", []):
            loc = ET.SubElement(pl, "Location3D")
            loc.set("Series", "CMASI")
            ET.SubElement(loc, "Latitude").text = str(pt.get("lat", 0))
            ET.SubElement(loc, "Longitude").text = str(pt.get("lng", 0))
            ET.SubElement(loc, "Altitude").text = str(pt.get("alt", 0))
    elif task_type == "AreaSearchTask":
        sa = ET.SubElement(root, "SearchArea")
        poly = ET.SubElement(sa, "Polygon")
        poly.set("Series", "CMASI")
        bp = ET.SubElement(poly, "BoundaryPoints")
        for pt in task_data.get("points", []):
            loc = ET.SubElement(bp, "Location3D")
            loc.set("Series", "CMASI")
            ET.SubElement(loc, "Latitude").text = str(pt.get("lat", 0))
            ET.SubElement(loc, "Longitude").text = str(pt.get("lng", 0))
            ET.SubElement(loc, "Altitude").text = "0"
    elif task_type == "PointSearchTask":
        sl = ET.SubElement(root, "SearchLocation")
        loc = ET.SubElement(sl, "Location3D")
        loc.set("Series", "CMASI")
        pts = task_data.get("points", [{"lat": 0, "lng": 0}])
        ET.SubElement(loc, "Latitude").text = str(pts[0].get("lat", 0))
        ET.SubElement(loc, "Longitude").text = str(pts[0].get("lng", 0))
        ET.SubElement(loc, "Altitude").text = "0"

    ET.SubElement(root, "TaskID").text = str(task_data.get("taskId", 1000))
    ET.SubElement(root, "Label").text = task_data.get("label", "Task")
    ET.SubElement(root, "EligibleEntities")
    ET.SubElement(root, "Priority").text = str(task_data.get("priority", 0))
    ET.SubElement(root, "Required").text = str(task_data.get("required", True)).lower()

    dwb = ET.SubElement(root, "DesiredWavelengthBands")
    ET.SubElement(dwb, "WavelengthBand").text = task_data.get("wavelengthBand", "AllAny")
    ET.SubElement(root, "DwellTime").text = str(task_data.get("dwellTime", 0))
    ET.SubElement(root, "GroundSampleDistance").text = str(task_data.get("gsd", 0))

    ET.indent(root, space="    ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def generate_automation_request_xml(request_data):
    """Generate AutomationRequest XML."""
    root = ET.Element("AutomationRequest")
    root.set("Series", "CMASI")
    ET.SubElement(root, "Label").text = request_data.get("label", "UIRequest")
    el = ET.SubElement(root, "EntityList")
    entities = request_data.get("entities",
                                request_data.get("entityIds", []))
    for eid in entities:
        e = ET.SubElement(el, "int64")
        e.text = str(eid)
    tl = ET.SubElement(root, "TaskList")
    tasks = request_data.get("tasks", request_data.get("taskIds", []))
    for tid in tasks:
        t = ET.SubElement(tl, "int64")
        t.text = str(tid)
    ET.indent(root, space="    ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def start_uxas(config_path, run_dir=None):
    """Start UxAS process with given config."""
    global uxas_process, uxas_output_lines, uxas_running

    if not os.path.isfile(UXAS_BIN):
        return {"error": f"UxAS binary not found at {UXAS_BIN}"}

    with uxas_lock:
        if uxas_running:
            return {"error": "UxAS is already running"}

    cwd = run_dir or os.path.dirname(config_path)
    cmd = [UXAS_BIN, "-cfgPath", config_path]

    with uxas_lock:
        uxas_output_lines = []
        uxas_running = True

    def run():
        global uxas_process, uxas_running, uxas_output_lines
        try:
            proc = subprocess.Popen(
                cmd, cwd=cwd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            uxas_process = proc
            for line in proc.stdout:
                with uxas_lock:
                    ts = time.strftime("%H:%M:%S")
                    uxas_output_lines.append(f"[{ts}] {line.rstrip()}")
                    if len(uxas_output_lines) > 5000:
                        uxas_output_lines = uxas_output_lines[-3000:]
            proc.wait()
        except Exception as e:
            with uxas_lock:
                uxas_output_lines.append(f"[ERROR] {str(e)}")
        finally:
            with uxas_lock:
                uxas_running = False
                uxas_output_lines.append("[SYSTEM] UxAS process terminated")
            uxas_process = None

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return {"status": "started", "cmd": " ".join(cmd), "cwd": cwd}


def stop_uxas():
    """Stop UxAS process."""
    global uxas_process, uxas_running
    if uxas_process:
        try:
            uxas_process.terminate()
            uxas_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            uxas_process.kill()
        uxas_process = None
        with uxas_lock:
            uxas_running = False
        return {"status": "stopped"}
    return {"status": "not_running"}


def get_output():
    """Get current output lines."""
    with uxas_lock:
        return {
            "running": uxas_running,
            "lines": list(uxas_output_lines[-200:]),
            "total": len(uxas_output_lines)
        }


def read_log_database(db_path):
    """Read messages from a UxAS log database."""
    results = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"SELECT * FROM [{table}] LIMIT 100")
            cols = [d[0] for d in cursor.description]
            for row in cursor.fetchall():
                results.append({"table": table, "columns": cols,
                                "data": [str(v) for v in row]})
        conn.close()
    except Exception as e:
        results.append({"error": str(e)})
    return results


def read_log_table(db_path, table_name):
    """Read a specific table from a UxAS log database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM [{table_name}] LIMIT 500")
        cols = [d[0] for d in cursor.description]
        rows = []
        for row in cursor.fetchall():
            rows.append({cols[i]: str(v) for i, v in enumerate(row)})
        conn.close()
        return {"columns": cols, "rows": rows}
    except Exception as e:
        return {"error": str(e), "columns": [], "rows": []}


def find_run_outputs(example_path):
    """Find output files from a previous run."""
    outputs = {"databases": [], "logs": [], "xml_files": []}
    for pattern in ["RUNDIR*", "datawork*", "log*"]:
        for d in glob.glob(os.path.join(example_path, pattern)):
            if os.path.isdir(d):
                for root_dir, dirs, files in os.walk(d):
                    for f in files:
                        fp = os.path.join(root_dir, f)
                        rel = os.path.relpath(fp, example_path)
                        if f.endswith('.db') or f.endswith('.db3'):
                            outputs["databases"].append(rel)
                        elif f.endswith('.log') or f.endswith('.txt'):
                            outputs["logs"].append(rel)
                        elif f.endswith('.xml'):
                            outputs["xml_files"].append(rel)
    return outputs


def validate_config(config_data):
    """Validate a UxAS configuration for common errors."""
    errors = []
    warnings = []

    eid = config_data.get("entityId", "")
    if not eid or not str(eid).isdigit():
        errors.append("EntityID must be a positive integer")

    services = config_data.get("services", [])
    service_types = [s["type"] for s in services]

    # Check required services for automation pipeline
    pipeline_services = [
        "AutomationRequestValidatorService",
        "TaskManagerService",
        "RouteAggregatorService",
        "RoutePlannerVisibilityService",
        "AssignmentTreeBranchBoundService",
        "PlanBuilderService"
    ]

    has_send_msg = "SendMessagesService" in service_types
    if has_send_msg:
        missing = [s for s in pipeline_services if s not in service_types]
        if missing:
            warnings.append(
                f"Automation pipeline incomplete. Missing: {', '.join(missing)}")

    # Check B&B cost function
    for svc in services:
        if svc["type"] == "AssignmentTreeBranchBoundService":
            cf = svc.get("attributes", {}).get("CostFunction", "")
            if cf and cf not in ["MINMAX", "CUMULATIVE"]:
                errors.append(
                    f"CostFunction must be MINMAX or CUMULATIVE, got '{cf}'")

    # Check WaypointPlanManager has VehicleID
    for svc in services:
        if svc["type"] == "WaypointPlanManagerService":
            if "VehicleID" not in svc.get("attributes", {}):
                errors.append("WaypointPlanManagerService requires VehicleID")

    # Check for duplicate service types that should be unique
    unique_types = ["TaskManagerService", "RouteAggregatorService",
                    "AssignmentTreeBranchBoundService", "PlanBuilderService"]
    for ut in unique_types:
        count = service_types.count(ut)
        if count > 1:
            warnings.append(f"{ut} appears {count} times (usually only 1)")

    return {"errors": errors, "warnings": warnings, "valid": len(errors) == 0}


# ── HTTP Request Handler ──────────────────────────────────────────────────

class UxASHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for the UxAS Web UI."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path.startswith("/api/"):
            self._handle_api_get(path, parse_qs(parsed.query))
        else:
            self.send_error(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len else "{}"
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        self._handle_api_post(path, data)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _serve_html(self):
        html_path = os.path.join(UXAS_ROOT, "uxas_ui.html")
        if os.path.isfile(html_path):
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "uxas_ui.html not found")

    def _handle_api_get(self, path, params):
        if path == "/api/examples":
            self._send_json(list_examples())

        elif path == "/api/config":
            fp = params.get("path", [""])[0]
            if fp and os.path.isfile(fp):
                self._send_json(parse_xml_config(fp))
            else:
                self._send_json({"error": "File not found"}, 404)

        elif path == "/api/messages":
            ep = params.get("example", [""])[0]
            if ep:
                self._send_json(list_message_files(ep))
            else:
                self._send_json([])

        elif path == "/api/message":
            fp = params.get("path", [""])[0]
            if fp and os.path.isfile(fp):
                self._send_json(parse_message_xml(fp))
            else:
                self._send_json({"error": "File not found"}, 404)

        elif path == "/api/message/raw":
            fp = params.get("path", [""])[0]
            if fp and os.path.isfile(fp):
                with open(fp, "r") as f:
                    self._send_json({"content": f.read()})
            else:
                self._send_json({"error": "File not found"}, 404)

        elif path == "/api/output":
            self._send_json(get_output())

        elif path == "/api/status":
            self._send_json({
                "running": uxas_running,
                "binary_exists": os.path.isfile(UXAS_BIN),
                "binary_path": UXAS_BIN
            })

        elif path == "/api/outputs":
            ep = params.get("path", params.get("example", [""]))[0]
            if ep:
                # Resolve relative paths against UXAS_ROOT
                if not os.path.isabs(ep):
                    ep = os.path.join(UXAS_ROOT, ep)
                outputs = find_run_outputs(ep)
                # Also look for .db files directly
                db_files = []
                for db in outputs.get("databases", []):
                    db_files.append(os.path.join(ep, db))
                # Get table names from first db
                db_tables = []
                if db_files and os.path.isfile(db_files[0]):
                    try:
                        conn = sqlite3.connect(db_files[0])
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT name FROM sqlite_master "
                            "WHERE type='table'")
                        db_tables = [r[0] for r in cursor.fetchall()]
                        conn.close()
                    except Exception:
                        pass
                outputs["dbPath"] = db_files[0] if db_files else ""
                outputs["dbTables"] = db_tables
                self._send_json(outputs)
            else:
                self._send_json({})

        elif path == "/api/logdb":
            fp = params.get("path", [""])[0]
            table = params.get("table", [""])[0]
            if fp and not os.path.isabs(fp):
                fp = os.path.join(UXAS_ROOT, fp)
            if fp and os.path.isfile(fp):
                if table:
                    # Return structured data for a specific table
                    result = read_log_table(fp, table)
                    self._send_json(result)
                else:
                    self._send_json(read_log_database(fp))
            else:
                self._send_json({"error": f"DB not found: {fp}"}, 404)

        elif path == "/api/file":
            fp = params.get("path", [""])[0]
            if fp and os.path.isfile(fp):
                with open(fp, "r") as f:
                    self._send_json({"content": f.read()})
            else:
                self._send_json({"error": "File not found"}, 404)

        else:
            self._send_json({"error": "Unknown API"}, 404)

    def _handle_api_post(self, path, data):
        if path == "/api/start":
            cfg = data.get("configPath", "")
            run_dir = data.get("runDir", None)
            example = data.get("example", "")
            if not cfg and not example:
                self._send_json({"error": "configPath required"}, 400)
                return
            # Resolve config path from example name
            if not cfg and example:
                example_name = os.path.basename(example.rstrip("/\\"))
                example_path = os.path.join(EXAMPLES_DIR, example_name)
                cfg_files = glob.glob(
                    os.path.join(example_path, "cfg_*.xml")) + \
                    glob.glob(os.path.join(example_path, "*_cfg.xml"))
                if cfg_files:
                    cfg = cfg_files[0]
                    if not run_dir:
                        run_dir = os.path.join(
                            example_path,
                            f"RUNDIR_{example_name}")
                        os.makedirs(run_dir, exist_ok=True)
            # Resolve relative paths
            if cfg and not os.path.isabs(cfg):
                cfg = os.path.join(UXAS_ROOT, cfg)
            if run_dir and not os.path.isabs(run_dir):
                run_dir = os.path.join(UXAS_ROOT, run_dir)
            if not os.path.isfile(cfg):
                self._send_json(
                    {"error": f"Config file not found: {cfg}"}, 404)
                return
            result = start_uxas(cfg, run_dir)
            self._send_json(result)

        elif path == "/api/stop":
            self._send_json(stop_uxas())

        elif path == "/api/validate":
            result = validate_config(data)
            self._send_json(result)

        elif path == "/api/generate/config":
            xml_str = generate_xml_config(data)
            self._send_json({"xml": xml_str})

        elif path == "/api/generate/vehicle":
            xml_str = generate_vehicle_xml(data)
            self._send_json({"xml": xml_str})

        elif path == "/api/generate/state":
            xml_str = generate_vehicle_state_xml(data)
            self._send_json({"xml": xml_str})

        elif path == "/api/generate/task":
            xml_str = generate_task_xml(data)
            self._send_json({"xml": xml_str})

        elif path == "/api/generate/request":
            xml_str = generate_automation_request_xml(data)
            self._send_json({"xml": xml_str})

        elif path == "/api/save":
            fp = data.get("path", "")
            content = data.get("content", "")
            if not fp:
                self._send_json({"error": "path required"}, 400)
                return
            try:
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, "w") as f:
                    f.write(content)
                self._send_json({"status": "saved", "path": fp})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        elif path == "/api/run/example":
            example_name = data.get("name", "")
            # Extract just the directory name if full path was sent
            example_name = os.path.basename(example_name.rstrip("/\\"))
            example_path = os.path.join(EXAMPLES_DIR, example_name)
            if not os.path.isdir(example_path):
                self._send_json({"error": f"Example not found: {example_name}"}, 404)
                return
            # Find config file
            cfg_files = glob.glob(os.path.join(example_path, "cfg_*.xml")) + \
                        glob.glob(os.path.join(example_path, "*_cfg.xml"))
            if not cfg_files:
                self._send_json({"error": "No config file found"}, 404)
                return
            cfg_path = cfg_files[0]
            # Create RUNDIR
            run_dir = os.path.join(example_path,
                                   f"RUNDIR_{example_name}")
            os.makedirs(run_dir, exist_ok=True)
            result = start_uxas(cfg_path, run_dir)
            self._send_json(result)

        elif path == "/api/run/custom":
            # Save config, messages, and run
            config = data.get("config", {})
            vehicles = data.get("vehicles", [])
            states = data.get("states", [])
            tasks = data.get("tasks", [])
            request = data.get("request", {})
            run_name = data.get("runName", "custom_run")

            run_dir = os.path.join(UXAS_ROOT, "custom_runs", run_name)
            msg_dir = os.path.join(run_dir, "MessagesToSend")
            task_dir = os.path.join(msg_dir, "tasks")
            os.makedirs(task_dir, exist_ok=True)

            # Generate message files and update config
            send_messages = []
            t_ms = 200

            for i, v in enumerate(vehicles):
                fname = f"AirVehicleConfiguration_V{v.get('ID', 400+i*100)}.xml"
                xml_str = generate_vehicle_xml(v)
                with open(os.path.join(msg_dir, fname), "w") as f:
                    f.write(xml_str)
                send_messages.append({"MessageFileName": fname,
                                      "SendTime_ms": str(t_ms)})
                t_ms += 50

            for i, s in enumerate(states):
                fname = f"AirVehicleState_V{s.get('ID', 400+i*100)}.xml"
                xml_str = generate_vehicle_state_xml(s)
                with open(os.path.join(msg_dir, fname), "w") as f:
                    f.write(xml_str)
                send_messages.append({"MessageFileName": fname,
                                      "SendTime_ms": str(t_ms)})
                t_ms += 50

            for i, task in enumerate(tasks):
                tid = task.get("taskId", 1000 + i)
                ttype = task.get("taskType", "LineSearchTask")
                fname = f"tasks/{tid}_{ttype}.xml"
                xml_str = generate_task_xml(task)
                with open(os.path.join(task_dir,
                          f"{tid}_{ttype}.xml"), "w") as f:
                    f.write(xml_str)
                send_messages.append({"MessageFileName": fname,
                                      "SendTime_ms": str(t_ms)})
                t_ms += 100

            if request:
                fname = "tasks/AutomationRequest.xml"
                xml_str = generate_automation_request_xml(request)
                with open(os.path.join(task_dir,
                          "AutomationRequest.xml"), "w") as f:
                    f.write(xml_str)
                send_messages.append({"MessageFileName": fname,
                                      "SendTime_ms": str(t_ms + 4000)})

            # Add SendMessagesService to config
            has_sender = False
            for svc in config.get("services", []):
                if svc["type"] == "SendMessagesService":
                    has_sender = True
                    svc["attributes"]["PathToMessageFiles"] = \
                        "./MessagesToSend/"
                    svc["messages"] = send_messages
            if not has_sender:
                config.setdefault("services", []).append({
                    "type": "SendMessagesService",
                    "attributes": {"PathToMessageFiles": "./MessagesToSend/"},
                    "messages": send_messages
                })

            # Save config XML
            cfg_path = os.path.join(run_dir, "cfg_custom.xml")
            xml_str = generate_xml_config(config)
            with open(cfg_path, "w") as f:
                f.write(xml_str)

            # Start UxAS
            result = start_uxas(cfg_path, run_dir)
            result["configPath"] = cfg_path
            result["runDir"] = run_dir
            self._send_json(result)

        else:
            self._send_json({"error": "Unknown API"}, 404)

    def log_message(self, format, *args):
        pass  # Suppress default HTTP logs


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "--port" and i + 2 < len(sys.argv):
                port = int(sys.argv[i + 2])
            elif arg.isdigit():
                port = int(arg)

    handler = UxASHandler
    with ReusableTCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"=" * 60)
        print(f"  OpenUxAS Web UI Server")
        print(f"  http://localhost:{port}")
        print(f"  UxAS Binary: {UXAS_BIN}")
        print(f"  Examples: {EXAMPLES_DIR}")
        print(f"=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            stop_uxas()
            httpd.shutdown()


if __name__ == "__main__":
    main()
