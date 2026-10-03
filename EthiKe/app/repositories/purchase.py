from app.models.purchase import Purchase
from sqlalchemy.orm import Session


class PurchaseRepository:
    def __init__(self):
        self.model = Purchase

    def get(self, db: Session, id):
        return db.get(Purchase, id)

    def get_all(self, db: Session):
        return db.query(Purchase).all()

    def get_by_product(self, db: Session, product_id):
        return (
            db.query(Purchase)
            .filter(Purchase.product_id == product_id)
            .order_by(Purchase.purchase_date.asc())
            .all()
        )

    def create(self, db: Session, data: dict):
        purchase = Purchase(**data)
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase

    def update(self, db: Session, db_obj: Purchase, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Purchase):
        db.delete(db_obj)
        db.commit()


purchase_repository = PurchaseRepository()
