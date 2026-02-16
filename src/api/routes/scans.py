from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
from datetime import datetime
from src.services.database import save_scan_result

router = APIRouter()

# Request model
class ScanRequest(BaseModel):
    url: HttpUrl

# Response model
class ScanResult(BaseModel):
    scan_id: int
    url: str
    domain: str
    risk_score: int
    risk_level: str
    warnings: list[str]
    recommendations: list[str]
    timestamp: str

# Dummy function to calculate risk (replace with your logic)
def calculate_risk(url: str):
    # Example dummy logic
    return 20, "Low", ["No issues detected"], ["No recommendations"]

# Complete Scan Endpoint
@router.post("/api/scan", response_model=ScanResult)
def complete_scan(request: ScanRequest):
    # Convert HttpUrl to string
    url_str = str(request.url)

    # Parse the URL
    parsed = urlparse(url_str if "://" in url_str else f"http://{url_str}")
    domain = parsed.netloc

    # Calculate risk (your actual scan logic here)
    risk_score, risk_level, warnings, recommendations = calculate_risk(url_str)

    # Timestamp
    timestamp = datetime.utcnow().isoformat()

    # Save scan result to database
    scan_id = save_scan_result(
        url=url_str,
        domain=domain,
        score=risk_score,
        level=risk_level,
        warnings=warnings,
        recommendations=recommendations,
        timestamp=timestamp
    )

    # Return scan result
    return ScanResult(
        scan_id=scan_id,
        url=url_str,
        domain=domain,
        risk_score=risk_score,
        risk_level=risk_level,
        warnings=warnings,
        recommendations=recommendations,
        timestamp=timestamp
    )
