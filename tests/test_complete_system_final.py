import requests
import time
from datetime import datetime
import os

BASE_URL = "http://127.0.0.1:8000/api/scan"

# ---------- URL DATASETS ----------

safe_urls = [
    "https://google.com", "https://github.com", "https://microsoft.com",
    "https://amazon.com", "https://wikipedia.org", "https://openai.com",
    "https://stackoverflow.com", "https://python.org", "https://apple.com",
    "https://netflix.com", "https://linkedin.com", "https://mozilla.org",
    "https://ubuntu.com", "https://cloudflare.com", "https://reddit.com"
]

phishing_urls = [
    "http://secure-login-amazon.xyz",
    "http://paypal-login-alert.xyz",
    "http://update-bank-account-login.xyz",
    "http://verify-facebook-account.xyz",
    "http://login-security-warning.xyz",
    "http://free-gift-card-offer.xyz",
    "http://account-verification-required.xyz",
    "http://reset-password-now.xyz",
    "http://bank-security-alert.xyz",
    "http://confirm-account-now.xyz",
    "http://crypto-bonus-offer.xyz",
    "http://urgent-account-update.xyz",
    "http://verify-payment-now.xyz",
    "http://secure-wallet-update.xyz",
    "http://update-login-immediately.xyz",
]

medium_risk = [
    "http://free-download-movies.net",
    "http://cheap-deals-store.biz",
    "http://unknownshop123.com",
    "http://randomblogspot.xyz",
    "http://unknownservice.site",
    "http://clickfastnow.info",
    "http://downloadnowfiles.net",
    "http://cheapproducts.store",
    "http://unknownsupport.help",
    "http://fastbonus.site",
]

edge_cases = [
    "http://192.168.1.1",
    "http://localhost",
    "ftp://example.com",
    "https://example.com:8080",
    "http://test",
    "http://.com",
    "https://example..com",
    "invalidurl",
    "",
    "https://verylongdomainnameexampletestingsite123456.com"
]

all_urls = safe_urls + phishing_urls + medium_risk + edge_cases

# ---------- OUTPUT FILE ----------
output_dir = "tests/outputs"
os.makedirs(output_dir, exist_ok=True)

output_file = f"{output_dir}/day9_final_comprehensive_test.txt"

results = []
success_count = 0
error_count = 0

start_time = time.time()

print("\nRunning Final System Test...\n")

# ---------- TEST LOOP ----------
for url in all_urls:
    try:
        response = requests.post(BASE_URL, json={"url": url}, timeout=15)

        data = response.json()
        results.append((url, response.status_code, data))

        if response.status_code == 200:
            success_count += 1
        else:
            error_count += 1

        print("✓ Tested:", url)

    except Exception as e:
        error_count += 1
        results.append((url, "ERROR", str(e)))
        print("✗ Error:", url)

end_time = time.time()
total_time = end_time - start_time

avg_time = total_time / len(all_urls)

# ---------- WRITE REPORT ----------
with open(output_file, "w", encoding="utf-8") as f:
    f.write("FINAL COMPREHENSIVE SYSTEM TEST\n")
    f.write("=" * 60 + "\n")
    f.write(f"Timestamp: {datetime.now()}\n\n")

    for url, status, result in results:
        f.write(f"URL: {url}\n")
        f.write(f"Status: {status}\n")
        f.write(f"Result: {result}\n")
        f.write("-" * 50 + "\n")

    f.write("\nPERFORMANCE METRICS\n")
    f.write("=" * 60 + "\n")
    f.write(f"Total URLs Tested: {len(all_urls)}\n")
    f.write(f"Successful Requests: {success_count}\n")
    f.write(f"Errors: {error_count}\n")
    f.write(f"Total Time: {total_time:.2f} seconds\n")
    f.write(f"Average Time per URL: {avg_time:.2f} seconds\n")

    f.write("\nSYSTEM HEALTH CHECK\n")
    f.write("=" * 60 + "\n")

    if error_count == 0:
        f.write("System Health: EXCELLENT\n")
    elif error_count < 5:
        f.write("System Health: GOOD\n")
    else:
        f.write("System Health: NEEDS ATTENTION\n")

print("\nTest completed successfully.")
print("Output saved to:", output_file)
