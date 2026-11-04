> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# FastAPI backend — implemented research prototype

## Actual responsibilities
`backend/app/main.py` accepts uploaded video, validates filename extension and video metadata, records motion using grayscale frame differences, saves a JPEG preview and JSON result, and conditionally executes **real R3D-18 V6 inference** via `backend/app/v6_inference.py`. This is **not** an SOP rules engine.

## Run
```powershell
# At repository root after setting up backend/.venv:
.ackend\.venv\Scripts\python.exe -m pip install -r backendequirements.txt
.ackend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```
The frontend Vite proxy points `/api` to port **8001**. If port is in use, stop the previous server instead of creating duplicates.

## API contract
| Endpoint | Method | Implemented behavior |
|---|---|---|
| `/api/health` | GET | Server health; presence of checkpoint, recipe, enabled flag, loaded flag |
| `/api/analyze` | POST | Multipart `file`; video metadata, motion, optional V6 predictions and error information |
| `/api/analyses/{job_id}` | GET | Stored analysis JSON |
| `/api/analyses/{job_id}/preview` | GET | Stored JPEG preview |

Upload extensions `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`; default limit 150 MB (environment `VISUALSOP_MAX_UPLOAD_MB`); video metadata cap 30 min. AI inference separately rejects videos longer than 120 s. Results and uploads reside in `backend/storage/` by default, or `VISUALSOP_STORAGE`. No auth, background jobs, formal retention, or production hardening.

## Model integration contract
Model path is repository-root `models/`, resolved from `backend/app/v6_inference.py` via `Path(__file__).resolve().parents[2]`. Local files: `best_finetuned_layer4_fc.pt` and `inference_recipe.json`. The checkpoint only includes fine-tuned layer4+fc; use official Kinetics-400 pretrained R3D-18. Pipeline uses 16 RGB frames, short edge 128, center/motion ROI ensemble, pretrained transform and overlapping heuristic temporal windows. Model status `experimental_v6` is not a measure of correctness; `sop_status` must be `not_evaluated`.

## Testing
```powershell
.ackend\.venv\Scripts\python.exe -m compileall -q backendpp
Invoke-RestMethod http://127.0.0.1:8001/api/health
# On PowerShell versions without -Form, use curl.exe -F with an authorized local video.
```
Check valid/invalid uploads, missing weights, failed pretrained fetch, repeated requests, retrieval and preview routes, no fabricated predictions, and correct JSON error paths. These are suggested acceptance checks; no comprehensive automated suite is claimed.

## Security and limitations
Bind localhost, keep `backend/storage/` out of Git, limit media decoding resource usage and never expose upload endpoints publicly without authentication, content scanning, rate-limiting, isolation, retention and privacy controls. Source-video access and licensing are separate from MIT source-code licensing. See root README and `docs/limitations.md`.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Backend FastAPI — prototipe penelitian yang sudah berjalan

## Tanggung jawab aktual
`backend/app/main.py` menerima video, memvalidasi ekstensi dan metadata, menghitung beda frame grayscale untuk motion, menyimpan JPEG preview + JSON hasil, serta menjalankan **inferensi R3D-18 V6 asli** melalui `backend/app/v6_inference.py` jika model tersedia. Ini **bukan** mesin aturan kepatuhan SOP.

## Menjalankan
```powershell
# Dari root repository, setelah backend/.venv dibuat:
.ackend\.venv\Scripts\python.exe -m pip install -r backendequirements.txt
.ackend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```
Vite proxy `/api` menuju port **8001**. Jika port terpakai, hentikan server lama; jangan jalankan dua backend.

## Endpoint
| API | Metode | Fungsi |
|---|---|---|
| `/api/health` | GET | Kesehatan server dan status file/loading model |
| `/api/analyze` | POST | Upload multipart `file`, metadata, motion, prediksi V6 opsional, pesan error |
| `/api/analyses/{job_id}` | GET | Ambil hasil analisis tersimpan |
| `/api/analyses/{job_id}/preview` | GET | Ambil preview JPEG |

Format yang diterima `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`; default maks 150 MB (`VISUALSOP_MAX_UPLOAD_MB`); metadata video maks 30 menit; inferensi AI maksimal **120 detik**. File video dan hasil tersimpan di `backend/storage/` atau `VISUALSOP_STORAGE`. Belum ada autentikasi, antrean tugas, kebijakan retensi formal, ataupun hardening produksi.

## Kontrak inferensi
Folder bobot berada di root `models/` melalui `parents[2]` dari `backend/app/v6_inference.py`. File wajib lokal: `best_finetuned_layer4_fc.pt` dan `inference_recipe.json`. Bobot fine-tune hanya layer4+fc, sehingga R3D-18 pretrained Kinetics-400 resmi **wajib tersedia**. Sampling 16 RGB frame, resize short edge 128, crop center/motion ensemble, transform pretrained, jendela heuristik bertumpang tindih. `experimental_v6` bukan bukti benar, `sop_status` tetap `not_evaluated`.

## Pengujian
```powershell
.ackend\.venv\Scripts\python.exe -m compileall -q backendpp
Invoke-RestMethod http://127.0.0.1:8001/api/health
```
Uji kasus file invalid, model hilang, bobot pretrained gagal, API retrieval/preview, upload berulang, dan pesan error. Perintah di atas adalah langkah tes yang disarankan, **bukan klaim bahwa suite otomatis menyeluruh sudah tersedia**. PowerShell lama dapat menggunakan `curl.exe -F`.

## Keamanan
Batasi ke localhost, ignore `backend/storage/`, dan jangan mengekspos endpoint unggah ke publik tanpa autentikasi, validasi isi file, pembatasan resource, rate limit, isolasi decoding, retensi dan review privasi. Hak lisensi video sumber terpisah dari MIT kode. Lihat README utama dan `docs/limitations.md`.
