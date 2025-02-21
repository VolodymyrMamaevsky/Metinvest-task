from celery import Celery
from celery.schedules import crontab
import os
import logging
from app.models.database import SessionLocal, Order
from app.core.config import logger
import time

app = Celery("tasks", broker=os.getenv("REDIS_URL"))

logger = logging.getLogger(__name__)


@app.task
def process_pending_orders():
    start_time = time.time()  # Record the start time of the task execution
    logger.info("Checking the queue for new orders.")

    db = SessionLocal()
    try:
        new_order = Order(
            supplier_id=1,
            customer_id=1,
            quantity=100,
            price=500.0,
            order_date="2025-01-01",
        )
        db.add(new_order)
        db.commit()
        end_time = time.time()  # Record the end time of the task execution
        execution_time = end_time - start_time  # Calculate execution time
        logger.info(
            f"New order added to the database: {new_order}. Execution time: {execution_time:.4f} seconds."
        )
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        logger.error(
            f"Error adding order to the database: {e}. Execution time: {execution_time:.4f} seconds."
        )
        db.rollback()
    finally:
        db.close()


# Configure Celery Beat schedule to run the task every minute
app.conf.beat_schedule = {
    "add_order_every_minute": {
        "task": "app.tasks.celery.process_pending_orders",
        "schedule": crontab(minute="*"),
    },
}

# Set Celery timezone
app.conf.timezone = "UTC"
