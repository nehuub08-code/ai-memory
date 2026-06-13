from fastapi.testclient import TestClient


def test_create_and_get_note(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    from app.main import app

    client = TestClient(app)
    resp = client.post("/api/v1/notes", json={"user_id": "u1", "title": "T1", "body_markdown": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == "u1"
    nid = data["id"]

    g = client.get(f"/api/v1/notes/{nid}")
    assert g.status_code == 200
    gd = g.json()
    assert gd["id"] == nid
