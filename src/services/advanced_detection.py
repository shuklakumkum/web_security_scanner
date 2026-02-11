import re
import requests
from typing import Dict, List
from urllib.parse import urlparse

TIMEOUT = 5


# ---------- Function 1 ----------
def check_url_length(url: str) -> Dict:
    length = len(url)

    risk = 0
    if length > 75:
        risk = min(10, (length - 75) // 5 + 5)

    return {
        "length": length,
        "is_suspicious": length > 75,
        "risk_points": min(risk, 10),
    }


# ---------- Function 2 ----------
def check_ip_in_url(url: str) -> Dict:
    domain = urlparse(url).netloc

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    has_ip = re.match(ip_pattern, domain) is not None

    return {
        "domain": domain,
        "contains_ip": has_ip,
        "risk_points": 30 if has_ip else 0,
    }


# ---------- Function 3 ----------
def check_special_characters(url: str) -> Dict:
    specials = re.findall(r"[^\w:/\.]", url)
    unique_chars = list(set(specials))
    count = len(specials)

    risk = 10 if count > 5 else 0

    return {
        "count": count,
        "characters_found": unique_chars,
        "risk_points": risk,
    }


# ---------- Function 4 ----------
def check_suspicious_keywords(url: str) -> Dict:
    keywords = [
        "login", "verify", "account", "secure",
        "signin", "banking", "paypal", "wallet",
        "crypto", "prize", "winner", "urgent"
    ]

    found: List[str] = []
    url_lower = url.lower()

    for word in keywords:
        if word in url_lower:
            found.append(word)

    risk = min(len(found) * 5, 30)

    return {
        "keywords_found": found,
        "risk_points": risk,
    }


# ---------- Function 5 ----------
def check_redirect_chains(url: str) -> Dict:
    try:
        response = requests.get(url, allow_redirects=True, timeout=TIMEOUT)
        redirects = len(response.history)
    except Exception:
        redirects = 0

    risk = 15 if redirects > 2 else 0

    return {
        "redirect_count": redirects,
        "risk_points": risk,
    }


# ---------- Function 6 ----------
def advanced_scan(url: str) -> Dict:
    length_check = check_url_length(url)
    ip_check = check_ip_in_url(url)
    special_check = check_special_characters(url)
    keyword_check = check_suspicious_keywords(url)
    redirect_check = check_redirect_chains(url)

    total_risk = (
        length_check["risk_points"]
        + ip_check["risk_points"]
        + special_check["risk_points"]
        + keyword_check["risk_points"]
        + redirect_check["risk_points"]
    )

    total_risk = min(total_risk, 100)

    return {
        "url": url,
        "checks": {
            "length": length_check,
            "ip_check": ip_check,
            "special_characters": special_check,
            "keywords": keyword_check,
            "redirects": redirect_check,
        },
        "advanced_risk_score": total_risk,
    }
