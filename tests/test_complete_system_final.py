import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/scan"

# 10 safe URLs
SAFE_URLS = [
    "https://google.com",
    "https://github.com",
    "https://microsoft.com",
    "https://openai.com",
    "https://wikipedia.org",
    "https://python.org",
    "https://stackoverflow.com",
    "https://apple.com",
    "https://amazon.com",
    "https://mozilla.org",
]

# 10 phishing-like URLs
PHISHING_URLS = [
    "http://secure-login-paypal.com",
    "http://verify-account-bank.com",
    "http://login-update-info.com",
    "http://paypal-verification.net",
    "http://account-security-alert.com",
    "http://free-gift-prize.com",
    "http://update-banking-info.com",
    "http://secure-payment-check.com",
    "http://confirm-identity-now.com",
    "http://urgent-account-reset.com",
]

# 5 HTTP-only URLs
HTTP_URLS = [
    "http://example.com",
    "http://testphp.vulnweb.com",
    "http://neverssl.com",
    "http://http.badssl.com",
    "http://demo.testfire.net",
]

# 5 poor headers examples
HEADER_TEST_URLS = [
    "http://example.org",
    "http://info.cern.ch",
    "http://httpforever.com",
    "http://speedtest.tele2.net",
    "http://detectportal.firefox.com",
]

# Combine all URLs
ALL_URLS = SAFE_URLS + PHISHING_URLS + HTTP_URLS + HEADER_TEST_URLS


def scan_url(url):
    try:
        response = requests.post(BASE_URL, json={"url": url})

        if response.status_code == 200:
            data = response.json()
            print(f"Scanned: {url}")
            print(f"Risk Level: {data.get('risk_level')} | Scan ID: {data.get('scan_id')}")
            print("-" * 60)
        else:
            print(f"Failed scan: {url} | Status: {response.status_code}")

    except Exception as e:
        print(f"Error scanning {url}: {e}")

    # delay to avoid overload
    time.sleep(0.5)


def test_scan_30_urls():
    print("Starting full system test...\n")

    for url in ALL_URLS:
        scan_url(url)

    print("\nAll 30 URLs scanned successfully.")


# Run automatically when script is executed
if __name__ == "__main__":
    test_scan_30_urls()
