# Architecture Decision Records (ADRs)

Short, dated records of the non-obvious choices made while building GuideU, so
they can be defended in the thesis.

## ADR-0001 — Keep committed service names (`analytics-engine`, `real-time-engine`)
**Date:** 2026-06-23 · **Status:** Accepted

The repo's `README.md` and architecture diagram already commit to
`services/analytics-engine` (FastAPI) and `services/real-time-engine` (Node). The
later brief alternately names these `ml-service` and `realtime-engine`. We keep
the **committed** names to avoid orphaning the existing documentation and diagram.
Renaming later is a trivial, mechanical change if desired.

## ADR-0002 — Additive catalog app instead of rewriting bookings
**Date:** 2026-06-23 · **Status:** Accepted

The existing `bookings` app models `TourPackage`/`BookingSession`. The dataset is
route + guide-registry centric. Rather than rewrite working, migrated code, we add
a `catalog` app (Region, TrekkingRoute, GuideRegistry, CulturalEvent,
PricingBenchmark) that mirrors the dataset, and link bookings to routes with a new
**nullable** FK. This is non-breaking and lets `TourPackage` (a curated bundle)
and `TrekkingRoute` (raw catalog) coexist — a defensible product distinction.

## ADR-0003 — `GuideRegistry` (catalog) is distinct from `GuideProfile` (accounts)
**Date:** 2026-06-23 · **Status:** Accepted

`verified_guides.csv` is an external NTB registry of 8,000 licensed guides — it is
reference data, not app accounts. We model it as `catalog.GuideRegistry`. An app
user who is a guide gets `authentication.GuideProfile` and may be *linked* to a
registry row once verified. This separates "who is licensed in Nepal" from "who
has signed up to GuideU."

## ADR-0004 — Synthetic tourists are reference rows, not login accounts
**Date:** 2026-06-23 · **Status:** Accepted

`tourists.csv` provides 40k profiles with latent survey scores that drive the
recommender. Creating 40k fake `User` rows with usable credentials would be a
security smell. We load them into a reference table the feature store joins
against; real users authenticate through `authentication.User`.

## ADR-0005 — Settings split into `base/dev/prod`
**Date:** 2026-06-23 · **Status:** Accepted

`config/settings.py` becomes a `config/settings/` package so `config.settings`
still resolves (back-compatible for `manage.py`, `wsgi`, `asgi`). `dev` defaults to
SQLite for zero-setup local runs; `prod` requires PostgreSQL and real secrets and
fails fast if they are missing.

## ADR-0006 — Heavy ML deps (PyTorch, MLflow) are optional at runtime
**Date:** 2026-06-23 · **Status:** Accepted

The analytics-engine must *boot and serve* with only pandas + scikit-learn so it
is runnable in CI and on modest hardware. PyTorch and MLflow are imported lazily
and degrade gracefully (MLflow falls back to a JSON registry; deep models are an
optional extra). Baseline-first matches the brief's ML strategy.

## ADR-0007 — Fairness guardrail on the scam model
**Date:** 2026-06-23 · **Status:** Accepted

The dataset *deliberately* encodes a nationality-based overcharge bias to mimic
real tourist-price discrimination. The scam classifier must flag overcharging
**without** using nationality/continent as a predictive feature (that would
launder discrimination into the model). We exclude protected attributes from the
feature set and run a post-hoc fairness audit (flag-rate parity across
continents). See [ethics-and-fairness.md](ethics-and-fairness.md).
