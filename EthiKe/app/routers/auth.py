from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from app.core.rate_limit import limiter
from app.schemas.user import UserCreate, UserRead, Token
from app.services import user as user_service
from dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, data: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, data)


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2-standard login: send as form data (username, password), not JSON.
    This is what makes the Swagger UI's 'Authorize' button work out of the box.
    Rate-limited to blunt password-guessing attacks."""
    return user_service.login(db, form_data.username, form_data.password)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
