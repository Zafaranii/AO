from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ApartmentSaleBase(BaseModel):
    title: str
    location: str
    description: Optional[str] = None
    price: Decimal


class ApartmentSaleCreate(ApartmentSaleBase):
    pass


class ApartmentSaleUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None


class ApartmentSaleResponse(ApartmentSaleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
