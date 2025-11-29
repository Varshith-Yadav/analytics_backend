from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AnalyticsType(str, Enum):
    """Supported analytics domains"""
    SALES = "sales"  # E-commerce / Sales Analytics
    FOOD_DELIVERY = "food_delivery"  # Food Delivery (Swiggy/Zomato)
    SAAS = "saas"  # SaaS Subscription Analytics (Stripe style)


class AggregationType(str, Enum):
    """Supported aggregation types"""
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MIN = "min"
    MAX = "max"


class TimeRange(BaseModel):
    """Time range filter"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SalesMetricsResponse(BaseModel):
    """Response model for sales metrics"""
    metric: str
    value: float
    filters_applied: Dict[str, Any] = {}


class AggregationResponse(BaseModel):
    """Response model for aggregations"""
    analytics_type: str
    aggregation_type: str
    field: str
    value: Optional[float] = None
    group_by: Optional[str] = None
    groups: Optional[List[Dict[str, Any]]] = None
    filters_applied: Dict[str, Any] = {}


class ChartDataPoint(BaseModel):
    """Data point for chart visualization"""
    label: str
    value: float
    metadata: Optional[Dict[str, Any]] = None


class ChartResponse(BaseModel):
    """Chart-ready JSON response"""
    analytics_type: str
    chart_type: str
    data: List[ChartDataPoint]
    metadata: Dict[str, Any] = {}


class FilterParams(BaseModel):
    """Common filter parameters - supports all analytics types"""
    # Sales/E-commerce filters
    category: Optional[str] = None
    region: Optional[str] = None
    product_name: Optional[str] = None
    payment_method: Optional[str] = None
    
    # Food Delivery filters
    restaurant_name: Optional[str] = None
    cuisine_type: Optional[str] = None
    city: Optional[str] = None
    delivery_status: Optional[str] = None
    
    # SaaS filters
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    status: Optional[str] = None
    currency: Optional[str] = None
    
    # Common filters
    customer_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Electronics",
                "region": "North",
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-12-31T23:59:59"
            }
        }

