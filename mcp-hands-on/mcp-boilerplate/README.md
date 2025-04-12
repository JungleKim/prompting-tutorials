# MCP 보일러플레이트 프로젝트

이 프로젝트는 [Model Context Protocol(MCP)](https://modelcontextprotocol.io/) 애플리케이션을 빠르게 시작할 수 있는 보일러플레이트입니다.

## MCP 소개

MCP는 대규모 언어 모델(LLM)이 외부 도구와 안전하게 상호작용할 수 있게 해주는 프로토콜입니다.

**주요 기능:**
- **리소스(Resources)**: API 응답이나 파일 내용 같은 데이터 제공
- **도구(Tools)**: LLM이 사용자 승인 하에 호출할 수 있는 함수 
- **프롬프트(Prompts)**: 사용자 작업을 돕는 템플릿

## 프로젝트 구조

```
mcp-boilerplate/
├── src/
│   ├── resources/      # 리소스 관련 코드
│   ├── tools/          # 도구 관련 코드
│   ├── prompts/        # 프롬프트 관련 코드
│   ├── main.py         # MCP 서버 및 데코레이터
│   └── __init__.py
├── .python-version
├── Makefile
├── README.md
└── pyproject.toml
```

### 시스템 요구사항
- Python 3.10 이상
- MCP SDK 1.6.0 이상

## 빠른 시작

### 환경 설정
```bash
# 프로젝트 설정
make setup
make install
```

### 실행 방법
```bash
make run
```

## 사용자 정의 방법

1. 도구 추가:
   - `src/tools/` 디렉토리에 새 파일 생성
   - 도구 로직 구현
   - `src/main.py`에 도구 등록 (`@mcp.tool()` 데코레이터 사용)

2. 리소스 추가:
   - `src/resources/` 디렉토리에 새 파일 생성
   - 리소스 로직 구현
   - `src/main.py`에 리소스 등록 (`@mcp.resource()` 데코레이터 사용)

3. 프롬프트 추가:
   - `src/prompts/` 디렉토리에 새 파일 생성
   - 프롬프트 템플릿 작성
   - `src/main.py`에 프롬프트 등록 (`mcp.register_prompt()` 함수 사용)

## 참고 자료
- [MCP 공식 문서](https://modelcontextprotocol.io/) 