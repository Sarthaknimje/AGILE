from __future__ import annotations

from fastapi import FastAPI, Depends, UploadFile
from pydantic import BaseModel, Field
from typing import List

from app.services.infer import RiskModelService
from app.models.db import get_session, engine
from app.models import Base
from app.models.jira import JiraIssue, JiraIssueCreate, JiraIssueRead
from sqlalchemy.orm import Session
import csv

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


# --- DB setup on startup ---
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


# --- Jira endpoints ---
@app.get("/jira/issues", response_model=List[JiraIssueRead])
def list_issues(session: Session = Depends(get_session)) -> List[JiraIssueRead]:
    issues = session.query(JiraIssue).order_by(JiraIssue.id.desc()).all()
    return [JiraIssueRead.model_validate(i) for i in issues]


@app.post("/jira/issues", response_model=JiraIssueRead)
def create_issue(payload: JiraIssueCreate, session: Session = Depends(get_session)) -> JiraIssueRead:
    issue = JiraIssue(
        issue_type=payload.issue_type,
        summary=payload.summary,
        description=payload.description,
        epic_link=payload.epic_link,
        priority=payload.priority,
    )
    session.add(issue)
    session.commit()
    session.refresh(issue)
    return JiraIssueRead.model_validate(issue)


@app.post("/jira/import", response_model=int)
def import_csv(file: UploadFile, session: Session = Depends(get_session)) -> int:
    # Expecting header: Issue Type,Summary,Description,Epic Link,Priority
    reader = csv.DictReader(line.decode("utf-8") for line in file.file)
    count = 0
    for row in reader:
        issue = JiraIssue(
            issue_type=row.get("Issue Type", "Task"),
            summary=row.get("Summary", ""),
            description=row.get("Description") or None,
            epic_link=row.get("Epic Link") or None,
            priority=row.get("Priority") or None,
        )
        session.add(issue)
        count += 1
    session.commit()
    return count
