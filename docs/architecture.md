# Architecture

## Components
- Data layer: synthetic generator, cleaning, feature engineering
- Model layer: training pipeline, model registry (`models/`)
- Service layer: FastAPI app for inference
- UI layer: Streamlit dashboard
- CI: GitHub Actions for tests and linting

## Data Flow
Raw data → cleaning → features → train/test split → train model → evaluate → save artifact → serve via API → visualize via dashboard.
