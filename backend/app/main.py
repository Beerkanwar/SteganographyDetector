from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import crypto, ml

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for secure image steganography and steganalysis",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(crypto.router, prefix=settings.API_V1_STR, tags=["Crypto & Stego"])
app.include_router(ml.router, prefix=settings.API_V1_STR, tags=["Steganalysis"])
