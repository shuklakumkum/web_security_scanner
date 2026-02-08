import requests
import time
import os

domains = [
    "https://google.com",
    "https://amazon.com",
    "https://flipkart.com",
    "https://facebook.com",
    "https://amazom.com",
    "https://gooogle.com",
    "https://faceb00k.com",
    "https://flipkart.co",
    "https://amazon-login.com",
    "https://secure-flipkart.com",
    "https://paytm-verify-account.com",
    "https://google-security-alert.com",
    "https://amazom-login-verify.xyz",
    "https://secure-amazon-account-update.tk",
    "https://faceb00k-security-check-urgent.ml",
]

url = "http://127.0.0.1:8000/api/check-domain"

output_dir = "tests/outputs"
os.makedirs(output_dir, exist_ok=True)

success = 0
fail = 0
times = []

with open(f"{output_dir}/day2_api_test_results.txt", "w") as f:
    f.write("Day 2 - Domain Check API Test Results\n")
    f.write("======================================\n\n")

    for i, d in enumerate(domains, 1):
        start = time.time()
        r = requests.post(url, json={"url": d})
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)

        if r.status_code == 200:
            success += 1
        else:
            fail += 1

        f.write(f"Test {i}: POST /api/check-domain\n")
        f.write(f"URL: {d}\n")
        f.write(f"Status: {r.status_code}\n")
        f.write("Response:\n")
        f.write(str(r.json()))
        f.write("\n\n")

    avg_time = sum(times) / len(times)

    f.write("API Performance:\n")
    f.write("----------------\n")
    f.write(f"Total Requests: {len(domains)}\n")
    f.write(f"Successful (200): {success}\n")
    f.write(f"Failed: {fail}\n")
    f.write(f"Average Response Time: {round(avg_time,2)} ms\n")
