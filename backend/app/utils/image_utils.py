from fastapi import HTTPException
from PIL import Image
import io

def validate_image(file_bytes: bytes) -> Image.Image:
    """Validates the uploaded file is a valid image and converts to RGB/RGBA."""
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify() # Verify it's an image
        
        # Reopen because verify() closes the file in some Pillow versions
        img = Image.open(io.BytesIO(file_bytes))
        
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
            
        return img
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

def calculate_capacity(img: Image.Image) -> int:
    """
    Calculates the maximum embedding capacity in bytes.
    Using 1 LSB per channel per pixel.
    Capacity = (Width * Height * Channels) bits / 8
    """
    width, height = img.size
    channels = len(img.getbands())
    total_bits = width * height * channels
    return total_bits // 8

def image_to_bytes(img: Image.Image, format: str = "PNG") -> bytes:
    """Converts a PIL Image back to bytes (lossless PNG is crucial for steganography)."""
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()
