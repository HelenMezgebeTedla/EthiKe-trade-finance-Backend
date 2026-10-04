import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CashSnapshotCreate(BaseModel):
    trader_id: UUID
    date: datetime.date | None = None
    cash_on_hand: Decimal = Decimal(0)
    mobile_money_balance: Decimal = Decimal(0)
    working_capital: Decimal = Decimal(0)


class CashSnapshotUpdate(BaseModel):
    date: datetime.date | None = None
    cash_on_hand: Decimal | None = None
    mobile_money_balance: Decimal | None = None
    true_profit_estimate: Decimal | None = None


class CashSnapshotRead(BaseModel):
    cash_snapshot_id: UUID
    trader_id: UUID
    date: datetime.date
    cash_on_hand: Decimal
    mobile_money_balance: Decimal
    working_capital: Decimal
    true_profit_estimate: Decimal | None

    model_config = ConfigDict(from_attributes=True)
