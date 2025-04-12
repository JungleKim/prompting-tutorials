# 커머스 데이터 분석 MCP 프로젝트

이 프로젝트는 [Model Context Protocol(MCP)](https://modelcontextprotocol.io/)을 활용하여 커머스 서비스의 판매 데이터를 분석하는 애플리케이션입니다.

## 프로젝트 소개

이 애플리케이션은 커머스 서비스의 주문, 결제, 상품, 고객 데이터를 분석하여 다음과 같은 기능을 제공합니다:

- 기간별 매출 분석
- 상품 카테고리별 매출 분석
- 고객 세그먼트 분석
- 데이터 기반 리포트 생성

**주요 기능:**
- **리소스(Resources)**: 테이블 스키마 및 메타데이터 정보를 제공
- **도구(Tools)**: 매출 분석, 고객 세그먼트 분석 등의 기능을 수행
- **프롬프트(Prompts)**: 보고서 생성 및 분석 가이드 템플릿 제공

## 프로젝트 구조

```
commerce-analytics/
├── src/
│   ├── resources/        # 테이블 스키마 및 메타데이터
│   │   └── commerce_schema.py
│   ├── tools/            # 분석 도구
│   │   └── sql_tools.py
│   ├── prompts/          # 분석 프롬프트 템플릿
│   │   └── sales_report.py
│   ├── main.py           # MCP 서버 및 등록 로직
│   └── client.py         # MCP 클라이언트 테스트
├── Makefile
├── README.md
└── pyproject.toml
```

## 주요 구성 요소

### 1. 테이블 스키마 리소스

다음과 같은 테이블 스키마 정보를 제공합니다:

- **customers**: 고객 정보
- **product_categories**: 상품 카테고리 정보
- **products**: 상품 정보
- **orders**: 주문 기본 정보
- **order_items**: 주문 상세 내역
- **payments**: 결제 정보

### 2. SQL 분석 도구

다음과 같은 SQL 분석 도구를 제공합니다:

- **execute_sql**: SQL 쿼리 실행
- **visualize_sql_result**: SQL 쿼리 결과 시각화
- **optimize_sql**: SQL 쿼리 최적화 제안
- **visualize_schema**: 데이터베이스 스키마 시각화

### 3. 프롬프트 템플릿

다음과 같은 분석 프롬프트 템플릿을 제공합니다:

- **generate_daily_sales_query**: 일일 매출 분석 SQL 쿼리 생성
- **generate_category_sales_query**: 카테고리별 매출 분석 SQL 쿼리 생성
- **generate_custom_query**: 사용자 정의 분석 SQL 쿼리 생성

## 시작하기

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

### 클라이언트 테스트
```bash
# 클라이언트 테스트 실행
python -m src.client
```

## 한글 지원 및 폰트 설정

프로젝트에서는 한글을 포함한 차트와 시각화를 제공합니다. 한글 지원을 위해 다음과 같은 설정이 적용되어 있습니다:

### 한글 폰트 설정

`src/tools/sql_tools.py` 파일에서 Matplotlib의 한글 폰트 설정이 포함되어 있습니다:

```python
import warnings
from matplotlib import pyplot as plt

# MacOS용 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'  # macOS 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
```

### 다른 운영체제에서의 한글 폰트 설정

- **Windows**: `Malgun Gothic` (맑은 고딕)
- **Linux**: `NanumGothic` (나눔고딕)

필요에 따라 `sql_tools.py` 파일의 폰트 설정을 변경하여 사용하세요:

```python
# Windows의 경우
plt.rcParams['font.family'] = 'Malgun Gothic'

# Linux의 경우 (나눔고딕 설치 필요)
plt.rcParams['font.family'] = 'NanumGothic'
```

## MCP 소개

MCP는 대규모 언어 모델(LLM)이 외부 도구와 안전하게 상호작용할 수 있게 해주는 프로토콜입니다.

**주요 기능:**
- **리소스(Resources)**: API 응답이나 파일 내용 같은 데이터 제공
- **도구(Tools)**: LLM이 사용자 승인 하에 호출할 수 있는 함수 
- **프롬프트(Prompts)**: 사용자 작업을 돕는 템플릿

### 시스템 요구사항
- Python 3.10 이상
- MCP SDK 1.6.0 이상

## 참고 자료
- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Matplotlib 한글 폰트 설정 가이드](https://matplotlib.org/stable/tutorials/text/text_props.html) 