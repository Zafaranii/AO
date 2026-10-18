from typing import Optional

from sqlalchemy.orm import Session

from models import Admin, AdminRoleEnum


def get_admin_phone_for_whatsapp(db: Session, admin_id: Optional[int] = None) -> Optional[str]:
    """Get admin phone number for WhatsApp link generation.

    Uses the listing admin's phone when available, otherwise falls back to the super admin.
    """
    if admin_id is not None:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if admin and admin.phone:
            return admin.phone
    admin = db.query(Admin).filter(Admin.role == AdminRoleEnum.super_admin).first()
    if admin:
        return admin.phone
    return None


