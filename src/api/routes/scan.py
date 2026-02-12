from fastapi import APIRouter
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

router = APIRouter()


# ---------------- Risk Calculation ----------------
def calculate_risk(
    valid_url: bool,
    typo_detected: bool,
    patterns: list,
    https_used: bool
):
    score = 0

    if not valid_url:
        score += 20

    if typo_detected:
        score += 50

    score += len(patterns) * 10

    # No HTTPS penalty
    if not https_used:
        score += 20

    return min(score, 100)


def risk_level(score: int):
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    return "High"


# ---------------- Scan Endpoint ----------------
@router.post("/scan", response_model=ScanResult)
def complete_scan(data: dict):
    url = data["url"]

    parsed = urlparse(url if "://" in url else f"http://{url}")
    domain = parsed.netloc.replace("www.", "")

    # ---------- Step 1: URL validation ----------
    url_result = validate_url(url)
    valid_url = url_result["valid"]

    # ---------- Step 2: Domain similarity ----------
    domain_result = check_domain_similarity(domain)
    typo_detected = domain_result["is_similar"]

    # ---------- Step 3: Pattern check ----------
    pattern_warnings = check_suspicious_patterns(domain)

    # ---------- Step 4: SSL analysis ----------
    ssl_result = analyze_ssl(url)
    https_used = ssl_result["has_https"]

    # ---------- Step 5: Base Risk calculation ----------
    score = calculate_risk(
        valid_url,
        typo_detected,
        pattern_warnings,
        https_used,
    )

    # Extra SSL penalty
    if https_used and not ssl_result["certificate_valid"]:
        score += 30

    # ---------- Step 6: Security Headers ----------
    headers_result = generate_security_score(url)

    headers_present = headers_result.get("headers_present", 0)
    weak_headers = len(
        headers_result.get("strength", {}).get("weak", [])
    )

    # Risk update based on headers
    if headers_present == 0:
        score += 20
    elif 1 <= headers_present <= 2:
        score += 10

    if weak_headers > 0:
        score += 5

    score = min(score, 100)
    level = risk_level(score)

    # ---------- Step 7: Warnings ----------
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
        warnings.append("SSL certificate is invalid or expired.")

    if headers_present < 6:
        warnings.append("Missing important security headers.")

    if weak_headers:
        warnings.append("Some security headers are weakly configured.")

    # ---------- Step 8: Recommendations ----------
    recommendations = []

    if typo_detected:
        recommendations.append(
            f"This domain is similar to {domain_result['matched_domain']}. Verify website carefully."
        )

    if pattern_warnings:
        recommendations.append(
            "Domain contains suspicious keywords. Be cautious."
        )

    if not https_used:
        recommendations.append(
            "Website doesn't use HTTPS. Your data may not be secure."
        )

    elif not ssl_result["certificate_valid"]:
        recommendations.append(
            "Website SSL certificate is invalid. Avoid entering sensitive data."
        )

    if headers_present < 6:
        recommendations.append(
            "Add missing security headers for better protection."
        )

    if weak_headers:
        recommendations.append(
            "Strengthen weak security header configurations."
        )

    if level == "High":
        recommendations.append(
            "HIGH RISK: This appears to be a phishing website. Do not enter personal information."
        )

    # ---------- Final Response ----------
    return ScanResult(
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
        },
        warnings=warnings,
        recommendations=recommendations,
    )
