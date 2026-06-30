# Sprint 3 — Review

Sprint 3 added the marketplace transaction layer to the mobile app: **bookings,
payments and reviews**, all wired to the existing core-engine APIs. As planned,
the backend domain apps were already there, so the work was the mobile frontend
plus a few small backend gap-fills (no rebuilds).

## Delivered

### Backend (core-engine) — small gap-fills
- Scoped `BookingSession` and `PaymentTransaction` lists to the logged-in user
  (tourists see their own; staff see all) and inject the owner from the request
  instead of trusting the client.
- Added `tour_package_title` to the booking response so "My Bookings" reads well.
- Added a payment `confirm` action that marks a payment successful and confirms
  its booking — a stand-in for real gateway verification (eSewa/Khalti sandbox
  callbacks remain a later integration).

### Mobile app (Flutter, clean architecture)
- **Bookings** — browse tour packages (`/bookings/packages/`), book a package
  (pick a start date, duration auto-calculated), "My Bookings" list with status,
  and cancel. Reachable from a Home CTA and the Profile tab.
- **Payments** — pay for a pending booking with eSewa or Khalti; on success the
  booking flips to confirmed.
- **Reviews** — rate and review a guide (1–5 stars + comment) from the guide
  profile, with an average-rating summary and the recent reviews shown inline.

Each feature follows `data / domain / presentation`, returns `(Failure?, T?)`
from the data layer, and exposes list state as a Riverpod `AsyncValue`.

## Verification
- `flutter analyze` — no issues.
- `flutter test` — passing.
- `manage.py check` — no issues.

## Notes / decisions
- Bookings are package-centric in the backend, so the mobile booking flow books
  tour packages. Guide discovery (Sprint 2) stays browse-only; the guide profile
  now points users to Tour Packages and lets them leave a review.
- New reviews start as "pending" until an admin approves them (existing
  moderation rule); the author sees their own pending review immediately.
- Real payment-gateway crypto (eSewa/Khalti/Stripe sandbox signatures, webhooks,
  Celery) was intentionally left out of scope — the `confirm` action keeps the
  end-to-end flow demoable without faking gateway internals.
