import os
import sys
from fastapi import HTTPException
from app.models.schemas import DetectResponse

# Add the project root to sys.path so we can import the ML module from the adjacent folder
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from ml.infer import predict_image
except ImportError as e:
    # Fallback if ml module is somehow missing
    predict_image = None
    print(f"Failed to import ML inference module: {e}")

async def predict_stego(file_bytes: bytes) -> DetectResponse:
    """
    Passes the image to the PyTorch Steganalysis model and returns true confidence scores.
    """
    if predict_image is None:
        raise HTTPException(
            status_code=503,
            detail="ML Inference Engine not available. Ensure the ml package is accessible."
        )
        
    try:
        # predict_image is synchronous, but we can run it in a threadpool in a real prod scenario.
        # For this prototype, blocking the async thread for inference is acceptable.
        result = predict_image(file_bytes)
        return DetectResponse(
            label=result["label"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}"
        )
