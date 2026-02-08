import requests
import time

API = "http://127.0.0.1:8000/api/scan"

urls = [
    "https://www.google.com",
    "https://amazon.in",
    "https://www.flipkart.com",
    "https://paytm.com",
    "https://myntra.com",
    "https://amazom.com",
    "https://gooogle.com",
    "https://faceb00k.com",
    "https://flipkart.co",
    "https://paytmm.com",
    "https://amazon-login.com",
    "https://flipkart-offers.xyz",
    "https://secure-paytm-wallet.com",
    "https://google-account-verify.tk",
    "http://facebook.com",
    "https://amazom-secure-login.xyz",
    "https://flipkart-sale-verify-account.ml",
    "http://secure-paytm-login-update.com",
    "https://google-security-alert-urgent.tk",
    "https://faceb00k-password-reset-now.ga",
]

for u in urls:
    start = time.time()
    r = requests.post(API, json={"url": u})
    end = time.time()

    print(u, "->", r.status_code, f"{(end-start)*1000:.2f} ms")
