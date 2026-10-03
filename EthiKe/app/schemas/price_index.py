from datetime import date
from decimal import Decimal
from typing import Optional
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
    country: Optional[str] = None
    category: Optional[str] = None
    month: Optional[date] = None
    index_value: Optional[Decimal] = None


class PriceIndexRead(PriceIndexBase):
    model_config = ConfigDict(from_attributes=True)

    price_index_id: UUID
