import requests

api_url = "http://127.0.0.1:8000/api/validate-url"

 test_urls = [
    "https://google.com",
    "amazon.com",
    "http://flipkart.com",
    "not a url",
    "www.myntra.com",
    "https://www.paytm.com/wallet",
    "",
    "ftp://example.com",
    "https://sub.domain.example.com",
    "invalid..domain"
]

with open("tests/outputs/day1_api_test/results.txt","w") as f:
    f.write("Day 1 - API Endpoint Test Results\n")
    f.write("="*40 + "\n")
    f.write(f"API Running: {api_url}\n\n")

    all+passed = True

    for i, url in enumerate(test_urls, 1):
        response = requests.post(api_url, json={"url": url})
        f.write(f"Test {i}: POST /api/validate-url\n")
        f.write(f"Body: {{'url': '{url}'}}\n")
        f.write(f"Status Code: {response.status_code}\n")
        f.write(f"Response: {response.json() if response.status_code == 200 else response.text}\n\n")
        if response.status_code != 200:
            all_passed = False

    
    f.write("Summary:\n")
    f.write(f"- Endpoint working: {'Yes' if all_passed else 'No'}\n")
    f.write(f"- All tests passed: {'Yes' if all_passed else 'No'}\n")

