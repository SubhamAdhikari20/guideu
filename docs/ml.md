# GuideU — Machine Learning

The `analytics-engine` (FastAPI) implements GuideU's AI features against the
synthetic Travel Planning dataset. Everything below is **reproducible**:
`make train` (or `python -m training.run_all`) regenerates the artifacts and the
numbers reported here (representative run, fixed dataset seed).

## Strategy (baseline-first)
Per the proposal, we build simple, defensible baselines first and leave heavier
models as a documented upgrade path (sprint 2). Models train on **2021–2023** and
are evaluated on **2024** (temporal split — no leakage). Every model is written to
a registry (`artifacts/model_registry.json`, optional MLflow) with a model card.

## 1. Anti-scam classifier
- **Task:** predict `was_flagged_by_app` (overcharge flag) for a quote.
- **Model:** logistic regression over one-hot `service_type` + `region` and the
  scaled `quoted_price_npr` (+ `log` price). Class-balanced.
- **Deliberately excluded features:**
  - `overcharge_ratio` / `benchmark_price_npr` — the label is, in the generator,
    a deterministic function of the ratio; feeding it back yields a meaningless
    ~1.0 AUC. Excluding it forces the model to *learn price bands per
    service/region* and detect anomalies, which generalises to quotes with no
    exact benchmark.
  - `nationality` / `continent` — **protected attributes**, never used (fairness).
- **Representative metrics (test = 2024):**
  | metric | value |
  |---|---|
  | accuracy | 0.95 |
  | precision | 0.82 |
  | recall | 1.00 |
  | ROC-AUC | 0.999 |
  | PR-AUC | 0.996 |

  High AUC is expected: for a given service+region, a higher quoted price almost
  always means an overcharge, and the model recovers that cleanly.

### Fairness finding (important, and honest)
The per-continent audit reports a **flag-rate disparity of ~0.21**, which exceeds
our 0.15 review gate — so the gate correctly flags the model for **review**, not
silent deployment. Interpreting it:

- The dataset *intentionally* simulates real tourist-price discrimination
  (Europe / North America / Oceania are quoted higher).
- Because those tourists really are overcharged more often, a fair overcharge
  detector **should** flag their quotes more often — the per-group report shows
  the model's `flag_rate` tracks the `actual_rate`.
- The disparity therefore lives **in the world, not in the model**: with protected
  attributes excluded, the model is protecting the affected tourists, not
  profiling them. The mitigation (exclude protected features + always return the
  benchmark + ratio + explanation) lets a human moderator see *why* a quote was
  flagged.

This is exactly the kind of nuance the proposal's responsible-AI section calls
for, and it is surfaced automatically at train time. See
[ethics-and-fairness.md](ethics-and-fairness.md).

## 2. Route recommender
- **Task:** rank the 2,000 routes for a tourist.
- **Model:** interpretable content score
  `0.45·adventure_fit + 0.2·season_fit + 0.2·budget_fit + 0.15·popularity`,
  where `adventure_fit` aligns route difficulty with the tourist's
  `pref_adventure_score` (the dataset's documented monotonic signal: mean
  difficulty rises 1.6→3.5 across adventure quintiles). Popularity comes from the
  **train-period** interaction log only.
- **Evaluation (2024 positive feedback, ~2,900 users):** Precision@5 ≈ 0.0011,
  NDCG@5 ≈ 0.0030, Hit-Rate@10 ≈ 0.0090 vs a popularity-only baseline ≈ 0.0083 —
  a **~1.08× lift** over popularity.
- **Honest read:** absolute precision is low because positive feedback is sparse
  across a 2,000-item catalog; the content signal beats popularity modestly. The
  documented upgrade path (sprint 2) is implicit-feedback matrix factorisation /
  a two-tower model (`uv sync --extra deep`), evaluated with the same harness.
- **Traceable:** every recommendation returns its component scores, answering
  "why am I seeing this?".

## 3. Verified-guide ranking
Transparent weighted score over certification tier (IFMGA highest, matching the
dataset's 4.55 average), normalised rating, region coverage and language overlap
with the requesting tourist. No opaque model — fully explainable by design.

## 4. Price benchmarking
Deterministic aggregation of `pricing_benchmarks.csv` with a three-level fallback
(`service+region+season` → `service+region` → `service`). Serves transparent
pricing and is the benchmark source for the scam scorer.

## Reproducibility & registry
- `python -m training.run_all` trains everything and prints a consolidated report.
- Artifacts + metrics land in `artifacts/model_registry.json`; set
  `MLFLOW_TRACKING_URI` to also log runs to MLflow.
- `GET /api/v1/models` exposes the live registry (versions, metrics, training
  metadata) for the admin dashboard.
