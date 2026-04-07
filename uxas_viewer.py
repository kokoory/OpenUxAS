#!/usr/bin/env python3
"""OpenUxAS PyQt Viewer - AMASE replacement with CesiumJS 3D map."""

import sys
import os
import json
import math
import time
import argparse
import threading
from pathlib import Path
from collections import deque

# e3 shim (pylmcp dependency)
import types
import glob as _glob
if 'e3' not in sys.modules:
    e3 = types.ModuleType('e3')
    e3_fs = types.ModuleType('e3.fs')
    e3_fs.ls = lambda p: sorted(_glob.glob(p))
    sys.modules['e3'] = e3
    sys.modules['e3.fs'] = e3_fs

# Add pylmcp to path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tests" / "cpp"))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QToolBar, QAction, QLabel, QComboBox,
    QSpinBox, QDoubleSpinBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QFormLayout, QGroupBox, QCheckBox, QStatusBar,
    QLineEdit, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QUrl
from PyQt5.QtGui import QFont, QColor

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
    from PyQt5.QtWebChannel import QWebChannel
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False

try:
    import zmq
    HAS_ZMQ = True
except ImportError:
    HAS_ZMQ = False

# Try loading pylmcp
HAS_PYLMCP = False
try:
    from pylmcp import Object
    from pylmcp.message import Message
    HAS_PYLMCP = True
except Exception:
    pass


# ============================================================
# Message Thread - ZMQ listener
# ============================================================
class MessageThread(QThread):
    vehicle_state = pyqtSignal(dict)
    vehicle_config = pyqtSignal(dict)
    mission_command = pyqtSignal(dict)
    task_received = pyqtSignal(dict)
    zone_received = pyqtSignal(dict)
    raw_message = pyqtSignal(str)
    connected = pyqtSignal(bool)

    def __init__(self, sub_port=5560, push_port=5561):
        super().__init__()
        self.sub_port = sub_port
        self.push_port = push_port
        self._running = True
        self.push_socket = None

    def run(self):
        if not HAS_ZMQ:
            self.raw_message.emit("[ERROR] pyzmq not installed. pip install pyzmq")
            return
        ctx = zmq.Context()
        sub = ctx.socket(zmq.SUB)
        sub.connect(f"tcp://127.0.0.1:{self.sub_port}")
        sub.setsockopt(zmq.SUBSCRIBE, b"")
        sub.setsockopt(zmq.RCVTIMEO, 500)

        self.push_socket = ctx.socket(zmq.PUSH)
        self.push_socket.connect(f"tcp://127.0.0.1:{self.push_port}")

        self.connected.emit(True)
        self.raw_message.emit(f"[CONNECTED] SUB:{self.sub_port} PUSH:{self.push_port}")

        while self._running:
            try:
                raw = sub.recv(zmq.NOBLOCK)
                self._process(raw)
            except zmq.Again:
                continue
            except Exception as e:
                self.raw_message.emit(f"[ERROR] {e}")

        sub.close()
        if self.push_socket:
            self.push_socket.close()
        ctx.term()
        self.connected.emit(False)

    def _process(self, raw):
        try:
            parts = raw.split(b'$', 2)
            if len(parts) < 3:
                return
            addr = parts[0].decode('utf-8', errors='replace')
            attrs = parts[1].decode('utf-8', errors='replace')
            attr_parts = attrs.split('|')
            descriptor = attr_parts[1] if len(attr_parts) > 1 else addr
            short_name = descriptor.split('.')[-1] if '.' in descriptor else descriptor

            ts = time.strftime('%H:%M:%S')
            self.raw_message.emit(f"[{ts}] {descriptor}")

            # Try LMCP unpack
            data = {}
            if HAS_PYLMCP:
                try:
                    msg = Message.unpack(raw)
                    data = self._obj_to_dict(msg.obj)
                except Exception:
                    pass

            if short_name == 'AirVehicleState':
                self._emit_vehicle_state(data, descriptor)
            elif short_name == 'AirVehicleConfiguration':
                self.vehicle_config.emit(data)
            elif short_name == 'MissionCommand':
                self.mission_command.emit(data)
            elif 'SearchTask' in short_name or 'Task' in short_name:
                data['_type'] = short_name
                self.task_received.emit(data)
            elif 'Zone' in short_name:
                data['_type'] = short_name
                self.zone_received.emit(data)
        except Exception as e:
            self.raw_message.emit(f"[PARSE ERROR] {e}")

    def _emit_vehicle_state(self, data, descriptor):
        state = {
            'id': data.get('ID', 0),
            'lat': 0, 'lng': 0, 'alt': 0,
            'heading': data.get('Heading', 0),
            'airspeed': data.get('Airspeed', 0),
            'energy': data.get('EnergyAvailable', 100),
            'time': data.get('Time', 0),
        }
        loc = data.get('Location', {})
        if isinstance(loc, dict):
            state['lat'] = loc.get('Latitude', 0)
            state['lng'] = loc.get('Longitude', 0)
            state['alt'] = loc.get('Altitude', 0)
        self.vehicle_state.emit(state)

    def _obj_to_dict(self, obj):
        if obj is None:
            return {}
        if hasattr(obj, 'data'):
            result = {}
            for k, v in obj.data.items():
                if hasattr(v, 'data'):
                    result[k] = self._obj_to_dict(v)
                elif isinstance(v, list):
                    result[k] = [self._obj_to_dict(i) if hasattr(i, 'data') else i for i in v]
                else:
                    result[k] = v
            return result
        return {}

    def send_msg(self, obj):
        if self.push_socket and HAS_PYLMCP:
            msg = Message(obj=obj, source_entity_id=100, source_service_id=0)
            self.push_socket.send(msg.pack())

    def stop(self):
        self._running = False


