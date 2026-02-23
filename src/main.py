from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.scan import router as scan_router
from src.api.routes.health import router as health_router
from src.config.settings import settings


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Web Security Scanner API - Phishing Detection System"
)


# -------------------------------
# CORS Middleware (Must be before routers)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Include API Routers
# -------------------------------
app.include_router(scan_router, prefix="/api", tags=["Scan"])
app.include_router(health_router, prefix="/api", tags=["Health"])


# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "API is running successfully"
    }