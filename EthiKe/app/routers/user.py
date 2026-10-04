from uuid import UUID

from database import get_db
from dependencies import get_current_user, require_roles
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.user import UserRole
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=UserRead)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


@router.get(
    "/",
    response_model=list[UserRead],
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.put(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def replace_user(user_id: UUID, data: UserCreate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, UserUpdate(**data.model_dump()))


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def update_user(user_id: UUID, data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)
