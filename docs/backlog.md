# Product Backlog and Sprint Plan

## Epics
- E1: Data Acquisition and Preparation
- E2: Baseline ML Model for Risk Prediction
- E3: API Service for Model Inference
- E4: Dashboard and Visualization
- E5: Evaluation, Reporting, and CI

## User Stories (High Priority First)
1. As a PO, I want a synthetic SPM dataset so that we can prototype quickly. (E1)
2. As an ML engineer, I want cleaned and feature-engineered data to train a baseline model. (E1)
3. As an analyst, I want a model that predicts portfolio risk level so I can segment portfolios. (E2)
4. As an integrator, I want an API endpoint to request predictions for new portfolios. (E3)
5. As a decision maker, I want a dashboard to visualize risk metrics by portfolio. (E4)
6. As a team, I want tests and CI to ensure quality and reproducibility. (E5)

## Sprint-1 (2 weeks): Data Preparation
- Generate synthetic dataset (portfolios, assets, factors)
- Clean, impute, normalize
- Feature engineering (returns, volatility, factor exposures)
- Deliverable: processed dataset and data docs

## Sprint-2 (2 weeks): Baseline Model
- Train baseline classifier for risk level
- Evaluate with accuracy, F1, ROC-AUC
- Save model artifact
- Deliverable: model + metrics report

## Sprint-3 (2 weeks): API and Dashboard
- FastAPI endpoints: health, predict
- Streamlit dashboard for portfolios
- Deliverable: running service and dashboard

## Sprint-4 (1 week): Evaluation and Report
- Refine features and thresholds
- Finalize documentation and report
- Deliverable: comprehensive report and presentation
