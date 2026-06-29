# Sprint 1 — Retrospective

## What went well
- **Non-destructive re-scope.** A safety branch (`backup/pre-sprint1-2026-06-29`)
  captured all uncommitted work before any history change — zero risk of loss.
- **Verified-as-you-go.** Every service commit was gated on a real check
  (`manage.py check`, `pytest`, `tsc`/`eslint`, `flutter analyze`/`test`,
  `next build`), so CI gates only on things proven to pass.
- **Reused proven patterns.** Frontend architecture mirrors the `leelame`
  reference (clean architecture) instead of reinventing structure.
- **One logical commit per task**, all pushed to `origin/sprint-1`.

## What could be improved
- Docker could not be exercised locally (not installed) — full-stack health is
  unverified until run on a Docker host.
- `mypy`/`ruff` are not yet wired into the Python services' CI (only Django
  `check` + `pytest`); add static typing/linting gates in a later sprint.
- The Sprint-2 feature code still needs to be merged onto `sprint-2` from the
  backup branch and re-verified against this foundation.

## Action items for Sprint 2
1. Bring feature apps onto `sprint-2`, wire them into settings/urls/routers.
2. Add `ruff` + `mypy` config and CI steps for the Python services.
3. Add a `docker compose config`/build job to CI once a Docker runner is available.
4. Implement the frontend feature folders (data/domain/presentation) against the
   live APIs.
