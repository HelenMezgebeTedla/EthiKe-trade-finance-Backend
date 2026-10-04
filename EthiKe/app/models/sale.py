import uuid

from database import Base
from sqlalchemy import DECIMAL, UUID, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    transaction_id = Column(
        UUID(as_uuid=True), ForeignKey("transactions.transaction_id"), nullable=False
    )
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False
    )
    quantity_sold = Column(DECIMAL(12, 2), nullable=False)
    unit_sale_price = Column(DECIMAL(12, 2), nullable=False)
    sale_date = Column(DateTime(timezone=True), server_default=func.now())

    transaction = relationship("Transaction", back_populates="sale")
    product = relationship("Product", back_populates="sales")
