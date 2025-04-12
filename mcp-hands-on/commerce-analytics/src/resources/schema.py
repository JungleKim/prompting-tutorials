


ORDER_TABLE = """
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'completed', 'canceled')),
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 인덱스
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);

-- 설명
COMMENT ON TABLE orders IS '커머스 서비스의 주문 기본 정보 테이블';
COMMENT ON COLUMN orders.order_id IS '주문 고유 식별자';
COMMENT ON COLUMN orders.customer_id IS '고객 고유 식별자';
COMMENT ON COLUMN orders.order_date IS '주문 일시';
COMMENT ON COLUMN orders.status IS '주문 상태 (pending, completed, canceled)';
COMMENT ON COLUMN orders.total_amount IS '주문 총 금액';
COMMENT ON COLUMN orders.shipping_address IS '배송지 주소';
COMMENT ON COLUMN orders.created_at IS '레코드 생성 시간';
COMMENT ON COLUMN orders.updated_at IS '레코드 최종 수정 시간';
"""

ORDER_ITEM_TABLE = """
CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 인덱스
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- 설명
COMMENT ON TABLE order_items IS '주문 상세 내역 테이블';
COMMENT ON COLUMN order_items.item_id IS '주문 상세 항목 고유 식별자';
COMMENT ON COLUMN order_items.order_id IS '주문 고유 식별자';
COMMENT ON COLUMN order_items.product_id IS '상품 고유 식별자';
COMMENT ON COLUMN order_items.quantity IS '주문 수량';
COMMENT ON COLUMN order_items.unit_price IS '주문 당시 상품 단가';
COMMENT ON COLUMN order_items.discount IS '항목별 할인 금액';
COMMENT ON COLUMN order_items.created_at IS '레코드 생성 시간';
COMMENT ON COLUMN order_items.updated_at IS '레코드 최종 수정 시간';
""",
        
PAYMENT_TABLE = """
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    payment_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 인덱스
CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_payments_date ON payments(payment_date);

-- 설명
COMMENT ON TABLE payments IS '결제 정보 테이블';
COMMENT ON COLUMN payments.payment_id IS '결제 고유 식별자';
COMMENT ON COLUMN payments.order_id IS '주문 고유 식별자';
COMMENT ON COLUMN payments.payment_method IS '결제 방법 (card, bank_transfer, mobile, etc)';
COMMENT ON COLUMN payments.payment_amount IS '결제 금액';
COMMENT ON COLUMN payments.payment_status IS '결제 상태 (pending, completed, failed, refunded)';
COMMENT ON COLUMN payments.payment_date IS '결제 처리 일시';
COMMENT ON COLUMN payments.created_at IS '레코드 생성 시간';
COMMENT ON COLUMN payments.updated_at IS '레코드 최종 수정 시간';
""",
        
CUSTOMER_TABLE = """
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    registration_date DATE NOT NULL,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_registration ON customers(registration_date);

-- 설명
COMMENT ON TABLE customers IS '고객 정보 테이블';
COMMENT ON COLUMN customers.customer_id IS '고객 고유 식별자';
COMMENT ON COLUMN customers.name IS '고객 이름';
COMMENT ON COLUMN customers.email IS '고객 이메일';
COMMENT ON COLUMN customers.phone IS '고객 전화번호';
COMMENT ON COLUMN customers.registration_date IS '회원 가입일';
COMMENT ON COLUMN customers.last_login IS '최근 로그인 시간';
COMMENT ON COLUMN customers.created_at IS '레코드 생성 시간';
COMMENT ON COLUMN customers.updated_at IS '레코드 최종 수정 시간';
""",
        
PRODUCT_TABLE = """
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES product_categories(category_id)
);

-- 인덱스
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_active ON products(is_active);

-- 설명
COMMENT ON TABLE products IS '상품 정보 테이블';
COMMENT ON COLUMN products.product_id IS '상품 고유 식별자';
COMMENT ON COLUMN products.category_id IS '카테고리 고유 식별자';
COMMENT ON COLUMN products.name IS '상품명';
COMMENT ON COLUMN products.description IS '상품 상세 설명';
COMMENT ON COLUMN products.price IS '상품 가격';
COMMENT ON COLUMN products.stock_quantity IS '재고 수량';
COMMENT ON COLUMN products.is_active IS '판매 활성화 여부';
COMMENT ON COLUMN products.created_at IS '레코드 생성 시간';
COMMENT ON COLUMN products.updated_at IS '레코드 최종 수정 시간';
""",
        
PRODUCT_CATEGORY_TABLE = """
CREATE TABLE product_categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES product_categories(category_id)
);

-- 인덱스
CREATE INDEX idx_categories_parent ON product_categories(parent_id);

-- 설명
COMMENT ON TABLE product_categories IS '상품 카테고리 테이블';
COMMENT ON COLUMN product_categories.category_id IS '카테고리 고유 식별자';
COMMENT ON COLUMN product_categories.name IS '카테고리 이름';
COMMENT ON COLUMN product_categories.parent_id IS '상위 카테고리 식별자';
COMMENT ON COLUMN product_categories.created_at IS '레코드 생성 시간';
COMMENT ON COLUMN product_categories.updated_at IS '레코드 최종 수정 시간';
"""