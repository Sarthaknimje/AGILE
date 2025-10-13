from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any
import joblib
import pandas as pd

from app.core.config import settings


class RiskModelService:
    def __init__(self, model_path: str | Path | None = None) -> None:
        self.model_path = Path(model_path or Path(settings.model_dir) / "risk_classifier.joblib")
        try:
            obj = joblib.load(self.model_path)
            self.pipeline = obj["pipeline"]
            self.features: List[str] = list(obj["features"])  # preserve order
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model from {self.model_path}. "
                f"This usually means the model needs to be retrained. "
                f"Run: python -m app.models.train. Error: {e}"
            )

    def predict(self, rows: List[Dict[str, Any]]) -> List[str]:
        df = pd.DataFrame(rows)
        df = df[self.features]
        preds = self.pipeline.predict(df)
        return preds.tolist()
