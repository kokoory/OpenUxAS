# OpenUxAS Web UI 사용 설명서

## 1. 개요

OpenUxAS Web UI는 브라우저 기반 제어판으로, 명령줄 없이 OpenUxAS를 설정, 실행, 분석할 수 있는 도구입니다.

### 주요 특징

- **외부 의존성 없음**: Python 표준 라이브러리만 사용
- **단일 HTML 파일**: 빌드 과정 없이 바로 사용 가능
- **6개 탭 구성**: Dashboard, Run Control, Input Config, Algorithm, Results, XML Editor
- **실시간 모니터링**: UxAS 프로세스 출력을 실시간으로 확인

### 시스템 요구사항

- Python 3.6 이상
- 웹 브라우저 (Chrome, Firefox, Edge 등)
- OpenUxAS 빌드 완료 (`obj/cpp/uxas` 바이너리 필요)

---

## 2. 서버 실행

### 기본 실행

```bash
python3 uxas_ui_server.py
```

기본 포트 8080에서 서버가 시작됩니다.

### 포트 지정

```bash
python3 uxas_ui_server.py 9000          # 포트 번호 직접 입력
python3 uxas_ui_server.py --port 9000   # --port 옵션 사용
```

### 접속

브라우저에서 `http://localhost:8080` 을 열면 제어판이 표시됩니다.

서버 시작 시 다음 정보가 출력됩니다:

```
============================================================
  OpenUxAS Web UI Server
  http://localhost:8080
  UxAS Binary: /path/to/OpenUxAS/obj/cpp/uxas
  Examples: /path/to/OpenUxAS/examples
============================================================
```

### 종료

터미널에서 `Ctrl+C`를 누르면 서버가 종료됩니다. 실행 중인 UxAS 프로세스도 함께 종료됩니다.

---

## 3. 탭별 기능 설명

### 3.1 Dashboard (대시보드)

메인 화면으로, 시스템 상태를 한눈에 파악할 수 있습니다.

| 항목 | 설명 |
|------|------|
| **Status** | UxAS 실행 상태 (RUNNING / STOPPED) |
| **Entity ID** | 현재 설정된 엔티티 ID |
| **Services** | 활성 서비스 수 |
| **Quick Start** | 예제 선택 후 즉시 실행 |
| **Pipeline Overview** | 자동화 파이프라인 서비스 흐름도 |
| **Recent Output** | 최근 콘솔 출력 (150줄) |

#### Quick Start 사용법

1. 드롭다운에서 예제 선택 (예: `02_Example_WaterwaySearch`)
2. **Start** 버튼 클릭
3. 콘솔 출력에서 실행 상태 확인
4. 종료 시 **Stop** 버튼 클릭

### 3.2 Run Control (실행 제어)

UxAS 실행을 세밀하게 제어할 수 있는 탭입니다.

#### 설정 항목

| 항목 | 설명 | 기본값 |
|------|------|--------|
| **Example** | 실행할 예제 디렉토리 | - |
| **Entity ID** | UAV 엔티티 식별자 | 100 |
| **Run Duration (s)** | 실행 제한 시간 (초) | 10 |
| **Config Path** | XML 설정 파일 경로 (직접 지정) | 자동 감지 |

#### 버튼 기능

- **Start UxAS**: 선택한 예제 또는 설정 파일로 UxAS 시작
- **Stop UxAS**: 실행 중인 UxAS 프로세스 종료
- **Run Custom Config**: Input Config/Algorithm 탭에서 설정한 내용으로 실행
- **Clear**: 콘솔 출력 지우기
- **Export Log**: 콘솔 출력을 텍스트 파일로 저장

### 3.3 Input Config (입력 설정)

차량(UAV)과 임무(Task)를 시각적으로 구성합니다.

#### 차량 설정 (AirVehicleConfiguration)

**+ Add Vehicle** 버튼으로 차량을 추가합니다. 각 차량의 설정:

