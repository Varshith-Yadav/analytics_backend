"""SaaS subscription analytics models"""
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.models.base import Base
from sqlalchemy.sql import func


class Subscription(Base):
    """Model for SaaS subscription analytics"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(String, unique=True, index=True)
    customer_id = Column(String, index=True)
    plan_name = Column(String, index=True)  # Basic, Pro, Enterprise
    plan_type = Column(String, index=True)  # monthly, annual
    amount = Column(Float)  # Monthly/Annual subscription amount
    status = Column(String, index=True)  # active, cancelled, past_due, trialing
    currency = Column(String, default="USD")
    billing_cycle_start = Column(DateTime, index=True)
    billing_cycle_end = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now())
    cancelled_at = Column(DateTime, nullable=True)
    mrr = Column(Float)  # Monthly Recurring Revenue (calculated)

