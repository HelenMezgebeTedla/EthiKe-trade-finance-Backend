from app.models.price_index import PriceIndex
from sqlalchemy.orm import Session


class PriceIndexRepository:
    def __init__(self):
        self.model = PriceIndex

    def get(self, db: Session, id):
        return db.get(PriceIndex, id)

    def get_all(self, db: Session):
        return db.query(PriceIndex).all()

    def get_by_category(self, db: Session, category: str):
        return (
            db.query(PriceIndex)
            .filter(PriceIndex.category == category)
            .order_by(PriceIndex.month.asc())
            .all()
        )

    def create(self, db: Session, data: dict):
        price_index = PriceIndex(**data)
        db.add(price_index)
        db.commit()
        db.refresh(price_index)
        return price_index

    def update(self, db: Session, db_obj: PriceIndex, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: PriceIndex):
        db.delete(db_obj)
        db.commit()


price_index_repository = PriceIndexRepository()
