#!/usr/bin/env bash
set -euo pipefail

# start-dev.sh
# Small helper to run the MEMORIA services locally WITHOUT Docker.
# It creates a Python venv, installs service requirements, configures
# a local SQLite DB (dev.db) and launches uvicorn for each FastAPI app.

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

VENV_DIR="$ROOT_DIR/.venv"
LOG_DIR="$ROOT_DIR/logs"
PIDS_DIR="$ROOT_DIR/.pids"
DB_PATH="$ROOT_DIR/dev.db"

mkdir -p "$LOG_DIR" "$PIDS_DIR" "$(dirname "$DB_PATH")"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv in $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip

echo "Installing Python requirements for services (skipping psycopg2-binary)..."
for req in services/*/requirements.txt; do
  if [ -f "$req" ]; then
    echo "  -> $req"
    # create a temporary requirements file that excludes psycopg2-binary
    tmpreq=$(mktemp)
    grep -vE "^\s*psycopg2-binary" "$req" > "$tmpreq" || true
    pip install -r "$tmpreq"
    rm -f "$tmpreq"
  fi
done

# install small extras
pip install requests || true

export DATABASE_URL="sqlite:///$DB_PATH"
export AUTH_SECRET_KEY="dev-secret-key"
export SEARCH_URL="http://localhost:8005/api/v1/search/query"
export DOCUMENTS_STORAGE_DIR="$ROOT_DIR/data/documents"
mkdir -p "$DOCUMENTS_STORAGE_DIR"

# ensure Python imports find libs/shared
export PYTHONPATH="$ROOT_DIR"

echo "Starting services (logs -> $LOG_DIR, pids -> $PIDS_DIR)"

# helper to start a service and record pid
start_service() {
  local module_path="$1"
  local port="$2"
  local name="$3"
  local logfile="$LOG_DIR/${name}.log"
  echo "Starting $name on port $port"
  nohup uvicorn "$module_path" --host 0.0.0.0 --port "$port" --reload > "$logfile" 2>&1 &
  echo $! > "$PIDS_DIR/${name}.pid"
}

start_service services.auth.app.main:app 8001 auth
start_service services.user.app.main:app 8002 user
start_service services.notes.app.main:app 8003 notes
start_service services.documents.app.main:app 8004 documents
start_service services.search.app.main:app 8005 search
start_service services.ai.app.main:app 8006 ai

echo "All backend services started."

# start frontend if npm is available
if command -v npm >/dev/null 2>&1; then
  echo "Starting frontend (Next.js)"
  (cd apps/frontend && npm install --no-audit --no-fund)
  # create frontend log file first to ensure tailing availability
  touch "$LOG_DIR/frontend.log"
  nohup bash -c "cd apps/frontend && npm run dev" > "$LOG_DIR/frontend.log" 2>&1 &
  echo $! > "$PIDS_DIR/frontend.pid"
  echo "Frontend started on http://localhost:3000"
else
  echo "npm not found: skipping frontend start. Install Node.js and run 'apps/frontend/npm install && npm run dev' yourself."
fi

echo "Done. Use './stop-dev.sh' to stop services. Tail logs in $LOG_DIR if needed."
