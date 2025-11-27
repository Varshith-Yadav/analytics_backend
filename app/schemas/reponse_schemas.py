from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


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
    chart_type: str
    data: List[ChartDataPoint]
    metadata: Dict[str, Any] = {}


class FilterParams(BaseModel):
    """Common filter parameters"""
    category: Optional[str] = None
    region: Optional[str] = None
    product_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_type: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Electronics",
                "region": "North",
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-12-31T23:59:59"
            }
        }

