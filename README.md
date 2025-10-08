# Agile SPM ML Project

This repository implements an Agile project for Machine Learning solutions in Strategic Portfolio Management (SPM) using Scrum. It includes data pipelines, ML models for portfolio risk prediction, an API service, a dashboard, and comprehensive documentation and reporting covering the 14 activities.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Run tests
pytest -q

# Start API
uvicorn app.api:app --reload

# Start dashboard
streamlit run app/dashboard.py
```

See `docs/` for the detailed Agile process, backlog, sprint plans, and the final report.


