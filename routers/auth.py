from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas.admin import AdminLogin, AdminCreate, AdminResponse
from schemas.auth import Token
from crud import authenticate_admin, get_admin_by_email, create_admin
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
    """Login admin and return JWT token."""
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=AdminResponse)
async def register_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    current_super_admin = Depends(get_current_super_admin)
):
    """Register new admin (super admin only)."""
    db_admin = get_admin_by_email(db, email=admin.email)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return create_admin(db=db, admin=admin)
