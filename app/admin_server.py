import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.db.base import get_db, engine, Base
from app.models.license import License
from app.models.device import Device
from app.models.service import Service
from app.schemas.license import LicenseCreate, LicenseUpdate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create admin app
app = FastAPI(
    title="Sufuss Admin",
    description="Admin interface for Sufuss - Sophos License Server Simulator",
    version="0.1.0"
)

# Security
security = HTTPBasic()

# Create templates directory if it doesn't exist
os.makedirs("app/templates", exist_ok=True)

# Create static directory if it doesn't exist
os.makedirs("app/static", exist_ok=True)

# Templates configuration
templates = Jinja2Templates(directory="app/templates")

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify the HTTP Basic Auth credentials."""
    is_username_correct = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    is_password_correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username


# Create a placeholder HTML template (minimal for example)
def create_default_template():
    os.makedirs("app/templates", exist_ok=True)
    with open("app/templates/admin.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Sufuss Admin</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .form-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="date"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .button {
            display: inline-block;
            padding: 5px 10px;
            margin: 2px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .button.delete {
            background-color: #f44336;
        }
        .button.edit {
            background-color: #2196F3;
        }
    </style>
</head>
<body>
    <h1>Sufuss Admin</h1>
    
    <div class="form-container">
        <h2>Add New License</h2>
        <form action="/licenses/add" method="post">
            <div class="form-group">
                <label for="license_key">License Key:</label>
                <input type="text" id="license_key" name="license_key" required>
            </div>
            <div class="form-group">
                <label for="description">Description:</label>
                <input type="text" id="description" name="description">
            </div>
            <div class="form-group">
                <label for="status">Status:</label>
                <input type="text" id="status" name="status" value="registered">
            </div>
            <div class="form-group">
                <label for="expiry_date">Expiry Date:</label>
                <input type="date" id="expiry_date" name="expiry_date" required>
            </div>
            <div class="form-group">
                <input type="submit" value="Add License">
            </div>
        </form>
    </div>
    
    <h2>Licenses</h2>
    <table>
        <tr>
            <th>License Key</th>
            <th>Description</th>
            <th>Status</th>
            <th>Issue Date</th>
            <th>Expiry Date</th>
            <th>Active</th>
            <th>Actions</th>
        </tr>
        {% for license in licenses %}
        <tr>
            <td>{{ license.license_key }}</td>
            <td>{{ license.description }}</td>
            <td>{{ license.status }}</td>
            <td>{{ license.issue_date }}</td>
            <td>{{ license.expiry_date }}</td>
            <td>{{ license.is_active }}</td>
            <td>
                <a href="/licenses/{{ license.id }}/edit" class="button edit">Edit</a>
                <a href="/licenses/{{ license.id }}/delete" class="button delete" onclick="return confirm('Are you sure you want to delete this license?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    
    <h2>Registered Devices</h2>
    <table>
        <tr>
            <th>Device ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>License Key</th>
            <th>Last Seen</th>
            <th>Active</th>
        </tr>
        {% for device in devices %}
        <tr>
            <td>{{ device.device_id }}</td>
            <td>{{ device.name }}</td>
            <td>{{ device.device_type }}</td>
            <td>{{ device.license.license_key }}</td>
            <td>{{ device.last_seen }}</td>
            <td>{{ device.is_active }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
        """)
    
    logger.info("Created default admin template")


@app.on_event("startup")
async def startup():
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create default template
    create_default_template()
    
    logger.info("Admin server started")


@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request, 
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db)
):
    # Get all licenses
    licenses = db.query(License).all()
    
    # Get all devices with license information
    devices = db.query(Device).all()
    
    return templates.TemplateResponse(
        "admin.html", 
        {"request": request, "licenses": licenses, "devices": devices}
    )


