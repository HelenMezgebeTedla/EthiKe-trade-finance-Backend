from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.credit import CreditStatus


class CreditBase(BaseModel):
    trader_id: UUID
    customer_name: str
    amount_owed: Decimal
    due_date: Optional[datetime] = None


class CreditCreate(CreditBase):
    pass


class CreditUpdate(BaseModel):
    customer_name: Optional[str] = None
    amount_owed: Optional[Decimal] = None
    due_date: Optional[datetime] = None
    status: Optional[CreditStatus] = None


class CreditRepay(BaseModel):
    amount: Decimal


class CreditRead(CreditBase):
    model_config = ConfigDict(from_attributes=True)

    credit_id: UUID
    date_given: datetime
    amount_repaid: Decimal
    status: CreditStatus
