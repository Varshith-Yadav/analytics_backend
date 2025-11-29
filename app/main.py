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
    ChartResponse
)
from app.services import AnalyticsService
from app import models

app = FastAPI(
    title="Analytics Backend API",
    description="A FastAPI backend for serving analytics metrics and dashboards",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Analytics Backend API",
        "version": "1.0.0",
        "endpoints": {
            "aggregations": "/api/v1/aggregate",
            "chart_data": "/api/v1/chart",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "analytics-backend"}


@app.get("/api/v1/aggregate", response_model=AggregationResponse)
async def get_aggregation(
    aggregation_type: AggregationType = Query(..., description="Type of aggregation (sum, avg, count, min, max)"),
    field: str = Query(..., description="Field to aggregate (amount, quantity)"),
    group_by: Optional[str] = Query(None, description="Field to group by (category, region, product_name)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    region: Optional[str] = Query(None, description="Filter by region"),
    product_name: Optional[str] = Query(None, description="Filter by product name"),
    start_date: Optional[datetime] = Query(None, description="Start date filter (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date filter (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Get aggregated metrics with optional filters and grouping.
    
    Supports:
    - Aggregation types: sum, avg, count, min, max
    - Fields: amount, quantity
    - Group by: category, region, product_name
    - Filters: category, region, product_name, date range
    """
    try:
        filters = FilterParams(
            category=category,
            region=region,
            product_name=product_name,
            start_date=start_date,
            end_date=end_date
        )

        result = AnalyticsService.aggregate_sales(
            db=db,
            aggregation_type=aggregation_type,
            field=field,
            filters=filters if any([category, region, product_name, start_date, end_date]) else None,
            group_by=group_by
        )

        return AggregationResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/chart", response_model=ChartResponse)
async def get_chart_data(
    chart_type: str = Query(..., description="Type of chart (bar, line, pie)"),
    field: str = Query(..., description="Field to aggregate (amount, quantity)"),
    group_by: str = Query(..., description="Field to group by (category, region, product_name)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    region: Optional[str] = Query(None, description="Filter by region"),
    product_name: Optional[str] = Query(None, description="Filter by product name"),
    start_date: Optional[datetime] = Query(None, description="Start date filter (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date filter (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Get chart-ready JSON data for visualization.
    
    Returns data in a format suitable for BI tools and charting libraries.
    """
    try:
        filters = FilterParams(
            category=category,
            region=region,
            product_name=product_name,
            start_date=start_date,
            end_date=end_date
        )

        result = AnalyticsService.get_chart_data(
            db=db,
            chart_type=chart_type,
            field=field,
            group_by=group_by,
            filters=filters if any([category, region, product_name, start_date, end_date]) else None
        )

        return ChartResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/metrics/summary")
async def get_metrics_summary(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get a summary of key metrics (total sales, average transaction, count).
    """
    try:
        filters = FilterParams(
            category=category,
            region=region,
            start_date=start_date,
            end_date=end_date
        )

        total_sales = AnalyticsService.aggregate_sales(
            db=db,
            aggregation_type=AggregationType.SUM,
            field="amount",
            filters=filters if any([category, region, start_date, end_date]) else None
        )

        avg_transaction = AnalyticsService.aggregate_sales(
            db=db,
            aggregation_type=AggregationType.AVG,
            field="amount",
            filters=filters if any([category, region, start_date, end_date]) else None
        )

        transaction_count = AnalyticsService.aggregate_sales(
            db=db,
            aggregation_type=AggregationType.COUNT,
            field="amount",
            filters=filters if any([category, region, start_date, end_date]) else None
        )

        return {
            "total_sales": total_sales["value"],
            "average_transaction": avg_transaction["value"],
            "transaction_count": transaction_count["value"],
            "filters_applied": filters.model_dump(exclude_none=True)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

