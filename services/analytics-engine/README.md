# GuideU — analytics-engine (FastAPI ML service)

Machine-learning and analytics service for GuideU. Serves the three headline AI
features against the synthetic Travel Planning dataset:

1. **Anti-scam scoring** — `POST /api/v1/scam/score`
2. **Route recommendations** — `POST /api/v1/recommendations/routes`
3. **Verified-guide ranking** — `POST /api/v1/guides/rank`

plus **price benchmarking** (`POST /api/v1/pricing/benchmark`) and a **model
registry** (`GET /api/v1/models`). Interactive docs at `/docs`.

## Design principles
- **Baseline-first** — logistic regression + content/popularity scoring before
  anything heavier (PyTorch is an optional extra).
- **Boots without artifacts** — endpoints serve via explainable heuristics until
  models are trained, then load the registered artifacts automatically.
- **Honest evaluation** — temporal split (train 2021-2023, test 2024).
- **Fairness-aware** — protected attributes are excluded from the scam model and
  a per-continent fairness audit runs at train time.

## Layout
```
app/            FastAPI: config, deps, api/ (routers), schemas/
data/           dataset loaders
features/       feature engineering (scam, recommender)
training/       train_scam, train_recommender, run_all
inference/      online scoring (scam, recommender, guides, pricing)
evaluation/     metrics + fairness audit
registry.py     model registry (JSON; optional MLflow)
artifacts/      trained models + model_registry.json (git-ignored)
tests/          pytest API + inference tests
```

## Run locally
```bash
uv sync
# Train models on the dataset (writes artifacts/ + registry):
uv run python -m training.run_all --dataset-dir "../../../Travel Planning"
# Serve:
uv run uvicorn app.main:app --reload --port 8001
```

## Example
```bash
curl -s localhost:8001/api/v1/scam/score \
  -H "X-API-Key: $ANALYTICS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"service_type":"Licensed Guide","region":"Everest/Khumbu","quoted_price_npr":9000}'
```

## Optional extras
- `uv sync --extra tracking` — MLflow experiment tracking
- `uv sync --extra deep` — PyTorch (two-tower recommender upgrade)
- `uv sync --extra mongo` — Mongo logging of inference requests

See `../../docs/data.md` and `../../docs/ethics-and-fairness.md` for the dataset
mapping and the fairness rationale.
