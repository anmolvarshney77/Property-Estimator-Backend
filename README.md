# Property Estimator Backend

FastAPI middleware between the Housing Insights Portal frontend and the ML price-prediction model (Task 1). Accepts property features, forwards them for prediction, stores results for history tracking, and supports side-by-side comparison.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/estimates` | Create a price estimate |
| `GET` | `/api/estimates/history` | Paginated history (query: `page`, `size`) |
| `DELETE` | `/api/estimates/history/{id}` | Delete an estimate |
| `POST` | `/api/estimates/compare` | Compare 2-5 properties |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI |

## Prerequisites

- Python 3.12+
- Task 1 ML Model API running on `http://localhost:8000`

## Local Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
```

Uses SQLite by default (`estimator.db`). Tables are created automatically on startup.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./estimator.db` | DB connection string |
| `ML_MODEL_URL` | `http://localhost:8000` | ML model API base URL |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | CORS origins (comma-separated) |
| `LOG_LEVEL` | `INFO` | Logging level |

## Production (PostgreSQL)

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/estimator uvicorn app.main:app --port 8001
```

## Docker

```bash
docker build -t property-estimator-backend .
docker run -p 8001:8001 -e ML_MODEL_URL=http://host.docker.internal:8000 property-estimator-backend
```

## Tests

```bash
pytest -v
```

## Example Requests

```bash
# Create estimate
curl -X POST http://localhost:8001/api/estimates \
  -H "Content-Type: application/json" \
  -d '{"square_footage":1550,"bedrooms":3,"bathrooms":2,"year_built":1997,"lot_size":6800,"distance_to_city_center":4.1,"school_rating":7.6}'

# History
curl http://localhost:8001/api/estimates/history?page=1&size=10

# Compare
curl -X POST http://localhost:8001/api/estimates/compare \
  -H "Content-Type: application/json" \
  -d '{"properties":[{"square_footage":1550,"bedrooms":3,"bathrooms":2,"year_built":1997,"lot_size":6800,"distance_to_city_center":4.1,"school_rating":7.6},{"square_footage":2200,"bedrooms":4,"bathrooms":2.5,"year_built":2008,"lot_size":9600,"distance_to_city_center":7.0,"school_rating":8.8}]}'
```
