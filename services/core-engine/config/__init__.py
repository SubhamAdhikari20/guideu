"""Expose the Celery app so ``@shared_task`` works and ``celery -A config`` resolves."""
from .celery import app as celery_app

__all__ = ("celery_app",)
