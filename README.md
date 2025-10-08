# Agile SPM ML Project

This repository implements an Agile project for Machine Learning solutions in Strategic Portfolio Management (SPM) using Scrum. It includes data pipelines, ML models for portfolio risk prediction, an API service, a dashboard, and comprehensive documentation and reporting covering the 14 activities.

## Quick Start

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Generate data and train
python -m app.data.generate
python -m app.models.train

# Run tests
pytest -q

# Start API (Swagger at /docs)
uvicorn app.api:app --reload

# Start GUI Dashboard
streamlit run app/dashboard.py
```

## Documentation
- Full report (Steps 1–14): `docs/report.md`
- Initiation: `docs/initiation.md`
- Backlog & Sprint Plan: `docs/backlog.md`
- Architecture: `docs/architecture.md`
- Data Dictionary: `docs/data.md`

## Repository
`https://github.com/Sarthaknimje/AGILE.git`


