import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings - reads from environment variables"""

    # App info
    APP_NAME: str = os.getenv("APP_NAME", "Phishing Detection System")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Server config
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    #API info(for docs)
    API_DESCRIPTION:str="""
    Phishing Detection System API

    This API helps identify fake/phishing websites by analyzing:
    *Domain similarity and typosquatting
    *SSL certificate validity
    *Security headers
    *Suspicious URL patterns
    """

settings = Settings()
