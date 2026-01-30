from fastapi import FastAPI
from config.settings import settings
from api.routes.health import router as health_router

#FastAPI app create karo
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.API_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health_router)

@app.get("/",tags=["Root"])
def root():
    """Root endpoint-API welcome message"""
    return{
        "message":f"Welcome to{settings.APP_NAME}",
        "version":settings.APP_VERSION,
        "docs":"/docs",
        "health":"/health"
    }