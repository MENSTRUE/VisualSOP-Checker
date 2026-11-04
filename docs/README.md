> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# Documentation index and evidence hierarchy

All existing repository Markdown documentation is **bilingual inside the same file**: English first, Bahasa Indonesia second. This preserves the fixed repository tree and avoids conflicting translations. Navigate via the language links at the top of each file.

## Project-wide
- [`../README.md`](../README.md) — complete research/system source of truth, architecture, status, metrics, installation, tests, troubleshooting, FAQ.
- [`../AGENTS.md`](../AGENTS.md) — non-negotiable coding-agent rules, repository contract and claim boundaries.
- [`../README_V6_SETUP.md`](../README_V6_SETUP.md) — local model integration runbook.

## Domain-specific
- [`dataset_provenance.md`](dataset_provenance.md) — source records, timebase, license and non-redistribution.
- [`methodology.md`](methodology.md) — split design, model, training, evaluation and inference differences.
- [`model_card.md`](model_card.md) — validated experimental scope, metrics and prohibited use.
- [`limitations.md`](limitations.md) — risks and staged roadmap.

## Component readmes
- [`../backend/README.md`](../backend/README.md), [`../frontend/README.md`](../frontend/README.md), [`../models/README.md`](../models/README.md), [`../notebooks/README.md`](../notebooks/README.md), [`../reports/README.md`](../reports/README.md), [`../scripts/README.md`](../scripts/README.md).

## Source-of-truth policy
Executable evidence and manifests outrank narrative summaries. Key authoritative data: `models/MODEL_CARD.json`, `models/inference_recipe.json`, `reports/v6/` and real source code. **Do not change these artifacts merely to fit documentation.** Metrics: validation 52.94% accuracy / 51.11% macro-F1; reused exploratory test 18.75% accuracy / 11.11% macro-F1, not blind. No SOP violation detection currently.

Update English and Indonesian sections together on every change. No dataset, model weight or application code is changed by this documentation-only package.

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# Indeks dokumentasi dan hierarki bukti

Seluruh Markdown yang sudah ada di repository dijadikan **dua bahasa dalam file yang sama**: English dahulu, Bahasa Indonesia sesudahnya. Format ini mempertahankan struktur folder dan mencegah dua terjemahan yang saling bertentangan. Gunakan link bahasa di bagian atas setiap file.

## Proyek
- [`../README.md`](../README.md) — source-of-truth proyek, arsitektur, status, metrik, instalasi, tes, troubleshooting dan FAQ.
- [`../AGENTS.md`](../AGENTS.md) — aturan coding agent, kontrak struktur dan batas klaim.
- [`../README_V6_SETUP.md`](../README_V6_SETUP.md) — panduan integrasi model lokal.

## Dokumen domain
- [`dataset_provenance.md`](dataset_provenance.md) — sumber, basis waktu, lisensi dan larangan redistribusi.
- [`methodology.md`](methodology.md) — desain split, training, model, evaluasi, dan protokol inference.
- [`model_card.md`](model_card.md) — cakupan penelitian, metrik dan penggunaan yang tidak boleh.
- [`limitations.md`](limitations.md) — risiko dan roadmap bertahap.

## README per komponen
- [`../backend/README.md`](../backend/README.md), [`../frontend/README.md`](../frontend/README.md), [`../models/README.md`](../models/README.md), [`../notebooks/README.md`](../notebooks/README.md), [`../reports/README.md`](../reports/README.md), [`../scripts/README.md`](../scripts/README.md).

## Source-of-truth
Bukti eksekusi dan manifest lebih kuat daripada ringkasan naratif. Artefak utama: `models/MODEL_CARD.json`, `models/inference_recipe.json`, `reports/v6/` serta kode implementasi. **Jangan ubah artefak agar cocok dengan tulisan**. Validasi 52,94% akurasi/51,11% macro-F1; reused test 18,75% akurasi/11,11% macro-F1 dan bukan blind. Belum ada deteksi pelanggaran SOP.

Saat ada perubahan wajib memperbarui English dan Bahasa Indonesia bersama. Paket ini tidak mengubah dataset, bobot model, atau kode aplikasi.
