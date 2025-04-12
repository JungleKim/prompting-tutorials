# 날씨 정보 조회 MCP 애플리케이션

이 프로젝트는 [Model Context Protocol(MCP)](https://modelcontextprotocol.io/)을 활용하여 미국 기상청(NWS) API로 날씨 정보를 조회하는 애플리케이션입니다.

## MCP 소개

MCP는 대규모 언어 모델(LLM)이 외부 도구와 안전하게 상호작용할 수 있게 해주는 프로토콜입니다.

**주요 기능:**
- **도구(Tools)**: LLM이 사용자 승인 하에 호출할 수 있는 함수 

이 날씨 애플리케이션은 도구(Tools) 기능을 활용한 예시입니다.

## 기능 및 구성

### 주요 기능
- 미국 주별 날씨 경보 조회 (`get_alerts`)
- 위도/경도 기반 날씨 예보 조회 (`get_forecast`)

### 시스템 요구사항
- Python 3.10 이상
- MCP SDK 1.2.0 이상

### 프로젝트 구조
- `main.py`: MCP 서버 구현 및 주요 기능
- `utils.py`: 헬퍼 함수 및 상수 정의
- `pyproject.toml`: 프로젝트 설정 및 의존성

## 빠른 시작

### 환경 설정
```bash
# uv 설치 (MacOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트 설정
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx
```

### 실행 방법
```bash
python main.py
```

### MCP 설정 JSON 출력
```bash
# 현재 경로 기반 MCP 설정 JSON 출력
make mcpconfig
```

출력되는 JSON은 다음과 같은 형식을 가집니다:
```json
{
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/CURRENT/FOLDER",
                "run",
                "weather.py"
            ]
        }
    }
}
```

이 설정은 MCP를 통해 날씨 서비스에 연결할 때 사용할 수 있습니다.

## 사용 예시

```python
# 캘리포니아 지역 날씨 경보 조회
get_alerts(state="CA")

# 샌프란시스코 날씨 예보 조회
get_forecast(latitude=37.7749, longitude=-122.4194)
```

## 문제 해결

### "Failed to retrieve grid point data" 오류
- 미국 내 좌표인지 확인 (미국 외 지역은 지원하지 않음)
- API 요청 사이에 지연 추가
- NWS API 상태 확인

## 참고 자료
- [MCP 공식 문서](https://modelcontextprotocol.io/)
