"""Custom exceptions and global error handlers."""

from fastapi import Request
from fastapi.responses import JSONResponse


class MlModelUnavailableError(Exception):
    """Raised when the ML model API cannot be reached."""


async def ml_model_unavailable_handler(_req: Request, exc: MlModelUnavailableError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})