| 항목 | 설명 | 기본값 |
|------|------|--------|
| **ID** | 차량 고유 식별자 | 400, 500, ... |
| **Label** | 차량 이름 | UAV400 |
| **Min Speed** | 최소 속도 (m/s) | 18 |
| **Max Speed** | 최대 속도 (m/s) | 33 |
| **Nominal Speed** | 순항 속도 (m/s) | 22 |
| **Altitude** | 비행 고도 (m) | 700 |
| **Latitude** | 초기 위도 | 45.3171 |
| **Longitude** | 초기 경도 | -120.9724 |
| **Heading** | 초기 방향 (도) | 0 |
| **EnergyRate** | 에너지 소비율 | 0.000278 |

#### 임무 설정 (Task)

지원하는 임무 유형:

| 임무 유형 | 설명 |
|-----------|------|
| **AreaSearchTask** | 영역 탐색 (다각형 영역) |
| **LineSearchTask** | 경로 탐색 (경유점 연결) |
| **PointSearchTask** | 지점 탐색 (단일 좌표) |
| **BlockadeTask** | 차단 임무 |
| **CordonTask** | 경계 설정 임무 |
| **EscortTask** | 호위 임무 |
| **LoiterTask** | 선회 대기 임무 |
| **MustFlyTask** | 필수 비행 경로 |
| **CommRelayTask** | 통신 중계 |
| **OverwatchTask** | 감시 임무 |
| **PatternSearchTask** | 패턴 탐색 |

각 임무에는 Task ID, Label, 적격 엔티티, GSD(지상 샘플 거리) 등을 설정할 수 있습니다. AreaSearch/LineSearch 등의 임무는 좌표점(Points)을 추가하여 탐색 영역을 정의합니다.

#### Zone 설정

- **KeepInZone**: 비행 허용 영역 (위도,경도 쌍으로 다각형 정의)
- **KeepOutZone**: 비행 금지 영역

#### 하단 버튼

- **Generate All XML**: 모든 설정을 XML로 변환하여 XML Editor 탭에 표시
- **Validate Config**: 설정 유효성 검사
- **Generate AutomationRequest**: 자동화 요청 XML 생성

### 3.4 Algorithm (알고리즘 설정)

자동화 파이프라인의 각 서비스를 개별적으로 활성화/비활성화하고 파라미터를 조정합니다.

#### 서비스 파이프라인

```
AutomationRequest
  → AutomationRequestValidatorService (검증)
  → TaskManagerService (임무 계획)
  → RouteAggregatorService (경로 요청 집계)
  → RoutePlannerVisibilityService (경로 계산)
  → AssignmentTreeBranchBoundService (최적 할당)
  → PlanBuilderService (계획 조립)
  → MissionCommand (차량 명령)
```

#### 주요 파라미터

| 서비스 | 파라미터 | 설명 |
|--------|----------|------|
| **ARV** | MaxResponseTime_ms | 응답 대기 시간 (ms) |
| **RoutePlanner** | TurnRadiusOffset_m | 선회 반경 오프셋 |
| **RoutePlanner** | MinWaypointSeparation_m | 최소 경유점 간격 |
| **B&B** | NumberNodesMaximum | 최대 탐색 노드 수 (0=무제한) |
| **B&B** | CostFunction | 비용 함수 (MINMAX / CUMULATIVE) |
| **PlanBuilder** | AssignmentStartPointLead_m | 할당 시작점 리드 거리 |

#### WaypointPlanManager 설정

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| WaypointsToServe | 전송할 경유점 수 | 15 |
| WaypointsOverlap | 중복 경유점 수 | 5 |
| LoiterRadius_m | 선회 반경 (m) | 250 |
| TurnType | 선회 방식 (FlyOver / TurnShort) | FlyOver |
| GimbalPayloadId | 짐벌 페이로드 ID | 1 |

#### Validation (검증)

**Validate Configuration** 버튼을 클릭하면:
- 필수 서비스 누락 여부 확인
- CostFunction 값 유효성 검사
- WaypointPlanManager의 VehicleID 설정 확인
- 중복 서비스 경고

### 3.5 Results (결과 분석)

실행 결과를 조회하고 분석하는 탭입니다.

