# GuideU — Sprint Status (through Sprint 4)

GuideU is an AI-powered tourism platform for Nepal (BSc thesis + startup).
GitHub: `SubhamAdhikari20/guideu`.

## Architecture
Polyglot microservices monorepo (kebab-case service dirs):
- `services/core-engine` — Django + DRF + Celery + SimpleJWT (`config/` + `src/<app>`)
- `services/analytics-engine` — FastAPI ML (scam, recommendations, pricing, registry)
- `services/real-time-engine` — Node + TypeScript + Socket.IO
- `apps/mobile_app` — Flutter + Riverpod (clean architecture from `leelame`)
- `apps/web_admin` — Next.js 16 (admin dashboard)
- `shared/ infra/ data/ scripts/ docs/` (docker-compose + nginx + mlflow)

Databases: PostgreSQL, MongoDB, Redis.

Mobile clean architecture: `features/<f>/{data,domain,presentation}`. The data
layer returns `(Failure?, T?)` records (no Either). Riverpod for DI; list state
exposed as `AsyncValue`. Dio client attaches JWT and does a one-shot refresh on 401.

## Branches
`main` + `sprint-1`..`sprint-5`. Sprints 1, 2, and 3 are merged into `main`.
Sprint 4 work lives on `sprint-4` (not yet merged at time of writing).
Local safety branch `backup/pre-sprint1-2026-06-29` is preserved.

## Sprint 1 — DONE (merged)
Repository foundation: monorepo layout, service skeletons, infra
(docker-compose + nginx + mlflow), per-service CI, docs.

## Sprint 2 — DONE (merged)
Mobile frontend wired to the existing backend: auth (JWT, secure storage),
destinations (Explore), guides (list + profile), home + bottom-nav shell.

## Sprint 3 — DONE (merged)
Marketplace transaction layer: tour packages + bookings, payments
(eSewa/Khalti sheet → confirm), reviews/ratings shown on the guide profile.
Bookings are package-centric.

## Sprint 4 — DONE (on `sprint-4`)
The AI + connectivity sprint. Verify-and-fill-gaps: reused the existing ML
service, anti-scam tool, festival data and socket server; filled small backend
gaps and built the app frontends.
- **Backend gaps:** `recommendations` app (route + guide feed proxying the
  analytics-engine with DB enrichment + fallback); `chat` app (Postgres thread +
  message history, participant-scoped) with the real-time-engine persisting each
  delivered message; `catalog/events/upcoming/` festival calendar grouping.
- **Mobile:** "Recommended for you" on Home, anti-scam "Is this price fair?"
  screen + overcharge reporting, a Festivals tab (calendar/info hub), and live
  guide ↔ tourist chat (Socket.IO + REST history, opened from a booking).
- **Web admin:** first real dashboard (Overview, ML Models, Festivals, Scam
  Reports) with server-side fetches so secrets stay server-side.
- See `docs/sprints/sprint_4/` for the plan and review.

## Verification
`manage.py check` clean; `pytest` 7 passing; `flutter analyze`/`test` clean;
real-time-engine `tsc` build clean; web_admin `lint` + `build` clean.

## Key API endpoints (core-engine, `/api/v1`)
- `auth/token/`, `auth/token/refresh/`, `auth/register/`, `auth/users/me/`
- `catalog/{routes,regions,guides-registry,events,pricing-benchmarks}/`
  (+ `events/upcoming/`, `pricing-benchmarks/lookup/`)
- `bookings/{packages,bookings,itinerary-items}/`
- `payments/{payments,escrow}/` + `payments/{id}/confirm/`
- `reviews/reviews/` + `reviews/reviews/summary/`
- `recommendations/{routes,guides}/`
- `chat/{threads,messages}/`
- `trust/price-check/` + `trust/scam-reports/`

Pagination: page-number `{count, next, previous, results}`, page_size 25.

## Next
Sprint 5 — offline maps / IoT SOS direction, plus carried-over admin auth +
moderation write actions and guide-verification / user-management pages.
