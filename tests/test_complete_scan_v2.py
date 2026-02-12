import requests

urls = [
    "https://github.com",
    "https://google.com",
    "https://mozilla.org",
    "https://amazon.in",
    "https://flipkart.com",
    "https://wikipedia.org",
    "http://example.com",
    "https://httpbin.org",
    "http://amazom-login.xyz",
    "http://paypa1-login.xyz",
    "https://github.com/login",
    "http://testphp.vulnweb.com",
    "https://expired.badssl.com",
    "https://self-signed.badssl.com",
    "http://neverssl.com"
]

for url in urls:
    response = requests.post(
        "http://127.0.0.1:8000/api/scan",
        json={"url": url}
    )

    print("Testing:", url)
    print(response.json())
    print("=" * 60)
