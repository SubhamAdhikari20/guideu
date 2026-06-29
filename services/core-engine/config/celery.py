"""Celery application for the GuideU core engine.

Background jobs: async notification fan-out, booking expiry sweeps, and nightly
hooks that ask the analytics-engine to retrain. The worker is started with
``celery -A config worker`` (see docker-compose / Makefile).
"""
from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("guideu")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:  # pragma: no cover - smoke task
    print(f"Celery request: {self.request!r}")
