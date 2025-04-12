import json
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport

# main.py에서 정의된 mcp 서버 가져오기
from .main import mcp as mcp_server

async def main():
    """MCP 클라이언트 테스트 함수"""
    async with Client(FastMCPTransport(mcp_server)) as client:
        try:
            # 서버에서 제공하는 리소스 목록 조회
            resources = await client.list_resources()
            print("서버에서 제공하는 리소스 목록:", resources)
            
            # 서버에서 제공하는 도구 목록 조회
            tools = await client.list_tools()
            print("서버에서 제공하는 도구 목록:", tools)
            
            # 서버에서 제공하는 프롬프트 목록 조회
            prompts = await client.list_prompts()
            print("서버에서 제공하는 프롬프트 목록:", prompts)
            
            print("\n--- SQL 쿼리 생성 프롬프트 테스트 ---\n")
            
            # 일일 매출 분석 SQL 쿼리 생성
            daily_sales_query = await client.get_prompt("generate_daily_sales_query", arguments={"date": "2023-12-01"})
            daily_sales_query_str = str(daily_sales_query)  # 문자열로 변환
            print("일일 매출 분석 SQL 쿼리:", daily_sales_query_str[:300] + "..." if len(daily_sales_query_str) > 300 else daily_sales_query_str)
            
            # 카테고리별 매출 분석 SQL 쿼리 생성
            category_sales_query = await client.get_prompt("generate_category_sales_query", arguments={
                "start_date": "2023-01-01", 
                "end_date": "2023-12-31"
            })
            category_sales_query_str = str(category_sales_query)  # 문자열로 변환
            print("카테고리별 매출 분석 SQL 쿼리:", category_sales_query_str[:300] + "..." if len(category_sales_query_str) > 300 else category_sales_query_str)
            
            # 사용자 정의 분석 SQL 쿼리 생성
            custom_query = await client.get_prompt("generate_custom_query", arguments={
                "query_description": "최근 3개월간 가장 많이 구매한 고객 상위 10명과 그들이 구매한 상품 카테고리 정보를 추출해주세요."
            })
            custom_query_str = str(custom_query)  # 문자열로 변환
            print("사용자 정의 분석 SQL 쿼리:", custom_query_str[:300] + "..." if len(custom_query_str) > 300 else custom_query_str)
            
            print("\n--- SQL 도구 테스트 ---\n")
            
            # SQL 쿼리 실행 테스트
            sample_query = """
            SELECT c.name AS 고객명, SUM(o.total_amount) AS 총구매액,
                   COUNT(o.order_id) AS 주문횟수,
                   MAX(o.order_date) AS 최근주문일
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            ORDER BY 총구매액 DESC
            """
            
            query_result = await client.call_tool("execute_sql", arguments={"query": sample_query})
            query_result_data = json.loads(query_result.content[0].text)
            print("SQL 쿼리 실행 결과:", query_result_data)
            # SQL 쿼리 결과 시각화 테스트
            if query_result_data["success"]:
                visualization = await client.call_tool("visualize_sql_result", arguments={
                    "query_result": query_result_data,
                    "chart_type": "bar",
                    "x_column": "고객명",
                    "y_column": "총구매액",
                    "title": "고객별 총 구매액"
                })
                visualization_data = json.loads(visualization.content[0].text)
                print("SQL 결과 시각화:", "성공" if visualization_data["success"] else "실패")
                # 시각화 이미지는 크기가 크므로 출력하지 않음
            
            # SQL 쿼리 최적화 테스트
            optimization = await client.call_tool("optimize_sql", arguments={"query": sample_query})
            optimization_data = json.loads(optimization.content[0].text)
            print("SQL 쿼리 최적화 제안:", optimization_data["suggested_indexes"] if optimization_data["success"] else "실패")
            
            # 스키마 시각화 테스트
            schema_diagram = await client.call_tool("visualize_schema")
            schema_diagram_data = json.loads(schema_diagram.content[0].text)
            print("스키마 시각화:", "성공" if schema_diagram_data["success"] else "실패")
            
        except Exception as e:
            print(f"오류 발생: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
