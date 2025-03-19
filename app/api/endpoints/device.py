from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.base import get_db
from app.models.device import Device
from app.models.license import License
from app.schemas.device import DeviceRegisterRequest, DeviceRegisterResponse, DeviceResponse

router = APIRouter()


@router.post("/register", response_model=DeviceRegisterResponse)
def register_device(
    request: DeviceRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a device without associating it with a license yet.
    This is useful for initial device setup.
    """
    # Check if device already exists
    device = db.query(Device).filter(Device.device_id == request.device_id).first()
    
    if device:
        return DeviceRegisterResponse(
            success=True,
            device_id=device.device_id,
            message="Device already registered"
        )
    
    # First, check if there's at least one active license
    license = db.query(License).filter(License.is_active == True).first()
    
    if not license:
        return DeviceRegisterResponse(
            success=False,
            message="No active license available for device registration"
        )
    
    # Create a new device with the first available license
    device = Device(
        device_id=request.device_id,
        name=request.name,
        device_type=request.device_type,
        model=request.model,
        firmware_version=request.firmware_version,
        ip_address=request.ip_address,
        license_id=license.id,
        last_seen=datetime.utcnow()
    )
    
    db.add(device)
    db.commit()
    db.refresh(device)
    
    return DeviceRegisterResponse(
        success=True,
        device_id=device.device_id,
        message="Device registered successfully"
    )


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: str,
    db: Session = Depends(get_db)
):
    """
    Get device information by device ID.
    """
    device = db.query(Device).filter(Device.device_id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return device


@router.get("/", response_model=List[DeviceResponse])
def list_devices(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    List all registered devices.
    """
    devices = db.query(Device).offset(skip).limit(limit).all()
    return devices 