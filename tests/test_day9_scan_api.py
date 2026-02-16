# tests/test_day9_final.py

import pytest
from fastapi.testclient import TestClient
from src.main import app  # Your FastAPI app
from src.services import url_validator, domain_checker  # Direct service imports

client = TestClient(app)

# -----------------------------
# API Endpoint Tests
# -----------------------------

def test_scan_safe_url_api():
    """Test safe URL via API endpoint"""
    url = "https://example.com"
    response = client.post("/scan", json={"url": url})
    
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert data["url"] == url
    assert "risk_level" in data
    assert data["risk_level"] in ["Low", "Medium", "High"]
    assert data.get("is_suspicious") is False or data.get("is_suspicious") is None

def test_scan_suspicious_url_api():
    """Test suspicious URL via API endpoint"""
    url = "http://192.168.1.1"
    response = client.post("/scan", json={"url": url})
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_suspicious"] is True
    assert data["risk_level"] == "High"

# -----------------------------
# Direct Service Tests
# -----------------------------

def test_url_validator_safe():
    """Directly test url_validator service"""
    result = url_validator.validate_url("https://example.com")
    assert result["valid"] is True
    assert result["domain"] == "example.com"

def test_url_validator_invalid():
    """Directly test url_validator with invalid URL"""
    result = url_validator.validate_url("htp://bad_url")
    assert result["valid"] is False

def test_domain_checker_suspicious():
    """Directly test domain_checker service for suspicious IP"""
    result = domain_checker.check_domain("http://192.168.1.1")
    assert result["risk_level"] == "High"
    assert result["is_suspicious"] is True

def test_domain_checker_safe():
    """Directly test domain_checker service for safe domain"""
    result = domain_checker.check_domain("https://example.com")
    assert result["risk_level"] in ["Low", "Medium"]
    assert result["is_suspicious"] is False or result["is_suspicious"] is None
