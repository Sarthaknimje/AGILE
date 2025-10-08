# Agile Project Report: ML for Strategic Portfolio Management (SPM)

Pimpri Chinchwad College of Engineering, Nigdi, Pune
Department of Computer Engineering
Course: Agile Project Management

Project Title: Agile ML Solution for Strategic Portfolio Management (SPM)

Team (Scrum Team of 5):
- Product Owner: Sarthak Nimje (sarthaknimje@gmail.com)
- Scrum Master: Yash Diwan (yashmdiwan@gmail.com)
- ML Engineer: Apurva (itsapurvasb343@gmail.com)
- Data Engineer: Student D
- UI/Backend Engineer (API & Dashboard): Student E

Repository: `https://github.com/Sarthaknimje/AGILE.git`

---

## Executive Summary
This project delivers a working ML-driven analytics layer for Strategic Portfolio Management using Scrum. We generate an SPM-like synthetic dataset, engineer features, train a baseline RandomForest model to classify portfolio risk (low/medium/high), serve the model via a FastAPI service with interactive Swagger (OpenAPI) documentation, and provide a Streamlit GUI dashboard for analysts. CI ensures consistent quality. The final deliverable includes this comprehensive report covering the 14 activities of FA-1 and FA-2.

---

## 1. Problem Statement
Strategic Portfolio Management (SPM) teams must allocate resources across portfolios while minimizing risk and maximizing returns. Decisions are often constrained by incomplete visibility into portfolio risk drivers. We aim to build an ML solution that classifies risk levels from portfolio attributes and factor exposures, improving decision-making speed and quality.

Objectives:
- Classify portfolio risk level (low/medium/high) to support allocation decisions.
- Offer a modern API (Swagger) for integration and a GUI (Streamlit) for analysts.
- Ensure reproducibility with pipelines, tests, and CI.

KPIs:
- Model: Accuracy ≥ 0.80; Weighted F1 ≥ 0.80 on held-out test data.
- Delivery: CI green on main; repeatable data/model runs.

---

## 2. Abstract
We built an end-to-end ML pipeline: synthetic SPM data generation, feature engineering, baseline RandomForest classifier, an inference service (FastAPI) with OpenAPI docs, and a Streamlit dashboard for EDA and interactive predictions. Work proceeds in sprints following Scrum: initiation, backlog, sprint planning, daily scrums, sprint reviews/retrospectives, and continuous improvement.

---

## 3. Introduction
- Domain: Strategic Portfolio Management and risk analytics
- Scope: Portfolio-level classification; dashboard insights for analysts
- Constraints: No proprietary data; hence synthetic generation with realistic patterns
- Success: Working vertical slice from data → model → API/GUI; documented, tested, CI-enabled

---

## 4. Proposed Architecture
- Data Layer (`app/data/generate.py`): synthetic dataset creation of portfolios with weights and factors; saved to `data/processed/portfolios.csv`.
- Model Layer (`app/models/train.py`): preprocessing (scaler), model (RandomForestClassifier, class_weight balanced), metrics (classification report), artifact stored at `models/risk_classifier.joblib`.
- Service Layer (`app/api.py`): FastAPI app exposing `/health` and `/predict` for JSON-based scoring; interactive Swagger UI at `/docs`.
- UI Layer (`app/dashboard.py`): Streamlit dashboard showing dataset snapshots, risk distribution, and a form for live prediction.
- Config (`app/core/config.py`): central settings (paths, random seed).
- Utilities (`app/services/infer.py`): model loading and structured predictions.
- CI (`.github/workflows/ci.yml`): ruff (lint), mypy (types), pytest (tests).

Data Flow:
Raw synthetic → clean/features → train/test split → train model → evaluate → save artifact → serve via API → explore via dashboard.

Security & Privacy:
- Synthetic data avoids PII.
- Future iterations may add request validation and auth for production.

---

## 5. Flow of Project (Lifecycle Overview)
1) Dataset synthesis and documentation
2) Feature engineering and model training
3) Evaluation and metrics reporting
4) API service and dashboard GUI
5) CI and documentation
6) Iteration and refinements

---

## 6. Analysis and Planning
Stakeholders:
- Product Owner (Sarthak): Sets vision, prioritizes backlog
- Scrum Master (Yash): Facilitates ceremonies, removes impediments
- ML Engineer (Apurva): Models, evaluation
- Data Engineer (D): Pipelines
- UI/Backend (E): FastAPI/Streamlit

Assumptions:
- Synthetic data is acceptable for academic demonstration.
- Baseline tree model is sufficient for the first increment.

