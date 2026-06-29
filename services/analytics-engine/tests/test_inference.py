from __future__ import annotations

import pytest


@pytest.mark.needs_dataset
def test_pricing_benchmark(client, api_headers):
    resp = client.post(
        "/api/v1/pricing/benchmark",
        headers=api_headers,
        json={"service_type": "Porter", "region": "Langtang"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["fair_price_npr"] > 0
    assert body["min_fair_npr"] <= body["fair_price_npr"] <= body["max_fair_npr"]


@pytest.mark.needs_dataset
def test_scam_score_flags_overcharge(client, api_headers):
    # First get a fair benchmark, then quote at 3x to force a flag.
    bench = client.post(
        "/api/v1/pricing/benchmark", headers=api_headers, json={"service_type": "Porter", "region": "Langtang"}
    ).json()
    quote = bench["fair_price_npr"] * 3
    resp = client.post(
        "/api/v1/scam/score",
        headers=api_headers,
        json={"service_type": "Porter", "region": "Langtang", "quoted_price_npr": quote},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_likely_scam"] is True
    assert body["overcharge_ratio"] > 1.25
    assert body["explanation"]


@pytest.mark.needs_dataset
def test_recommend_routes(client, api_headers):
    resp = client.post(
        "/api/v1/recommendations/routes",
        headers=api_headers,
        json={"tourist": {"pref_adventure_score": 0.9, "budget_band": "Mid-range"}, "season": "Autumn", "top_k": 5},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["items"]) == 5
    # High adventure score should surface harder routes near the top.
    assert body["items"][0]["components"]["adventure_fit"] >= 0.5


def test_guide_rank(client, api_headers):
    resp = client.post(
        "/api/v1/guides/rank",
        headers=api_headers,
        json={
            "tourist": {"region": "Everest/Khumbu", "language": "English"},
            "candidates": [
                {"guide_id": "G1", "certification": "IFMGA Mountain Guide", "average_rating": 4.8, "regions_covered": "Everest/Khumbu", "languages_spoken": "Nepali, English"},
                {"guide_id": "G2", "certification": "City Guide (Licensed)", "average_rating": 3.5, "regions_covered": "Kathmandu Valley", "languages_spoken": "Nepali"},
            ],
        },
    )
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert items[0]["guide_id"] == "G1"  # IFMGA + region/language match ranks first
