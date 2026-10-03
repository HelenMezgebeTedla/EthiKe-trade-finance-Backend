from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CashSnapshotCreate(BaseModel):
    trader_id: UUID
    date: Optional[date] = None
    cash_on_hand: Decimal = Decimal("0")
    mobile_money_balance: Decimal = Decimal("0")
    working_capital: Decimal = Decimal("0")
    true_profit_estimate: Decimal = Decimal("0")


class CashSnapshotUpdate(BaseModel):
    cash_on_hand: Optional[Decimal] = None
    mobile_money_balance: Optional[Decimal] = None
    working_capital: Optional[Decimal] = None
    true_profit_estimate: Optional[Decimal] = None


class CashSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cash_snapshot_id: UUID
    trader_id: UUID
    date: date
    cash_on_hand: Decimal
    mobile_money_balance: Decimal
    working_capital: Decimal
    true_profit_estimate: Decimal
