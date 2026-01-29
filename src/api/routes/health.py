from fastapi import APIRouter
from datetime import datetime, timezone
from config.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

# Basic health check
@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "API is running normally"
    }

# Detailed health check
@router.get("/detailed")
def detailed_health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug_mode": settings.DEBUG,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "api": "ok",
            "config": "ok"
        }
    }
