.PHONY: setup venv install clean run help mcpconfig

# 기본 명령어
help:
	@echo "MCP 보일러플레이트 애플리케이션"
	@echo ""
	@echo "사용 가능한 명령어:"
	@echo "  make setup    - 프로젝트 환경 설정 (uv 설치 및 가상환경 생성)"
	@echo "  make install  - 필요한 의존성 설치 (pyproject.toml 기반)"
	@echo "  make run      - 애플리케이션 실행"
	@echo "  make clean    - 임시 파일 및 가상환경 제거"
	@echo "  make mcpconfig - 현재 경로 기반 MCP 설정 JSON 출력 (SSE 기반)"
	@echo ""

# 환경 설정
setup:
	@echo "환경 설정 중..."
	@if ! command -v uv &> /dev/null; then \
		echo "uv 설치 중..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "터미널을 재시작하거나 경로를 업데이트하세요"; \
	else \
		echo "uv가 이미 설치되어 있습니다"; \
	fi
	@echo "가상환경 생성 중..."
	uv venv

# 의존성 설치
install: venv
	@echo "의존성 설치 중 (pyproject.toml 기반)..."
	. .venv/bin/activate && uv pip install -e .

# 가상환경 생성
venv:
	@if [ ! -d ".venv" ]; then \
		echo "가상환경 생성 중..."; \
		uv venv; \
	else \
		echo "가상환경이 이미 존재합니다"; \
	fi

# 애플리케이션 실행
run:
	@echo "MCP 보일러플레이트 애플리케이션 실행 중..."
	. .venv/bin/activate && python -m src.main

# MCP 설정 JSON 출력
mcpconfig:
	@echo '{'; \
	echo '    "mcpServers": {'; \
	echo '        "data-analytics": {'; \
	echo '            "url": "http://127.0.0.1:8000/sse",'; \
	echo '            "transport": "sse"'; \
	echo '        }'; \
	echo '    }'; \
	echo '}'

# 정리
clean:
	@echo "임시 파일 제거 중..."
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "가상환경 제거하려면 'make cleanvenv' 명령어를 사용하세요"

# 가상환경 제거
cleanvenv:
	@echo "가상환경 제거 중..."
	rm -rf .venv 