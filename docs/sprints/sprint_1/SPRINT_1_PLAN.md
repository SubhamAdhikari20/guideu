# Sprint 1 — Plan

**Goal:** a clean, professional, production-ready repository **foundation** that
every later sprint builds on. No business features.

## Audit of the starting repository

The repo already contained substantial, **uncommitted** work (a full Django
domain, an ML engine and a realtime engine — effectively built ahead). Decision:
**re-scope** `sprint-1` to foundation-only and **preserve** all feature code.

| Area | Action |
| --- | --- |
| All uncommitted feature work | **Preserved** on `backup/pre-sprint1-2026-06-29`; relocated to `sprint-2` |
| `core-engine` (config, `common`, `authentication`) | **Keep** as foundation |
| `core-engine` feature apps (catalog, bookings, payments, …) | **Defer** to sprint-2 |
| `analytics-engine` ML pipeline (training, inference, features) | **Defer** to sprint-2 |
| `real-time-engine` `socket.ts` / `redisBridge.ts` | **Defer** to sprint-2 |
| `db.sqlite3`, caches | **Untrack** + git-ignore |
| Service names / layout (kebab-case, `config/`+`src/`) | **Keep** (ADR-0001/0002) and **enrich** |

## Architecture decision

Keep the existing ADR-backed structure and **add** the missing foundation from
the brief: `shared/`, `infra/` (nginx, mlflow), `data/`, `scripts/`, `.github/`
CI, structured `docs/`, frontends. Frontends mirror the `leelame` clean
architecture (ADR-0010).

## Planned commits

1. `chore:` harden root `.gitignore`, untrack local sqlite db
2. `docs:` architecture, ADRs, data, ml, ethics, API contracts
3. `build(core-engine):` Django foundation (settings split, common, authentication)
4. `build(analytics-engine):` FastAPI foundation (app, config, health, registry, tests)
5. `build(realtime-engine):` Node + TS + Socket.IO foundation
6. `build(infra):` docker-compose + nginx gateway + mlflow
7. `chore(shared):` TS event/API types & constants
8. `build:` data workspace, scripts, Makefile
9. `build(mobile-app):` Flutter clean-architecture scaffold
10. `build(web-admin):` Next.js layered scaffold
11. `ci:` GitHub Actions for all services
12. `chore(quality):` EditorConfig + recommended extensions
13. `docs:` README + architecture/setup/sprint documentation

## Definition of Done
Foundation builds/checks pass per service; branches `main` + `sprint-1..5` exist;
≥12 conventional commits; no feature code in `sprint-1`; nothing lost.
