# Sprint 5 — Review (final sprint)

Sprint 5 completes GuideU into a demoable, thesis-ready product: the last
features (travel workspace, currency, safety SOS), app polish, security
hardening, end-to-end tests, a production deployment setup, and the thesis
documentation. As planned, it follows the real repo and the verify-and-fill-gaps
style — nothing from Sprints 1–4 was rebuilt.

## Delivered

**New features (backend + mobile)**
- **Travel workspace** — `workspace` app: trips + day-by-day items, drag-and-drop
  reorder, budget summary. Mobile: My Trips, create-trip sheet, detail page with
  a reorderable itinerary, budget bar and add-item sheet.
- **AI itinerary suggestions** — reuses the Sprint 4 route recommender to seed a
  trip ("Suggest trip"), with a fallback to top routes when the ML service is down.
- **Currency conversion** — `currency` app: NPR-based rates cached in Redis,
  refreshed by Celery Beat, static fallback. Mobile: converter page, a reusable
  `PriceDisplay` widget and a session currency preference.
- **Safety SOS** — `safety` app: `SosAlert` record + endpoint (app and device
  ready), resolve action. Mobile: an Emergency SOS sheet in Profile.

**Quality & hardening**
- Shared `EmptyState` / `ErrorRetry` widgets applied across list screens.
- Security: login (10/min) and register (5/min) rate limits, HTML-stripping
  input sanitisation for free-text, Nginx security headers, documented in
  `docs/architecture/SECURITY.md` (prod already had TLS/HSTS/JWT rotation).
- Performance: `select_related`/`prefetch_related` audit, a 30-min cache on the
  festival calendar, `docs/performance/PERFORMANCE.md`.
- Testing: an **end-to-end journey** test (register → login → catalog →
  recommendations → workspace → budget → currency → SOS) using a real JWT, plus
  per-app tests. Full suite: **21 passed**.

**Deployment & docs**
- `docker-compose.prod.yml` (gunicorn, prod settings, restart policies,
  internal-only datastores), `scripts/deploy.sh`, `docs/DEPLOYMENT.md`.
- `docs/THESIS_SUBMISSION_CHECKLIST.md`, `docs/DEMO_SCRIPT.md`.

## Honest scope (as set out in the plan)
- **Simulated:** IoT SOS — app SOS button + backend record; no real hardware, but
  the endpoint accepts the same payload a wearable would send.
- **Future work (documented):** offline map tile pre-download (needs route
  lat/lng on the catalog model), on-device chat translation (heavy native dep),
  and real hotel/flight/bus inventory APIs.

## Verification
`manage.py check` clean; `pytest` 21 passed; `flutter analyze` clean;
`flutter test` passing; web_admin `lint`/`build` clean (Sprint 4); realtime
`tsc` build clean.

## Project status
All five sprints are complete. GuideU is a working AI-powered tourism platform:
auth, catalog, bookings, payments, reviews, ML recommendations, anti-scam, chat,
festivals, trip planning, currency and safety — across Django, FastAPI, Node,
Flutter and Next.js, with tests, security, caching, a production compose and full
thesis documentation.
