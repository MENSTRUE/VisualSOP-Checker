> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Models — baseline, contracts and artifact policy

## Selected V6 baseline
Model: torchvision R3D-18 pretrained on Kinetics-400, with `layer4` and `fc` fine-tuned for six Assembly101 toy-assembly action categories. The selection was validation-based, not based on an untouched external benchmark. **Research-only model.**

| Evidence | Value |
|---|---:|
| Validation | 17 intervals; accuracy **52.94%**, macro-F1 **51.11%** |
| Reused exploratory test | 16 intervals; accuracy **18.75%**, macro-F1 **11.11%** |
| Source sessions / training intervals | 13 paired sessions / 62 independent train intervals |
| Blind independent test | **No** |
| SOP violation ground truth | **No** |

Metrics are grounded in `models/MODEL_CARD.json` and `reports/v6/`.

## Locally required files
- `models/inference_recipe.json` (tracked) — class order, 16 frames, resize short edge 128, inner fraction 0.78, ROI `ensemble`, transforms.
- `models/MODEL_CARD.json` (tracked) — claims, metrics, limitations.
- `models/best_finetuned_layer4_fc.pt` (local only, ignored by Git) — fine-tuned `layer4` and `fc` states; not a standalone complete model.
- Official Kinetics-400 pretrained R3D-18 weights in torchvision's cache (third-party artifact).

**Never** load only the fine-tuned checkpoint into `r3d_18(weights=None)` and claim valid predictions. Verify six class names and ROI mode match checkpoint and recipe; fail closed on incompatibility. Current inference uses `torch.load(..., weights_only=False)` for the known locally controlled checkpoint: never load an untrusted `.pt` because Python pickle deserialization can execute code. Future work should move to a safer format/loader where practical.

## Provenance and distribution
Checkpoint isn't committed; preserve a private, access-controlled artifact and record SHA-256, code commit SHA, training environment, source rights, recipe version, model lineage, and exact retrieval steps. Do not invent a download URL or version string. MIT licensing of original code does not override the Assembly101 dataset license or the pretrained weights' license.

## Evaluation and deployment
High softmax confidence is not calibrated correctness. Test performance is weak; the old test is not blind. Model is unsuitable for production SOP enforcement, safety surveillance or personnel scoring. More diverse licensed data, blind testing, calibration, and a separately annotated violation dataset are required.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Model — baseline, kontrak dan aturan artefak

## Baseline V6 terpilih
Model adalah torchvision R3D-18 pra-latih Kinetics-400 yang fine-tune `layer4` dan `fc` untuk enam kategori aktivitas Assembly101. Pemilihan model melalui validasi, bukan benchmark eksternal yang masih tersegel. Statusnya **khusus penelitian**.

| Bukti | Nilai |
|---|---:|
| Validation | 17 interval; akurasi **52,94%**, macro-F1 **51,11%** |
| Test eksploratif terpakai ulang | 16 interval; akurasi **18,75%**, macro-F1 **11,11%** |
| Sesi / interval train | 13 sesi terpasang / 62 interval independen |
| Test independen benar-benar buta | **Tidak** |
| Label ground truth pelanggaran SOP | **Tidak ada** |

Sumber angka adalah `models/MODEL_CARD.json` dan `reports/v6/`.

## File lokal wajib
- `models/inference_recipe.json` (tracked): urutan kelas, 16 frame, short-edge 128, inner fraction 0.78, ROI `ensemble`, transform.
- `models/MODEL_CARD.json` (tracked): metrik, batas klaim dan keterbatasan.
- `models/best_finetuned_layer4_fc.pt` (lokal, di-ignore): state fine-tune `layer4` dan `fc`, **bukan** model lengkap.
- Bobot pra-latih resmi Kinetics-400 R3D-18 di cache torchvision.

**Jangan** memasangkan checkpoint fine-tune ke `r3d_18(weights=None)` lalu menyebutnya model valid. Validasi kesamaan kelas dan ROI pada recipe dan checkpoint. Kode saat ini memakai `torch.load(..., weights_only=False)` untuk checkpoint lokal yang dipercaya; **jangan memuat file `.pt` dari sumber tidak tepercaya** karena deserialisasi pickle dapat menjalankan kode. Perbaikan format loader yang lebih aman termasuk pekerjaan berikutnya.

## Provenance dan distribusi
Bobot tidak dikomit. Simpan sebagai artefak terkontrol, rekam SHA-256, commit SHA kode, environment training, izin dataset, recipe, lineage dan langkah pemulihan. Jangan menciptakan URL download atau versi yang tidak nyata. Lisensi MIT kode tidak otomatis mencakup Assembly101 dan bobot dari pihak lain.

## Kualitas dan deployment
Confidence tinggi bukan bukti prediksi benar; softmax belum dikalibrasi. Hasil test lemah dan bukan blind. Model tidak layak menilai SOP produksi, keselamatan, atau pekerja. Butuh lebih banyak data legal, test buta baru, kalibrasi, dan anotasi pelanggaran SOP yang terpisah.
