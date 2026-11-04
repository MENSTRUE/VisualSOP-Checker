> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Dataset provenance, licensing, and audit — Assembly101

## Primary upstream sources
- Official project: https://assembly101.github.io/
- Dataset access: https://huggingface.co/datasets/cvml-nus/assembly101
- Dataset role: action-label research for toy assembly/disassembly, not industrial SOP-violation ground truth.

## What V6 actually used
Nine initially paired RGB recordings plus four additional recordings = **13 paired video sessions**. The source-side inventory contained **680 coarse-annotation files**. Many annotated sessions were not paired with sampled source videos; do not infer full-dataset coverage. Training 62 independent action intervals (124 correlated clip views); validation 17; historically reused exploratory test 16. Paired groups: train 9013/9014/9015/9022; validation 9011/9012; test 9016/9021. Sample sizes and candidate pairing should be audited from `reports/v6/audit/` and `v6/metadata/dataset_provenance.json`.

## Essential temporal metadata
Annotations use a **30 FPS annotation-index timebase**, whereas RGB videos are approximately **60 FPS**. Convert index-based annotations to seconds using 30 as documented. Never equate annotation frame indices with raw video frame indices. Store video identifiers, action label, annotation original start/end, conversion method and clip timestamps; validate timing visually.

## Usage and rights
Assembly101 comes with its own access conditions and CC BY-NC 4.0 restrictions, including non-commercial terms; always check actual dataset license/access terms before any reuse. Do not assume repository MIT code license grants rights to source footage. Do not commit raw recordings, gated archives or redistributed annotated video clips. Retain attribution and annotate derivatives. Official pretrained weights are a separate third-party dependency.

## Provenance discipline
Record exact URL(s), upstream revision/version if available, date of access (if documented), file identifiers, checksums where lawful, rights/permissions, extraction/preprocessing, retained/excluded sessions, annotation pairing failures and known representativeness gaps. **Do not invent** version or access date when unavailable; mark `not recorded`. Support each metrics claim from report files, not dataset marketing text.

## Known limitations
Toy actions differ from manufacturing settings. Only 13 paired sessions and a small segment sample were analyzed. The exploratory test was historically inspected; 14 of 16 test intervals came from one group. Source-group disjoint split reduces some leakage but does not ensure diversity or a blind test. No SOP violations or production equipment labels exist in these experimental labels.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Provenance, lisensi, dan audit dataset — Assembly101

## Sumber primer
- Proyek resmi: https://assembly101.github.io/
- Akses dataset: https://huggingface.co/datasets/cvml-nus/assembly101
- Kegunaan: riset label aksi perakitan/pembongkaran mainan, **bukan** ground truth pelanggaran SOP industri.

## Data yang benar-benar digunakan V6
Sembilan video RGB awal dan empat video tambahan = **13 sesi video terpasangkan**. Inventaris awal memiliki **680 file anotasi coarse**. Banyak anotasi tidak memiliki pasangan dalam video yang digunakan sehingga tidak boleh mengklaim seluruh dataset terpakai. Train 62 interval asli independen (124 tampilan klip berkorelasi); val 17; reused exploratory test 16. Kelompok: train 9013/9014/9015/9022, val 9011/9012, test 9016/9021. Verifikasi seluruh nama video dan pasangan dari `reports/v6/audit/` dan `reports/v6/metadata/dataset_provenance.json`.

## Konversi waktu penting
Anotasi menggunakan **basis indeks 30 FPS**, video sumber sekitar **60 FPS**. Konversikan indeks anotasi ke detik dengan 30 sesuai definisi; jangan samakan dengan indeks frame video mentah. Catat ID video, label, indeks start/end, aturan konversi dan timestamp potongan. Audit hasilnya secara visual agar tidak terjadi label salah akibat perbedaan FPS.

## Hak penggunaan
Assembly101 mempunyai syarat akses sendiri termasuk CC BY-NC 4.0 (non-komersial) yang harus diperiksa sebelum penggunaan ulang. Lisensi MIT kode tidak otomatis memberikan hak atas video sumber. Jangan commit rekaman/arsip gated atau mengunggah ulang potongan video beranotasi tanpa izin. Simpan atribusi dan informasi turunan. Bobot pretrained juga milik pihak ketiga dengan ketentuan terpisah.

## Disiplin provenance
Rekam URL asli, versi/revisi upstream bila ada, tanggal akses bila tercatat, ID file, checksum bila diizinkan, perizinan, transform/preprocessing, sesi yang dipakai dan dikeluarkan, anotasi gagal pasang, serta ketimpangan representasi. **Jangan mengarang tanggal akses atau versi**; tulis `tidak tercatat` bila tidak ditemukan. Klaim metrik harus merujuk file laporan nyata.

## Batasan
Gerak merakit mainan berbeda dari lingkungan manufaktur. Data hanya 13 sesi terpasangkan dan sedikit interval; test historis terpapar, 14/16 dari satu kelompok. Split kelompok membantu mengurangi kebocoran tapi tidak menjamin keberagaman atau blind benchmark. Tidak ada label pelanggaran SOP/pabrik dalam dataset eksperimen ini.
