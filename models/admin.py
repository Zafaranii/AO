from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from .enums import AdminRoleEnum


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)  # Required for all admins
    phone = Column(String(20), unique=True, nullable=False)  # Required for all admins
    role = Column(Enum(AdminRoleEnum), nullable=False)  # No default, must be specified
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_apartment_parts = relationship("ApartmentPart", back_populates="created_by_admin")


