import requests

urls = [
    "https://google.com",
    "https://github.com",
    "https://wikipedia.org",
    "https://stackoverflow.com",
    "https://openai.com",
    "https://python.org",
    "https://mozilla.org",
    "https://linkedin.com",
    "https://reddit.com",
    "https://example.com",
    "http://malicious.example.com",
    "http://phishingsite.com/login",
    "http://badsite.fakebank.com",
    "http://evil.com",
    "http://test-phish.com",
    "http://login-paypal.com",
    "http://secure-facebook.com",
    "http://fake-google.com",
    "http://banking-fake.com",
    "http://hacker-site.org"
]

API_URL = "http://127.0.0.1:8000/api/scan"

for url in urls:
    r = requests.post(API_URL, json={"url": url})
    print("Scanned:", url, "| Status:", r.status_code)

print("All scans completed!")
