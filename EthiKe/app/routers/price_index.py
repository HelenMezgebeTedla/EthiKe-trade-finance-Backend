from uuid import UUID

from database import get_db
from dependencies import get_current_user, require_roles
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import UserRole
from app.schemas.price_index import PriceIndexCreate, PriceIndexRead, PriceIndexUpdate
from app.services import price_index as price_index_service

router = APIRouter(
    prefix="/price-index", tags=["PriceIndex"], dependencies=[Depends(get_current_user)]
)
ADMIN_ONLY = Depends(require_roles(UserRole.ADMIN))


@router.get("/", response_model=list[PriceIndexRead])
def list_price_indices(db: Session = Depends(get_db)):
    """Reference data — readable by any authenticated user (trader or admin)."""
    return price_index_service.list_price_indices(db)


@router.get("/category/{category}", response_model=list[PriceIndexRead])
def get_category_series(category: str, db: Session = Depends(get_db)):
    return price_index_service.get_category_series(db, category)


@router.get("/{price_index_id}", response_model=PriceIndexRead)
def get_price_index(price_index_id: UUID, db: Session = Depends(get_db)):
    return price_index_service.get_price_index(db, price_index_id)


@router.post(
    "/",
    response_model=PriceIndexRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ADMIN_ONLY],
)
def create_index_point(data: PriceIndexCreate, db: Session = Depends(get_db)):
    """Admin only — this is shared reference data, not a trader's own record."""
    return price_index_service.create_index_point(db, data)


@router.put(
    "/{price_index_id}", response_model=PriceIndexRead, dependencies=[ADMIN_ONLY]
)
def replace_index_point(
    price_index_id: UUID, data: PriceIndexCreate, db: Session = Depends(get_db)
):
    return price_index_service.replace_index_point(db, price_index_id, data)


@router.patch(
    "/{price_index_id}", response_model=PriceIndexRead, dependencies=[ADMIN_ONLY]
)
def update_index_point(
    price_index_id: UUID, data: PriceIndexUpdate, db: Session = Depends(get_db)
):
    return price_index_service.update_index_point(db, price_index_id, data)


@router.delete(
    "/{price_index_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[ADMIN_ONLY],
)
def delete_index_point(price_index_id: UUID, db: Session = Depends(get_db)):
    return price_index_service.delete_index_point(db, price_index_id)
