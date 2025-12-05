"""Sales/E-commerce analytics models"""
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


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

