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

## 3. 탭별 기능 설명 및 사용 예시

### 3.1 Dashboard (대시보드)

메인 화면으로, 시스템 상태를 한눈에 파악할 수 있습니다.

| 항목 | 설명 |
|------|------|
| **Status** | UxAS 실행 상태 표시등 (RUNNING: 녹색 / STOPPED: 빨간색) |
| **Entity ID** | 현재 설정된 엔티티 ID |
| **Services** | 활성 서비스 수 |
| **Quick Start** | 드롭다운에서 예제 선택 후 즉시 실행 |
| **Pipeline Overview** | Validator → TaskMgr → RouteAgg → Planner → B&B → PlanBuilder 서비스 흐름도 |
| **Recent Output** | 최근 콘솔 출력 (150줄, 3초 간격 자동 갱신) |

#### Quick Start 사용 예시

```
1. 드롭다운에서 "01_HelloWorld" 선택
2. [Start] 버튼 클릭
3. Recent Output 콘솔에서 메시지 확인:
   [20:35:41] *** RECEIVED:: Received Id[52] Sent Id[51] Message[Hello from #1] ***
   [20:35:41] *** RECEIVED:: Received Id[51] Sent Id[52] Message[Hello from #2] ***
4. 10초 후 자동 종료, 또는 [Stop] 버튼으로 수동 종료
```

```
1. 드롭다운에서 "02_Example_WaterwaySearch" 선택
2. [Start] 버튼 클릭
3. Recent Output에서 서비스 초기화 확인:
   Successfully launched AutomationRequestValidatorService
   Successfully launched TaskManagerService
   Successfully launched RoutePlannerVisibilityService
   ...
4. AMASE 없이 실행하므로 차량 상태 메시지는 없지만, 서비스 초기화와
   메시지 라우팅이 정상 동작하는지 확인 가능
5. [Stop] 버튼으로 종료
```

### 3.2 Run Control (실행 제어)

UxAS 실행을 세밀하게 제어할 수 있는 탭입니다.

#### 입력 필드

| 항목 | 설명 | 기본값 |
|------|------|--------|
| **Example** | 실행할 예제 드롭다운 | - |
| **Entity ID** | UAV 엔티티 식별자 | 100 |
| **Run Duration (s)** | 실행 제한 시간 (초) | 10 |
| **Config Path** | XML 설정 파일 경로 (직접 지정 시 Example보다 우선) | 자동 감지 |

#### 버튼별 기능

| 버튼 | 동작 | API |
|------|------|-----|
| **Start UxAS** | Example 또는 Config Path로 UxAS 시작. Example만 선택한 경우 자동으로 cfg 파일과 RUNDIR을 찾아 실행 | `POST /api/start` |
| **Stop UxAS** | 실행 중인 UxAS 프로세스 종료 (SIGTERM → 5초 후 SIGKILL) | `POST /api/stop` |
| **Run Custom Config** | Input Config + Algorithm 탭 설정을 바탕으로 XML 파일 자동 생성 후 `custom_runs/` 디렉토리에서 UxAS 실행 | `POST /api/run/custom` |
| **Clear** | 콘솔 출력 지우기 (서버 로그는 유지) | 클라이언트 전용 |
| **Export Log** | 콘솔 출력을 `uxas_log.txt` 파일로 다운로드 | 클라이언트 전용 |

#### Start UxAS 사용 예시

```
1. Example 드롭다운에서 "02_Example_WaterwaySearch" 선택
2. Run Duration을 "15"로 설정
3. [Start UxAS] 클릭
4. 콘솔에서 실행 로그 확인
5. 15초 후 자동 종료
```

#### Run Custom Config 사용 예시

```
1. Input Config 탭에서 차량 2대, LineSearchTask 1개 설정
2. Algorithm 탭에서 서비스 활성화/비활성화
3. Run Control 탭으로 돌아와 [Run Custom Config] 클릭
4. 자동으로:
   - custom_runs/custom_run/MessagesToSend/ 에 차량 XML 생성
   - custom_runs/custom_run/cfg_custom.xml 생성
   - UxAS 실행
5. 콘솔에서 결과 확인
```

