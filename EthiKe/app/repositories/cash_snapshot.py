from app.models.cash_snapshot import CashSnapshot
from sqlalchemy.orm import Session


class CashSnapshotRepository:
    def __init__(self):
        self.model = CashSnapshot

    def get(self, db: Session, id):
        return db.get(CashSnapshot, id)

    def get_all(self, db: Session):
        return db.query(CashSnapshot).all()

    def get_latest_for_trader(self, db: Session, trader_id):
        return (
            db.query(CashSnapshot)
            .filter(CashSnapshot.trader_id == trader_id)
            .order_by(CashSnapshot.date.desc())
            .first()
        )

    def create(self, db: Session, data: dict):
        snapshot = CashSnapshot(**data)
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return snapshot

    def update(self, db: Session, db_obj: CashSnapshot, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: CashSnapshot):
        db.delete(db_obj)
        db.commit()


cash_snapshot_repository = CashSnapshotRepository()
