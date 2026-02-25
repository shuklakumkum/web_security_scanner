import re
import requests


# =====================================================
# 1️⃣ URL LENGTH CHECK
# =====================================================
def check_url_length(url: str):
    length = len(url)
    is_suspicious = length > 75

    # Risk scale (0–10)
    if length <= 75:
        risk_points = 0
    elif length <= 100:
        risk_points = 3
    elif length <= 150:
        risk_points = 6
    elif length <= 200:
        risk_points = 8
    else:
        risk_points = 10

    return {
        "length": length,
        "is_suspicious": is_suspicious,
        "risk_points": risk_points
    }


# =====================================================
# 2️⃣ IP ADDRESS IN URL CHECK
# =====================================================
def check_ip_in_url(url: str):
    ip_pattern = r"\b((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"

    match = re.search(ip_pattern, url)

    return {
        "ip_found": bool(match),
        "risk_points": 30 if match else 0
    }


# =====================================================
# 3️⃣ SPECIAL CHARACTER CHECK
# =====================================================
def check_special_characters(url: str):
    # Count suspicious characters (not normal URL symbols)
    suspicious_pattern = r"[@%$!^*()+={}[\]|\\<>]"

    matches = re.findall(suspicious_pattern, url)
    count = len(matches)

    risk_points = 10 if count > 5 else 0

    return {
        "special_char_count": count,
        "risk_points": risk_points
    }


# =====================================================
# 4️⃣ SUSPICIOUS KEYWORD CHECK
# =====================================================
def check_suspicious_keywords(url: str):
    suspicious_keywords = [
        "login", "verify", "account", "secure",
        "signin", "banking", "paypal", "wallet",
        "crypto", "prize", "winner", "urgent"
    ]

    url_lower = url.lower()
    found_keywords = []

    for keyword in suspicious_keywords:
        if keyword in url_lower:
            found_keywords.append(keyword)

    risk_points = len(found_keywords) * 5

    return {
        "found_keywords": found_keywords,
        "risk_points": risk_points
    }


# =====================================================
# 5️⃣ REDIRECT CHAIN CHECK
# =====================================================
def check_redirect_chains(url: str):
    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        redirect_count = len(response.history)
        risk_points = 15 if redirect_count > 2 else 0

        return {
            "redirect_count": redirect_count,
            "risk_points": risk_points,
            "error": None
        }

    except requests.exceptions.Timeout:
        return {
            "redirect_count": 0,
            "risk_points": 0,
            "error": "Request timed out"
        }

    except requests.exceptions.RequestException as e:
        return {
            "redirect_count": 0,
            "risk_points": 0,
            "error": f"Request failed: {str(e)}"
        }


# =====================================================
# 6️⃣ ADVANCED SCAN (MASTER FUNCTION)
# =====================================================
def advanced_scan(url: str):
    """
    Perform full advanced phishing detection scan.
    """

    length_result = check_url_length(url)
    ip_result = check_ip_in_url(url)
    special_char_result = check_special_characters(url)
    keyword_result = check_suspicious_keywords(url)
    redirect_result = check_redirect_chains(url)

    total_score = (
        length_result["risk_points"] +
        ip_result["risk_points"] +
        special_char_result["risk_points"] +
        keyword_result["risk_points"] +
        redirect_result["risk_points"]
    )

    # Cap maximum score at 100
    total_score = min(total_score, 100)

    # Risk classification
    if total_score >= 60:
        risk_level = "High"
    elif total_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "total_risk_score": total_score,
        "risk_level": risk_level,
        "details": {
            "url_length": length_result,
            "ip_check": ip_result,
            "special_characters": special_char_result,
            "suspicious_keywords": keyword_result,
            "redirect_chain": redirect_result
        }
    }