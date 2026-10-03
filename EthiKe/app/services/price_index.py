from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.price_index import price_index_repository
from app.schemas.price_index import PriceIndexCreate, PriceIndexUpdate


def get_price_index(db: Session, price_index_id):
    price_index = price_index_repository.get(db, price_index_id)
    if not price_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price index point not found")
    return price_index


def list_price_indices(db: Session):
    return price_index_repository.get_all(db)


def get_category_series(db: Session, category: str):
    return price_index_repository.get_by_category(db, category)


def create_index_point(db: Session, data: PriceIndexCreate):
    return price_index_repository.create(db, data.model_dump())


def replace_index_point(db: Session, price_index_id, data: PriceIndexCreate):
    price_index = get_price_index(db, price_index_id)
    return price_index_repository.update(db, price_index, data.model_dump())


def update_index_point(db: Session, price_index_id, data: PriceIndexUpdate):
    price_index = get_price_index(db, price_index_id)
    return price_index_repository.update(db, price_index, data.model_dump(exclude_unset=True))


def delete_index_point(db: Session, price_index_id):
    price_index = get_price_index(db, price_index_id)
    price_index_repository.delete(db, price_index)