# ============================================================
# Map Bridge - Python <-> JS communication
# ============================================================
class MapBridge(QWidget):
    """Wraps QWebEngineView with CesiumJS map."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        if HAS_WEBENGINE:
            self.web = QWebEngineView()
            html_path = ROOT / "cesium_map.html"
            if html_path.exists():
                self.web.setUrl(QUrl.fromLocalFile(str(html_path)))
            else:
                self.web.setHtml("<h2>cesium_map.html not found</h2>")
            layout.addWidget(self.web)
        else:
            lbl = QLabel("PyQtWebEngine not installed.\npip install PyQtWebEngine")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("background:#1a1a2e;color:#aaa;font-size:16px;padding:40px")
            layout.addWidget(lbl)
            self.web = None

    def run_js(self, code):
        if self.web:
            self.web.page().runJavaScript(code)

    def update_vehicle(self, vid, lat, lng, alt, heading, speed):
        self.run_js(f"updateVehicle({vid},{lat},{lng},{alt},{heading},{speed})")

    def add_waypoint(self, wp_id, lat, lng, alt, vehicle_id):
        self.run_js(f"addWaypoint({wp_id},{lat},{lng},{alt},{vehicle_id})")

    def draw_route(self, vehicle_id, wp_list):
        js_arr = json.dumps(wp_list)
        self.run_js(f"drawRoute({vehicle_id},{js_arr})")

    def draw_task(self, task_id, task_type, label, points):
        js_pts = json.dumps(points)
        self.run_js(f"drawTaskArea({task_id},'{task_type}','{label}',{js_pts})")

    def draw_zone(self, zone_id, zone_type, points):
        js_pts = json.dumps(points)
        self.run_js(f"drawZone({zone_id},'{zone_type}',{js_pts})")

    def fly_to(self, lat, lng, alt=30000):
        self.run_js(f"flyTo({lat},{lng},{alt})")

    def fit_all(self):
        self.run_js("fitAll()")

    def clear_all(self):
        self.run_js("clearAll()")


# ============================================================
# Vehicle Config Panel
# ============================================================
class VehiclePanel(QGroupBox):
    def __init__(self):
        super().__init__("Vehicle Configuration")
        layout = QFormLayout(self)
        self.vehicle_select = QComboBox()
        self.vehicle_select.currentIndexChanged.connect(self._on_select)
        layout.addRow("Vehicle:", self.vehicle_select)

        self.lbl_id = QLabel("--")
        self.lbl_speed = QLabel("--")
        self.lbl_alt = QLabel("--")
        self.lbl_pos = QLabel("--")
        self.lbl_heading = QLabel("--")
        self.lbl_energy = QLabel("--")
        self.lbl_time = QLabel("--")

        layout.addRow("ID:", self.lbl_id)
        layout.addRow("Speed (m/s):", self.lbl_speed)
        layout.addRow("Altitude (m):", self.lbl_alt)
        layout.addRow("Position:", self.lbl_pos)
        layout.addRow("Heading:", self.lbl_heading)
        layout.addRow("Energy %:", self.lbl_energy)
        layout.addRow("Sim Time:", self.lbl_time)

        self.vehicles = {}

    def update_state(self, state):
        vid = state.get('id', 0)
        self.vehicles[vid] = state
        # Add to combo if new
        if self.vehicle_select.findText(str(vid)) < 0:
            self.vehicle_select.addItem(str(vid))
        # Update if selected
        sel = self.vehicle_select.currentText()
        if str(vid) == sel:
            self._show(state)

    def _on_select(self, idx):
        txt = self.vehicle_select.currentText()
        if txt and int(txt) in self.vehicles:
            self._show(self.vehicles[int(txt)])

    def _show(self, s):
        self.lbl_id.setText(str(s.get('id', '--')))
        self.lbl_speed.setText(f"{s.get('airspeed', 0):.1f}")
        self.lbl_alt.setText(f"{s.get('alt', 0):.0f}")
        self.lbl_pos.setText(f"{s.get('lat', 0):.5f}, {s.get('lng', 0):.5f}")
        self.lbl_heading.setText(f"{s.get('heading', 0):.1f}")
        self.lbl_energy.setText(f"{s.get('energy', 0):.0f}")
        self.lbl_time.setText(str(s.get('time', '--')))


# ============================================================
# Task Panel
# ============================================================
class TaskPanel(QGroupBox):
    def __init__(self):
        super().__init__("Tasks & Zones")
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Label"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

    def add_task(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(data.get('TaskID', data.get('id', '')))))
        self.table.setItem(row, 1, QTableWidgetItem(data.get('_type', '')))
        self.table.setItem(row, 2, QTableWidgetItem(data.get('Label', '')))

    def add_zone(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(data.get('ZoneID', ''))))
        self.table.setItem(row, 1, QTableWidgetItem(data.get('_type', '')))
        self.table.setItem(row, 2, QTableWidgetItem(data.get('Label', '')))


# ============================================================
# Message Log Panel
# ============================================================
class MessageLog(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 9))
        self.setStyleSheet("background:#0f172a;color:#a3e635;border:none")
        self.max_lines = 500
        self.line_count = 0

    def append_msg(self, text):
        self.append(text)
        self.line_count += 1
        if self.line_count > self.max_lines:
            cursor = self.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.Down, cursor.KeepAnchor, 100)
            cursor.removeSelectedText()
            self.line_count -= 100


# ============================================================
# Main Window
# ============================================================
class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("OpenUxAS Viewer")
        self.setMinimumSize(1200, 700)
        self.args = args
        self.msg_thread = None
        self.msg_count = 0

        self._build_toolbar()
        self._build_ui()
        self._build_statusbar()

        # Auto-connect if ports specified
        if args.auto_connect:
            QTimer.singleShot(500, self.do_connect)

    def _build_toolbar(self):
        tb = QToolBar("Main")
        tb.setMovable(False)
        self.addToolBar(tb)

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.setStyleSheet("background:#22c55e;color:#fff;padding:6px 16px;border-radius:4px;font-weight:bold")
        self.btn_connect.clicked.connect(self.do_connect)
        tb.addWidget(self.btn_connect)

        tb.addSeparator()

        tb.addWidget(QLabel(" SUB Port: "))
        self.spin_sub = QSpinBox()
        self.spin_sub.setRange(1000, 65535)
        self.spin_sub.setValue(self.args.sub_port)
        tb.addWidget(self.spin_sub)

        tb.addWidget(QLabel(" PUSH Port: "))
        self.spin_push = QSpinBox()
        self.spin_push.setRange(1000, 65535)
        self.spin_push.setValue(self.args.push_port)
        tb.addWidget(self.spin_push)

        tb.addSeparator()

        btn_fit = QPushButton("Fit All")
        btn_fit.clicked.connect(lambda: self.map_widget.fit_all())
        tb.addWidget(btn_fit)

        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self._clear_all)
        tb.addWidget(btn_clear)

        tb.addSeparator()

        tb.addWidget(QLabel(" Map: "))
        self.map_combo = QComboBox()
        self.map_combo.addItems(["OpenStreetMap", "VWorld"])
        tb.addWidget(self.map_combo)

        self.vworld_key = QLineEdit()
        self.vworld_key.setPlaceholderText("VWorld API Key")
        self.vworld_key.setFixedWidth(150)
        tb.addWidget(self.vworld_key)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)

        # Main splitter: left panel | map | right panel
        h_split = QSplitter(Qt.Horizontal)

        # Left panel
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.vehicle_panel = VehiclePanel()
        self.task_panel = TaskPanel()
        left_layout.addWidget(self.vehicle_panel)
        left_layout.addWidget(self.task_panel)
        left.setMaximumWidth(280)

        # Map
        self.map_widget = MapBridge()

        # Right: tabs for log
        right = QTabWidget()
        self.msg_log = MessageLog()
        right.addTab(self.msg_log, "Messages")

        # Info tab
        info = QTextEdit()
        info.setReadOnly(True)
        info.setHtml("""
        <h3>OpenUxAS Viewer</h3>
        <p><b>Usage:</b></p>
        <ol>
        <li>Start UxAS with PublishPullBridge (ports 5560/5561)</li>
        <li>Click <b>Connect</b> to receive messages</li>
        <li>Vehicle positions appear on the 3D map</li>
        <li>Routes and tasks are drawn automatically</li>
        </ol>
        <p><b>Dependencies:</b> PyQt5, PyQtWebEngine, pyzmq</p>
        <p><b>Map:</b> CesiumJS + OpenStreetMap (no API key needed)</p>
        """)
        right.addTab(info, "Help")
        right.setMaximumWidth(350)

        h_split.addWidget(left)
        h_split.addWidget(self.map_widget)
        h_split.addWidget(right)
        h_split.setSizes([250, 600, 300])

        main_layout.addWidget(h_split)

    def _build_statusbar(self):
        self.statusBar().showMessage("Disconnected | 0 messages | 0 vehicles")

    def do_connect(self):
        if self.msg_thread and self.msg_thread.isRunning():
            self.msg_thread.stop()
            self.msg_thread.wait(2000)
            self.msg_thread = None
            self.btn_connect.setText("Connect")
            self.btn_connect.setStyleSheet("background:#22c55e;color:#fff;padding:6px 16px;border-radius:4px;font-weight:bold")
            self._update_status(False)
            return

        sub_port = self.spin_sub.value()
        push_port = self.spin_push.value()
        self.msg_thread = MessageThread(sub_port, push_port)
        self.msg_thread.vehicle_state.connect(self._on_vehicle_state)
        self.msg_thread.vehicle_config.connect(self._on_vehicle_config)
        self.msg_thread.mission_command.connect(self._on_mission_command)
        self.msg_thread.task_received.connect(self._on_task)
        self.msg_thread.zone_received.connect(self._on_zone)
        self.msg_thread.raw_message.connect(self._on_raw_msg)
        self.msg_thread.connected.connect(self._update_status)
        self.msg_thread.start()

        self.btn_connect.setText("Disconnect")
        self.btn_connect.setStyleSheet("background:#ef4444;color:#fff;padding:6px 16px;border-radius:4px;font-weight:bold")

    def _on_vehicle_state(self, state):
        vid = state.get('id', 0)
        self.vehicle_panel.update_state(state)
        self.map_widget.update_vehicle(
            vid, state['lat'], state['lng'], state['alt'],
            state['heading'], state['airspeed']
        )

    def _on_vehicle_config(self, data):
        vid = data.get('ID', 0)
        self.msg_log.append_msg(f"[CONFIG] Vehicle {vid}: {data.get('Label', '')}")

    def _on_mission_command(self, data):
        vid = data.get('VehicleID', 0)
        wp_list_raw = data.get('WaypointList', [])
        wp_list = []
        for wp in wp_list_raw:
            if isinstance(wp, dict):
                loc = wp
                wp_list.append({
                    'id': loc.get('Number', 0),
                    'lat': loc.get('Latitude', 0),
                    'lng': loc.get('Longitude', 0),
                    'alt': loc.get('Altitude', 500)
                })
                self.map_widget.add_waypoint(
                    loc.get('Number', 0),
                    loc.get('Latitude', 0), loc.get('Longitude', 0),
                    loc.get('Altitude', 500), vid
                )
        if wp_list:
            self.map_widget.draw_route(vid, wp_list)
        self.msg_log.append_msg(f"[MISSION] Vehicle {vid}: {len(wp_list)} waypoints")

    def _on_task(self, data):
        self.task_panel.add_task(data)
        ttype = data.get('_type', '')
        tid = data.get('TaskID', 0)
        label = data.get('Label', '')
        points = []

        if 'AreaSearch' in ttype:
            area = data.get('SearchArea', {})
            bp = area.get('BoundaryPoints', [])
            for p in bp:
                if isinstance(p, dict):
                    points.append({'lat': p.get('Latitude', 0), 'lng': p.get('Longitude', 0)})
            if points:
                self.map_widget.draw_task(tid, 'area', label, points)
        elif 'LineSearch' in ttype:
            pl = data.get('PointList', [])
            for p in pl:
                if isinstance(p, dict):
                    points.append({'lat': p.get('Latitude', 0), 'lng': p.get('Longitude', 0)})
            if points:
                self.map_widget.draw_task(tid, 'line', label, points)
        elif 'PointSearch' in ttype:
            loc = data.get('SearchLocation', {})
            if isinstance(loc, dict):
                points.append({'lat': loc.get('Latitude', 0), 'lng': loc.get('Longitude', 0)})
            if points:
                self.map_widget.draw_task(tid, 'point', label, points)

    def _on_zone(self, data):
        self.task_panel.add_zone(data)
        zid = data.get('ZoneID', 0)
        ztype = 'keepin' if 'KeepIn' in data.get('_type', '') else 'keepout'
        boundary = data.get('Boundary', {})
        points = []
        bp = boundary.get('BoundaryPoints', [])
        for p in bp:
            if isinstance(p, dict):
                points.append({'lat': p.get('Latitude', 0), 'lng': p.get('Longitude', 0)})
        if points:
            self.map_widget.draw_zone(zid, ztype, points)

    def _on_raw_msg(self, text):
        self.msg_count += 1
        self.msg_log.append_msg(text)
        n_vehicles = len(self.vehicle_panel.vehicles)
        self.statusBar().showMessage(
            f"Connected | {self.msg_count} messages | {n_vehicles} vehicles"
        )

    def _update_status(self, connected):
        if connected:
            self.statusBar().showMessage("Connected | 0 messages | 0 vehicles")
        else:
            self.statusBar().showMessage("Disconnected")

    def _clear_all(self):
        self.map_widget.clear_all()
        self.msg_log.clear()
        self.msg_count = 0
        self.vehicle_panel.vehicles.clear()
        self.vehicle_panel.vehicle_select.clear()
        self.task_panel.table.setRowCount(0)

    def closeEvent(self, event):
        if self.msg_thread:
            self.msg_thread.stop()
            self.msg_thread.wait(2000)
        event.accept()


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="OpenUxAS PyQt Viewer")
    parser.add_argument("--sub-port", type=int, default=5560, help="ZMQ SUB port (default 5560)")
    parser.add_argument("--push-port", type=int, default=5561, help="ZMQ PUSH port (default 5561)")
    parser.add_argument("--auto-connect", action="store_true", help="Auto-connect on startup")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark theme
    from PyQt5.QtGui import QPalette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.WindowText, QColor(205, 214, 244))
    palette.setColor(QPalette.Base, QColor(24, 24, 37))
    palette.setColor(QPalette.AlternateBase, QColor(30, 30, 46))
    palette.setColor(QPalette.ToolTipBase, QColor(205, 214, 244))
    palette.setColor(QPalette.ToolTipText, QColor(205, 214, 244))
    palette.setColor(QPalette.Text, QColor(205, 214, 244))
    palette.setColor(QPalette.Button, QColor(49, 50, 68))
    palette.setColor(QPalette.ButtonText, QColor(205, 214, 244))
    palette.setColor(QPalette.Highlight, QColor(137, 180, 250))
    palette.setColor(QPalette.HighlightedText, QColor(30, 30, 46))
    app.setPalette(palette)

    win = MainWindow(args)
    win.show()

    # Status check
    deps = []
    if not HAS_ZMQ:
        deps.append("pyzmq")
    if not HAS_WEBENGINE:
        deps.append("PyQtWebEngine")
    if deps:
        win.msg_log.append_msg(f"[WARNING] Missing: {', '.join(deps)}")
        win.msg_log.append_msg(f"[WARNING] pip install {' '.join(deps)}")
    if not HAS_PYLMCP:
        win.msg_log.append_msg("[WARNING] pylmcp not loaded - message parsing limited")
    win.msg_log.append_msg("[INFO] OpenUxAS Viewer ready")
    win.msg_log.append_msg("[INFO] Click 'Connect' to start receiving messages")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
