# Notes Service

Run the Notes service (development):

```bash
cd services/notes
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
uvicorn app.main:app --reload --port 8003
```

Health endpoint: `GET /health`
