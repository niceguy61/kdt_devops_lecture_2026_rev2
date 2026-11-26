"""order-api 단위 테스트 — DB · Redis · catalog-api 없이 돌아간다 (3주차 2일차 CI)."""
import app as order


def client():
    order.app.config["TESTING"] = True
    return order.app.test_client()


def test_health_ok():
    res = client().get("/health")
    assert res.status_code == 200


def test_ready_fails_without_dependencies(monkeypatch):
    # 의존 서비스가 없으면 /ready 는 503 — /health 와 다르다
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.setattr(order, "REDIS_HOST", "127.0.0.1")
    res = client().get("/ready")
    assert res.status_code == 503
    assert res.get_json()["status"] == "not ready"


def test_order_returns_503_when_catalog_is_down(monkeypatch):
    # 상품 서비스가 응답하지 않으면 주문을 저장하지 않고 503을 돌려줘야 한다
    monkeypatch.setattr(order, "CATALOG_URL", "http://127.0.0.1:9")
    monkeypatch.setattr(order, "CATALOG_TIMEOUT", 0.5)
    res = client().post("/api/orders", json={"product_id": 1})
    assert res.status_code == 503
    assert res.get_json()["error"] == "catalog unavailable"
