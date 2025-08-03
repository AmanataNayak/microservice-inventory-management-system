from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
from schemas import OrderStatus
from database import Base

class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    fee = Column(Float)
    total = Column(Float)
    quantity = Column(Integer)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)