### 3.3 Input Config (입력 설정)

차량(UAV)과 임무(Task)를 시각적으로 구성합니다. 페이지 로드 시 차량 1대와 태스크 1개가 기본 추가됩니다.

#### 차량 설정 (AirVehicleConfiguration)

**[+ Add Vehicle]** 버튼으로 차량을 추가합니다. 각 차량 카드의 **[X]** 버튼으로 삭제합니다.

| 항목 | 설명 | 기본값 | 참고 |
|------|------|--------|------|
| **ID** | 차량 고유 식별자 | 400, 500, ... (100씩 증가) | AutomationRequest의 EntityList에 포함됨 |
| **Label** | 차량 이름 | UAV400 | 식별용 |
| **Min Speed** | 최소 속도 (m/s) | 18 | 약 65 km/h |
| **Max Speed** | 최대 속도 (m/s) | 33 | 약 119 km/h |
| **Nominal Speed** | 순항 속도 (m/s) | 22 | 약 79 km/h |
| **Altitude** | 비행 고도 (m) | 700 | MSL 기준 |
| **Latitude** | 초기 위도 | 45.3171 | WaterwaySearch 기본 좌표 |
| **Longitude** | 초기 경도 | -120.9724 | WaterwaySearch 기본 좌표 |
| **Heading** | 초기 방향 (도) | 0 | 북쪽 기준 |
| **EnergyRate** | 에너지 소비율 | 0.000278 | 비행 프로파일용 |

#### 임무 설정 (Task)

드롭다운에서 임무 유형 선택 후 **[+ Add Task]** 버튼으로 추가합니다.

| 임무 유형 | 설명 | 좌표 입력 |
|-----------|------|-----------|
| **AreaSearchTask** | 다각형 영역 탐색 | 3개 이상 좌표점 (다각형 꼭짓점) |
| **LineSearchTask** | 경로 따라 탐색 | 2개 이상 좌표점 (경유점) |
| **PointSearchTask** | 단일 지점 탐색 | 위도/경도 1개 |
| **BlockadeTask** | 지역 봉쇄 | 3개 이상 좌표점 |
| **CordonTask** | 지역 격리/경계 | 3개 이상 좌표점 |
| **EscortTask** | 대상 호위 | - |
| **LoiterTask** | 특정 지점 선회 대기 | - |
| **MustFlyTask** | 필수 비행 경로 | - |
| **CommRelayTask** | 통신 중계 | - |
| **OverwatchTask** | 감시/정찰 | - |
| **PatternSearchTask** | 패턴 기반 탐색 | 3개 이상 좌표점 |

AreaSearch, LineSearch 등의 임무는 **[+ Point]** 버튼으로 좌표점을 추가합니다.

#### Zone 설정

- **KeepInZone**: 차량이 반드시 머물러야 하는 비행 허용 영역
- **KeepOutZone**: 차량이 진입 금지인 영역
- 형식: `위도,경도;위도,경도;...` (세미콜론 구분 좌표 쌍)

#### 하단 버튼

| 버튼 | 동작 | 결과 |
|------|------|------|
| **Generate All XML** | 모든 설정을 XML로 변환 | XML Editor 탭으로 이동, Config 미리보기에 생성된 XML 표시 |
| **Validate Config** | 알고리즘 설정 유효성 검사 | Algorithm 탭 하단 콘솔에 "Valid!" 또는 에러/경고 표시 |
| **Generate AutomationRequest** | 차량 ID 및 Task ID로 자동화 요청 XML 생성 | XML Editor의 Request 미리보기에 표시 |

#### Input Config 사용 예시: 2대 UAV 라인 탐색

```
1. 기본 차량(ID: 400)의 좌표를 확인 (45.3171, -120.9724)
2. [+ Add Vehicle] 클릭하여 2번째 차량 추가 (ID: 500 자동 부여)
   - Latitude: 45.3300, Longitude: -120.9500 으로 변경
3. Task Type 드롭다운에서 "LineSearchTask" 선택 → [+ Add Task]
4. Task의 Points에 경유점 추가:
   - Point 1: Lat 45.32, Lng -120.97
   - Point 2: Lat 45.33, Lng -120.96
   - Point 3: Lat 45.34, Lng -120.95
5. [Generate All XML] 클릭 → XML Editor에서 생성된 config 확인
6. [Generate AutomationRequest] 클릭 → Request 탭에서 확인:
   <AutomationRequest Series="CMASI">
     <EntityList><int64>400</int64><int64>500</int64></EntityList>
     <TaskList><int64>1</int64></TaskList>
   </AutomationRequest>
```

