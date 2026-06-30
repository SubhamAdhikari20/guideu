"""Fair-price benchmark lookup, served from the dataset.

Builds cached aggregations at three granularities and falls back progressively:
(service, region, season) -> (service, region) -> (service). This is both a
standalone endpoint and the benchmark source for the scam scorer.
"""
from __future__ import annotations

from functools import lru_cache

import pandas as pd

from data.loader import load_pricing


@lru_cache(maxsize=1)
def _lookups() -> dict[str, pd.DataFrame]:
    pricing = load_pricing()
    agg = {"fair_price_npr": "mean", "min_fair_npr": "mean", "max_fair_npr": "mean"}
    return {
        "srs": pricing.groupby(["service_type", "region", "season"]).agg(agg),
        "sr": pricing.groupby(["service_type", "region"]).agg(agg),
        "s": pricing.groupby(["service_type"]).agg(agg),
    }


def _row_to_dict(row, *, service_type, region, season, granularity, n) -> dict:
    return {
        "service_type": service_type,
        "region": region,
        "season": season,
        "fair_price_npr": int(round(row["fair_price_npr"])),
        "min_fair_npr": int(round(row["min_fair_npr"])),
        "max_fair_npr": int(round(row["max_fair_npr"])),
        "currency": "NPR",
        "granularity": granularity,
        "sample_basis": int(n),
    }


def fair_price(service_type: str, region: str | None = None, season: str | None = None) -> dict | None:
    lookups = _lookups()
    if region and season:
        try:
            row = lookups["srs"].loc[(service_type, region, season)]
            return _row_to_dict(row, service_type=service_type, region=region, season=season, granularity="service+region+season", n=1)
        except KeyError:
            pass
    if region:
        try:
            row = lookups["sr"].loc[(service_type, region)]
            return _row_to_dict(row, service_type=service_type, region=region, season=season, granularity="service+region", n=1)
        except KeyError:
            pass
    try:
        row = lookups["s"].loc[service_type]
        return _row_to_dict(row, service_type=service_type, region=region, season=season, granularity="service", n=1)
    except KeyError:
        return None
