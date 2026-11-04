> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# V6 local setup and compatibility runbook

## Scope and status
This runbook installs the **actual experimental R3D-18 V6 classifier** in the existing local FastAPI + React application. It is not an SOP compliance engine. The first demonstrated successful POST used a 20-second Assembly101 clip and returned 10 overlapping windows with `model_status=experimental_v6` and `ai_error=null`; prediction correctness was not established. Read root README for full metrics and limitations.

## Prerequisites
- Python environment in `backend/.venv`; matching torch and torchvision, OpenCV, FastAPI and python-multipart, see `backend/requirements.txt`.
- Node.js/npm, installed from `frontend/package-lock.json` with `npm ci`.
- Local `models/best_finetuned_layer4_fc.pt` and version-matched `models/inference_recipe.json`.
- Official `R3D_18_Weights.DEFAULT` Kinetics-400 pretraining available in torchvision cache (first run may download).
- Source video that you are authorized to use. The repository does not redistribute the Assembly101 footage.

## PowerShell startup (run each server once)
```powershell
cd "D:\porto@ day\day 30\VisualSOP Checker"
.ackend\.venv\Scripts\python.exe -m pip install -r backendequirements.txt
Test-Path .\modelsest_finetuned_layer4_fc.pt
Test-Path .\models\inference_recipe.json
.ackend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```
In a second terminal:
```powershell
cd "D:\porto@ day\day 30\VisualSOP Checkerrontend"
npm ci
npm run dev
```
Visit `http://localhost:5173`; Vite `/api` must point to `http://127.0.0.1:8001`.

## Health check and inference
```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/health
# Only if the sample video exists locally:
curl.exe -sS -X POST "http://127.0.0.1:8001/api/analyze" -F "file=@D:\porto@ day\day 30\VisualSOP Checkerssets\examplesssembly101_test_20s.mp4"
```
`model_inference_enabled=true` means files exist; `model_loaded=false` may appear before inference. A successful inference returns `activity_predictions` and null `ai_error`. `sop_status` stays `not_evaluated`. Do not use fake values in tests or UI.

## Reproducibility contract
`models/inference_recipe.json` controls 16 frames, center 78% of segment, short-edge resize 128, `ensemble` center+motion crops, six label mapping, R3D-18 pretrained transforms. The fine-tuned checkpoint contains only `layer4` and `fc`; `weights=None` is invalid. Continuous-video windows are heuristic 3 s with 2 s stride, not learned action segmentation. Confidence is uncalibrated.

## Troubleshooting
- HTTP proxy ECONNREFUSED 8000: configure Vite port 8001.
- Backend `Errno 10048`: stop existing backend, do not start another.
- Missing checkpoint/recipe: verify repo root path from `backend/app/v6_inference.py` uses `parents[2]`.
- `model_loaded=false`: run video analysis; if `inference_failed`, inspect `ai_error` and backend traceback.
- PowerShell `-Form` missing: use `curl.exe -F`.
- Pretrained download unavailable: obtain licensed official weights in a controlled environment and populate supported cache.
- Video >120 seconds: metadata/motion report can work, but current V6 classifier rejects long videos.

## Release boundaries
Keep on localhost. Never publish uploaded videos, source data, checkpoints, or secrets; do not advertise safety monitoring, production use, or automatic SOP violation detection.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Panduan instalasi dan kompatibilitas V6 lokal

## Cakupan dan status
Panduan ini menjalankan **klasifikasi enam aktivitas asli R3D-18 V6** pada FastAPI dan React lokal; bukan detektor kepatuhan SOP. Percobaan POST video Assembly101 20 detik pernah menghasilkan sepuluh prediksi dengan `model_status=experimental_v6` dan `ai_error=null`; ketepatan prediksinya belum diverifikasi.

## Syarat
- Python di `backend/.venv`; pasang `backend/requirements.txt` termasuk torch, torchvision, FastAPI, OpenCV, python-multipart.
- Node/npm; instal dependensi sesuai lockfile dengan `npm ci`.
- Dua file lokal `models/best_finetuned_layer4_fc.pt` dan `models/inference_recipe.json` yang cocok.
- Bobot pra-latih resmi `R3D_18_Weights.DEFAULT` Kinetics-400 dalam cache torchvision; koneksi mungkin diperlukan saat pemanggilan awal.
- Video uji dengan izin pakai yang sesuai; rekaman Assembly101 tidak didistribusikan di repo.

## Langkah PowerShell
```powershell
cd "D:\porto@ day\day 30\VisualSOP Checker"
.ackend\.venv\Scripts\python.exe -m pip install -r backendequirements.txt
Test-Path .\modelsest_finetuned_layer4_fc.pt
Test-Path .\models\inference_recipe.json
.ackend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```
Terminal kedua:
```powershell
cd "D:\porto@ day\day 30\VisualSOP Checkerrontend"
npm ci
npm run dev
```
Buka `http://localhost:5173`. Pastikan proxy `/api` di Vite menuju **8001**, bukan 8000.

## Cek integrasi
```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/health
# Jika video contoh tersedia secara lokal:
curl.exe -sS -X POST "http://127.0.0.1:8001/api/analyze" -F "file=@D:\porto@ day\day 30\VisualSOP Checkerssets\examplesssembly101_test_20s.mp4"
```
`model_inference_enabled=true` hanya berarti file ada; `model_loaded=false` masih normal sebelum inferensi pertama. Hasil yang berhasil mempunyai `activity_predictions` dan `ai_error=null`, sedangkan `sop_status=not_evaluated`.

## Kontrak model
Recipe menentukan 16 frame, 78% interval tengah, resize short edge 128, crop center+motion `ensemble`, urutan enam kelas, dan transform pretrained. Checkpoint hanya menyimpan `layer4` dan `fc`, sehingga **jangan** mengganti bobot dasar dengan `weights=None`. Jendela 3 detik/stride 2 detik hanyalah heuristik, bukan segmentasi yang dilatih. Confidence belum dikalibrasi.

## Troubleshooting
- `ECONNREFUSED :8000`: perbaiki Vite proxy ke 8001.
- `Errno 10048`: backend lama belum berhenti; tekan `Ctrl+C`.
- Checkpoint/recipe tidak ditemukan: `backend/app/v6_inference.py` harus menunjuk root melalui `parents[2]`.
- `model_loaded=false`: jalankan video; bila gagal baca `ai_error`.
- PowerShell tak mengenal `-Form`: gunakan `curl.exe -F`.
- Bobot pra-latih tidak tersedia: ambil bobot resmi melalui koneksi dan izin yang sesuai.
- Video di atas 120 detik: motion dapat diproses, namun inferensi V6 dibatasi.

Gunakan **lokal**, bukan sistem keselamatan, penilaian pekerja, atau penentu pelanggaran SOP produksi.
