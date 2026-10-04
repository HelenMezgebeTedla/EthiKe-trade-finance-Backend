import uuid

from database import Base
from sqlalchemy import DECIMAL, UUID, Column, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class CashSnapshot(Base):
    """Derived/rollup row — written by the service layer, not created directly by users."""

    __tablename__ = "cash_snapshots"

    cash_snapshot_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    trader_id = Column(
        UUID(as_uuid=True), ForeignKey("traders.trader_id"), nullable=False
    )
    date = Column(Date, server_default=func.current_date())
    cash_on_hand = Column(DECIMAL(12, 2), nullable=False, default=0)
    mobile_money_balance = Column(DECIMAL(12, 2), nullable=False, default=0)
    working_capital = Column(DECIMAL(12, 2), nullable=False, default=0)
    true_profit_estimate = Column(DECIMAL(12, 2), nullable=False, default=0)

    trader = relationship("Trader", back_populates="cash_snapshots")
