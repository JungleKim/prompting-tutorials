from fastmcp.prompts.base import Message as MCPMessage, UserMessage, AssistantMessage
from typing import List, Optional

# 리소스 import 추가
from ..resources import (
    get_order_schema, get_order_item_schema, get_payment_schema, 
    get_customer_schema, get_product_schema, get_product_category_schema
)

"""
DDL 정보를 활용하여 SQL 쿼리를 생성하는 프롬프트 정의
"""

def _get_schema_info() -> str:
    """실제 resources에서 스키마 정보를 가져오는 함수"""
    schemas = {
        "orders": get_order_schema(),
        "order_items": get_order_item_schema(),
        "payments": get_payment_schema(),
        "customers": get_customer_schema(),
        "products": get_product_schema(),
        "product_categories": get_product_category_schema()
    }
    
    # 스키마 정보를 간략하게 요약
    summary = """
커머스 서비스에는 다음과 같은 테이블들이 있습니다.
각 테이블의 상세 DDL 정보는 다음과 같습니다:

"""
    
    # 각 테이블의 DDL 정보 추가
    for table_name, schema in schemas.items():
        summary += f"\n## {table_name} 테이블\n```sql\n{schema}\n```\n"
    
    # 테이블 간 관계 정보 추가
    summary += """
## 테이블 간 관계
- orders - customers: 1:N 관계 (customer_id 컬럼으로 연결)
- orders - order_items: 1:N 관계 (order_id 컬럼으로 연결)
- orders - payments: 1:N 관계 (order_id 컬럼으로 연결)
- products - product_categories: N:1 관계 (category_id 컬럼으로 연결)
- order_items - products: N:1 관계 (product_id 컬럼으로 연결)
"""
    
    return summary

def _get_daily_sales_query_prompt(date=None) -> str:
    """일일 매출 쿼리 생성 프롬프트"""
    date_info = f" {date}" if date else " 오늘"
    
    return f"""
# 일일 매출 분석 SQL 쿼리 생성

## 데이터베이스 스키마
{_get_schema_info()}

## 요청
{date_info}의 매출 데이터를 분석하기 위한 SQL 쿼리를 작성해주세요.

## 필요한 정보
1. 총 매출 금액
2. 총 주문 건수
3. 평균 주문 금액
4. 가장 많이 팔린 상위 5개 상품
5. 시간대별 매출 추이

## 요구사항
- 명확하고 효율적인 SQL 쿼리를 작성해주세요
- 필요한 경우 여러 개의 쿼리로 나누어도 좋습니다
- 테이블 조인이 필요한 경우 적절한 JOIN 문을 사용하세요
- 결과를 이해하기 쉽도록 적절한 열 이름(alias)을 지정해주세요
"""

def _get_sales_by_category_query_prompt(start_date=None, end_date=None) -> str:
    """카테고리별 매출 쿼리 생성 프롬프트"""
    date_range = ""
    if start_date and end_date:
        date_range = f" {start_date}부터 {end_date}까지의"
    elif start_date:
        date_range = f" {start_date}부터 현재까지의"
    elif end_date:
        date_range = f" {end_date}까지의"
    else:
        date_range = " 전체 기간의"
    
    return f"""
# 카테고리별 매출 분석 SQL 쿼리 생성

## 데이터베이스 스키마
{_get_schema_info()}

## 요청
{date_range} 상품 카테고리별 매출 데이터를 분석하기 위한 SQL 쿼리를 작성해주세요.

## 필요한 정보
1. 카테고리별 총 매출
2. 카테고리별 판매 상품 수
3. 카테고리별 평균 주문 금액
4. 기간 내 매출 성장률이 가장 높은 카테고리

## 요구사항
- 카테고리별로 집계된 정보를 반환하는 쿼리를 작성해주세요
- 상위 카테고리와 하위 카테고리를 모두 고려해주세요
- 매출 기준 내림차순으로 정렬해주세요
- 필요한 경우 CTE(Common Table Expression)를 사용해도 좋습니다
"""

