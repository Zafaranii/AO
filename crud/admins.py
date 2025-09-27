from sqlalchemy.orm import Session

from models import Admin
from schemas.admin import AdminCreate, AdminUpdate
from dependencies import get_password_hash


def get_admin(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


def get_admin_by_phone(db: Session, phone: str):
    return db.query(Admin).filter(Admin.phone == phone).first()


def get_admin_by_username(db: Session, username: str):
    """Get admin by email or phone."""
    # Try email first
    admin = get_admin_by_email(db, username)
    if admin:
        return admin
    # Try phone
    return get_admin_by_phone(db, username)


def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Admin).offset(skip).limit(limit).all()


def create_admin(db: Session, admin: AdminCreate):
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        full_name=admin.full_name,
        email=admin.email,
        phone=admin.phone,
        role=admin.role,
        password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def update_admin(db: Session, admin_id: int, admin: AdminUpdate):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if db_admin:
        update_data = admin.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
        for field, value in update_data.items():
            setattr(db_admin, field, value)
        db.commit()
        db.refresh(db_admin)
    return db_admin


def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
    return db_admin


def authenticate_admin(db: Session, username: str, password: str):
    """Authenticate admin by email or phone and password."""
    from dependencies import verify_password
    admin = get_admin_by_username(db, username)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin


def verify_admin_password(db: Session, admin_id: int, password: str):
    """Verify admin's current password."""
    from dependencies import verify_password
    admin = get_admin(db, admin_id)
    if not admin:
        return False
    return verify_password(password, admin.password)


def update_admin_email(db: Session, admin_id: int, new_email: str):
    """Update admin's email address."""
    admin = get_admin(db, admin_id)
    if not admin:
        return None
    
    # Check if new email is already taken by another admin
    existing_admin = get_admin_by_email(db, new_email)
    if existing_admin and existing_admin.id != admin_id:
        return None
    
    admin.email = new_email
    db.commit()
    db.refresh(admin)
    return admin


def update_admin_password(db: Session, admin_id: int, new_password: str):
    """Update admin's password."""
    from dependencies import get_password_hash
    admin = get_admin(db, admin_id)
    if not admin:
        return None
    
    admin.password = get_password_hash(new_password)
    db.commit()
    db.refresh(admin)
    return admin



