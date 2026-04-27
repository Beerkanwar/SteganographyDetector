# Final Validation & Testing Checklist

Use this checklist to validate the local functionality of the SteganographyDetector project.

## 1. Setup Validation
- [ ] **Backend Env**: Did you create the `.env` file in the root based on `.env.example`?
- [ ] **Python Dependencies**: Did you run `pip install -r backend/requirements.txt`?
- [ ] **Node Dependencies**: Did you run `npm install` inside the `frontend/` directory?

## 2. API Endpoints (Backend)
Run `uvicorn app.main:app --reload` inside `backend/` and verify:
- [ ] `GET http://127.0.0.1:8000/health` returns `{"status":"healthy"}`.
- [ ] The `test_integration.py` script runs successfully from the root directory.
- [ ] **Encrypt Flow**: Successfully hides a text payload in a PNG image, returning a valid Base64 image and AES-256 Key.
- [ ] **Decrypt Flow**: Successfully recovers the exact original text using the generated key and Stego PNG.

## 3. Web UI (Frontend)
Run `npm run dev` inside `frontend/` and verify:
- [ ] The Next.js app loads at `http://localhost:3000` with the custom dark theme.
- [ ] **CORS**: Submitting an image on the "Encrypt" page successfully communicates with the backend without browser CORS errors.
- [ ] **Drag & Drop**: Dropping an image on the Dropzone successfully populates the file state.
- [ ] **Download**: You can click "Download Stego Image" on the success screen and it saves a valid PNG.

## 4. ML Engine (Training)
- [ ] Run `python train.py` inside `ml/`. It should successfully locate the COCO dataset and start Epoch 1 (Note: This requires a GPU for reasonable speed).
- [ ] Once `best_model.pth` is saved, the backend `/detect` endpoint automatically switches from returning `503 Service Unavailable` to returning real `DetectResponse` probabilities.

## Example Manual Testing via cURL
If you want to test encryption manually:
```bash
curl -X POST "http://localhost:8000/api/v1/encrypt" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your_image.png;type=image/png" \
  -F "plaintext=My Secret Payload"
```
