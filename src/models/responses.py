from pydantic import BaseModel
from typing import Dict, List


# Health endpoint response
class HealthResponse(BaseModel):
    status: str
    message: str


class DetailedHealthResponse(BaseModel):
    status: str
    message: str
    version: str


# Day 3 scan response
class ScanResult(BaseModel):
    url: str
    domain: str
    is_suspicious: bool
    risk_score: int
    risk_level: str
    timestamp: str

    checks: Dict
    warnings: List[str]
    recommendations: List[str]
