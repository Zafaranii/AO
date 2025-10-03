from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from .enums import CustomerSourceEnum


class RentalContract(Base):
    __tablename__ = "rental_contracts"

    id = Column(Integer, primary_key=True, index=True)
    apartment_part_id = Column(Integer, ForeignKey("apartment_parts.id"), nullable=False, unique=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_id_number = Column(String(50), nullable=False)
    how_did_customer_find_us = Column(Enum(CustomerSourceEnum), nullable=False)
    paid_deposit = Column(Numeric(10, 2), nullable=False)
    warrant_amount = Column(Numeric(10, 2), nullable=False)
    rent_start_date = Column(Date, nullable=False)
    rent_end_date = Column(Date, nullable=False)
    rent_period = Column(Integer, nullable=False)  # Period in months
    contract_url = Column(String(500), nullable=True)
    customer_id_url = Column(String(500), nullable=True)
    commission = Column(Numeric(10, 2), nullable=False)
    rent_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    created_by_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    apartment_part = relationship("ApartmentPart", back_populates="rental_contract")
    created_by_admin = relationship("Admin")
