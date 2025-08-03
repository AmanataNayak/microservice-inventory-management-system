from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import OrderCreate, OrderOut, OrderStatus
from crud import create_order, update_status, get_order
import requests
from common.auth import get_current_user
from common.configurations import config

payment_router = APIRouter(prefix="/orders", tags=["orders"])
url = config['app']['product.url']

@payment_router.post("/", response_model=OrderOut)
async def create(request: Request, background_task: BackgroundTasks, db: Session = Depends(get_db), user = Depends(get_current_user)):
    body = await request.json()

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token missing")

    headers = {
        "Authorization": token  
    }

    # Fetch product details
    try:
        response = requests.get(f"{url}/products/{body['id']}", headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product service error: {e}")

    product = response.json()

    # Create order
    order = OrderCreate(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status=OrderStatus.PENDING
    )

    new_order = create_order(db, order)
    background_task.add_task(update_status, db, new_order.id, headers, url)
    return new_order


@payment_router.get("/{id}", response_model=OrderOut)
def get(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    order = get_order(db, id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    return order