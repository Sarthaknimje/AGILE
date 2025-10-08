#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSV_PATH="$ROOT_DIR/docs/jira_import.csv"

echo "[1/4] Building and starting Docker services..."
docker compose up -d --build

echo "[2/4] Waiting for API to be healthy at http://localhost:8000/health ..."
for i in {1..60}; do
  if curl -fsS http://localhost:8000/health >/dev/null; then
    echo "API is healthy."
    break
  fi
  sleep 1
  if [[ "$i" -eq 60 ]]; then
    echo "API did not become healthy in time." >&2
    exit 1
  fi
done

echo "[3/4] Ensuring Jira issues are imported..."
existing_count=$(curl -fsS http://localhost:8000/jira/issues | jq length || echo 0)
if [[ "$existing_count" -eq 0 ]]; then
  if [[ -f "$CSV_PATH" ]]; then
    echo "Importing CSV from $CSV_PATH ..."
    curl -fsS -X POST -H "Content-Type: multipart/form-data" -F "file=@$CSV_PATH" http://localhost:8000/jira/import || true
  else
    echo "CSV not found at $CSV_PATH. Skipping import."
  fi
else
  echo "Issues already present ($existing_count). Skipping import."
fi

echo "[4/4] Services are ready."
echo "---------------------------"
echo "API Docs:      http://localhost:8000/docs"
echo "Health:        http://localhost:8000/health"
echo "Jira Issues:   http://localhost:8000/jira/issues"
echo "Dashboard:     http://localhost:8501"
echo "---------------------------"
echo "Done."


