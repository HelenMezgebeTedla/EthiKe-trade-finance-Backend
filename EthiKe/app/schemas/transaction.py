from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.transaction import TransactionType, PaymentMethod


class TransactionBase(BaseModel):
    trader_id: UUID
    type: TransactionType
    amount: Decimal
    currency: str = "ETB"
    payment_method: Optional[PaymentMethod] = None
    counterparty: Optional[str] = None
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    counterparty: Optional[str] = None
    notes: Optional[str] = None


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: UUID
    timestamp: datetime
