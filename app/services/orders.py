from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import Order
from datetime import datetime


def get_total_spent(db: Session, start_date: datetime, end_date: datetime):
    return (
        db.query(func.sum(Order.quantity * Order.price))
        .filter(Order.order_date.between(start_date, end_date))
        .scalar()
    )


def get_top_products(db: Session, start_date: datetime, end_date: datetime):
    return (
        db.query(Order.supplier_id, func.sum(Order.quantity).label("total_quantity"))
        .filter(Order.order_date.between(start_date, end_date))
        .group_by(Order.supplier_id)
        .order_by(func.sum(Order.quantity).desc())
        .limit(10)
        .all()
    )


def get_top_suppliers(db: Session, start_date: datetime, end_date: datetime):
    return (
        db.query(Order.supplier_id, func.count(Order.orderid).label("order_count"))
        .filter(Order.order_date.between(start_date, end_date))
        .group_by(Order.supplier_id)
        .order_by(func.count(Order.orderid).desc())
        .limit(5)
        .all()
    )
