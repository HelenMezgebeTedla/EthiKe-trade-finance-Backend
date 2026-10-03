from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.trader import trader_repository
from app.repositories.user import user_repository
from app.schemas.trader import TraderCreate, TraderUpdate


def get_trader(db: Session, trader_id):
    trader = trader_repository.get(db, trader_id)
    if not trader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trader not found")
    return trader


def list_traders(db: Session):
    return trader_repository.get_all(db)


def create_trader(db: Session, data: TraderCreate, current_user):
    """Creates the Trader business profile and links it to the caller's
    account (current_user.trader_id) so future requests resolve ownership
    automatically. Admins may create a trader profile without it being
    linked to their own account."""
    trader = trader_repository.create(db, data.model_dump())
    if current_user.role.value == "trader" and current_user.trader_id is None:
        user_repository.update(db, current_user, {"trader_id": trader.trader_id})
    return trader


def replace_trader(db: Session, trader_id, data: TraderCreate):
    trader = get_trader(db, trader_id)
    return trader_repository.update(db, trader, data.model_dump())


def update_trader(db: Session, trader_id, data: TraderUpdate):
    trader = get_trader(db, trader_id)
    return trader_repository.update(db, trader, data.model_dump(exclude_unset=True))


def delete_trader(db: Session, trader_id):
    trader = get_trader(db, trader_id)
    trader_repository.delete(db, trader)
