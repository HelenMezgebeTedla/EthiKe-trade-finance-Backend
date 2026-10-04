from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product as product_service
from database import get_db
from dependencies import assert_can_access_trader, get_current_user, get_owned_trader_id

router = APIRouter(
    prefix="/products", tags=["Product"], dependencies=[Depends(get_current_user)]
)


@router.get("/trader/{trader_id}", response_model=list[ProductRead])
def list_trader_products(
    trader_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assert_can_access_trader(trader_id, current_user)
    return product_service.list_trader_products(db, trader_id)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, product_id)
    assert_can_access_trader(product.trader_id, current_user)
    return product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return product_service.create_product(db, data, owned_trader_id)


@router.put("/{product_id}", response_model=ProductRead)
def replace_product(
    product_id: UUID,
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, product_id)
    assert_can_access_trader(product.trader_id, current_user)
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return product_service.replace_product(db, product_id, data, owned_trader_id)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: UUID,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, product_id)
    assert_can_access_trader(product.trader_id, current_user)
    return product_service.update_product(db, product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, product_id)
    assert_can_access_trader(product.trader_id, current_user)
    product_service.delete_product(db, product_id)
