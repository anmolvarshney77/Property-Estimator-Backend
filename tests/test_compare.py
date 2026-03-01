"""Tests for the compare endpoint."""

import pytest
from httpx import AsyncClient

PROPERTY_A = {
    "square_footage": 1550, "bedrooms": 3, "bathrooms": 2,
    "year_built": 1997, "lot_size": 6800,
    "distance_to_city_center": 4.1, "school_rating": 7.6,
}
PROPERTY_B = {
    "square_footage": 2200, "bedrooms": 4, "bathrooms": 2.5,
    "year_built": 2008, "lot_size": 9600,
    "distance_to_city_center": 7.0, "school_rating": 8.8,
}


@pytest.mark.asyncio
async def test_compare_two_properties(client: AsyncClient, mock_ml_predict):
    resp = await client.post(
        "/api/estimates/compare",
        json={"properties": [PROPERTY_A, PROPERTY_B]},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["results"]) == 2
    assert body["results"][0]["predicted_price"] == 250000.0
    assert body["results"][1]["predicted_price"] == 350000.0


@pytest.mark.asyncio
async def test_compare_too_few(client: AsyncClient, mock_ml_predict):
    resp = await client.post(
        "/api/estimates/compare",
        json={"properties": [PROPERTY_A]},
    )
    assert resp.status_code == 422
