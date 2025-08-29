from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Admin, AdminRoleEnum
from schemas.admin import AdminCreate, AdminUpdate, AdminResponse
from crud import get_admins, get_admin, create_admin, update_admin, delete_admin, get_admin_by_email
from dependencies import get_current_super_admin, get_current_admin_or_super_admin

router = APIRouter(
    prefix="/admins",
    tags=["admin-management"]
)

@router.get("/", response_model=List[AdminResponse])
async def list_admins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin)
):
    """Get list of all admins (super admin only)."""
    admins = get_admins(db, skip=skip, limit=limit)
    return admins

@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get current admin's information."""
    return current_admin

@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin_by_id(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin)
):
    """Get admin by ID (super admin only)."""
    admin = get_admin(db, admin_id=admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.post("/", response_model=AdminResponse)
async def create_new_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin)
):
    """Create new admin (super admin only)."""
    db_admin = get_admin_by_email(db, email=admin.email)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return create_admin(db=db, admin=admin)

@router.put("/{admin_id}", response_model=AdminResponse)
async def update_admin_by_id(
    admin_id: int,
    admin: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin)
):
    """Update admin (super admin only)."""
    db_admin = update_admin(db, admin_id=admin_id, admin=admin)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.put("/me", response_model=AdminResponse)
async def update_current_admin(
    admin: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Update current admin's own information."""
    # Remove role from update if not super admin
    if current_admin.role != AdminRoleEnum.super_admin:
        admin.role = None
    
    db_admin = update_admin(db, admin_id=current_admin.id, admin=admin)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.delete("/{admin_id}", response_model=AdminResponse)
async def delete_admin_by_id(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin)
):
    """Delete admin (super admin only)."""
    # Prevent super admin from deleting themselves
    if admin_id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )
    
    db_admin = delete_admin(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin
