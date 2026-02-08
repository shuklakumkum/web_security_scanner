from urllib.parse import urlparse
import re
from typing import Dict, Optional


def is_valid_domain(domain: str) -> bool:
    """Check if domain is valid"""
    if not domain or "." not in domain:
        return False

    # only letters, numbers, dots, dashes
    if not re.match(r"^[A-Za-z0-9.-]+$", domain):
        return False

    # No consecutive dots
    if ".." in domain:
        return False

    return True


def extract_domain(url: str) -> str:
    """Get clean domain without www."""
    parsed = urlparse(url)
    domain = parsed.netloc

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def validate_url(url: str) -> Dict[str, Optional[str]]:
    """Validate URL and extract info"""
    if not url:
        return {"valid": False, "domain": None, "scheme": None, "error": "URL is empty"}

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urlparse(url)
        domain = extract_domain(url)
        scheme = parsed.scheme

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
            "error": None
        }

    except Exception as e:
        return {
            "valid": False,
            "domain": None,
            "scheme": None,
            "error": str(e)
        }


# Test script
if __name__ == "__main__":
    test_urls = [
        "https://google.com",
        "amazon.com",
        "http://flipkart.com",
        "not a url",
        "www.myntra.com",
        "https://www.paytm.com/wallet",
        "",
        "ftp://example.com",
        "https://sub.domain.example.com",
        "invalid..domain"
    ]

    with open("tests/outputs/day1_url_validation_results.txt", "w") as f:
        f.write("Day 1 - URL Validation Test Results\n")
        f.write("=" * 40 + "\n")

        passed = 0
        failed = 0

        for i, url in enumerate(test_urls, 1):
            result = validate_url(url)
            f.write(f"Test {i}: {url}\n")
            f.write(f"Result: {result}\n\n")

            if result["valid"]:
                passed += 1
            else:
                failed += 1

        f.write("Summary:\n")
        f.write(f"- Total tests: {len(test_urls)}\n")
        f.write(f"- Passed: {passed}\n")
        f.write(f"- Failed: {failed}\n")
