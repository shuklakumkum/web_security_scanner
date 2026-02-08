import requests
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict


def check_https(url: str) -> bool:
    """Check if URL uses HTTPS"""
    return url.lower().startswith("https://")


def verify_ssl_certificate(url: str) -> Dict:
    """Verify SSL certificate using requests"""
    try:
        response = requests.head(
            url,
            timeout=5,
            verify=True,
            allow_redirects=True,
        )

        return {
            "valid": True,
            "error": "",
            "status_code": response.status_code,
        }

    except requests.exceptions.SSLError as e:
        return {
            "valid": False,
            "error": f"SSL Error: {str(e)}",
            "status_code": None,
        }

    except requests.exceptions.Timeout:
        return {
            "valid": False,
            "error": "Request timeout",
            "status_code": None,
        }

    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
            "status_code": None,
        }


def get_certificate_info(domain: str) -> Dict:
    """Fetch SSL certificate details"""
    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        issuer = dict(x[0] for x in cert["issuer"])
        subject = dict(x[0] for x in cert["subject"])

        expiry_date = datetime.strptime(
            cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
        )

        days_left = (expiry_date - datetime.utcnow()).days

        return {
            "issuer": issuer.get("organizationName", ""),
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "days_until_expiry": days_left,
            "subject": subject.get("commonName", ""),
        }

    except Exception as e:
        return {
            "issuer": "",
            "expiry_date": "",
            "days_until_expiry": -1,
            "subject": "",
            "error": str(e),
        }


def analyze_ssl(url: str) -> Dict:
    """Complete SSL analysis with scoring"""

    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path

    has_https = check_https(url)

    score = 0
    cert_valid = False
    cert_info = {}

    if not has_https:
        return {
            "has_https": False,
            "certificate_valid": False,
            "certificate_info": {},
            "ssl_score": 0,
        }

    score += 50

    verification = verify_ssl_certificate(url)
    cert_valid = verification["valid"]

    if cert_valid:
        score += 30

    cert_info = get_certificate_info(domain)

    if cert_info.get("days_until_expiry", 0) > 30:
        score += 20

    return {
        "has_https": has_https,
        "certificate_valid": cert_valid,
        "certificate_info": cert_info,
        "ssl_score": score,
        "verification": verification,
    }
