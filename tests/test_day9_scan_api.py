import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.url_validator import validate_url
from src.services.domain_checker import analyze_domain

client = TestClient(app)

# ---------------------------
# API Endpoint Tests
# ---------------------------

def test_scan_safe_url_api():
    """Test a safe URL via the API endpoint"""
    url = "https://example.com"
    response = client.post("/api/scan", json={"url": url})  # <-- added /api
    
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == url
    assert data["risk_level"] in ["Low", "Medium", "High"]
    assert data["is_suspicious"] is False

def test_scan_suspicious_url_api():
    """Test a suspicious URL via the API endpoint"""
    url = "http://192.168.1.1"
    response = client.post("/api/scan", json={"url": url})  # <-- added /api
    
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == url
    assert data["risk_level"] == "High"
    assert data["is_suspicious"] is True

# ---------------------------
# Service Function Tests
# ---------------------------

def test_url_validator_safe():
    """Directly test validate_url() with a safe URL"""
    url = "https://example.com"
    result = validate_url(url)
    
    assert result["valid"] is True
    assert result["domain"] == "example.com"
    assert result["scheme"] == "https"

def test_url_validator_invalid():
    """Directly test validate_url() with an invalid URL"""
    url = "ht!tp://invalid-url"
    result = validate_url(url)
    
    assert result["valid"] is False
    assert result["domain"] == ""
    assert "error" in result

def test_domain_checker_safe():
    """Directly test analyze_domain() for a safe domain"""
    result = analyze_domain("example.com")
    
    assert result["is_suspicious"] is False
    assert result["risk_score"] <= 30
    assert isinstance(result["warnings"], list)

def test_domain_checker_suspicious():
    """Directly test analyze_domain() for a suspicious IP"""
    result = analyze_domain("192.168.1.1")
    
    assert result["is_suspicious"] is True
    assert result["risk_score"] > 0
    assert isinstance(result["warnings"], list)
