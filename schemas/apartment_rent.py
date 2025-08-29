from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from .apartment_part import ApartmentPartResponse


class ApartmentRentBase(BaseModel):
    title: str
    location: str
    total_parts: int
    description: Optional[str] = None
    rent_price: Decimal


class ApartmentRentCreate(ApartmentRentBase):
    pass


class ApartmentRentUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    total_parts: Optional[int] = None
    description: Optional[str] = None
    rent_price: Optional[Decimal] = None


class ApartmentRentResponse(ApartmentRentBase):
    id: int
    listed_by_admin_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ApartmentRentWithParts(ApartmentRentResponse):
    apartment_parts: List[ApartmentPartResponse] = []
