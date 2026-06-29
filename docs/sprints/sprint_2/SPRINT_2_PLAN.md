# Sprint 2 — Plan (overview)

**Goal:** deliver the domain features on top of the Sprint-1 foundation. The
implementation already exists (built ahead) on `backup/pre-sprint1-2026-06-29`
and is brought onto `sprint-2` branch by branch, wired into the foundation.

## Backlog

### core-engine
- [ ] Register feature apps in `INSTALLED_APPS` + `config/urls.py`:
      `catalog, bookings, permits, payments, reviews, favorites, notifications,
      analytics, trust, gamification, audit`
- [ ] Restore audit middleware + booking Celery beat schedule
- [ ] `seed_from_dataset` management command

### analytics-engine
- [ ] Restore feature routers (`scam, recommendations, guides, pricing`)
- [ ] Restore `features/`, `training/`, `inference/`, `evaluation/`
- [ ] Re-enable the full `test_health` + inference tests

### real-time-engine
- [ ] Restore `socket.ts` handlers + `redisBridge.ts`; wire into `server.ts`

### frontends
- [ ] mobile_app: auth, destinations, guides, bookings, profile features
- [ ] web_admin: auth flows + moderation / analytics / verification dashboards

## Definition of Done
Each restored area passes its CI gate, the API contract docs are updated, and the
feature is demoable end-to-end through the nginx gateway.
