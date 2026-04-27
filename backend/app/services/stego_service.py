import zlib
import numpy as np
from PIL import Image
from fastapi import HTTPException
import struct

# We prepend a 4-byte header indicating the size of the embedded payload in bytes
HEADER_SIZE = 4 

def embed_data(img: Image.Image, payload: bytes) -> Image.Image:
    """
    Compresses payload and embeds it into the LSBs of the image.
    Format: [4-byte payload length] + [compressed_payload]
    """
    # 1. Compress the payload
    compressed_payload = zlib.compress(payload)
    
    # 2. Add size header
    payload_size = len(compressed_payload)
    header = struct.pack(">I", payload_size) # 4 bytes unsigned int, big-endian
    full_payload = header + compressed_payload
    
    # 3. Check capacity
    width, height = img.size
    channels = len(img.getbands())
    total_pixels = width * height
    capacity_bytes = (total_pixels * channels) // 8
    
    if len(full_payload) > capacity_bytes:
        raise HTTPException(
            status_code=400, 
            detail=f"Payload too large. Capacity: {capacity_bytes}B, Required: {len(full_payload)}B"
        )
        
    # 4. Convert image to numpy array
    img_arr = np.array(img)
    flat_arr = img_arr.flatten()
    
    # 5. Convert payload to bits
    payload_bits = np.unpackbits(np.frombuffer(full_payload, dtype=np.uint8))
    
    # 6. Embed: Clear LSB and set to payload bit
    flat_arr[:len(payload_bits)] = (flat_arr[:len(payload_bits)] & ~1) | payload_bits
    
    # 7. Reshape and return
    stego_arr = flat_arr.reshape(img_arr.shape)
    return Image.fromarray(stego_arr, mode=img.mode), len(full_payload)

def extract_data(img: Image.Image) -> bytes:
    """
    Extracts the payload from the LSBs of the image, decompresses it.
    """
    # 1. Convert to flat array
    img_arr = np.array(img)
    flat_arr = img_arr.flatten()
    
    # 2. Extract header bits (4 bytes = 32 bits)
    header_bits = flat_arr[:32] & 1
    header_bytes = np.packbits(header_bits)
    
    # 3. Unpack header
    try:
        payload_size = struct.unpack(">I", header_bytes.tobytes())[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to read payload size header. Image may not contain a payload or is corrupted.")
        
    # Validation: sanity check on payload size
    capacity_bytes = len(flat_arr) // 8
    if payload_size == 0 or payload_size > capacity_bytes - HEADER_SIZE:
        raise HTTPException(status_code=400, detail="Invalid payload size detected. This image likely does not contain a steganographic payload.")
        
    # 4. Extract payload bits
    total_bits_to_read = (HEADER_SIZE + payload_size) * 8
    payload_bits = flat_arr[32:total_bits_to_read] & 1
    
    # 5. Pack bits to bytes
    compressed_payload = np.packbits(payload_bits).tobytes()
    
    # 6. Decompress
    try:
        payload = zlib.decompress(compressed_payload)
        return payload
    except zlib.error:
        raise HTTPException(status_code=400, detail="Failed to decompress payload. The image might be corrupted or not contain a valid steganographic payload.")
