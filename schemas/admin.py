from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

from .enums import AdminRoleEnum


class AdminBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    role: AdminRoleEnum
    
    @validator('role')
    def validate_role_not_super_admin(cls, v):
        """Only super_admin role is not allowed for regular registration."""
        if v == AdminRoleEnum.super_admin:
            raise ValueError('Cannot create super admin through regular registration')
        return v


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[AdminRoleEnum] = None
    password: Optional[str] = None


class AdminResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    role: AdminRoleEnum
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    username: str  # Can be email or phone
    password: str


class PasswordVerification(BaseModel):
    current_password: str


class EmailUpdate(BaseModel):
    new_email: EmailStr
    current_password: str


class PasswordUpdate(BaseModel):
    new_password: str
    current_password: str


class MasterAdminCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    master_password: str  # Special password to create master admin


class MasterAdminCreateData(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: AdminRoleEnum = AdminRoleEnum.super_admin
