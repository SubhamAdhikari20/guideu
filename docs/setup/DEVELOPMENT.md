# Development Setup

## Prerequisites

| Tool | Version | Used by |
| --- | --- | --- |
| [uv](https://docs.astral.sh/uv/) | latest | core-engine, analytics-engine |
| Python | 3.12+ (managed by uv) | both Python services |
| Node.js | 20+ | real-time-engine, web_admin |
| Flutter | 3.44+ (stable) | mobile_app |
| Docker + Compose | latest | full local stack |

## One-command setup

```bash
cp .env.example .env
./scripts/setup.sh
```

This installs dependencies for every service (`uv sync`, `npm install`,
`flutter pub get`) and creates `.env` if missing.

## Running services individually

```bash
make core        # Django core-engine   → :8000
make ml          # FastAPI analytics    → :8001
make realtime    # Node Socket.IO       → :8002
cd apps/web_admin && npm run dev   # Next.js admin → :3000
cd apps/mobile_app && flutter run  # Flutter app
```

## Running the full stack

```bash
docker compose up --build
```

`docker-compose.override.yml` is auto-merged for hot-reload dev. nginx fronts the
stack on `:80`; MLflow UI on `:5000`.

## Quality checks

```bash
./scripts/lint.sh    # django check, tsc + eslint, flutter analyze
./scripts/test.sh    # pytest across the Python services
```

Per-service equivalents:

| Service | Check | Test |
| --- | --- | --- |
| core-engine | `uv run python manage.py check` | `uv run pytest` |
| analytics-engine | — | `uv run pytest` |
| real-time-engine | `npm run typecheck` / `npm run lint` | — |
| web_admin | `npm run lint` / `npm run build` | — |
| mobile_app | `flutter analyze` | `flutter test` |

## Environment variables

All variables are documented in [`../../.env.example`](../../.env.example). Never
commit a real `.env` — only `.env.example` (with placeholder/sandbox values) is
tracked.
