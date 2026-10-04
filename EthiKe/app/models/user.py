import enum
import uuid

from database import Base
from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TRADER = "trader"


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum(UserRole, name="user_role_enum"), nullable=False, default=UserRole.TRADER
    )
    # Optional link from a "trader" role account to the Trader business profile it owns.
    trader_id = Column(
        UUID(as_uuid=True), ForeignKey("traders.trader_id"), nullable=True
    )
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trader = relationship("Trader")
