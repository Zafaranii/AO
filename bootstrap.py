"""Create the first super admin from environment variables (idempotent)."""
import logging

from decouple import config

from database import SessionLocal
from models import Admin, AdminRoleEnum
from dependencies import get_password_hash

logger = logging.getLogger(__name__)


def bootstrap_super_admin() -> None:
    """Create a super admin from BOOTSTRAP_ADMIN_* env vars if none exists yet."""
    email = config("BOOTSTRAP_ADMIN_EMAIL", default="")
    phone = config("BOOTSTRAP_ADMIN_PHONE", default="")
    password = config("BOOTSTRAP_ADMIN_PASSWORD", default="")
    full_name = config("BOOTSTRAP_ADMIN_NAME", default="Super Admin")
    if not (email and phone and password):
        return

    db = SessionLocal()
    try:
        if db.query(Admin).filter(Admin.role == AdminRoleEnum.super_admin).first():
            return
        db.add(Admin(
            full_name=full_name,
            email=email,
            phone=phone,
            role=AdminRoleEnum.super_admin,
            password=get_password_hash(password),
        ))
        db.commit()
        logger.info("Bootstrap super admin created: %s", email)
    except Exception:
        db.rollback()
        logger.exception("Failed to create bootstrap super admin")
    finally:
        db.close()