### 3.4 Algorithm (알고리즘 설정)

자동화 파이프라인의 각 서비스를 개별적으로 활성화/비활성화하고 파라미터를 조정합니다.

#### 서비스 파이프라인

체크박스로 각 서비스를 활성화/비활성화합니다:

```
AutomationRequest (입력)
  → [v] AutomationRequestValidatorService  ← 요청 유효성 검증
  → [v] TaskManagerService                 ← 작업 계획 옵션 생성
  → [v] RoutePlannerVisibilityService      ← 가시성 그래프 기반 경로 계산
  → [v] RouteAggregatorService             ← 경로 요청 집계
  → [v] AssignmentTreeBranchBoundService   ← Branch & Bound 최적 할당
  → [v] PlanBuilderService                 ← 최종 미션 계획 조립
  → [v] SensorManagerService               ← 센서 발자국 계산
  → [v] BatchSummaryService                ← 배치 처리 조율
  → MissionCommand (출력)
```

#### 주요 파라미터

| 서비스 | 파라미터 | 설명 | 기본값 |
|--------|----------|------|--------|
| **ARV** | MaxResponseTime_ms | 자동화 응답 대기 시간 | 5000 |
| **RoutePlanner** | TurnRadiusOffset_m | 선회 반경 오프셋 | 0 |
| **RoutePlanner** | MinWaypointSeparation_m | 최소 경유점 간격 | 50 |
| **B&B** | NumberNodesMaximum | 최대 탐색 노드 (0=무제한) | 0 |
| **B&B** | CostFunction | MINMAX (최대 비용 최소화) 또는 CUMULATIVE (총 비용 최소화) | MINMAX |
| **PlanBuilder** | AssignmentStartPointLead_m | 할당 시작점 리드 거리 | 0 |

**MINMAX vs CUMULATIVE:**
- MINMAX: 가장 비용이 높은 차량의 비용을 최소화 (모든 차량이 비슷한 시간에 완료)
- CUMULATIVE: 전체 비용 합계를 최소화 (한 차량에 작업이 집중될 수 있음)

#### WaypointPlanManager 설정

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| WaypointsToServe | 한 번에 차량에 전송할 경유점 수 | 15 |
| WaypointsOverlap | 다음 세그먼트와 겹치는 경유점 수 | 5 |
| LoiterRadius_m | 마지막 경유점 도달 시 선회 반경 | 250 |
| TurnType | FlyOver (직선 통과) / TurnShort (최단 선회) | FlyOver |
| GimbalPayloadId | 짐벌 페이로드 센서 ID | 1 |

#### Validation (검증) 버튼

**[Validate Configuration]** 클릭 시 하단 콘솔에 결과 표시:

```
# 성공 시 (녹색):
Valid!

# 경고 시:
Valid!

Warnings:
Automation pipeline incomplete. Missing: AutomationRequestValidatorService

# 오류 시 (빨간색):
Errors:
EntityID must be a positive integer
CostFunction must be MINMAX or CUMULATIVE, got 'INVALID'
WaypointPlanManagerService requires VehicleID
```

### 3.5 Results (결과 분석)

실행 결과를 조회하고 분석하는 탭입니다.

#### 사용 방법

```
1. 상단 드롭다운에서 실행한 예제 선택 (예: "02_Example_WaterwaySearch")
2. [Load] 버튼 클릭
3. 토스트 메시지 표시: "Loaded 1 DBs, 3 XMLs"
```

#### 3개 하위 탭

| 하위 탭 | 내용 |
|---------|------|
| **Messages** | 실행 결과 파일 목록 (XML, Log, DB). 각 파일의 [View] 버튼으로 XML Editor에서 열기 |
| **Database** | SQLite 로그 DB 테이블 조회. 테이블 선택 후 칼럼/데이터 표시 |
| **Summary** | 할당(Assignment: Vehicle-Task-Cost) 및 경유점(Waypoint: ID-Lat-Lng-Alt-Speed) 요약 |

