"""Settings package selector.

Keeps ``DJANGO_SETTINGS_MODULE=config.settings`` working (manage.py/wsgi/asgi
default to it) while selecting an environment via ``GUIDEU_ENV``. Deployments may
also point ``DJANGO_SETTINGS_MODULE`` directly at ``config.settings.prod``.
"""
import os

_ENV = os.environ.get("GUIDEU_ENV", "dev").lower()

if _ENV in {"prod", "production"}:
    from .prod import *  # noqa: F401,F403
else:
    from .dev import *  # noqa: F401,F403
