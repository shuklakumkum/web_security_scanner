from fastapi import FastAPI
<<<<<<< Updated upstream
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.scan import router as scan_router
from src.api.routes.health import router as health_router
from src.config.settings import settings
=======
from config.settings import settings
from api.router import health
from api.routes.health import router as health_router
>>>>>>> Stashed changes

app = FastAPI()

# ✅ CORS MUST BE BEFORE ROUTERS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ← TEMP FIX
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< Updated upstream
# ✅ ROUTERS
app.include_router(scan_router, prefix="/api")
app.include_router(health_router, prefix="/api")
=======
app.add_exception_handler(PhishingDetectionError,phishing_error_handler)

app.include_router(health_router)
>>>>>>> Stashed changes

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
    }