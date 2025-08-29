from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Admin
from schemas.rental_contract import (
    RentalContractCreate, RentalContractUpdate, RentalContractResponse
)
from crud import (
    get_rental_contract, get_rental_contract_by_part, get_rental_contracts,
    create_rental_contract, update_rental_contract, delete_rental_contract
)
from dependencies import get_current_admin_or_super_admin, get_current_super_admin

router = APIRouter(
    prefix="/rental-contracts",
    tags=["rental-contracts"]
)

@router.get("/", response_model=List[RentalContractResponse])
async def list_rental_contracts(
    skip: int = 0,
    limit: int = 100,
    apartment_id: Optional[int] = Query(None, description="Filter by apartment ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get rental contracts (admin only)."""
    contracts = get_rental_contracts(
        db=db,
        apartment_id=apartment_id,
        is_active=is_active,
        skip=skip,
        limit=limit
    )
    return contracts

@router.get("/{contract_id}", response_model=RentalContractResponse)
async def get_rental_contract_by_id(
    contract_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Get rental contract by ID (admin only)."""
    contract = get_rental_contract(db, contract_id=contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="Rental contract not found")
    return contract

@router.post("/", response_model=RentalContractResponse)
async def create_new_rental_contract(
    contract: RentalContractCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Create new rental contract (admin only)."""
    return create_rental_contract(db=db, contract=contract, created_by_admin_id=current_admin.id)

@router.put("/{contract_id}", response_model=RentalContractResponse)
async def update_rental_contract_details(
    contract_id: int,
    contract: RentalContractUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin)
):
    """Update rental contract (admin only)."""
    db_contract = update_rental_contract(db, contract_id=contract_id, contract=contract)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Rental contract not found")
    return db_contract

@router.delete("/{contract_id}", response_model=RentalContractResponse)
async def delete_rental_contract_by_id(
    contract_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin)
):
    """Delete rental contract (super admin only)."""
    db_contract = delete_rental_contract(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Rental contract not found")
    return db_contract
