import requests
import os
from PIL import Image
import io
import base64

API_BASE = "http://localhost:8000/api/v1"

def create_dummy_image() -> str:
    """Create a basic RGB PNG image for testing and return the path."""
    path = "test_carrier.png"
    img = Image.new("RGB", (256, 256), color=(73, 109, 137))
    img.save(path, format="PNG")
    return path

def test_encrypt_decrypt():
    print("=== Testing Encrypt & Decrypt Flow ===")
    img_path = create_dummy_image()
    
    # 1. Test Encrypt
    secret_msg = "This is a highly confidential secret payload!"
    print(f"[*] Hiding message: '{secret_msg}'")
    
    with open(img_path, "rb") as f:
        res = requests.post(
            f"{API_BASE}/encrypt",
            files={"image": ("test_carrier.png", f, "image/png")},
            data={"plaintext": secret_msg}
        )
        
    if res.status_code != 200:
        print(f"[!] Encrypt failed: {res.text}")
        return
        
    data = res.json()
    key = data["key"]
    stego_b64 = data["stego_image"]
    print(f"[+] Encryption successful!")
    print(f"    AES-256 Key: {key}")
    print(f"    Payload Size: {data['payload_size_bytes']} bytes")
    print(f"    Capacity Used: {data['utilization_percent']:.2f}%")
    
    # Save stego image locally for the next step
    stego_path = "test_stego.png"
    with open(stego_path, "wb") as f:
        f.write(base64.b64decode(stego_b64))
        
    # 2. Test Decrypt
    print("\n[*] Extracting and Decrypting...")
    with open(stego_path, "rb") as f:
        res = requests.post(
            f"{API_BASE}/decrypt",
            files={"image": ("test_stego.png", f, "image/png")},
            data={"key": key}
        )
        
    if res.status_code != 200:
        print(f"[!] Decrypt failed: {res.text}")
        return
        
    decrypted_msg = res.json()["plaintext"]
    print(f"[+] Decryption successful! Extracted message: '{decrypted_msg}'")
    
    assert decrypted_msg == secret_msg, "Data mismatch!"
    print("[+] Flow validated successfully!\n")

def test_detect():
    print("=== Testing Steganalysis Detect Flow ===")
    img_path = "test_carrier.png"
    if not os.path.exists(img_path):
        img_path = create_dummy_image()
        
    with open(img_path, "rb") as f:
        res = requests.post(
            f"{API_BASE}/detect",
            files={"image": ("test_carrier.png", f, "image/png")}
        )
        
    if res.status_code == 200:
        print(f"[+] Detect successful: {res.json()}")
    elif res.status_code == 503:
        print("[*] Detect returned 503 (Expected if ML model is not yet trained/loaded).")
        print(f"    Message: {res.json()['detail']}")
    else:
        print(f"[!] Detect failed: {res.text}")

if __name__ == "__main__":
    print("Please ensure the FastAPI backend is running on localhost:8000 before executing.\n")
    try:
        test_encrypt_decrypt()
        test_detect()
    except requests.exceptions.ConnectionError:
        print("[!] Connection Error: Is the backend server running?")
    finally:
        # Cleanup
        for p in ["test_carrier.png", "test_stego.png"]:
            if os.path.exists(p):
                os.remove(p)
