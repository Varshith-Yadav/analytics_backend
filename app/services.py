from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import SalesTransaction, FoodOrder, Subscription
from app.schemas import AggregationType, FilterParams, AnalyticsType
from typing import Optional, List, Dict, Any
from datetime import datetime


class AnalyticsService:
    """Service layer for analytics operations - supports multiple analytics domains"""

    # Field mappings for each analytics type
    ANALYTICS_CONFIG = {
        AnalyticsType.SALES: {
            "model": SalesTransaction,
            "date_field": "sale_date",
            "aggregatable_fields": ["amount", "quantity"],
            "groupable_fields": ["category", "region", "product_name", "payment_method"],
            "filter_fields": {
                "category": "category",
                "region": "region",
                "product_name": "product_name",
                "payment_method": "payment_method",
                "customer_id": "customer_id"
            }
        },
        AnalyticsType.FOOD_DELIVERY: {
            "model": FoodOrder,
            "date_field": "order_date",
            "aggregatable_fields": ["order_amount", "delivery_fee", "tip_amount", "total_amount", "delivery_time_minutes"],
            "groupable_fields": ["restaurant_name", "cuisine_type", "city", "delivery_status"],
            "filter_fields": {
                "restaurant_name": "restaurant_name",
                "cuisine_type": "cuisine_type",
                "city": "city",
                "delivery_status": "delivery_status",
                "customer_id": "customer_id"
            }
        },
        AnalyticsType.SAAS: {
            "model": Subscription,
            "date_field": "billing_cycle_start",
            "aggregatable_fields": ["amount", "mrr"],
            "groupable_fields": ["plan_name", "plan_type", "status", "currency"],
            "filter_fields": {
                "plan_name": "plan_name",
                "plan_type": "plan_type",
                "status": "status",
                "currency": "currency",
                "customer_id": "customer_id"
            }
        }
    }

    @staticmethod
    def get_config(analytics_type: AnalyticsType) -> Dict[str, Any]:
        """Get configuration for analytics type"""
        if analytics_type not in AnalyticsService.ANALYTICS_CONFIG:
            raise ValueError(f"Unsupported analytics type: {analytics_type}")
        return AnalyticsService.ANALYTICS_CONFIG[analytics_type]

    @staticmethod
    def apply_filters(query, model, filters: FilterParams, config: Dict[str, Any]):
        """Apply filters to a query based on analytics type"""
        filter_fields = config["filter_fields"]
        date_field = config["date_field"]

        # Apply domain-specific filters
        for filter_param, model_field in filter_fields.items():
            filter_value = getattr(filters, filter_param, None)
            if filter_value:
                model_attr = getattr(model, model_field, None)
                if model_attr is not None:
                    query = query.filter(model_attr == filter_value)

        # Apply date range filters
        if filters.start_date:
            date_attr = getattr(model, date_field, None)
            if date_attr is not None:
                query = query.filter(date_attr >= filters.start_date)

        if filters.end_date:
            date_attr = getattr(model, date_field, None)
            if date_attr is not None:
                query = query.filter(date_attr <= filters.end_date)

        return query

    @staticmethod
    def aggregate(
        db: Session,
        analytics_type: AnalyticsType,
        aggregation_type: AggregationType,
        field: str,
        filters: Optional[FilterParams] = None,
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """Perform aggregations on any analytics type"""
        config = AnalyticsService.get_config(analytics_type)
        model = config["model"]
        query = db.query(model)

        # Apply filters
        if filters:
            query = AnalyticsService.apply_filters(query, model, filters, config)

        # Validate field
        valid_fields = config["aggregatable_fields"]
        if field not in valid_fields:
            raise ValueError(f"Invalid field for {analytics_type.value}. Must be one of: {valid_fields}")

        # Get the field to aggregate
        field_attr = getattr(model, field)

        # Validate group_by if provided
        if group_by:
            valid_group_fields = config["groupable_fields"]
            if group_by not in valid_group_fields:
                raise ValueError(f"Invalid group_by field for {analytics_type.value}. Must be one of: {valid_group_fields}")

        # Perform aggregation
        if aggregation_type == AggregationType.SUM:
            if group_by:
                group_attr = getattr(model, group_by)
                result = query.with_entities(
                    group_attr,
                    func.sum(field_attr).label('total')
                ).group_by(group_attr).all()
                groups = [{"group": str(row[0]), "value": float(row[1]) if row[1] else 0.0} for row in result]
                return {
                    "analytics_type": analytics_type.value,
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "group_by": group_by,
                    "groups": groups,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }
            else:
                result = query.with_entities(func.sum(field_attr)).scalar()
                return {
                    "analytics_type": analytics_type.value,
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "value": float(result) if result else 0.0,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }

        elif aggregation_type == AggregationType.AVG:
            if group_by:
                group_attr = getattr(model, group_by)
                result = query.with_entities(
                    group_attr,
                    func.avg(field_attr).label('average')
                ).group_by(group_attr).all()
                groups = [{"group": str(row[0]), "value": float(row[1]) if row[1] else 0.0} for row in result]
                return {
                    "analytics_type": analytics_type.value,
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "group_by": group_by,
                    "groups": groups,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }
            else:
                result = query.with_entities(func.avg(field_attr)).scalar()
                return {
                    "analytics_type": analytics_type.value,
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "value": float(result) if result else 0.0,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }

        elif aggregation_type == AggregationType.COUNT:
            if group_by:
                group_attr = getattr(model, group_by)
                result = query.with_entities(
                    group_attr,
                    func.count().label('count')
                ).group_by(group_attr).all()
                groups = [{"group": str(row[0]), "value": float(row[1])} for row in result]
                return {
                    "analytics_type": analytics_type.value,
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "group_by": group_by,
                    "groups": groups,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }
            else:
                result = query.count()
                return {
                    "analytics_type": analytics_type.value,
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "value": float(result),
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }

        elif aggregation_type == AggregationType.MIN:
            result = query.with_entities(func.min(field_attr)).scalar()
            return {
                "analytics_type": analytics_type.value,
                "aggregation_type": aggregation_type.value,
                "field": field,
                "value": float(result) if result else 0.0,
                "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
            }

        elif aggregation_type == AggregationType.MAX:
            result = query.with_entities(func.max(field_attr)).scalar()
            return {
                "analytics_type": analytics_type.value,
                "aggregation_type": aggregation_type.value,
                "field": field,
                "value": float(result) if result else 0.0,
                "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
            }

    @staticmethod
    def get_chart_data(
        db: Session,
        analytics_type: AnalyticsType,
        chart_type: str,
        field: str,
        group_by: str,
        filters: Optional[FilterParams] = None
    ) -> Dict[str, Any]:
        """Get chart-ready JSON data for any analytics type"""
        config = AnalyticsService.get_config(analytics_type)
        model = config["model"]
        query = db.query(model)

        if filters:
            query = AnalyticsService.apply_filters(query, model, filters, config)

        # Validate field
        valid_fields = config["aggregatable_fields"]
        if field not in valid_fields:
            raise ValueError(f"Invalid field for {analytics_type.value}. Must be one of: {valid_fields}")

        # Validate group_by
        valid_group_fields = config["groupable_fields"]
        if group_by not in valid_group_fields:
            raise ValueError(f"Invalid group_by field for {analytics_type.value}. Must be one of: {valid_group_fields}")

        group_attr = getattr(model, group_by)
        field_attr = getattr(model, field)

        result = query.with_entities(
            group_attr,
            func.sum(field_attr).label('total')
        ).group_by(group_attr).all()

        data_points = [
            {
                "label": str(row[0]),
                "value": float(row[1]) if row[1] else 0.0,
                "metadata": {}
            }
            for row in result
        ]

        return {
            "analytics_type": analytics_type.value,
            "chart_type": chart_type,
            "data": data_points,
            "metadata": {
                "field": field,
                "group_by": group_by,
                "filters_applied": filters.model_dump(exclude_none=True) if filters else {},
                "total_points": len(data_points)
            }
        }
