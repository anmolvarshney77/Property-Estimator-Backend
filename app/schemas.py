"""Pydantic request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class PropertyFeatures(BaseModel):
    """The 7 input features for a housing price prediction."""

    square_footage: float = Field(..., gt=0, description="Living area in sq ft")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms")
    bathrooms: float = Field(..., ge=0, description="Number of bathrooms")
    year_built: int = Field(..., ge=1800, le=2030, description="Year built")
    lot_size: float = Field(..., gt=0, description="Lot size in sq ft")
    distance_to_city_center: float = Field(..., ge=0, description="Miles to city center")
    school_rating: float = Field(..., ge=0, le=10, description="School rating 0-10")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "square_footage": 1550,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "year_built": 1997,
                    "lot_size": 6800,
                    "distance_to_city_center": 4.1,
                    "school_rating": 7.6,
                }
            ]
        }
    }


class EstimateResponse(BaseModel):
    id: int
    square_footage: float
    bedrooms: int
    bathrooms: float
    year_built: int
    lot_size: float
    distance_to_city_center: float
    school_rating: float
    predicted_price: float
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedHistory(BaseModel):
    items: list[EstimateResponse]
    total: int
    page: int
    size: int
    pages: int


class CompareRequest(BaseModel):
    properties: list[PropertyFeatures] = Field(..., min_length=2, max_length=5)


class CompareResult(BaseModel):
    features: PropertyFeatures
    predicted_price: float


class CompareResponse(BaseModel):
    results: list[CompareResult]


class HealthResponse(BaseModel):
    status: str
    ml_model_connected: bool
