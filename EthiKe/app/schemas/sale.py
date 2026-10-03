from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SaleBase(BaseModel):
    transaction_id: UUID
    product_id: UUID
    quantity_sold: Decimal
    unit_sale_price: Decimal


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    quantity_sold: Optional[Decimal] = None
    unit_sale_price: Optional[Decimal] = None


class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)

    sale_id: UUID
    sale_date: datetime
