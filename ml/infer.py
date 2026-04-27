import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as T
import io
import os

from ml.config import Config
from ml.model import get_model

# Global model instance for fast inference
_model = None

def get_inference_model():
    global _model
    if _model is None:
        _model = get_model(pretrained=False) # Don't download pretrained weights for inference
        checkpoint_path = os.path.join(Config.CHECKPOINT_DIR, "best_model.pth")
        if os.path.exists(checkpoint_path):
            checkpoint = torch.load(checkpoint_path, map_location=Config.DEVICE)
            _model.load_state_dict(checkpoint['model_state_dict'])
        _model.eval()
    return _model

transform = T.Compose([
    T.Resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_image(file_bytes: bytes) -> dict:
    """
    Used by the backend to detect steganography.
    Returns real model probabilities.
    """
    model = get_inference_model()
    
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(Config.DEVICE)
    
    with torch.no_grad():
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)[0]
        
    confidence_stego = probs[1].item()
    confidence_clean = probs[0].item()
    
    label = "stego" if confidence_stego > 0.5 else "clean"
    confidence = confidence_stego if label == "stego" else confidence_clean
    
    return {
        "label": label,
        "confidence": round(confidence * 100, 2)
    }
