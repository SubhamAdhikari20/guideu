# Sprint 2 — Review

Sprint 2 wired the Flutter mobile app to the existing core-engine APIs and
delivered the first end-to-end screens for tourists. The backend domain apps
(authentication, catalog, bookings, etc.) were already built ahead, so the focus
this sprint was the **mobile frontend** plus a couple of small backend fixes.

## Delivered

### Backend (core-engine)
- Email + password login (`EmailTokenObtainPairSerializer` / view) so the app can
  sign in with an email instead of a username.
- Cleaned up the doubled auth URL prefix (`/api/v1/auth/...`).

### Mobile app (Flutter, clean architecture)
- **Auth** — splash, login, sign up, forgot password; Dio client with JWT
  attach + refresh, secure token storage, Riverpod state, go_router.
- **Theme** — GuideU teal + gold brand, logo asset.
- **Destinations** — Explore screen listing trekking routes from
  `/catalog/routes/`, search, and a "Destination Details" bottom sheet
  (duration, difficulty, max altitude, best season, permits).
- **Guides** — "Available Guides" list from `/catalog/guides-registry/`, search,
  and a "Guide Profile" bottom sheet (rating, experience, certification,
  languages, regions covered).
- **Home** — discovery landing (greeting, search, hero banner, quick actions,
  nearby-guides strip) with bottom navigation across Home / Explore / Guides /
  Profile, and a Profile tab with logout.
- Upgraded Flutter packages (Riverpod 3, go_router 17, secure_storage 10).

Each feature follows the `data / domain / presentation` split mirrored from the
`leelame` reference, returning a `(Failure?, T?)` record from the data layer and
exposing list state as a Riverpod `AsyncValue`.

## Verification
- `flutter analyze` — no issues.
- `flutter test` — passing.
- `manage.py check` — no issues.

## Carried over to later sprints
- Web-admin guide-verification + user-management dashboards (still scaffolded).
- ML ingestion endpoint for Sprint 4 models.
- Guide booking from the profile screen → handled in Sprint 3 (booking flow).

## Notes
The catalog is dataset-driven, so the prototype's "destinations" map onto
`TrekkingRoute` and the "guides" onto the `GuideRegistry` licensing registry.
Cards use brand gradient placeholders because the catalog has no image URLs yet;
real media can be added when the content pipeline lands.
