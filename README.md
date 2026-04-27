# Steganography Detector Project

A complete, runnable, production-grade web application combining AES-256 secure encryption, image steganography, and deep-learning-based steganalysis detection.

## Architecture & Monorepo Structure

- **`backend/`**: FastAPI application handling API routes, AES-256-GCM encryption/decryption, steganography embedding/extracting, and ML inference.
- **`frontend/`**: Next.js application providing a premium, modern UI with Tailwind CSS and Framer Motion.
- **`ml/`**: PyTorch workspace for training an EfficientNetV2 model on the COCO dataset for steganalysis detection.

## Prerequisites

- Node.js (v18+)
- Python (3.10+)

## Local Development Workflow

### 1. Backend

```bash
cd backend
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Unix: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# The frontend will be available at http://localhost:3000
```

### 3. ML Training (Optional/When needed)

```bash
cd ml
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Unix: source venv/bin/activate
pip install -r requirements.txt
python training/train.py
```