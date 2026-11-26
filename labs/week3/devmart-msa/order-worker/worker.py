"""DevMart 주문 처리기(order-worker) — 3주차 MSA 실습용.

Redis 큐에서 주문 메시지를 하나씩 꺼내 '처리'하고(결제·재고 확인을 흉내 내 잠깐 기다림)
orders DB의 상태를 'completed'로 바꾼다. 웹 요청을 받지 않으므로 포트가 없다.
"""
import json
import os
import socket
import time

import psycopg
import redis

SERVICE = "order-worker"
QUEUE_NAME = os.getenv("QUEUE_NAME", "orders")
WORK_SECONDS = float(os.getenv("WORK_SECONDS", "1"))
WORKER_ID = socket.gethostname()


def log(event, **fields):
    print(json.dumps({"service": SERVICE, "worker": WORKER_ID, "event": event, **fields},
                     ensure_ascii=False), flush=True)


def conninfo():
    return (f"host={os.environ['DB_HOST']} port={os.getenv('DB_PORT', '5432')} "
            f"dbname={os.getenv('DB_NAME', 'orders')} user={os.getenv('DB_USER', 'devmart')} "
            f"password={os.getenv('DB_PASSWORD', '')}")


def main():
    q = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379,
                    socket_connect_timeout=2, socket_timeout=10)
    log("worker_started", queue=QUEUE_NAME, work_seconds=WORK_SECONDS)
    while True:
        try:
            item = q.brpop(QUEUE_NAME, timeout=5)  # 최대 5초 기다리며 메시지 하나를 꺼낸다
        except redis.exceptions.RedisError as e:  # 연결 끊김 · 시간 초과 — 죽지 않고 다시 시도
            log("queue_error", error=str(e))
            time.sleep(2)
            continue
        if item is None:
            continue  # 5초 동안 할 일이 없었다
        msg = json.loads(item[1])
        order_id, request_id = msg["order_id"], msg["request_id"]
        log("order_processing", request_id=request_id, order_id=order_id)
        time.sleep(WORK_SECONDS)
        try:
            with psycopg.connect(conninfo(), connect_timeout=3) as conn:
                conn.execute("UPDATE orders SET status = 'completed', processed_at = now(), "
                             "processed_by = %s WHERE id = %s", (WORKER_ID, order_id))
            log("order_completed", request_id=request_id, order_id=order_id)
        except Exception as e:
            log("db_error", request_id=request_id, order_id=order_id, error=str(e))


if __name__ == "__main__":
    main()
