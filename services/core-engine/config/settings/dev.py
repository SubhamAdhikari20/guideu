"""Development settings — zero-setup local runs.

Defaults to SQLite so the project boots with no external services, but honours
``DJANGO_DB_ENGINE=postgresql`` (+ creds) when Postgres is available.
"""
from __future__ import annotations

from .base import *  # noqa: F401,F403
from .base import REST_FRAMEWORK

DEBUG = True

# Permissive CORS in development only.
CORS_ALLOW_ALL_ORIGINS = True

# Print emails to the console instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Make domain events fire immediately so they are observable without a worker.
EVENTS_PUBLISH_EAGER = True

# Browsable API is handy while developing.
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
)
