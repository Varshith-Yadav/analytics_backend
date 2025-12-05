"""Pytest configuration and fixtures"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app
from app.models import SalesTransaction, FoodOrder, Subscription
from datetime import datetime, timedelta
import random
import uuid


# Test database URL
TEST_DATABASE_URL = "sqlite:///./test_analytics.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_sales_data(db_session):
    """Create sample sales data for testing"""
    transactions = []
    base_date = datetime.now() - timedelta(days=30)

    # Create diverse test data
    test_data = [
        ("Laptop Pro", "Electronics", "North", 1000.0, 2, base_date + timedelta(days=1), "credit_card"),
        ("Laptop Pro", "Electronics", "South", 1200.0, 1, base_date + timedelta(days=2), "debit_card"),
        ("Smartphone X", "Electronics", "North", 600.0, 3, base_date + timedelta(days=3), "credit_card"),
        ("Office Chair", "Furniture", "East", 250.0, 1, base_date + timedelta(days=4), "paypal"),
        ("Coffee Maker", "Appliances", "West", 150.0, 2, base_date + timedelta(days=5), "credit_card"),
        ("Running Shoes", "Sports", "North", 80.0, 4, base_date + timedelta(days=6), "debit_card"),
    ]

    for product_name, category, region, amount, quantity, sale_date, payment_method in test_data:
        transaction = SalesTransaction(
            product_name=product_name,
            category=category,
            amount=amount,
            quantity=quantity,
            region=region,
            customer_id=f"CUST_{random.randint(1000, 9999)}",
            payment_method=payment_method,
            sale_date=sale_date
        )
        transactions.append(transaction)

    db_session.add_all(transactions)
    db_session.commit()
    return transactions


@pytest.fixture
def sample_food_orders(db_session):
    """Create sample food delivery data for testing"""
    orders = []
    base_date = datetime.now() - timedelta(days=30)

    test_data = [
        ("Pizza Palace", "Italian", "Mumbai", 500.0, 30.0, 50.0, "delivered", base_date + timedelta(days=1)),
        ("Burger King", "Fast Food", "Delhi", 300.0, 25.0, 0.0, "delivered", base_date + timedelta(days=2)),
        ("Spice Garden", "Indian", "Mumbai", 800.0, 40.0, 100.0, "delivered", base_date + timedelta(days=3)),
        ("Sushi House", "Japanese", "Bangalore", 1200.0, 50.0, 150.0, "out_for_delivery", base_date + timedelta(days=4)),
        ("Taco Bell", "Mexican", "Delhi", 400.0, 30.0, 0.0, "preparing", base_date + timedelta(days=5)),
    ]

    for restaurant_name, cuisine_type, city, order_amount, delivery_fee, tip_amount, status, order_date in test_data:
        order = FoodOrder(
            order_id=f"ORD_{uuid.uuid4().hex[:8].upper()}",
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            order_amount=order_amount,
            delivery_fee=delivery_fee,
            tip_amount=tip_amount,
            total_amount=order_amount + delivery_fee + tip_amount,
            customer_id=f"CUST_{random.randint(1000, 9999)}",
            city=city,
            delivery_status=status,
            order_date=order_date,
            delivery_time_minutes=random.randint(20, 45) if status == "delivered" else None
        )
        orders.append(order)

    db_session.add_all(orders)
    db_session.commit()
    return orders


@pytest.fixture
def sample_subscriptions(db_session):
    """Create sample SaaS subscription data for testing"""
    subscriptions = []
    base_date = datetime.now() - timedelta(days=180)

    test_data = [
        ("Basic", "monthly", 9.99, "active", base_date + timedelta(days=1)),
        ("Pro", "monthly", 29.99, "active", base_date + timedelta(days=2)),
        ("Enterprise", "annual", 999.99, "active", base_date + timedelta(days=3)),
        ("Basic", "annual", 99.99, "cancelled", base_date + timedelta(days=4)),
        ("Pro", "monthly", 29.99, "trialing", base_date + timedelta(days=5)),
    ]

    for plan_name, plan_type, amount, status, created_at in test_data:
        cycle_days = 30 if plan_type == "monthly" else 365
        billing_cycle_start = created_at
        billing_cycle_end = billing_cycle_start + timedelta(days=cycle_days)
        mrr = amount if plan_type == "monthly" else amount / 12

        subscription = Subscription(
            subscription_id=f"SUB_{uuid.uuid4().hex[:8].upper()}",
            customer_id=f"CUST_{random.randint(1000, 9999)}",
            plan_name=plan_name,
            plan_type=plan_type,
            amount=amount,
            status=status,
            currency="USD",
            billing_cycle_start=billing_cycle_start,
            billing_cycle_end=billing_cycle_end,
            cancelled_at=billing_cycle_start + timedelta(days=10) if status == "cancelled" else None,
            mrr=round(mrr, 2)
        )
        subscriptions.append(subscription)

    db_session.add_all(subscriptions)
    db_session.commit()
    return subscriptions

