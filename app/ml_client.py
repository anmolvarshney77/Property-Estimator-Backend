"""Async HTTP client for the ML Model API (Task 1)."""

import httpx

from app.config import settings


class MlModelClient:
    """Wraps httpx.AsyncClient for calls to the ML prediction service."""

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.ML_MODEL_URL,
            timeout=httpx.Timeout(10.0),
        )

    async def stop(self) -> None:
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("ML client not initialised; call start() first")
        return self._client

    async def is_healthy(self) -> bool:
        try:
            resp = await self.client.get("/health", timeout=3.0)
            return resp.status_code == 200
        except httpx.HTTPError:
            return False

    async def predict_single(self, features: dict) -> float:
        resp = await self.client.post("/predict", json=features)
        resp.raise_for_status()
        return resp.json()["prediction"]["predicted_price"]

    async def predict_batch(self, instances: list[dict]) -> list[float]:
        resp = await self.client.post("/predict/batch", json={"instances": instances})
        resp.raise_for_status()
        return [p["predicted_price"] for p in resp.json()["predictions"]]


ml_client = MlModelClient()
