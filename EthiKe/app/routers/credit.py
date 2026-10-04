from uuid import UUID

from database import get_db
from dependencies import assert_can_access_trader, get_current_user, get_owned_trader_id
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.credit import CreditCreate, CreditRead, CreditRepay, CreditUpdate
from app.services import credit as credit_service

router = APIRouter(
    prefix="/credits", tags=["Credit"], dependencies=[Depends(get_current_user)]
)


@router.get("/trader/{trader_id}/open", response_model=list[CreditRead])
def list_open_credit(
    trader_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assert_can_access_trader(trader_id, current_user)
    return credit_service.list_open_credit(db, trader_id)


@router.get("/{credit_id}", response_model=CreditRead)
def get_credit(
    credit_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit = credit_service.get_credit(db, credit_id)
    assert_can_access_trader(credit.trader_id, current_user)
    return credit


@router.post("/", response_model=CreditRead, status_code=status.HTTP_201_CREATED)
def create_credit(
    data: CreditCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return credit_service.create_credit(db, data, owned_trader_id)


@router.post("/{credit_id}/repay", response_model=CreditRead)
def repay_credit(
    credit_id: UUID,
    data: CreditRepay,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit = credit_service.get_credit(db, credit_id)
    assert_can_access_trader(credit.trader_id, current_user)
    return credit_service.repay_credit(db, credit_id, data)


@router.put("/{credit_id}", response_model=CreditRead)
def replace_credit(
    credit_id: UUID,
    data: CreditCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit = credit_service.get_credit(db, credit_id)
    assert_can_access_trader(credit.trader_id, current_user)
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return credit_service.replace_credit(db, credit_id, data, owned_trader_id)


@router.patch("/{credit_id}", response_model=CreditRead)
def update_credit(
    credit_id: UUID,
    data: CreditUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit = credit_service.get_credit(db, credit_id)
    assert_can_access_trader(credit.trader_id, current_user)
    return credit_service.update_credit(db, credit_id, data)


@router.delete("/{credit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credit(
    credit_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    credit = credit_service.get_credit(db, credit_id)
    assert_can_access_trader(credit.trader_id, current_user)
    credit_service.delete_credit(db, credit_id)
