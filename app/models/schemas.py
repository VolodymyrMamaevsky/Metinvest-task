from pydantic import BaseModel
from datetime import datetime


# Schema for creating a new order
class OrderCreate(BaseModel):
    supplier_id: int
    customer_id: int
    quantity: int
    price: float
    order_date: datetime


# Schema for the response containing order data
class OrderResponse(BaseModel):
    orderid: int
    supplier_id: int
    customer_id: int
    quantity: int
    price: float
    order_date: datetime

    class Config:
        from_attributes = True
