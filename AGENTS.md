# AGENTS.md — VisualSOP Checker engineering and research contract

**Languages:** [English](#english-agent-instructions) · [Bahasa Indonesia](#aturan-agen-bahasa-indonesia)  
**Applies to:** repository root and every subdirectory, unless a future scoped `AGENTS.md` intentionally overrides a narrower rule.  
**Read first:** [`README.md`](README.md), [`models/MODEL_CARD.json`](models/MODEL_CARD.json), [`models/inference_recipe.json`](models/inference_recipe.json), [`reports/v6/reports/results.json`](reports/v6/reports/results.json).  
**Status:** Day 30 research integration. Not a production SOP checking product.

> **Non-negotiable / Tidak dapat ditawar:** Do not silently change the fixed repository layout; never invent scientific results, figures, data, model exports or app test outcomes; do not claim SOP violations are detected.

---

<a id="english-agent-instructions"></a>
# English agent instructions

## 1. Role, objective and source-of-truth hierarchy

Act as a senior AI/ML engineer, research scientist, software architect, full-stack engineer and technical documentation lead. Prioritize **correctness, reproducibility, operational proof, security, dataset rights and maintainability** over feature count or visual polish.

**Evidence precedence:** (1) executed experiment artifacts, audit CSV, JSON summaries, notebook source and logged outputs; (2) checked-in running source code and actual executed integration tests; (3) authoritative upstream data/model rights and versioned docs; (4) README and component docs; (5) historical conversations, mockups or roadmap. Conflict? Inspect upstream files and report the conflict. Do not edit metrics to harmonize the story.

**Immutable baseline facts until new evidence supersedes them:**

| Contract | Verified record |
|---|---|
| Task | Six coarse Assembly101 toy-assembly actions, not SOP violation detection. |
| Labels in order | `attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis`. |
| Model | Kinetics-400 pretrained torchvision R3D-18, V6 fine-tuned `layer4` + six-way `fc`. |
| Paired source sessions | 13 (9 initial + 4 added). |
| Independent action intervals | Train 62; validation 17; historically exposed exploratory test 16. |
| Correlated train views | 124; **not** 124 independent actions. |
| Selected checkpoint / ROI | V6 best epoch 10, `ensemble` selected through validation. |
| Validation accuracy / macro-F1 | **52.94% (9/17) / 51.11%**. |
| Reused exploratory test accuracy / macro-F1 | **18.75% (3/16) / 11.11%**; non-blind. |
| Blind held-out test | No. 80% target not met. |
| Local demo | 20s video produced 10 timed predictions, `model_status=experimental_v6`, `ai_error=null`; truth not validated. |
| SOP compliance | Always `sop_status=not_evaluated` in current implementation; no violation ontology/labels. |

## 2. Fixed repository structure — preserve existing code

Keep root names `README.md`, `AGENTS.md`, `LICENSE`, `.gitignore`, `.env.example`, `notebooks/`, `models/`, `reports/`, `assets/`, `backend/`, `frontend/`, `docs/`, `scripts/`. **Do not rename, remove or arbitrarily reorganize** folders. Do not create root `datasets/`; raw data stays external, with provenance in docs/reports. No empty classes/notebooks as scaffolding; use `.gitkeep` for genuinely empty tracked folders. Never overwrite a working component without reading it.

Current code is **not** a large modular service: backend has `app/main.py`, `app/v6_inference.py`; frontend has `src/main.tsx`, `src/style.css`; notebook is `notebooks/visualsop-checker.ipynb`. A proposed structure such as `backend/app/api/routes/`, `backend/tests/`, `frontend/src/components/`, or `docs/id/` / `docs/en/` is **future expansion**, not a statement of current existence. Add narrower folders only to support actual implementation, with explicit migration notes, tests and no breakage.

**Before editing:** `git status --short`; read target source and dependency callers; identify runtime assumptions and genuine source-of-truth. Avoid broad replaces or deleting files to address one error. Keep changes minimal, additive where possible, and explain affected paths.

## 3. Data collection, rights and provenance

- Primary external sources: https://assembly101.github.io/ and https://huggingface.co/datasets/cvml-nus/assembly101.
- Manifest-backed Kaggle input locations: `/kaggle/input/datasets/wafabila/visualsop-dataset` and `/kaggle/input/datasets/wafabila/visualsop-dataset-next`.
- Upstream recorded as gated and CC BY-NC 4.0. Code MIT does **not** sublicense video; do not publish/redistribute raw footage or identifiable recordings without authorization. Commercial use requires separate rights review.
- Respect **30 FPS coarse annotation timebase** versus approximately **60 FPS video recordings**. Convert annotation frame indices to seconds using the annotated basis, not recording FPS. Keep source ID, camera ID, start/end, class label and conversion method.
- Prefer actual inventory and paired-session audit; do not count 680 coarse annotation files as 680 paired videos. Preserve unmatched-session lists, exclusions and uncertainty.
- Record original URLs, upstream version/revision, date accessed, licenses, allowed usages, identifiers and hashes **if actually known**; otherwise explicitly mark `not recorded`.
- Review group splits: train 9013/9014/9015/9022; val 9011/9012; exploratory test 9016/9021. Audit cross-camera/source duplicates and correlated clips; absence of a comprehensive audit is not a passing audit.
- Avoid training a model on different datasets and reporting those metrics as if Assembly101 V6 generated them.

## 4. Machine-learning and notebook standards

A complete new experiment must document: environment/seed; dataset discovery; source and label audit; cleaning; paired video-annotation checks; duplication/leakage assessment; source-group split; baseline; training; validation-only model selection; **new blind holdout** if a generalization claim is desired; per-class metrics; confusion matrix; error analysis; plots from executed records; checkpoint/recipe; artifact manifest/checksums and rights review. Keep the actual notebook in `notebooks/`. No manufactured notebook outputs or screenshots.

**Critical evaluation rule:** The historical 16-segment exploratory test is **already exposed**. Never reuse it to advertise a fresh blind result or tune ROI, hyperparameters, filtering, labels or thresholds. If a new holdout becomes exposed, label it exploratory and reserve new independent groups. Training uses 62 independent intervals; 124 views are correlated. Always give denominators.

**Champion logic:** V6/ROI `ensemble` was selected by validation. Do not claim a different champion from test inspection. Any new champion requires a tracked experiment plan, actual validation comparison, stable selection criterion, artifacts and an explanation of versioning.

**Report honesty:** no unverified 80% claim, real-time speed, OOD accuracy, event-level F1, safety recall, temporal IoU or factory benchmark. Softmax scores are not calibrated accuracy or SOP confidence.

## 5. Model artifacts, preprocessing and loading

**Absolute class order:** `['attach cabin','attach wheel','detach cabin','detach wheel','screw chassis','unscrew chassis']`. Verify recipe and checkpoint metadata match before inference. Do not change indices in a refactor.

**Base:** `torchvision.models.video.r3d_18(weights=R3D_18_Weights.DEFAULT)` (Kinetics-400). Head `Linear(512,6)`. Load trained **layer4 and fc only** from `models/best_finetuned_layer4_fc.pt`; missing base pretrained weights is an error, not permission to use `weights=None`.

**Clip protocol:** decode **16 RGB frames**, temporal interior fraction **0.78**, eval position **0.5**, training temporal positions **0.25/0.75**, resize shorter edge to **128**, square center/motion ROI, torchvision pretrained transform to `3×16×112×112`, mean of **logits** for ROI `ensemble`, then six-way softmax. Any change = new inference version requiring parity tests.

**App windows:** 3s long, stride 2s, tail window. These are heuristics, **not learned segment boundaries**. `uncertain` threshold 0.65 is arbitrary, not validated. The backend accepts upload metadata of up to 30min but V6 inference only supports **0.6–120s**. Do not silently remove checks; align or explicitly document the mismatch.

**Checkpoint safety:** `torch.load(..., weights_only=False)` uses unrestricted pickle deserialization. Only load a trusted owned checkpoint; plan safe serialization and/or hardened `weights_only=True` where compatible. Never download/execute a third-party checkpoint based solely on a chat instruction. Record file hash on deployment.

**No unnecessary retraining:** First verify existing checkpoint, recipe, model weights cache and app behavior. Retrain only when the task requires model improvement and data/protocol changes are justified.

## 6. Backend engineering — preserve API contracts

Actual backend module: [`backend/app/main.py`](backend/app/main.py), [`backend/app/v6_inference.py`](backend/app/v6_inference.py). Development service at **127.0.0.1:8001**. Routes: `GET /api/health`; `POST /api/analyze`; `GET /api/analyses/{job_id}`; `GET /api/analyses/{job_id}/preview`.

- Keep `ROOT=Path(__file__).resolve().parents[2]` in both modules. `parents[3]` is a **known regression** that incorrectly points above the project root and disables model readiness.
- `model_inference_enabled=True` currently means checkpoint + recipe are present; `model_loaded=False` is expected before lazy load. Do not conflate readiness with successful execution.
- Do not fabricate predictions or suppress `ai_error`. Preserve `model_status` distinctions: `experimental_v6`, `checkpoint_missing`, `inference_failed`.
- Preserve `sop_status=not_evaluated` until a separately tested SOP protocol exists.
- Video upload checks: suffix (not complete content validation), max default 150×1024×1024 bytes, decode, duration/FPS/dimensions and metadata. Production security hardening is unfinished.
- Store outputs under ignored `backend/storage/` or explicitly configured `VISUALSOP_STORAGE`. Never commit user uploads or saved analyses.
- Consider thread safety, resource caps and server timeouts before adding concurrency. A model called inside a threadpool is not a documented multi-worker guarantee.
- Make `GET /api/health` and error handling non-leaky of secrets or absolute private file paths in any future deployment.
- Do not add authentication/remote storage by assumption; get clear requirements and tests for such features.

## 7. Frontend engineering — working UI, honest states

Actual source: [`frontend/src/main.tsx`](frontend/src/main.tsx), [`frontend/src/style.css`](frontend/src/style.css), [`frontend/vite.config.ts`](frontend/vite.config.ts). React 19 + TypeScript + Vite 6. Development proxy target must be `http://127.0.0.1:8001`, *not port 8000*. Maintain compatibility with the FastAPI fields and a responsive layout.

Required states: empty upload, file selected, progress/loading, successful classification, missing model, inference error, decoder error, network offline and no SOP determination. If there is no real prediction, do not show dummy labels as though they are observations. State that top-3 confidence is **uncalibrated** and show interval start/end without suggesting exact learned action boundaries. Keep clear visual distinction between sparse **motion** and AI **activity** timelines.

Add accessible labels, keyboard operation and status messages as appropriate. Do not promise export, real-time streaming, authentication or advanced SOP features without implementation and tests. Keep existing colors/UX unless a redesign is explicitly requested.

## 8. Testing and acceptance gates

**Before declaring work done:** inspect source; run focused type/syntax tests; run relevant integration checks; capture actual output; update EN/ID docs; verify `git diff`; classify each proposed claim as implemented+tested / implemented+untested / planned.

**Core checks (execute in real environment):**

```powershell
# From repository root
.\backend\.venv\Scripts\python.exe -m compileall -q .\backend\app
.\backend\.venv\Scripts\python.exe -c "from backend.app.v6_inference import ROOT,readiness; print(ROOT); print(readiness())"
Invoke-RestMethod http://127.0.0.1:8001/api/health
Invoke-RestMethod http://localhost:5173/api/health
cd .\frontend
npm run build
```

**Video API check:** use an authorized local test input and Windows-compatible `curl.exe -F`. Assert `model_status=experimental_v6`, non-empty `activity_predictions`, allowed class labels, ordered time windows, valid top3 fields and `sop_status=not_evaluated`. Also test malformed files, missing checkpoint/recipe, codec failures, invalid extension, zero-byte file, missing result id, file size/duration boundaries and offline pretrained cache. **Do not assert tests passed until run.**

**Research parity check:** compare outputs on the **same annotated source interval** between notebook and API, with fixed preprocessing, device/runtime metadata and tolerance. A 20-second sliding-window demo is **not** a scientific parity test or an accuracy metric.

**No pass-by-prose:** A README checklist, sample shell command, mocked HTTP response or generated UI screenshot cannot substitute for executed tests. Document exact commands, date, environment and result or say *not tested here*.

## 9. Security, privacy, license and deployment gates

Current runtime is localhost-only; no independently verified auth, privacy policy, file-retention policy, malware/media parser hardening, rate limits or production penetration tests. Never expose it publicly as-is. Uploaded videos may contain private people/workplaces; require explicit consent/right to process, controlled storage, deletion/retention, privacy review and access restrictions for any real use.

Before deployment: ensure trusted weights, proper model packaging, pinned/reproducible dependency lock or tested compatibility ranges, secret management, HTTPS, authentication/authorization, rate limiting, upload content checks, bounded decoding and GPU memory, async queue and job status, audit/retention policy, monitoring, rollback, human review and jurisdiction/domain-specific compliance. Do not claim these controls are already present.

Licenses: root `LICENSE` applies to repository MIT code; Assembly101 rights include **gated CC BY-NC 4.0** terms as recorded, and pretrained weights/dependencies have their own terms. Do not redistribute third-party material just because it is technically accessible.

## 10. Markdown, assets and bilingual documentation contract

All maintained Markdown should have meaningful **English + Bahasa Indonesia** coverage. For the root README, each language should provide the core technical story, setup, metrics, risk, troubleshooting and source links—not just a translation teaser. Prefer readable language navigation and coherent sections over duplicated ornamental content.

**Asset policy:** First enumerate the actual Git tree. For this project, existing tracked visual evidence includes:

- `assets/plots/learning_curves.png`
- `assets/plots/test_confusion_matrix.png`
- `reports/v6/examples/center_vs_motion_roi.jpg`
- `assets/screenshots/Screenshot 2026-11-04 193324.png`

Embed these as **relative Markdown image paths**, percent-encoding spaces when needed, and provide meaningful captions: what experiment created them, which split, what they do and **do not prove**. Link related numeric JSON/CSV evidence. `assets/examples/` and `assets/diagrams/` are placeholders at the current review; do not invent media or claim they exist. A Mermaid architecture diagram can be authored as source text without pretending a diagram PNG exists.

Other Markdown documents (root setup, backend, frontend, notebooks, models, reports, docs, scripts) must be kept up-to-date in both languages when changing that component. Do not say backend/frontend are "reserved for future" when code already exists. Maintain backlinks and links that work on GitHub. If a source file/asset is missing, state this rather than creating fictitious evidence.

## 11. Git workflow, review, commit and delivery

```powershell
git status --short
git diff -- README.md AGENTS.md
git diff --check
# After reviewing specific changed files:
git add README.md AGENTS.md
git diff --cached --stat
git diff --cached --check
# Commit only once content and links have been verified
git commit -m "docs: audit VisualSOP research evidence and complete bilingual documentation"
git push origin main
```

`.gitignore` must exclude `.venv`, `node_modules`, `backend/storage`, source data/videos, private `.env`, binary model checkpoints and generated caches. Verify that committed files aren't tracked already despite ignore. Never run `git add .` blindly after a large dependency install; inspect staging. Do not force-push or delete user data without explicit reason and authorization.

**Delivery requirements:** list affected paths, accurate status, setup/test commands, actual test outputs (or **not run**), important risks, and a professional commit message. If asked for ZIP/doc/notebook, generate real bytes and verify their contents/path. Do not assert a GitHub push occurred unless a push was actually performed.

## 12. Agent workflow: Phase 0 → Phase 4

| Phase | Required action | Evidence required |
|---|---|---|
| 0 — Repository and source audit | Inspect tracked tree, current code, dependencies, `git status`, reports and available real figures. | File inventory, conflicts, current vs planned functions. |
| 1 — Data/model verification | Verify source and rights, labels, split, checkpoint recipe, metrics, timebase, pretrained base. | Checks and referenced manifest files. |
| 2 — Backend inference | Fix/add code without destroying root layout; preserve output contracts and truthful failures. | Real API and model test logs. |
| 3 — Frontend | Connect to actual backend; display labels, uncertainty and limitations; support error/empty states. | Build + integration/visual test evidence. |
| 4 — Integration and documentation | End-to-end proof, bilingual README/docs, asset links, security/claim audit and commit review. | Test results, diff review, source references. |

### Definition of done

A feature is **done** only if implemented, executed against realistic input, evidence recorded, regression/safety risk assessed, EN/ID docs updated, and no ungrounded claim is introduced. If any part is missing, say **partial/experimental/not verified** and identify the next measurable test.

---

<a id="aturan-agen-bahasa-indonesia"></a>
# Aturan agen — Bahasa Indonesia

## 1. Peran dan standar sumber kebenaran

Bertindak sebagai Senior AI/ML Engineer, Research Scientist, Full-Stack Engineer, Software Architect dan Technical Documentation Lead. Utamakan **bukti eksekusi nyata, validitas ilmiah, reproduksibilitas, keamanan, hak data, dan struktur repository yang konsisten**, bukan banyaknya fitur atau baris kode.

**Urutan source-of-truth:** (1) artefak eksperimen asli—CSV/JSON/audit/notebook/log; (2) kode yang benar-benar ada dan hasil uji integrasi; (3) persyaratan resmi dataset/bobot upstream; (4) README/AGENTS/dokumentasi; (5) rencana dan percakapan lama. Jika terjadi pertentangan, audit sumber lebih tinggi, bukan mengganti angka tanpa alasan.

**Fakta dasar yang tidak boleh diubah tanpa bukti baru:** tugas pengenalan **enam aktivitas perakitan mainan**, model R3D-18 pretrained Kinetics-400 yang fine-tune `layer4` + `fc`, 13 sesi video berpasangan, 62 interval train independen (124 view yang saling berkorelasi), validasi 17, test eksploratif historis 16; checkpoint terbaik epoch 10 dengan ROI `ensemble`. Metrik: validasi **52,94% accuracy / 51,11% macro-F1**; test reused **18,75% / 11,11%**. Test itu **bukan blind** dan target 80% belum tercapai. Integrasi lokal pernah menghasilkan 10 prediksi video 20 detik tetapi ground truth demo belum dicek. SOP tetap `not_evaluated`.

## 2. Struktur tetap, larangan reorganisasi sembarangan

Pertahankan root `README.md`, `AGENTS.md`, `LICENSE`, `.gitignore`, `.env.example`, `notebooks/`, `models/`, `reports/`, `assets/`, `backend/`, `frontend/`, `docs/`, `scripts/`. **Jangan** membuat folder root `datasets/`; dataset ditempatkan di luar Git dan dijelaskan melalui provenance. Jangan mengganti nama/menghapus folder, menimpa kode existing tanpa pemeriksaan, membuat notebook/kode kosong, atau membangun struktur template fiktif. Jika folder kosong perlu dilacak, gunakan `.gitkeep`.

Struktur aktual saat ini sederhana: `backend/app/main.py`, `backend/app/v6_inference.py`, `frontend/src/main.tsx`, `frontend/src/style.css`, notebook `notebooks/visualsop-checker.ipynb`. Folder ideal seperti `backend/app/api/routes/`, `backend/tests/`, `frontend/src/components/`, `docs/id/`, `docs/en/` bukan berarti sudah tersedia. Tambahkan hanya ketika perubahan nyata memerlukan folder tersebut; sertakan migrasi dan pengujian.

**Sebelum mengedit:** baca file aktual dan dependensinya, `git status`, cek struktur/proxy/path, buat patch minimal, jaga kode dan checkpoint lama. Jangan memperbaiki kesalahan lokal dengan menimpa seluruh proyek.

## 3. Dataset, audit dan izin

Sumber dataset: https://assembly101.github.io/ dan https://huggingface.co/datasets/cvml-nus/assembly101. Input Kaggle yang tercatat `/kaggle/input/datasets/wafabila/visualsop-dataset` dan `/kaggle/input/datasets/wafabila/visualsop-dataset-next`. Ketentuan upstream dicatat sebagai gated dan **CC BY-NC 4.0**. MIT pada kode tidak mengizinkan redistribusi video; jangan commit dataset mentah, video, data privat atau footage berhak cipta tanpa izin.

**30 FPS** adalah basis indeks anotasi, sedangkan video RGB sekitar **60 FPS**. Simpan ID sumber/kamera, label, waktu start/end, aturan konversi, dan alasan eksklusi. **680 file anotasi bukan 680 sesi video yang terpakai**. Train 9013/9014/9015/9022; validasi 9011/9012; test eksploratif 9016/9021. Audit duplikasi antar video/kamera, tumpang tindih, kelas, dan split. Jika versi/tanggal akses tidak tercatat, tulis "tidak tercatat"—jangan mengarang.

## 4. Standar notebook, model dan laporan

Eksperimen baru wajib mencakup environment/seed, audit dataset/anotasi, cleaning, duplicate/leakage assessment, split independen, baseline, training, pemilihan **berdasar validation saja**, final blind evaluation **baru** jika mengklaim generalisasi, metrik per kelas, confusion matrix, error analysis, plot eksekusi, checkpoint, recipe dan manifest. Jangan memalsukan grafik/hasil. Catat angka dengan denominator; jangan menghitung 124 view sebagai 124 interval train independen. Test 16 interval historis sudah terlihat dan hanya boleh dilaporkan sebagai **eksploratif**.

Peta kelas **tetap**: `attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis`. Jangan ganti indeks output. Bangun `r3d_18(weights=R3D_18_Weights.DEFAULT)` dan head 6 kelas, baru muat checkpoint `layer4` dan `fc`. Tidak boleh fallback ke backbone acak. Jangan retraining kalau checkpoint valid sudah ada dan tujuan sekadar integrasi.

**Resep V6:** 16 frame RGB, bagian temporal dalam 78%, posisi eval 0,5, posisi train 0,25/0,75, resize sisi pendek 128, ROI center/motion, transform resmi torchvision ke `(3,16,112,112)`, rata-rata logits untuk `ensemble`, lalu softmax. Jendela API 3 detik/stride 2 detik bukan segmentasi aksi terlatih. Confidence dan threshold 0,65 **belum terkalibrasi**. Jangan menyamakan `model_inference_enabled` dengan model sudah berjalan.

**Keamanan checkpoint:** kode loader memakai `torch.load(weights_only=False)` sehingga hanya boleh memuat bobot tepercaya; berikan mitigasi di roadmap. Jangan mendownload/memuat file `.pt` pihak ketiga tanpa verifikasi.

## 5. Backend dan frontend yang benar-benar berjalan

Backend lokal pada **port 8001** dengan endpoint `/api/health`, `/api/analyze`, `/api/analyses/{job_id}`, dan `/api/analyses/{job_id}/preview`. Tetapkan `ROOT=Path(__file__).resolve().parents[2]` pada dua modul backend. `parents[3]` adalah bug lama yang membuat file model tidak ditemukan. `model_loaded=False` sebelum inferensi pertama wajar. Pertahankan `ai_error` dan `model_status`; **jangan buat prediksi palsu sebagai fallback**. Status SOP belum berubah menjadi patuh/melanggar.

Frontend React/Vite dev pada **5173**, proxy `/api` ke `127.0.0.1:8001`, bukan 8000. Jaga state loading, empty, error, offline, missing model, output berhasil dan warning. Bedakan grafik frame-difference dari klasifikasi R3D-18; tampilkan top-3/confidence sebagai softmax yang belum dikalibrasi. Jangan mengklaim streaming real-time, autentikasi, export atau SOP compliance bila belum ada implementasi.

## 6. Testing dan bukti hasil

**Yang sudah pernah teramati:** health API, path checkpoint/recipe benar, dan inferensi video 20 detik dengan 10 prediksi, `ai_error=null`. Ini **smoke test**, bukan seluruh suite automated. Jangan menyatakan tes lain lolos tanpa log.

**Pengujian wajib sebelum menyelesaikan perubahan:** kompilasi backend, build frontend, cek `/api/health` dari backend dan proxy, POST video legal dengan `curl.exe`, validasi kelas/timestamp/top3, file kosong/corrupt/salah ekstensi, checkpoint hilang, bobot pretrained tak tersedia, durasi/ukuran batas, kode respons dan UI error. Untuk perubahan preprocessing, bandingkan inferensi **interval anotasi identik** dengan notebook; jangan bandingkan secara sembarang dengan video 20 detik yang menggunakan jendela lain. Rekam command, lingkungan, tanggal dan hasil—atau sebut belum diuji.

```powershell
# Dari root
.\backend\.venv\Scripts\python.exe -m compileall -q .\backend\app
.\backend\.venv\Scripts\python.exe -c "from backend.app.v6_inference import readiness; print(readiness())"
Invoke-RestMethod http://127.0.0.1:8001/api/health
Invoke-RestMethod http://localhost:5173/api/health
# Di frontend
npm run build
```

Windows PowerShell 5.1 tidak mendukung `Invoke-RestMethod -Form` untuk multipart; gunakan `curl.exe -F "file=@..."`. Jika `Errno 10048`, matikan backend lama sebelum menjalankan lagi. Jika frontend `ECONNREFUSED :8000`, koreksi proxy. Jika status model False, cek root `parents[2]` dan restart server.

## 7. Keamanan, privasi, lisensi, deployment

Aplikasi saat ini **lokal dan eksperimental**, tanpa bukti auth, kebijakan retensi otomatis, rate limit, atau audit keamanan publik. Video dapat berisi orang/lokasi sensitif; pastikan izin pemrosesan, perlindungan penyimpanan, aturan hapus, akses terbatas, uji codec, rate/resource limit, monitoring dan review manusia sebelum deployment. Jangan membuka endpoint demo ke internet tanpa hardening. Batas default upload 150×1024×1024 byte dan metadata hingga 30 menit; inferensi AI hanya 0,6–120 detik. Ketidaksamaan batas merupakan risiko yang harus ditangani.

Lisensi MIT berlaku untuk kode. Dataset Assembly101 memiliki lisensi/syarat tersendiri; bobot pretrained juga pihak ketiga. Jangan mengklaim legalitas komersial, sertifikasi keselamatan atau penilaian pekerja.

## 8. Dokumentasi bilingual dan seluruh aset nyata

Semua Markdown yang diperbarui harus substantif dalam **English dan Indonesia**, tidak cukup menerjemahkan judul. README utama wajib berisi masalah, objective, Before–Now–Next, audit/provenance, kelas, split, leakage, arsitektur, metodologi, metrik yang jujur, error analysis, keterbatasan, struktur aktual, setup, API, reproducibility, testing, security, deployment, troubleshooting, FAQ, roadmap, license dan referensi. Jika komponen berubah, perbarui README terkait pada kedua bahasa.

**Aset gambar yang benar-benar ada:** `assets/plots/learning_curves.png`, `assets/plots/test_confusion_matrix.png`, `reports/v6/examples/center_vs_motion_roi.jpg`, `assets/screenshots/Screenshot 2026-11-04 193324.png`. Gunakan `![alt](path-relatif)` agar langsung terlihat di GitHub dan sertakan caption tentang bukti serta keterbatasan. Untuk nama file dengan spasi, encode `%20`. Cocokkan grafik dengan CSV/JSON sumber. Jangan mengarang gambar dari folder `assets/examples/` atau `assets/diagrams/` yang masih placeholder `.gitkeep`. Mermaid boleh digunakan sebagai diagram sumber teks.

**Standar klaim:** fitur terimplementasi ≠ fitur sudah diuji; inferensi berhasil ≠ prediksi benar; validasi ≠ test; test eksploratif ≠ blind; klasifikasi aktivitas ≠ deteksi pelanggaran SOP. Jangan menghilangkan catatan ini demi tampilan profesional.

## 9. Git, delivery, review dan workflow

Selalu cek `git status`, diff, data yang akan distage dan keamanan `.gitignore`. Jangan commit `node_modules`, `.venv`, dataset/video, bobot besar, secrets atau `backend/storage`. Hindari `git add .` secara buta; gunakan `git add README.md AGENTS.md` untuk perubahan dokumentasi utama. Jangan menimpa branch, force push atau menghapus data tanpa kewenangan.

**Fase wajib:**

| Fase | Pekerjaan | Bukti |
|---|---|---|
| 0 — Audit repo | Daftar struktur/file riil dan konflik status. | Inventaris + diff. |
| 1 — Audit data/model | Hak sumber, label, split, recipe, checkpoint, metrik dan timebase. | JSON/CSV/notebook/model card. |
| 2 — Backend inference | Kode asli dan pesan gagal yang jujur. | API dan log uji nyata. |
| 3 — Frontend | UI nyata yang tersambung backend dan menampilkan warning. | Build/integrasi. |
| 4 — Integrasi, testing, dokumentasi | Verifikasi end-to-end, README bilingual, aset, audit klaim. | Output uji, dokumentasi, commit review. |

**Definition of done:** kode ada dan dieksekusi dengan input realistis, hasilnya diperiksa, kegagalan dan risiko dicatat, dokumentasi EN/ID sinkron, dan klaim tidak melebihi bukti. Jika belum lengkap, laporkan **parsial / eksperimen / belum teruji**. Sertakan perintah PowerShell, hasil yang benar-benar dijalankan, file yang berubah dan commit message profesional. Jangan mengaku sudah push jika belum.

---

**Final engineering principle / Prinsip akhir:** **Real problem → Audited data → Reproducible experiment → Honest evaluation → Working application → Complete documentation.**
