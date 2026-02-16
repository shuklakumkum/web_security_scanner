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

for url in urls:
    res = requests.post(
        "http://127.0.0.1:8000/api/scan",
        json={"url": url}
    )
    print("Scanned:", url, res.status_code)

print("All scans completed!")
