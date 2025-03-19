from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    feature_code = Column(String(50), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="running")  # running, stopped, disabled
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    license = relationship("License", back_populates="services") 