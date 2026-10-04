from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    trader_id: UUID
    product_name: str
    category: str | None = None
    unit: str | None = None
    current_stock_quantity: Decimal = Decimal(0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str | None = None
    category: str | None = None
    unit: str | None = None
    current_stock_quantity: Decimal | None = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
