console.log("App.js loaded successfully");

const API_URL = "http://127.0.0.1:8000/api/scan"; // Replace with your API
const SCANS_API_URL = "http://127.0.0.1:8000/api/scans";
const TIMEOUT = 20000; // 20 seconds

// ===== SCAN WEBSITE =====
async function scanURL() {
    const inputElement = document.getElementById("urlInput");
    const url = inputElement.value.trim();
    if (!url) return showError("Enter a valid URL");

    try { new URL(url); } catch { return showError("Invalid URL entered"); }

    clearResults();
    hideError();
    showLoading();

    try {
        const controller = new AbortController();
        const fetchPromise = fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url }),
            signal: controller.signal
        }).then(res => res.ok ? res.json() : Promise.reject(`HTTP ${res.status}`));

        const timeoutPromise = new Promise((_, reject) =>
            setTimeout(() => { controller.abort(); reject("API timeout"); }, TIMEOUT)
        );

        const data = await Promise.race([fetchPromise, timeoutPromise]);

        displayResults(data);
        displayDetailedChecks(data);
        const { warnings, recommendations } = extractWarningsAndRecommendations(data);
        displayWarnings(warnings);
        displayRecommendations(recommendations);

        addScanToHistory({
            url: data.url,
            risk_level: data.risk_score <= 30 ? "Low" : data.risk_score <= 70 ? "Medium" : "High",
            timestamp: data.timestamp || new Date().toISOString(),
            issues: warnings
        });

    } catch (err) {
        showError(err);
        console.error(err);
    } finally { hideLoading(); }
}

// ===== HELPERS =====
function showLoading() {
    const results = document.getElementById("resultsSection");
    results.style.display = "block";
    results.innerHTML = `<div class="loading-spinner">Scanning... ⏳</div>`;
}

function hideLoading() {
    const spinner = document.querySelector(".loading-spinner");
    if (spinner) spinner.remove();
}

function showError(msg) {
    const div = document.getElementById("errorMessage");
    div.innerText = msg;
}

function hideError() {
    document.getElementById("errorMessage").innerText = "";
}

function clearResults() {
    document.getElementById("resultsSection").innerHTML = "";
}

// ===== DISPLAY RESULTS =====
function displayResults(data) {
    const results = document.getElementById("resultsSection");
    results.style.display = "block";

    const score = data.risk_score || 0;
    const riskLevel = score <= 30 ? "Low" : score <= 70 ? "Medium" : "High";

    results.innerHTML = `
        <div class="result-card">
            <h2>Scan Results</h2>
            <div class="score-box">
                <div class="risk-score">${score}</div>
                <div class="risk-badge ${riskLevel.toLowerCase()}">${riskLevel}</div>
            </div>
            <div class="result-details">
                <p><strong>URL:</strong> ${data.url}</p>
                <p><strong>Domain:</strong> ${data.domain || "-"}</p>
                <p><strong>Timestamp:</strong> ${formatTimestamp(data.timestamp)}</p>
            </div>
            <div id="detailedChecks" class="detailed-checks"></div>
            <div id="warnings-section" class="detailed-checks">
                <h3>Warnings ⚠️</h3><ul id="warnings-list"></ul>
            </div>
            <div id="recommendations-section" class="detailed-checks">
                <h3>Recommendations ℹ️</h3><ul id="recommendations-list"></ul>
            </div>
        </div>`;
}

function displayDetailedChecks(data) {
    const ssl = data.checks?.ssl || {};
    const headers = data.checks?.security_headers || {};
    const domain = data.checks?.domain_analysis || {};
    const advanced = data.checks?.advanced_detection || {};

    const detailed = document.getElementById("detailedChecks");
    detailed.innerHTML = `
        <h3>Detailed Security Checks</h3>
        <div><strong>SSL Certificate:</strong> ${ssl.certificate_valid ? "✓ Pass" : "✗ Fail"}</div>
        <div><strong>Security Headers:</strong> ${headers.missing_headers?.length ? "⚠ Missing " + headers.missing_headers.join(", ") : "✓ All Present"}</div>
        <div><strong>Domain Analysis:</strong> ${domain.is_suspicious ? "✗ Suspicious" : "✓ Safe"}</div>
        <div><strong>Advanced Detection:</strong> ${advanced.warnings?.length ? `⚠ ${advanced.warnings.length} issues` : "✓ No Issues Detected"}</div>
    `;
}

