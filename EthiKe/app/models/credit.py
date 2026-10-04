import enum
import uuid

from database import Base
from sqlalchemy import DECIMAL, UUID, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class CreditStatus(str, enum.Enum):
    OPEN = "open"
    PARTIAL = "partial"
    CLOSED = "closed"


class Credit(Base):
    __tablename__ = "credits"

    credit_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    trader_id = Column(
        UUID(as_uuid=True), ForeignKey("traders.trader_id"), nullable=False
    )
    customer_name = Column(String, nullable=False)
    amount_owed = Column(DECIMAL(12, 2), nullable=False)
    date_given = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)
    amount_repaid = Column(DECIMAL(12, 2), nullable=False, default=0)
    status = Column(
        Enum(CreditStatus, name="credit_status_enum"),
        nullable=False,
        default=CreditStatus.OPEN,
    )

    trader = relationship("Trader", back_populates="credits")