Risks & Mitigations:
- Data realism: tune generator distributions; later incorporate public datasets
- Overfitting: use stratified split, track weighted F1 and per-class metrics
- Operational: coverage via tests and CI; typed code where reasonable

Backlog & sprints are detailed in `docs/backlog.md`.

---

## 7. Outcome (Increment Summary)
- Dataset (1,000 portfolios) with factors, allocations, returns/volatility
- Baseline model with saved artifact and reproducible metrics
- API with request/response schema via Pydantic and Swagger UI
- Streamlit GUI for quick analyst interaction
- CI green on commit; unit tests pass

Artifacts:
- `data/processed/portfolios.csv`
- `models/risk_classifier.joblib`
- `docs/metrics.json` (classification report)

---

## 8. Conclusion
We delivered a complete, reproducible vertical slice for SPM risk analytics. Stakeholders can explore data, query predictions through a documented API, and interact via a GUI. The platform is ready for iteration: richer features (drawdown, correlations), explainability (SHAP), and deployment hardening.

---

## 9. References
- scikit-learn User Guide (classification pipelines)
- FastAPI Documentation (OpenAPI/Swagger integration)
- Streamlit Documentation (interactive dashboards)

---

# Agile Activities (14 Steps)

## Step 1: Project Initiation
- Goal: Improve SPM decision-making using ML risk classification and insights.
- Product Vision: An explainable ML service and dashboard for portfolio risk that integrates with SPM workflows.
- Stakeholder Alignment: Roles assigned; delivery cadence agreed; success criteria defined.

See `docs/initiation.md` for full initiation notes.

## Step 2: Form the Scrum Team
- Roles:
  - Product Owner: Sarthak Nimje — vision, backlog priority
  - Scrum Master: Yash Diwan — ceremonies, impediment removal
  - Development Team: Apurva (ML), Student D (Data), Student E (API/UI)

## Step 3: Product Backlog Creation
- Requirements: risk classification, factor analytics, API for integration, GUI for analysts
- User Stories: captured per Epic (Data, Model, API, Dashboard, CI)
- Prioritization: focus on vertical slice delivery first

Backlog & sprint plan: `docs/backlog.md`.

## Step 4: Sprint Planning
- Sprint-1: Data prep and documentation
- Sprint-2: Baseline model and metrics
- Sprint-3: API + dashboard
- Sprint-4: Reporting, polish, and CI verification

## Step 5: Data Preparation (Sprint-1)
- Synthetic data generation: `app/data/generate.py`
- Outputs saved to `data/processed/portfolios.csv`
- Data dictionary: `docs/data.md`

Key Features:
- Portfolio allocations (equity/bond/alt)
- Factor exposures (mkt/size/value/mom)
- Return, volatility, Sharpe ratio
- Risk level labeling via quantiles

## Step 6: Model Development (Sprint-2+)
- Model: RandomForestClassifier with class balancing
- Preprocessing: StandardScaler on numeric features in a scikit-learn `Pipeline`
- Train/test: stratified split
- Metrics: accuracy, precision/recall/F1 per class + weighted averages

Artifacts:
- Trainer: `app/models/train.py`
- Saved model: `models/risk_classifier.joblib`
- Metrics JSON: `docs/metrics.json`

## Step 7: Daily Scrum
Template used (see `docs/scrum.md`): yesterday/today/blockers. Scrum Master (Yash) ensures the team is unblocked.

## Step 8: Sprint Review and Demo
- Demo flow: Dataset snapshot → metrics → API request via Swagger → Streamlit prediction demo
- Feedback examples:
  - Add GUI prediction inputs
  - Expose model input schema in docs clearly

## Step 9: Sprint Retrospective
- Went well: modular code, CI green, early vertical slice
- Improve: add feature importance, batch infer endpoint, dockerization
- Actions: add user stories for explainability and batch scoring

## Step 10: Iterate and Refine
- CI: `.github/workflows/ci.yml` for lint/type-check/tests
- Metric tracking: monitor class balance and weighted metrics
- Automation: scripts via `python -m` modules; future Makefile and Docker

## Step 11: Deployment and Integration
- Local deployment instructions (below) validated end-to-end
- Future: container images, cloud deployment, API gateway security

## Step 12: Monitoring and Maintenance
- Monitor model distribution shifts by comparing inference inputs vs. training
- Maintenance: periodic retraining; CI prevents regressions

## Step 13: Project Closure
- Review goals vs outcomes: vertical slice completed, KPIs met on synthetic set
- Documentation: this report, `README.md`, architecture, backlog, scrum notes, metrics

