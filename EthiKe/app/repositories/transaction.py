from app.models.transaction import Transaction
from sqlalchemy.orm import Session


class TransactionRepository:
    def __init__(self):
        self.model = Transaction

    def get(self, db: Session, id):
        return db.get(Transaction, id)

    def get_all(self, db: Session):
        return db.query(Transaction).all()

    def get_by_trader(self, db: Session, trader_id, limit: int = 200):
        return (
            db.query(Transaction)
            .filter(Transaction.trader_id == trader_id)
            .order_by(Transaction.timestamp.desc())
            .limit(limit)
            .all()
        )

    def create(self, db: Session, data: dict):
        transaction = Transaction(**data)
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    def update(self, db: Session, db_obj: Transaction, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Transaction):
        db.delete(db_obj)
        db.commit()


transaction_repository = TransactionRepository()