#### Messages 탭 출력 예시

```
| Time | Type | File                                          | Action     |
|------|------|-----------------------------------------------|------------|
| -    | DB   | RUNDIR_WaterwaySearch/datawork/.../log.db3     | (Database) |
| -    | XML  | RUNDIR_WaterwaySearch/datawork/.../msg_001.xml | [View]     |
| -    | Log  | RUNDIR_WaterwaySearch/log/log_1_17754...       | [View]     |
```

#### Database 탭 사용

```
1. Messages 탭에서 DB 파일이 로드되면, Database 탭의 드롭다운에 테이블 목록 표시
2. 테이블 선택 (예: "msg_log")
3. 해당 테이블의 칼럼명과 행 데이터가 테이블로 표시
4. 주요 테이블:
   - msg_log: 메시지 송수신 기록
   - ServiceStatus: 서비스 상태 변경 이력
```

#### CSV 내보내기

**[Export CSV]** 버튼으로 Messages 탭의 내용을 `uxas_output.csv` 파일로 다운로드합니다.

### 3.6 XML Editor (XML 편집기)

XML 설정 파일을 직접 편집하고 실행할 수 있는 탭입니다.

#### 상단 도구 모음

| 버튼 | 동작 | 설명 |
|------|------|------|
| **Load** | 드롭다운 선택 파일 로드 | 파일 내용이 편집기에 표시 |
| **Save** | 편집 내용 디스크에 저장 | `POST /api/save` 호출 |
| **Apply & Run** | 저장 후 즉시 UxAS 실행 | Save → Start 순차 실행 |
| **Validate** | XML 문법 검사 | DOMParser로 클라이언트 측 검증 |

**Validate 결과:**
- 유효: 녹색 배경에 `Valid XML: <UxAS>` 표시
- 오류: 빨간색 배경에 파싱 에러 메시지

#### Generated Preview (생성 미리보기)

Input Config 탭에서 **[Generate All XML]** 실행 후, 4개 하위 탭에서 생성된 XML 확인:

| 미리보기 탭 | 내용 |
|-------------|------|
| **Config** | `cfg_custom.xml` - 전체 UxAS 설정 (서비스, 브리지 등) |
| **Vehicle** | `AirVehicleConfiguration` XML |
| **Task** | 임무별 XML (LineSearchTask, AreaSearchTask 등) |
| **Request** | `AutomationRequest` XML (차량 목록, 작업 목록) |

**[Generate Full Config]** 버튼: Input Config + Algorithm 설정을 합쳐서 Config 미리보기 갱신

#### XML Editor 사용 예시: 기존 예제 수정 후 실행

```
1. 드롭다운에서 "02_Example_WaterwaySearch/cfg_WaterwaySearch.xml" 선택
2. [Load] 클릭 → 편집기에 XML 표시
3. EntityID를 "100"에서 "200"으로 변경
4. RunDuration_s="10"을 추가
5. [Validate] 클릭 → "Valid XML: <UxAS>" 확인
6. [Apply & Run] 클릭 → 저장 및 실행
7. Run Control 탭에서 콘솔 출력 확인
```

---

## 4. Web UI 전체 워크플로우 예시

### 예시 A: HelloWorld 빠른 실행 (초보자용)

```
[Dashboard 탭]
  1. 좌측 하단에서 "UxAS Binary: found" 확인 (녹색)
  2. Quick Start 드롭다운에서 "01_HelloWorld" 선택
  3. [Start] 클릭
  4. Recent Output에서 확인:
     [HH:MM:SS] *** RECEIVED:: Received Id[52] Sent Id[51] Message[Hello from #1] ***
     [HH:MM:SS] *** RECEIVED:: Received Id[51] Sent Id[52] Message[Hello from #2] ***
  5. 10초 후 자동 종료 또는 [Stop] 클릭
  
  결과: 2개의 HelloWorld 서비스가 메시지를 주고받는 것 확인
```