#### 사용 방법

1. 드롭다운에서 실행 결과가 있는 예제 선택
2. **Load** 버튼 클릭
3. 3개 하위 탭에서 결과 확인:

| 하위 탭 | 내용 |
|---------|------|
| **Messages** | 출력 파일 목록 (XML, Log, DB). **View** 버튼으로 XML Editor에서 열기 |
| **Database** | SQLite 로그 DB 테이블 조회. 테이블 선택 후 데이터 열람 |
| **Summary** | 할당(Assignment) 및 경유점(Waypoint) 요약 테이블 |

#### CSV 내보내기

**Export CSV** 버튼으로 Messages 탭의 내용을 CSV 파일로 다운로드합니다.

### 3.6 XML Editor (XML 편집기)

XML 설정 파일을 직접 편집하고 실행할 수 있는 탭입니다.

#### 기능

| 버튼 | 설명 |
|------|------|
| **Load** | 선택한 파일을 편집기에 불러오기 |
| **Save** | 편집한 내용을 파일에 저장 |
| **Apply & Run** | 저장 후 즉시 UxAS 실행 |
| **Validate** | XML 문법 검사 |

#### Generated Preview (생성 미리보기)

Input Config 탭에서 **Generate All XML** 실행 후, 4개 하위 탭에서 생성된 XML을 확인:

- **Config**: UxAS 전체 설정 XML
- **Vehicle**: 차량 설정 XML
- **Task**: 임무 설정 XML
- **Request**: AutomationRequest XML

---

## 4. API 레퍼런스

### GET 엔드포인트

| 엔드포인트 | 설명 | 파라미터 |
|------------|------|----------|
| `GET /api/examples` | 사용 가능한 예제 목록 | 없음 |
| `GET /api/status` | UxAS 실행 상태 | 없음 |
| `GET /api/output` | 콘솔 출력 버퍼 (최근 200줄) | 없음 |
| `GET /api/config?path=` | XML 설정 파일 파싱 | `path`: 파일 경로 |
| `GET /api/messages?example=` | 예제의 메시지 파일 목록 | `example`: 예제 경로 |
| `GET /api/outputs?path=` | 실행 결과 파일 목록 | `path`: 예제/실행 경로 |
| `GET /api/logdb?path=&table=` | SQLite DB 테이블 조회 | `path`: DB 경로, `table`: 테이블명 |
| `GET /api/file?path=` | 파일 내용 읽기 | `path`: 파일 경로 |

### POST 엔드포인트

| 엔드포인트 | 설명 | 요청 본문 |
|------------|------|-----------|
| `POST /api/start` | UxAS 시작 | `{configPath, example, runDir}` |
| `POST /api/stop` | UxAS 중지 | `{}` |
| `POST /api/validate` | 설정 검증 | `{entityId, services:[{type, attributes}]}` |
| `POST /api/generate/config` | 설정 XML 생성 | `{entityId, runDuration, services/algorithm}` |
| `POST /api/generate/vehicle` | 차량 XML 생성 | `{ID, Label, MinimumSpeed, ...}` |
| `POST /api/generate/state` | 차량 상태 XML 생성 | `{ID, Latitude, Longitude, ...}` |
| `POST /api/generate/task` | 임무 XML 생성 | `{taskType, taskId, points, ...}` |
| `POST /api/generate/request` | 자동화 요청 XML 생성 | `{entities:[], tasks:[]}` |
| `POST /api/run/example` | 예제 실행 | `{name}` |
| `POST /api/run/custom` | 커스텀 설정으로 실행 | `{config, vehicles, states, tasks, request}` |
| `POST /api/save` | 파일 저장 | `{path, content}` |

### 응답 형식

모든 API는 JSON으로 응답합니다.

```json
// 성공 (POST /api/start)
{"status": "started", "cmd": "...", "cwd": "..."}

// 오류
{"error": "설명 메시지"}

// 상태 (GET /api/status)
{"running": false, "binary_exists": true, "binary_path": "..."}
```

---

## 5. 아키텍처

### 전체 구조

