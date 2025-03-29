.PHONY: venv install setup clean help jupyter-setup run-lab

# 기본 목표는 도움말
.DEFAULT_GOAL := help

# Python 바이너리 경로
PYTHON := python
PIP := pip

# 가상 환경 경로
VENV := venv
VENV_ACTIVATE := $(VENV)/bin/activate

# 주요 실행 명령어
JUPYTER_LAB := jupyter lab
JUPYTER_CONFIG := jupyter_notebook_config.py
JUPYTER_HOME := ~/.jupyter

# 도움말
help:
	@echo "프롬프트 엔지니어링 실습 프로젝트 Makefile"
	@echo ""
	@echo "사용 가능한 명령어:"
	@echo "  make venv         - 가상 환경 생성"
	@echo "  make install      - 필요한 패키지 설치"
	@echo "  make setup        - .env 파일 설정"
	@echo "  make run      - JupyterLab 실행"
	@echo "  make clean        - 프로젝트 정리 (가상 환경 및 캐시 파일 삭제)"
	@echo "  make help         - 이 도움말 표시"
	@echo ""
	@echo "일반적인 사용 순서:"
	@echo "  1. make venv"
	@echo "  2. make install"
	@echo "  3. make setup"
	@echo "  4. make run"

# 가상 환경 생성
venv:
	@echo "가상 환경 생성 중..."
	@$(PYTHON) -m venv $(VENV)
	@echo "가상 환경이 생성되었습니다. 다음 명령어로 활성화하세요:"
	@echo "  source $(VENV_ACTIVATE)  # Linux/Mac"
	@echo "  $(VENV)\Scripts\activate  # Windows"

# 필요한 패키지 설치
install:
	@echo "필요한 패키지 설치 중..."
	@$(PIP) install -r requirements.txt
	@echo "패키지 설치가 완료되었습니다."

# .env 파일 설정
setup:
	@echo ".env 파일 설정 중..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env 파일이 생성되었습니다. API 키를 설정하세요."; \
	else \
		echo ".env 파일이 이미 존재합니다."; \
	fi

# JupyterLab 실행
run:
	@echo "JupyterLab 실행 중..."
	@$(JUPYTER_LAB) --config=$(JUPYTER_CONFIG)

# 프로젝트 정리
clean:
	@echo "프로젝트 정리 중..."
	@rm -rf $(VENV) __pycache__ .ipynb_checkpoints
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	@echo "프로젝트가 정리되었습니다." 