@app.post("/licenses/add")
async def add_license(
    username: str = Depends(verify_credentials),
    license_key: str = Form(...),
    description: str = Form(None),
    status: str = Form("registered"),
    expiry_date: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if license already exists
    existing_license = db.query(License).filter(License.license_key == license_key).first()
    if existing_license:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="License key already exists"
        )
    
    # Convert expiry_date string to datetime
    try:
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid expiry date format. Use YYYY-MM-DD."
        )
    
    # Create new license
    new_license = License(
        license_key=license_key,
        description=description,
        status=status,
        expiry_date=expiry_date
    )
    
    db.add(new_license)
    db.commit()
    db.refresh(new_license)
    
    # Create default services for this license
    default_services = [
        {"name": "Firewall", "feature_code": "FW", "description": "Sophos Firewall Service"},
        {"name": "IPS", "feature_code": "IPS", "description": "Intrusion Prevention System"},
        {"name": "VPN", "feature_code": "VPN", "description": "Virtual Private Network"},
        {"name": "WAF", "feature_code": "WAF", "description": "Web Application Firewall"},
        {"name": "Sandstorm", "feature_code": "SAND", "description": "Advanced Threat Protection"},
        {"name": "Email", "feature_code": "MAIL", "description": "Email Protection"}
    ]
    
    for service_data in default_services:
        service = Service(
            **service_data,
            status="running",
            license_id=new_license.id
        )
        db.add(service)
    
    db.commit()
    
    # Redirect back to the admin dashboard
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/licenses/{license_id}/delete")
async def delete_license(
    license_id: int,
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db)
):
    # Get the license
    license = db.query(License).filter(License.id == license_id).first()
    
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Delete the license (cascading delete will remove associated services and devices)
    db.delete(license)
    db.commit()
    
    # Redirect back to the admin dashboard
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/licenses/{license_id}/edit", response_class=HTMLResponse)
async def edit_license_form(
    license_id: int,
    request: Request,
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db)
):
    # Get the license
    license = db.query(License).filter(License.id == license_id).first()
    
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Create a simple edit form (since we don't have a dedicated template)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit License</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            h1 {{
                color: #333;
            }}
            .form-container {{
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin-top: 20px;
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }}
            input[type="text"], input[type="date"], select {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            input[type="submit"] {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            input[type="submit"]:hover {{
                background-color: #45a049;
            }}
            a {{
                display: inline-block;
                margin-top: 10px;
                color: #2196F3;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>Edit License</h1>
        
        <div class="form-container">
            <form action="/licenses/{license_id}/update" method="post">
                <div class="form-group">
                    <label for="license_key">License Key:</label>
                    <input type="text" id="license_key" name="license_key" value="{license.license_key}" required>
                </div>
                <div class="form-group">
                    <label for="description">Description:</label>
                    <input type="text" id="description" name="description" value="{license.description or ''}">
                </div>
                <div class="form-group">
                    <label for="status">Status:</label>
                    <input type="text" id="status" name="status" value="{license.status}">
                </div>
                <div class="form-group">
                    <label for="expiry_date">Expiry Date:</label>
                    <input type="date" id="expiry_date" name="expiry_date" value="{license.expiry_date.strftime('%Y-%m-%d')}" required>
                </div>
                <div class="form-group">
                    <label for="is_active">Active:</label>
                    <select id="is_active" name="is_active">
                        <option value="true" {'selected' if license.is_active else ''}>Yes</option>
                        <option value="false" {'selected' if not license.is_active else ''}>No</option>
                    </select>
                </div>
                <div class="form-group">
                    <input type="submit" value="Update License">
                </div>
            </form>
            
            <a href="/">Back to Dashboard</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


@app.post("/licenses/{license_id}/update")
async def update_license(
    license_id: int,
    username: str = Depends(verify_credentials),
    license_key: str = Form(...),
    description: str = Form(None),
    status: str = Form("registered"),
    expiry_date: str = Form(...),
    is_active: str = Form("true"),
    db: Session = Depends(get_db)
):
    # Get the license
    license = db.query(License).filter(License.id == license_id).first()
    
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Check if license key is being changed and if it already exists
    if license_key != license.license_key:
        existing_license = db.query(License).filter(License.license_key == license_key).first()
        if existing_license:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="License key already exists"
            )
    
    # Convert expiry_date string to datetime
    try:
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid expiry date format. Use YYYY-MM-DD."
        )
    
    # Convert is_active string to boolean
    is_active_bool = is_active.lower() == "true"
    
    # Update license
    license.license_key = license_key
    license.description = description
    license.status = status
    license.expiry_date = expiry_date
    license.is_active = is_active_bool
    license.updated_at = datetime.utcnow()
    
    db.commit()
    
    # Redirect back to the admin dashboard
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("ADMIN_HOST", "127.0.0.1")
    port = int(os.getenv("ADMIN_PORT", "8001"))
    
    logger.info(f"Starting admin server on {host}:{port}")
    uvicorn.run(
        "app.admin_server:app",
        host=host,
        port=port,
        reload=True
    ) 