```
브라우저 (uxas_ui.html)
    ↕ HTTP (fetch API)
Python 서버 (uxas_ui_server.py)
    ↕ subprocess
UxAS 바이너리 (obj/cpp/uxas)
```

### 백엔드 구성요소

| 구성요소 | 설명 |
|----------|------|
| `ReusableTCPServer` | SO_REUSEADDR 활성화된 TCP 서버 |
| `UxASHandler` | HTTP 요청 처리 (GET/POST 라우팅) |
| `start_uxas()` | UxAS 프로세스 시작 (별도 스레드) |
| `stop_uxas()` | UxAS 프로세스 종료 |
| `generate_xml_config()` | UI 설정 → XML 변환 |
| `_build_services_from_ui_config()` | Algorithm 탭 설정 → 서비스 리스트 변환 |
| `validate_config()` | 설정 유효성 검사 |
| `read_log_table()` | SQLite DB 테이블별 조회 |

### 프론트엔드 구성요소

| 함수 | 설명 |
|------|------|
| `api()` | 서버 API 호출 (GET/POST) |
| `buildConfig()` | 모든 탭 설정을 하나의 객체로 수집 |
| `getVehicles()` | 차량 설정 DOM에서 데이터 추출 |
| `getTasks()` | 임무 설정 DOM에서 데이터 추출 |
| `checkStatus()` | 3초 간격 상태 폴링 |
| `switchTab()` | 탭 전환 |

---

## 6. 사용 예시

### 예시 1: HelloWorld 실행

1. Dashboard 탭에서 `01_HelloWorld` 선택
2. **Start** 클릭
3. 콘솔에서 "Hello" 메시지 교환 확인
4. 약 10초 후 자동 종료

### 예시 2: 커스텀 다중 UAV 임무

1. **Input Config** 탭으로 이동
2. **+ Add Vehicle** 로 UAV 2대 추가 (ID: 400, 500)
3. 각 차량의 위도/경도를 다르게 설정
4. **LineSearchTask** 선택 후 **+ Add Task**
5. 탐색 경로의 좌표점 3개 이상 추가
6. **Algorithm** 탭에서 CostFunction을 `MINMAX`로 설정
7. **Run Control** 탭에서 **Run Custom Config** 클릭
8. **Results** 탭에서 실행 결과 확인

### 예시 3: XML 직접 편집

1. **XML Editor** 탭으로 이동
2. 드롭다운에서 `02_Example_WaterwaySearch/cfg_WaterwaySearch.xml` 선택
3. **Load** 클릭하여 내용 불러오기
4. XML을 편집 (예: EntityID 변경, 서비스 추가)
5. **Validate** 로 문법 확인
6. **Apply & Run** 으로 즉시 실행

---

## 7. 문제 해결

### 자주 발생하는 문제

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| "UxAS binary not found" | 바이너리 미빌드 | `make -j all` 실행 |
| "Address already in use" | 포트 충돌 | 다른 포트 사용 또는 기존 프로세스 종료 |
| 예제 목록이 비어있음 | examples 디렉토리 부재 | 저장소 전체 클론 확인 |
| DB 테이블 조회 실패 | 실행 기록 없음 | UxAS를 한번 실행한 후 결과 확인 |
| Config 생성 오류 | 필수 필드 누락 | Entity ID가 숫자인지 확인 |
| AMASE 연동 불가 | 디스플레이 없음 | X11 환경 필요 (headless에서는 불가) |

### 로그 확인

서버는 HTTP 로그를 출력하지 않습니다 (`log_message` 비활성화). UxAS 실행 로그는 웹 UI 콘솔 또는 RUNDIR 내 로그 파일에서 확인합니다.

---

## 8. 파일 구성

| 파일 | 크기 | 설명 |
|------|------|------|
| `uxas_ui_server.py` | ~550줄 | Python 백엔드 서버 |
| `uxas_ui.html` | ~580줄 | 프론트엔드 (HTML/CSS/JS 통합) |
| `WebUI_Guide_Korean.md` | 본 문서 | 한글 사용 설명서 |
