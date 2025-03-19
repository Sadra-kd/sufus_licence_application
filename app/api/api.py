from fastapi import APIRouter

from app.api.endpoints import license, device

api_router = APIRouter()

# Include license-related endpoints
api_router.include_router(license.router, prefix="/license", tags=["license"])

# Include device-related endpoints
api_router.include_router(device.router, prefix="/device", tags=["device"]) 