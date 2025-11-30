"""Script to seed the database with sample analytics data"""
from app.database import SessionLocal, init_db
from app.models import SalesTransaction
from datetime import datetime, timedelta
import random

# Sample data
PRODUCTS = [
    ("Laptop Pro", "Electronics", "North"),
    ("Laptop Pro", "Electronics", "South"),
    ("Laptop Pro", "Electronics", "East"),
    ("Laptop Pro", "Electronics", "West"),
    ("Smartphone X", "Electronics", "North"),
    ("Smartphone X", "Electronics", "South"),
    ("Smartphone X", "Electronics", "East"),
    ("Smartphone X", "Electronics", "West"),
    ("Wireless Mouse", "Electronics", "North"),
    ("Wireless Mouse", "Electronics", "South"),
    ("Office Chair", "Furniture", "North"),
    ("Office Chair", "Furniture", "South"),
    ("Office Chair", "Furniture", "East"),
    ("Desk Lamp", "Furniture", "North"),
    ("Desk Lamp", "Furniture", "West"),
    ("Coffee Maker", "Appliances", "North"),
    ("Coffee Maker", "Appliances", "South"),
    ("Coffee Maker", "Appliances", "East"),
    ("Coffee Maker", "Appliances", "West"),
    ("Blender", "Appliances", "North"),
    ("Blender", "Appliances", "South"),
    ("Running Shoes", "Sports", "North"),
    ("Running Shoes", "Sports", "South"),
    ("Running Shoes", "Sports", "East"),
    ("Yoga Mat", "Sports", "West"),
]


def seed_database(num_transactions: int = 1000):
    """Seed database with sample sales transactions"""
    init_db()
    db = SessionLocal()

    try:
        # Clear existing data
        db.query(SalesTransaction).delete()
        db.commit()

        # Generate transactions
        base_date = datetime.now() - timedelta(days=365)
        transactions = []

        for i in range(num_transactions):
            product_name, category, region = random.choice(PRODUCTS)
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
                sale_date=sale_date
            )
            transactions.append(transaction)

        db.bulk_save_objects(transactions)
        db.commit()
        print(f"✓ Seeded {num_transactions} transactions successfully!")

    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database(1000)

