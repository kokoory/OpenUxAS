# CLAUDE.md - OpenUxAS Project Guide

## Project Overview

OpenUxAS is a multi-UAV autonomous mission planning and control framework developed by the Air Force Research Laboratory (AFRL). It uses a modular service-based architecture where loosely coupled services communicate via LMCP (Lightweight Message Control Protocol) messages over ZeroMQ transport.

- **Version**: 3.2.0
- **Languages**: C++ (primary), Ada/SPARK (formally verified services)
- **License**: Air Force Open Source Agreement v1.0
- **Repository**: https://github.com/afrl-rq/OpenUxAS

## Repository Structure

```
OpenUxAS/
├── src/
│   ├── cpp/                          # C++ source (main implementation)
│   │   ├── UxAS_Main.cpp             # Entry point (v3.2.0)
│   │   ├── Services/                 # 25+ service implementations
│   │   ├── Tasks/                    # 22 task service implementations
│   │   ├── Communications/           # ZeroMQ + LMCP networking layer
│   │   ├── Plans/                    # Planning algorithms, data structures
│   │   ├── DPSS/                     # Dynamic Path Search & Smooth planning
│   │   ├── Includes/                 # Constants, type definitions
│   │   ├── Utilities/                # Logging, file I/O, config management
│   │   └── VisilibityLib/            # Visibility graph library
│   └── ada/                          # Ada/SPARK formally verified services
│       ├── src/services/             # arv, atbb, route_aggregator, waypoint_manager
│       └── proof/sessions/           # SPARK proof session cache
├── mdms/                             # LMCP message definition XMLs
│   ├── CMASI.xml                     # Core mission management messages
│   ├── IMPACT.xml                    # Impact analysis messages
│   ├── UXTASK.xml                    # UxAS task messages
│   ├── ROUTE.xml                     # Route planning messages
│   ├── UXNATIVE.xml                  # UxAS native messages
│   ├── PERCEIVE.xml                  # Perception messages
│   └── VEHICLES.xml                  # Vehicle configuration messages
├── infrastructure/
│   ├── specs/                        # Anod build specifications
│   │   ├── uxas.anod                 # Main UxAS build spec
│   │   ├── uxas-ada.anod             # Ada variant
│   │   ├── uxas-lmcp.anod            # LMCP code generation
│   │   ├── boost.anod, zeromq.anod   # Dependencies
│   │   └── ...
│   ├── uxas/src/uxas/cli/            # CLI tools (build, printenv, devel-setup)
│   ├── paths.sh                      # Environment variables
│   ├── run_example.py                # Example runner framework
│   └── sbx/                          # Sandbox (built third-party libs, gitignored)
├── tests/
│   ├── cpp/                          # C++ test suite
│   │   ├── run-tests / run-tests.py  # Test runner
│   │   ├── tests/arv/               # 21+ ARV test scenarios
│   │   └── pylmcp/                   # Python LMCP library for testing
│   └── proof/                        # SPARK proof suite
│       ├── run-proofs / run-proofs.py
│       └── proofs/                   # Proof test cases
├── examples/                         # 15 example configurations
│   ├── 01_HelloWorld/                # Simple message exchange
│   ├── 02_Example_WaterwaySearch/    # Main multi-UAV demo
│   ├── 05_AssignTasks/               # Task assignment demo
│   └── ...
├── external_libraries/               # External algorithm libs
├── doc/                              # Doxygen and reference docs
├── resources/                        # Build scripts, LMCP gen tools
├── Makefile                          # C++ build (non-recursive)
├── anod                              # Anod build orchestration entry point
└── run-example                       # Example execution wrapper
```

## Build System

### Primary Build: Anod + Make

OpenUxAS uses a two-layer build system:

1. **Anod** (from e3 framework): Manages dependency resolution and orchestration
2. **GNU Make**: Compiles C++ source via `Makefile`

### Quick Build Commands

