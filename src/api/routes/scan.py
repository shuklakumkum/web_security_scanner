from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

# Services
from src.services.url_validator import validate_url
from src.services.domain_checker import analyze_domain
from src.services.ssl_checker import analyze_ssl
from src.services.security_headers import generate_security_score
from src.services.advanced_detection import advanced_scan

from src.services.database import (
    save_scan_result,
    get_scan_by_id,
    get_recent_scans,
    get_scans_by_domain,
)

# IMPORTANT: This must exist for import to work
router = APIRouter(tags=["Scans"])


# =========================
# Request Model
# =========================
class URLRequest(BaseModel):
    url: str


# =========================
# HEALTH ENDPOINTS
# =========================
@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/health/detailed")
def health_detailed():
    return {
        "status": "healthy",
        "service": "Web Security Scanner",
        "time": datetime.utcnow().isoformat()
    }


@router.get("/health/test-error")
def health_error():
    raise HTTPException(status_code=500, detail="Test error endpoint")


# =========================
# COMPLETE SCAN ENDPOINT
# =========================
@router.post("/scan")
def complete_scan(request: URLRequest):

    url = request.url.strip()
    risk_score = 0
    warnings: List[str] = []
    recommendations: List[str] = []

    # -------------------------
    # 1. URL VALIDATION
    # -------------------------
    try:
        validation = validate_url(url)
    except Exception as e:
        validation = {"valid": False, "domain": "", "scheme": "", "error": str(e)}

    if not validation.get("valid", False):
        risk_score += 20
        warnings.append("Invalid URL format")
        recommendations.append("Check URL format before visiting.")
        domain = ""
    else:
        domain = validation.get("domain", "")

    # -------------------------
    # 2. DOMAIN ANALYSIS
    # -------------------------
    try:
        domain_result = analyze_domain(domain)
    except Exception as e:
        domain_result = {
            "is_suspicious": False,
            "matched_domain": "",
            "warnings": [f"Domain analysis failed: {str(e)}"],
            "risk_score": 0
        }

    risk_score += domain_result.get("risk_score", 0)
    warnings.extend(domain_result.get("warnings", []))

    if domain_result.get("is_suspicious"):
        recommendations.append(
            f"Domain similar to {domain_result.get('matched_domain')}."
        )

    # -------------------------
    # 3. SSL CHECK
    # -------------------------
    try:
        ssl_result = analyze_ssl(url)
    except Exception as e:
        ssl_result = {
            "has_https": False,
            "valid_certificate": False,
            "certificate_info": {},
            "error": f"SSL check failed: {str(e)}"
        }

    if not ssl_result.get("has_https", True):
        risk_score += 20
        warnings.append("Website not using HTTPS")
        recommendations.append("Avoid entering data on HTTP sites.")

    if not ssl_result.get("valid_certificate", True):
        risk_score += 30
        warnings.append("Invalid SSL certificate")

    # -------------------------
    # 4. SECURITY HEADERS
    # -------------------------
    try:
        headers_result = generate_security_score(url)
    except Exception as e:
        headers_result = {
            "missing_headers": [],
            "error": f"Security headers check failed: {str(e)}"
        }

    missing_headers = headers_result.get("missing_headers", [])

    if len(missing_headers) >= 5:
        risk_score += 20
    elif len(missing_headers) >= 3:
        risk_score += 10

    # -------------------------
    # 5. ADVANCED DETECTION
    # -------------------------
    try:
        advanced_result = advanced_scan(url)
    except Exception as e:
        advanced_result = {
            "risk_score": 0,
            "warnings": [f"Advanced detection failed: {str(e)}"]
        }

    risk_score += advanced_result.get("risk_score", 0)
    warnings.extend(advanced_result.get("warnings", []))

    # -------------------------
    # LIMIT SCORE
    # -------------------------
    risk_score = min(100, risk_score)

    # -------------------------
    # RISK LEVEL
    # -------------------------
    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"
        recommendations.append("HIGH RISK: Possible phishing website.")

    timestamp = datetime.utcnow().isoformat()

    result = {
        "url": url,
        "domain": domain,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "is_suspicious": domain_result.get("is_suspicious", False),
        "timestamp": timestamp,
        "checks": {
            "url_validation": validation,
            "domain_analysis": domain_result,
            "ssl": ssl_result,
            "security_headers": headers_result,
            "advanced_detection": advanced_result,
        },
        "warnings": warnings,
        "recommendations": recommendations,
    }

    # -------------------------
    # SAVE TO DATABASE
    # -------------------------
    try:
        scan_id = save_scan_result(
            url,
            domain,
            risk_score,
            risk_level,
            warnings,
            recommendations,
            timestamp,
        )
        result["scan_id"] = scan_id
    except Exception as e:
        result["scan_id"] = None
        warnings.append(f"Failed to save scan: {str(e)}")

    return result


# =========================
# DATABASE ENDPOINTS
# =========================
@router.get("/scans")
def recent_scans():
    try:
        return get_recent_scans(20)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch recent scans: {str(e)}"
        )


@router.get("/scans/{scan_id}")
def scan_by_id(scan_id: int):
    scan = get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@router.get("/scans/domain/{domain}")
def scans_by_domain(domain: str):
    return get_scans_by_domain(domain)


# =========================
# ROOT
# =========================
@router.get("/")
def root():
    return {"message": "Web Security Scanner API running"}