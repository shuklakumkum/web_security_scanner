from typing import Dict, List
from difflib import SequenceMatcher
import re


# ✅ Legitimate domains (Add more if needed)
LEGITIMATE_DOMAINS = [
    "amazon.com",
    "amazon.in",
    "flipkart.com",
    "myntra.com",
    "paytm.com",
    "google.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "linkedin.com",
    "paypal.com",
    "microsoft.com",
]


# ==============================
# 🔍 1️⃣ Typosquatting Detection
# ==============================
def check_typosquatting(domain: str) -> Dict:
    best_match = ""
    highest_similarity = 0.0

    for legit in LEGITIMATE_DOMAINS:
        similarity = SequenceMatcher(None, domain, legit).ratio()

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = legit

    is_suspicious = highest_similarity > 0.80 and domain != best_match

    return {
        "is_suspicious": is_suspicious,
        "matched_domain": best_match if is_suspicious else "",
        "similarity": round(highest_similarity, 2),
        "reason": "Possible typosquatting detected"
        if is_suspicious
        else "",
    }


# ==============================
# 🔎 2️⃣ Suspicious Pattern Check
# ==============================
def check_suspicious_patterns(domain: str) -> List[str]:
    warnings = []

    # Multiple dashes
    if domain.count("-") > 2:
        warnings.append("Multiple dashes detected")

    # Suspicious keywords
    keywords = [
        "login", "verify", "secure",
        "account", "update", "confirm",
        "alert", "password", "bank"
    ]
    for word in keywords:
        if word in domain:
            warnings.append(f"Suspicious keyword: {word}")

    # Suspicious extensions
    suspicious_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf"]
    for ext in suspicious_tlds:
        if domain.endswith(ext):
            warnings.append(f"Suspicious domain extension: {ext}")

    # Long domain
    if len(domain) > 30:
        warnings.append("Unusually long domain")

    # Numbers mixed with letters (e.g., paypa1.com)
    if re.search(r"[a-zA-Z]", domain) and re.search(r"\d", domain):
        warnings.append("Suspicious character substitution")

    return warnings


# =================================
# 🛡 3️⃣ Main Domain Analysis Engine
# =================================
def analyze_domain(domain: str) -> Dict:

    typo_result = check_typosquatting(domain)
    pattern_warnings = check_suspicious_patterns(domain)

    warnings = []
    risk_score = 0
    is_suspicious = False

    # 🔴 Strong Typosquatting Detection
    if typo_result["is_suspicious"]:
        risk_score += 50
        is_suspicious = True
        warnings.append(
            f"Domain similar to {typo_result['matched_domain']}"
        )

    # 🔴 Brand Impersonation Detection
    famous_brands = [
        "paypal", "google", "amazon",
        "facebook", "microsoft"
    ]

    for brand in famous_brands:
        if brand in domain and domain != f"{brand}.com":
            risk_score += 40
            is_suspicious = True
            warnings.append(f"Possible impersonation of {brand}.")
            break

    # 🔴 Suspicious Keyword Weight
    suspicious_keywords = [
        "login", "secure", "verify",
        "account", "update", "alert",
        "password", "bank", "confirm"
    ]

    for word in suspicious_keywords:
        if word in domain:
            risk_score += 15
            is_suspicious = True
            warnings.append(f"Phishing keyword detected: {word}")

    # 🔴 Add Pattern Warnings
    risk_score += len(pattern_warnings) * 10
    warnings.extend(pattern_warnings)

    # Cap risk score
    risk_score = min(risk_score, 100)

    # Risk Level
    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "domain": domain,
        "is_suspicious": is_suspicious,
        "matched_domain": typo_result["matched_domain"],
        "similarity": typo_result["similarity"],
        "warnings": warnings,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


# =================================
# 🔄 Similarity Check API Utility
# =================================
def check_domain_similarity(domain: str) -> Dict:
    result = check_typosquatting(domain)

    return {
        "is_similar": result["is_suspicious"],
        "matched_domain": result["matched_domain"],
        "similarity": result["similarity"],
    }