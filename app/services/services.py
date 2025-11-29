from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.models import SalesTransaction, MetricEvent
from app.schemas import AggregationType, FilterParams
from typing import Optional, List, Dict, Any
from datetime import datetime


class AnalyticsService:
    """Service layer for analytics operations"""

    @staticmethod
    def apply_filters(query, model, filters: FilterParams):
        """Apply filters to a query"""
        if filters.category:
            query = query.filter(model.category == filters.category)
        if filters.region:
            query = query.filter(model.region == filters.region)
        if filters.product_name:
            query = query.filter(model.product_name == filters.product_name)
        if filters.start_date:
            if hasattr(model, 'sale_date'):
                query = query.filter(model.sale_date >= filters.start_date)
            elif hasattr(model, 'event_date'):
                query = query.filter(model.event_date >= filters.start_date)
        if filters.end_date:
            if hasattr(model, 'sale_date'):
                query = query.filter(model.sale_date <= filters.end_date)
            elif hasattr(model, 'event_date'):
                query = query.filter(model.event_date <= filters.end_date)
        if filters.event_type and hasattr(model, 'event_type'):
            query = query.filter(model.event_type == filters.event_type)
        if filters.user_id and hasattr(model, 'user_id'):
            query = query.filter(model.user_id == filters.user_id)
        return query

    @staticmethod
    def aggregate_sales(
        db: Session,
        aggregation_type: AggregationType,
        field: str,
        filters: Optional[FilterParams] = None,
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """Perform aggregations on sales data"""
        query = db.query(SalesTransaction)

        # Apply filters
        if filters:
            query = AnalyticsService.apply_filters(query, SalesTransaction, filters)

        # Validate field
        valid_fields = ['amount', 'quantity']
        if field not in valid_fields:
            raise ValueError(f"Invalid field. Must be one of: {valid_fields}")

        # Get the field to aggregate
        field_attr = getattr(SalesTransaction, field)

        # Perform aggregation
        if aggregation_type == AggregationType.SUM:
            if group_by:
                group_attr = getattr(SalesTransaction, group_by, None)
                if group_attr is None:
                    raise ValueError(f"Invalid group_by field: {group_by}")
                result = query.with_entities(
                    group_attr,
                    func.sum(field_attr).label('total')
                ).group_by(group_attr).all()
                groups = [{"group": str(row[0]), "value": float(row[1])} for row in result]
                return {
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "group_by": group_by,
                    "groups": groups,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }
            else:
                result = query.with_entities(func.sum(field_attr)).scalar()
                return {
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "value": float(result) if result else 0.0,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }

        elif aggregation_type == AggregationType.AVG:
            if group_by:
                group_attr = getattr(SalesTransaction, group_by, None)
                if group_attr is None:
                    raise ValueError(f"Invalid group_by field: {group_by}")
                result = query.with_entities(
                    group_attr,
                    func.avg(field_attr).label('average')
                ).group_by(group_attr).all()
                groups = [{"group": str(row[0]), "value": float(row[1]) if row[1] else 0.0} for row in result]
                return {
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "group_by": group_by,
                    "groups": groups,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }
            else:
                result = query.with_entities(func.avg(field_attr)).scalar()
                return {
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "value": float(result) if result else 0.0,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }

        elif aggregation_type == AggregationType.COUNT:
            if group_by:
                group_attr = getattr(SalesTransaction, group_by, None)
                if group_attr is None:
                    raise ValueError(f"Invalid group_by field: {group_by}")
                result = query.with_entities(
                    group_attr,
                    func.count().label('count')
                ).group_by(group_attr).all()
                groups = [{"group": str(row[0]), "value": float(row[1])} for row in result]
                return {
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "group_by": group_by,
                    "groups": groups,
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }
            else:
                result = query.count()
                return {
                    "aggregation_type": aggregation_type.value,
                    "field": field,
                    "value": float(result),
                    "filters_applied": filters.model_dump(exclude_none=True) if filters else {}
                }

        elif aggregation_type == AggregationType.MIN:
            result = query.with_entities(func.min(field_attr)).scalar()
            return {
                "aggregation_type": aggregation_type.value,
                "field": field,
                "value": float(result) if result else 0.0,
                "filters_applied": filters.dict(exclude_none=True) if filters else {}
            }

        elif aggregation_type == AggregationType.MAX:
            result = query.with_entities(func.max(field_attr)).scalar()
            return {
                "aggregation_type": aggregation_type.value,
                "field": field,
                "value": float(result) if result else 0.0,
                "filters_applied": filters.dict(exclude_none=True) if filters else {}
            }

    @staticmethod
    def get_chart_data(
        db: Session,
        chart_type: str,
        field: str,
        group_by: str,
        filters: Optional[FilterParams] = None
    ) -> Dict[str, Any]:
        """Get chart-ready JSON data"""
        query = db.query(SalesTransaction)

        if filters:
            query = AnalyticsService.apply_filters(query, SalesTransaction, filters)

        group_attr = getattr(SalesTransaction, group_by, None)
        if group_attr is None:
            raise ValueError(f"Invalid group_by field: {group_by}")

        field_attr = getattr(SalesTransaction, field)
        valid_fields = ['amount', 'quantity']
        if field not in valid_fields:
            raise ValueError(f"Invalid field. Must be one of: {valid_fields}")

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
            "chart_type": chart_type,
            "data": data_points,
            "metadata": {
                "field": field,
                "group_by": group_by,
                "filters_applied": filters.model_dump(exclude_none=True) if filters else {},
                "total_points": len(data_points)
            }
        }