### 예시 B: 커스텀 2-UAV 라인 탐색 미션

```
[Input Config 탭]
  1. 기본 차량 확인 (ID: 400, Lat: 45.3171, Lng: -120.9724)
  2. [+ Add Vehicle] 클릭
     - ID: 500, Lat: 45.3300, Lng: -120.9500
  3. Task Type "LineSearchTask" 선택 → [+ Add Task]
     - Task ID: 1, Label: RiverSearch
     - [+ Point] x3:
       Point 1: 45.32, -120.97
       Point 2: 45.33, -120.96
       Point 3: 45.34, -120.95

[Algorithm 탭]
  4. 모든 서비스 체크 확인 (기본 활성)
  5. CostFunction: MINMAX 확인
  6. [Validate Configuration] → "Valid!" 확인

[Run Control 탭]
  7. Entity ID: 100, Run Duration: 15
  8. [Run Custom Config] 클릭
  9. 토스트: "Custom run started"
  10. 콘솔에서 서비스 초기화 확인:
      Successfully launched AutomationRequestValidatorService
      Successfully launched TaskManagerService
      ...

[Results 탭]
  11. 드롭다운에서 "custom_run" 또는 실행 예제 선택
  12. [Load] 클릭
  13. Messages에서 생성된 XML 파일 확인
  14. Database 탭에서 메시지 로그 테이블 조회
```

### 예시 C: XML 직접 편집 후 실행

```
[XML Editor 탭]
  1. 드롭다운에서 cfg_WaterwaySearch.xml 선택 → [Load]
  2. RunDuration_s="20" 추가
  3. [Validate] → "Valid XML: <UxAS>" 확인
  4. [Apply & Run] 클릭
  5. Run Control 탭 콘솔에서 실행 확인
  6. 20초 후 자동 종료
  
[Results 탭]
  7. "02_Example_WaterwaySearch" 선택 → [Load]
  8. Database 탭에서 테이블 조회
  9. [Export CSV]로 결과 다운로드
```

---

## 5. 명령줄 예제 실행 가이드

Web UI 없이 터미널에서 직접 예제를 실행하는 방법입니다.

### 5.1 환경 설정

```bash
cd /path/to/OpenUxAS
source .vpython/bin/activate
export PATH="$PWD/obj/cpp:$PWD/src/ada:$PATH"
```

### 5.2 예제 목록 확인

```bash
./run-example --list
```

### 5.3 예제별 상세 설명

#### 01_HelloWorld - 기본 메시지 교환

```bash
./run-example 01_HelloWorld
```

- **시나리오**: 2개의 HelloWorld 서비스가 주기적으로 메시지를 교환
- **차량**: 없음 (순수 서비스 테스트)
- **실행 시간**: 10초 (자동 종료)
- **사용 서비스**: HelloWorld x 2 (StringToSend="Hello from #1", "#2")
- **확인 사항**:
  ```
  *** RECEIVED:: Received Id[52] Sent Id[51] Message[Hello from #1] ***
  *** RECEIVED:: Received Id[51] Sent Id[52] Message[Hello from #2] ***
  ```
- **의미**: UxAS 프레임워크의 서비스 간 메시지 라우팅이 정상 동작하는지 기본 검증

#### 02_Example_WaterwaySearch - 수로 탐색 (주요 예제)

```bash
./run-example --no-amase 02_Example_WaterwaySearch
# Ctrl+C로 종료
```

- **시나리오**: Deschutes River(오리건주) 수로를 따라 2대의 UAV가 라인 탐색 수행
- **차량**: 2대 (ID: 400, 500)
  - UAV 400: 위도 45.3171, 경도 -120.9724, 고도 700m, 속도 22m/s
  - UAV 500: 위도 45.3391, 경도 -121.0067, 고도 700m, 속도 26m/s
- **작업**: LineSearchTask 1개 (강줄기를 따라 95개 경유점)
- **서비스 파이프라인**: ARV → TaskMgr → RoutePlanner → RouteAgg → B&B → PlanBuilder
- **메시지 발송 순서** (시간순):
  1. AirVehicleConfiguration x 2 (100ms, 200ms)
  2. AirVehicleState x 2 (400ms, 600ms)
  3. LineSearchTask (1000ms)
  4. OperatingRegion + KeepInZone (1100ms)
  5. AutomationRequest (5000ms) → 파이프라인 시작