```bash
# Full build via Anod (handles all dependencies)
./anod build uxas

# Incremental C++ build via Make (after initial Anod setup)
make -j all

# Build Ada variant
./anod build uxas-ada

# Generate LMCP code from MDM XMLs
./anod build uxas-lmcp

# Print build environment
./anod printenv uxas
./anod printenv uxas --build-env    # Export-ready format

# Clean sandbox and rebuild
./anod reset
```

### Makefile Details

- **Location**: `/home/user/OpenUxAS/Makefile`
- **C++ Standard**: C++17 (`-std=c++17`)
- **Flags**: `-fPIC -DBOOST_ALLOW_DEPRECATED_HEADERS -DBOOST_GEOMETRY_DISABLE_DEPRECATED_03_WARNING`
- **Output**: `obj/cpp/` directory
- **Binary**: `uxas` executable
- **Coverage**: Set `ENABLE_COVERAGE=true` for gcov instrumentation

### Key Dependencies

| Library    | Purpose                         |
|------------|--------------------------------|
| Boost      | filesystem, regex, date_time   |
| ZeroMQ     | Message queue transport        |
| CZMQ       | C binding for ZeroMQ           |
| CppZMQ     | C++ ZeroMQ header-only binding |
| Zyre       | P2P discovery over ZeroMQ      |
| PugiXML    | XML parsing (int64-patched)    |
| SQLite3    | Embedded database              |
| SQLiteCPP  | C++ wrapper for SQLite         |

### LMCP Code Generation

LMCP classes are auto-generated from XML definitions in `mdms/`. Generated code goes to `src/cpp/LMCP/` (gitignored). Regenerate with:

```bash
./anod build uxas-lmcp
# or
python3 resources/run_lmcpgen.py
```

## Architecture

### Service-Based Design

All functionality is implemented as **services** that:
1. Extend `ServiceBase` (which extends `LmcpObjectNetworkClientBase`)
2. Self-register via `CreationRegistrar<T>` static factory pattern
3. Subscribe to LMCP message types
4. Communicate through a central `LmcpObjectNetworkServer` message hub
5. Run in their own threads

### Key Service Categories

**Planning & Routing:**
- `AssignmentTreeBranchBoundService` - Branch & Bound task assignment optimization
- `RouteAggregatorService` - Route request aggregation
- `RoutePlannerVisibilityService` - Visibility graph path planning
- `PlanBuilderService` - Final plan assembly

**Automation:**
- `AutomationRequestValidatorService` (ARV) - Request validation & orchestration
- `TaskManagerService` - Task lifecycle management
- `SensorManagerService` - Sensor footprint computation
- `BatchSummaryService` - Batch processing coordination

**Vehicle Control:**
- `WaypointPlanManagerService` - Waypoint plan management
- `SteeringService` - Vehicle steering commands
- `LoiterLeash` - Loiter radius management

**Communication:**
- `SendMessagesService` - Timed message dispatch
- `StatusReportService` - Status reporting
- `MessageLoggerDataService` - Message logging to SQLite

### Task Services

Task services extend `TaskServiceBase` and implement specific mission tasks:
- `CmasiAreaSearchTaskService`, `CmasiLineSearchTaskService`, `CmasiPointSearchTaskService`
- `PatternSearchTaskService`, `AngledAreaSearchTaskService`
- `BlockadeTaskService`, `CordonTaskService`, `EscortTaskService`
- `CommRelayTaskService`, `OverwatchTaskService`, `MustFlyTaskService`
- `LoiterTaskService`, `MultiVehicleWatchTaskService`

### Message Flow Pipeline

```
AutomationRequest
  → AutomationRequestValidatorService (validation)
  → TaskManagerService (task planning options)
  → RouteAggregatorService (route requests)
  → RoutePlannerVisibilityService (path computation)
  → AssignmentTreeBranchBoundService (optimal assignment)
  → PlanBuilderService (plan assembly)
  → MissionCommand (output to vehicles)
```

### Communication Architecture

