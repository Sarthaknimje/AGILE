import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from app.core.config import settings
from app.services.infer import RiskModelService

st.set_page_config(page_title="SPM Dashboard", layout="wide")

st.title("Strategic Portfolio Management - Risk Dashboard")

processed = Path(settings.data_dir) / "processed" / "portfolios.csv"
if not processed.exists():
    st.warning("Dataset not found. Generate data with: python -m app.data.generate")
else:
    df = pd.read_csv(processed)
    st.subheader("Dataset Snapshot")
    st.dataframe(df.head(20))

    st.subheader("Risk Distribution")
    fig = px.histogram(df, x="risk_level", color="risk_level")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Try Prediction")
cols = st.columns(3)
with cols[0]:
    avg_return = st.number_input("avg_return", value=0.06)
    volatility = st.number_input("volatility", value=0.12)
    sharpe_ratio = st.number_input("sharpe_ratio", value=0.35)
    size = st.number_input("size", value=1_000_000.0)
with cols[1]:
    equity_weight = st.number_input("equity_weight", value=0.6)
    bond_weight = st.number_input("bond_weight", value=0.3)
    alt_weight = st.number_input("alt_weight", value=0.1)
with cols[2]:
    factor_mkt = st.number_input("factor_mkt", value=0.0)
    factor_size = st.number_input("factor_size", value=0.0)
    factor_value = st.number_input("factor_value", value=0.0)
    factor_mom = st.number_input("factor_mom", value=0.0)

if st.button("Predict Risk"):
    try:
        svc = RiskModelService()
        row = {
            "avg_return": avg_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "size": size,
            "equity_weight": equity_weight,
            "bond_weight": bond_weight,
            "alt_weight": alt_weight,
            "factor_mkt": factor_mkt,
            "factor_size": factor_size,
            "factor_value": factor_value,
            "factor_mom": factor_mom,
        }
        pred = svc.predict([row])[0]
        st.success(f"Predicted risk level: {pred}")
    except Exception as e:
        st.error(f"Error predicting. Ensure model is trained. Details: {e}")
        st.info("Train model with: python -m app.models.train")
