from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="registered")
    issue_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    devices = relationship("Device", back_populates="license", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="license", cascade="all, delete-orphan") 