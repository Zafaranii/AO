from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

from .enums import CustomerSourceEnum


class RentalContractBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_id_number: str
    how_did_customer_find_us: CustomerSourceEnum
    paid_deposit: Decimal
    warrant_amount: Decimal
    rent_start_date: date
    rent_end_date: date
    rent_period: int  # Period in months
    contract_url: Optional[str] = None
    customer_id_url: Optional[str] = None
    commission: Decimal
    rent_price: Decimal


class RentalContractCreate(RentalContractBase):
    apartment_part_id: int


class RentalContractUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_id_number: Optional[str] = None
    how_did_customer_find_us: Optional[CustomerSourceEnum] = None
    paid_deposit: Optional[Decimal] = None
    warrant_amount: Optional[Decimal] = None
    rent_start_date: Optional[date] = None
    rent_end_date: Optional[date] = None
    rent_period: Optional[int] = None
    contract_url: Optional[str] = None
    customer_id_url: Optional[str] = None
    commission: Optional[Decimal] = None
    rent_price: Optional[Decimal] = None
    is_active: Optional[bool] = None


class RentalContractResponse(RentalContractBase):
    id: int
    apartment_part_id: int
    is_active: bool
    created_by_admin_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
