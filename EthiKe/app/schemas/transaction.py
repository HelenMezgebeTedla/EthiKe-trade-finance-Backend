from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.transaction import PaymentMethod, TransactionType


class TransactionBase(BaseModel):
    trader_id: UUID
    type: TransactionType
    amount: Decimal
    currency: str = "ETB"
    payment_method: PaymentMethod | None = None
    counterparty: str | None = None
    notes: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type: TransactionType | None = None
    amount: Decimal | None = None
    currency: str | None = None
    payment_method: PaymentMethod | None = None
    counterparty: str | None = None
    notes: str | None = None


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: UUID
    timestamp: datetime
