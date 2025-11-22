# app/db/seed_data.py
from faker import Faker
import random
from .database import SessionLocal, engine, Base
from .models import Customer, Product, Order, OrderItem

fake = Faker()

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Seed Customers
    customers = [
        Customer(name=fake.name(), email=fake.email(), country=fake.country())
        for _ in range(100)
    ]
    db.add_all(customers)
    db.commit()

    # Seed Products
    products = [
        Product(name=fake.word(), category=random.choice(["Electronics", "Fashion", "Books"]), price=random.uniform(10, 500))
        for _ in range(50)
    ]
    db.add_all(products)
    db.commit()

    customers = db.query(Customer).all()
    products = db.query(Product).all()

    # Seed Orders and Order Items
    for _ in range(500):  # 500 sample orders
        customer = random.choice(customers)
        status = random.choice(["PAID", "CANCELLED", "REFUNDED"])
        order = Order(customer_id=customer.id, status=status, total_amount=0.0)
        db.add(order)
        db.commit()

        total = 0
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price)
            db.add(item)
            total += product.price * quantity

        order.total_amount = total
        db.commit()

    print("Seed complete")


if __name__ == "__main__":
    seed()
