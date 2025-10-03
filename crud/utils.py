from typing import Optional

from sqlalchemy.orm import Session

from models import Admin, AdminRoleEnum


def get_admin_phone_for_whatsapp(db: Session, admin_id: int) -> Optional[str]:
    """Get admin phone number for WhatsApp link generation."""
    admin = db.query(Admin).filter(Admin.role == AdminRoleEnum.super_admin).first()
    if admin:
        return admin.phone
    return None


