import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime


def analyze_ssl(url: str):
    try:
        parsed = urlparse(url)

        # Check HTTPS
        has_https = parsed.scheme.lower() == "https"
        if not has_https:
            return {
                "has_https": False,
                "certificate_valid": False,
                "certificate_info": {}
            }

        hostname = parsed.hostname
        port = 443

        # Create SSL context
        context = ssl.create_default_context()

        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # Check expiry
        not_after = cert.get("notAfter")
        expiry_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")

        certificate_valid = expiry_date > datetime.utcnow()

        return {
            "has_https": True,
            "certificate_valid": certificate_valid,
            "certificate_info": {
                "issuer": cert.get("issuer"),
                "subject": cert.get("subject"),
                "expiry_date": not_after,
            }
        }

    except Exception:
        return {
            "has_https": True,
            "certificate_valid": False,
            "certificate_info": {}
        }