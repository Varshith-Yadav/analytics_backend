# Analytics Backend API

A FastAPI-based analytics backend for serving metrics and dashboard data. This application provides RESTful endpoints for aggregations, filtering, and chart-ready JSON data suitable for BI tools and dashboards.

## Features

### Core Features
- **Aggregations**: Support for sum, average, count, min, and max operations
- **Filters**: Filter data by category, region, product name, and date ranges
- **Grouping**: Group results by category, region, or product name
- **Chart-Ready JSON**: Endpoints that return data formatted for visualization libraries

### API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /api/v1/aggregate` - Perform aggregations with optional filters and grouping
- `GET /api/v1/chart` - Get chart-ready JSON data for visualizations
- `GET /api/v1/metrics/summary` - Get summary of key metrics

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database and seed sample data**
   ```bash
   python -m app.seed_data
   ```

## Running the Application

### Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Production deployment

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Testing

### Run all tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=app --cov-report=html
```

### Run specific test file

```bash
pytest tests/test_aggregations.py
```

### Test Coverage

The test suite includes:
- ✅ Unit tests for aggregations (sum, avg, count, min, max)
- ✅ Integration tests for filters (category, region, date range)
- ✅ Tests for group_by functionality
- ✅ Tests for chart endpoint
- ✅ Tests for metrics summary
- ✅ Error handling tests (invalid fields, invalid group_by)
- ✅ Health check tests

**Total: 10+ tests covering happy paths, edge cases, and error scenarios**

## Sample Client

A sample client script is provided to demonstrate API usage:

```bash
python sample_client.py
```

Make sure the server is running before executing the sample client.

## API Usage Examples

### 1. Get sum of all sales

```bash
curl "http://localhost:8000/api/v1/aggregate?aggregation_type=sum&field=amount"
```

### 2. Get average transaction amount for Electronics category

```bash
curl "http://localhost:8000/api/v1/aggregate?aggregation_type=avg&field=amount&category=Electronics"
```

### 3. Get total sales grouped by category

```bash
curl "http://localhost:8000/api/v1/aggregate?aggregation_type=sum&field=amount&group_by=category"
```

### 4. Get sales with multiple filters

```bash
curl "http://localhost:8000/api/v1/aggregate?aggregation_type=sum&field=amount&category=Electronics&region=North"
```

### 5. Get chart-ready data

```bash
curl "http://localhost:8000/api/v1/chart?chart_type=bar&field=amount&group_by=category"
```

### 6. Get metrics summary

```bash
curl "http://localhost:8000/api/v1/metrics/summary?category=Electronics&region=North"
```

## API Parameters

### Aggregation Endpoint (`/api/v1/aggregate`)

**Required:**
- `aggregation_type`: One of `sum`, `avg`, `count`, `min`, `max`
- `field`: Field to aggregate (`amount` or `quantity`)

**Optional:**
- `group_by`: Group results by (`category`, `region`, `product_name`)
- `category`: Filter by category
- `region`: Filter by region
- `product_name`: Filter by product name
- `start_date`: Start date filter (ISO format)
- `end_date`: End date filter (ISO format)

### Chart Endpoint (`/api/v1/chart`)

**Required:**
- `chart_type`: Type of chart (`bar`, `line`, `pie`)
- `field`: Field to aggregate (`amount` or `quantity`)
- `group_by`: Field to group by (`category`, `region`, `product_name`)

**Optional:** Same filters as aggregation endpoint

## Response Format

### Aggregation Response

```json
{
  "aggregation_type": "sum",
  "field": "amount",
  "value": 12345.67,
  "filters_applied": {
    "category": "Electronics"
  }
}
```

### Grouped Aggregation Response

```json
{
  "aggregation_type": "sum",
  "field": "amount",
  "group_by": "category",
  "groups": [
    {"group": "Electronics", "value": 5000.0},
    {"group": "Furniture", "value": 3000.0}
  ],
  "filters_applied": {}
}
```

### Chart Response

```json
{
  "chart_type": "bar",
  "data": [
    {"label": "Electronics", "value": 5000.0, "metadata": {}},
    {"label": "Furniture", "value": 3000.0, "metadata": {}}
  ],
  "metadata": {
    "field": "amount",
    "group_by": "category",
    "total_points": 2
  }
}
```

## Performance

- Query execution time target: **<100ms** (sample data)
- Optimized with database indexes on frequently filtered fields
- Efficient SQL aggregation queries

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid parameters (invalid field, invalid group_by, etc.)
- **500 Internal Server Error**: Server-side errors with descriptive messages

All errors return JSON responses with error details:

```json
{
  "detail": "Invalid field. Must be one of: ['amount', 'quantity']"
}
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic and analytics service
│   └── seed_data.py         # Database seeding script
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_aggregations.py # Aggregation tests
│   ├── test_filters.py      # Filter tests
│   ├── test_chart_endpoint.py # Chart endpoint tests
│   ├── test_metrics_summary.py # Summary tests
│   └── test_health.py       # Health check tests
├── sample_client.py         # Sample client script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── analytics.db            # SQLite database (created on first run)
```

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database (can be easily switched to PostgreSQL)
- **Pytest**: Testing framework

## Real-World Context

This analytics backend is designed to serve data to:
- **BI Tools**: Tableau, Power BI, Looker
- **Dashboard Applications**: React dashboards, Vue dashboards
- **Data Visualization Libraries**: Chart.js, D3.js, Plotly
- **Custom Analytics Platforms**

The chart-ready JSON format makes it easy to integrate with any frontend visualization library.

## Development

### Adding New Aggregations

1. Add the aggregation type to `AggregationType` enum in `app/schemas.py`
2. Implement the logic in `AnalyticsService.aggregate_sales()` in `app/services.py`
3. Add tests in `tests/test_aggregations.py`

### Adding New Filters

1. Add filter field to `FilterParams` in `app/schemas.py`
2. Implement filter logic in `AnalyticsService.apply_filters()` in `app/services.py`
3. Add tests in `tests/test_filters.py`

## License

This project is provided as-is for educational and demonstration purposes.

