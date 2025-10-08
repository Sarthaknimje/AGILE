from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

from app.services.infer import RiskModelService

app = FastAPI(title="SPM Risk API", version="0.1.0")


class PortfolioRow(BaseModel):
    avg_return: float
    volatility: float
    sharpe_ratio: float
    size: float
    equity_weight: float
    bond_weight: float
    alt_weight: float
    factor_mkt: float
    factor_size: float
    factor_value: float
    factor_mom: float


class PredictRequest(BaseModel):
    rows: List[PortfolioRow] = Field(default_factory=list)


class PredictResponse(BaseModel):
    predictions: List[str]


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    service = RiskModelService()
    preds = service.predict([r.model_dump() for r in req.rows])
    return PredictResponse(predictions=preds)
