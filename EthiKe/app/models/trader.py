import uuid

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Trader(Base):
    __tablename__ = "traders"

    trader_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    name = Column(String, nullable=False)
    phone_number = Column(String(50), nullable=False, unique=True)
    business_type = Column(String, nullable=True)
    region = Column(String, nullable=True)
    city = Column(String, nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", back_populates="trader")
    products = relationship("Product", back_populates="trader")
    purchases = relationship("Purchase", back_populates="trader")
    credits = relationship("Credit", back_populates="trader")
    cash_snapshots = relationship("CashSnapshot", back_populates="trader")
