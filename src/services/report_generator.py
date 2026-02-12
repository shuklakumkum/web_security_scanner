import json
import os
from datetime import datetime

# -------------------------------
# TEXT REPORT
# -------------------------------
def generate_text_report(scan_result: dict) -> str:
    lines = []

    lines.append("WEB SECURITY SCAN REPORT")
    lines.append("=" * 50)

    lines.append(f"URL: {scan_result.get('url')}")
    lines.append(f"Domain: {scan_result.get('domain')}")
    lines.append(
        f"Risk Score: {scan_result.get('risk_score')} "
        f"({scan_result.get('risk_level')})"
    )
    lines.append("")

    lines.append("CHECK RESULTS")
    lines.append("-" * 50)

    checks = scan_result.get("checks", {})
    for name, result in checks.items():
        lines.append(f"{name}: {result}")

    lines.append("")
    lines.append("WARNINGS")
    lines.append("-" * 50)

    for warning in scan_result.get("warnings", []):
        lines.append(f"- {warning}")

    lines.append("")
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 50)

    for rec in scan_result.get("recommendations", []):
        lines.append(f"- {rec}")

    lines.append("")
    lines.append("=" * 50)
    lines.append(f"Generated at: {datetime.utcnow()}")

    return "\n".join(lines)


# -------------------------------
# JSON REPORT
# -------------------------------
def generate_json_report(scan_result: dict) -> str:
    return json.dumps(scan_result, indent=4, default=str)


# -------------------------------
# HTML REPORT
# -------------------------------
def _risk_color(level: str) -> str:
    if level.lower() == "low":
        return "green"
    if level.lower() == "medium":
        return "orange"
    return "red"


def generate_html_report(scan_result: dict) -> str:
    color = _risk_color(scan_result.get("risk_level", "High"))

    checks_html = ""
    for name, result in scan_result.get("checks", {}).items():
        checks_html += f"<li><b>{name}</b>: {result}</li>"

    warnings_html = "".join(
        f"<li>{w}</li>" for w in scan_result.get("warnings", [])
    )

    rec_html = "".join(
        f"<li>{r}</li>" for r in scan_result.get("recommendations", [])
    )

    html = f"""
    <html>
    <head>
        <title>Scan Report</title>
        <style>
            body {{
                font-family: Arial;
                margin: 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 20px;
                border-radius: 8px;
            }}
            .risk {{
                color: {color};
                font-weight: bold;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Security Scan Report</h1>

            <p><b>URL:</b> {scan_result.get('url')}</p>
            <p><b>Domain:</b> {scan_result.get('domain')}</p>

            <p>
                <b>Risk Score:</b>
                <span class="risk">
                    {scan_result.get('risk_score')}
                    ({scan_result.get('risk_level')})
                </span>
            </p>

            <h2>Checks</h2>
            <ul>{checks_html}</ul>

            <h2>Warnings</h2>
            <ul>{warnings_html}</ul>

            <h2>Recommendations</h2>
            <ul>{rec_html}</ul>

            <p>Generated at: {datetime.utcnow()}</p>
        </div>
    </body>
    </html>
    """

    return html


# -------------------------------
# SAVE REPORT
# -------------------------------
def save_report(report: str, format: str, scan_id: int, folder: str = "reports") -> str:
    """
    Save a report to the specified folder.
    Returns the full file path.
    """
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_{scan_id}_{timestamp}.{format}"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    return filepath
