from src.services.security_headers import generate_security_score

sites = [
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
]

for site in sites:
    result = generate_security_score(site)
    print(site, result["final_score"])
