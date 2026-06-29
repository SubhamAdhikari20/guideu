# GuideU — Agile / Scrum Delivery Board

Delivery follows two-week sprints. The repository keeps only long-lived branches
`main` and `sprint-1`…`sprint-5`. Sprint scope below reflects the **re-scoped**
plan: `sprint-1` is foundation-only; feature code lands from `sprint-2`.

## Sprint 1 — Repository foundation ✅ (current)
- [x] Monorepo structure, hardened `.gitignore`, hygiene
- [x] core-engine: Django foundation (settings split, `common`, `authentication`)
- [x] analytics-engine: FastAPI foundation (app, config, health, model registry)
- [x] real-time-engine: Node + TS + Socket.IO foundation
- [x] Frontends scaffolded: Flutter `mobile_app`, Next.js `web_admin` (clean architecture)
- [x] Infra: docker-compose (postgres/mongo/redis/mlflow/nginx) + override
- [x] `shared/` TS contracts, `data/` workspace, `scripts/`, Makefile
- [x] CI workflows (GitHub Actions) for all five services
- [x] Quality tooling + documentation

## Sprint 2 — Domain features (next)
- [ ] core-engine: catalog, bookings, payments, reviews, favorites, notifications, trust, gamification, audit, permits
- [ ] analytics-engine: anti-scam, recommender, guide-rank, pricing inference + training pipelines
- [ ] real-time-engine: Socket.IO handlers + Redis→Django event bridge
- [ ] Frontends: auth + discovery + booking + dashboards wired to the APIs
- [ ] `seed_from_dataset` ingestion command

> The full Sprint-2 implementation already exists on the `backup/pre-sprint1-*`
> branch (built ahead) and is the source for these stories.

## Sprint 3 — Hardening
- [ ] Object-level permissions audit across every viewset
- [ ] Celery: async notifications, nightly retrain, demand-forecast job
- [ ] Contract tests across services; load-test the realtime fan-out

## Sprint 4 — Production readiness
- [ ] Observability: structured logs, tracing, Prometheus metrics
- [ ] Payment gateway live-mode hardening (eSewa/Khalti) + reconciliation
- [ ] Fairness regression gate in CI; model cards per release

## Sprint 5 — Polish & demo
- [ ] UX polish, accessibility, demo script, final thesis documentation
- [ ] Optional IoT (Arduino SOS) simulation

## Definition of Done
Code is reviewed, typed/linted, unit-tested, the relevant service
`check`/build passes, the API contract doc is updated, and (for ML) the model
card + evaluation metrics are recorded in the registry.
