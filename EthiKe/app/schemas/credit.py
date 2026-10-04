from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.credit import CreditStatus


class CreditBase(BaseModel):
    trader_id: UUID
    customer_name: str
    amount_owed: Decimal
    due_date: datetime | None = None


class CreditCreate(CreditBase):
    pass


class CreditUpdate(BaseModel):
    customer_name: str | None = None
    amount_owed: Decimal | None = None
    due_date: datetime | None = None
    status: CreditStatus | None = None


class CreditRepay(BaseModel):
    amount: Decimal


class CreditRead(CreditBase):
    model_config = ConfigDict(from_attributes=True)

    credit_id: UUID
    date_given: datetime
    amount_repaid: Decimal
    status: CreditStatus
