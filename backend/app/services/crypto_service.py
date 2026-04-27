import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import HTTPException
import base64

from app.core.config import settings

def generate_key() -> str:
    """Generates a secure AES-256 key and returns it as a Base64 string."""
    key = AESGCM.generate_key(bit_length=256)
    return base64.b64encode(key).decode('utf-8')

def encrypt_payload(plaintext: bytes, key_b64: str) -> bytes:
    """
    Encrypts a payload using AES-256-GCM.
    Returns: nonce (12 bytes) + ciphertext + auth tag (16 bytes implicitly added by AESGCM).
    """
    try:
        key = base64.b64decode(key_b64)
        if len(key) != 32:
            raise ValueError("Key must be 256-bit (32 bytes)")
            
        aesgcm = AESGCM(key)
        nonce = os.urandom(settings.NONCE_SIZE)
        
        # We don't use associated data (AAD) for now, but could tie it to image hash if desired
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
        
        # Prepend nonce to the ciphertext
        return nonce + ciphertext
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

def decrypt_payload(encrypted_payload: bytes, key_b64: str) -> bytes:
    """
    Decrypts a payload using AES-256-GCM.
    Expects payload format: nonce (12 bytes) + ciphertext + auth tag.
    """
    try:
        key = base64.b64decode(key_b64)
        if len(key) != 32:
            raise ValueError("Key must be 256-bit (32 bytes)")
            
        if len(encrypted_payload) < settings.NONCE_SIZE + 16: # nonce + tag
            raise ValueError("Encrypted payload is too short or corrupted.")
            
        nonce = encrypted_payload[:settings.NONCE_SIZE]
        ciphertext = encrypted_payload[settings.NONCE_SIZE:]
        
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
        return plaintext
    except Exception as e:
        # Cryptography will raise InvalidTag if authentication fails
        raise HTTPException(status_code=400, detail=f"Decryption failed or data corrupted: {str(e)}")
