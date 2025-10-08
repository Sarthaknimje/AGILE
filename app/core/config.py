from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    random_seed: int = int(os.getenv("RANDOM_SEED", 42))
    model_dir: str = os.getenv("MODEL_DIR", "models")
    data_dir: str = os.getenv("DATA_DIR", "data")


settings = Settings()
