from pydantic import BaseModel
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class OrderCreate(BaseModel):
    product_id: int
    price: float
    fee: float
    total: float
    quantity: int
    status: OrderStatus

class OrderOut(OrderCreate):
    id: int

    class Config:
        from_attributes = True