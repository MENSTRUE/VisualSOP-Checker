> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Model card — VisualSOP V6 R3D-18

## Overview
- **Task:** six-class *coarse toy assembly action recognition* (not SOP violation detection).
- **Architecture:** `torchvision.models.video.r3d_18`, official Kinetics-400 pretrained weights; fine-tuned `layer4` and six-way `fc`.
- **Research dataset:** 13 paired Assembly101 video sessions, 62 independent training action intervals, 17 validation, 16 historically reused exploratory test; train uses 124 temporal clip views.
- **Status:** `RESEARCH_ONLY`; not evaluated for production SOP compliance or safety use.
- **Evidence source:** `models/MODEL_CARD.json`, V6 report directory and executed Kaggle notebook.

## Class map
`attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis` (fixed order). Input: 16 RGB video frames, short edge resize 128, crop ROI center/motion and pretrained transforms, `ensemble` crop logit averaging selected by validation.

## Evaluation
| Set | Independent intervals | Accuracy | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|---:|
| Validation | 17 | **52.94%** (9/17) | **51.11%** | 51.39% |
| Reused exploratory test (non-blind) | 16 | **18.75%** (3/16) | **11.11%** | 16.67% |

Best epoch 10. Test historically exposed and dominated by one group (14/16 test intervals from group 9021). Sample size is too small for strong generalization claims. No independent blind test and no SOP-violation ground truth. Per-class details in `reports/v6/reports/test_per_class.csv` and predictions/CM.

## Intended and prohibited use
**Permitted research intent:** investigate activity recognition, error patterns and video-model integration, with human review. **Prohibited claim/use:** automatic compliance assessment, safety monitoring, worker surveillance/scoring, production decisions, certified anomaly/violation detection, or legal/disciplinary action. No calibration evidence for confidence percentages.

## Technical and social limitations
Small and imbalanced groups, video/annotation timebase mismatch risk, heuristic motion ROI possibly tracking irrelevant motion, distribution shift, non-blind test reuse, no procedural object-state understanding, and no independent segment localization. A demonstrated 20-second upload returned ten window-level predictions, mostly `detach cabin`; correctness not independently checked. Failing or absent model must be surfaced as error; no fabricated fallback outputs.

## Artifact handling
`models/best_finetuned_layer4_fc.pt` is a locally controlled, Git-ignored checkpoint containing **only layer4 and fc**. Base Kinetics-400 pretrained weights are necessary. Confirm recipe and class consistency before loading. Current loader uses `torch.load(weights_only=False)`; **never load untrusted checkpoints**. Preserve hash, source rights and artifact lineage separately. Code MIT; dataset Assembly101 gated/CC BY-NC conditions must be respected.

## Improvement criteria
Expand licensed paired data, create untouched blind evaluation, report metrics per source class/group, calibrate scores, establish temporal boundary labels, and collect explicit SOP violation annotations before claiming compliance functionality.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Kartu model — VisualSOP V6 R3D-18

## Gambaran
- **Tugas:** pengenalan enam kelas aktivitas kasar perakitan mainan, **bukan deteksi pelanggaran SOP**.
- **Arsitektur:** `torchvision.models.video.r3d_18` pretrained resmi Kinetics-400; fine-tune `layer4` dan `fc` enam kelas.
- **Data:** 13 sesi video Assembly101 terpasangkan, 62 interval train independen, 17 val, 16 test eksploratif historis; data train menjadi 124 tampilan temporal.
- **Status:** `RESEARCH_ONLY`, tidak tervalidasi untuk produksi atau keselamatan.
- **Bukti:** `models/MODEL_CARD.json`, laporan V6, notebook Kaggle yang dieksekusi.

## Peta kelas dan preprocessing
`attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis` dalam urutan tetap. Input 16 frame RGB, resize sisi pendek 128, ROI center/motion, transform pretrained, dan rata-rata logits `ensemble` yang dipilih melalui validasi.

## Evaluasi
| Data | Interval independen | Akurasi | Macro-F1 | Balanced accuracy |
|---|---:|---:|---:|---:|
| Validasi | 17 | **52,94%** (9/17) | **51,11%** | 51,39% |
| Test eksploratif reused (non-blind) | 16 | **18,75%** (3/16) | **11,11%** | 16,67% |

Epoch terbaik 10. Test lama pernah dilihat dan didominasi satu kelompok (14/16 interval dari 9021). Sampel terlalu kecil untuk menyatakan generalisasi kuat. Tidak ada blind test independen maupun ground truth pelanggaran SOP. Detail per kelas di `reports/v6/reports/test_per_class.csv` dan confusion matrix.

## Penggunaan yang sesuai dan dilarang
**Tujuan riset:** mengevaluasi pengenalan aksi, kesalahan, dan integrasi model video dengan review manusia. **Tidak boleh diklaim/digunakan:** otomatisasi keputusan patuh/tidak patuh SOP, pemantauan keselamatan, penilaian pekerja, keputusan produksi, ataupun bukti pelanggaran untuk tindakan hukum/disiplin. Confidence persentase belum dikalibrasi.

## Keterbatasan
Sesi kecil dan tidak seimbang, risiko salah konversi basis waktu 30/60 FPS, motion ROI yang bisa fokus ke gerakan lain, domain shift, reuse test tidak buta, tidak memahami keadaan benda/urutan prosedur, dan tidak ada lokalisasi batas aksi terlatih. Demo video 20 detik menampilkan sepuluh prediksi, mayoritas `detach cabin`, tetapi kebenarannya belum diverifikasi. Jangan buat fallback prediksi palsu saat model gagal.

## Penanganan artefak
File lokal yang di-ignore `models/best_finetuned_layer4_fc.pt` hanya berisi **layer4 dan fc**; bobot dasar Kinetics-400 resmi wajib disediakan. Cocokkan recipe dan urutan kelas. Loader saat ini `torch.load(weights_only=False)`; **jangan muat checkpoint tidak tepercaya**. Simpan checksum, izin sumber dan lineage terpisah. Kode MIT; Assembly101 memiliki ketentuan gated/CC BY-NC tersendiri.

## Kriteria peningkatan
Tambah data sah dan beragam, buat blind test baru, laporkan metrik per kelas/kelompok, kalibrasi confidence, anotasi batas aksi, dan dataset eksplisit pelanggaran SOP sebelum klaim kepatuhan.
