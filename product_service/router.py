from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import ProductCreate, ProductOut
from crud import get_all_producst, create_product, get_product, delete_product, update_product, decrease_quantity
from database import get_db
from models import Product
from common.auth import get_current_user

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.get("/", response_model=list[ProductOut])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user=Depends(get_current_user())):
    return get_all_producst(db, skip, limit)


@product_router.post("/", response_model=ProductOut)
def create(product: ProductCreate, db: Session = Depends(get_db), user=Depends(get_current_user(required_role="creator"))):
    return create_product(db, product)

@product_router.get("/{id}", response_model=ProductOut)
def get(id: int, db: Session = Depends(get_db), user=Depends(get_current_user())):
    product = get_product(db, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")

    return product
    

@product_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), user=Depends(get_current_user("creator"))):
    product = delete_product(db, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    

@product_router.put("/{id}", response_model=ProductOut)
def update(id: int, product: ProductCreate, db: Session = Depends(get_db), user=Depends(get_current_user("creator"))):
    product = update_product(db, id, product)
    if not update_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )
    return product

@product_router.post("/{id}/decrease")
def decrease(id: int, payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user())):
    quantity = payload['quantity']
    product = decrease_quantity(db, id, quantity)
    if not product:
        raise HTTPException(status_code=400, detail="Insufficient stock or product not found")
    return {"message": "Quantity updated"}