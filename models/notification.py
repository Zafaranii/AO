from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from .enums import NotificationStatusEnum


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    rental_contract_id = Column(Integer, ForeignKey("rental_contracts.id"), nullable=False)
    status = Column(Enum(NotificationStatusEnum), nullable=False)
    notify_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    description = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    rental_contract = relationship("RentalContract", back_populates="notifications")
    notify_admin = relationship("Admin", back_populates="notifications")


