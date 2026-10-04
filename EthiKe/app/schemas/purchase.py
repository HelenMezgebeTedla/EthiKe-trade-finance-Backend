from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PurchaseBase(BaseModel):
    product_id: UUID
    trader_id: UUID
    quantity: Decimal
    unit_cost_at_purchase: Decimal
    supplier: str | None = None


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(BaseModel):
    quantity: Decimal | None = None
    unit_cost_at_purchase: Decimal | None = None
    supplier: str | None = None


class PurchaseRead(PurchaseBase):
    model_config = ConfigDict(from_attributes=True)

    purchase_id: UUID
    purchase_date: datetime
