from __future__ import annotations


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert "models" in body


def test_scam_requires_api_key(client):
    resp = client.post("/api/v1/scam/score", json={"service_type": "Porter", "quoted_price_npr": 5000})
    assert resp.status_code == 401
