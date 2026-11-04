> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Notebooks — executed research record

The tracked research notebook is **`notebooks/visualsop-checker.ipynb`** (verified in the repository tree). Do not replace this name with an older suggested `VisualSOP_Day30_V6_FINETUNE_Kaggle.ipynb` without explicit instruction. V6 was the validation-selected experiment; notebook outputs must be authentic, not manually fabricated.

## Experimental workflow
Environment and dataset audit → label mapping → 30 FPS annotation timestamp conversion against approximately 60 FPS source videos → verify paired sessions → source-group-disjoint split → decode video clips → sample 16 frames → train/validation view generation → R3D-18 Kinetics-400 baseline/fine-tuning → validation-only selection → historically exposed exploratory test → per-class/CM/error analysis → controlled export of checkpoint, recipe, manifests, plots.

## Split and claims
Train 62 independent intervals / 124 temporal views; validation 17; reused exploratory test 16. Selected V6 validation accuracy 52.94%, macro-F1 51.11%; exploratory test 18.75%, macro-F1 11.11%. The old test was used previously and is not blind; do not tune with it or claim independence. Only 13 paired source sessions used.

## Reproducibility checklist
Document input dataset URLs and access terms, access date if known, annotation version, session IDs, split/group IDs, clip identifiers, preprocessing choices, random seeds, hardware and software environment, all train/validation logs, per-class performance, confusion matrix, best checkpoint selection and SHA-256. Use actual Kaggle run evidence. A changed code cell without execution is **not** an executed result.

## Source locations
Assembly101: https://huggingface.co/datasets/cvml-nus/assembly101; https://assembly101.github.io/. Previous input mounts: `/kaggle/input/datasets/wafabila/visualsop-dataset` and `/kaggle/input/datasets/wafabila/visualsop-dataset-next` (access not guaranteed). Raw recordings and annotations are not redistributed.

## Downstream
The FastAPI inference implementation must match `models/inference_recipe.json`. The 3-second window/2-second stride video demo is a later heuristic; evaluate it separately from clip-level notebook metrics. No SOP violation ground truth exists.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Notebook — catatan eksperimen yang dieksekusi

Notebook yang **benar-benar ada di repository** adalah `notebooks/visualsop-checker.ipynb`. Jangan mengganti nama menjadi nama usulan lama `VisualSOP_Day30_V6_FINETUNE_Kaggle.ipynb` tanpa persetujuan. V6 merupakan eksperimen pilihan dari validasi; output notebook harus benar-benar dihasilkan eksekusi.

## Alur eksperimen
Audit environment/dataset → pemetaan label → konversi waktu anotasi 30 FPS terhadap video sekitar 60 FPS → pasangkan sesi → split kelompok sumber → decode clip → sampling 16 frame → dua view temporal train → baseline/fine-tune R3D-18 Kinetics-400 → pemilihan berbasis validasi → exploratory test historis → analisis per kelas/confusion matrix → ekspor checkpoint, recipe, manifest, plot.

## Split dan batas klaim
62 interval train independen / 124 tampilan temporal; validation 17; reused exploratory test 16. Validasi V6 52,94% accuracy dan 51,11% macro-F1; test eksploratif 18,75% accuracy dan 11,11% macro-F1. Test lama sudah dipakai dalam eksperimen sebelumnya, jadi tidak blind. Total sesi sumber terpasangkan hanya 13.

## Standar reproducibility
Catat URL sumber/ketentuan lisensi, tanggal akses jika diketahui, versi anotasi, sesi dan kelompok split, ID klip, preprocessing, seed, perangkat, versi library, histori training, evaluasi per kelas, confusion matrix, dasar pemilihan model, checksum checkpoint. Gunakan bukti runtime Kaggle asli. Mengedit sel kode **bukan** bukti eksperimen sudah dijalankan.

## Sumber
Assembly101: https://huggingface.co/datasets/cvml-nus/assembly101; https://assembly101.github.io/. Direktori Kaggle yang pernah digunakan: `/kaggle/input/datasets/wafabila/visualsop-dataset` dan `/kaggle/input/datasets/wafabila/visualsop-dataset-next` (akses bergantung pemilik). Video/anotasi mentah tidak diunggah ulang.

## Hubungan dengan aplikasi
Backend harus mengikuti `models/inference_recipe.json`. Jendela 3 detik/stride 2 detik di demo adalah heuristik baru dan wajib dievaluasi terpisah dari metrik clip-level. Belum ada ground truth pelanggaran SOP.
