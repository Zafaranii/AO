from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Admin, NotificationStatusEnum, Notification, AdminRoleEnum
from schemas.notification import NotificationResponse, NotificationUpdate
from crud import get_notifications, update_notification
from dependencies import get_current_admin_or_super_admin

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[NotificationStatusEnum] = Query(None, description="Filter by notification status"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    is_resolved: Optional[bool] = Query(None, description="Filter by resolved status"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get notifications for current admin."""
    notifications = get_notifications(
        db=db,
        admin_id=current_admin.id,
        status=status,
        is_read=is_read,
        is_resolved=is_resolved,
        skip=skip,
        limit=limit
    )
    return notifications

@router.get("/all", response_model=List[NotificationResponse])
async def list_all_notifications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[NotificationStatusEnum] = Query(None, description="Filter by notification status"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    is_resolved: Optional[bool] = Query(None, description="Filter by resolved status"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get all notifications (for super admins to see system-wide notifications)."""
    notifications = get_notifications(
        db=db,
        status=status,
        is_read=is_read,
        is_resolved=is_resolved,
        skip=skip,
        limit=limit
    )
    return notifications

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification_status(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Update notification status (mark as read/resolved)."""
    # Get the notification to verify ownership
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Check if admin owns this notification or is super admin
    if (db_notification.notify_admin_id != current_admin.id and 
        current_admin.role != AdminRoleEnum.super_admin):
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to update this notification"
        )
    
    updated_notification = update_notification(db, notification_id=notification_id, notification=notification)
    if updated_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification

@router.get("/unread/count")
async def get_unread_notifications_count(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get count of unread notifications for current admin."""
    count = len(get_notifications(
        db=db,
        admin_id=current_admin.id,
        is_read=False,
        limit=1000  # Get all unread notifications to count them
    ))
    return {"unread_count": count}
