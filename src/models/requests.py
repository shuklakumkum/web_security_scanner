from pydantic import BaseModel, HttpUrl

class ScanRequest(BaseModel):
    """
    Request body model for /api/scan endpoint.

    Example:
    {
        "url": "https://example.com"
    }
    """
    url: HttpUrl
