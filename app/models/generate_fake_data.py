from app.models.database import SessionLocal, Order
from faker import Faker
import random

fake = Faker()


def generate_fake_orders(num_orders: int):
    db = SessionLocal()

    current_count = db.query(Order).count()
    if current_count >= num_orders:
        print(f"Database already contains {current_count} orders. Skipping generation.")
        db.close()
        return

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
