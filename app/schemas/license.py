from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ServiceBase(BaseModel):
    name: str
    feature_code: str
    status: str = "running"
    description: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    license_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class LicenseBase(BaseModel):
    license_key: str
    description: Optional[str] = None
    status: str = "registered"
    expiry_date: datetime


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class LicenseResponse(LicenseBase):
    id: int
    issue_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    services: List[ServiceResponse] = []
    
    class Config:
        orm_mode = True


class LicenseValidateRequest(BaseModel):
    license_key: str
    device_id: str


class LicenseValidateResponse(BaseModel):
    valid: bool
    license_key: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    services: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None


class LicenseActivateRequest(BaseModel):
    license_key: str
    device_id: str
    device_name: Optional[str] = None
    device_type: str = "physical"
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    ip_address: Optional[str] = None


class LicenseActivateResponse(BaseModel):
    success: bool
    license_key: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    services: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None


class LicenseStatusRequest(BaseModel):
    license_key: str
    device_id: str


class LicenseStatusResponse(BaseModel):
    license_key: str
    status: str
    expiry_date: datetime
    is_active: bool
    services: List[Dict[str, Any]] 