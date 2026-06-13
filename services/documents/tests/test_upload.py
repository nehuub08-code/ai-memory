from fastapi.testclient import TestClient
import io


def test_upload_document(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("DOCUMENTS_STORAGE_DIR", str(tmp_path / "docs"))
    from app.main import app

    client = TestClient(app)
    data = {
        "file": (io.BytesIO(b"hello world"), "test.txt"),
    }
    r = client.post("/api/v1/documents", files=data)
    assert r.status_code == 200
    j = r.json()
    assert "document_id" in j
