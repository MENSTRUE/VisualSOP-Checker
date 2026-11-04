> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Frontend React + Vite — implemented local analysis UI

## Current implementation
The frontend is **already implemented**, not merely planned. It uses React, TypeScript and Vite, with `frontend/src/main.tsx`, `frontend/src/style.css`, `frontend/index.html`, and `frontend/vite.config.ts`. The UI is a local experimental dashboard: choose a video, call `/api/analyze`, show video information, a motion timeline, and experimental V6 action windows when returned. Never display a predicted SOP pass/fail result.

## Install and run
```powershell
cd "D:\porto@ day\day 30\VisualSOP Checkerrontend"
npm ci
npm run dev
```
Open `http://localhost:5173`. Start FastAPI separately on `127.0.0.1:8001`. Vite's `/api` proxy **must** target `http://127.0.0.1:8001`.

## Contract with backend
`GET /api/health` reports server and model file readiness; it does not certify prediction quality. `POST /api/analyze` returns `motion`, `model_status`, `activity_predictions`, `ai_error`, `sop_status`, `warning`, plus video metadata. Handle `experimental_v6`, `checkpoint_missing`, `inference_failed` distinctly; do not fabricate demo predictions if API errors. Show uncertainty for `uncertain=true` and clearly label confidence as uncalibrated.

## Verification
```powershell
npm ci
npm run build
```
While FastAPI and Vite are running, confirm `http://localhost:5173/api/health` passes through to the backend. Upload an authorized test clip and compare UI predictions with the API response. Check empty/error/loading states, small viewport overflow, file selection and preview. The commands are suggested verification, not evidence of a completed comprehensive frontend test suite.

## Production boundary
Vite development mode is not a production deployment. The backend is unauthenticated, model reliability is weak, and the app must not be marketed as an industrial SOP enforcement product. Do not commit `node_modules/`, build files, video uploads or secrets.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Frontend React + Vite — antarmuka analisis lokal yang sudah dibuat

## Implementasi saat ini
Frontend **sudah ada**, bukan sekadar rencana. Teknologi React, TypeScript dan Vite, dengan `frontend/src/main.tsx`, `frontend/src/style.css`, `frontend/index.html`, serta `frontend/vite.config.ts`. Pengguna memilih video, mengirim ke `/api/analyze`, kemudian melihat metadata, grafik motion dan prediksi aktivitas V6 eksperimental jika API berhasil. Jangan menampilkan status SOP lulus/gagal palsu.

## Instalasi dan jalan
```powershell
cd "D:\porto@ day\day 30\VisualSOP Checkerrontend"
npm ci
npm run dev
```
Buka `http://localhost:5173`, dengan backend FastAPI aktif di `127.0.0.1:8001`. Target proxy `/api` Vite **harus ke 8001**, bukan 8000.

## Kontrak respons backend
`GET /api/health` menyatakan status keberadaan/loaded model, bukan kualitas prediksi. `POST /api/analyze` mengembalikan metadata video, `motion`, `model_status`, `activity_predictions`, `ai_error`, `sop_status`, dan `warning`. Pisahkan kasus `experimental_v6`, `checkpoint_missing` dan `inference_failed`. Jangan buat prediksi palsu saat API gagal. Bila `uncertain=true`, tampilkan ketidakpastian, dan jelaskan confidence belum dikalibrasi.

## Pengujian
```powershell
npm ci
npm run build
```
Periksa `http://localhost:5173/api/health`, unggah video yang memiliki izin, lalu cocokkan hasil UI dengan JSON backend. Uji state loading/kosong/error, responsivitas, preview dan pemilihan file. Tes tersebut adalah acceptance checks yang **perlu dilakukan**, bukan klaim sudah ada pengujian otomatis lengkap.

## Batas deployment
Vite development server bukan deployment produksi. Backend tanpa autentikasi, model lemah, dan aplikasi tidak boleh dipromosikan sebagai sistem penegak SOP industri. Ignore `node_modules`, `dist`, video dan secrets.
