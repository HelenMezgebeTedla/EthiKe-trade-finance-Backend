from sqlalchemy import Column, String, DECIMAL, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    trader_id = Column(UUID(as_uuid=True), ForeignKey("traders.trader_id"), nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    current_stock_quantity = Column(DECIMAL(12, 2), nullable=False, default=0)

    trader = relationship("Trader", back_populates="products")
    purchases = relationship("Purchase", back_populates="product")
    sales = relationship("Sale", back_populates="product")
