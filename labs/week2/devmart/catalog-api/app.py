"""DevMart 상품 API — 2주차 실습용.

- DB_HOST 환경 변수가 없으면 코드 안의 샘플 상품을 돌려준다.
- DB_HOST가 있으면 PostgreSQL의 products 테이블에서 읽는다.
"""
import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False  # 한글을 그대로 보여 준다

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "local")

SAMPLE_PRODUCTS = [
    {"id": 1, "name": "러닝화", "price": 59000},
    {"id": 2, "name": "후드 집업", "price": 45000},
    {"id": 3, "name": "에코백", "price": 12000},
]


def db_configured() -> bool:
    return bool(os.getenv("DB_HOST"))


def load_products_from_db():
    import psycopg  # DB를 쓸 때만 불러온다

    conninfo = (
        f"host={os.environ['DB_HOST']} "
        f"port={os.getenv('DB_PORT', '5432')} "
        f"dbname={os.getenv('DB_NAME', 'devmart')} "
        f"user={os.getenv('DB_USER', 'devmart')} "
        f"password={os.getenv('DB_PASSWORD', '')}"
    )
    with psycopg.connect(conninfo, connect_timeout=3) as conn:
        rows = conn.execute("SELECT id, name, price FROM products ORDER BY id").fetchall()
    return [{"id": r[0], "name": r[1], "price": r[2]} for r in rows]


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/info")
def info():
    return jsonify(
        service="catalog-api",
        version=APP_VERSION,
        env=APP_ENV,
        hostname=socket.gethostname(),
        database="configured" if db_configured() else "not configured (sample data)",
    )


@app.get("/api/products")
def products():
    if not db_configured():
        return jsonify(source="sample", items=SAMPLE_PRODUCTS)
    try:
        return jsonify(source="database", items=load_products_from_db())
    except Exception as e:  # 실습에서 장애 원인을 읽을 수 있도록 에러 종류를 보여 준다
        app.logger.error("DB 조회 실패: %s", e)
        return jsonify(error="database unavailable", detail=type(e).__name__), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
