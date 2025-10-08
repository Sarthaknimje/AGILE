from __future__ import annotations

import os
from pathlib import Path
import numpy as np
import pandas as pd

from app.core.config import settings


def generate_synthetic_portfolios(num_portfolios: int = 1000, random_seed: int | None = None) -> pd.DataFrame:
    rng = np.random.default_rng(random_seed or settings.random_seed)

    size = rng.lognormal(mean=3.0, sigma=1.0, size=num_portfolios) * 1e6
    equity_weight = rng.beta(2, 2, size=num_portfolios)
    bond_weight = (1 - equity_weight) * rng.beta(2, 2, size=num_portfolios)
    alt_weight = np.clip(1 - equity_weight - bond_weight, 0, 1)

    factor_mkt = rng.normal(0.0, 1.0, size=num_portfolios)
    factor_size = rng.normal(0.0, 1.0, size=num_portfolios)
    factor_value = rng.normal(0.0, 1.0, size=num_portfolios)
    factor_mom = rng.normal(0.0, 1.0, size=num_portfolios)

    base_return = 0.06 + 0.02 * factor_mkt + 0.01 * factor_value + 0.005 * factor_mom
    risk = 0.10 + 0.05 * np.abs(factor_mkt) + 0.03 * equity_weight - 0.02 * bond_weight

    avg_return = rng.normal(base_return, 0.02, size=num_portfolios)
    volatility = np.clip(rng.normal(risk, 0.02, size=num_portfolios), 0.02, None)

    sharpe_ratio = (avg_return - 0.02) / np.maximum(volatility, 1e-6)

    # Risk label via quantiles
    risk_score = 0.6 * volatility - 0.2 * sharpe_ratio + 0.2 * equity_weight
    q33, q66 = np.quantile(risk_score, [0.33, 0.66])
    risk_level = np.where(
        risk_score < q33, "low", np.where(risk_score < q66, "medium", "high")
    )

    df = pd.DataFrame(
        {
            "portfolio_id": [f"P{i:05d}" for i in range(num_portfolios)],
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
            "risk_level": risk_level,
        }
    )

    return df


def save_dataset(df: pd.DataFrame, out_dir: str | Path | None = None) -> Path:
    out = Path(out_dir or settings.data_dir) / "processed"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "portfolios.csv"
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    df = generate_synthetic_portfolios()
    path = save_dataset(df)
    print(f"Saved dataset to {path}")
