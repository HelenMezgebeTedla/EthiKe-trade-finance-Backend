from sqlalchemy.orm import Session

from app.models.credit import Credit


class CreditRepository:
    def __init__(self):
        self.model = Credit

    def get(self, db: Session, id):
        return db.get(Credit, id)

    def get_all(self, db: Session):
        return db.query(Credit).all()

    def get_open_by_trader(self, db: Session, trader_id):
        return (
            db.query(Credit)
            .filter(Credit.trader_id == trader_id, Credit.status != "closed")
            .all()
        )

    def create(self, db: Session, data: dict):
        credit = Credit(**data)
        db.add(credit)
        db.commit()
        db.refresh(credit)
        return credit

    def update(self, db: Session, db_obj: Credit, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Credit):
        db.delete(db_obj)
        db.commit()


credit_repository = CreditRepository()
