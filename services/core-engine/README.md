# GuideU — core-engine (Django + DRF)

The authoritative business backend: accounts/RBAC, tourism catalog, bookings,
payments/escrow, trekking permits, reviews, favorites, notifications, analytics
events, anti-scam (trust), gamification and an audit trail. It owns the
PostgreSQL source of truth and publishes domain events to Redis for the
realtime engine.

## Domain apps (`src/`)
| App | Responsibility |
|---|---|
| `common` | shared base models, pagination, permissions, event bus, ML client |
| `authentication` | custom `User`, roles, JWT, guide/tourist profiles |
| `catalog` | dataset-backed routes, guide registry, events, regions, pricing |
| `bookings` | tour packages, booking lifecycle, itineraries (links to routes) |
| `permits` | TIMS / National Park permit applications |
| `payments` | transactions + escrow ledger (eSewa / Khalti hooks) |
| `reviews` | guide/route reviews with moderation + rating aggregation |
| `favorites` | wishlist + recently-viewed |
| `notifications` | in-app notifications, mirrored to realtime |
| `analytics` | user event tracking + funnel |
| `trust` | scam reports + the anti-scam price-check (calls the ML service) |
| `gamification` | badges, awards, leaderboard |
| `audit` | append-only audit log middleware |

## Run locally
```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed_from_dataset          # ingest the synthetic dataset
uv run python manage.py createsuperuser
uv run python manage.py runserver
```
Defaults to SQLite (zero-setup). Set `DJANGO_DB_ENGINE=django.db.backends.postgresql`
(+ creds) for Postgres. Production settings (`config.settings.prod`) require a real
DB and secret and fail fast otherwise.

## Key URLs
- `GET /api/docs/` — Swagger UI (OpenAPI via drf-spectacular)
- `POST /api/v1/auth/token/` — obtain JWT
- `GET /api/v1/catalog/routes/` — trekking routes (public)
- `GET /api/v1/catalog/pricing-benchmarks/lookup/?service_type=Porter&region=Langtang`
- `POST /api/v1/trust/price-check/` — anti-scam "is this fair?"
- `/admin/` — Django admin

## Tests
```bash
uv run pytest
```

See `../../docs/` for architecture, the dataset mapping, ADRs and ML notes.
