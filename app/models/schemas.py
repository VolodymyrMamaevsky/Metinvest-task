from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Schema for creating a new order
class OrderCreate(BaseModel):
    supplier_id: int
    customer_id: int
    quantity: int
    price: float
    order_date: datetime


# Schema for retrieving an order response
class OrderResponse(BaseModel):
    orderid: int
    supplier_id: int
    customer_id: int
    quantity: int
    price: float
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for total spent response
class TotalSpentResponse(BaseModel):
    total_spent: float


# Schema for top products response
class TopProductResponse(BaseModel):
    product_id: int
    total_sold: int


# Schema for top suppliers response
class TopSupplierResponse(BaseModel):
    supplier_id: int
    total_orders: int
