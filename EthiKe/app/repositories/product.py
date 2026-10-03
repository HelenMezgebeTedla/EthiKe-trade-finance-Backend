from app.models.product import Product
from sqlalchemy.orm import Session


class ProductRepository:
    def __init__(self):
        self.model = Product

    def get(self, db: Session, id):
        return db.get(Product, id)

    def get_all(self, db: Session):
        return db.query(Product).all()

    def get_by_trader(self, db: Session, trader_id):
        return db.query(Product).filter(Product.trader_id == trader_id).all()

    def create(self, db: Session, data: dict):
        product = Product(**data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, db_obj: Product, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product):
        db.delete(db_obj)
        db.commit()


product_repository = ProductRepository()
