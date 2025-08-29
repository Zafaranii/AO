from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class RentalContract(Base):
    __tablename__ = "rental_contracts"

    id = Column(Integer, primary_key=True, index=True)
    apartment_part_id = Column(Integer, ForeignKey("apartment_parts.id"), nullable=False, unique=True)
    tenant_name = Column(String(100), nullable=False)
    tenant_phone = Column(String(20), nullable=False)
    contract_start_date = Column(Date, nullable=False)
    contract_end_date = Column(Date, nullable=False)
    rent_value = Column(Numeric(10, 2), nullable=False)
    id_card_scan_url = Column(String(500), nullable=True)
    contract_scan_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_by_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    apartment_part = relationship("ApartmentPart", back_populates="rental_contract")
    created_by_admin = relationship("Admin")
    notifications = relationship("Notification", back_populates="rental_contract", cascade="all, delete-orphan")
