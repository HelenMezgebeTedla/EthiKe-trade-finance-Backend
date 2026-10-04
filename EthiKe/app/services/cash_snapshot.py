from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transaction import PaymentMethod, TransactionType
from app.repositories.cash_snapshot import cash_snapshot_repository
from app.repositories.credit import credit_repository
from app.repositories.transaction import transaction_repository
from app.schemas.cash_snapshot import CashSnapshotCreate, CashSnapshotUpdate


def get_snapshot(db: Session, cash_snapshot_id):
    snapshot = cash_snapshot_repository.get(db, cash_snapshot_id)
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cash snapshot not found"
        )
    return snapshot


def list_snapshots(db: Session):
    return cash_snapshot_repository.get_all(db)


def get_latest_snapshot(db: Session, trader_id):
    snapshot = cash_snapshot_repository.get_latest_for_trader(db, trader_id)
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No snapshot yet — call /compute first",
        )
    return snapshot


def create_snapshot(db: Session, data: CashSnapshotCreate, owned_trader_id):
    """Manual create — the usual path is compute_snapshot() below."""
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    payload["date"] = payload["date"] or date.today()
    return cash_snapshot_repository.create(db, payload)


def replace_snapshot(
    db: Session, cash_snapshot_id, data: CashSnapshotCreate, owned_trader_id
):
    snapshot = get_snapshot(db, cash_snapshot_id)
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    payload["date"] = payload["date"] or date.today()
    return cash_snapshot_repository.update(db, snapshot, payload)


def update_snapshot(db: Session, cash_snapshot_id, data: CashSnapshotUpdate):
    snapshot = get_snapshot(db, cash_snapshot_id)
    return cash_snapshot_repository.update(
        db, snapshot, data.model_dump(exclude_unset=True)
    )


def delete_snapshot(db: Session, cash_snapshot_id):
    snapshot = get_snapshot(db, cash_snapshot_id)
    cash_snapshot_repository.delete(db, snapshot)


def compute_snapshot(db: Session, trader_id):
    """Rolls up recent transactions and open credit into one true-profit snapshot row."""
    transactions = transaction_repository.get_by_trader(db, trader_id)
    open_credit = credit_repository.get_open_by_trader(db, trader_id)

    mobile_methods = (
        PaymentMethod.TELEBIRR,
        PaymentMethod.CBE_BIRR,
        PaymentMethod.M_PESA,
    )

    cash = sum(
        t.amount
        for t in transactions
        if t.payment_method == PaymentMethod.CASH and t.type == TransactionType.SALE
    )
    cash -= sum(
        t.amount
        for t in transactions
        if t.payment_method == PaymentMethod.CASH
        and t.type in (TransactionType.EXPENSE, TransactionType.PERSONAL_WITHDRAWAL)
    )
    mobile = sum(
        t.amount
        for t in transactions
        if t.payment_method in mobile_methods and t.type == TransactionType.SALE
    )
    mobile -= sum(
        t.amount
        for t in transactions
        if t.payment_method in mobile_methods
        and t.type in (TransactionType.EXPENSE, TransactionType.PERSONAL_WITHDRAWAL)
    )
    outstanding_credit = sum(c.amount_owed - c.amount_repaid for c in open_credit)

    working_capital = cash + mobile - outstanding_credit
    true_profit_estimate = working_capital

    return cash_snapshot_repository.create(
        db,
        {
            "trader_id": trader_id,
            "date": date.today(),
            "cash_on_hand": cash,
            "mobile_money_balance": mobile,
            "working_capital": working_capital,
            "true_profit_estimate": true_profit_estimate,
        },
    )
