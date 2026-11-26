"""catalog-api 단위 테스트 — DB 없이 돌아간다 (3주차 2일차 CI)."""
import app as catalog


def client():
    catalog.app.config["TESTING"] = True
    return catalog.app.test_client()


def test_health_ok():
    res = client().get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_info_has_service_name():
    res = client().get("/api/info")
    assert res.get_json()["service"] == "catalog-api"


def test_products_without_db_returns_503(monkeypatch):
    # DB 주소가 없으면 죽지 않고 503과 이유를 돌려줘야 한다
    monkeypatch.delenv("DB_HOST", raising=False)
    res = client().get("/api/products")
    assert res.status_code == 503
    assert res.get_json()["error"] == "database unavailable"
