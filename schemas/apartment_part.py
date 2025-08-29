from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from .enums import PartStatusEnum


class ApartmentPartBase(BaseModel):
    status: PartStatusEnum = PartStatusEnum.available
    studio_number: Optional[str] = None
    rent_value: Optional[Decimal] = None


class ApartmentPartCreate(ApartmentPartBase):
    pass


class ApartmentPartUpdate(BaseModel):
    status: Optional[PartStatusEnum] = None
    studio_number: Optional[str] = None
    rent_value: Optional[Decimal] = None


class ApartmentPartResponse(ApartmentPartBase):
    id: int
    apartment_id: int
    created_by_admin_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
