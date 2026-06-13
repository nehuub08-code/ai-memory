import os
from fastapi.testclient import TestClient


def test_signup_and_login(monkeypatch):
    # run against sqlite in-memory
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    from app.main import app

    client = TestClient(app)

    signup_resp = client.post(
        "/api/v1/auth/signup",
        json={"email": "inttest@example.com", "password": "pass1234", "name": "Integration"},
    )
    assert signup_resp.status_code == 200
    data = signup_resp.json()
    assert "access_token" in data

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "inttest@example.com", "password": "pass1234"},
    )
    assert login_resp.status_code == 200
    ldata = login_resp.json()
    assert "access_token" in ldata
