# Sprint 3 — Plan

Sprint 3 delivers the marketplace transaction layer: **bookings, payments and
reviews**. As in Sprint 2, the backend domain apps already exist (`bookings`,
`payments`, `reviews`), so the work is the **mobile frontend** wired to the real
APIs, plus a few small backend gap-fills (no rebuilds).

## What already exists (verified)
- `bookings` → `/api/v1/bookings/{packages,bookings,itinerary-items}/`
  (`TourPackage`, `BookingSession`, `ItineraryItem`). Bookings are
  package-centric: a booking needs a `tour_package` and dates.
- `payments` → `/api/v1/payments/{payments,escrow}/` (`PaymentTransaction`,
  `EscrowLedger`). Gateways supported: eSewa, Khalti, Other.
- `reviews` → `/api/v1/reviews/reviews/` — targets a `GuideRegistry` guide or a
  `TrekkingRoute` route (exactly the entities the mobile app already lists),
  author auto-injected, `summary` aggregation, admin moderation.

## Backend gaps to fill (small, additive)
- Scope `BookingSession` and `PaymentTransaction` list/detail to the logged-in
  user (tourists see their own bookings/payments; staff see all).
- Inject `tourist` / `user` from the request instead of trusting the client.
- Add `tour_package_title` to the booking response so "My Bookings" is readable.
- Add a `confirm` action on payments that marks the payment successful and the
  booking confirmed (a stand-in for real gateway verification, which is a later
  integration — the sandbox crypto for eSewa/Khalti/Stripe is out of scope here).

## Mobile work (Flutter, clean architecture)
1. **Bookings** — browse tour packages, book a package (pick start date +
   duration), see "My Bookings" with status, cancel a booking.
2. **Payments** — pay for a pending booking (choose eSewa / Khalti), then see it
   move to confirmed.
3. **Reviews** — rate and review a guide (and route), shown on the guide profile
   with an average-rating summary.

Each follows `data / domain / presentation`, returns `(Failure?, T?)` from the
data layer, and exposes list state as a Riverpod `AsyncValue`.

## Commit sequence (plain messages, pushed after each)
1. scope bookings and payments to the logged in user and add payment confirm
2. add tour packages and booking screens with my bookings
3. add payment screen for booking with esewa and khalti options
4. add ratings and reviews for guides
5. write sprint 3 review notes

## Verification
`manage.py check`, `flutter analyze`, `flutter test` must pass before each commit.
