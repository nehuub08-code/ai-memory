#!/usr/bin/env bash
set -euo pipefail

# stop-dev.sh
# Stops processes launched by start-dev.sh using recorded PIDs.

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDS_DIR="$ROOT_DIR/.pids"

if [ ! -d "$PIDS_DIR" ]; then
  echo "No pids directory found ($PIDS_DIR). Nothing to stop."
  exit 0
fi

for pidfile in "$PIDS_DIR"/*.pid; do
  [ -e "$pidfile" ] || continue
  name="$(basename "$pidfile" .pid)"
  pid="$(cat "$pidfile")"
  if kill -0 "$pid" >/dev/null 2>&1; then
    echo "Stopping $name (pid $pid)"
    kill "$pid" || true
    sleep 0.5
  else
    echo "$name (pid $pid) not running"
  fi
  rm -f "$pidfile"
done

echo "Stopped."
