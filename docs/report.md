# Agile Project Report: ML for Strategic Portfolio Management (SPM)

## 1. Problem statement
Strategic Portfolio Management needs data-driven insights to optimize portfolio performance, allocate resources efficiently, and manage risk. We implement ML models and analytics to support decision-making using an Agile Scrum process.

## 2. Abstract
We develop a data pipeline, baseline ML models for portfolio risk prediction, an API, and a dashboard. We follow Scrum across 14 activities: initiation to closure and reporting.

## 3. Introduction
- Domain: SPM, focusing on risk prediction and allocation insights.
- Approach: ML-driven analytics with reproducible pipelines.
- Stakeholders: Product Owner, Scrum Master, SPM analysts, data/ML engineers.

## 4. Proposed Architecture
- Data: synthetic SPM dataset (portfolios, assets, factors).
- Processing: ETL → feature engineering → model training.
- Model: tree-based baseline for risk classification; regression for expected drawdown.
- Serving: FastAPI service; Streamlit dashboard.
- Storage: versioned artifacts via joblib; model registry folder.
- CI: lint, type-check, tests via GitHub Actions.

## 5. Flow of Project
1) Data ingestion 2) Cleaning 3) Feature engineering 4) Model training 5) Evaluation 6) API 7) Dashboard 8) Deploy.

## 6. Analysis and Planning
- Backlog prioritized by business value and feasibility. See `docs/backlog.md`.
- Sprint-1: data prep; Sprint-2: baseline model; Sprint-3: API and dashboard; Sprint-4: evaluation/report.

## 7. Outcome
- Working ML baseline with metrics and serving endpoints.
- Dashboard visualizations for portfolio risk segments.

## 8. Conclusion
The Agile process enabled iterative delivery of SPM ML capabilities with stakeholder feedback.

## 9. References
- scikit-learn docs
- FastAPI docs
- Streamlit docs
