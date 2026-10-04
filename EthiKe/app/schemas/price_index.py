from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceIndexBase(BaseModel):
    country: str
    category: str
    month: date
    index_value: Decimal


class PriceIndexCreate(PriceIndexBase):
    pass


class PriceIndexUpdate(BaseModel):
    country: str | None = None
    category: str | None = None
    month: date | None = None
    index_value: Decimal | None = None


class PriceIndexRead(PriceIndexBase):
    model_config = ConfigDict(from_attributes=True)

    price_index_id: UUID
