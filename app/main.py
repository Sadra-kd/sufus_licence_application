import os
import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import uuid
import traceback

from app.api.api import api_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sufuss - Sophos License Server Simulator",
    description="A simulator for Sophos license server API endpoints",
    version="0.2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Mount certificates directory for easier access
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# SFOS 18.5.0 specific catch-all routes at root level
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def catch_all(request: Request, path: str):
    """
    Catch-all endpoint to handle SFOS 18.5.0 specific requests that might not match our defined routes
    """
    logger.info(f"[SFOS 18.5.0] Catch-all received: {request.method} {path}")
    logger.info(f"[SFOS 18.5.0] Headers: {dict(request.headers)}")
    
    # Attempt to read and log request body
    body_content = ""
    try:
        body = await request.body()
        if body:
            body_content = body.decode('utf-8', errors='ignore')
            logger.info(f"[SFOS 18.5.0] Body: {body_content}")
            try:
                json_body = json.loads(body_content)
            except:
                json_body = {}
    except Exception as e:
        logger.error(f"[SFOS 18.5.0] Error reading request body: {e}")
        json_body = {}
    
    # Special handling for common SFOS 18.5.0 requests
    if path.startswith("licensing/v1/installations") or path.startswith("licensing/installations"):
        return handle_licensing_installations(path, json_body)
    
    if path.startswith("endpoint-security/v1"):
        return handle_endpoint_security(path, json_body)
        
    if path.startswith("central/") or path.startswith("central/v1/"):
        return handle_central(path, json_body)
        
    if path.startswith("api/") or path.startswith("api/v1/"):
        return handle_api(path, json_body)
        
    if path.startswith("services/") or path.startswith("services/v1/"):
        return handle_services(path, json_body)
        
    if "download" in path or "update" in path or "firmware" in path:
        return handle_downloads(path, json_body)
        
    if "auth" in path or "token" in path or "login" in path:
        return handle_auth(path, json_body)
    
    # Default license response for any unknown path
    logger.info(f"[SFOS 18.5.0] Generating default response for {path}")
    response = {
        "status": "registered",
        "licensed": True,
        "expiryDate": (datetime.utcnow() + timedelta(days=3650)).isoformat(),
        "installationId": str(uuid.uuid4()),
        "message": "License is valid"
    }
    
    return JSONResponse(content=response)

