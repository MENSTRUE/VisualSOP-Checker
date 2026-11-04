> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Research methodology and evaluation protocol

## Research objective and hypothesis
Evaluate whether Kinetics-400 pretrained R3D-18 adapted to six Assembly101 coarse actions generalizes across source toy/session groups. This is clip-level action recognition and an experimental local inference integration; **not** SOP violation detection.

## Labels and sampling
Class order (fixed): `attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis`. Use original Assembly101 coarse-label intervals and convert annotation indices using **30 FPS annotation timebase**. RGB source is about 60 FPS. Decode 16 frames within the inner 78% of the annotated interval, resize shorter edge to 128 and apply proper pretrained transforms. Training uses two temporal positions at 0.25 and 0.75; validation uses 0.5. Crops include center/motion-guided options; `ensemble` was selected via validation for V6.

## Data split
Source-group disjoint: train toy groups 9013/9014/9015/9022; val 9011/9012; test 9016/9021. Counts: 62 independent train intervals, represented by 124 correlated training views; 17 val, 16 historically reused exploratory test. Only 13 paired source sessions. Inspect `reports/v6/audit/` for exact source rows and pairing problems. Do not mix correlated intervals across groups.

## V6 model
Initialize `r3d_18(weights=R3D_18_Weights.DEFAULT)` using official Kinetics-400 weights. Freeze earlier blocks and train `layer4` + six-way classification `fc`. Selected best epoch **10**, validation-selected ROI `ensemble`. Export `layer4`, `fc`, `class_names`, ROI mode and matching `models/inference_recipe.json`. Loading random base weights is not a valid recreation.

## Selection and metrics
Use validation to pick checkpoint, ROI and hyperparameters. Evaluate accuracy, balanced accuracy, macro-F1, confusion matrix and per-class precision/recall. Frozen reported validation: 52.94% accuracy (9/17), 51.11% macro-F1; reused exploratory test: 18.75% accuracy (3/16), 11.11% macro-F1. The older test set was inspected in earlier iterations and **must not be described as independent or blind**. New benchmarking requires an untouched source-group-separated test set.

## Local video integration is a different protocol
A continuous upload is heuristically divided into 3-second windows, stride 2 seconds, with a tail window. Each window independently produces softmax top-3 labels. These windows are **not** annotated ground-truth action segments and do not prove temporal localization. Compare this new protocol against fresh timestamped annotations before reporting clip/event detection metrics. Confidence is uncalibrated.

## Reproducibility and risks
Preserve source attribution, IDs and split manifests, environment, seeds, input times, transformations, model state, run logs, true metrics, plots and hash of externally stored checkpoint. Audit duplicates, selection bias, imbalanced groups, domain shift and label noise. Do not train on historically seen test results. No claim of real-world manufacturing safety or SOP compliance is permitted.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Metodologi penelitian dan protokol evaluasi

## Tujuan
Menguji apakah R3D-18 pretrained Kinetics-400 yang diadaptasi ke enam aksi coarse Assembly101 mampu melakukan generalisasi antar kelompok mainan/sesi. Tugasnya **klasifikasi clip aktivitas**, bukan deteksi pelanggaran SOP.

## Label dan sampling
Urutan tetap: `attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis`. Gunakan interval anotasi coarse Assembly101 yang dikonversi dengan **timebase 30 FPS**, sementara rekaman video sekitar 60 FPS. Decode 16 frame dari 78% bagian tengah interval, resize sisi pendek menjadi 128 dan terapkan transform pretrained yang sama. Training menggunakan posisi temporal 0.25 dan 0.75; validasi posisi 0.5. Ada pilihan ROI center dan motion; `ensemble` dipilih berdasarkan validasi V6.

## Split
Pisah berdasar kelompok sumber: train 9013/9014/9015/9022; val 9011/9012; test 9016/9021. Jumlah: 62 interval train independen atau 124 tampilan training yang berkorelasi; val 17, test eksploratif historis 16. Hanya 13 sesi video terpasangkan. Detail pasangan dan audit di `reports/v6/audit/`. Jangan mencampur potongan berkorelasi antar split.

## Model V6
Bangun `r3d_18(weights=R3D_18_Weights.DEFAULT)` dengan bobot Kinetics-400 resmi. Bekukan blok sebelumnya lalu fine-tune `layer4` serta `fc` enam kelas. Epoch terbaik **10**, ROI terpilih `ensemble`. Simpan checkpoint berisi `layer4`, `fc`, `class_names`, ROI dan `models/inference_recipe.json` yang konsisten. Tidak valid membangun dengan bobot dasar acak.

## Pemilihan dan metrik
Hanya gunakan validasi untuk memilih model dan pengaturan. Metrik: accuracy, balanced accuracy, macro-F1, per-class precision/recall dan confusion matrix. Validasi V6 akurasi 52,94% (9/17), macro-F1 51,11%; reused test akurasi 18,75% (3/16), macro-F1 11,11%. Test lama **sudah pernah diperiksa**, bukan evaluasi blind independen. Benchmark baru harus memisahkan data sumber yang belum tersentuh.

## Inferensi video kontinu adalah protokol berbeda
Unggahan video dipotong secara heuristik menjadi jendela 3 detik/stride 2 detik dengan tail window. Setiap jendela menghasilkan top-3 softmax. Batas jendela bukan segmentasi aksi terlatih dan tidak membuktikan lokalisasi temporal. Evaluasi dengan anotasi timestamp baru sebelum melaporkan metrik event detection. Confidence belum dikalibrasi.

## Reproducibility dan risiko
Pertahankan atribusi sumber, manifest ID/split, environment, seed, waktu input, transformasi, state model, log training, hasil nyata, plot dan checksum checkpoint. Audit duplikasi, bias seleksi, ketidakseimbangan sumber, domain shift, serta noise label. Jangan mengoptimalkan berdasarkan test lama. Tidak boleh mengklaim validasi keselamatan manufaktur atau SOP compliance.
