from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .enums import NotificationStatusEnum


class NotificationBase(BaseModel):
    status: NotificationStatusEnum
    description: Optional[str] = None


class NotificationCreate(NotificationBase):
    rental_contract_id: int
    notify_admin_id: int


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_resolved: Optional[bool] = None
    description: Optional[str] = None


class NotificationResponse(NotificationBase):
    id: int
    rental_contract_id: int
    notify_admin_id: int
    is_read: bool
    is_resolved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
