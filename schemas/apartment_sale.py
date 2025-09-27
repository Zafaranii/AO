from pydantic import BaseModel, field_validator
from typing import Optional, List, Union
from datetime import datetime
from decimal import Decimal
import json

from .enums import LocationEnum, BathroomTypeEnum


class ApartmentSaleBase(BaseModel):
    name: str
    location: LocationEnum
    address: str
    area: Decimal
    number: str
    price: Decimal
    bedrooms: int
    bathrooms: BathroomTypeEnum
    description: Optional[str] = None
    photos_url: Optional[List[str]] = None
    location_on_map: Optional[str] = None
    facilities_amenities: Optional[str] = None

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


class ApartmentSaleCreate(ApartmentSaleBase):
    pass


class ApartmentSaleUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[LocationEnum] = None
    address: Optional[str] = None
    area: Optional[Decimal] = None
    number: Optional[str] = None
    price: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[BathroomTypeEnum] = None
    description: Optional[str] = None
    photos_url: Optional[List[str]] = None
    location_on_map: Optional[str] = None
    facilities_amenities: Optional[str] = None


class ApartmentSaleResponse(ApartmentSaleBase):
    id: int
    contact_number: str
    listed_by_admin_id: int
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
