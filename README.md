# Multi-Domain Analytics Backend API

A FastAPI-based analytics backend for serving metrics and dashboard data across **three major business domains**:
- **Sales / E-commerce Analytics**
- **Food Delivery Analytics** (Swiggy/Zomato style)
- **SaaS Subscription Analytics** (Stripe style)

This application provides RESTful endpoints for aggregations, filtering, and chart-ready JSON data suitable for BI tools and dashboards.

## Features

### Core Features
- **Multi-Domain Support**: Single API for three different analytics domains
- **Aggregations**: Support for sum, average, count, min, and max operations
- **Filters**: Domain-specific filtering capabilities
- **Grouping**: Group results by various categorical fields
- **Chart-Ready JSON**: Endpoints that return data formatted for visualization libraries

### Supported Analytics Domains

#### 1. Sales / E-commerce Analytics
- **Aggregatable Fields**: `amount`, `quantity`
- **Groupable Fields**: `category`, `region`, `product_name`, `payment_method`
- **Filters**: category, region, product_name, payment_method, customer_id, date range

#### 2. Food Delivery Analytics (Swiggy/Zomato style)
- **Aggregatable Fields**: `order_amount`, `delivery_fee`, `tip_amount`, `total_amount`, `delivery_time_minutes`
- **Groupable Fields**: `restaurant_name`, `cuisine_type`, `city`, `delivery_status`
- **Filters**: restaurant_name, cuisine_type, city, delivery_status, customer_id, date range

#### 3. SaaS Subscription Analytics (Stripe style)
- **Aggregatable Fields**: `amount`, `mrr` (Monthly Recurring Revenue)
- **Groupable Fields**: `plan_name`, `plan_type`, `status`, `currency`
- **Filters**: plan_name, plan_type, status, currency, customer_id, date range

## API Endpoints

### Analytics Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /api/v1/fields` - Get available fields for an analytics type
- `GET /api/v1/aggregate` - Perform aggregations with optional filters and grouping
- `GET /api/v1/chart` - Get chart-ready JSON data for visualizations
- `GET /api/v1/metrics/summary` - Get summary of key metrics

### Data Import Endpoints
- `POST /api/v1/import/sales/csv` - Import sales data from CSV
- `POST /api/v1/import/sales/json` - Import sales data from JSON
- `POST /api/v1/import/food_delivery/csv` - Import food orders from CSV
- `POST /api/v1/import/food_delivery/json` - Import food orders from JSON
- `POST /api/v1/import/saas/csv` - Import subscriptions from CSV
- `POST /api/v1/import/saas/json` - Import subscriptions from JSON

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

4. **Initialize the database and seed sample data (optional)**
   ```bash
   python -m app.scripts.seed_data
   ```

   This will create sample data for all three analytics domains:
   - 500 sales transactions
   - 500 food delivery orders
   - 300 SaaS subscriptions

   **Note**: For production use, import your own data using the import methods below.

## Running the Application

### Start the development server

```bash
uvicorn app.main:app --reload
```

Or use the quick start script:

```bash
python run.py
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

The test suite includes **20+ tests** covering:
- ✅ Unit tests for aggregations across all three domains
- ✅ Integration tests for filters (all domains)
- ✅ Tests for group_by functionality
- ✅ Tests for chart endpoint (all domains)
- ✅ Tests for metrics summary (all domains)
- ✅ Error handling tests (invalid fields, invalid group_by, invalid analytics_type)
- ✅ Health check tests

## Sample Client

A comprehensive sample client script demonstrates usage for all three analytics domains:

```bash
python sample_client.py
```

Make sure the server is running before executing the sample client.

## API Usage Examples

### Get Available Fields

```bash
# Get available fields for sales analytics
curl "http://localhost:8000/api/v1/fields?analytics_type=sales"

# Get available fields for food delivery
curl "http://localhost:8000/api/v1/fields?analytics_type=food_delivery"

# Get available fields for SaaS
curl "http://localhost:8000/api/v1/fields?analytics_type=saas"
```

### Sales / E-commerce Analytics

#### 1. Get total sales amount

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount"
```

#### 2. Get sales grouped by category

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount&group_by=category"
```

#### 3. Get average transaction for Electronics category

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=sales&aggregation_type=avg&field=amount&category=Electronics"
```

#### 4. Get chart data - Sales by region

```bash
curl "http://localhost:8000/api/v1/chart?analytics_type=sales&chart_type=bar&field=amount&group_by=region"
```

### Food Delivery Analytics

#### 1. Get total order value

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount"
```

#### 2. Get orders grouped by cuisine type

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount&group_by=cuisine_type"
```

#### 3. Get average delivery time for delivered orders

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=avg&field=delivery_time_minutes&delivery_status=delivered"
```

#### 4. Get chart data - Orders by city

```bash
curl "http://localhost:8000/api/v1/chart?analytics_type=food_delivery&chart_type=pie&field=total_amount&group_by=city"
```

### SaaS Subscription Analytics

#### 1. Get total MRR (Monthly Recurring Revenue)

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr"
```

