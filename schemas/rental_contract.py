from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class RentalContractBase(BaseModel):
    tenant_name: str
    tenant_phone: str
    contract_start_date: date
    contract_end_date: date
    rent_value: Decimal
    id_card_scan_url: Optional[str] = None
    contract_scan_url: Optional[str] = None


class RentalContractCreate(RentalContractBase):
    apartment_part_id: int


class RentalContractUpdate(BaseModel):
    tenant_name: Optional[str] = None
    tenant_phone: Optional[str] = None
    contract_start_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    rent_value: Optional[Decimal] = None
    id_card_scan_url: Optional[str] = None
    contract_scan_url: Optional[str] = None
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
