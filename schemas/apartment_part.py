from pydantic import BaseModel, field_validator
from typing import Optional, List, Union
from datetime import datetime
from decimal import Decimal
import json

from .enums import PartStatusEnum, BathroomTypeEnum, FurnishedEnum, BalconyEnum


class ApartmentPartBase(BaseModel):
    status: PartStatusEnum = PartStatusEnum.available
    title: str
    area: Decimal
    floor: int
    monthly_price: Decimal
    bedrooms: int
    bathrooms: BathroomTypeEnum
    furnished: FurnishedEnum
    balcony: BalconyEnum
    description: Optional[str] = None
    photos_url: Optional[List[str]] = None

    @field_validator('photos_url', mode='before')
    @classmethod
    def parse_photos_url(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]  # If it's not valid JSON, treat as single URL
        return v


class ApartmentPartCreate(BaseModel):
    status: PartStatusEnum = PartStatusEnum.available
    title: str
    area: Decimal
    floor: Optional[int] = None  # Will be inherited from apartment
    monthly_price: Decimal
    bedrooms: int
    bathrooms: BathroomTypeEnum
    furnished: FurnishedEnum
    balcony: BalconyEnum
    description: Optional[str] = None
    photos_url: Optional[List[str]] = None


class ApartmentPartUpdate(BaseModel):
    status: Optional[PartStatusEnum] = None
    title: Optional[str] = None
    area: Optional[Decimal] = None
    floor: Optional[int] = None
    monthly_price: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[BathroomTypeEnum] = None
    furnished: Optional[FurnishedEnum] = None
    balcony: Optional[BalconyEnum] = None
    description: Optional[str] = None
    photos_url: Optional[List[str]] = None


class ApartmentPartResponse(ApartmentPartBase):
    id: int
    apartment_id: int
    created_by_admin_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @field_validator('photos_url', mode='after')
    @classmethod
    def serialize_photos_url(cls, v):
        if v is None:
            return None
        if isinstance(v, list):
            return v
        return v
    
    class Config:
        from_attributes = True
