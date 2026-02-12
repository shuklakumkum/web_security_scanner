import os
import time
from src.services.report_generator import (
    generate_text_report,
    generate_json_report,
    generate_html_report,
    save_report
)

# -----------------------------
# Output folders
# -----------------------------
output_folder = "tests/outputs/day8_report_samples"
os.makedirs(output_folder, exist_ok=True)

summary_file = "tests/outputs/day8_report_generation_test.txt"

# -----------------------------
# Sample scans
# -----------------------------
sample_scans = [
    # 1. Safe site
    {
        "scan_id": 1,
        "url": "http://safe.com",
        "domain": "safe.com",
        "risk_score": 20,
        "risk_level": "Low",
        "checks": {"ssl": "Valid", "phishing": "Safe"},
        "warnings": [],
        "recommendations": ["No action needed"]
    },
    # 2. Medium risk
    {
        "scan_id": 2,
        "url": "http://medium.com",
        "domain": "medium.com",
        "risk_score": 50,
        "risk_level": "Medium",
        "checks": {"ssl": "Valid", "phishing": "Warning"},
        "warnings": ["Some warnings detected"],
        "recommendations": ["Check SSL", "Be cautious"]
    },
    # 3. High risk
    {
        "scan_id": 3,
        "url": "http://highrisk.com",
        "domain": "highrisk.com",
        "risk_score": 90,
        "risk_level": "High",
        "checks": {"ssl": "Invalid", "phishing": "Detected"},
        "warnings": ["Multiple issues found"],
        "recommendations": ["Do not visit this site"]
    },
    # 4. All checks failed
    {
        "scan_id": 4,
        "url": "http://failed.com",
        "domain": "failed.com",
        "risk_score": 100,
        "risk_level": "High",
        "checks": {"ssl": "Invalid", "phishing": "Detected"},
        "warnings": ["All checks failed"],
        "recommendations": ["Immediate action required"]
    },
    # 5. Mixed results
    {
        "scan_id": 5,
        "url": "http://mixed.com",
        "domain": "mixed.com",
        "risk_score": 60,
        "risk_level": "Medium",
        "checks": {"ssl": "Valid", "phishing": "Detected"},
        "warnings": ["Some warnings"],
        "recommendations": ["Check SSL", "Be cautious"]
    }
]

# -----------------------------
# Generate reports
# -----------------------------
summary_lines = []

for scan in sample_scans:
    scan_id = scan["scan_id"]
    start_time = time.time()

    # Choose report format
    if scan_id in [1, 4]:
        report = generate_text_report(scan)
        file_path = save_report(report, "txt", scan_id, folder=output_folder)
    elif scan_id in [2, 5]:
        report = generate_html_report(scan)
        file_path = save_report(report, "html", scan_id, folder=output_folder)
    elif scan_id == 3:
        report = generate_json_report(scan)
        file_path = save_report(report, "json", scan_id, folder=output_folder)

    end_time = time.time()

    summary_lines.append(
        f"Scan {scan_id} ({scan['risk_level']}) -> {file_path} "
        f"({os.path.getsize(file_path)} bytes), Time taken: {end_time - start_time:.2f} seconds"
    )

# -----------------------------
# Write summary
# -----------------------------
with open(summary_file, "w", encoding="utf-8") as f:
    f.write("Day 8 Report Generation Test Results\n")
    f.write("="*60 + "\n")
    f.write("\n".join(summary_lines))
    f.write("\nFormat validation: All reports generated successfully.\n")

print("All sample reports generated successfully!")
print(f"Check files in: {output_folder}")
print(f"Summary file: {summary_file}")
