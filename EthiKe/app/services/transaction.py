from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.transaction import transaction_repository
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def get_transaction(db: Session, transaction_id):
    transaction = transaction_repository.get(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return transaction


def list_trader_transactions(db: Session, trader_id):
    return transaction_repository.get_by_trader(db, trader_id)


def create_transaction(db: Session, data: TransactionCreate, owned_trader_id):
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    return transaction_repository.create(db, payload)


def replace_transaction(
    db: Session, transaction_id, data: TransactionCreate, owned_trader_id
):
    transaction = get_transaction(db, transaction_id)
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    return transaction_repository.update(db, transaction, payload)


def update_transaction(db: Session, transaction_id, data: TransactionUpdate):
    transaction = get_transaction(db, transaction_id)
    return transaction_repository.update(
        db, transaction, data.model_dump(exclude_unset=True)
    )


def delete_transaction(db: Session, transaction_id):
    transaction = get_transaction(db, transaction_id)
    transaction_repository.delete(db, transaction)
