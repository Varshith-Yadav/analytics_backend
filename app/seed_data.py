"""Script to seed the database with sample analytics data for all three domains"""
from app.database import SessionLocal, init_db
from app.models import SalesTransaction, FoodOrder, Subscription
from datetime import datetime, timedelta
import random
import uuid

# ============================================================================
# SALES / E-COMMERCE DATA
# ============================================================================

SALES_PRODUCTS = [
    ("Laptop Pro", "Electronics", "North", "credit_card"),
    ("Laptop Pro", "Electronics", "South", "debit_card"),
    ("Laptop Pro", "Electronics", "East", "paypal"),
    ("Laptop Pro", "Electronics", "West", "credit_card"),
    ("Smartphone X", "Electronics", "North", "credit_card"),
    ("Smartphone X", "Electronics", "South", "debit_card"),
    ("Smartphone X", "Electronics", "East", "paypal"),
    ("Wireless Mouse", "Electronics", "North", "credit_card"),
    ("Office Chair", "Furniture", "North", "credit_card"),
    ("Office Chair", "Furniture", "South", "debit_card"),
    ("Desk Lamp", "Furniture", "East", "paypal"),
    ("Coffee Maker", "Appliances", "North", "credit_card"),
    ("Coffee Maker", "Appliances", "South", "debit_card"),
    ("Running Shoes", "Sports", "North", "credit_card"),
    ("Yoga Mat", "Sports", "South", "paypal"),
]


# ============================================================================
# FOOD DELIVERY DATA
# ============================================================================

FOOD_RESTAURANTS = [
    ("Pizza Palace", "Italian", "Mumbai"),
    ("Pizza Palace", "Italian", "Delhi"),
    ("Burger King", "Fast Food", "Mumbai"),
    ("Burger King", "Fast Food", "Bangalore"),
    ("Spice Garden", "Indian", "Delhi"),
    ("Spice Garden", "Indian", "Mumbai"),
    ("Sushi House", "Japanese", "Bangalore"),
    ("Sushi House", "Japanese", "Delhi"),
    ("Taco Bell", "Mexican", "Mumbai"),
    ("Taco Bell", "Mexican", "Bangalore"),
    ("Curry Corner", "Indian", "Delhi"),
    ("Curry Corner", "Indian", "Mumbai"),
]

DELIVERY_STATUSES = ["pending", "preparing", "out_for_delivery", "delivered", "cancelled"]


# ============================================================================
# SAAS SUBSCRIPTION DATA
# ============================================================================

SAAS_PLANS = [
    ("Basic", "monthly", 9.99),
    ("Basic", "annual", 99.99),
    ("Pro", "monthly", 29.99),
    ("Pro", "annual", 299.99),
    ("Enterprise", "monthly", 99.99),
    ("Enterprise", "annual", 999.99),
]

SUBSCRIPTION_STATUSES = ["active", "cancelled", "past_due", "trialing"]


# ============================================================================
# SEEDING FUNCTIONS
# ============================================================================

def seed_sales_transactions(db, num_transactions: int = 500):
    """Seed sales transactions"""
    base_date = datetime.now() - timedelta(days=365)
    transactions = []

    for i in range(num_transactions):
        product_name, category, region, payment_method = random.choice(SALES_PRODUCTS)
        sale_date = base_date + timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Vary amounts based on product
        if "Laptop" in product_name:
            amount = random.uniform(800, 1500)
            quantity = random.randint(1, 3)
        elif "Smartphone" in product_name:
            amount = random.uniform(400, 800)
            quantity = random.randint(1, 5)
        elif "Chair" in product_name:
            amount = random.uniform(150, 400)
            quantity = random.randint(1, 2)
        else:
            amount = random.uniform(20, 200)
            quantity = random.randint(1, 10)

        transaction = SalesTransaction(
            product_name=product_name,
            category=category,
            amount=round(amount, 2),
            quantity=quantity,
            region=region,
            customer_id=f"CUST_{random.randint(1000, 9999)}",
            payment_method=payment_method,
            sale_date=sale_date
        )
        transactions.append(transaction)

    db.bulk_save_objects(transactions)
    db.commit()
    print(f"✓ Seeded {num_transactions} sales transactions")


def seed_food_orders(db, num_orders: int = 500):
    """Seed food delivery orders"""
    base_date = datetime.now() - timedelta(days=180)
    orders = []

    for i in range(num_orders):
        restaurant_name, cuisine_type, city = random.choice(FOOD_RESTAURANTS)
        order_date = base_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Generate order amounts
        order_amount = round(random.uniform(200, 1500), 2)
        delivery_fee = round(random.uniform(20, 50), 2)
        tip_amount = round(random.uniform(0, order_amount * 0.15), 2)
        total_amount = order_amount + delivery_fee + tip_amount
        delivery_status = random.choice(DELIVERY_STATUSES)
        delivery_time_minutes = random.randint(15, 60) if delivery_status == "delivered" else None

        order = FoodOrder(
            order_id=f"ORD_{uuid.uuid4().hex[:8].upper()}",
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            order_amount=order_amount,
            delivery_fee=delivery_fee,
            tip_amount=tip_amount,
            total_amount=total_amount,
            customer_id=f"CUST_{random.randint(1000, 9999)}",
            city=city,
            delivery_status=delivery_status,
            order_date=order_date,
            delivery_time_minutes=delivery_time_minutes
        )
        orders.append(order)

    db.bulk_save_objects(orders)
    db.commit()
    print(f"✓ Seeded {num_orders} food delivery orders")


def seed_subscriptions(db, num_subscriptions: int = 300):
    """Seed SaaS subscriptions"""
    base_date = datetime.now() - timedelta(days=730)  # 2 years
    subscriptions = []

    for i in range(num_subscriptions):
        plan_name, plan_type, amount = random.choice(SAAS_PLANS)
        created_at = base_date + timedelta(days=random.randint(0, 730))
        
        # Calculate billing cycle dates
        if plan_type == "monthly":
            cycle_days = 30
        else:  # annual
            cycle_days = 365

        billing_cycle_start = created_at
        billing_cycle_end = billing_cycle_start + timedelta(days=cycle_days)
        
        # Adjust if end date is in future
        if billing_cycle_end > datetime.now():
            billing_cycle_end = datetime.now()

        status = random.choice(SUBSCRIPTION_STATUSES)
        cancelled_at = None
        if status == "cancelled":
            cancelled_at = billing_cycle_start + timedelta(days=random.randint(1, cycle_days - 1))

        # Calculate MRR (Monthly Recurring Revenue)
        if plan_type == "monthly":
            mrr = amount
        else:  # annual
            mrr = amount / 12

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
            cancelled_at=cancelled_at,
            mrr=round(mrr, 2)
        )
        subscriptions.append(subscription)

    db.bulk_save_objects(subscriptions)
    db.commit()
    print(f"✓ Seeded {num_subscriptions} SaaS subscriptions")


def seed_all(num_sales: int = 500, num_orders: int = 500, num_subscriptions: int = 300):
    """Seed all analytics types"""
    init_db()
    db = SessionLocal()

    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(SalesTransaction).delete()
        db.query(FoodOrder).delete()
        db.query(Subscription).delete()
        db.commit()

        print("\nSeeding data...")
        seed_sales_transactions(db, num_sales)
        seed_food_orders(db, num_orders)
        seed_subscriptions(db, num_subscriptions)

        print(f"\n✓ Successfully seeded all analytics data!")
        print(f"  - Sales Transactions: {num_sales}")
        print(f"  - Food Orders: {num_orders}")
        print(f"  - Subscriptions: {num_subscriptions}")

    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all(500, 500, 300)
