from uuid import UUID

from database import get_db
from dependencies import assert_can_access_trader, get_current_user, get_owned_trader_id
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.purchase import PurchaseCreate, PurchaseRead, PurchaseUpdate
from app.services import purchase as purchase_service

router = APIRouter(
    prefix="/purchases", tags=["Purchase"], dependencies=[Depends(get_current_user)]
)


@router.get("/product/{product_id}", response_model=list[PurchaseRead])
def get_purchase_history(product_id: UUID, db: Session = Depends(get_db)):
    return purchase_service.get_purchase_history(db, product_id)


@router.get("/{purchase_id}", response_model=PurchaseRead)
def get_purchase(
    purchase_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    purchase = purchase_service.get_purchase(db, purchase_id)
    assert_can_access_trader(purchase.trader_id, current_user)
    return purchase


@router.post("/", response_model=PurchaseRead, status_code=status.HTTP_201_CREATED)
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return purchase_service.create_purchase(db, data, owned_trader_id)


@router.patch("/{purchase_id}", response_model=PurchaseRead)
def update_purchase(
    purchase_id: UUID,
    data: PurchaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    purchase = purchase_service.get_purchase(db, purchase_id)
    assert_can_access_trader(purchase.trader_id, current_user)
    return purchase_service.update_purchase(db, purchase_id, data)


@router.put("/{purchase_id}", response_model=PurchaseRead)
def replace_purchase(
    purchase_id: UUID,
    data: PurchaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """PUT reuses the same partial-update logic as PATCH here, since a Purchase's
    identity fields (product_id, trader_id) are immutable after stock has been
    adjusted against them — only quantity/cost/supplier are ever replaced."""
    purchase = purchase_service.get_purchase(db, purchase_id)
    assert_can_access_trader(purchase.trader_id, current_user)
    return purchase_service.update_purchase(db, purchase_id, data)


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(
    purchase_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    purchase = purchase_service.get_purchase(db, purchase_id)
    assert_can_access_trader(purchase.trader_id, current_user)
    purchase_service.delete_purchase(db, purchase_id)
