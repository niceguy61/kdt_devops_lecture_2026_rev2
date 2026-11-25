"""DevMart 주문 서비스(order-api) — 3주차 MSA 실습용.

POST /api/orders 흐름
  1) catalog-api에 상품 가격을 묻는다 (동기 HTTP, 타임아웃 있음)
  2) orders DB에 주문을 'pending'으로 저장한다
  3) Redis 큐에 "이 주문을 처리해 주세요" 메시지를 넣는다 (비동기)
  4) 처리를 기다리지 않고 202 Accepted로 바로 답한다
"""
import json
import os
import socket
import time
import urllib.error
import urllib.request
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False

SERVICE = "order-api"
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-api:8000")
CATALOG_TIMEOUT = float(os.getenv("CATALOG_TIMEOUT", "2"))
CATALOG_RETRIES = int(os.getenv("CATALOG_RETRIES", "0"))   # 실패하면 몇 번 더 해 볼까 (2일차)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
QUEUE_NAME = os.getenv("QUEUE_NAME", "orders")


def rid():
    return request.headers.get("X-Request-ID") or uuid.uuid4().hex


def log(event, **fields):
    print(json.dumps({"service": SERVICE, "event": event, **fields}, ensure_ascii=False), flush=True)


def db():
    import psycopg
    return psycopg.connect(
        f"host={os.environ['DB_HOST']} port={os.getenv('DB_PORT', '5432')} "
        f"dbname={os.getenv('DB_NAME', 'orders')} user={os.getenv('DB_USER', 'devmart')} "
        f"password={os.getenv('DB_PASSWORD', '')}", connect_timeout=3)


def queue():
    import redis
    return redis.Redis(host=REDIS_HOST, port=6379, socket_timeout=2, socket_connect_timeout=2)


def get_product(product_id, request_id):
    """catalog-api 호출. (상태 코드, 내용)을 돌려준다.

    네트워크 오류일 때만 CATALOG_RETRIES 번 더 시도한다.
    기다리는 시간은 0.2초 → 0.4초 → 0.8초 … 로 늘린다 (지수 백오프).
    """
    req = urllib.request.Request(f"{CATALOG_URL}/api/products/{product_id}",
                                 headers={"X-Request-ID": request_id})
    for attempt in range(CATALOG_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=CATALOG_TIMEOUT) as res:
                return res.status, json.load(res)
        except urllib.error.HTTPError as e:
            return e.code, {}          # 404 같은 답은 다시 물어도 같다 → 재시도하지 않는다
        except Exception as e:  # 이름을 못 찾음, 연결 거부, 타임아웃 …
            log("catalog_error", request_id=request_id, attempt=attempt + 1, error=str(e))
            if attempt < CATALOG_RETRIES:
                time.sleep(0.2 * (2 ** attempt))
    return None, {}


@app.get("/health")
def health():
    """살아 있나? — 이 프로세스만 본다 (의존 서비스는 보지 않는다)."""
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    """일할 준비가 됐나? — DB와 큐까지 확인한다."""
    checks = {}
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        checks["db"] = "ok"
    except Exception as e:
        checks["db"] = type(e).__name__
    try:
        queue().ping()
        checks["queue"] = "ok"
    except Exception as e:
        checks["queue"] = type(e).__name__
    ok = all(v == "ok" for v in checks.values())
    return jsonify(status="ready" if ok else "not ready", checks=checks), (200 if ok else 503)


@app.get("/api/orders")
def list_orders():
    try:
        with db() as conn:
            rows = conn.execute(
                "SELECT id, product_name, quantity, total_price, status, request_id "
                "FROM orders ORDER BY id DESC LIMIT 10").fetchall()
    except Exception as e:
        log("db_error", error=str(e))
        return jsonify(error="database unavailable"), 503
    keys = ["id", "product_name", "quantity", "total_price", "status", "request_id"]
    return jsonify(items=[dict(zip(keys, r)) for r in rows], hostname=socket.gethostname())


@app.post("/api/orders")
def create_order():
    request_id = rid()
    body = request.get_json(silent=True) or {}
    product_id = body.get("product_id")
    quantity = int(body.get("quantity", 1))
    log("order_received", request_id=request_id, product_id=product_id, quantity=quantity)

    status, product = get_product(product_id, request_id)
    if status is None or status >= 500:
        return jsonify(error="catalog unavailable", request_id=request_id), 503
    if status == 404:
        return jsonify(error="product not found", request_id=request_id), 400

    total = product["price"] * quantity
    try:
        with db() as conn:
            order_id = conn.execute(
                "INSERT INTO orders (product_id, product_name, quantity, total_price, status, request_id) "
                "VALUES (%s, %s, %s, %s, 'pending', %s) RETURNING id",
                (product_id, product["name"], quantity, total, request_id)).fetchone()[0]
    except Exception as e:
        log("db_error", request_id=request_id, error=str(e))
        return jsonify(error="database unavailable", request_id=request_id), 503
    log("order_saved", request_id=request_id, order_id=order_id, total_price=total)

    try:
        queue().lpush(QUEUE_NAME, json.dumps({"order_id": order_id, "request_id": request_id}))
    except Exception as e:
        # 주의: 주문은 이미 DB에 'pending'으로 저장됐다 → 2일차 '유령 주문' 사고의 씨앗
        log("queue_error", request_id=request_id, order_id=order_id, error=str(e))
        return jsonify(error="queue unavailable", order_id=order_id, request_id=request_id), 503
    log("order_queued", request_id=request_id, order_id=order_id)
    return jsonify(order_id=order_id, status="pending", total_price=total, request_id=request_id), 202
