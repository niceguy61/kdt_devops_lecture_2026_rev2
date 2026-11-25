-- catalog DB (POSTGRES_DB로 이미 만들어져 있다) — 상품 서비스의 데이터
CREATE TABLE IF NOT EXISTS products (
    id    SERIAL PRIMARY KEY,
    name  TEXT    NOT NULL,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

INSERT INTO products (name, price, stock) VALUES
    ('러닝화', 59000, 12),
    ('후드 집업', 45000, 8),
    ('에코백', 12000, 30),
    ('텀블러', 18000, 20),
    ('무선 이어폰', 89000, 5);
