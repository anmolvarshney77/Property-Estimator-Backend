"""FastAPI application for the Property Estimator backend."""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.exceptions import MlModelUnavailableError, ml_model_unavailable_handler
from app.ml_client import ml_client
from app.models import Base
from app.routes import router

logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle: create tables (dev) and manage the ML client."""
    if settings.DATABASE_URL.startswith("sqlite"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("SQLite tables ensured")

    await ml_client.start()
    logger.info("ML client started -> %s", settings.ML_MODEL_URL)

    yield

    await ml_client.stop()
    logger.info("ML client closed")


app = FastAPI(
    title="Property Estimator API",
    description="Middleware between the frontend portal and the ML price-prediction model.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(MlModelUnavailableError, ml_model_unavailable_handler)
app.include_router(router)
