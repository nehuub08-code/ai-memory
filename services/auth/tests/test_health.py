from fastapi.testclient import TestClient


def test_health(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # import app after setting env so DB metadata is created
    from app.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
