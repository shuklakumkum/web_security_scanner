from fastapi import FastAPI
from src.api.routes.scan import router as scan_router

app = FastAPI(
    title="Web Security Scanner",
    version="1.0"
)

app.include_router(scan_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Web Security Scanner running"}