#### 2. Get MRR grouped by plan

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr&group_by=plan_name"
```

#### 3. Get active subscriptions count

```bash
curl "http://localhost:8000/api/v1/aggregate?analytics_type=saas&aggregation_type=count&field=mrr&status=active"
```

#### 4. Get chart data - MRR by status

```bash
curl "http://localhost:8000/api/v1/chart?analytics_type=saas&chart_type=bar&field=mrr&group_by=status"
```

### Metrics Summary

#### Get summary for any analytics type

```bash
# Sales summary
curl "http://localhost:8000/api/v1/metrics/summary?analytics_type=sales"

# Food delivery summary
curl "http://localhost:8000/api/v1/metrics/summary?analytics_type=food_delivery"

# SaaS summary
curl "http://localhost:8000/api/v1/metrics/summary?analytics_type=saas"
```

## API Parameters

### Aggregation Endpoint (`/api/v1/aggregate`)

**Required:**
- `analytics_type`: One of `sales`, `food_delivery`, or `saas`
- `aggregation_type`: One of `sum`, `avg`, `count`, `min`, `max`
- `field`: Field to aggregate (varies by analytics_type)

**Optional:**
- `group_by`: Group results by (varies by analytics_type)
- Domain-specific filters (see field documentation)
- `start_date`: Start date filter (ISO format)
- `end_date`: End date filter (ISO format)
- `customer_id`: Filter by customer ID

### Chart Endpoint (`/api/v1/chart`)

**Required:**
- `analytics_type`: One of `sales`, `food_delivery`, or `saas`
- `chart_type`: Type of chart (`bar`, `line`, `pie`)
- `field`: Field to aggregate (varies by analytics_type)
- `group_by`: Field to group by (varies by analytics_type)

**Optional:** Same filters as aggregation endpoint

## Response Format

### Aggregation Response

```json
{
  "analytics_type": "sales",
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
  "analytics_type": "food_delivery",
  "aggregation_type": "sum",
  "field": "total_amount",
  "group_by": "cuisine_type",
  "groups": [
    {"group": "Italian", "value": 5000.0},
    {"group": "Indian", "value": 8000.0}
  ],
  "filters_applied": {}
}
```

### Chart Response

```json
{
  "analytics_type": "saas",
  "chart_type": "bar",
  "data": [
    {"label": "Basic", "value": 1000.0, "metadata": {}},
    {"label": "Pro", "value": 5000.0, "metadata": {}}
  ],
  "metadata": {
    "field": "mrr",
    "group_by": "plan_name",
    "total_points": 2
  }
}
```

## Performance

- Query execution time target: **<100ms** (sample data)
- Optimized with database indexes on frequently filtered fields
- Efficient SQL aggregation queries
- Supports all three analytics domains with consistent performance

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid parameters (invalid field, invalid group_by, etc.)
- **422 Unprocessable Entity**: Invalid analytics_type or missing required parameters
- **500 Internal Server Error**: Server-side errors with descriptive messages

All errors return JSON responses with error details:

```json
{
  "detail": "Invalid field for sales. Must be one of: ['amount', 'quantity']"
}
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/                      # Core configuration and database
│   │   ├── __init__.py
│   │   ├── config.py              # Application settings
│   │   └── database.py            # Database configuration and session management
│   ├── models/                    # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model class
│   │   ├── sales.py              # Sales/E-commerce models
│   │   ├── food_delivery.py      # Food delivery models
│   │   └── saas.py               # SaaS subscription models
│   ├── schemas/                   # Pydantic schemas for API
│   │   ├── __init__.py
│   │   └── common.py             # Common schemas (enums, request/response models)
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── analytics.py          # Analytics service (aggregations, chart data)
│   │   └── import_service.py     # Data import service
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── analytics.py      # Analytics endpoints
│   │       └── import_routes.py  # Data import endpoints
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   └── data_import.py        # Data import utilities (CSV/JSON)
│   └── scripts/                   # Utility scripts
│       ├── __init__.py
│       └── seed_data.py          # Database seeding script
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_aggregations.py      # Aggregation tests (all domains)
│   ├── test_filters.py           # Filter tests (all domains)
│   ├── test_chart_endpoint.py    # Chart endpoint tests
│   ├── test_metrics_summary.py   # Summary tests
│   └── test_health.py            # Health check tests
├── templates/                     # Data import templates
│   ├── sales_template.csv
│   ├── sales_template.json
│   ├── food_delivery_template.csv
│   └── saas_template.csv
├── sample_client.py              # Sample client script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── run.py                        # Quick start script
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Docker image definition
└── analytics.db                  # SQLite database (created on first run)
```

### Architecture Overview

The project follows a **layered architecture** with clear separation of concerns:

- **Core Layer** (`app/core/`): Database configuration and application settings
- **Models Layer** (`app/models/`): Database models organized by domain
- **Schemas Layer** (`app/schemas/`): API request/response validation schemas
- **Services Layer** (`app/services/`): Business logic and domain services
- **API Layer** (`app/api/`): REST API endpoints organized by version
- **Utils Layer** (`app/utils/`): Reusable utility functions
- **Scripts Layer** (`app/scripts/`): Database management and seeding scripts

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database (can be easily switched to PostgreSQL)
- **Pytest**: Testing framework

## Importing Your Own Data

Organizations can import their own datasets in three ways:

### Method 1: CSV/JSON Import via CLI

**Sales Data:**
```bash
python -m app.utils.data_import sales your_sales_data.csv csv
python -m app.utils.data_import sales your_sales_data.json json
```

**Food Delivery Data:**
```bash
python -m app.utils.data_import food_delivery your_orders.csv csv
python -m app.utils.data_import food_delivery your_orders.json json
```

**SaaS Data:**
```bash
python -m app.utils.data_import saas your_subscriptions.csv csv
python -m app.utils.data_import saas your_subscriptions.json json
```

### Method 2: API Upload (Recommended)

**Upload via cURL:**
```bash
# Sales CSV
curl -X POST "http://localhost:8000/api/v1/import/sales/csv" \
  -F "file=@your_sales_data.csv"

