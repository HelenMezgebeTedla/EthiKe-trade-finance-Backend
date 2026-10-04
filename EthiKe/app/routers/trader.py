from uuid import UUID

from database import get_db
from dependencies import assert_can_access_trader, get_current_user, require_roles
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.trader import TraderCreate, TraderRead, TraderUpdate
from app.services import trader as trader_service

router = APIRouter(
    prefix="/traders", tags=["Trader"], dependencies=[Depends(get_current_user)]
)
ADMIN_ONLY = Depends(require_roles(UserRole.ADMIN))


@router.get("/", response_model=list[TraderRead], dependencies=[ADMIN_ONLY])
def list_traders(db: Session = Depends(get_db)):
    """Admin only — traders can only ever see their own profile (GET /traders/{id})."""
    return trader_service.list_traders(db)


@router.get("/{trader_id}", response_model=TraderRead)
def get_trader(
    trader_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assert_can_access_trader(trader_id, current_user, db)
    return trader_service.get_trader(db, trader_id)


@router.post("/", response_model=TraderRead, status_code=status.HTTP_201_CREATED)
def create_trader(
    data: TraderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Any authenticated user can create a trader profile; if you're a
    'trader'-role account with no profile yet, it's linked to you automatically."""
    return trader_service.create_trader(db, data, current_user)


@router.put("/{trader_id}", response_model=TraderRead)
def replace_trader(
    trader_id: UUID,
    data: TraderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assert_can_access_trader(trader_id, current_user, db)
    return trader_service.replace_trader(db, trader_id, data)


@router.patch("/{trader_id}", response_model=TraderRead)
def update_trader(
    trader_id: UUID,
    data: TraderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assert_can_access_trader(trader_id, current_user, db)
    return trader_service.update_trader(db, trader_id, data)


@router.delete(
    "/{trader_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[ADMIN_ONLY]
)
def delete_trader(trader_id: UUID, db: Session = Depends(get_db)):
    return trader_service.delete_trader(db, trader_id)
