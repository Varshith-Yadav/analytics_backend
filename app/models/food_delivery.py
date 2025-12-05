"""Food delivery analytics models"""
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


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

