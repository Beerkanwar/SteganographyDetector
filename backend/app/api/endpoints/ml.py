from fastapi import APIRouter, UploadFile, File
from app.models.schemas import DetectResponse
from app.services.ml_service import predict_stego

router = APIRouter()

@router.post("/detect", response_model=DetectResponse)
async def detect(image: UploadFile = File(...)):
    """
    Analyzes an image to determine if it contains a steganographic payload.
    """
    file_bytes = await image.read()
    # Will raise 503 until Phase 3 is implemented
    return await predict_stego(file_bytes)
