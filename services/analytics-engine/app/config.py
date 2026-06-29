"""Runtime configuration for the analytics-engine."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# analytics-engine/  (config.py -> app -> analytics-engine)
SERVICE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_ROOT.parent.parent  # guideu/


def _default_dataset_dir() -> Path:
    """Best-effort discovery of the Travel Planning dataset for local runs."""
    candidates = [
        REPO_ROOT.parent / "Travel Planning",  # Project/Travel Planning (repo sibling)
        REPO_ROOT / "Travel Planning",
        Path("/data/travel-planning"),          # docker mount
    ]
    for candidate in candidates:
        if (candidate / "trekking_routes.csv").exists():
            return candidate
    return candidates[0]


class Settings(BaseSettings):
    """Settings sourced from environment variables (see repo-root .env.example)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key: str = Field("change-me-internal-service-token", validation_alias="ANALYTICS_API_KEY")
    host: str = Field("0.0.0.0", validation_alias="ANALYTICS_HOST")
    port: int = Field(8001, validation_alias="ANALYTICS_PORT")

    dataset_dir: Path = Field(default_factory=_default_dataset_dir, validation_alias="GUIDEU_DATASET_DIR")
    artifact_dir: Path = Field(default=SERVICE_ROOT / "artifacts", validation_alias="MODEL_ARTIFACT_DIR")
    mlflow_tracking_uri: str = Field("", validation_alias="MLFLOW_TRACKING_URI")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.artifact_dir.mkdir(parents=True, exist_ok=True)
    return settings