- **확인 사항**:
  - `RUNDIR_WaterwaySearch/datawork/` 디렉토리 생성
  - `SavedMessages/` 에 LMCP 메시지 파일들
  - 서비스 초기화 성공 메시지 (콘솔)
- **AMASE와 함께 실행 시**: UAV가 강줄기를 따라 탐색하는 경로 시각화 가능

#### 02a_Ada_WaterwaySearch - Ada/C++ 혼합 수로 탐색

```bash
./run-example --no-amase 02a_Ada_WaterwaySearch
```

- **시나리오**: 위와 동일하지만, C++ 대신 Ada(SPARK) 구현체 사용
- **차량**: 2대 (ID: 400, 500)
- **특징**: `uxas-ada` 바이너리로 실행. ARV(자동화 요청 검증) 서비스가 Ada로 구현됨
- **확인 사항**:
  ```
  Found bridge addressPUB: "tcp://127.0.0.1:5560"
  Found bridge addressPULL: "tcp://127.0.0.1:5561"
  Successfully launched AutomationRequestValidatorService
  Initialization complete
  ```
- **의미**: 형식 검증(formally verified)된 Ada 서비스가 C++ 서비스와 동일한 결과를 생성하는지 검증

#### 02b_Double_WaterwaySearch - 이중 인스턴스 수로 탐색

```bash
./run-example --no-amase 02b_Double_WaterwaySearch
```

- **시나리오**: 2개의 독립적인 UxAS 인스턴스가 동시에 실행
- **구성**: `cfg_cpp_one.xml` + `cfg_cpp_two.xml`
- **차량**: 각 인스턴스마다 2대 (총 4대)
- **확인 사항**: 각 인스턴스가 독립적으로 미션 계획 생성
- **의미**: 다중 UxAS 인스턴스 간 독립적 계획 수립 능력 검증

#### 02c_Ada_ARV_RA_WaterwaySearch - Ada ARV/RA 검증

```bash
./run-example --no-amase 02c_Ada_ARV_RA_WaterwaySearch
```

- **시나리오**: WaterwaySearch + Ada 구현의 AutomationRequestValidator와 RouteAggregator 서비스 검증
- **확인 사항**: ARV와 RA가 Ada로 구현된 상태에서도 정상 메시지 처리

#### 02d_Ada_WPM_WaterwaySearch - Ada WPM 검증

```bash
./run-example --no-amase 02d_Ada_WPM_WaterwaySearch
```

- **시나리오**: WaterwaySearch + Ada 구현의 WaypointPlanManager 서비스 검증
- **확인 사항**: 경유점 계획 관리가 Ada 구현에서도 정상 동작

#### 03_Example_DistributedCooperation - 분산 협력

```bash
./run-example --no-amase 03_Example_DistributedCooperation
```

- **시나리오**: 2대의 UAV가 네트워크를 통해 분산 협력하여 작업 할당
- **차량**: 2대 (ID: 1000, 2000), 각각 별도 UxAS 인스턴스에서 실행
- **작업**: AreaSearchTask 1개 + AngledAreaSearchTask 1개 + LineSearchTask 2개 + ImpactLineSearchTask 1개 (총 5개)
- **핵심 기술**:
  - ZeroMQ Zyre Bridge로 P2P 통신
  - AssignmentCoordination 메시지 교환
  - "중앙 알고리즘, 분산 구현" - 각 인스턴스가 전체 할당을 계산하되 자신의 할당만 실행
- **확인 사항**:
  - 2개 콘솔에서 동시에 서비스 초기화
  - `UAV_1000/datawork/AutomationDiagramDataService/` 에 플롯 데이터 생성
  - TaskAutomationRequest 발송 및 할당 결과 메시지
- **의미**: 통신 링크가 있는 다중 플랫폼 간 분산 의사결정 능력 검증

#### 04_Ada_SparkGoldWPM - SPARK Gold WaypointPlanManager

```bash
./run-example --no-amase 04_Ada_SparkGoldWPM
```

