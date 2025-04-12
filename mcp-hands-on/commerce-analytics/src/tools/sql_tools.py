"""
SQL 쿼리 관련 도구들을 포함하는 모듈입니다.
- execute_sql: SQL 쿼리 실행
- optimize_sql: SQL 쿼리 최적화 제안
- visualize_schema: 데이터베이스 스키마 시각화
- visualize_sql_result: SQL 쿼리 결과 시각화
"""
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import re
from typing import List, Dict, Any, Optional


# Matplotlib 한글 폰트 설정 (MacOS 기본 폰트만 사용)
plt.rcParams['font.family'] = 'AppleGothic'  # macOS 기본 한글 폰트만 사용
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 임시 데이터베이스 연결을 위한 설정
DB_PATH = ":memory:"  # 메모리 DB 사용


def _create_test_database() -> sqlite3.Connection:
    """
    테스트용 임시 데이터베이스를 생성합니다.
    
    Returns:
        sqlite3.Connection: 데이터베이스 연결 객체
    """
    # 데이터베이스 연결
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 테이블 생성
    # 고객 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        registration_date DATE NOT NULL,
        last_login TIMESTAMP
    )
    ''')
    
    # 상품 카테고리 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_categories (
        category_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES product_categories(category_id)
    )
    ''')
    
    # 상품 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT 1,
        FOREIGN KEY (category_id) REFERENCES product_categories(category_id)
    )
    ''')
    
    # 주문 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TIMESTAMP NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'canceled')),
        total_amount DECIMAL(10, 2) NOT NULL,
        shipping_address TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    ''')
    
    # 주문 상세 내역 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        unit_price DECIMAL(10, 2) NOT NULL,
        discount DECIMAL(10, 2) NOT NULL DEFAULT 0,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')
    
    # 결제 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        payment_method TEXT NOT NULL,
        payment_amount DECIMAL(10, 2) NOT NULL,
        payment_status TEXT NOT NULL CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
        payment_date TIMESTAMP NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
    ''')
    
    # 테스트 데이터 생성
    _populate_test_data(conn)
    
    return conn


def _populate_test_data(conn: sqlite3.Connection) -> None:
    """
    테스트 데이터베이스에 샘플 데이터를 추가합니다.
    
    Args:
        conn: 데이터베이스 연결 객체
    """
    cursor = conn.cursor()
    
    # 고객 데이터
    customers = [
        (1, "홍길동", "hong@example.com", "010-1234-5678", "2023-01-15", "2023-12-01 08:30:00"),
        (2, "김영희", "kim@example.com", "010-2345-6789", "2023-02-20", "2023-12-02 10:15:00"),
        (3, "이철수", "lee@example.com", "010-3456-7890", "2023-03-10", "2023-11-28 14:45:00"),
        (4, "박지영", "park@example.com", "010-4567-8901", "2023-04-05", "2023-12-03 09:20:00"),
        (5, "최민준", "choi@example.com", "010-5678-9012", "2023-05-12", "2023-11-30 16:10:00")
    ]
    cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?, ?)", customers)
    
    # 카테고리 데이터
    categories = [
        (1, "전자기기", None),
        (2, "의류", None),
        (3, "식품", None),
        (4, "스마트폰", 1),
        (5, "노트북", 1),
        (6, "남성의류", 2),
        (7, "여성의류", 2),
        (8, "간식", 3),
        (9, "음료", 3)
    ]
    cursor.executemany("INSERT OR REPLACE INTO product_categories VALUES (?, ?, ?)", categories)
    
    # 상품 데이터
    products = [
        (1, 4, "Galaxy S23", "삼성 최신 스마트폰", 1200000, 50, 1),
        (2, 4, "iPhone 15", "애플 최신 스마트폰", 1500000, 30, 1),
        (3, 5, "MacBook Pro", "애플 최신 노트북", 2500000, 20, 1),
        (4, 5, "Galaxy Book", "삼성 최신 노트북", 1800000, 25, 1),
        (5, 6, "남성 니트", "겨울용 남성 니트", 89000, 100, 1),
        (6, 7, "여성 코트", "겨울용 여성 코트", 250000, 80, 1),
        (7, 8, "감자칩", "짭짤한 감자칩", 2500, 500, 1),
        (8, 9, "콜라", "시원한 탄산음료", 1800, 1000, 1),
        (9, 9, "생수", "깨끗한 생수", 1000, 2000, 1),
        (10, 8, "초콜릿", "달콤한 초콜릿", 3000, 300, 1)
    ]
    cursor.executemany("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", products)
    
    # 주문 데이터
    orders = [
        (1, 1, "2023-11-01 10:30:00", "completed", 1200000, "서울시 강남구"),
        (2, 2, "2023-11-05 14:20:00", "completed", 89000, "서울시 서초구"),
        (3, 3, "2023-11-10 11:45:00", "completed", 2500000, "서울시 종로구"),
        (4, 4, "2023-11-15 16:30:00", "completed", 250000, "서울시 강서구"),
        (5, 5, "2023-11-20 09:15:00", "completed", 8800, "서울시 강동구"),
        (6, 1, "2023-11-25 13:40:00", "completed", 1800000, "서울시 강남구"),
        (7, 2, "2023-11-30 15:50:00", "completed", 92000, "서울시 서초구"),
        (8, 3, "2023-12-01 10:10:00", "pending", 5300, "서울시 종로구"),
        (9, 4, "2023-12-02 12:25:00", "pending", 1500000, "서울시 강서구"),
        (10, 5, "2023-12-03 17:30:00", "pending", 255000, "서울시 강동구")
    ]
    cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?)", orders)
    
    # 주문 상세 내역 데이터
    order_items = [
        (1, 1, 1, 1, 1200000, 0),
        (2, 2, 5, 1, 89000, 0),
        (3, 3, 3, 1, 2500000, 0),
        (4, 4, 6, 1, 250000, 0),
        (5, 5, 7, 1, 2500, 0),
        (6, 5, 8, 2, 1800, 0),
        (7, 5, 9, 2, 1000, 0),
        (8, 5, 10, 1, 3000, 0),
        (9, 6, 4, 1, 1800000, 0),
        (10, 7, 5, 1, 89000, 0),
        (11, 7, 7, 1, 2500, 0),
        (12, 7, 10, 1, 3000, 2500),
        (13, 8, 7, 1, 2500, 0),
        (14, 8, 8, 1, 1800, 0),
        (15, 8, 10, 1, 3000, 2000),
        (16, 9, 2, 1, 1500000, 0),
        (17, 10, 6, 1, 250000, 0),
        (18, 10, 10, 3, 3000, 4000)
    ]
    cursor.executemany("INSERT OR REPLACE INTO order_items VALUES (?, ?, ?, ?, ?, ?)", order_items)
    
    # 결제 데이터
    payments = [
        (1, 1, "card", 1200000, "completed", "2023-11-01 10:35:00"),
        (2, 2, "card", 89000, "completed", "2023-11-05 14:25:00"),
        (3, 3, "bank_transfer", 2500000, "completed", "2023-11-10 11:50:00"),
        (4, 4, "card", 250000, "completed", "2023-11-15 16:35:00"),
        (5, 5, "mobile", 8800, "completed", "2023-11-20 09:20:00"),
        (6, 6, "card", 1800000, "completed", "2023-11-25 13:45:00"),
        (7, 7, "mobile", 92000, "completed", "2023-11-30 15:55:00"),
        (8, 8, "card", 5300, "pending", "2023-12-01 10:15:00"),
        (9, 9, "bank_transfer", 1500000, "pending", "2023-12-02 12:30:00"),
        (10, 10, "mobile", 255000, "pending", "2023-12-03 17:35:00")
    ]
    cursor.executemany("INSERT OR REPLACE INTO payments VALUES (?, ?, ?, ?, ?, ?)", payments)
    
    # 변경사항 커밋
    conn.commit()


def execute_sql(query: str) -> Dict[str, Any]:
    """
    SQL 쿼리를 실행하고 결과를 반환합니다.
    
    Args:
        query: 실행할 SQL 쿼리
        
    Returns:
        Dict: 쿼리 실행 결과와 메타데이터
    """
    try:
        # 테스트 데이터베이스 생성
        conn = _create_test_database()
        
        # 쿼리 실행 전 검증 (예: DROP, DELETE 등의 위험 명령어 체크)
        if re.search(r'\b(DROP|DELETE|TRUNCATE|UPDATE)\b', query, re.IGNORECASE):
            return {
                "success": False,
                "error": "안전상의 이유로 데이터를 변경하는 쿼리(DROP, DELETE, TRUNCATE, UPDATE)는 실행할 수 없습니다."
            }
        
        # 쿼리 실행 시간 측정
        start_time = pd.Timestamp.now()
        
        # pandas로 쿼리 실행 (결과를 DataFrame으로 얻기 위해)
        result_df = pd.read_sql_query(query, conn)
        
        end_time = pd.Timestamp.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # 결과 반환
        return {
            "success": True,
            "data": result_df.to_dict(orient='records'),
            "columns": result_df.columns.tolist(),
            "row_count": len(result_df),
            "execution_time": execution_time
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        if 'conn' in locals():
            conn.close()


def visualize_sql_result(
    query_result: Dict[str, Any], 
    chart_type: str = "auto", 
    x_column: Optional[str] = None, 
    y_column: Optional[str] = None,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    SQL 쿼리 결과를 시각화합니다.
    
    Args:
        query_result: execute_sql 함수에서 반환된 쿼리 결과
        chart_type: 차트 유형 (auto, bar, line, pie, scatter)
        x_column: x축에 사용할 컬럼 이름
        y_column: y축에 사용할 컬럼 이름
        title: 차트 제목
        
    Returns:
        Dict: 시각화 결과 (base64 인코딩된 이미지)
    """
    try:
        # 쿼리 실행 결과 검증
        if not query_result.get("success", False):
            return {
                "success": False,
                "error": "유효하지 않은 쿼리 결과입니다."
            }
        
        # 결과 데이터가 없는 경우
        if not query_result.get("data", []):
            return {
                "success": False,
                "error": "시각화할 데이터가 없습니다."
            }
        
        # 데이터프레임으로 변환
        df = pd.DataFrame(query_result["data"])
        
        # 컬럼이 없는 경우
        if df.empty or len(df.columns) == 0:
            return {
                "success": False,
                "error": "시각화할 열이 없습니다."
            }
        
        # x_column과 y_column이 지정되지 않은 경우 자동 선택
        if x_column is None or y_column is None:
            if len(df.columns) >= 2:
                # 첫 번째 열을 x축, 두 번째 열을 y축으로 사용
                x_column = df.columns[0]
                y_column = df.columns[1]
            else:
                # 열이 하나밖에 없는 경우
                x_column = df.index.name or "index"
                y_column = df.columns[0]
        
        # 차트 유형 자동 선택
        if chart_type == "auto":
            if len(df) <= 10:  # 데이터가 적으면 막대 차트
                chart_type = "bar"
            elif pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column]):
                chart_type = "scatter"
            elif pd.api.types.is_datetime64_dtype(df[x_column]) or pd.api.types.is_period_dtype(df[x_column]):
                chart_type = "line"
            else:
                chart_type = "bar"
        
        # 차트 그리기
        plt.figure(figsize=(10, 6))
        
        if chart_type == "bar":
            df.plot(kind='bar', x=x_column, y=y_column, ax=plt.gca())
        elif chart_type == "line":
            df.plot(kind='line', x=x_column, y=y_column, ax=plt.gca(), marker='o')
        elif chart_type == "pie":
            df.plot(kind='pie', y=y_column, ax=plt.gca(), autopct='%1.1f%%')
        elif chart_type == "scatter":
            df.plot(kind='scatter', x=x_column, y=y_column, ax=plt.gca())
        else:
            return {
                "success": False,
                "error": f"지원하지 않는 차트 유형입니다: {chart_type}"
            }
        
        # 차트 제목 설정
        if title:
            plt.title(title)
        else:
            plt.title(f"{y_column} by {x_column}")
        
        plt.tight_layout()
        
        # 이미지로 변환
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return {
            "success": True,
            "chart_type": chart_type,
            "x_column": x_column,
            "y_column": y_column,
            "image": f"data:image/png;base64,{image_base64}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def optimize_sql(query: str) -> Dict[str, Any]:
    """
    SQL 쿼리를 분석하고 최적화 제안을 제공합니다.
    
    Args:
        query: 최적화할 SQL 쿼리
        
    Returns:
        Dict: 최적화 제안 및 분석 결과
    """
    try:
        # 쿼리 기본 검증
        if not query.strip():
            return {
                "success": False,
                "error": "빈 쿼리입니다."
            }
        
        # 테이블 및 조인 추출
        tables = set(re.findall(r'\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', query, re.IGNORECASE))
        tables.update(re.findall(r'\bJOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)', query, re.IGNORECASE))
        
        # WHERE 조건 추출
        where_conditions = re.findall(r'\bWHERE\s+(.*?)(?:\bGROUP BY|\bORDER BY|\bLIMIT|\bHAVING|\bUNION|\bINTERSECT|\bEXCEPT|\bFOR|\b$)',
                                      query, re.IGNORECASE | re.DOTALL)
        
        # ORDER BY 추출
        order_by = re.findall(r'\bORDER BY\s+(.*?)(?:\bLIMIT|\bHAVING|\bUNION|\bINTERSECT|\bEXCEPT|\bFOR|\b$)',
                             query, re.IGNORECASE | re.DOTALL)
        
        # GROUP BY 추출
        group_by = re.findall(r'\bGROUP BY\s+(.*?)(?:\bORDER BY|\bLIMIT|\bHAVING|\bUNION|\bINTERSECT|\bEXCEPT|\bFOR|\b$)',
                             query, re.IGNORECASE | re.DOTALL)
        
        # 서브쿼리 확인
        has_subquery = '(' in query and 'SELECT' in query.upper() and ')' in query
        
        # 최적화 제안
        suggestions = []
        
        # 테스트 DB 연결 (EXPLAIN 분석을 위해)
        conn = _create_test_database()
        cursor = conn.cursor()
        
        # EXPLAIN 실행
        try:
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            explain_results = cursor.fetchall()
        except sqlite3.Error:
            explain_results = []
        
        # 인덱스 제안
        suggested_indexes = []
        
        # 인덱스 제안 로직
        if where_conditions and tables:
            for table in tables:
                for condition in where_conditions:
                    # 컬럼 추출 시도
                    columns = re.findall(rf'\b{table}\.([a-zA-Z_][a-zA-Z0-9_]*)\b', condition, re.IGNORECASE)
                    
                    if columns:
                        for column in columns:
                            suggested_indexes.append({
                                "table": table,
                                "column": column,
                                "reason": f"{column}은(는) WHERE 절에서 필터링 조건으로 사용됩니다."
                            })
        
        # ORDER BY에서 인덱스 제안
        if order_by and tables:
            for clause in order_by:
                for table in tables:
                    columns = re.findall(rf'\b{table}\.([a-zA-Z_][a-zA-Z0-9_]*)\b', clause, re.IGNORECASE)
                    
                    if columns:
                        for column in columns:
                            suggested_indexes.append({
                                "table": table,
                                "column": column,
                                "reason": f"{column}은(는) ORDER BY 절에서 정렬 기준으로 사용됩니다."
                            })
        
        # GROUP BY에서 인덱스 제안
        if group_by and tables:
            for clause in group_by:
                for table in tables:
                    columns = re.findall(rf'\b{table}\.([a-zA-Z_][a-zA-Z0-9_]*)\b', clause, re.IGNORECASE)
                    
                    if columns:
                        for column in columns:
                            suggested_indexes.append({
                                "table": table,
                                "column": column,
                                "reason": f"{column}은(는) GROUP BY 절에서 그룹화 기준으로 사용됩니다."
                            })
        
        # 중복 제거
        unique_indexes = {}
        for idx in suggested_indexes:
            key = f"{idx['table']}.{idx['column']}"
            if key not in unique_indexes:
                unique_indexes[key] = idx
            else:
                # 이유 결합
                unique_indexes[key]['reason'] += f" 또한, {idx['reason']}"
        
        # 쿼리 패턴 분석 및 제안
        # 1. SELECT * 사용 확인
        if re.search(r'SELECT\s+\*', query, re.IGNORECASE):
            suggestions.append({
                "type": "column_selection",
                "description": "SELECT * 대신 필요한 컬럼만 명시적으로 선택하는 것이 좋습니다.",
                "reason": "필요한 컬럼만 선택하면 I/O와 네트워크 트래픽을 줄일 수 있습니다."
            })
        
        # 2. LIKE '%...%' 패턴 확인 (인덱스 사용 불가)
        if re.search(r'LIKE\s+[\'"]%', query, re.IGNORECASE):
            suggestions.append({
                "type": "like_pattern",
                "description": "LIKE '%...'로 시작하는 패턴은 인덱스를 효과적으로 활용할 수 없습니다.",
                "reason": "앞에 %가 있는 LIKE 패턴은 전체 테이블 스캔이 필요합니다."
            })
        
        # 3. 조인 최적화 제안
        if len(tables) > 1:
            suggestions.append({
                "type": "join_order",
                "description": "조인 순서가 성능에 큰 영향을 미칠 수 있습니다.",
                "reason": "작은 테이블을 먼저 조인하고, 조인 조건의 컬럼에 인덱스가 있는지 확인하세요."
            })
        
        # 4. GROUP BY 최적화 제안
        if group_by:
            suggestions.append({
                "type": "group_by",
                "description": "GROUP BY 절에서 사용하는 컬럼에 인덱스를 추가하는 것이 좋습니다.",
                "reason": "GROUP BY 연산은 정렬이나 해시 테이블을 사용하는데, 인덱스가 있으면 더 효율적입니다."
            })
        
        # 서브쿼리 관련 제안
        if has_subquery:
            suggestions.append({
                "type": "subquery",
                "description": "서브쿼리를 JOIN으로 변환하거나 임시 테이블을 사용하는 것이 더 효율적일 수 있습니다.",
                "reason": "일부 서브쿼리는 최적화하기 어려울 수 있으며, JOIN으로 변환하면 성능이 향상될 수 있습니다."
            })
        
        return {
            "success": True,
            "query": query,
            "tables": list(tables),
            "has_where": bool(where_conditions),
            "has_order_by": bool(order_by),
            "has_group_by": bool(group_by),
            "has_subquery": has_subquery,
            "suggested_indexes": list(unique_indexes.values()),
            "optimization_suggestions": suggestions,
            "explain_results": explain_results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        if 'conn' in locals():
            conn.close()


def visualize_schema(tables: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    데이터베이스 스키마를 시각화합니다.
    
    Args:
        tables: 시각화할 테이블 목록 (None인 경우 모든 테이블)
        
    Returns:
        Dict: 시각화 결과 (base64 인코딩된 이미지)
    """
    try:
        # 테스트 데이터베이스 연결
        conn = _create_test_database()
        cursor = conn.cursor()
        
        # 테이블 정보 가져오기
        if tables:
            table_list = tables
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_list = [row[0] for row in cursor.fetchall()]
            # 시스템 테이블 제외
            table_list = [t for t in table_list if not t.startswith('sqlite_')]
        
        # 테이블 정보와 관계 정보 저장
        schema_info = {}
        relations = []
        
        for table in table_list:
            # 테이블 컬럼 정보 가져오기
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            schema_info[table] = {
                "columns": [{"name": col[1], "type": col[2], "pk": col[5] == 1} for col in columns]
            }
            
            # 외래 키 정보 가져오기
            cursor.execute(f"PRAGMA foreign_key_list({table})")
            fk_list = cursor.fetchall()
            
            for fk in fk_list:
                relations.append({
                    "from_table": table,
                    "from_column": fk[3],
                    "to_table": fk[2],
                    "to_column": fk[4]
                })
        
        # Matplotlib으로 ER 다이어그램 그리기
        plt.figure(figsize=(12, 8))
        
        # 그래프 레이아웃 계산 (간단한 원형 배치)
        n_tables = len(table_list)
        radius = 3
        table_positions = {}
        
        # 테이블 위치 계산
        for i, table in enumerate(table_list):
            angle = 2 * np.pi * i / n_tables
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            table_positions[table] = (x, y)
        
        # 테이블 그리기
        for table, (x, y) in table_positions.items():
            # 테이블 박스 그리기
            table_width = 2.0
            table_height = 0.8 + 0.25 * len(schema_info[table]["columns"])
            
            # 테이블 배경
            rect = plt.Rectangle((x - table_width/2, y - table_height/2), 
                                 table_width, table_height, 
                                 facecolor='lightblue', alpha=0.7, edgecolor='black')
            plt.gca().add_patch(rect)
            
            # 테이블 이름
            plt.text(x, y + table_height/2 - 0.2, table, 
                     fontsize=10, fontweight='bold', 
                     horizontalalignment='center')
            
            # 컬럼 정보
            for i, col in enumerate(schema_info[table]["columns"]):
                marker = "PK" if col["pk"] else ""
                col_text = f"{col['name']} ({col['type']}) {marker}"
                plt.text(x, y + table_height/2 - 0.5 - i*0.25, col_text, 
                         fontsize=8, horizontalalignment='center')
        
        # 관계 화살표 그리기
        for relation in relations:
            from_table = relation["from_table"]
            to_table = relation["to_table"]
            
            if from_table in table_positions and to_table in table_positions:
                from_x, from_y = table_positions[from_table]
                to_x, to_y = table_positions[to_table]
                
                # 화살표 그리기
                plt.arrow(from_x, from_y, (to_x - from_x) * 0.9, (to_y - from_y) * 0.9,
                          head_width=0.1, head_length=0.1, fc='black', ec='black', length_includes_head=True)
                
                # 관계 레이블
                mid_x = (from_x + to_x) / 2
                mid_y = (from_y + to_y) / 2
                relation_text = f"{relation['from_column']} → {relation['to_column']}"
                plt.text(mid_x, mid_y, relation_text, fontsize=6, 
                         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        # 그래프 설정
        plt.title("데이터베이스 스키마 다이어그램")
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        
        # 이미지로 변환
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=150)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return {
            "success": True,
            "tables": table_list,
            "relations": relations,
            "schema_info": schema_info,
            "image": f"data:image/png;base64,{image_base64}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        if 'conn' in locals():
            conn.close() 