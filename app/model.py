from sqlalchemy import Column, Integer, Float, String, DateTime, Date, Boolean
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


# ============================================================================
# E-COMMERCE / SALES ANALYTICS
# ============================================================================

class SalesTransaction(Base):
    """Model for e-commerce sales transactions"""
    __tablename__ = "sales_transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    category = Column(String, index=True)
    amount = Column(Float)
    quantity = Column(Integer)
    region = Column(String, index=True)
    customer_id = Column(String, index=True)
    payment_method = Column(String, index=True)
    sale_date = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now())


# ============================================================================
# FOOD DELIVERY ANALYTICS (Swiggy/Zomato style)
# ============================================================================

class FoodOrder(Base):
    """Model for food delivery orders"""
    __tablename__ = "food_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    restaurant_name = Column(String, index=True)
    cuisine_type = Column(String, index=True)
    order_amount = Column(Float)
    delivery_fee = Column(Float)
    tip_amount = Column(Float)
    total_amount = Column(Float)  # order_amount + delivery_fee + tip
    customer_id = Column(String, index=True)
    city = Column(String, index=True)
    delivery_status = Column(String, index=True)  # pending, preparing, out_for_delivery, delivered, cancelled
    order_date = Column(DateTime, index=True)
    delivery_time_minutes = Column(Integer)  # Time taken for delivery
    created_at = Column(DateTime, server_default=func.now())


# ============================================================================
# SAAS SUBSCRIPTION ANALYTICS (Stripe style)
# ============================================================================

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