function extractWarningsAndRecommendations(data) {
    const warnings = [];
    const recommendations = [];

    if (!data.checks?.ssl?.certificate_valid) {
        warnings.push("No HTTPS / Invalid SSL certificate");
        recommendations.push("Enable HTTPS and fix SSL certificate");
    }

    const missingHeaders = data.checks?.security_headers?.missing_headers || [];
    if (missingHeaders.length > 0) {
        warnings.push(`Missing security headers: ${missingHeaders.join(", ")}`);
        recommendations.push("Add missing security headers");
    }

    if (data.checks?.domain_analysis?.is_suspicious) {
        warnings.push("Suspicious domain detected");
        recommendations.push("Check domain carefully");
    }

    const adv = data.checks?.advanced_detection?.warnings || [];
    adv.forEach(w => warnings.push(w));
    if (adv.length > 0) recommendations.push("Investigate advanced detection issues");

    return { warnings, recommendations };
}

function displayWarnings(warnings) {
    const list = document.getElementById("warnings-list");
    list.innerHTML = "";
    if (!warnings.length) return list.innerHTML = `<li>No warnings detected</li>`;
    warnings.forEach(w => { const li = document.createElement("li"); li.textContent = w; list.appendChild(li); });
}

function displayRecommendations(recs) {
    const list = document.getElementById("recommendations-list");
    list.innerHTML = "";
    if (!recs.length) return list.innerHTML = `<li>No recommendations needed</li>`;
    recs.forEach(r => { const li = document.createElement("li"); li.textContent = r; list.appendChild(li); });
}

// ===== HISTORY / RECENT SCANS =====
function addScanToHistory(scan) {
    const list = document.getElementById("scans-list");
    const li = document.createElement("li");
    const ts = new Date(scan.timestamp);
    const displayTime = isNaN(ts) ? "Unknown" : ts.toLocaleString();
    li.innerHTML = `<strong>${scan.url}</strong> - Risk: <span class="${scan.risk_level.toLowerCase()}">${scan.risk_level}</span> - ${displayTime}`;
    li.addEventListener("click", () => showScanDetails(scan));
    list.prepend(li);
}

function showScanDetails(scan) {
    const details = document.getElementById("details-content");
    const ts = new Date(scan.timestamp);
    const displayTime = isNaN(ts) ? "Unknown" : ts.toLocaleString();
    details.innerHTML = `
        <p><strong>URL:</strong> ${scan.url}</p>
        <p><strong>Risk Level:</strong> ${scan.risk_level}</p>
        <p><strong>Timestamp:</strong> ${displayTime}</p>
        <p><strong>Issues:</strong> ${scan.issues?.length ? scan.issues.join(", ") : "None"}</p>
    `;
    document.getElementById("scan-details").style.display = "block";
}

// ===== CLOSE MODAL =====
document.getElementById("close-details").addEventListener("click", () => {
    document.getElementById("scan-details").style.display = "none";
});
document.getElementById("close-details-btn").addEventListener("click", () => {
    document.getElementById("scan-details").style.display = "none";
});

// ===== FORMAT TIMESTAMP =====
function formatTimestamp(ts) {
    if (!ts) return "Unknown";
    const date = new Date(ts);
    return isNaN(date) ? "Unknown" : date.toLocaleString();
}

// ===== INIT =====
window.addEventListener("DOMContentLoaded", () => {
    console.log("Page Loaded");
});