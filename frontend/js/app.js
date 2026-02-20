console.log("App.js loaded successfully");

const API_URL = "http://127.0.0.1:8000/api/scan";

function scanURL() {

    const inputElement = document.getElementById("urlInput");

    if (!inputElement) {
        alert("Input element not found!");
        return;
    }

    const url = inputElement.value.trim();

    console.log("Entered URL:", url);

    if (url === "") {
        alert("Please enter a URL");
        return;
    }

    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            displayDetailedChecks(data);
        })
        .catch(error => {
            console.error("Fetch error:", error);
            alert("Error scanning URL: " + error.message);
        });
}


function displayResults(data) {

    document.getElementById("resultsSection").style.display = "block";

    const score = data.risk_score || 0;
    document.getElementById("riskScore").innerText = score;

    const riskLevel = document.getElementById("riskLevel");
    riskLevel.classList.remove("low", "medium", "high");

    if (score <= 30) {
        riskLevel.innerText = "Low";
        riskLevel.classList.add("low");
    } else if (score <= 70) {
        riskLevel.innerText = "Medium";
        riskLevel.classList.add("medium");
    } else {
        riskLevel.innerText = "High";
        riskLevel.classList.add("high");
    }

    document.getElementById("resultUrl").innerText = data.url || "-";
    document.getElementById("resultDomain").innerText = data.domain || "-";
    document.getElementById("resultTimestamp").innerText = data.timestamp || "-";
}


function displayDetailedChecks(data) {

    const ssl = data.checks?.ssl || {};
    const headers = data.checks?.security_headers || {};
    const domain = data.checks?.domain_analysis || {};
    const advanced = data.checks?.advanced_detection || {};

    // SSL Check
    const sslStatus = ssl.certificate_valid ? "✓ Pass" : "✗ Fail";
    document.getElementById("sslCheck").innerHTML =
        `<strong>SSL Certificate:</strong> ${sslStatus}`;

    // Security Headers
    const missingHeaders = headers.missing_headers || [];
    const headersStatus =
        missingHeaders.length === 0
            ? "✓ All Present"
            : `⚠ Missing ${missingHeaders.length} headers`;

    document.getElementById("headersCheck").innerHTML =
        `<strong>Security Headers:</strong> ${headersStatus}`;

    // Domain Analysis
    const domainStatus = domain.is_suspicious
        ? "✗ Suspicious Domain"
        : "✓ Safe Domain";

    document.getElementById("domainCheck").innerHTML =
        `<strong>Domain Analysis:</strong> ${domainStatus}`;

    // Advanced Detection
    const advancedWarnings = advanced.warnings || [];
    const advancedStatus =
        advancedWarnings.length > 0
            ? `⚠ ${advancedWarnings.length} issues found`
            : "✓ No Issues Detected";

    document.getElementById("advancedCheck").innerHTML =
        `<strong>Advanced Detection:</strong> ${advancedStatus}`;
}