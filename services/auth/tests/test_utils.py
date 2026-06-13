import os


def test_password_hash_and_verify_import_after_env(monkeypatch):
    # ensure sqlite in-memory used for DB so module creates tables
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # import after env set
    from app.main import get_password_hash, verify_password, create_access_token

    pw = "s3cret"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed)


def test_create_access_token_returns_string_import_after_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    from app.main import create_access_token

    token = create_access_token({"sub": "test-user"})
    assert isinstance(token, str)
