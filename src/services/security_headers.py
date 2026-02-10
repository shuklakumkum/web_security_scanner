import requests
from typing import Dict

# Required security headers
REQUIRED_HEADERS = {
    "X-Frame-Options": "Protects against clickjacking attacks",
    "X-Content-Type-Options": "Prevents MIME type sniffing",
    "Strict-Transport-Security": "Enforces HTTPS connections",
    "Content-Security-Policy": "Prevents XSS attacks",
    "X-XSS-Protection": "Enables browser XSS filter",
    "Referrer-Policy": "Controls referrer information",
}


def check_security_headers(url: str) -> Dict:
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        headers = response.headers
    except Exception as e:
        return {"error": str(e)}

    present = []
    missing = []

    for header, desc in REQUIRED_HEADERS.items():
        if header in headers:
            present.append({
                "header": header,
                "value": headers.get(header),
                "description": desc
            })
        else:
            missing.append({
                "header": header,
                "description": desc
            })

    score = int((len(present) / len(REQUIRED_HEADERS)) * 100)

    return {
        "url": url,
        "present_headers": present,
        "missing_headers": missing,
        "score": score,
        "raw_headers": dict(headers)
    }


def analyze_header_strength(headers: dict) -> Dict:
    strong = []
    weak = []
    missing = []

    for header in REQUIRED_HEADERS.keys():
        value = headers.get(header)

        if not value:
            missing.append(header)
            continue

        val = value.lower()

        if header == "X-Frame-Options":
            if val in ["deny", "sameorigin"]:
                strong.append(header)
            else:
                weak.append(header)

        elif header == "X-Content-Type-Options":
            if val == "nosniff":
                strong.append(header)
            else:
                weak.append(header)

        elif header == "Strict-Transport-Security":
            if "max-age" in val:
                try:
                    age = int(val.split("max-age=")[1].split(";")[0])
                    if age > 31536000:
                        strong.append(header)
                    else:
                        weak.append(header)
                except:
                    weak.append(header)
            else:
                weak.append(header)

        elif header == "Content-Security-Policy":
            if "default-src *" in val:
                weak.append(header)
            else:
                strong.append(header)

        else:
            strong.append(header)

    return {"strong": strong, "weak": weak, "missing": missing}


def generate_security_score(url: str) -> Dict:
    result = check_security_headers(url)

    if "error" in result:
        return result

    headers = result["raw_headers"]
    strength = analyze_header_strength(headers)

    present_count = len(result["present_headers"])

    score = present_count * 15
    score += len(strength["strong"]) * 2
    score -= len(strength["weak"]) * 5

    score = max(0, min(score, 100))

    return {
        "url": url,
        "headers_present": present_count,
        "analysis": result,
        "strength": strength,
        "final_score": score
    }
