import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.advanced_detection import advanced_scan

OUTPUT_PATH = "tests/outputs/day7_advanced_detection_results.txt"

urls = [
    # crafted URLs
    "https://example.com/" + "a" * 120,
    "http://192.168.1.1/login",
    "http://example.com/a-b_c@d-e_f@g",
    "http://paypal-login-winner-prize.com",
    "http://github.com",

    # mix safe & suspicious
    "https://google.com",
    "https://amazon.in",
    "https://secure-login-bank.com",
    "https://crypto-wallet-secure.net",
    "https://example.org",
    "https://winner-prize-claim-now.com",
    "https://stackoverflow.com",
    "https://microsoft.com",
    "https://secure-update-account.com",
    "https://flipkart.com",
]

os.makedirs("tests/outputs", exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for url in urls:
        try:
            result = advanced_scan(url)

            f.write(f"\nURL: {url}\n")
            f.write(f"Length: {result['checks']['length']}\n")
            f.write(f"IP Check: {result['checks']['ip_check']}\n")
            f.write(f"Special Characters: {result['checks']['special_characters']}\n")
            f.write(f"Keywords: {result['checks']['keywords']}\n")
            f.write(f"Redirects: {result['checks']['redirects']}\n")
            f.write(f"TOTAL SCORE: {result['advanced_risk_score']}\n")
            f.write("-" * 60 + "\n")

        except Exception as e:
            f.write(f"\nURL: {url}\nERROR: {str(e)}\n")
            f.write("-" * 60 + "\n")

print("Results saved.")
