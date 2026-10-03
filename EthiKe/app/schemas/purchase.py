from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class PurchaseBase(BaseModel):
    product_id: UUID
    trader_id: UUID
    quantity: Decimal
    unit_cost_at_purchase: Decimal
    supplier: Optional[str] = None


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    unit_cost_at_purchase: Optional[Decimal] = None
    supplier: Optional[str] = None


class PurchaseRead(PurchaseBase):
    model_config = ConfigDict(from_attributes=True)

    purchase_id: UUID
    purchase_date: datetime
