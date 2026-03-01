"""Tests for estimate CRUD endpoints."""

import pytest
from httpx import AsyncClient

SAMPLE_FEATURES = {
    "square_footage": 1550,
    "bedrooms": 3,
    "bathrooms": 2,
    "year_built": 1997,
    "lot_size": 6800,
    "distance_to_city_center": 4.1,
    "school_rating": 7.6,
}


@pytest.mark.asyncio
async def test_create_estimate(client: AsyncClient, mock_ml_predict):
    resp = await client.post("/api/estimates", json=SAMPLE_FEATURES)
    assert resp.status_code == 201
    body = resp.json()
    assert body["predicted_price"] == 250000.0
    assert body["square_footage"] == 1550
    assert "id" in body
    assert "created_at" in body


@pytest.mark.asyncio
async def test_get_history_empty(client: AsyncClient, mock_ml_predict):
    resp = await client.get("/api/estimates/history")
    assert resp.status_code == 200
    body = resp.json()
    assert body["items"] == []
    assert body["total"] == 0


@pytest.mark.asyncio
async def test_get_history_with_data(client: AsyncClient, mock_ml_predict):
    await client.post("/api/estimates", json=SAMPLE_FEATURES)
    resp = await client.get("/api/estimates/history")
    body = resp.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1


@pytest.mark.asyncio
async def test_delete_estimate(client: AsyncClient, mock_ml_predict):
    create_resp = await client.post("/api/estimates", json=SAMPLE_FEATURES)
    eid = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/estimates/history/{eid}")
    assert del_resp.status_code == 204

    history = await client.get("/api/estimates/history")
    assert history.json()["total"] == 0


@pytest.mark.asyncio
async def test_delete_not_found(client: AsyncClient, mock_ml_predict):
    resp = await client.delete("/api/estimates/history/9999")
    assert resp.status_code == 404
