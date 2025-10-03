from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import urllib.parse

from database import get_db
from models import Admin
from schemas.apartment_sale import (
    ApartmentSaleCreate, ApartmentSaleUpdate, ApartmentSaleResponse
)
from schemas.apartment_rent import (
    ApartmentRentCreate, ApartmentRentUpdate, ApartmentRentResponse, ApartmentRentWithParts, AdminOwnContentResponse
)
from schemas.apartment_part import (
    ApartmentPartCreate, ApartmentPartUpdate, ApartmentPartResponse
)
from schemas.auth import WhatsAppLinkResponse
from crud import (
    get_admin_phone_for_whatsapp,
    get_apartments_rent,
    get_apartment_rent,
    create_apartment_rent,
    update_apartment_rent,
    delete_apartment_rent,
    get_apartments_rent_by_admin,
    get_apartments_with_parts_by_admin,
    get_apartment_parts,
    get_apartment_part,
    create_apartment_part,
    update_apartment_part,
    delete_apartment_part,
    get_apartments_sale,
    get_apartment_sale,
    create_apartment_sale,
    update_apartment_sale,
    delete_apartment_sale,
    get_apartments_sale_by_admin,
)
from dependencies import get_current_admin_or_super_admin, get_current_super_admin

router = APIRouter(prefix="/apartments", tags=["apartments"])

