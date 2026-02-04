from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone


class PhishingDetectionError(Exception):
    """Base exception for all app errors"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class URLValidationError(PhishingDetectionError):
    """Raised when URL format is invalid"""

    def __init__(self, message: str = "Invalid URL format"):
        super().__init__(message=message, status_code=400)


class ScanFailedError(PhishingDetectionError):
    """Raised when scanning fails"""

    def __init__(self, message: str = "Failed to scan the URL"):
        super().__init__(message=message, status_code=500)


class RateLimitError(PhishingDetectionError):
    """Raised when rate limit exceeded"""

    def __init__(self, message: str = "Too many requests, please slow down"):
        super().__init__(message=message, status_code=429)


# Exception handler - converts errors into JSON response
async def phishing_error_handler(request: Request, exc: PhishingDetectionError):
    """Convert PhishingDetectionError to JSON response"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.__class__.__name__,
            "detail": exc.message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )
