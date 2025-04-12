"""
MCP 프롬프트들을 포함하는 패키지입니다.
"""

from .sql_generator import (
    generate_daily_sales_query, generate_category_sales_query,
    generate_customer_segment_query, generate_custom_query
)

__all__ = [
    'generate_daily_sales_query', 'generate_category_sales_query',
    'generate_customer_segment_query', 'generate_custom_query'
] 