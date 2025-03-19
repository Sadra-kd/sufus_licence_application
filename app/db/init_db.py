import logging
from sqlalchemy.exc import ProgrammingError
from app.db.base import engine, Base
from app.models.license import License
from app.models.device import Device
from app.models.service import Service
from app.db.base import SessionLocal
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_LICENSE_DURATION_DAYS = int(os.getenv("DEFAULT_LICENSE_DURATION_DAYS", "365"))
DEFAULT_LICENSE_STATUS = os.getenv("DEFAULT_LICENSE_STATUS", "registered")
DEFAULT_SERVICE_STATUS = os.getenv("DEFAULT_SERVICE_STATUS", "running")

# List of default services to create
DEFAULT_SERVICES = [
    {"name": "Firewall", "feature_code": "FW", "description": "Sophos Firewall Service"},
    {"name": "IPS", "feature_code": "IPS", "description": "Intrusion Prevention System"},
    {"name": "VPN", "feature_code": "VPN", "description": "Virtual Private Network"},
    {"name": "WAF", "feature_code": "WAF", "description": "Web Application Firewall"},
    {"name": "Sandstorm", "feature_code": "SAND", "description": "Advanced Threat Protection"},
    {"name": "Email", "feature_code": "MAIL", "description": "Email Protection"}
]

# Sample license to create
SAMPLE_LICENSE = {
    "license_key": "SUFUSS-XXXX-YYYY-ZZZZ-DEMO1",
    "description": "Demo License",
    "status": DEFAULT_LICENSE_STATUS,
    "expiry_date": datetime.now() + timedelta(days=DEFAULT_LICENSE_DURATION_DAYS)
}


def init_db() -> None:
    """Initialize the database with tables and sample data."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Created database tables")
        
        # Check if database already has data
        db = SessionLocal()
        license_count = db.query(License).count()
        
        if license_count == 0:
            # Create sample data
            # 1. Create a sample license
            sample_license = License(**SAMPLE_LICENSE)
            db.add(sample_license)
            db.commit()
            db.refresh(sample_license)
            logger.info(f"Created sample license: {sample_license.license_key}")
            
            # 2. Create default services
            for service_data in DEFAULT_SERVICES:
                service = Service(
                    **service_data,
                    status=DEFAULT_SERVICE_STATUS,
                    license_id=sample_license.id
                )
                db.add(service)
            
            db.commit()
            logger.info(f"Created {len(DEFAULT_SERVICES)} default services")
            
            logger.info("Database initialized with sample data")
        else:
            logger.info("Database already contains data, skipping initialization")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    logger.info("Creating initial database")
    init_db()
    logger.info("Database initialization completed") 