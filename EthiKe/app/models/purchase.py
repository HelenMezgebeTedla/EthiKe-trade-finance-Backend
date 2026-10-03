from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    purchase_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    trader_id = Column(UUID(as_uuid=True), ForeignKey("traders.trader_id"), nullable=False)
    quantity = Column(DECIMAL(12, 2), nullable=False)
    unit_cost_at_purchase = Column(DECIMAL(12, 2), nullable=False)
    supplier = Column(String, nullable=True)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="purchases")
    trader = relationship("Trader", back_populates="purchases")
