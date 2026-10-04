from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.repositories.user import user_repository
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user = user_repository.get(db, UUID(user_id))
    except ValueError:
        raise credentials_exception

    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_roles(*allowed_roles: UserRole):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {[r.value for r in allowed_roles]}",
            )
        return current_user

    return dependency


def get_owned_trader_id(requested_trader_id: UUID | None, current_user: User) -> UUID:

    if current_user.role == UserRole.ADMIN:
        if requested_trader_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="trader_id is required for admin requests",
            )
        return requested_trader_id

    if current_user.trader_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have a trader profile yet — create one at POST /traders/",
        )
    return current_user.trader_id


def assert_can_access_trader(
    trader_id: UUID, current_user: User, db: Session = None
) -> None:
    """Raises 403 unless current_user is an admin or the owner of trader_id."""
    if current_user.role == UserRole.ADMIN:
        return
    if current_user.trader_id != trader_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this trader's data",
        )
