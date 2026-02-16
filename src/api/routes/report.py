from fastapi import APIRouter
from pydantic import BaseModel
from src.services.report_generator import generate_report

router = APIRouter(
    prefix="/api",
    tags=["Reports"]
)

class ReportRequest(BaseModel):
    scan_id: int

@router.post("/generate_report", tags=["Reports"])
def generate_report_endpoint(request: ReportRequest):
    """
    Generates a text/HTML report for a given scan_id
    """
    report_content = generate_report(request.scan_id)
    return {
        "scan_id": request.scan_id,
        "report": report_content
    }
