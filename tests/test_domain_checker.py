import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.domain_checker import analyze_domain


domains = [
    "google.com",
    "amazon.com",
    "flipkart.com",
    "facebook.com",
    "amazom.com",
    "gooogle.com",
    "faceb00k.com",
    "flipkart.co",
    "amazon-login.com",
    "secure-flipkart.com",
    "paytm-verify-account.com",
    "google-security-alert.com",
    "amazom-login-verify.xyz",
    "secure-amazon-account-update.tk",
    "faceb00k-security-check-urgent.ml",
]

output_dir = "tests/outputs"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/day2_domain_analysis_results.txt", "w") as f:
    f.write("Day 2 - Domain Analysis Test Results\n")
    f.write("=====================================\n\n")

    low = med = high = 0

    for i, domain in enumerate(domains, 1):
        result = analyze_domain(domain)

        if result["risk_level"] == "Low":
            low += 1
        elif result["risk_level"] == "Medium":
            med += 1
        else:
            high += 1

        f.write(f"Test {i}: {domain}\n")
        f.write("Result:\n")
        f.write(f"  - Is Suspicious: {result['is_suspicious']}\n")
        f.write(f"  - Matched Domain: {result['matched_domain']}\n")
        f.write(f"  - Similarity: {result['similarity']}\n")
        f.write(f"  - Risk Score: {result['risk_score']}\n")
        f.write(f"  - Risk Level: {result['risk_level']}\n")
        f.write(f"  - Warnings: {result['warnings']}\n\n")

    f.write("SUMMARY:\n")
    f.write("--------\n")
    f.write(f"Total Domains Tested: {len(domains)}\n")
    f.write(f"Safe (0-30): {low}\n")
    f.write(f"Medium Risk (31-60): {med}\n")
    f.write(f"High Risk (61-100): {high}\n")
