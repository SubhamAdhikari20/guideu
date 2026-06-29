# `data/`

Workspace for datasets used by the analytics-engine. Contents are git-ignored
(only the directory placeholders are tracked) — see the root `.gitignore`.

```text
data/
├── raw/         # raw source datasets (immutable inputs)
├── processed/   # feature-engineered / cleaned outputs
└── synthetic/   # generated synthetic data (Sprint 4)
```

## Primary dataset

The project's synthetic **Travel Planning** dataset (≈500k rows) currently lives
as a repo sibling at `../Travel Planning/` and is mounted read-only into the
analytics-engine container (`/data/travel-planning`, see
[`../docker-compose.yml`](../docker-compose.yml)). The analytics-engine resolves
it automatically for local runs (`app/config.py`). See
[`../docs/data.md`](../docs/data.md) for the dataset → service mapping.
