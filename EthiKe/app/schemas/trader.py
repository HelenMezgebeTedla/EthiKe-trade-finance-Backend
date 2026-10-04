from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TraderBase(BaseModel):
    name: str
    phone_number: str
    business_type: str | None = None
    region: str | None = None
    city: str | None = None


class TraderCreate(TraderBase):
    pass


class TraderUpdate(BaseModel):
    name: str | None = None
    business_type: str | None = None
    region: str | None = None
    city: str | None = None


class TraderRead(TraderBase):
    model_config = ConfigDict(from_attributes=True)

    trader_id: UUID
    registration_date: datetime
