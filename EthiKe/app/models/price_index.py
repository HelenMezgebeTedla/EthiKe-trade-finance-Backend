import uuid

from sqlalchemy import DECIMAL, UUID, Column, Date, String

from database import Base


class PriceIndex(Base):
    __tablename__ = "price_indices"

    price_index_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False
    )
    country = Column(String, nullable=False)
    category = Column(String, nullable=False)
    month = Column(Date, nullable=False)
    index_value = Column(DECIMAL(10, 2), nullable=False)
