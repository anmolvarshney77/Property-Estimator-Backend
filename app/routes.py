"""API route handlers."""

import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import MlModelUnavailableError
from app.ml_client import ml_client
from app.models import Estimate
from app.schemas import (
    CompareRequest,
    CompareResponse,
    CompareResult,
    EstimateResponse,
    HealthResponse,
    PaginatedHistory,
    PropertyFeatures,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Service health check -- also verifies ML model connectivity."""
    connected = await ml_client.is_healthy()
    return HealthResponse(status="healthy", ml_model_connected=connected)


@router.post("/api/estimates", response_model=EstimateResponse, status_code=201, tags=["Estimates"])
async def create_estimate(
    features: PropertyFeatures,
    db: AsyncSession = Depends(get_db),
) -> EstimateResponse:
    """Submit property features, get a price prediction, and store the result."""
    try:
        predicted_price = await ml_client.predict_single(features.model_dump())
    except Exception as exc:
        raise MlModelUnavailableError(f"ML model API unreachable: {exc}") from exc

    estimate = Estimate(
        **features.model_dump(),
        predicted_price=predicted_price,
    )
    db.add(estimate)
    await db.commit()
    await db.refresh(estimate)
    return EstimateResponse.model_validate(estimate)


@router.get("/api/estimates/history", response_model=PaginatedHistory, tags=["Estimates"])
async def get_history(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> PaginatedHistory:
    """Return paginated history of all estimates, newest first."""
    total_result = await db.execute(select(func.count(Estimate.id)))
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await db.execute(
        select(Estimate).order_by(Estimate.created_at.desc()).offset(offset).limit(size)
    )
    items = result.scalars().all()

    return PaginatedHistory(
        items=[EstimateResponse.model_validate(e) for e in items],
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 0,
    )


@router.delete("/api/estimates/history/{estimate_id}", status_code=204, tags=["Estimates"])
async def delete_estimate(
    estimate_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a single estimate by ID."""
    result = await db.execute(select(Estimate).where(Estimate.id == estimate_id))
    estimate = result.scalar_one_or_none()
    if estimate is None:
        raise HTTPException(status_code=404, detail="Estimate not found")
    await db.delete(estimate)
    await db.commit()


@router.post("/api/estimates/compare", response_model=CompareResponse, tags=["Estimates"])
async def compare_properties(request: CompareRequest) -> CompareResponse:
    """Compare 2-5 properties side-by-side. Results are NOT stored in history."""
    instances = [p.model_dump() for p in request.properties]
    try:
        prices = await ml_client.predict_batch(instances)
    except Exception as exc:
        raise MlModelUnavailableError(f"ML model API unreachable: {exc}") from exc

    results = [
        CompareResult(features=features, predicted_price=price)
        for features, price in zip(request.properties, prices)
    ]
    return CompareResponse(results=results)
