console.log("App.js loaded successfully");

const API_URL = "http://127.0.0.1:8000/api/scan";
const TIMEOUT = 20000; // 20-second timeout

async function scanURL() {
    const inputElement = document.getElementById("urlInput");
    if (!inputElement) return alert("Input element not found!");
    const url = inputElement.value.trim();

    try { new URL(url); }
    catch (e) { return showError("Invalid URL entered. Please enter a valid URL."); }

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
        }).then(res => { if (!res.ok) throw new Error(`HTTP ${res.status}`); return res.json(); });

        const timeoutPromise = new Promise((_, reject) =>
            setTimeout(() => { controller.abort(); reject(new Error("API timeout. Please try again.")); }, TIMEOUT)
        );

        const data = await Promise.race([fetchPromise, timeoutPromise]);
        displayResults(data);
        displayDetailedChecks(data);
        const { warnings, recommendations } = extractWarningsAndRecommendations(data);
        displayWarnings(warnings);
        displayRecommendations(recommendations);

    } catch (err) { showError(err.message); console.error(err); }
    finally { hideLoading(); }
}

function showLoading() {
    const resultsSection = document.getElementById("resultsSection");
    if (!resultsSection) return;
    resultsSection.style.display = "block";
    resultsSection.innerHTML = `<div class="loading-spinner">Scanning... ⏳</div>`;
}

function hideLoading() { }

function showError(message) {
    let errorDiv = document.getElementById("errorMessage");
    if (!errorDiv) {
        errorDiv = document.createElement("div");
        errorDiv.id = "errorMessage";
        errorDiv.classList.add("error-message");
        const main = document.querySelector("main");
        main.insertBefore(errorDiv, main.firstChild);
    }
    errorDiv.innerText = message;
}

function hideError() { const errorDiv = document.getElementById("errorMessage"); if (errorDiv) errorDiv.remove(); }

function clearResults() {
    const resultsSection = document.getElementById("resultsSection");
    if (resultsSection) resultsSection.innerHTML = "";
}

function displayResults(data) {
    document.getElementById("resultsSection").style.display = "block";
    const score = data.risk_score || 0;
    const riskLevel = score <= 30 ? "Low" : score <= 70 ? "Medium" : "High";

    const resultsHTML = `
        <div class="result-card">
            <h2>Scan Results</h2>
            <div class="score-box">
                <div id="riskScore" class="risk-score">${score}</div>
                <div id="riskLevel" class="risk-badge ${riskLevel.toLowerCase()}">${riskLevel}</div>
            </div>
            <div class="result-details">
                <p><strong>URL:</strong> <span id="resultUrl">${data.url || "-"}</span></p>
                <p><strong>Domain:</strong> <span id="resultDomain">${data.domain || "-"}</span></p>
                <p><strong>Timestamp:</strong> <span id="resultTimestamp">${data.timestamp || "-"}</span></p>
            </div>
            <div id="detailedChecks" class="detailed-checks">
                <h3>Detailed Security Checks</h3>
                <div id="sslCheck"></div>
                <div id="headersCheck"></div>
                <div id="domainCheck"></div>
                <div id="advancedCheck"></div>
            </div>
            <div id="warnings-section" class="detailed-checks">
                <h3>Warnings ⚠️</h3>
                <ul id="warnings-list"></ul>
            </div>
            <div id="recommendations-section" class="detailed-checks">
                <h3>Recommendations ℹ️</h3>
                <ul id="recommendations-list"></ul>
            </div>
        </div>`;
    document.getElementById("resultsSection").innerHTML = resultsHTML;
}

function displayDetailedChecks(data) {
    const ssl = data.checks?.ssl || {};
    const headers = data.checks?.security_headers || {};
    const domain = data.checks?.domain_analysis || {};
    const advanced = data.checks?.advanced_detection || {};

    document.getElementById("sslCheck").innerHTML = `<strong>SSL Certificate:</strong> ${ssl.certificate_valid ? "✓ Pass" : "✗ Fail"}`;
    const missingHeaders = headers.missing_headers || [];
    document.getElementById("headersCheck").innerHTML = `<strong>Security Headers:</strong> ${missingHeaders.length === 0 ? "✓ All Present" : `⚠ Missing ${missingHeaders.join(", ")}`}`;
    document.getElementById("domainCheck").innerHTML = `<strong>Domain Analysis:</strong> ${domain.is_suspicious ? "✗ Suspicious Domain" : "✓ Safe Domain"}`;
    const advancedWarnings = advanced.warnings || [];
    document.getElementById("advancedCheck").innerHTML = `<strong>Advanced Detection:</strong> ${advancedWarnings.length > 0 ? `⚠ ${advancedWarnings.length} issues found` : "✓ No Issues Detected"}`;
}

function displayWarnings(warnings) {
    const warningsList = document.getElementById("warnings-list");
    warningsList.innerHTML = "";
    if (warnings.length === 0) { const li = document.createElement("li"); li.textContent = "No warnings detected"; li.classList.add("clean"); warningsList.appendChild(li); return; }
    warnings.forEach(w => { const li = document.createElement("li"); li.textContent = `⚠️ ${w}`; warningsList.appendChild(li); });
}

function displayRecommendations(recommendations) {
    const recList = document.getElementById("recommendations-list");
    recList.innerHTML = "";
    if (recommendations.length === 0) { const li = document.createElement("li"); li.textContent = "No recommendations needed"; li.classList.add("clean"); recList.appendChild(li); return; }
    recommendations.forEach(r => { const li = document.createElement("li"); li.textContent = `ℹ️ ${r}`; recList.appendChild(li); });
}

function extractWarningsAndRecommendations(data) {
    const warnings = [], recommendations = [];
    if (!data.checks.ssl?.certificate_valid) { warnings.push("No HTTPS / Invalid SSL certificate"); recommendations.push("Enable HTTPS and fix SSL certificate"); }
    const missingHeaders = data.checks.security_headers?.missing_headers || [];
    if (missingHeaders.length > 0) { warnings.push(`Missing security headers: ${missingHeaders.join(", ")}`); recommendations.push("Add missing security headers"); }
    if (data.checks.domain_analysis?.is_suspicious) { warnings.push("Suspicious domain detected"); recommendations.push("Check domain carefully"); }
    const advancedWarnings = data.checks.advanced_detection?.warnings || [];
    advancedWarnings.forEach(w => warnings.push(w));
    if (advancedWarnings.length > 0) recommendations.push("Investigate advanced detection issues");
    return { warnings, recommendations };
}