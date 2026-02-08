import requests

urls = [
    "https://google.com",
    "https://github.com",
    "https://amazon.in",
    "http://example.com",
    "http://neverssl.com",
    "https://amazom.com",
    "https://faceboook.com",
    "https://paypa1.com",
    "http://amazom.com",
    "http://faceboook.com",
]

output_lines = []

for url in urls:
    res = requests.post(
        "http://127.0.0.1:8000/api/scan",
        json={"url": url},
    )

    data = res.json()

    output_lines.append(f"""
URL: {url}
Risk Score: {data.get("risk_score")}
SSL: {data.get("ssl_analysis")}
Warnings: {data.get("warnings")}
""")

with open(
    "tests/outputs/day4_scan_with_ssl_results.txt",
    "w",
    encoding="utf-8",
) as f:
    f.write("Day 4 Scan Results\n\n")
    f.write("\n".join(output_lines))

print("Scan results saved.")
