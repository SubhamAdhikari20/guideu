# GuideU — Sprint Status (through Sprint 3)

GuideU is an AI-powered tourism platform for Nepal (BSc thesis + startup).
GitHub: `SubhamAdhikari20/guideu`.

## Architecture
Polyglot microservices monorepo (kebab-case service dirs):
- `services/core-engine` — Django + DRF + Celery + SimpleJWT (`config/` + `src/<app>`)
- `services/analytics-engine` — FastAPI ML
- `services/real-time-engine` — Node + TypeScript + Socket.IO
- `apps/mobile_app` — Flutter + Riverpod (clean architecture from `leelame`)
- `apps/web_admin` — Next.js (still scaffold)
- `shared/ infra/ data/ scripts/ docs/` (docker-compose + nginx + mlflow)

Databases: PostgreSQL, MongoDB, Redis.

Mobile clean architecture: `features/<f>/{data,domain,presentation}`. The data
layer returns `(Failure?, T?)` records (no Either). Riverpod for DI; list state
exposed as `AsyncValue` via `FutureProvider.family` keyed by search string
(Riverpod 3 — `StateProvider` is legacy). Dio client attaches JWT and does a
one-shot refresh on 401.

## Branches
`main` + `sprint-1`..`sprint-5`. Sprints 1, 2, and 3 are all MERGED into `main`
and pushed (`--no-ff` release merge commits). `main` tree == `sprint-3` tip.
Local safety branch `backup/pre-sprint1-2026-06-29` is preserved (do not push or
delete without asking). sprint-4/5 are still stubs.

## Sprint 1 — DONE (merged)
Repository foundation: monorepo layout, service skeletons, infra
(docker-compose + nginx + mlflow), per-service CI, docs.

## Sprint 2 — DONE (merged)
Mobile frontend wired to the existing backend.
- Backend: email login (`EmailTokenObtainPairSerializer`), auth URL cleanup.
- Mobile: **auth** (splash/login/signup/forgot, JWT, secure storage),
  theme + logo, **destinations** (Explore + detail sheet, `/catalog/routes/`),
  **guides** (list + profile sheet, `/catalog/guides-registry/`), **home** +
  bottom-nav shell (Home/Explore/Guides/Profile) + Profile tab with logout.
  Flutter packages upgraded (Riverpod 3, go_router 17, secure_storage 10).
- Carried over (deferred): web_admin guide-verification + user-management
  dashboards, ML ingestion endpoint.

## Sprint 3 — DONE (merged)
Marketplace transaction layer.
- Backend gap-fills only (no rebuild, no migrations):
  - Scoped `BookingSession` & `PaymentTransaction` lists to `request.user` and
    inject the owner server-side (clients can't spoof it).
  - Added `tour_package_title` to booking output.
  - Added a payment `confirm` action (simulated gateway success → booking
    flips to CONFIRMED). Real eSewa/Khalti/Stripe crypto + webhooks + Celery
    left out of scope.
- Mobile:
  - **bookings** — browse `TourPackage` (`/bookings/packages/`), create booking
    (`/bookings/bookings/`), My Bookings + cancel.
  - **payments** — eSewa/Khalti sheet → confirm.
  - **reviews** — rate/review guides (`/reviews/reviews/` + summary), shown in
    the guide profile.
- Notes: bookings are PACKAGE-centric (no guide-direct booking); the guide
  profile "Book" points to packages. Reviews start PENDING until admin
  moderation.

## Verification
`flutter analyze` — clean; `flutter test` — passing; `manage.py check` — clean
(each Sprint 3 slice).

## Key API endpoints (core-engine, `/api/v1`)
- `auth/token/` (email + password), `auth/token/refresh/`, `auth/register/`,
  `auth/users/me/`
- `catalog/{routes,regions,guides-registry}/`
- `bookings/{packages,bookings,itinerary-items}/`
- `payments/{payments,escrow}/` + `payments/{id}/confirm/`
- `reviews/reviews/` + `reviews/reviews/summary/`

Pagination: page-number `{count, next, previous, results}`, page_size 25.
Datasources also tolerate bare lists.

## Next
Sprint 4 (ML / analytics-engine) — verify-and-fill-gaps style. Plus the
carried-over web_admin dashboards + ML ingestion endpoint. Confirm with the
user before starting.
