> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Scripts and reproducibility utilities

## Current status
The `scripts/` directory is retained as a stable repository location. The current checked-in tree contains documentation, not a verified automated end-to-end research runner. Do **not** claim executable audit, training, prediction, model migration or packaging scripts exist until they are committed and run.

## Intended reproducibility utilities (roadmap)
1. Safe dataset inventory reader that respects Assembly101 access terms; never silently downloads or republishes gated recordings.
2. Annotation/timebase validator (30 FPS annotation basis against ~60 FPS recordings).
3. Source-group split and leakage audit, with duplicate/overlap checks.
4. Model artifact manifest generator: SHA-256, class order, recipe and environment.
5. Evaluation CLI to produce per-class reports, confusion matrices and error examples from real predictions.
6. Local smoke-test runner for FastAPI/React integration using authorized fixture video.

All proposed scripts require explicit implementation and execution before being described as available.

## Contribution standards
Scripts should be idempotent where practical, accept explicit input/output paths, work on Windows PowerShell or document platform requirements, fail with actionable errors, and never overwrite evidence without versioning. Keep datasets and weight files ignored. Preserve the repository folder structure and update **both language sections** in relevant Markdown files.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Scripts dan utilitas reproducibility

## Kondisi sekarang
Folder `scripts/` dipertahankan sebagai bagian standar repository. Tree GitHub yang diaudit berisi dokumentasi, **belum** skrip otomatis end-to-end yang sudah diverifikasi. Jangan mengklaim skrip audit, training, prediksi, migrasi atau packaging tersedia jika belum dikomit dan diuji.

## Rencana utilitas
1. Inventaris dataset aman yang mematuhi hak akses Assembly101 dan tidak mengunduh/menyebar ulang data gated secara diam-diam.
2. Validator konversi timebase anotasi 30 FPS versus video sekitar 60 FPS.
3. Audit split kelompok sumber, kebocoran, duplikasi dan interval tumpang tindih.
4. Pembuat manifest artefak model (SHA-256, urutan kelas, recipe, environment).
5. CLI evaluasi untuk per-class, confusion matrix, dan kasus error berdasarkan prediksi aktual.
6. Smoke-test integrasi FastAPI/React dengan video fixture yang telah mendapat izin.

Semua masih **roadmap** sampai ada implementasi dan bukti eksekusi.

## Standar kontribusi
Usahakan idempotent, input-output eksplisit, dukung PowerShell Windows atau tulis persyaratan platform, error dapat ditindaklanjuti, dan jangan menimpa artefak tanpa versi. Data/bobot tetap di-ignore. Pertahankan struktur folder; jika `.md` diperbarui, **English dan Bahasa Indonesia wajib sinkron**.
