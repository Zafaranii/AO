from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import Notification, NotificationStatusEnum, Admin, AdminRoleEnum
from schemas.notification import NotificationCreate, NotificationUpdate


def get_notifications(
    db: Session,
    admin_id: Optional[int] = None,
    status: Optional[NotificationStatusEnum] = None,
    is_read: Optional[bool] = None,
    is_resolved: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Notification)
    if admin_id:
        query = query.filter(Notification.notify_admin_id == admin_id)
    if status:
        query = query.filter(Notification.status == status)
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    if is_resolved is not None:
        query = query.filter(Notification.is_resolved == is_resolved)
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


def create_notification(db: Session, notification: NotificationCreate):
    # Check if notification already exists to avoid duplicates
    existing = db.query(Notification).filter(
        and_(
            Notification.rental_contract_id == notification.rental_contract_id,
            Notification.status == notification.status,
            Notification.is_resolved == False
        )
    ).first()

    if existing:
        return existing

    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def update_notification(db: Session, notification_id: int, notification: NotificationUpdate):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification:
        update_data = notification.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notification, field, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification



