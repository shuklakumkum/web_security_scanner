from urllib.parse import urlparse
import re
from typing import Dict, Optional


def is_valid_domain(domain: str) -> bool:
    if not domain:
        return False

    if "." not in domain:
        return False

    if not re.match(r"^[A-Za-z0-9.-]+$", domain):
        return False

    if ".." in domain:
        return False

    return True


def normalize_url(url: str) -> str:
    url = url.strip()

    # If user types only name like "google"
    if "." not in url:
        url = url + ".com"

    # Add HTTPS if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def validate_url(url: str) -> Dict[str, Optional[str]]:
    if not url:
        return {
            "valid": False,
            "domain": None,
            "scheme": None,
            "error": "URL is empty"
        }

    try:
        normalized_url = normalize_url(url)
        parsed = urlparse(normalized_url)

        domain = parsed.netloc
        scheme = parsed.scheme

        if domain.startswith("www."):
            domain = domain[4:]

        if not is_valid_domain(domain):
            return {
                "valid": False,
                "domain": domain,
                "scheme": scheme,
                "error": "Invalid domain"
            }

        return {
            "valid": True,
            "domain": domain,
            "scheme": scheme,
            "normalized_url": normalized_url,
            "error": None
        }

    except Exception as e:
        return {
            "valid": False,
            "domain": None,
            "scheme": None,
            "error": str(e)
        }