## Step 14: Final Report (This Document)
- Includes problem statement, abstract, intro, architecture, flow, plan, outcomes, conclusion, references, and the 14 Scrum steps with artifacts and instructions.

---

# How To Run (Detailed)

## Prerequisites
- Python 3.10+

## Setup
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Data Generation
```bash
python -m app.data.generate
# Output: data/processed/portfolios.csv
```

## Train Model
```bash
python -m app.models.train
# Output: models/risk_classifier.joblib
# Metrics: docs/metrics.json (created during tooling run in our setup)
```

## Run API (Swagger/OpenAPI)
```bash
uvicorn app.api:app --reload
# Visit http://127.0.0.1:8000/docs for Swagger UI
# Endpoints:
#  - GET /health -> {"status": "ok"}
#  - POST /predict -> PredictResponse
```

Sample request body for `/predict` (via Swagger "Try it out"):
```json
{
  "rows": [
    {
      "avg_return": 0.06,
      "volatility": 0.12,
      "sharpe_ratio": 0.35,
      "size": 1000000,
      "equity_weight": 0.6,
      "bond_weight": 0.3,
      "alt_weight": 0.1,
      "factor_mkt": 0.0,
      "factor_size": 0.2,
      "factor_value": -0.1,
      "factor_mom": 0.05
    }
  ]
}
```
Expected response:
```json
{
  "predictions": ["medium"]
}
```

## Run Streamlit Dashboard (GUI)
```bash
streamlit run app/dashboard.py
```
Dashboard features:
- Dataset snapshot table (first rows)
- Risk distribution histogram
- Interactive prediction form (inputs for all model features) with result banner

Troubleshooting tips:
- If the dashboard cannot find the dataset, run `python -m app.data.generate`.
- If prediction fails due to missing model, run `python -m app.models.train`.

---

# Governance, Quality, and Metrics

## Roles & Responsibilities
- Sarthak (PO): Defines scope, approves backlog priorities, accepts increments
- Yash (SM): Facilitates Scrum events, removes blockers, ensures team cadence
- Apurva (ML): Model design, training, and evaluation
- Student D (Data): Data generation and feature engineering
- Student E (API/UI): FastAPI and Streamlit implementation

## Definition of Done (DoD)
- Code merged to `main` with passing CI (ruff, mypy, pytest)
- Documentation updated (`README.md`, `docs/`)
- Usable increment (API and/or dashboard as applicable)

## Engineering Metrics
- Test results: `pytest -q` all green
- Lint/type checks: no errors on CI
- Model metrics: accuracy & per-class precision/recall/F1 in `docs/metrics.json`

---

# Future Work
- Explainability: SHAP values and feature importance plots
- Data realism: include additional factors and correlations, scenario stress tests
- Batch scoring endpoint and CSV upload in GUI
- Packaging and Docker images for deployment
- AuthZ/AuthN for production environments

---

# Appendix

## Key Files
- `app/data/generate.py` — synthetic data generator
- `app/models/train.py` — training pipeline and artifact saving
- `app/services/infer.py` — model loading and inference
- `app/api.py` — FastAPI app with `/docs` Swagger UI
- `app/dashboard.py` — Streamlit GUI
- `docs/metrics.json` — evaluation metrics snapshot
- `docs/backlog.md` — product backlog and sprints
- `docs/scrum.md` — ceremonies template
- `.github/workflows/ci.yml` — CI pipeline

## Quick Commands
```bash
# Setup
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

# E2E (data + model + tests)
python -m app.data.generate && python -m app.models.train && pytest -q

# API + GUI
uvicorn app.api:app --reload &
streamlit run app/dashboard.py
```

---

# Jira Process and Deployment Guide

## Jira (Planning and Tracking)
- Project: SPM (Scrum) with board columns Backlog → Selected → In Progress → In Review → Done
- Issue Types: Epic, Story, Task, Bug; Epics for Data/Model/API/Dashboard/CI/Deployment
- Branching: `feature/SPM-<issue>-<slug>`; commits and PRs reference issue key
- Import template: see `docs/jira_import.csv`
- Operating rhythm: 2-week sprints; ceremonies per `docs/scrum.md`

## Deployment (Local Containers)
Prerequisites: Docker and docker-compose

Build and run both API and dashboard:
```bash
docker compose up --build
# API: http://localhost:8000/docs
# Dashboard: http://localhost:8501
```

Stop services:
```bash
docker compose down
```

Image details:
- Single base image (`agile-spm-ml`) runs API by default (UVicorn)
- Dashboard service overrides CMD to run Streamlit