# Food Delivery JSON
curl -X POST "http://localhost:8000/api/v1/import/food_delivery/json" \
  -F "file=@your_orders.json"

# SaaS CSV
curl -X POST "http://localhost:8000/api/v1/import/saas/csv" \
  -F "file=@your_subscriptions.csv"
```

**Upload via Python:**
```python
import requests

with open('sales_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/import/sales/csv',
        files={'file': f}
    )
    print(response.json())
```

**Upload via Swagger UI:**
1. Navigate to `http://localhost:8000/docs`
2. Find import endpoints under "Data Import"
3. Upload your file and execute

### Method 3: Using Template Files

Template CSV and JSON files are available in `templates/` directory:
- `templates/sales_template.csv` / `templates/sales_template.json`
- `templates/food_delivery_template.csv`
- `templates/saas_template.csv`

Use these as starting points for formatting your data.

### Data Format Requirements

**Sales CSV Columns:**
```
product_name, category, amount, quantity, region, customer_id, payment_method, sale_date
```

**Food Delivery CSV Columns:**
```
order_id, restaurant_name, cuisine_type, order_amount, delivery_fee, tip_amount,
total_amount, customer_id, city, delivery_status, order_date, delivery_time_minutes
```

**SaaS CSV Columns:**
```
subscription_id, customer_id, plan_name, plan_type, amount, status, currency,
billing_cycle_start, billing_cycle_end, cancelled_at, mrr
```

For detailed import instructions, see [Data Import Guide](docs/DATA_IMPORT_GUIDE.md).

## Real-World Context

This analytics backend is designed to serve data to:

### Sales / E-commerce
- E-commerce dashboards (Amazon, Flipkart style)
- Sales performance tracking
- Product category analysis
- Regional sales reports

### Food Delivery
- Restaurant performance metrics
- Delivery time analytics
- City-wise order analysis
- Cuisine popularity tracking
- Delivery status monitoring

### SaaS Subscriptions
- MRR (Monthly Recurring Revenue) tracking
- Churn analysis
- Plan performance metrics
- Subscription lifecycle management
- Revenue forecasting

### Integration
- **BI Tools**: Tableau, Power BI, Looker
- **Dashboard Applications**: React dashboards, Vue dashboards
- **Data Visualization Libraries**: Chart.js, D3.js, Plotly
- **Custom Analytics Platforms**

The chart-ready JSON format makes it easy to integrate with any frontend visualization library.

## Development

### Adding New Analytics Domains

1. Add a new model in `app/models/` (create a new file or add to existing domain file)
2. Add configuration in `AnalyticsService.ANALYTICS_CONFIG` in `app/services/analytics.py`
3. Update `FilterParams` in `app/schemas/common.py` if needed
4. Add seed data function in `app/scripts/seed_data.py`
5. Add tests in `tests/`

### Adding New Aggregations

1. Add the aggregation type to `AggregationType` enum in `app/schemas/common.py`
2. Implement the logic in `AnalyticsService.aggregate()` in `app/services/analytics.py`
3. Add tests in `tests/test_aggregations.py`

### Adding New Filters

1. Add filter field to `FilterParams` in `app/schemas/common.py`
2. Add filter mapping in `ANALYTICS_CONFIG` in `app/services/analytics.py`
3. Implement filter logic in `AnalyticsService.apply_filters()` in `app/services/analytics.py`
4. Add tests in `tests/test_filters.py`

## License

This project is provided as-is for educational and demonstration purposes.