# ----- Sale apartments -----
@router.get("/sale", response_model=List[ApartmentSaleResponse])
async def list_apartments_sale(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_apartments_sale(db, skip=skip, limit=limit)

@router.get("/sale/{apartment_id}", response_model=ApartmentSaleResponse)
async def get_apartment_sale_details(apartment_id: int, db: Session = Depends(get_db)):
    apartment = get_apartment_sale(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment

@router.post("/sale", response_model=ApartmentSaleResponse)
async def create_apartment_sale_endpoint(
    apartment: ApartmentSaleCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    return create_apartment_sale(db=db, apartment=apartment, admin_id=current_admin.id, admin_phone=current_admin.phone)

@router.put("/sale/{apartment_id}", response_model=ApartmentSaleResponse)
async def update_apartment_sale(
    apartment_id: int,
    apartment: ApartmentSaleUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    try:
        db_apartment = update_apartment_sale(
            db, 
            apartment_id=apartment_id, 
            apartment=apartment,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_apartment is None:
            raise HTTPException(status_code=404, detail="Apartment not found")
        return db_apartment
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/sale/{apartment_id}", response_model=ApartmentSaleResponse)
async def delete_apartment_sale(
    apartment_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    try:
        db_apartment = delete_apartment_sale(
            db, 
            apartment_id=apartment_id,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_apartment is None:
            raise HTTPException(status_code=404, detail="Apartment not found")
        return db_apartment
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

# ----- Rent (father) apartments -----
@router.get("/rent", response_model=List[ApartmentRentResponse])
async def list_apartments_rent(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_apartments_rent(db, skip=skip, limit=limit)

@router.get("/rent/{apartment_id}", response_model=ApartmentRentWithParts)
async def get_apartment_rent_details(apartment_id: int, db: Session = Depends(get_db)):
    apartment = get_apartment_rent(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment

@router.post("/rent", response_model=ApartmentRentResponse)
async def create_apartment_rent_endpoint(
    apartment: ApartmentRentCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    return create_apartment_rent(db=db, apartment=apartment, listed_by_admin_id=current_admin.id, admin_phone=current_admin.phone)

@router.put("/rent/{apartment_id}", response_model=ApartmentRentResponse)
async def update_apartment_rent_endpoint(
    apartment_id: int,
    apartment: ApartmentRentUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    try:
        db_apartment = update_apartment_rent(
            db, 
            apartment_id=apartment_id, 
            apartment=apartment,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_apartment is None:
            raise HTTPException(status_code=404, detail="Apartment not found")
        return db_apartment
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/rent/{apartment_id}", response_model=ApartmentRentResponse)
async def delete_apartment_rent_endpoint(
    apartment_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    try:
        db_apartment = delete_apartment_rent(
            db, 
            apartment_id=apartment_id,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_apartment is None:
            raise HTTPException(status_code=404, detail="Apartment not found")
        return db_apartment
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

# Apartment Parts endpoints (under rent father apartment)
@router.get("/rent/{apartment_id}/parts", response_model=List[ApartmentPartResponse])
async def list_apartment_parts(
    apartment_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    apartment = get_apartment_rent(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    parts = get_apartment_parts(db, apartment_id=apartment_id, skip=skip, limit=limit)
    return parts

@router.post("/rent/{apartment_id}/parts", response_model=ApartmentPartResponse)
async def create_apartment_part_for_apartment(
    apartment_id: int,
    part: ApartmentPartCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Create apartment part (admin only). Master admin can create parts for any apartment, regular admins can only create parts for apartments they created."""
    apartment = get_apartment_rent(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    
    try:
        return create_apartment_part(
            db=db, 
            part=part, 
            admin_id=current_admin.id, 
            apartment_id=apartment_id,
            current_admin_role=current_admin.role.value
        )
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.put("/rent/{apartment_id}/parts/{part_id}", response_model=ApartmentPartResponse)
async def update_apartment_part_details(
    apartment_id: int,
    part_id: int,
    part: ApartmentPartUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Update apartment part (admin only). Master admin can update parts for any apartment, regular admins can only update parts for apartments they created."""
    apartment = get_apartment_rent(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    
    try:
        db_part = update_apartment_part(
            db, 
            part_id=part_id, 
            part=part,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_part is None:
            raise HTTPException(status_code=404, detail="Apartment part not found")
        
        # Verify part belongs to apartment
        if db_part.apartment_id != apartment_id:
            raise HTTPException(
                status_code=400, 
                detail="Apartment part does not belong to specified apartment"
            )
        
        return db_part
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/rent/{apartment_id}/parts/{part_id}", response_model=ApartmentPartResponse)
async def delete_apartment_part_by_id(
    apartment_id: int,
    part_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Delete apartment part (admin only). Master admin can delete parts for any apartment, regular admins can only delete parts for apartments they created."""
    apartment = get_apartment_rent(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    
    try:
        db_part = delete_apartment_part(
            db, 
            part_id=part_id,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_part is None:
            raise HTTPException(status_code=404, detail="Apartment part not found")
        
        return db_part
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/rent/{apartment_id}/whatsapp", response_model=WhatsAppLinkResponse)
async def get_whatsapp_contact(
    apartment_id: int,
    db: Session = Depends(get_db)
):
    """Get WhatsApp contact link for apartment inquiry (accessible by guests)."""
    apartment = get_apartment_rent(db, apartment_id=apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    
    admin_phone = get_admin_phone_for_whatsapp(db)
    if not admin_phone:
        raise HTTPException(status_code=500, detail="No admin contact available")
    
    # Clean phone number (remove any non-digits except +)
    clean_phone = ''.join(c for c in admin_phone if c.isdigit() or c == '+')
    
    # Create WhatsApp message
    # message = f"Hello! I'm interested in the apartment: {apartment.name} located at {apartment.location}. Could you please provide more information?"
    # encoded_message = urllib.parse.quote(message)
    # whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_message}"
    
    return {
        "admin_phone": admin_phone
    }

@router.get("/parts", response_model=List[ApartmentPartResponse])
async def list_all_apartment_parts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all apartment parts across all apartments."""
    return get_apartment_parts(db, apartment_id=None, skip=skip, limit=limit)

@router.get("/parts/{part_id}", response_model=ApartmentPartResponse)
async def get_apartment_part_details(part_id: int, db: Session = Depends(get_db)):
    """Get specific apartment part by ID."""
    part = get_apartment_part(db, part_id=part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Apartment part not found")
    return part

@router.put("/parts/{part_id}", response_model=ApartmentPartResponse)
async def update_apartment_part_direct(
    part_id: int,
    part: ApartmentPartUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Update apartment part directly by ID (admin only)."""
    try:
        db_part = update_apartment_part(
            db, 
            part_id=part_id, 
            part=part,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_part is None:
            raise HTTPException(status_code=404, detail="Apartment part not found")
        return db_part
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/parts/{part_id}", response_model=ApartmentPartResponse)
async def delete_apartment_part_direct(
    part_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Delete apartment part directly by ID (admin only)."""
    try:
        db_part = delete_apartment_part(
            db, 
            part_id=part_id,
            current_admin_id=current_admin.id,
            current_admin_role=current_admin.role.value
        )
        if db_part is None:
            raise HTTPException(status_code=404, detail="Apartment part not found")
        return db_part
    except ValueError as e:
        if "Only the admin who created the apartment" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-content", response_model=AdminOwnContentResponse)
async def get_admin_own_content(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get apartments and studios created by the requesting admin. Master admin sees all apartments."""
    # Get rent apartments with their parts
    rent_apartments_data = get_apartments_with_parts_by_admin(db, current_admin.id, current_admin.role.value, skip=skip, limit=limit)
    
    # Get sale apartments
    sale_apartments = get_apartments_sale_by_admin(db, current_admin.id, current_admin.role.value, skip=skip, limit=limit)
    
    # Count total studios
    total_studios = 0
    for apartment in rent_apartments_data:
        total_studios += len(apartment.get("apartment_parts", []))
    
    return AdminOwnContentResponse(
        rent_apartments=rent_apartments_data,
        sale_apartments=sale_apartments,
        total_rent_apartments=len(rent_apartments_data),
        total_sale_apartments=len(sale_apartments),
        total_studios=total_studios
    )
