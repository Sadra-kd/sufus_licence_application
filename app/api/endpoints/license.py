from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import uuid
import logging

from app.db.base import get_db
from app.models.license import License
from app.models.device import Device
from app.models.service import Service
from app.schemas.license import (
    LicenseCreate, 
    LicenseResponse, 
    LicenseUpdate, 
    LicenseValidateRequest,
    LicenseValidateResponse,
    LicenseActivateRequest,
    LicenseActivateResponse,
    LicenseStatusRequest,
    LicenseStatusResponse
)
from app.schemas.device import DeviceCreate

router = APIRouter()
logger = logging.getLogger(__name__)

# SFOS 18.5.0 specific endpoints
@router.get("/installations", response_class=Response)
@router.get("/installations/", response_class=Response)
async def get_installations(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    SFOS 18.5.0 installation endpoint
    """
    logger.info(f"SFOS 18.5.0 installation request received: {request.url}")
    
    # Construct a response that SFOS 18.5.0 expects
    sfos_response = {
        "installations": [
            {
                "id": str(uuid.uuid4()),
                "product": "XG Firewall",
                "version": "18.5.0",
                "status": "registered",
                "registrationDate": datetime.utcnow().isoformat(),
                "lastSeenDate": datetime.utcnow().isoformat(),
                "expiryDate": (datetime.utcnow() + timedelta(days=3650)).isoformat(),
                "features": [
                    {"name": "Base Firewall", "status": "registered"},
                    {"name": "Network Protection", "status": "registered"},
                    {"name": "Web Protection", "status": "registered"},
                    {"name": "Email Protection", "status": "registered"},
                    {"name": "Web Server Protection", "status": "registered"},
                    {"name": "Sandstorm", "status": "registered"}
                ]
            }
        ]
    }
    
    response.headers["Content-Type"] = "application/json"
    return Response(content=json.dumps(sfos_response), media_type="application/json")

@router.get("/v1/installations", response_class=Response)
@router.get("/v1/installations/", response_class=Response)
async def get_v1_installations(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    SFOS 18.5.0 v1 installation endpoint
    """
    return await get_installations(request, response, db)

@router.post("/v1/installations/register", response_class=Response)
@router.post("/v1/installations/register/", response_class=Response)
async def register_installation(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    SFOS 18.5.0 installation registration endpoint
    """
    logger.info(f"SFOS 18.5.0 installation registration request received: {request.url}")
    
    # Parse the request body
    try:
        body = await request.json()
        logger.info(f"Registration request body: {body}")
    except Exception as e:
        logger.error(f"Failed to parse request body: {e}")
        body = {}
    
    # Construct registration response
    sfos_response = {
        "id": str(uuid.uuid4()),
        "registrationDate": datetime.utcnow().isoformat(),
        "lastSeenDate": datetime.utcnow().isoformat(),
        "expiryDate": (datetime.utcnow() + timedelta(days=3650)).isoformat(),
        "status": "registered",
        "features": [
            {"name": "Base Firewall", "status": "registered"},
            {"name": "Network Protection", "status": "registered"},
            {"name": "Web Protection", "status": "registered"},
            {"name": "Email Protection", "status": "registered"},
            {"name": "Web Server Protection", "status": "registered"},
            {"name": "Sandstorm", "status": "registered"}
        ]
    }
    
    # Try to extract device info and save to database
    try:
        if 'deviceId' in body:
            device_id = body['deviceId']
            license = db.query(License).filter(License.is_active == True).first()
            
            if license and device_id:
                # Check if device already exists
                device = db.query(Device).filter(Device.device_id == device_id).first()
                
                if not device and license:
                    # Create a new device entry
                    device = Device(
                        device_id=device_id,
                        name=body.get('hostname', 'SFOS Device'),
                        device_type="firewall",
                        model=body.get('model', 'XG Firewall'),
                        firmware_version=body.get('version', '18.5.0'),
                        ip_address=request.client.host,
                        license_id=license.id,
                        last_seen=datetime.utcnow()
                    )
                    db.add(device)
                    db.commit()
                    logger.info(f"Registered new device: {device_id}")
    except Exception as e:
        logger.error(f"Error saving device information: {e}")
    
    response.headers["Content-Type"] = "application/json"
    return Response(content=json.dumps(sfos_response), media_type="application/json")

@router.post("/v1/installations/{installation_id}/features/refresh", response_class=Response)
@router.put("/v1/installations/{installation_id}/features", response_class=Response)
async def refresh_features(
    installation_id: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    SFOS 18.5.0 feature refresh endpoint
    """
    logger.info(f"SFOS 18.5.0 feature refresh request received: {request.url}")
    
    # Construct feature refresh response
    sfos_response = {
        "features": [
            {"name": "Base Firewall", "status": "registered"},
            {"name": "Network Protection", "status": "registered"},
            {"name": "Web Protection", "status": "registered"},
            {"name": "Email Protection", "status": "registered"},
            {"name": "Web Server Protection", "status": "registered"},
            {"name": "Sandstorm", "status": "registered"}
        ]
    }
    
    response.headers["Content-Type"] = "application/json"
    return Response(content=json.dumps(sfos_response), media_type="application/json")

@router.post("/v1/installations/{installation_id}/heartbeat", response_class=Response)
async def installation_heartbeat(
    installation_id: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    SFOS 18.5.0 heartbeat endpoint
    """
    logger.info(f"SFOS 18.5.0 heartbeat request received: {request.url}")
    
    # Update device last seen time
    try:
        body = await request.json()
        if 'deviceId' in body:
            device_id = body['deviceId']
            device = db.query(Device).filter(Device.device_id == device_id).first()
            if device:
                device.last_seen = datetime.utcnow()
                db.commit()
                logger.info(f"Updated last seen for device: {device_id}")
    except Exception as e:
        logger.error(f"Error updating device last seen time: {e}")
    
    # Empty response with 200 OK is sufficient
    return Response()

# Original endpoints - keep these intact
@router.post("/validate", response_model=LicenseValidateResponse)
def validate_license(
    request: LicenseValidateRequest,
    db: Session = Depends(get_db)
):
    """
    Validate a license key for a specific device.
    This endpoint simulates the Sophos license validation process.
    """
    license = db.query(License).filter(License.license_key == request.license_key).first()
    
    if not license:
        return LicenseValidateResponse(
            valid=False,
            message="License key not found"
        )
    
    if not license.is_active:
        return LicenseValidateResponse(
            valid=False,
            license_key=license.license_key,
            status="inactive",
            message="License is inactive"
        )
    
    if license.expiry_date < datetime.utcnow():
        return LicenseValidateResponse(
            valid=False,
            license_key=license.license_key,
            status="expired",
            expiry_date=license.expiry_date,
            message="License has expired"
        )
    
    # Get all services associated with the license
    services = db.query(Service).filter(Service.license_id == license.id).all()
    service_list = [
        {
            "name": service.name,
            "feature_code": service.feature_code,
            "status": service.status,
            "description": service.description
        }
        for service in services
    ]
    
    return LicenseValidateResponse(
        valid=True,
        license_key=license.license_key,
        status=license.status,
        expiry_date=license.expiry_date,
        services=service_list,
        message="License is valid"
    )


@router.post("/activate", response_model=LicenseActivateResponse)
def activate_license(
    request: LicenseActivateRequest,
    db: Session = Depends(get_db)
):
    """
    Activate a license for a specific device.
    This endpoint simulates the Sophos license activation process.
    """
    license = db.query(License).filter(License.license_key == request.license_key).first()
    
    if not license:
        return LicenseActivateResponse(
            success=False,
            message="License key not found"
        )
    
    if not license.is_active:
        return LicenseActivateResponse(
            success=False,
            license_key=license.license_key,
            status="inactive",
            message="License is inactive"
        )
    
    if license.expiry_date < datetime.utcnow():
        return LicenseActivateResponse(
            success=False,
            license_key=license.license_key,
            status="expired",
            expiry_date=license.expiry_date,
            message="License has expired"
        )
    
    # Check if device already exists
    device = db.query(Device).filter(Device.device_id == request.device_id).first()
    
    if not device:
        # Create a new device
        device_data = DeviceCreate(
            device_id=request.device_id,
            name=request.device_name,
            device_type=request.device_type,
            model=request.model,
            firmware_version=request.firmware_version,
            ip_address=request.ip_address,
            license_id=license.id
        )
        
        device = Device(
            device_id=device_data.device_id,
            name=device_data.name,
            device_type=device_data.device_type,
            model=device_data.model,
            firmware_version=device_data.firmware_version,
            ip_address=device_data.ip_address,
            license_id=license.id,
            last_seen=datetime.utcnow()
        )
        
        db.add(device)
        db.commit()
        db.refresh(device)
    else:
        # Update existing device
        device.name = request.device_name or device.name
        device.device_type = request.device_type or device.device_type
        device.model = request.model or device.model
        device.firmware_version = request.firmware_version or device.firmware_version
        device.ip_address = request.ip_address or device.ip_address
        device.last_seen = datetime.utcnow()
        device.license_id = license.id
        device.is_active = True
        
        db.commit()
        db.refresh(device)
    
    # Get all services associated with the license
    services = db.query(Service).filter(Service.license_id == license.id).all()
    service_list = [
        {
            "name": service.name,
            "feature_code": service.feature_code,
            "status": service.status,
            "description": service.description
        }
        for service in services
    ]
    
    return LicenseActivateResponse(
        success=True,
        license_key=license.license_key,
        status=license.status,
        expiry_date=license.expiry_date,
        services=service_list,
        message="License activated successfully"
    )


@router.post("/status", response_model=LicenseStatusResponse)
def get_license_status(
    request: LicenseStatusRequest,
    db: Session = Depends(get_db)
):
    """
    Get the status of a license for a specific device.
    This endpoint simulates checking the Sophos license status.
    """
    license = db.query(License).filter(License.license_key == request.license_key).first()
    
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License key not found"
        )
    
    # Check if device exists and is associated with this license
    device = db.query(Device).filter(
        Device.device_id == request.device_id,
        Device.license_id == license.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found or not associated with this license"
        )
    
    # Update last seen timestamp
    device.last_seen = datetime.utcnow()
    db.commit()
    
    # Get all services associated with the license
    services = db.query(Service).filter(Service.license_id == license.id).all()
    service_list = [
        {
            "name": service.name,
            "feature_code": service.feature_code,
            "status": service.status,
            "description": service.description
        }
        for service in services
    ]
    
    return LicenseStatusResponse(
        license_key=license.license_key,
        status=license.status,
        expiry_date=license.expiry_date,
        is_active=license.is_active,
        services=service_list
    ) 