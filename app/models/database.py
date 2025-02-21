from sqlalchemy import create_engine, Integer, Float, DateTime, Index
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")

Base = DeclarativeBase()


class Order(Base):
    __tablename__ = "orders"

    orderid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supplier_id: Mapped[int] = mapped_column(Integer)
    customer_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Indexes for performance optimization
    __table_args__ = (
        Index("ix_order_supplier", "supplier_id"),
        Index("ix_order_customer", "customer_id"),
        Index("ix_order_date", "order_date"),
    )


# Create a connection and session with the database
def get_engine():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
    return engine


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine)
