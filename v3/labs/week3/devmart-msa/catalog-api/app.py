"""DevMart 상품 서비스(catalog-api) — 3주차 MSA 실습용.

2주차 코드에 두 가지를 더했다.
- GET /api/products/<id> : 주문 서비스가 가격을 확인할 때 부른다
- 요청마다 X-Request-ID를 로그에 남겨, 여러 서비스에 걸친 요청을 추적한다
"""
import json
import os
import socket

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False

SERVICE = "catalog-api"
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
APP_ENV = os.getenv("APP_ENV", "local")


def log(event, **fields):
    """한 줄짜리 JSON 로그 — 사람도 읽고, 4주차 로그 수집 도구도 읽는다."""
    rid = request.headers.get("X-Request-ID", "-") if request else "-"
    print(json.dumps({"service": SERVICE, "event": event, "request_id": rid, **fields},
                     ensure_ascii=False), flush=True)


def conninfo():
    return (
        f"host={os.environ['DB_HOST']} port={os.getenv('DB_PORT', '5432')} "
        f"dbname={os.getenv('DB_NAME', 'catalog')} user={os.getenv('DB_USER', 'devmart')} "
        f"password={os.getenv('DB_PASSWORD', '')}"
    )


def query(sql, params=()):
    import psycopg
    with psycopg.connect(conninfo(), connect_timeout=3) as conn:
        return conn.execute(sql, params).fetchall()


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/info")
def info():
    return jsonify(service=SERVICE, version=APP_VERSION, env=APP_ENV,
                   hostname=socket.gethostname())


@app.get("/api/products")
def products():
    try:
        rows = query("SELECT id, name, price, stock FROM products ORDER BY id")
    except Exception as e:
        log("db_error", error=str(e))
        return jsonify(error="database unavailable", detail=type(e).__name__), 503
    log("list_products", count=len(rows))
    return jsonify(items=[{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows])


@app.get("/api/products/<int:pid>")
def product(pid):
    try:
        rows = query("SELECT id, name, price, stock FROM products WHERE id = %s", (pid,))
    except Exception as e:
        log("db_error", error=str(e))
        return jsonify(error="database unavailable", detail=type(e).__name__), 503
    if not rows:
        log("product_not_found", product_id=pid)
        return jsonify(error="product not found", product_id=pid), 404
    r = rows[0]
    log("get_product", product_id=pid)
    return jsonify(id=r[0], name=r[1], price=r[2], stock=r[3])
