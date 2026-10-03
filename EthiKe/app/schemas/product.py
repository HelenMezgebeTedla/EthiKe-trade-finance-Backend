from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    trader_id: UUID
    product_name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    current_stock_quantity: Decimal = Decimal("0")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    current_stock_quantity: Optional[Decimal] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