def handle_licensing_installations(path: str, body: dict = None):
    """Handle licensing installation requests"""
    logger.info(f"[SFOS 18.5.0] Handling licensing installation: {path}")
    
    # Specific handling for different licensing path patterns
    if "register" in path:
        logger.info("[SFOS 18.5.0] Processing registration request")
        response = {
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
    elif "features" in path:
        logger.info("[SFOS 18.5.0] Processing features request")
        response = {
            "features": [
                {"name": "Base Firewall", "status": "registered"},
                {"name": "Network Protection", "status": "registered"},
                {"name": "Web Protection", "status": "registered"},
                {"name": "Email Protection", "status": "registered"},
                {"name": "Web Server Protection", "status": "registered"},
                {"name": "Sandstorm", "status": "registered"}
            ]
        }
    else:
        # Default installation list response
        logger.info("[SFOS 18.5.0] Sending default installation list")
        response = {
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
    
    return JSONResponse(content=response)

def handle_endpoint_security(path: str, body: dict = None):
    """Handle endpoint security requests"""
    logger.info(f"[SFOS 18.5.0] Handling endpoint security: {path}")
    response = {
        "status": "active",
        "licensed": True,
        "features": [
            {"name": "Endpoint Protection", "status": "registered"},
            {"name": "Endpoint Detection and Response", "status": "registered"}
        ]
    }
    return JSONResponse(content=response)

def handle_central(path: str, body: dict = None):
    """Handle central management requests"""
    logger.info(f"[SFOS 18.5.0] Handling central management: {path}")
    response = {
        "status": "connected",
        "account": {
            "id": str(uuid.uuid4()),
            "name": "Sufuss Test Account"
        },
        "tenant": {
            "id": str(uuid.uuid4()),
            "name": "Sufuss Tenant"
        }
    }
    return JSONResponse(content=response)

def handle_api(path: str, body: dict = None):
    """Handle API requests"""
    logger.info(f"[SFOS 18.5.0] Handling API request: {path}")
    response = {
        "status": "success",
        "message": "API request processed successfully"
    }
    return JSONResponse(content=response)

def handle_services(path: str, body: dict = None):
    """Handle services requests"""
    logger.info(f"[SFOS 18.5.0] Handling services request: {path}")
    response = {
        "services": [
            {"name": "update", "status": "active"},
            {"name": "central", "status": "active"},
            {"name": "licensing", "status": "active"}
        ]
    }
    return JSONResponse(content=response)

def handle_downloads(path: str, body: dict = None):
    """Handle download requests"""
    logger.info(f"[SFOS 18.5.0] Handling download request: {path}")
    response = {
        "status": "success",
        "url": "https://download.example.com/dummy",
        "message": "Download available"
    }
    return JSONResponse(content=response)

def handle_auth(path: str, body: dict = None):
    """Handle authentication requests"""
    logger.info(f"[SFOS 18.5.0] Handling auth request: {path}")
    response = {
        "token": f"dummy-token-{str(uuid.uuid4())}",
        "expires_in": 3600,
        "token_type": "Bearer"
    }
    return JSONResponse(content=response)

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint to check if the server is running.
    """
    return {
        "message": "Welcome to Sufuss - Sophos License Server Simulator",
        "version": "0.2.0",
        "status": "running"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "version": "0.2.0"
    }

# Serve certificate files at a URL that's easier to access
@app.get("/certificates/ca", tags=["certificates"])
async def get_ca_certificate():
    """
    Serve the CA certificate file for easy download
    """
    cert_path = "./app/certificates/ca.crt"
    if os.path.exists(cert_path):
        with open(cert_path, "rb") as f:
            content = f.read()
        return Response(content=content, media_type="application/x-x509-ca-cert", headers={
            "Content-Disposition": "attachment; filename=sufuss-ca.crt"
        })
    return {"error": "Certificate not found"}


# Error handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle any unhandled exceptions.
    """
    logger.error(f"[ERROR] Unhandled exception: {str(exc)}")
    logger.error(f"[ERROR] Request path: {request.url.path}")
    logger.error(f"[ERROR] Stack trace: {traceback.format_exc()}")
    
    try:
        # Try to read body, if any
        body = await request.body()
        if body:
            logger.error(f"[ERROR] Request body: {body.decode('utf-8', errors='ignore')}")
    except Exception:
        pass
    
    # For SFOS 18.5.0, always try to return a successful license response
    if any(keyword in request.url.path.lower() for keyword in ["license", "installations", "validate", "sync"]):
        logger.info(f"[RECOVERY] Generating license success response for failed request: {request.url.path}")
        return JSONResponse(
            status_code=200,
            content={
                "status": "registered",
                "licensed": True,
                "expiryDate": (datetime.utcnow() + timedelta(days=3650)).isoformat(),
                "message": "License is valid",
                "features": [
                    {"name": "Base Firewall", "status": "registered"},
                    {"name": "Network Protection", "status": "registered"},
                    {"name": "Web Protection", "status": "registered"},
                    {"name": "Email Protection", "status": "registered"},
                    {"name": "Web Server Protection", "status": "registered"},
                    {"name": "Sandstorm", "status": "registered"}
                ]
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please check the logs for more details."}
    )


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    ssl_enabled = os.getenv("SSL_ENABLED", "true").lower() == "true"
    
    if ssl_enabled:
        ssl_cert_file = os.getenv("SSL_CERT_FILE", "./app/certificates/server.crt")
        ssl_key_file = os.getenv("SSL_KEY_FILE", "./app/certificates/server.key")
        
        logger.info(f"Starting server with SSL on {host}:{port}")
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=True,
            ssl_certfile=ssl_cert_file,
            ssl_keyfile=ssl_key_file
        )
    else:
        logger.info(f"Starting server without SSL on {host}:{port}")
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=True
        ) 