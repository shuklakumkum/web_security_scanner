from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional,Dict,Any

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status:str=Field(example="healthy")
    timestamp:str=Field(example="2024-01_15T10:30:00Z")
    message:str=Field(example="API is running normally")

class DetailedHealthResponse(BaseModel):
   """Response model for detailed health check"""
   status: str
   app_name: str
   version: str
   debug_mode: bool
   timestamp: str
   checks: Dict[str, str]

class SuccessRespone(BaseModel):
  """Generic success response wrapper"""
   success:bool=Field(default=True)
   message:str
   data:Optional[Dict[str,Any]]=None


#Future use-URL scan ke liye
class URLScanRequest(BaseModel):
    """Request model for URL scanning"""
   url:str=Field(
    min_length=10,
    max_length=2048,
    example="https://amazon.com"
   )  

class URLScanResponse(BaseModel):
  """Response model for URL scan results"""
  success: bool
  url: str
  is_suspicious: bool
  risk_score: int = Field(ge=0, le=100) # 0-100
  message: str
  timestamp: str