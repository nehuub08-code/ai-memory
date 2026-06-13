# Search Service

Run the Search service (development):

```bash
cd services/search
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
uvicorn app.main:app --reload --port 8005
```

Search endpoint: `POST /api/v1/search/query` with JSON `{q, top_k}`.