- **시나리오**: SPARK/Ada Gold 레벨로 형식 검증된 WaypointPlanManager의 엣지 케이스 테스트
- **차량**: 2대 (ID: 400, 500)
- **테스트 케이스**:
  - 중복 ID 경유점 → 무시
  - 순서 어긋난 경유점 → 정렬
  - 사이클 포함 경유점 → 탐지/처리
  - 참조되지 않은 경유점 → 무시
- **확인 사항**:
  - UAV 400이 15개 경유점 세그먼트를 따라 비행
  - 마지막 5개 경유점 도달 시 다음 세그먼트 자동 로드 (5개 중복)
- **의미**: 형식 검증된 코드의 안전성/정확성 확인

#### 05_AssignTasks - 복합 작업 할당

```bash
./run-example --no-amase 05_AssignTasks
```

- **시나리오**: 다양한 작업 유형을 2대의 UAV에 최적 할당
- **차량**: 2대 (ID: 1, 2)
- **작업**: 6개
  - PointSearchTask x 2 (특정 지점 탐색)
  - LineSearchTask x 2 (경로 탐색)
  - AreaSearchTask x 2 (영역 탐색)
- **보안 영역**: KeepInZone (비행 허용), KeepOutZone (비행 금지), OperatingRegion
- **서비스**: ARV (MaxResponseTime: 10초), SensorManager, WPM (512개 경유점 버퍼)
- **확인 사항**:
  - 6개 작업 모두에 대한 AssignmentCostMatrix 메시지 생성
  - 각 작업-차량 조합의 비용(Cost) 계산 결과
  - 경로가 KeepOutZone을 회피하는지 확인
  - `datawork/` 에 RoutePlanner 메시지 저장
- **의미**: B&B 알고리즘이 다양한 작업 유형과 제약 조건을 올바르게 처리하는지 검증

#### 05a_Ada_AssignTasks - Ada 복합 작업 할당

```bash
./run-example --no-amase 05a_Ada_AssignTasks
```

- **시나리오**: 위와 동일 (Ada + C++ 혼합)
- **의미**: Ada 서비스가 복합 작업 할당에서도 동일한 결과 생성 확인

#### 06_AutomationDiagram - 자동화 다이어그램

```bash
./run-example --no-amase 06_AutomationDiagram
```

- **시나리오**: 6대의 UAV + 복합 작업으로 자동화 과정 시각화 데이터 생성
- **차량**: 6대 (ID: 1~6) + 지상 객체 2개
- **작업**: AreaSearchTask 3개 + LineSearchTask 2개
- **보안 영역**: KeepInZone 3개 + KeepOutZone 3개 + OperatingRegion 1개
- **핵심 서비스**: AutomationDiagramDataService (할당 과정 그래프 데이터 생성)
- **확인 사항**:
  - `datawork/AutomationDiagramDataService/` 디렉토리에 플롯 데이터
  - MessageLoggerDataService에 전체 메시지 기록
- **의미**: 대규모 시나리오에서 자동화 파이프라인의 전체 흐름 시각화

#### 08_ExampleSparkService - SPARK 서비스 예제

```bash
./run-example --no-amase 08_ExampleSparkService
```

- **시나리오**: WaterwaySearch 설정 + 사용자 정의 SPARK 서비스 통합 예제
- **확인 사항**: WaterwaySearch와 동일 + SPARK 서비스 통합 정상 동작

#### 99_Tasks/* - 개별 작업 유형 테스트

```bash
./run-example --no-amase 99_Tasks/CmasiAreaSearchTask/Polygon
./run-example --no-amase 99_Tasks/CmasiLineSearchTask
./run-example --no-amase 99_Tasks/BlockadeTask
# ... 등
```

각 작업 유형에 대한 독립적인 테스트:

