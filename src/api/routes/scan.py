from fastapi import APIRouter, HTTPException
from datetime import datetime
from urllib.parse import urlparse

from src.models.responses import ScanResult
from src.services.url_validator import validate_url
from src.services.domain_checker import (
    check_domain_similarity,
    check_suspicious_patterns,
)
from src.services.ssl_checker import analyze_ssl
from src.services.security_headers import generate_security_score
from src.services.advanced_detection import advanced_scan  # Day 7

# Database
from src.services.database import (
    init_database,
    save_scan,
    get_scan_by_id,
    get_recent_scans,
    get_scans_by_domain,
)

router = APIRouter()

# Initialize database
init_database()


# ---------- Risk Calculation ----------
def calculate_risk(valid_url, typo_detected, patterns, https_used):
    score = 0

    if not valid_url:
        score += 20

    if typo_detected:
        score += 50

    score += len(patterns) * 10

    if not https_used:
        score += 20

    return min(score, 100)


def risk_level(score: int):
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    return "High"


# ---------- Scan Endpoint ----------
@router.post("/scan", response_model=ScanResult)
def complete_scan(data: dict):
    url = data["url"]

    parsed = urlparse(url if "://" in url else f"http://{url}")
    domain = parsed.netloc.replace("www.", "")

    # URL validation
    url_result = validate_url(url)
    valid_url = url_result["valid"]

    # Domain similarity
    domain_result = check_domain_similarity(domain)
    typo_detected = domain_result["is_similar"]

    # Suspicious patterns
    pattern_warnings = check_suspicious_patterns(domain)

    # SSL analysis
    ssl_result = analyze_ssl(url)
    https_used = ssl_result["has_https"]

    # ---------- Day 7 Advanced Detection ----------
    advanced_result = advanced_scan(url)
    advanced_score = advanced_result["advanced_risk_score"]

    # ---------- Base Risk ----------
    score = calculate_risk(
        valid_url,
        typo_detected,
        pattern_warnings,
        https_used,
    )

    # Add advanced detection impact
    score += advanced_score // 2

    # SSL certificate issue
    if https_used and not ssl_result["certificate_valid"]:
        score += 30

    # ---------- Security headers ----------
    headers_result = generate_security_score(url)

    headers_present = headers_result.get("headers_present", 0)
    weak_headers = len(
        headers_result.get("strength", {}).get("weak", [])
    )

    if headers_present == 0:
        score += 20
    elif headers_present <= 2:
        score += 10

    if weak_headers > 0:
        score += 5

    score = min(score, 100)
    level = risk_level(score)

    # ---------- Warnings ----------
    warnings = []

    if typo_detected:
        warnings.append(
            f"Domain similar to legitimate site: {domain_result['matched_domain']}"
        )

    if pattern_warnings:
        warnings.extend(pattern_warnings)

    if not https_used:
        warnings.append("Website does not use HTTPS.")
    elif not ssl_result["certificate_valid"]:
        warnings.append("SSL certificate invalid or expired.")

    if headers_present < 6:
        warnings.append("Missing important security headers.")

    if weak_headers:
        warnings.append("Some headers weakly configured.")

    # ---------- Recommendations ----------
    recommendations = []

    if typo_detected:
        recommendations.append(
            f"Domain resembles {domain_result['matched_domain']}. Verify site."
        )

    if pattern_warnings:
        recommendations.append("Suspicious keywords detected.")

    if not https_used:
        recommendations.append("Website not secure without HTTPS.")
    elif not ssl_result["certificate_valid"]:
        recommendations.append("SSL invalid. Avoid entering data.")

    if headers_present < 6:
        recommendations.append("Add missing security headers.")

    if weak_headers:
        recommendations.append("Strengthen weak headers.")

    if level == "High":
        recommendations.append("HIGH RISK: Possible phishing site.")

    # ---------- Final Result ----------
    result = ScanResult(
        url=url,
        domain=domain,
        is_suspicious=score > 30,
        risk_score=score,
        risk_level=level,
        timestamp=datetime.utcnow().isoformat(),
        checks={
            "url_validation": url_result,
            "domain_analysis": domain_result,
            "patterns_detected": pattern_warnings,
            "https": https_used,
            "ssl_analysis": ssl_result,
            "security_headers": headers_result,
            "advanced_detection": advanced_result,  # Day 7
        },
        warnings=warnings,
        recommendations=recommendations,
    )

    # Save to database
    scan_id = save_scan(result.dict())

    response = result.dict()
    response["scan_id"] = scan_id

    return response


# ---------- Database Endpoints ----------

@router.get("/scans")
def recent_scans():
    return get_recent_scans(20)


@router.get("/scans/domain/{domain}")
def scans_by_domain(domain: str):
    return get_scans_by_domain(domain)


@router.get("/scans/{scan_id}")
def scan_by_id(scan_id: int):
    result = get_scan_by_id(scan_id)
    if not result:
        raise HTTPException(404, "Scan not found")
    return result
