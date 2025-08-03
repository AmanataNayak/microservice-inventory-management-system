from sqlalchemy.orm import Session
from models import Order
from schemas import OrderOut, OrderCreate, OrderStatus
import time, requests

def create_order(db: Session, order: OrderCreate) -> Order:
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_status(db: Session, order_id: int, headers: dict, url: str) -> Order:
    time.sleep(15)
    order = db.query(Order).get(order_id)
    if order and order.status != OrderStatus.COMPLETED:
        try: 
            requests.post(f"{url}/products/{order.product_id}/decrease",
                            json={"quantity": order.quantity}, headers=headers
                        )
            order.status = OrderStatus.COMPLETED
            db.commit()
            db.refresh(order)
        except requests.exceptions.RequestException as re:
            print(f"failed to update product quantity")


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).get(order_id)
