from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class TraderBase(BaseModel):
    name: str
    phone_number: str
    business_type: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None


class TraderCreate(TraderBase):
    pass


class TraderUpdate(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None


class TraderRead(TraderBase):
    model_config = ConfigDict(from_attributes=True)

    trader_id: UUID
    registration_date: datetime
