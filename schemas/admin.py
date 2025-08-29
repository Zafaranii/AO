from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from .enums import AdminRoleEnum


class AdminBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: AdminRoleEnum = AdminRoleEnum.admin


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[AdminRoleEnum] = None
    password: Optional[str] = None


class AdminResponse(AdminBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    email: EmailStr
    password: str
