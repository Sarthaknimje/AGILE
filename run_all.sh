#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSV_PATH="$ROOT_DIR/docs/jira_import.csv"

echo "🚀 Starting AGILE SPM ML System..."

echo "[1/5] Setting up ML model and data..."
./setup_model.sh

echo "[2/5] Building and starting Docker services..."
docker compose up -d --build

echo "[3/5] Waiting for API to be healthy at http://localhost:8000/health ..."
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

echo "[4/5] Ensuring Jira issues are imported..."
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

echo "[5/5] Testing prediction endpoint..."
curl -fsS -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"rows":[{"avg_return":0.06,"volatility":0.12,"sharpe_ratio":0.35,"size":1000000.0,"equity_weight":0.60,"bond_weight":0.30,"alt_weight":0.10,"factor_mkt":0.0,"factor_size":0.0,"factor_value":0.0,"factor_mom":0.0}]}' || echo "Prediction test failed"

echo ""
echo "🎉 All services are ready!"
echo "---------------------------"
echo "📊 Access Points:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • AI Dashboard:      http://localhost:8501"
echo "   • Health Check:      http://localhost:8000/health"
echo "   • Jira Issues:       http://localhost:8000/jira/issues"
echo "   • Database:          localhost:5432"
echo "---------------------------"
echo "🔮 Try the AI Prediction page in the dashboard!"
echo "🤖 Gemini AI analysis is available with your API key"
echo "Done."



