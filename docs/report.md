# Agile Project Report: ML for Strategic Portfolio Management (SPM)

Pimpri Chinchwad College of Engineering, Nigdi, Pune
Department of Computer Engineering
Course: Agile Project Management

Team (Scrum Team of 5):
- Product Owner: Student A
- Scrum Master: Student B
- ML Engineer: Student C
- Data Engineer: Student D
- UI/Backend Engineer: Student E

Repo: `https://github.com/Sarthaknimje/AGILE.git`

---

## 1. Problem statement
Strategic Portfolio Management (SPM) needs reliable, explainable ML insights to optimize portfolio performance, allocate resources efficiently, and control risk. We build an ML solution to classify portfolio risk levels and surface key drivers, supporting better decision-making.

## 2. Abstract
We implement an end-to-end ML pipeline: synthetic SPM dataset generation, feature engineering, a baseline risk classifier (Random Forest), and serving via FastAPI with a Streamlit dashboard for analytics. The project is executed using Scrum across 14 activities, with iterative sprints, CI, and comprehensive documentation.

## 3. Introduction
- Domain: Portfolio analytics for SPM
- Objective: Predict portfolio risk level (low/medium/high) from portfolio attributes and factor exposures
- Constraints: Reproducibility, transparency of metrics, incremental delivery
- Deliverables: Data pipeline, ML model, API, dashboard, CI, and documentation

## 4. Proposed Architecture
- Data Layer: Synthetic generator (`app/data/generate.py`), persisted to `data/processed/portfolios.csv`
- Model Layer: Training pipeline with preprocessing and RandomForest (`app/models/train.py`), artifact saved to `models/risk_classifier.joblib`
- Service Layer: FastAPI (`app/api.py`) exposes `/health` and `/predict`
- UI Layer: Streamlit (`app/dashboard.py`) for dataset exploration and on-the-fly predictions
- Config: Centralized in `app/core/config.py`
- CI: GitHub Actions (`.github/workflows/ci.yml`) for lint/type-check/tests

Data flow: Raw (synthetic) → clean/feature → train/test split → train → evaluate → save model → serve via API → visualize via dashboard.

## 5. Flow of Project (High-level)
1) Data ingestion 2) Cleaning 3) Feature engineering 4) Train 5) Evaluate 6) Serve API 7) Dashboard 8) Iterate/Deploy.

## 6. Analysis and Planning
- Stakeholders: Product Owner (prioritizes), SPM analysts (consumers), Dev team
- Assumptions: Synthetic data approximates SPM characteristics; baseline model acceptable for first increment
- Risks: Data realism, overfitting, metric drift, UX clarity
- Mitigations: Clear metrics, modular pipeline, iterative feature refinement

Backlog and Sprint plan: see `docs/backlog.md`.

## 7. Outcome (Current Increment)
- Dataset: 1,000 synthetic portfolios with factors and weights
- Baseline Model: RandomForest classifier for risk level
- API: Predict from JSON inputs
- Dashboard: Explore risk distribution and run single-sample predictions
- CI: Tests and linting pass on push/PR

## 8. Conclusion
The baseline delivers a working vertical slice: data → model → service → UI, enabling early feedback and iterative improvement.

## 9. References
- scikit-learn: classification, model selection
- FastAPI: service development
- Streamlit: dashboarding

---

# Agile Activities (FA-1 and FA-2)

## Step 1: Project Initiation
- Goal Definition: Improve decision-making via risk-level predictions and insights
- Product Vision: An ML-powered analytics layer providing SPM risk segmentation and explainability through an accessible API and dashboard
- Stakeholder Alignment: Product Owner, Scrum Master, SPM analysts, dev team

See `docs/initiation.md` for more details.

## Step 2: Form the Scrum Team
- Roles assigned as listed above; responsibilities clarified (vision, facilitation, development/testing)

## Step 3: Product Backlog Creation
- Requirements gathered: risk analysis, factor sensitivities, dashboard exploration
- User stories split across epics (Data, Model, API, Dashboard, CI)
- Prioritization based on business value and feasibility

See `docs/backlog.md`.

## Step 4: Sprint Planning
- Sprint-1 Goal: Deliver cleaned dataset and features
- Sprint-2 Goal: Baseline risk classifier with metrics
- Sprint-3 Goal: API + dashboard vertical slice
- Sprint-4 Goal: Evaluation/reporting polish

## Step 5: Data Preparation (First Sprint)
- Data Acquisition: Synthetic generation for reproducibility
- Cleaning & Preprocessing: Normalization via pipeline, feature selection defined in code

Artifacts:
- Generator: `app/data/generate.py`
- Output: `data/processed/portfolios.csv`

## Step 6: Model Development (Subsequent Sprints)
- Model Selection: RandomForestClassifier (balanced class weights)
- Training/Testing: `train_test_split` with stratification, standardized features
- Feature Engineering: Returns, volatility, Sharpe, asset weights, factors

Artifacts:
- Training: `app/models/train.py`
- Model: `models/risk_classifier.joblib`
- Metrics (example excerpt in `docs/metrics.json`): precision/recall/F1 per class, weighted averages, accuracy

## Step 7: Daily Scrum
- 15 minutes: yesterday/today/blockers; notes kept sprint-wise
- Impediments escalated to Scrum Master

Templates in `docs/scrum.md`.

## Step 8: Sprint Review and Demo
- Demo scope: dataset, metrics printout, API curl, dashboard walkthrough
- Stakeholder feedback recorded; backlog updated accordingly

## Step 9: Sprint Retrospective
- What went well: fast iteration, CI green, clear interfaces
- Improvements: add SHAP/feature importance, dataset realism, batch prediction UI
- Action items: plan feature importance and batch scoring story for next sprint

## Step 10: Iterate and Refine
- Continuous Integration: Workflow runs `ruff`, `mypy`, and `pytest`
- Model Evaluation: Track weighted F1 and class balance
- Automation: Scripts via module entry points; future: Makefile or task runner

## Step 11: Deployment and Integration
- Local deployment instructions below (API + dashboard)
- Future: containerization and cloud deployment

## Step 12: Monitoring and Maintenance
- Monitor: API logs, inference distribution vs. training
- Maintenance: periodic retraining as factor regimes shift, automated tests in CI

## Step 13: Project Closure
- Final Review: Verify goals met (working vertical slice, metrics reported, GUI ready)
- Documentation: Code comments, this report, `docs/*`, CI logs

## Step 14: Full Report Prepared (this document)
- Problem statement, Abstract, Introduction, Architecture, Flow, Analysis & Planning, Outcome, Conclusion, References, and Agile steps 1–14

---

# How to Run

## Prerequisites
- Python 3.10+

## Setup
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Generate Data and Train Model
```bash
python -m app.data.generate
python -m app.models.train
```

## Run API (FastAPI)
```bash
uvicorn app.api:app --reload
# Open http://127.0.0.1:8000/docs for Swagger UI
```

## Run Dashboard (Streamlit GUI)
```bash
streamlit run app/dashboard.py
```

The dashboard shows dataset snapshots and allows interactive single-sample predictions using the trained model. Ensure `models/risk_classifier.joblib` exists (train step above) before predicting.
