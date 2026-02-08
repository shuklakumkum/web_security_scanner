from typing import Dict,List
from difflib import SequenceMatcher
import re

# Legitimate domains
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
]

def check_typosquatting (domain: str) -> Dict:
    best_match=""
    highest_similarity = 0.0

    for legit in LEGITIMATE_DOMAINS:
        similarity = SequenceMatcher(None, domain, legit).ratio()

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = legit

    is_suspicious  = highest_similarity > 0.80 and domain != best_match

    return{
         "is_suspicious": is_suspicious,
        "matched_domain": best_match if is_suspicious else "",
        "similarity": round(highest_similarity, 2),
        "reason": "Possible typosquatting detected"
        if is_suspicious
        else "",
    }
def check_suspicious_patterns(domain: str) -> List[str]:
    warnings = []

    # Multiple dashes
    if domain.count("-") > 2:
        warnings.append("Multiple dashes detected")

    # Suspicious keywords
    keywords = ["login", "verify", "secure", "account", "update", "confirm"]
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

    # Numbers mixed with letters
    if re.search(r"[a-zA-Z]", domain) and re.search(r"\d", domain):
        warnings.append("Suspicious character substitution")

    return warnings


def analyze_domain(domain: str) -> Dict:
    typo_result = check_typosquatting(domain)
    warnings = check_suspicious_patterns(domain)

    risk_score = 0

    if typo_result["is_suspicious"]:
        risk_score += 50

    risk_score += len(warnings) * 10
    risk_score = min(risk_score, 100)

    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "domain": domain,
        "is_suspicious": typo_result["is_suspicious"],
        "matched_domain": typo_result["matched_domain"],
        "similarity": typo_result["similarity"],
        "warnings": warnings,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }

def check_domain_similarity(domain: str) -> Dict:
    result = check_typosquatting(domain)

    return {
        "is_similar": result["is_suspicious"],
        "matched_domain": result["matched_domain"],
        "similarity": result["similarity"],
    }


