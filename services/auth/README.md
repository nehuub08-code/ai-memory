# Auth Service

Run the Auth service (development):

1. Ensure Postgres is running (see `docker-compose.yml`).
2. Apply DB schema: `psql postgresql://postgres:postgres@localhost:5432/postgres -f infra/db/schema.sql`
3. Create a virtualenv and run:

```bash
cd services/auth
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
export AUTH_SECRET_KEY=replace-with-secret
uvicorn app.main:app --reload --port 8001
```

Health endpoint: `GET /health`
