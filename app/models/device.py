from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    device_type = Column(String(50), nullable=False, default="physical")  # physical or virtual
    model = Column(String(100), nullable=True)
    firmware_version = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)
    last_seen = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    license = relationship("License", back_populates="devices") 