# Documents Service

Run the Documents service (development):

```bash
cd services/documents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
uvicorn app.main:app --reload --port 8004
```

Upload endpoint: `POST /api/v1/documents` (multipart/form-data file field `file`).