def _get_customer_segment_query_prompt(segment_type=None) -> str:
    """고객 세그먼트 분석 쿼리 생성 프롬프트"""
    segment_info = f" {segment_type} 기준으로" if segment_type else " RFM(Recency, Frequency, Monetary) 기준으로"
    
    return f"""
# 고객 세그먼트 분석 SQL 쿼리 생성

## 데이터베이스 스키마
{_get_schema_info()}

## 요청
고객을{segment_info} 세그먼트화하고 분석하기 위한 SQL 쿼리를 작성해주세요.

## 필요한 정보
1. 고객별 최근 구매일(Recency)
2. 고객별 구매 빈도(Frequency)
3. 고객별 총 구매 금액(Monetary)
4. 세그먼트별 고객 수와 비율

## 요구사항
- 고객을 여러 세그먼트로 나누는 쿼리를 작성해주세요
- 세그먼트 기준을 명확히 정의해주세요
- 세그먼트별 특성을 분석할 수 있는 추가 쿼리도 작성해주세요
- 필요한 경우 윈도우 함수나 서브쿼리를 활용하세요
"""

# FastMCP에서 사용할 함수 정의
def generate_daily_sales_query(date: Optional[str] = None) -> List[MCPMessage]:
    """
    일일 매출 분석을 위한 SQL 쿼리 생성 프롬프트
    
    Args:
        date: 분석할 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)
    """
    return [
        AssistantMessage(
            content="당신은 커머스 데이터베이스의 DDL 정보를 기반으로 SQL 쿼리를 생성하는 전문가입니다. 주어진 요구사항을 분석하여 최적화된 SQL 쿼리를 작성해주세요."
        ),
        UserMessage(
            content=_get_daily_sales_query_prompt(date)
        )
    ]

def generate_category_sales_query(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> List[MCPMessage]:
    """
    카테고리별 매출 분석을 위한 SQL 쿼리 생성 프롬프트
    
    Args:
        start_date: 분석 시작일 (YYYY-MM-DD 형식)
        end_date: 분석 종료일 (YYYY-MM-DD 형식)
    """
    return [
        AssistantMessage(
            content="당신은 커머스 데이터베이스의 DDL 정보를 기반으로 SQL 쿼리를 생성하는 전문가입니다. 주어진 요구사항을 분석하여 최적화된 SQL 쿼리를 작성해주세요."
        ),
        UserMessage(
            content=_get_sales_by_category_query_prompt(start_date, end_date)
        )
    ]

def generate_customer_segment_query(
    segment_type: Optional[str] = None
) -> List[MCPMessage]:
    """
    고객 세그먼트 분석을 위한 SQL 쿼리 생성 프롬프트
    
    Args:
        segment_type: 세그먼트 기준 (RFM, 구매금액, 구매빈도 등)
    """
    return [
        AssistantMessage(
            content="당신은 커머스 데이터베이스의 DDL 정보를 기반으로 SQL 쿼리를 생성하는 전문가입니다. 주어진 요구사항을 분석하여 최적화된 SQL 쿼리를 작성해주세요."
        ),
        UserMessage(
            content=_get_customer_segment_query_prompt(segment_type)
        )
    ]

def generate_custom_query(
    query_description: str
) -> List[MCPMessage]:
    """
    사용자 정의 분석을 위한 SQL 쿼리 생성 프롬프트
    
    Args:
        query_description: 생성할 쿼리에 대한 자연어 설명
    """
    return [
        AssistantMessage(
            content="당신은 커머스 데이터베이스의 DDL 정보를 기반으로 SQL 쿼리를 생성하는 전문가입니다. 주어진 요구사항을 분석하여 최적화된 SQL 쿼리를 작성해주세요."
        ),
        UserMessage(
            content=f"""
# 사용자 정의 SQL 쿼리 생성

## 데이터베이스 스키마
{_get_schema_info()}

## 요청
{query_description}

## 요구사항
- 명확하고 효율적인 SQL 쿼리를 작성해주세요
- 필요한 테이블을 적절히 조인하세요
- 결과를 이해하기 쉽도록 적절한 열 이름(alias)을 지정해주세요
- 필요한 경우 여러 개의 쿼리로 나누어도 좋습니다
"""
        )
    ] 