| 작업 | 설명 | UAV 수 |
|------|------|--------|
| CmasiAreaSearchTask (Circle/Polygon/Rectangle) | CMASI 영역 탐색 (원형/다각형/직사각형) | 2~4 |
| CmasiLineSearchTask | CMASI 라인 탐색 | 2 |
| CmasiPointSearchTask | CMASI 지점 탐색 | 2 |
| AngledAreaSearchTask | 각도 지정 영역 탐색 (IMPACT) | 2 |
| BlockadeTask | 지역 봉쇄 | 2 |
| CommRelayTask | 통신 중계 | 3+ |
| CordonTask | 지역 격리/경계 설정 | 3+ |
| EscortTask | 대상 호위 | 2 |
| ImpactLineSearchTask | IMPACT 라인 탐색 | 2 |
| ImpactPointSearchTask | IMPACT 지점 탐색 | 2 |
| LoiterTask | 특정 지점 선회 대기 | 2 |
| MultiVehicleWatchTask | 다중 차량 감시 | 3+ |
| MustFlyTask | 필수 비행 경로 | 2 |
| PatternSearchTask | 패턴 기반 탐색 | 2 |
| RendezvousTask | 집결점 합류 | 2 |
| WatchTask | 단일 차량 감시 | 2 |

### 5.4 실행 결과 확인 방법

모든 예제 실행 후 `RUNDIR_*/` 디렉토리에 결과가 생성됩니다:

```
RUNDIR_예제이름/
├── datawork/
│   ├── AutomationDiagramDataService/  # 자동화 다이어그램 (해당 시)
│   └── SavedMessages/                 # 송수신한 LMCP 메시지 (XML)
│       ├── 0001_*.xml
│       ├── 0002_*.xml
│       └── ...
└── log/
    └── log_1_<timestamp>/
        └── log.db3                    # SQLite 메시지 로그 데이터베이스
```

#### SQLite DB 조회 (명령줄)

```bash
sqlite3 RUNDIR_*/log/log_1_*/log.db3
> .tables                    # 테이블 목록
> SELECT * FROM msg LIMIT 5; # 메시지 확인
> .quit
```

#### Web UI로 결과 확인

```
1. Results 탭 → 예제 선택 → [Load]
2. Messages 탭에서 파일 목록 확인
3. Database 탭에서 테이블 선택 → 데이터 조회
4. [Export CSV]로 내보내기
```

---

## 6. 참고: AMASE 연동

일부 예제(02, 03, 05, 06 시리즈)는 OpenAMASE GUI 시뮬레이터와 연동하도록 설계되었습니다.

- **AMASE 역할**: 차량 상태(AirVehicleState) 생성, 경로 시각화, 시뮬레이션 시간 관리
- **AMASE 없이 실행**: `--no-amase` 플래그 사용. 서비스 초기화와 메시지 라우팅은 확인 가능하지만, 차량 상태 업데이트가 없어 완전한 파이프라인 동작은 불가
- **AMASE 필요 시**: X11 디스플레이 환경 필요 (headless 서버에서는 실행 불가)

---

## 7. 문제 해결

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| "UxAS binary not found" | 바이너리 미빌드 | `make -j all` 실행 |
| "Address already in use" | 포트 충돌 | `pkill uxas` 후 재시작, 또는 다른 포트 사용 |
| 예제 목록이 비어있음 | examples 디렉토리 부재 | 저장소 전체 클론 확인 |
| DB 테이블 조회 실패 | 실행 기록 없음 | UxAS를 한번 실행한 후 결과 확인 |
| "AMASE not found" | OpenAMASE 미설치 | `--no-amase` 플래그 사용 |
| Ada 예제 실패 | Ada 바이너리 없음 | `src/ada/uxas-ada` 빌드 필요 |
| Config 생성 오류 | 필수 필드 누락 | Entity ID가 숫자인지 확인 |
| `run-example` 실행 불가 | venv 미생성 | `source .vpython/bin/activate` 후 실행 |

---

## 8. 파일 구성

| 파일 | 설명 |
|------|------|
| `uxas_ui_server.py` | Python 백엔드 서버 (~550줄) |
| `uxas_ui.html` | 프론트엔드 HTML/CSS/JS 통합 (~580줄) |
| `WebUI_Guide_Korean.md` | 본 문서 |
| `run-example` | 명령줄 예제 실행 스크립트 |
| `infrastructure/run_example.py` | 예제 실행 Python 구현 |
| `examples/` | 15+ 예제 디렉토리 |