```
Services ←→ LmcpObjectNetworkServer (ZeroMQ hub) ←→ Bridges ←→ External Systems
```

- **Internal**: ZeroMQ PUSH/PULL sockets between services and hub
- **External Bridges**: TCP, Serial, Zyre (P2P), Pub/Pull, Sub/Push
- **Message Format**: `address$contentType|descriptor|sourceGroup|sourceEntityId|sourceServiceId$payload`
- **Address Format**: `eid<entityId>.sid<serviceId>` for targeted delivery

### Threading Model

- Main thread: Configuration loading, startup
- Network server thread: Central message routing
- ServiceManager thread: Service lifecycle monitoring
- Per-service threads: Independent service execution
- Bridge threads: External communication

## Configuration

### XML Service Configuration

Services are configured via XML files (typically `cfg_*.xml`):

```xml
<UxAS EntityID="100" FormatVersion="1.0" RunDuration_s="10.0">
  <Service Type="HelloWorld" StringToSend="Hello" SendPeriod_ms="1000"/>
  <Service Type="TaskManagerService"/>
  <Bridge Type="LmcpObjectNetworkPublishPullBridge"
          AddressPUB="tcp://*:5560" AddressPULL="tcp://*:5561">
    <SubscribeToMessage MessageType="afrl.cmasi.MissionCommand"/>
  </Bridge>
</UxAS>
```

### Example Configuration (YAML)

Each example has a `config.yaml`:

```yaml
amase:
  scenario: Scenario_WaterwaySearch.xml
uxas:
  config: cfg_WaterwaySearch.xml
  rundir: RUNDIR_WaterwaySearch
```

## Testing

### C++ Tests

```bash
# Run all C++ tests
./tests/cpp/run-tests

# Tests are in tests/cpp/tests/<category>/<test_name>/test.py
# 21+ ARV test scenarios covering:
#   - correct_automation_request
#   - wrong_automation_request_* (various error conditions)
#   - task_automation_request_planning_states
#   - timeout_automation_response
#   - etc.
```

**Test Framework (pylmcp)**:
- Tests are Python scripts using `pylmcp` library
- `UxASConfig()` creates service configurations dynamically
- `Server()` launches UxAS and manages ZeroMQ communication
- `wait_for_msg()` validates expected LMCP responses

### SPARK Proofs

```bash
# Run proofs in replay mode (fast, uses cached sessions)
./tests/proof/run-proofs

# Generate new session files (slow)
./tests/proof/run-proofs --no-replay

# Show error diffs
./tests/proof/run-proofs -E
```

### Running Examples

```bash
./run-example --list                      # List available examples
./run-example 01_HelloWorld               # Run hello world
./run-example 02_Example_WaterwaySearch   # Run waterway search (needs AMASE for full sim)
```

## Development Patterns

### Adding a New Service

1. Copy template from `src/cpp/Services/00_ServiceTemplate.h/.cpp`
2. Rename class and update service type string
3. Implement `configure()`, `initialize()`, `processReceivedLmcpMessage()`
4. Register with `CreationRegistrar<YourService>` static member
5. Add to Makefile source list (auto-discovered from `src/cpp/Services/`)

### Adding a New Task

1. Copy template from `src/cpp/Tasks/00_TaskTemplate.h/.cpp`
2. Extend `TaskServiceBase`
3. Implement `buildTaskPlanOptions()`, `activeEntityState()`, `taskComplete()`
4. Register with `CreationRegistrar<YourTask>`

### Adding New LMCP Messages

1. Edit or create XML definitions in `mdms/` (see `mdms/ADDMDM.md`)
2. Run LMCP code generation: `./anod build uxas-lmcp`
3. Generated code appears in `src/cpp/LMCP/` (gitignored)
4. Rebuild: `make -j all`

### Service Registration Pattern

```cpp
// In header:
static const std::string& s_registryServiceTypeNames() {
    static std::string name = "MyServiceType";
    return name;
}

// In cpp:
static ServiceBase::CreationRegistrar<MyService>
    s_registrar(MyService::s_registryServiceTypeNames());
```

