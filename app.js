const API_URL = "http://localhost:8000/api/scan";  // localhost, NOT 127.0.0.1

async function scanURL(url) {
    if (!url) {
        alert("Please enter a URL");
        return;
    }

    const resultsDiv = document.getElementById("resultsContent");
    resultsDiv.textContent = "Scanning...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();
        resultsDiv.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resultsDiv.textContent = `Error: ${err.message}`;
        console.error(err);
    }
}
