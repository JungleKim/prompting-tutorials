from fastmcp import FastMCP

# Import tools, resources, and prompts
from .tools import (
    execute_sql, visualize_sql_result, optimize_sql, visualize_schema
)
from .resources import (
    get_order_schema, get_order_item_schema, get_payment_schema, get_customer_schema, get_product_schema, get_product_category_schema
)
from .prompts import (
    generate_daily_sales_query, generate_category_sales_query,
    generate_customer_segment_query, generate_custom_query
)

# Initialize FastMCP server
mcp = FastMCP("data-analytics")

# 도구 등록
mcp.tool(name="execute_sql", description="SQL 쿼리 실행하고 결과를 반환")(execute_sql)
mcp.tool(name="visualize_sql_result", description="SQL 쿼리 결과를 차트로 시각화")(visualize_sql_result)
mcp.tool(name="optimize_sql", description="SQL 쿼리 분석 및 최적화 제안 제공")(optimize_sql)
mcp.tool(name="visualize_schema", description="데이터베이스 스키마를 다이어그램으로 시각화")(visualize_schema)

# 리소스 등록
mcp.resource(uri="commerce://schema/order", name="주문 스키마 조회", description="주문 스키마 조회")(get_order_schema) 
mcp.resource(uri="commerce://schema/order_item", name="주문 아이템 스키마 조회", description="주문 아이템 스키마 조회")(get_order_item_schema)
mcp.resource(uri="commerce://schema/payment", name="결제 스키마 조회", description="결제 스키마 조회")(get_payment_schema)
mcp.resource(uri="commerce://schema/customer", name="고객 스키마 조회", description="고객 스키마 조회")(get_customer_schema)
mcp.resource(uri="commerce://schema/product", name="상품 스키마 조회", description="상품 스키마 조회")(get_product_schema)
mcp.resource(uri="commerce://schema/product_category", name="상품 카테고리 스키마 조회", description="상품 카테고리 스키마 조회")(get_product_category_schema)

# 새로운 SQL 쿼리 생성 프롬프트 등록
mcp.prompt(name="generate_daily_sales_query", description="일일 매출 분석 SQL 쿼리 생성")(generate_daily_sales_query)
mcp.prompt(name="generate_category_sales_query", description="카테고리별 매출 분석 SQL 쿼리 생성")(generate_category_sales_query)
mcp.prompt(name="generate_customer_segment_query", description="고객 세그먼트 분석 SQL 쿼리 생성")(generate_customer_segment_query)
mcp.prompt(name="generate_custom_query", description="사용자 정의 분석 SQL 쿼리 생성")(generate_custom_query)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')
