from pydantic import BaseModel, Field

class EncryptResponse(BaseModel):
    key: str = Field(..., description="Base64 encoded AES-256 key")
    stego_image: str = Field(..., description="Base64 encoded PNG stego image")
    capacity_bytes: int = Field(..., description="Total available embedding capacity in bytes")
    payload_size_bytes: int = Field(..., description="Size of the encrypted and compressed payload in bytes")
    utilization_percent: float = Field(..., description="Percentage of capacity used")

class DecryptResponse(BaseModel):
    plaintext: str = Field(..., description="The extracted and decrypted secret message")

class DetectResponse(BaseModel):
    label: str = Field(..., description="Predicted class (e.g., 'clean' or 'stego')")
    confidence: float = Field(..., description="Softmax probability confidence score")
