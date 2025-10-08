from pathlib import Path

from app.data.generate import generate_synthetic_portfolios
from app.models.train import train_and_save


def test_generate_data_shape():
    df = generate_synthetic_portfolios(100)
    assert len(df) == 100
    assert {"avg_return", "volatility", "risk_level"}.issubset(df.columns)


def test_train_and_save(tmp_path: Path):
    # Save synthetic data to temp
    df = generate_synthetic_portfolios(200)
    data_file = tmp_path / "portfolios.csv"
    df.to_csv(data_file, index=False)

    result = train_and_save(data_file)
    assert Path(result["model_path"]).exists()
    assert "accuracy" in result["metrics"]["weighted avg"]
