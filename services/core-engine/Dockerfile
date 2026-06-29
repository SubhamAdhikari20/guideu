# GuideU core-engine (Django + DRF)
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

# psycopg[binary] bundles libpq, so no system Postgres libs are required.
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && uv pip install --system --no-cache .

COPY . .

EXPOSE 8000
# Migrations are applied by the compose command; default to a gunicorn server.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