## File Naming Conventions

| Type              | Pattern                            | Example                           |
|-------------------|------------------------------------|-----------------------------------|
| Service header    | `NameService.h`                    | `PlanBuilderService.h`            |
| Service source    | `NameService.cpp`                  | `PlanBuilderService.cpp`          |
| Task header       | `NameTaskService.h`                | `CmasiAreaSearchTaskService.h`    |
| Task source       | `NameTaskService.cpp`              | `CmasiAreaSearchTaskService.cpp`  |
| Service config    | `cfg_<example>.xml`                | `cfg_WaterwaySearch.xml`          |
| AMASE scenario    | `Scenario_<name>.xml`              | `Scenario_WaterwaySearch.xml`     |
| Message files     | `<ID>_<Type>_<Desc>.xml`           | `01_AirVehicleConfig_UAV.xml`     |
| Example config    | `config.yaml`                      | (in each example directory)       |
| Anod spec         | `<library>.anod`                   | `zeromq.anod`                     |
| Test script       | `test.py`                          | (in each test directory)          |

## Environment Variables

Key variables defined in `infrastructure/paths.sh`:

| Variable         | Path                    | Description               |
|------------------|-------------------------|---------------------------|
| `OPENUXAS_ROOT`  | Repository root         | Project base directory    |
| `SRC_DIR`        | `src/`                  | Source root               |
| `CPP_DIR`        | `src/cpp/`              | C++ source                |
| `ADA_DIR`        | `src/ada/`              | Ada source                |
| `OBJ_DIR`        | `obj/`                  | Build artifacts           |
| `TESTS_DIR`      | `tests/`                | Test root                 |
| `EXAMPLES_DIR`   | `examples/`             | Examples directory        |
| `UXAS_BIN`       | `obj/cpp/uxas`          | Compiled C++ binary       |
| `UXAS_ADA_BIN`   | `uxas-ada`              | Compiled Ada binary       |
| `SBX_DIR`        | `infrastructure/sbx/`   | Anod sandbox              |
| `SPEC_DIR`       | `infrastructure/specs/` | Anod build specs          |

## Command-Line Arguments

```bash
./obj/cpp/uxas -cfgPath <path_to_config.xml>    # Run with config
./obj/cpp/uxas -runUntil <seconds>               # Run for duration
./obj/cpp/uxas -version                          # Print version info
```

## Common Gotchas

- **Generated LMCP code is gitignored**: Run `./anod build uxas-lmcp` after fresh clone before building
- **C++17 required**: System Boost >= 1.74 needs C++14+; Makefile uses `-std=c++17`
- **Boost deprecation warnings**: Suppressed via `-DBOOST_ALLOW_DEPRECATED_HEADERS`
- **PugiXML patched**: Uses custom int64 support patch; don't replace with vanilla pugixml
- **SendMessagesService paths**: Message file paths in XML configs are relative to the `rundir`, not the repo root
- **AMASE requires display**: OpenAMASE GUI needs X11/display; won't work in headless environments
- **Test port allocation**: Tests use dynamic ports starting at 5560+; port conflicts may occur with parallel runs
- **Python venv**: `.vpython/` is auto-created on first script execution; delete and recreate if corrupted
- **Anod sandbox**: `infrastructure/sbx/` contains all built dependencies; `./anod reset` clears it completely

## Code Style Notes

- Services use `m_` prefix for member variables (e.g., `m_serviceId`, `m_entityConfigurations`)
- LMCP types use full qualified names: `afrl::cmasi::AirVehicleState`
- Log macros: `UXAS_LOG_INFORM()`, `UXAS_LOG_WARN()`, `UXAS_LOG_ERROR()`
- All services are singletons in practice (one instance per type per entity)
- XML configuration is parsed via pugixml (`pugi::xml_node`)
- Shared pointers used extensively for LMCP message objects
