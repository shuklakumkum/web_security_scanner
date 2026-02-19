from fastapi import FastAPI
from src.config.settings import settings
from src.api.routes.scan import router as scan_router
from src.api.routes.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.API_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(scan_router, prefix="/api")
app.include_router(health_router, prefix="/api")

@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
