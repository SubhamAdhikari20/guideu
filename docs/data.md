# GuideU — Data Strategy & Dataset Mapping

The platform is developed against a **synthetic, relational, 500k-row dataset**
(`Travel Planning/`) generated with research-informed correlations and a fixed
seed (`20240519`). It is synthetic by design — see the dataset README's ethics
statement — which sidesteps privacy risk while preserving learnable signal.

## Dataset → service ownership

| Dataset file | Rows | Primary owner | How it is used |
|---|---:|---|---|
| `tourists.csv` | 40,000 | core-engine (`catalog.SyntheticTourist`* / accounts) | User profiles + latent survey scores; the central recommender input. |
| `verified_guides.csv` | 8,000 | core-engine `catalog.GuideRegistry` | NTB/IFMGA/NATHM registry; basis for verified-guide trust + ranking. |
| `trekking_routes.csv` | 2,000 | core-engine `catalog.TrekkingRoute` | Route catalog: permits, difficulty, altitude, seasons, badge points. |
| `cultural_events.csv` | 4,000 | core-engine `catalog.CulturalEvent` | Festival calendar for discovery + gamification. |
| `pricing_benchmarks.csv` | 85,000 | core-engine `catalog.PricingBenchmark` | Fair-price ranges per (service, region, season) — anti-scam ground truth. |
| `bookings.csv` | 95,000 | analytics-engine (training) | Historical transactions for recommender + demand signals. |
| `recommendation_interactions.csv` | 140,000 | analytics-engine (training) | view/wishlist/book/rate/share/complete — collaborative-filtering signal. |
| `scam_reports.csv` | 35,000 | analytics-engine (training) | Labeled overcharge reports; `was_flagged_by_app` is the scam classifier target. |
| `gamification_log.csv` | 31,000 | core-engine `analytics` (reference) | Badge/points reference for the gamification design. |
| `tourist_arrivals.csv` | 60,000 | analytics-engine (forecasting) | Aggregated arrivals time series (2021–2024) for demand forecasting. |
| `recommendation_flat.csv` | 95,000 | analytics-engine (training) | Pre-joined wide table for quick modeling. |

\* The synthetic tourist rows are reference/training records, **not** live app
credentials. The ingestion command loads them into a reference table so the
catalog and the ML feature store can join against them without creating
fake login accounts. Real app users come from `authentication.User`.

## The three headline AI features (and their clean signals)

1. **Anti-scam price benchmarking** — binary classification on
   `was_flagged_by_app` (~21.7% positive) from `overcharge_ratio`, `service_type`,
   `region`, `season`, and tourist demographics. The dataset cleanly separates
   severity by overcharge ratio (Fair 0.91 → Likely Scam 2.78), so a calibrated
   classifier plus the benchmark table gives an explainable overcharge flag.
2. **Personalized recommendations** — content-based scoring from the survey
   fields (`pref_adventure_score` etc.) against route/guide/event metadata,
   blended with popularity from the interaction log. Route difficulty rises
   monotonically with the user's adventure quintile (1.6 → 3.5), a deliberately
   learnable signal.
3. **Verified-guide ranking** — learning-to-rank / scoring using certification
   tier, rating, regions, languages, and the requesting tourist's profile.
   IFMGA guides carry the highest average rating (4.55).

## Raw → cleaned → features

The analytics-engine keeps a strict separation:

```
services/analytics-engine/
  data/raw/         # symlink or copy of Travel Planning (read-only)
  data/processed/   # cleaned, typed parquet written by the cleaning step
  features/         # feature engineering (fit scores, recency, encoders)
  artifacts/        # trained model binaries + model_registry.json
  mlruns/           # MLflow tracking store
```

## Ingestion into the core engine

`python manage.py seed_from_dataset --dataset-dir "Travel Planning"` performs an
idempotent, chunked bulk load of the **catalog** tables (regions, routes, guide
registry, cultural events, pricing benchmarks) into PostgreSQL. Transactional
tables (bookings/interactions/scam reports) stay in the dataset for ML training;
a small demo subset can be materialised with `--with-demo-bookings`.

## Temporal split for honest evaluation

Per the dataset README, models train on **2021–2023** and test on **2024** to
avoid leakage and reflect deployment. Metrics reported: Precision@K / NDCG@K
(recommender), ROC-AUC / PR-AUC / calibration (scam), RMSE (rating/price).
