-- 컨테이너가 처음 만들어질 때(데이터가 비어 있을 때) 한 번만 실행된다.
CREATE TABLE IF NOT EXISTS products (
    id    SERIAL PRIMARY KEY,
    name  TEXT    NOT NULL,
    price INTEGER NOT NULL
);

INSERT INTO products (name, price) VALUES
    ('러닝화', 59000),
    ('후드 집업', 45000),
    ('에코백', 12000),
    ('텀블러', 18000),
    ('무선 이어폰', 89000);
