from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db, init_db
from app.schemas import (
    AggregationResponse,
    FilterParams,
    AggregationType,
    ChartResponse,
    AnalyticsType
)
from app.services import AnalyticsService
from app import models
from app.api_import import router as import_router

app = FastAPI(
    title="Multi-Domain Analytics Backend API",
    description="A FastAPI backend for serving analytics metrics across Sales/E-commerce, Food Delivery, and SaaS domains",
    version="2.0.0"
)

# Include import router
app.include_router(import_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Domain Analytics Backend API",
        "version": "2.0.0",
        "supported_analytics_types": {
            "sales": "E-commerce / Sales Analytics",
            "food_delivery": "Food Delivery Analytics (Swiggy/Zomato style)",
            "saas": "SaaS Subscription Analytics (Stripe style)"
        },
        "endpoints": {
            "aggregations": "/api/v1/aggregate",
            "chart_data": "/api/v1/chart",
            "metrics_summary": "/api/v1/metrics/summary",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "analytics-backend"}


@app.get("/api/v1/aggregate", response_model=AggregationResponse)
async def get_aggregation(
    analytics_type: AnalyticsType = Query(..., description="Analytics domain: sales, food_delivery, or saas"),
    aggregation_type: AggregationType = Query(..., description="Type of aggregation (sum, avg, count, min, max)"),
    field: str = Query(..., description="Field to aggregate (varies by analytics_type)"),
    group_by: Optional[str] = Query(None, description="Field to group by (varies by analytics_type)"),
    # Sales filters
    category: Optional[str] = Query(None, description="Filter by category (sales)"),
    region: Optional[str] = Query(None, description="Filter by region (sales)"),
    product_name: Optional[str] = Query(None, description="Filter by product name (sales)"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method (sales)"),
    # Food delivery filters
    restaurant_name: Optional[str] = Query(None, description="Filter by restaurant name (food_delivery)"),
    cuisine_type: Optional[str] = Query(None, description="Filter by cuisine type (food_delivery)"),
    city: Optional[str] = Query(None, description="Filter by city (food_delivery)"),
    delivery_status: Optional[str] = Query(None, description="Filter by delivery status (food_delivery)"),
    # SaaS filters
    plan_name: Optional[str] = Query(None, description="Filter by plan name (saas)"),
    plan_type: Optional[str] = Query(None, description="Filter by plan type (saas)"),
    status: Optional[str] = Query(None, description="Filter by subscription status (saas)"),
    currency: Optional[str] = Query(None, description="Filter by currency (saas)"),
    # Common filters
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    start_date: Optional[datetime] = Query(None, description="Start date filter (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date filter (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Get aggregated metrics with optional filters and grouping.
    
    Supports three analytics domains:
    - **sales**: E-commerce/Sales Analytics
      - Fields: amount, quantity
      - Group by: category, region, product_name, payment_method
    - **food_delivery**: Food Delivery Analytics
      - Fields: order_amount, delivery_fee, tip_amount, total_amount, delivery_time_minutes
      - Group by: restaurant_name, cuisine_type, city, delivery_status
    - **saas**: SaaS Subscription Analytics
      - Fields: amount, mrr
      - Group by: plan_name, plan_type, status, currency
    """
    try:
        filters = FilterParams(
            category=category,
            region=region,
            product_name=product_name,
            payment_method=payment_method,
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            city=city,
            delivery_status=delivery_status,
            plan_name=plan_name,
            plan_type=plan_type,
            status=status,
            currency=currency,
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date
        )

        # Check if any filters are applied
        has_filters = any([
            category, region, product_name, payment_method,
            restaurant_name, cuisine_type, city, delivery_status,
            plan_name, plan_type, status, currency,
            customer_id, start_date, end_date
        ])

        result = AnalyticsService.aggregate(
            db=db,
            analytics_type=analytics_type,
            aggregation_type=aggregation_type,
            field=field,
            filters=filters if has_filters else None,
            group_by=group_by
        )

        return AggregationResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/chart", response_model=ChartResponse)
async def get_chart_data(
    analytics_type: AnalyticsType = Query(..., description="Analytics domain: sales, food_delivery, or saas"),
    chart_type: str = Query(..., description="Type of chart (bar, line, pie)"),
    field: str = Query(..., description="Field to aggregate (varies by analytics_type)"),
    group_by: str = Query(..., description="Field to group by (varies by analytics_type)"),
    # Sales filters
    category: Optional[str] = Query(None, description="Filter by category (sales)"),
    region: Optional[str] = Query(None, description="Filter by region (sales)"),
    product_name: Optional[str] = Query(None, description="Filter by product name (sales)"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method (sales)"),
    # Food delivery filters
    restaurant_name: Optional[str] = Query(None, description="Filter by restaurant name (food_delivery)"),
    cuisine_type: Optional[str] = Query(None, description="Filter by cuisine type (food_delivery)"),
    city: Optional[str] = Query(None, description="Filter by city (food_delivery)"),
    delivery_status: Optional[str] = Query(None, description="Filter by delivery status (food_delivery)"),
    # SaaS filters
    plan_name: Optional[str] = Query(None, description="Filter by plan name (saas)"),
    plan_type: Optional[str] = Query(None, description="Filter by plan type (saas)"),
    status: Optional[str] = Query(None, description="Filter by subscription status (saas)"),
    currency: Optional[str] = Query(None, description="Filter by currency (saas)"),
    # Common filters
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    start_date: Optional[datetime] = Query(None, description="Start date filter (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date filter (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Get chart-ready JSON data for visualization.
    
    Returns data in a format suitable for BI tools and charting libraries.
    Supports all three analytics domains (sales, food_delivery, saas).
    """
    try:
        filters = FilterParams(
            category=category,
            region=region,
            product_name=product_name,
            payment_method=payment_method,
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            city=city,
            delivery_status=delivery_status,
            plan_name=plan_name,
            plan_type=plan_type,
            status=status,
            currency=currency,
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date
        )

        has_filters = any([
            category, region, product_name, payment_method,
            restaurant_name, cuisine_type, city, delivery_status,
            plan_name, plan_type, status, currency,
            customer_id, start_date, end_date
        ])

        result = AnalyticsService.get_chart_data(
            db=db,
            analytics_type=analytics_type,
            chart_type=chart_type,
            field=field,
            group_by=group_by,
            filters=filters if has_filters else None
        )

        return ChartResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/metrics/summary")
async def get_metrics_summary(
    analytics_type: AnalyticsType = Query(..., description="Analytics domain: sales, food_delivery, or saas"),
    # Sales filters
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    # Food delivery filters
    city: Optional[str] = Query(None),
    cuisine_type: Optional[str] = Query(None),
    # SaaS filters
    plan_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    # Common filters
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get a summary of key metrics for the specified analytics type.
    """
    try:
        filters = FilterParams(
            category=category,
            region=region,
            city=city,
            cuisine_type=cuisine_type,
            plan_name=plan_name,
            status=status,
            start_date=start_date,
            end_date=end_date
        )

        has_filters = any([category, region, city, cuisine_type, plan_name, status, start_date, end_date])

        # Determine primary field based on analytics type
        if analytics_type == AnalyticsType.SALES:
            primary_field = "amount"
        elif analytics_type == AnalyticsType.FOOD_DELIVERY:
            primary_field = "total_amount"
        else:  # SAAS
            primary_field = "mrr"

        total = AnalyticsService.aggregate(
            db=db,
            analytics_type=analytics_type,
            aggregation_type=AggregationType.SUM,
            field=primary_field,
            filters=filters if has_filters else None
        )

        average = AnalyticsService.aggregate(
            db=db,
            analytics_type=analytics_type,
            aggregation_type=AggregationType.AVG,
            field=primary_field,
            filters=filters if has_filters else None
        )

        count = AnalyticsService.aggregate(
            db=db,
            analytics_type=analytics_type,
            aggregation_type=AggregationType.COUNT,
            field=primary_field,
            filters=filters if has_filters else None
        )

        return {
            "analytics_type": analytics_type.value,
            "total": total["value"],
            "average": average["value"],
            "count": count["value"],
            "filters_applied": filters.model_dump(exclude_none=True)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/fields")
async def get_available_fields(
    analytics_type: AnalyticsType = Query(..., description="Analytics domain: sales, food_delivery, or saas")
):
    """
    Get available fields for aggregation and grouping for a specific analytics type.
    """
    config = AnalyticsService.get_config(analytics_type)
    return {
        "analytics_type": analytics_type.value,
        "aggregatable_fields": config["aggregatable_fields"],
        "groupable_fields": config["groupable_fields"],
        "filterable_fields": list(config["filter_fields"].keys())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
