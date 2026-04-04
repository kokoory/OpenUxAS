# OpenUxAS 분석 및 실행 가이드

이 문서는 OpenUxAS 프로젝트의 현재 상태 분석 결과와 "UxAS binary missing" 오류 해결을 위한 가이드를 포함합니다.

## 1. 현상 분석
- **오류 내용:** `run-example` 실행 시 UxAS 바이너리를 찾을 수 없음.
- **원인:** 
    - 프로젝트 루트에 빌드 결과물인 `obj/` 디렉토리가 존재하지 않음 (빌드 미수행).
    - 현재 운영체제가 **Windows**이나, 프로젝트는 **Linux(Ubuntu)** 기반의 빌드 환경을 요구함.
    - `Makefile`은 `obj/cpp/uxas`에 바이너리를 생성하려 하지만, `paths.py`는 `cpp/uxas`를 기본 경로로 참조하는 설정 불일치 가능성 확인.

## 2. 해결 방법 (Step-by-Step)

### A. 권장 환경 (WSL2 또는 Linux)
OpenUxAS는 ZeroMQ, Boost, SQLite3 등 많은 리눅스 라이브러리에 의존하므로 Windows 사용자라면 **WSL2(Ubuntu 22.04)** 설치를 강력히 권장합니다.

### B. 빌드 절차 (WSL2/Linux 터미널 기준)
1. **의존성 설치:** 가이드에 명시된 `anod` 도구를 사용합니다.
   ```bash
   ./anod build uxas
   ./anod build amase
   ```
2. **바이너리 위치 확인:** 빌드가 완료되면 다음 위치에 파일이 있는지 확인합니다.
   - `OpenUxAS/obj/cpp/uxas`

### C. 윈도우에서의 대안
직접 빌드가 어려운 경우, `uxas_ui_server.py`와 `uxas_ui.html`을 사용하여 UI 서버를 구동하거나, Docker 컨테이너를 통해 실행하는 방식을 고려해야 합니다.

## 3. 관련 파일 정보
- `OpenUxAS/OpenUxAS_Guide_Korean.md`: 상세 설치 및 운용 가이드 (제4장 필독).
- `OpenUxAS/infrastructure/uxas/src/uxas/paths.py`: 시스템 내 주요 경로 정의 파일.
- `OpenUxAS/Makefile`: C++ 소스 빌드 규칙 정의 파일.
- `OpenUxAS/run-example`: 예제 실행을 위한 래퍼 스크립트.

## 4. 향후 작업 제안
- WSL2 환경 구축 후 `./anod build uxas` 실행.
- `paths.py`의 `UXAS_BIN` 경로를 `obj/cpp/uxas`로 일치시키도록 수정 고려.
