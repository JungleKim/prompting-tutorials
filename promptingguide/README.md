# 프롬프트 엔지니어링 실습 프로젝트

프롬프트 엔지니어링 기법을 실습하고 이해하기 위한 주피터 노트북 기반 튜토리얼 프로젝트입니다. [Prompt Engineering Guide](https://www.promptingguide.ai/techniques)에서 소개된 다양한 프롬프팅 기법을 직접 실습해볼 수 있습니다.

## 프로젝트 개요

대규모 언어 모델(LLM)의 성능은 프롬프트의 품질에 크게 의존합니다. 이 프로젝트에서는 다양한 프롬프트 엔지니어링 기법을 통해 LLM과 더 효과적으로 상호작용하는 방법을 배울 수 있습니다.

## 설치 방법

### 필수 요구사항
- Python 3.8 이상
- Jupyter Notebook 또는 JupyterLab
- Make (Makefile 사용 시)
- OpenAI API 키

### 설치 과정

#### Makefile 활용 (권장)

프로젝트 설정을 위해 Makefile을 제공합니다. 다음 명령어로 쉽게 환경을 구성할 수 있습니다:

1. 가상 환경 생성
```bash
make venv
```

2. 가상 환경 활성화
```bash
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

3. 필요한 패키지 설치
```bash
make install
```

4. API 키 설정
```bash
make setup
# .env 파일을 편집하여 OpenAI API 키 등을 추가하세요
```

5. 주피터 노트북 실행
```bash
make run
```

모든 Makefile 명령어 확인:
```bash
make help
```

#### 수동 설치

Makefile을 사용하지 않는 경우, 다음 단계를 따르세요:

1. 저장소 클론하기
```bash
git clone https://github.com/사용자명/prompting-tutorials.git
cd prompting-tutorials
```

2. 가상 환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. API 키 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 OpenAI API 키 등을 추가하세요
```

## OpenAI API 모델 설정

이 프로젝트는 OpenAI API를 사용합니다. 다음과 같은 모델을 지원합니다:

- 기본 모델: `gpt-4o`
- 대체 모델: `gpt-4o-mini`, `gpt-3.5-turbo`

모델 선택은 다음과 같은 순서로 결정됩니다:
1. `.env` 파일의 `MODEL` 환경 변수에 설정된 모델
2. 해당 모델이 사용 불가능한 경우 대체 모델 자동 시도
3. 모든 모델이 실패하면 기본값 사용

모델 관련 문제가 발생하면 다음을 확인하세요:
- OpenAI API 키가 유효한지 확인
- API 사용량 한도를 초과하지 않았는지 확인
- `.env` 파일에서 모델명을 제대로 설정했는지 확인
- OpenAI 계정에서 해당 모델 사용 권한이 있는지 확인

## 프로젝트 구조

```
prompting-tutorials/
├── README.md                  # 프로젝트 설명서
├── Makefile                   # 자동화 스크립트
├── requirements.txt           # 필요한 패키지 목록
├── jupyter_notebook_config.py # Jupyter 설정 파일
├── data/                      # 실습에 필요한 데이터 파일
├── utils/                     # 유틸리티 함수 모음
│   └── helpers.py             # 공통 헬퍼 함수
└── notebooks/                 # 실습용 주피터 노트북
    ├── 01_zero_shot.ipynb     # 제로샷 프롬프팅
    ├── 02_few_shot.ipynb      # 퓨샷 프롬프팅
    ├── 03_chain_of_thought.ipynb # Chain of Thought 프롬프팅
    ├── 04_self_consistency.ipynb # 자기 일관성 프롬프팅
    ├── 05_knowledge.ipynb     # 지식 기반 프롬프팅
    ├── 06_prompt_chaining.ipynb # 프롬프트 체이닝
    ├── 07_rag.ipynb          # Retrieval Augmented Generation
    └── 08_react.ipynb        # ReAct (Reasoning+Acting)
```

## 시작하기

Jupyter Notebook 서버를 실행하여 노트북을 열고 실습을 시작합니다.

```bash
jupyter notebook
# 또는
jupyter lab
```

## 문제 해결

### Jupyter 커널 오류
Jupyter 노트북에서 "Kernel does not exist" 오류가 발생하면:
1. 주피터 서버를 종료하고 다시 시작합니다.
2. 노트북 파일을 열고 'Kernel' 메뉴에서 'Restart' 또는 'Change kernel'을 선택합니다.
3. '.ipynb_checkpoints' 폴더를 삭제합니다: `rm -rf .ipynb_checkpoints/`

### OpenAI API 오류
API 관련 오류가 발생하면:
1. OpenAI 계정에서 Billing 설정이 되어있는지 확인합니다. 무료 크레딧이 있더라도 결제 정보를 등록하지 않으면 API가 동작하지 않습니다.
2. `.env` 파일의 API 키가 올바른지 확인합니다.
3. 모델명이 올바른지 확인합니다 (예: `gpt-4o`, `gpt-4o-mini`).
4. API 사용량 한도와 남은 크레딧을 확인합니다.
5. API 요청 시 발생하는 구체적인 에러 메시지를 확인합니다.

## 유지보수

프로젝트 정리:
```bash
make clean
```

## 라이센스

이 프로젝트는 MIT 라이센스로 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요. 
