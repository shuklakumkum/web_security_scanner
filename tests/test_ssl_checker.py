import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.ssl_checker import analyze_ssl

urls = [
    "https://google.com",
    "https://github.com",
    "https://amazon.in",
    "https://wikipedia.org",
    "http://example.com",
    "http://neverssl.com",
    "http://httpforever.com",
    "https://expired.badssl.com",
    "https://wrong.host.badssl.com",
    "https://self-signed.badssl.com",
    "https://goggle.com",
    "http://paypa1.com",
]

results = []

secure = warning = insecure = 0

for url in urls:
    result = analyze_ssl(url)

    score = result["ssl_score"]

    if score >= 80:
        secure += 1
    elif score >= 30:
        warning += 1
    else:
        insecure += 1

    results.append(f"""
URL: {url}
Has HTTPS: {result['has_https']}
SSL Score: {score}
Info: {result.get('certificate_info')}
""")

output = "\n".join(results)

summary = f"""
SUMMARY
Total URLs: {len(urls)}
Secure: {secure}
Warning: {warning}
Insecure: {insecure}
"""

with open("tests/outputs/day4_ssl_check_results.txt", "w", encoding="utf-8") as f:
    f.write("Day 4 SSL Results\n\n")
    f.write(output)
    f.write(summary)

print("Results saved.")
