# Data Import Guide

This guide explains how organizations can import their own datasets into the Analytics Backend.

## Overview

The Analytics Backend supports data import for all three analytics domains:
- **Sales / E-commerce Analytics**
- **Food Delivery Analytics**
- **SaaS Subscription Analytics**

You can import data via:
1. **CSV files** (recommended for bulk imports)
2. **JSON files** (flexible format)
3. **API endpoints** (for programmatic uploads)

## Method 1: CSV Import (CLI)

### Sales / E-commerce Data

1. **Prepare your CSV file** with the following columns:
   ```
   product_name, category, amount, quantity, region, customer_id, payment_method, sale_date
   ```

2. **Example CSV:**
   ```csv
   product_name,category,amount,quantity,region,customer_id,payment_method,sale_date
   Laptop Pro,Electronics,1200.00,2,North,CUST_1001,credit_card,2024-01-15 10:30:00
   Smartphone X,Electronics,699.99,1,South,CUST_1002,debit_card,2024-01-16 14:20:00
   ```

3. **Import the data:**
   ```bash
   python -m app.data_import sales your_data.csv csv
   ```

### Food Delivery Data

1. **CSV columns required:**
   ```
   order_id, restaurant_name, cuisine_type, order_amount, delivery_fee, tip_amount, 
   total_amount, customer_id, city, delivery_status, order_date, delivery_time_minutes
   ```

2. **Import:**
   ```bash
   python -m app.data_import food_delivery your_orders.csv csv
   ```

### SaaS Subscription Data

1. **CSV columns required:**
   ```
   subscription_id, customer_id, plan_name, plan_type, amount, status, currency,
   billing_cycle_start, billing_cycle_end, cancelled_at, mrr
   ```

2. **Import:**
   ```bash
   python -m app.data_import saas your_subscriptions.csv csv
   ```

## Method 2: JSON Import (CLI)

### Sales Data JSON Format

```json
[
  {
    "product_name": "Laptop Pro",
    "category": "Electronics",
    "amount": 1200.00,
    "quantity": 2,
    "region": "North",
    "customer_id": "CUST_1001",
    "payment_method": "credit_card",
    "sale_date": "2024-01-15T10:30:00"
  }
]
```

**Import:**
```bash
python -m app.data_import sales your_data.json json
```

## Method 3: API Upload (Recommended for Production)

### Using cURL

**Upload Sales CSV:**
```bash
curl -X POST "http://localhost:8000/api/v1/import/sales/csv" \
  -F "file=@your_sales_data.csv"
```

**Upload Food Delivery JSON:**
```bash
curl -X POST "http://localhost:8000/api/v1/import/food_delivery/json" \
  -F "file=@your_orders.json"
```

**Upload SaaS CSV:**
```bash
curl -X POST "http://localhost:8000/api/v1/import/saas/csv" \
  -F "file=@your_subscriptions.csv"
```

### Using Python requests

```python
import requests

# Upload sales data
with open('sales_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/import/sales/csv',
        files={'file': f}
    )
    print(response.json())
```

### Using Swagger UI

1. Navigate to `http://localhost:8000/docs`
2. Find the import endpoints under "Data Import"
3. Click "Try it out"
4. Upload your file
5. Execute

## Field Mappings

### Sales / E-commerce

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| product_name | string | Yes | Name of the product |
| category | string | Yes | Product category |
| amount | float | Yes | Transaction amount |
| quantity | integer | Yes | Number of items |
| region | string | Yes | Sales region |
| customer_id | string | No | Customer identifier (auto-generated if missing) |
| payment_method | string | No | Payment method (default: credit_card) |
| sale_date | datetime | Yes | Date and time of sale |

### Food Delivery

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| order_id | string | No | Unique order ID (auto-generated if missing) |
| restaurant_name | string | Yes | Name of restaurant |
| cuisine_type | string | Yes | Type of cuisine |
| order_amount | float | Yes | Order amount before fees |
| delivery_fee | float | Yes | Delivery fee |
| tip_amount | float | Yes | Tip amount |
| total_amount | float | Yes | Total order amount |
| customer_id | string | No | Customer identifier |
| city | string | Yes | Delivery city |
| delivery_status | string | Yes | Status: pending, preparing, out_for_delivery, delivered, cancelled |
| order_date | datetime | Yes | Order date and time |
| delivery_time_minutes | integer | No | Delivery time in minutes |

### SaaS Subscriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| subscription_id | string | No | Unique subscription ID (auto-generated if missing) |
| customer_id | string | No | Customer identifier |
| plan_name | string | Yes | Plan name (e.g., Basic, Pro, Enterprise) |
| plan_type | string | Yes | monthly or annual |
| amount | float | Yes | Subscription amount |
| status | string | Yes | active, cancelled, past_due, trialing |
| currency | string | No | Currency code (default: USD) |
| billing_cycle_start | datetime | Yes | Billing cycle start date |
| billing_cycle_end | datetime | Yes | Billing cycle end date |
| cancelled_at | datetime | No | Cancellation date (if cancelled) |
| mrr | float | Yes | Monthly Recurring Revenue |

## Date Formats

The importer accepts various date formats:
- `2024-01-15 10:30:00`
- `2024-01-15T10:30:00`
- `2024-01-15`
- `15/01/2024 10:30:00`
- `15-01-2024 10:30:00`

## Data Validation

The import process validates:
- Required fields are present
- Numeric fields are valid numbers
- Date fields are parseable
- Enums match expected values

## Bulk Import Best Practices

1. **Chunk Large Files**: For files with >10,000 records, consider splitting into smaller chunks
2. **Validate Before Import**: Check your CSV/JSON format matches the template
3. **Backup First**: Always backup your database before bulk imports
4. **Monitor Progress**: Use the API response to track import success
5. **Handle Errors**: Review error messages and fix data issues

## Example: Complete Import Workflow

```bash
# 1. Prepare your data in CSV format
# 2. Validate the format matches the template
# 3. Import via CLI
python -m app.data_import sales my_sales_data.csv csv

# Or via API
curl -X POST "http://localhost:8000/api/v1/import/sales/csv" \
  -F "file=@my_sales_data.csv"

# 4. Verify import
curl "http://localhost:8000/api/v1/aggregate?analytics_type=sales&aggregation_type=count&field=amount"
```

## Troubleshooting

### Common Issues

1. **Date parsing errors**: Ensure dates are in a supported format
2. **Missing required fields**: Check all required columns are present
3. **Type mismatches**: Ensure numeric fields contain numbers
4. **Duplicate IDs**: The system will handle duplicates, but ensure unique IDs for better tracking

### Error Messages

- `Unable to parse date`: Check date format
- `Invalid field value`: Check data types match expected format
- `Missing required field`: Add missing columns to your CSV/JSON

## Template Files

Template CSV and JSON files are available in the `templates/` directory:
- `templates/sales_template.csv`
- `templates/food_delivery_template.csv`
- `templates/saas_template.csv`
- `templates/sales_template.json`

Use these as starting points for your data import.

