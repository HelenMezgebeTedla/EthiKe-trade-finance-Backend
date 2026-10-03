from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.product import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def list_trader_products(db: Session, trader_id):
    return product_repository.get_by_trader(db, trader_id)


def create_product(db: Session, data: ProductCreate, owned_trader_id):
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    return product_repository.create(db, payload)


def replace_product(db: Session, product_id, data: ProductCreate, owned_trader_id):
    product = get_product(db, product_id)
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    return product_repository.update(db, product, payload)


def update_product(db: Session, product_id, data: ProductUpdate):
    product = get_product(db, product_id)
    return product_repository.update(db, product, data.model_dump(exclude_unset=True))


def delete_product(db: Session, product_id):
    product = get_product(db, product_id)
    product_repository.delete(db, product)
