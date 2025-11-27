from sqlalchemy import Column, Integer, Float, String, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class SalesTransaction(Base):
    """Model for sales transactions - represents business metrics"""
    __tablename__ = "sales_transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    category = Column(String, index=True)
    amount = Column(Float)
    quantity = Column(Integer)
    region = Column(String, index=True)
    sale_date = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now())


class MetricEvent(Base):
    """Model for metric events - represents various business events"""
    __tablename__ = "metric_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    user_id = Column(String, index=True)
    value = Column(Float)
    event_metadata = Column(String)  # JSON string for additional data
    event_date = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now())

