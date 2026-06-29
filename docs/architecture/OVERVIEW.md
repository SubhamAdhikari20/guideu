# Architecture Overview

GuideU is a **polyglot microservices** platform. This document explains the
*why*; see [`../architecture.md`](../architecture.md) for the detailed component
view and [`../api-contracts.md`](../api-contracts.md) for cross-service contracts.

## Why microservices

The workload splits cleanly into three runtimes with very different profiles:

- **Transactional business logic** (auth, bookings, payments, permits) needs ACID
  guarantees and a mature ORM/admin → **Django + PostgreSQL**.
- **High-frequency, long-lived connections** (chat, live location, presence)
  need a non-blocking event loop → **Node.js + Socket.IO**, decoupled so it never
  exhausts Django's request workers.
- **Compute-heavy ML** (anti-scam scoring, recommendations, pricing) benefits
  from the Python data stack and independent scaling → **FastAPI + scikit-learn**.

Services communicate over HTTP (REST/inference) and asynchronously via a **Redis**
pub/sub bus: Django publishes domain events, the realtime engine fans them out to
clients. This gives fault isolation and independent deployability.

## Service responsibilities

| Service | Owns | Storage |
| --- | --- | --- |
| core-engine | identities (RBAC + JWT), catalog, bookings, payments, permits, reviews, notifications, trust/anti-scam orchestration | PostgreSQL |
| analytics-engine | model training + inference, model registry, fairness audit | MongoDB / artifacts |
| real-time-engine | websockets, chat, live updates, presence | Redis (ephemeral) |

## Database polyglotism

- **PostgreSQL** — relational core entities; FK integrity protects escrow/payment
  flows from race conditions.
- **MongoDB** — flexible documents (itineraries, activity logs, ML metadata) that
  evolve without migrations.
- **Redis** — cross-service pub/sub broker, cache, and ephemeral tracking state.

## ML/AI system design

Baseline-first and **runnable with only pandas + scikit-learn**; PyTorch and
MLflow are optional and imported lazily (ADR-0006). The anti-scam model is
explicitly built to flag over-charging **without** using nationality as a feature,
with a post-hoc fairness audit (ADR-0007). See [`../ml.md`](../ml.md) and
[`../ethics-and-fairness.md`](../ethics-and-fairness.md).

## Frontend architecture

Both clients follow **clean architecture**, adapted from the team's reference
projects:

- `apps/mobile_app` (Flutter): `app/` shell, `core/` cross-cutting utilities, and
  feature-first `features/<f>/{data,domain,presentation}` with MVVM + Riverpod.
- `apps/web_admin` (Next.js): `app/` routing, `components/`, `lib/{api,actions}`
  (data access + use cases), `schemas/` (zod), `types/`, `hooks/`.
