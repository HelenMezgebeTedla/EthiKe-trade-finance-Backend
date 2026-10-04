from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.credit import credit_repository
from app.schemas.credit import CreditCreate, CreditRepay, CreditUpdate


def get_credit(db: Session, credit_id):
    credit = credit_repository.get(db, credit_id)
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credit record not found"
        )
    return credit


def list_open_credit(db: Session, trader_id):
    return credit_repository.get_open_by_trader(db, trader_id)


def create_credit(db: Session, data: CreditCreate, owned_trader_id):
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    return credit_repository.create(db, payload)


def replace_credit(db: Session, credit_id, data: CreditCreate, owned_trader_id):
    credit = get_credit(db, credit_id)
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    return credit_repository.update(db, credit, payload)


def update_credit(db: Session, credit_id, data: CreditUpdate):
    credit = get_credit(db, credit_id)
    return credit_repository.update(db, credit, data.model_dump(exclude_unset=True))


def delete_credit(db: Session, credit_id):
    credit = get_credit(db, credit_id)
    credit_repository.delete(db, credit)


def repay_credit(db: Session, credit_id, data: CreditRepay):
    credit = get_credit(db, credit_id)
    new_repaid = credit.amount_repaid + data.amount
    status_value = (
        "closed"
        if new_repaid >= credit.amount_owed
        else "partial"
        if new_repaid > 0
        else "open"
    )
    return credit_repository.update(
        db, credit, {"amount_repaid": new_repaid, "status": status_value}
    )
