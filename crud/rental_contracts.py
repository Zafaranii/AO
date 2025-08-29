from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import RentalContract
from schemas.rental_contract import RentalContractCreate, RentalContractUpdate


def get_rental_contract(db: Session, contract_id: int):
    return db.query(RentalContract).filter(RentalContract.id == contract_id).first()


def get_rental_contract_by_part(db: Session, apartment_part_id: int):
    return db.query(RentalContract).filter(RentalContract.apartment_part_id == apartment_part_id).first()


def get_rental_contracts(
    db: Session,
    apartment_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(RentalContract)
    if apartment_id:
        query = query.join(RentalContract.apartment_part).filter(
            RentalContract.apartment_part.has(apartment_id=apartment_id)
        )
    if is_active is not None:
        query = query.filter(RentalContract.is_active == is_active)
    return query.offset(skip).limit(limit).all()


def create_rental_contract(db: Session, contract: RentalContractCreate, created_by_admin_id: int):
    # Create the rental contract
    db_contract = RentalContract(**contract.dict(), created_by_admin_id=created_by_admin_id)
    db.add(db_contract)
    
    # Update the apartment part status to 'rented'
    from models import ApartmentPart, PartStatusEnum
    apartment_part = db.query(ApartmentPart).filter(ApartmentPart.id == contract.apartment_part_id).first()
    if apartment_part:
        apartment_part.status = PartStatusEnum.rented
    
    db.commit()
    db.refresh(db_contract)
    return db_contract


def update_rental_contract(db: Session, contract_id: int, contract: RentalContractUpdate):
    db_contract = db.query(RentalContract).filter(RentalContract.id == contract_id).first()
    if db_contract:
        update_data = contract.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contract, field, value)
        db.commit()
        db.refresh(db_contract)
    return db_contract


def delete_rental_contract(db: Session, contract_id: int):
    db_contract = db.query(RentalContract).filter(RentalContract.id == contract_id).first()
    if db_contract:
        # Update the apartment part status back to 'available'
        from models import ApartmentPart, PartStatusEnum
        apartment_part = db.query(ApartmentPart).filter(ApartmentPart.id == db_contract.apartment_part_id).first()
        if apartment_part:
            apartment_part.status = PartStatusEnum.available
        
        db.delete(db_contract)
        db.commit()
    return db_contract


def get_expiring_contracts(db: Session, days_ahead: int = 30):
    """Get rental contracts expiring within specified days."""
    from datetime import date, timedelta
    expiry_date = date.today() + timedelta(days=days_ahead)
    return db.query(RentalContract).filter(
        and_(
            RentalContract.contract_end_date <= expiry_date,
            RentalContract.contract_end_date >= date.today(),
            RentalContract.is_active == True
        )
    ).all()
