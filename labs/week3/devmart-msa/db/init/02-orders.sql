-- orders DB — 주문 서비스만 쓰는 데이터. 상품 서비스와 데이터베이스를 나눈다.
CREATE DATABASE orders;
\connect orders

CREATE TABLE IF NOT EXISTS orders (
    id           SERIAL PRIMARY KEY,
    product_id   INTEGER NOT NULL,      -- 다른 서비스의 데이터라 FOREIGN KEY를 걸 수 없다
    product_name TEXT    NOT NULL,      -- 주문 당시 이름을 복사해 둔다
    quantity     INTEGER NOT NULL,
    total_price  INTEGER NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'pending',
    request_id   TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ,
    processed_by TEXT
);
