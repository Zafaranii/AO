from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas.admin import AdminCreate, AdminResponse, MasterAdminCreate, MasterAdminCreateData
from schemas.auth import Token
from crud import authenticate_admin, get_admin_by_email, get_admin_by_phone, create_admin
from dependencies import (
    create_access_token, get_current_super_admin, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/login", response_model=Token)
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login admin with email or phone and return JWT token."""
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=AdminResponse)
async def register_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    current_super_admin = Depends(get_current_super_admin)
):
    """Register new admin (super admin only)."""
    # Check if email is already registered
    db_admin = get_admin_by_email(db, email=admin.email)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if phone is already registered
    db_admin = get_admin_by_phone(db, phone=admin.phone)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )
    
    return create_admin(db=db, admin=admin)


@router.post("/create-master-admin", response_model=AdminResponse)
async def create_master_admin(
    admin: MasterAdminCreate,
    db: Session = Depends(get_db)
):
    """Create master admin with special password (no authentication required for initial setup)."""
    # Check master password
    MASTER_PASSWORD = "MASTER_ADMIN_SETUP_2024"  # You can change this or make it configurable
    
    if admin.master_password != MASTER_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid master password"
        )
    
    # Check if any super admin already exists
    from models import Admin, AdminRoleEnum
    existing_super_admin = db.query(Admin).filter(Admin.role == AdminRoleEnum.super_admin).first()
    if existing_super_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Master admin already exists. Use regular admin creation instead."
        )
    
    # Check if email is already registered
    db_admin = get_admin_by_email(db, email=admin.email)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if phone is already registered
    db_admin = get_admin_by_phone(db, phone=admin.phone)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )
    
    # Create admin with super_admin role
    admin_data = MasterAdminCreateData(
        full_name=admin.full_name,
        email=admin.email,
        phone=admin.phone,
        password=admin.password,
        role="super_admin"  # Force super_admin role
    )
    
    return create_admin(db=db, admin=admin_data)
