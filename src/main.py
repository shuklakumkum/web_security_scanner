from fastapi import FastAPI
from src.api.routes import scan


app = FastAPI(title="Web Security Scanner API")

from src.config.settings import settings
from src.api.routes.health import router as health_router
from src.api.exceptions import (
    PhishingDetectionError,
    phishing_error_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.API_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_exception_handler(
    PhishingDetectionError,
    phishing_error_handler
)

app.include_router(health_router)
app.include_router(scan.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }
