> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Experiment reports and audit evidence

`reports/v6/` stores **real executed V6 outputs**, not marketing claims. Only assert metrics that match the files. V6 is selected by validation, not by an independent blind test. The historically reused exploratory test remains non-blind.

## Directory map
| Path | Evidence |
|---|---|
| `v6/audit/session_inventory.csv` | Candidate/paired session inventory |
| `v6/audit/video_metadata.csv` | Video metadata |
| `v6/audit/segments.csv` | Extracted action intervals |
| `v6/audit/cached_clips.csv` | Cached clip records |
| `v6/audit/unmatched_annotation_sessions.csv` | Unpaired annotation sessions |
| `v6/metadata/dataset_provenance.json` | Data lineage and restrictions |
| `v6/metadata/environment.json` | Experiment software/hardware metadata |
| `v6/reports/results.json` | Reported metrics |
| `v6/reports/training_history.csv` | Learning progression |
| `v6/reports/test_per_class.csv` | Per-class evaluation |
| `v6/reports/test_confusion_matrix.csv` | Confusion matrix table |
| `v6/predictions/validation_predictions.csv` | Validation predictions |
| `v6/predictions/reused_exploratory_test_predictions.csv` | Non-blind exploratory predictions |
| `v6/plots/learning_curves.png`, `v6/plots/test_confusion_matrix.png` | Visual evidence |
| `v6/examples/center_vs_motion_roi.jpg` | ROI illustration |

## Frozen V6 figures
Validation 9/17 = 52.94% accuracy, 51.11% macro-F1; reused exploratory test 3/16 = 18.75% accuracy, 11.11% macro-F1. There are 62 independent training intervals (124 train clip views) and 13 paired video sessions. 14/16 test intervals belong to one group. Report sample sizes next to percentages and never call this independent test.

## Auditing new results
For every new run, preserve a new versioned report path rather than overwriting V6; include dataset lineage, complete configuration, environment, split, metrics, confusion matrix, prediction CSV, true experiment identifier and checksums. Label negative results faithfully. Avoid source footage and personal data in reports, and follow Assembly101 redistribution terms.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Laporan eksperimen dan bukti audit

`reports/v6/` menyimpan **hasil eksekusi V6 yang nyata**, bukan klaim pemasaran. Angka harus cocok dengan file bukti. V6 dipilih berdasarkan validasi; exploratory test historis pernah terlihat dan **bukan blind test**.

## Peta folder bukti
| Lokasi | Isi |
|---|---|
| `v6/audit/session_inventory.csv` | Inventaris sesi kandidat/terpasangkan |
| `v6/audit/video_metadata.csv` | Metadata video |
| `v6/audit/segments.csv` | Interval aksi hasil ekstraksi |
| `v6/audit/cached_clips.csv` | Catatan clip cache |
| `v6/audit/unmatched_annotation_sessions.csv` | Sesi anotasi yang tidak berpasangan |
| `v6/metadata/dataset_provenance.json` | Asal data dan pembatasan |
| `v6/metadata/environment.json` | Informasi environment eksperimen |
| `v6/reports/results.json` | Metrik |
| `v6/reports/training_history.csv` | Histori pembelajaran |
| `v6/reports/test_per_class.csv` | Evaluasi tiap kelas |
| `v6/reports/test_confusion_matrix.csv` | Matriks kesalahan numerik |
| `v6/predictions/validation_predictions.csv` | Prediksi validasi |
| `v6/predictions/reused_exploratory_test_predictions.csv` | Prediksi test historis non-blind |
| `v6/plots/learning_curves.png`, `v6/plots/test_confusion_matrix.png` | Grafik bukti |
| `v6/examples/center_vs_motion_roi.jpg` | Ilustrasi ROI |

## Metrik V6 yang dibekukan
Validasi 9/17 = 52,94% akurasi dan 51,11% macro-F1; reused test 3/16 = 18,75% akurasi dan 11,11% macro-F1. Train 62 interval independen/124 tampilan clip, 13 sesi sumber terpasangkan; 14/16 interval test dari satu kelompok. Cantumkan jumlah sampel saat menampilkan persentase; jangan disebut uji independen.

## Audit eksperimen baru
Simpan hasil baru ke direktori versi baru, jangan menimpa V6. Wajib catat lineage dataset, konfigurasi, environment, split, metrik, confusion matrix, prediction CSV, identitas run dan checksum. Laporkan hasil buruk dengan jujur. Hindari memasukkan rekaman sumber dan data personal ke laporan; taati ketentuan distribusi Assembly101.
