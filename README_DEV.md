# Local Development (No Docker)

This project can be run locally without Docker by using a Python virtual environment and a local SQLite database.

Files:
- `start-dev.sh` — creates a venv, installs service requirements, sets `DATABASE_URL` to `sqlite:///dev.db`, and launches all FastAPI services and the Next.js frontend (if `npm` is available).
- `stop-dev.sh` — stops services started by `start-dev.sh`.

Quick start (macOS, zsh):

```bash
cd '/Users/sakshsmac/AI Memory Assistent'
./start-dev.sh
```

Then open http://localhost:3000 for the frontend (if Node/npm is installed and the script started it).

Health endpoints:
- Auth: http://localhost:8001/health
- User: http://localhost:8002/health
- Notes: http://localhost:8003/health
- Documents: http://localhost:8004/health
- Search: http://localhost:8005/health
- AI: http://localhost:8006/health

Stopping:

```bash
./stop-dev.sh
```

Notes:
- The dev DB is `dev.db` in the repo root. The services will auto-create tables when running against SQLite.
- If you prefer Postgres, install Postgres locally and set `DATABASE_URL` accordingly before running services.
