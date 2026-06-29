"""Lightweight model registry with an optional MLflow backend.

Training writes artifacts here; inference loads the latest version. When MLflow
is installed and ``MLFLOW_TRACKING_URI`` is set, runs are also logged to MLflow —
otherwise everything is recorded in ``artifacts/model_registry.json`` so the
service has no hard dependency on a tracking server (see ADR-0006).
"""
from __future__ import annotations

import datetime as dt
import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import joblib

from app.config import get_settings

logger = logging.getLogger("guideu.ml.registry")


@dataclass
class ModelCard:
    name: str
    version: str
    artifact_path: str
    metrics: dict[str, float]
    params: dict[str, Any]
    trained_at: str
    n_train: int
    notes: str = ""


def _registry_path() -> Path:
    return Path(get_settings().artifact_dir) / "model_registry.json"


def _load_registry() -> dict[str, ModelCard]:
    path = _registry_path()
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {name: ModelCard(**card) for name, card in raw.items()}


def _save_registry(cards: dict[str, ModelCard]) -> None:
    path = _registry_path()
    path.write_text(json.dumps({k: asdict(v) for k, v in cards.items()}, indent=2), encoding="utf-8")


def save_model(
    *, name: str, model: Any, metrics: dict[str, float], params: dict[str, Any], n_train: int, notes: str = ""
) -> ModelCard:
    """Persist a trained model + its card; optionally log to MLflow."""
    settings = get_settings()
    version = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    artifact_path = Path(settings.artifact_dir) / f"{name}.joblib"
    joblib.dump(model, artifact_path)

    card = ModelCard(
        name=name,
        version=f"{name}-{version}",
        artifact_path=str(artifact_path),
        metrics={k: round(float(v), 4) for k, v in metrics.items()},
        params=params,
        trained_at=dt.datetime.now(dt.timezone.utc).isoformat(),
        n_train=n_train,
        notes=notes,
    )
    cards = _load_registry()
    cards[name] = card
    _save_registry(cards)
    _maybe_log_mlflow(card)
    logger.info("saved model %s (%s) metrics=%s", name, card.version, card.metrics)
    return card


def load_model(name: str) -> Any | None:
    cards = _load_registry()
    card = cards.get(name)
    if not card or not Path(card.artifact_path).exists():
        return None
    return joblib.load(card.artifact_path)


def get_card(name: str) -> ModelCard | None:
    return _load_registry().get(name)


def list_models() -> list[ModelCard]:
    return list(_load_registry().values())


def _maybe_log_mlflow(card: ModelCard) -> None:
    settings = get_settings()
    if not settings.mlflow_tracking_uri:
        return
    try:  # pragma: no cover - optional dependency
        import mlflow

        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment("guideu")
        with mlflow.start_run(run_name=card.version):
            mlflow.log_params(card.params)
            mlflow.log_metrics(card.metrics)
            mlflow.log_artifact(card.artifact_path)
    except Exception as exc:  # pragma: no cover
        logger.warning("MLflow logging skipped: %s", exc)
