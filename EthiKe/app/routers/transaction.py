from uuid import UUID

from database import get_db
from dependencies import assert_can_access_trader, get_current_user, get_owned_trader_id
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from app.services import transaction as transaction_service

router = APIRouter(
    prefix="/transactions",
    tags=["Transaction"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/trader/{trader_id}", response_model=list[TransactionRead])
def list_trader_transactions(
    trader_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assert_can_access_trader(trader_id, current_user)
    return transaction_service.list_trader_transactions(db, trader_id)


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(db, transaction_id)
    assert_can_access_trader(transaction.trader_id, current_user)
    return transaction


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return transaction_service.create_transaction(db, data, owned_trader_id)


@router.put("/{transaction_id}", response_model=TransactionRead)
def replace_transaction(
    transaction_id: UUID,
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(db, transaction_id)
    assert_can_access_trader(transaction.trader_id, current_user)
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return transaction_service.replace_transaction(
        db, transaction_id, data, owned_trader_id
    )


@router.patch("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: UUID,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(db, transaction_id)
    assert_can_access_trader(transaction.trader_id, current_user)
    return transaction_service.update_transaction(db, transaction_id, data)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = transaction_service.get_transaction(db, transaction_id)
    assert_can_access_trader(transaction.trader_id, current_user)
    transaction_service.delete_transaction(db, transaction_id)
