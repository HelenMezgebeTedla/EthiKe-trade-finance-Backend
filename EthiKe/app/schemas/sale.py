from datetime import datetime
from decimal import Decimal
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
    quantity_sold: Decimal | None = None
    unit_sale_price: Decimal | None = None


class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)

    sale_id: UUID
    sale_date: datetime
