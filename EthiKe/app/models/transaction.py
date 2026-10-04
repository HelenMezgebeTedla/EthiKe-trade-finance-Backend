import enum
import uuid

from database import Base
from sqlalchemy import DECIMAL, UUID, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class TransactionType(str, enum.Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    EXPENSE = "expense"
    PERSONAL_WITHDRAWAL = "personal_withdrawal"
    CREDIT_GIVEN = "credit_given"
    CREDIT_REPAID = "credit_repaid"


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    TELEBIRR = "telebirr"
    CBE_BIRR = "cbe_birr"
    M_PESA = "m_pesa"
    CREDIT = "credit"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    trader_id = Column(
        UUID(as_uuid=True), ForeignKey("traders.trader_id"), nullable=False
    )
    type = Column(Enum(TransactionType, name="transaction_type_enum"), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="ETB")
    payment_method = Column(
        Enum(PaymentMethod, name="payment_method_enum"), nullable=True
    )
    counterparty = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String, nullable=True)

    trader = relationship("Trader", back_populates="transactions")
    sale = relationship("Sale", back_populates="transaction", uselist=False)
