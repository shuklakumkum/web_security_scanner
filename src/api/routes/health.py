from fastapi import APIRouter
from datetime import datetime, timezone

from src.models.responses import HealthResponse, DetailedHealthResponse
from src.config.settings import settings
from src.api.exceptions import URLValidationError, ScanFailedError    

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Health check endpoint
    Returns API status and basic info
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        message="API is running normally",
    )


@router.get("/detailed", response_model=DetailedHealthResponse)
def detailed_health() -> DetailedHealthResponse:
    """
    Detailed health check
    Returns more information about the system
    """
    return DetailedHealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug_mode=settings.DEBUG,
        timestamp=datetime.now(timezone.utc).isoformat(),
        checks={
            "api": "ok",
            "config": "ok",
        },
    )


@router.get("/test-error")
def test_error(error_type: str = "validation"):
    """
    Test endpoint to verify error handling works

    error_type options:
    validation: triggers URLValidationError (400)
    scan: triggers ScanFailedError (500)
    none: returns success
    """
    if error_type == "validation":
        raise URLValidationError("This is a test validation error")   
    elif error_type == "scan":
        raise ScanFailedError("This is a test scan error")
    else:
        return {"message": "No error triggered", "success": True}
