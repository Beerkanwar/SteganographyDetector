import base64
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from app.models.schemas import EncryptResponse, DecryptResponse
from app.utils.image_utils import validate_image, calculate_capacity, image_to_bytes
from app.services.crypto_service import generate_key, encrypt_payload, decrypt_payload
from app.services.stego_service import embed_data, extract_data

router = APIRouter()

@router.post("/encrypt", response_model=EncryptResponse)
async def encrypt(
    image: UploadFile = File(...),
    plaintext: str = Form(...)
):
    # 1. Validate image
    file_bytes = await image.read()
    img = validate_image(file_bytes)
    
    # 2. Check Capacity
    capacity_bytes = calculate_capacity(img)
    plaintext_bytes = plaintext.encode('utf-8')
    
    # 3. Generate key and encrypt
    key_b64 = generate_key()
    encrypted_payload = encrypt_payload(plaintext_bytes, key_b64)
    
    # 4. Embed data (compresses internally)
    stego_img, payload_size_bytes = embed_data(img, encrypted_payload)
    
    # 5. Convert back to base64
    stego_bytes = image_to_bytes(stego_img, format="PNG")
    stego_b64 = base64.b64encode(stego_bytes).decode('utf-8')
    
    utilization_percent = (payload_size_bytes / capacity_bytes) * 100 if capacity_bytes > 0 else 0
    
    return EncryptResponse(
        key=key_b64,
        stego_image=stego_b64,
        capacity_bytes=capacity_bytes,
        payload_size_bytes=payload_size_bytes,
        utilization_percent=utilization_percent
    )

@router.post("/decrypt", response_model=DecryptResponse)
async def decrypt(
    image: UploadFile = File(...),
    key: str = Form(...)
):
    # 1. Validate image
    file_bytes = await image.read()
    img = validate_image(file_bytes)
    
    # 2. Extract data (decompresses internally)
    encrypted_payload = extract_data(img)
    
    # 3. Decrypt
    plaintext_bytes = decrypt_payload(encrypted_payload, key)
    
    # 4. Decode
    try:
        plaintext = plaintext_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Decrypted data is not valid UTF-8 string.")
        
    return DecryptResponse(plaintext=plaintext)
