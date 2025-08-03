from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate

def get_all_producst(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, id: int) -> Product | None:
    return db.query(Product).get(id)

def delete_product(db: Session, id: int) -> bool:
    db_product = db.query(Product).get(id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

def update_product(db: Session, id: int, product: ProductCreate) -> Product | None:
    product_data = db.query(Product).get(id)
    if product_data:
        for key, value in product.model_dump().items():
            setattr(product_data, key, value)
        db.commit()
        db.refresh(product_data)
        return product_data
    return None

def decrease_quantity(db: Session, product_id: int, quantity: int) -> Product | None:
    product = db.query(Product).get(product_id)
    if product and product.quantity >= quantity:
        product.quantity -= quantity
        db.commit()
        db.refresh(product)
    else:
        None
