from sqlalchemy.orm import Session

from app.models.trader import Trader


class TraderRepository:
    def __init__(self):
        self.model = Trader

    def get(self, db: Session, id):
        return db.get(Trader, id)

    def get_all(self, db: Session):
        return db.query(Trader).all()

    def get_by_phone(self, db: Session, phone_number: str):
        return db.query(Trader).filter(Trader.phone_number == phone_number).first()

    def create(self, db: Session, data: dict):
        trader = Trader(**data)
        db.add(trader)
        db.commit()
        db.refresh(trader)
        return trader

    def update(self, db: Session, db_obj: Trader, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Trader):
        db.delete(db_obj)
        db.commit()


trader_repository = TraderRepository()
