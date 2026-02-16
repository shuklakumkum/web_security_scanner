# Web Security Scanner Backend API

A complete backend system that scans URLs and detects phishing and security risks using multiple analysis techniques.

The system validates URLs, analyzes domains, checks SSL certificates, inspects security headers, applies advanced phishing detection, stores scan history, and generates reports.

This backend is fully tested and documented and is ready for frontend integration.

---

## Project Overview

This project was developed in phases over 9 days.

### Phase 2 – Domain Analysis (Days 1–3)
- URL validation
- Domain similarity checking
- Suspicious pattern detection
- Complete scan endpoint

### Phase 3 – Security Checks (Days 4–6)
- SSL certificate analysis
- Security headers analysis
- Database integration
- Scan history API

### Phase 4 – Advanced Features (Days 7–9)
- Advanced phishing detection
- Report generation
- Full system testing
- Complete documentation

---

## Features

### URL & Domain Checks
- URL validation
- Domain extraction
- Typosquatting detection
- Suspicious domain pattern detection

### Security Checks
- HTTPS verification
- SSL certificate validation
- Certificate expiry detection
- Security headers analysis

### Advanced Detection
- URL length detection
- IP address in URL detection
- Suspicious keyword detection
- Special character analysis
- Redirect chain detection

### Data Storage
- SQLite database storage
- Scan history tracking
- Domain scan history retrieval

### Reporting System
Reports available in:
- Text format
- JSON format
- HTML format

Reports include:
- Scan summary
- Risk score
- Warnings
- Recommendations
- All check results

---

## Installation Instructions

### 1. Clone Repository
```bash
git clone <repository_url>
cd web_security_scanner
