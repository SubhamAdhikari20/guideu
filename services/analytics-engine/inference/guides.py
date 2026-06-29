"""Verified-guide ranking — transparent scoring (no opaque model).

Combines certification tier, rating, region coverage and language overlap with
the requesting tourist's needs. IFMGA carries the highest tier weight, matching
the dataset's quality signal (IFMGA average rating 4.55).
"""
from __future__ import annotations

CERT_WEIGHT = {
    "IFMGA Mountain Guide": 1.0,
    "NATHM Trekking Guide": 0.8,
    "Government Trekking Guide": 0.75,
    "Adventure Sports Guide": 0.75,
    "Cultural Specialist": 0.7,
    "NATHM Tour Guide": 0.65,
    "Bird-watching Specialist": 0.6,
    "City Guide (Licensed)": 0.55,
}

WEIGHTS = {"certification": 0.35, "rating": 0.3, "region": 0.2, "language": 0.15}


def _overlap(csv_field: str | None, wanted: str | None) -> float:
    if not wanted:
        return 0.5
    items = {p.strip().lower() for p in str(csv_field or "").split(",")}
    return 1.0 if wanted.strip().lower() in items else 0.0


def rank(*, tourist: dict, candidates: list[dict]) -> dict:
    wanted_region = tourist.get("region")
    wanted_language = tourist.get("language")

    ranked = []
    for guide in candidates:
        components = {
            "certification": round(CERT_WEIGHT.get(guide.get("certification", ""), 0.5), 4),
            "rating": round(min(float(guide.get("average_rating", 0)) / 5.0, 1.0), 4),
            "region": round(_overlap(guide.get("regions_covered"), wanted_region), 4),
            "language": round(_overlap(guide.get("languages_spoken"), wanted_language), 4),
        }
        score = sum(WEIGHTS[k] * components[k] for k in WEIGHTS)
        ranked.append({**guide, "score": round(score, 4), "components": components})

    ranked.sort(key=lambda g: g["score"], reverse=True)
    return {"model_version": "guide-rank-v1", "items": ranked}
