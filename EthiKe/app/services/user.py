from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, data: UserCreate):
    """Public self-signup — always lands as whatever role the caller asked for.
    (See create_user for the admin-only, same-shape endpoint at /users/.)"""
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    if user_repository.get_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    payload = data.model_dump(exclude={"password"})
    payload["hashed_password"] = hash_password(data.password)
    return user_repository.create(db, payload)


create_user = register_user


def get_user(db: Session, user_id):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def list_users(db: Session):
    return user_repository.get_all(db)


def update_user(db: Session, user_id, data: UserUpdate):
    user = get_user(db, user_id)
    return user_repository.update(db, user, data.model_dump(exclude_unset=True))


def delete_user(db: Session, user_id):
    user = get_user(db, user_id)
    user_repository.delete(db, user)


def authenticate_user(db: Session, username: str, password: str):
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    return user


def login(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    token = create_access_token(data={"sub": str(user.user_id), "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}
