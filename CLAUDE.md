# CLAUDE.md - OpenUxAS

## Role

You are a UAV (Unmanned Aerial Vehicle) autonomy systems expert specializing in unmanned systems architecture, mission planning, task allocation, and multi-vehicle coordination. You have deep knowledge of service-oriented architectures for autonomous systems, LMCP messaging protocol, and formal verification with SPARK/Ada.

## Project Overview

OpenUxAS (Unmanned Systems Autonomy Services) is an open-source framework for unmanned system autonomy. It provides a modular, service-based architecture for mission planning, task allocation, route planning, and vehicle coordination. Developed under AFRL (Air Force Research Laboratory), it supports both simulation and real-world UAS operations.

**License**: Air Force Open Source Agreement Version 1.0

## Architecture

### Service-Based Design
OpenUxAS follows a **service-oriented architecture** where independent services communicate via ZeroMQ messaging using LMCP (Lightweight Message Construction Protocol) serialization.

### Key Components

- **Services** (`src/cpp/Services/`): Core autonomy services
  - Task assignment and allocation
  - Route planning and optimization
  - Waypoint management
  - Sensor footprint calculation
  - Vehicle state tracking
  - Automation request handling

- **Tasks** (`src/cpp/Tasks/`): Task type implementations
  - Area search, line search, point search
  - Loiter, patrol
  - Overwatch, escort
  - Impact assessment

- **Communications** (`src/cpp/Communications/`): ZeroMQ-based messaging infrastructure

- **DPSS** (`src/cpp/DPSS/`): Dynamic Priority Search Space algorithms

- **Plans** (`src/cpp/Plans/`): Planning utilities and algorithms

- **Ada/SPARK** (`src/ada/`): Formally verified components using SPARK proof system

- **LMCP** (`mdms/`): Message Data Model Schemas — XML definitions for all message types

### Message Flow
```
Vehicle/GCS -> ZeroMQ -> LMCP Deserialize -> Service -> LMCP Serialize -> ZeroMQ -> Vehicle/GCS
```

## Build & Test

### C++ Build (Makefile)
```bash
# Build using Make
make

# Build with coverage
make GCOV=1
```

### Anod Build System (recommended)
```bash
# Bootstrap the build system
./infrastructure/bootstrap

# Install dependencies
./infrastructure/install

# Build with anod
./anod build uxas

# Run examples
./run-example <example_name>
python3 infrastructure/run_example.py <example_name>
```

### Testing
```bash
# C++ integration tests
cd tests/cpp && ./run-tests

# Run specific test
cd tests/cpp && python3 run-tests.py --test <test_name>

# Ada/SPARK formal proofs
cd tests/proof && python3 run-proofs.py
```

### Python Linting
```bash
# From infrastructure/uxas/
mypy .
flake8
```

## Code Standards

- **C++11** standard for C++ components
- **SPARK/Ada** for formally verified components
- **Python**: mypy + flake8 (config in `infrastructure/uxas/`)
- Follow existing service patterns when adding new services
- All messages must use LMCP serialization

## Key Domain Knowledge

### LMCP (Lightweight Message Construction Protocol)
- XML schema definitions in `mdms/` directory
- Auto-generated C++ serialization code from schemas
- Standard message format for all inter-service communication
- Python bindings available in `tests/cpp/pylmcp/`

### Autonomy Concepts
- **Task Assignment**: Allocating tasks to vehicles based on capabilities and cost
- **Route Planning**: Computing optimal paths considering vehicle dynamics and constraints
- **Operating Region**: Defined areas with keep-in/keep-out zones
- **Automation Request**: High-level mission specifications from operators
- **Waypoint Following**: Low-level vehicle guidance along planned routes

### Service Development Pattern
1. Create service class inheriting from base service
2. Register subscribed LMCP message types
3. Implement message handlers
4. Register published message types
5. Add service to build system

### Multi-Vehicle Coordination
- Cooperative task allocation across heterogeneous vehicles
- Conflict resolution for shared resources/airspace
- Timing constraints and synchronization
- Communication topology management

## Directory Structure

| Path | Purpose |
|------|---------|
| `src/cpp/Services/` | Core autonomy services |
| `src/cpp/Tasks/` | Task type implementations |
| `src/cpp/Communications/` | ZeroMQ messaging layer |
| `src/cpp/DPSS/` | Dynamic priority search algorithms |
| `src/cpp/UxAS_Main.cpp` | Main entry point |
| `src/ada/` | Formally verified Ada/SPARK components |
| `mdms/` | LMCP message schema definitions |
| `examples/` | Example scenarios and configurations |
| `tests/cpp/` | C++ integration tests |
| `tests/proof/` | SPARK formal proofs |
| `infrastructure/` | Build system (anod) and tooling |
| `external_libraries/` | Third-party dependencies |
| `resources/` | Documentation and automation diagrams |

## Dependencies

- **ZeroMQ (zmq)**: Messaging transport
- **Boost**: C++ utilities
- **PugiXML**: XML parsing (LMCP, configurations)
- **SQLite**: Local data storage
- **zyre**: Distributed peer discovery
- **GNAT/GNATprove**: Ada/SPARK compiler and prover
