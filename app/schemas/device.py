from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DeviceBase(BaseModel):
    device_id: str
    name: Optional[str] = None
    device_type: str = "physical"
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    ip_address: Optional[str] = None


class DeviceCreate(DeviceBase):
    license_id: int


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    ip_address: Optional[str] = None
    is_active: Optional[bool] = None
    last_seen: Optional[datetime] = None


class DeviceResponse(DeviceBase):
    id: int
    license_id: int
    last_seen: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class DeviceRegisterRequest(BaseModel):
    device_id: str
    name: Optional[str] = None
    device_type: str = "physical"
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    ip_address: Optional[str] = None


class DeviceRegisterResponse(BaseModel):
    success: bool
    device_id: Optional[str] = None
    message: Optional[str] = None 