# Ethics, Privacy & Fairness

GuideU's proposal commits to responsible, privacy-aware, fairness-aware AI. This
document records how that commitment is implemented, mapped to the dataset's
**Area 6** (`Travel Planning/regulatory_framework.md`).

## Privacy by design
- **Data minimisation** — the API collects only what a workflow needs; profile
  fields (passport, citizenship) are optional and indexed but never returned in
  list endpoints.
- **No fake credentials** — synthetic tourists are reference rows, not login
  accounts (ADR-0004).
- **Consent hooks** — `accounts` exposes a `data_consent` flag and the analytics
  ingest respects an opt-out; event logging is pseudonymous (user id, not PII).
- **Secrets** — sourced from environment only; `.env` is git-ignored;
  `prod` settings fail fast if `DJANGO_SECRET_KEY` is unset.

## Fairness: the scam model must not discriminate
The dataset intentionally simulates real-world tourist-price discrimination —
tourists from Europe / North America / Oceania are quoted systematically higher
prices. A naive classifier could learn "European ⇒ flag," laundering
discrimination into automation.

**Mitigations implemented in `analytics-engine`:**
1. **Protected attributes excluded** from the scam feature set (`nationality`,
   `continent` are never model inputs). The signal comes from
   `overcharge_ratio = quoted / benchmark`, which is the *fair* basis.
2. **Fairness audit** after training: flag-rate and ROC-AUC are reported per
   continent (`evaluation/fairness.py`); a large disparity fails the gate.
3. **Explainability** — every scam score returns the benchmark, the ratio, and
   the contributing factors, so a human moderator can audit the decision.

## Recommendations: traceable, not a black box
Content-based scores are computed from interpretable fit terms (adventure-fit,
culture-fit, budget-fit, season-fit). Each recommendation response includes the
component scores so the "why am I seeing this?" question is answerable.

## Worker fairness
Price benchmarking flags *overcharging*, but the fair range protects guides and
porters too — quoting **below** `min_fair_npr` is surfaced as "below fair wage,"
aligning with the proposal's pledge not to harm local workers.
