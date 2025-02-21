from app.models.database import SessionLocal, Order
from faker import Faker
import random

fake = Faker()


def generate_fake_orders(num_orders: int):
    db = SessionLocal()
    orders = []
    for _ in range(num_orders):
        order = Order(
            supplier_id=random.randint(1, 100),
            customer_id=random.randint(1, 100),
            quantity=random.randint(1, 100),
            price=random.uniform(1, 1000),
            order_date=fake.date_this_year(),
        )
        orders.append(order)

    db.bulk_save_objects(orders)
    db.commit()
    db.close()


generate_fake_orders(10000)  # Generation of 10,000 orders
