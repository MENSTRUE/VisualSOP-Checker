> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Limitations, risks, claim boundaries and roadmap

## What is proven
- Local FastAPI + Vite/React integration can execute **real** R3D-18 V6 inference with local checkpoint and recipe.
- A 20-second authorized Assembly101 sample returned ten overlapping 3-second/2-second-stride window predictions, `model_status=experimental_v6`, `ai_error=null`.
- Research data and evaluations are documented in `models/MODEL_CARD.json` and `reports/v6`.

## What is NOT proven
No reliable generalization (exploratory test 18.75% accuracy, 11.11% macro-F1), no blind independent test, no validated temporal action boundaries, no SOP rules, no ground-truth SOP violation labels, no real manufacturing trials, no calibrated confidence and no safety/privacy assurance. `sop_status=not_evaluated` is the only defensible current compliance status.

## Data/model risks
Only 13 paired sessions (62 independent training intervals), tiny validation/test, 14/16 test intervals from one group, test historically exposed, annotations indexed at 30 FPS while videos about 60 FPS, sensitivity to toy/viewpoint, motion ROI attention to irrelevant movement, strongly correlated temporal train views, and softmax overconfidence.

## Software/operations risks
Local upload code processes videos and stores them in `backend/storage` with no authentication. Default max 150 MB and metadata up to 30 min; AI classifier caps 120 s. Media parsing, CPU/GPU load, concurrency, retention, exception logging and untrusted model loading need hardening. Never expose localhost demo to public networks without threat modelling and controls.

## Claims you may make
“Experimental six-class action recognition prototype using Assembly101, with an R3D-18 model selected on validation and integrated into a local video-analysis API/UI. Poor exploratory test generalization remains unresolved.” Include the validation/test figures and test caveat nearby.

## Claims you may NOT make
“Certified SOP checker,” “detects production violations,” “80%+ accuracy,” “real-time industry monitoring,” “safe for worker assessment,” “calibrated certainty,” “independent blind test passed,” or “production ready.”

## Roadmap, not completed features
**P0** verify local testability and add API/UI regression tests; audit actual 20-second demo against original action timestamps. **P1** acquire more licensed paired sessions and seal an untouched source-group test; evaluate calibration and per-group distribution shift. **P2** temporal segmentation and domain-specific SOP rules with human-annotated violations. **P3** production security/privacy/retention, operational observability and deployment evaluation. Completion requires execution evidence and updated bilingual documentation.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Keterbatasan, risiko, batas klaim, dan roadmap

## Yang sudah terbukti
- FastAPI + Vite/React lokal dapat menjalankan inferensi **asli** R3D-18 V6 dengan checkpoint dan recipe yang tersedia.
- Video Assembly101 20 detik pernah menghasilkan sepuluh prediksi jendela 3 detik/stride 2 detik, `model_status=experimental_v6`, `ai_error=null`.
- Data dan evaluasi penelitian terdokumentasi dalam `models/MODEL_CARD.json` dan `reports/v6`.

## Yang belum terbukti
Belum ada generalisasi andal (test eksploratif hanya 18,75% akurasi dan 11,11% macro-F1), blind test independen, batas waktu aksi yang tervalidasi, aturan SOP, ground truth pelanggaran SOP, uji pabrik nyata, kalibrasi confidence, ataupun jaminan privasi/keamanan. `sop_status=not_evaluated` adalah status kepatuhan yang tepat saat ini.

## Risiko data dan model
Hanya 13 sesi terpasangkan (62 interval training asli), val/test kecil, 14/16 interval test dari satu kelompok, test lama sudah terlihat, anotasi menggunakan indeks 30 FPS vs video sekitar 60 FPS, domain shift mainan/kamera, motion ROI bisa memilih gerakan tidak relevan, dua view train saling berkorelasi, dan softmax bisa terlalu yakin.

## Risiko software dan operasional
Kode upload lokal menyimpan video ke `backend/storage` tanpa autentikasi. Default maks 150 MB dan metadata 30 menit; inferensi AI maks 120 detik. Parsing video, pemakaian resource CPU/GPU, concurrency, retensi, logging dan loader bobot dari file tidak tepercaya masih memerlukan hardening. Jangan membuka demo localhost ke jaringan publik tanpa mitigasi.

## Klaim yang boleh
“Prototipe pengenalan enam aktivitas Assembly101 berbasis R3D-18, dipilih melalui validasi dan diintegrasikan ke API/UI video lokal; generalisasi test eksploratif masih buruk.” Sertakan angka metrik dan catatan non-blind.

## Klaim yang dilarang
“Checker SOP tersertifikasi”, “mendeteksi pelanggaran SOP pabrik”, “akurasi di atas 80%”, “monitoring real-time industri”, “aman untuk penilaian pekerja”, “confidence terkalibrasi”, “sukses blind test”, “siap produksi”.

## Roadmap, masih rencana
**P0:** pastikan demo dan tes regresi API/UI, audit prediksi video terhadap anotasi asal. **P1:** tambah data legal, blind split sumber baru, evaluasi domain shift dan confidence. **P2:** segmentasi temporal serta aturan SOP/domain dengan pelanggaran yang dianotasi manusia. **P3:** keamanan, privasi, retensi, observabilitas dan studi deployment. Fitur baru baru disebut selesai ketika ada bukti eksekusi serta dokumentasi dua bahasa yang sinkron.
