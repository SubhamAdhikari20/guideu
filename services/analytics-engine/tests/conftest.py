from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def api_headers() -> dict[str, str]:
    return {"X-API-Key": get_settings().api_key}


@pytest.fixture(scope="session")
def dataset_available() -> bool:
    return (get_settings().dataset_dir / "trekking_routes.csv").exists()


@pytest.fixture(autouse=True)
def _skip_without_dataset(request, dataset_available):
    """Skip data-dependent tests when the Travel Planning dataset is absent (e.g. CI)."""
    if request.node.get_closest_marker("needs_dataset") and not dataset_available:
        pytest.skip("Travel Planning dataset not available")


def pytest_configure(config):
    config.addinivalue_line("markers", "needs_dataset: test requires the synthetic dataset")
