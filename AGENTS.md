> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# AGENTS.md — VisualSOP Checker Engineering & Research Contract

**Scope:** Applies to the entire `MENSTRUE/VisualSOP-Checker` repository, including humans, AI coding assistants, research contributors and automation.  
**Last documentation review:** 2026-11-04.  
**Status:** Active local research prototype; **not** a validated SOP-compliance or production system.

> **Non-negotiable:** Do not invent data, experiment runs, outputs, screenshots, metrics, model readiness, API routes, security properties or deployment status. Do not call six-class toy-assembly action recognition “SOP violation detection.” Honor dataset rights and preserve the fixed repository structure.

## 1. Mission and definition of done

VisualSOP Checker is Day 30 in the 100 Days of Projects portfolio. Its current demonstrable purpose is to upload and inspect a video and optionally return **genuine experimental six-class R3D-18 V6 action predictions**. The future goal of visual SOP review is **not implemented**.

An agent's task is complete only when it:

1. Preserves repository structure and existing real features.
2. Confirms requirements against checked-in source-of-truth files, not assumptions.
3. Makes the smallest justified changes for the requested scope; produces full usable files when asked.
4. Tests what can actually be executed and distinguishes executed tests from recommendations.
5. Does not change baseline metrics or labels without new attributable execution evidence.
6. Documents data provenance, new requirements and known gaps.
7. Does not commit secrets, checkpoint weights, gated video data, temporary caches or `node_modules`.
8. Provides a clear change summary, exact verification commands, and risks/limitations.

## 2. Absolute repository structure contract

Maintain this root layout:

```text
README.md
AGENTS.md
LICENSE
.gitignore
.env.example
notebooks/
models/
reports/
assets/
  plots/
  examples/
  screenshots/
  diagrams/
backend/
frontend/
docs/
scripts/
```

**Forbidden without explicit owner approval:** renaming root folders, moving the notebook into `backend`, inventing a parallel `src/` project at root, renaming classes, changing the server port, flattening reports, deleting placeholder directories, creating a `datasets/` directory, or replacing existing code with generated scaffolding.

Use `.gitkeep` for intentionally empty directories. Extend the current structure **inside existing folders** rather than moving it. Preserve [`README_V6_SETUP.md`](README_V6_SETUP.md) as integration history if it exists.

### Known key locations

```text
notebooks/visualsop-checker.ipynb       V6 experiment source
models/MODEL_CARD.json                  machine-readable source-of-truth metrics
models/inference_recipe.json            inference contract / label mapping
models/best_finetuned_layer4_fc.pt      LOCAL ONLY (not committed)
reports/v6/audit/                       interval/session/video matching evidence
reports/v6/metadata/                    data and environment manifests
reports/v6/predictions/                 validation / reused test predictions
reports/v6/reports/                     metrics, training history and confusion
reports/v6/plots/                       published images
backend/app/main.py                     FastAPI upload/storage/motion and API
backend/app/v6_inference.py             real experimental V6 inference
backend/requirements.txt                backend package ranges
frontend/src/main.tsx                   React UI entry
frontend/src/style.css                  styling
frontend/vite.config.ts                 /api proxy -> 127.0.0.1:8001
frontend/package.json                   npm scripts and dependencies
docs/dataset_provenance.md              source and rights
docs/methodology.md                     research method
docs/limitations.md                     limitations and next steps
```

The GitHub repository **does not include model weights**. Do not delete local checkpoints merely because Git ignores them. Any new file path not listed above must be justified and documented.

## 3. Source-of-truth and conflict-resolution order

When documents disagree:

1. **Executed V6 result artifacts** in `reports/v6/` are authoritative for empirical scores, predictions and data audits, after checking their integrity.
2. `models/MODEL_CARD.json` and `models/inference_recipe.json` document the selected model and deployment preprocessing contract.
3. `notebooks/visualsop-checker.ipynb` defines the historical experiment; actual executed outputs still outrank notebook comments or intended logs.
4. `backend/app/*.py`, `frontend/src/*`, `frontend/vite.config.ts`, requirements and package manifests define **currently implemented behavior**.
5. `docs/*.md`, `README.md` and other prose explain the above; correct outdated prose when sources disagree, not vice versa.

Before claiming a change is deployed or a test passed, **actually run the relevant command** or record that it was not run. Do not infer production readiness from local HTTP 200 responses.

## 4. Ground-truth baseline — preserve these exact facts

### Current task

**Six-class coarse activity recognition** on toy assembly recordings from **Assembly101**. No ground-truth SOP violation labels; no step ordering/compliance model; no evaluated violation detector.

### Exact label order

```python
CLASSES = [
    'attach cabin',
    'attach wheel',
    'detach cabin',
    'detach wheel',
    'screw chassis',
    'unscrew chassis',
]
```

Do not alphabetize, translate, change ID mapping, reorder or add labels without retraining, producing a versioned model card and migration plan. Predictions using a mismatched mapping are invalid.

### Verified V6 research data

| Item | Evidence-backed value |
|---|---:|
| RGB recordings in the investigated subset | 9 earlier + 4 later = 13 sessions |
| Coarse annotation files inspected | 680 |
| Independent training intervals | 62 |
| Training clip views (correlated augmentations/views) | 124 |
| Validation intervals | 17 |
| Historically exposed exploratory test intervals | 16 |
| Best epoch | 10 |
| Selected ROI variant | `ensemble` |
| Validation accuracy / macro F1 | **52.94% / 51.11%** |
| Reused exploratory test accuracy / macro F1 | **18.75% / 11.11%** |
| Reused exploratory test correct | 3/16 |
| New independent blind test | **Not available** |
| 80% accuracy target met | **No** |
| Ground-truth SOP violation labels | **No** |

`models/MODEL_CARD.json` also records balanced accuracy **51.39% validation** and **16.67% reused exploratory test**, only 13/350 annotated sessions paired with videos, 14/16 test intervals from group 9021, and major coverage limitations. Treat this as a small, nonrepresentative research subset.

### Group splits

- Training toy groups: `9013`, `9014`, `9015`, `9022`.
- Validation groups: `9011`, `9012`.
- Historically exposed exploratory test groups: `9016`, `9021`.

Source-group separation is intended, but must be validated against file/video/session IDs. Do not leak correlated views, repeated videos or adjacent original intervals across splits. Historical test **must not be used for future tuning**; if it informs development, classify it as development evidence and obtain a new untouched blind holdout.

## 5. Dataset provenance, rights and integrity

Primary dataset references:

- https://assembly101.github.io/
- https://huggingface.co/datasets/cvml-nus/assembly101

Assembly101 is a restricted, gated toy assembly video dataset with upstream **CC BY-NC 4.0** conditions; confirm the original terms. This repository's MIT license **does not** license the upstream videos, annotation files, pretrained Kinetics-400 datasets or third-party artifacts.

For every new dataset or source update, record:

- Canonical source URL, original publisher, revision/version and access date.
- License, access conditions, redistribution restrictions and commercial-use constraints.
- Original format, frame/timestamp conventions, checksum/size when feasible.
- Count of source recordings, usable paired sessions, annotation segments, class counts and exclusions.
- Whether data is authoritative ground truth, only weakly supervised, auxiliary, derived or synthetic.
- Duplicate/near-duplicate checks, leakage control, label conflicts, corrupt media and resolution decisions.
- Immutable split/group assignments and independently held-out test protocol.
- Known biases, unpaired sessions and coverage limitations.

**Key timing rule:** Assembly101 coarse annotation frame indices use a **30 FPS annotation timebase**; source RGB recordings commonly report approximately **60 FPS**. Convert annotation indices to seconds with `/30` before seeking in video. Never change the constant to 60 because the raw MP4 reports 60 FPS.

Don't use unverified synthetic SOP violation labels as real factory ground truth. Don't upload or commit media subject to gated restrictions. No `datasets/` folder in the root; local external dataset locations remain outside tracked repo or in the existing ignored `dataset/` path only when explicitly approved.

## 6. ML architecture and preprocessing invariants

### V6 model

- `torchvision.models.video.r3d_18(weights=R3D_18_Weights.DEFAULT)`; pretrained base is Kinetics-400.
- Replace `model.fc = nn.Linear(512, 6)`.
- Load trained **`layer4` and `fc`** state dictionaries, strictly, from the V6 checkpoint.
- Local checkpoint `models/best_finetuned_layer4_fc.pt` is incomplete without the official pretrained backbone.
- For inference, `torch.load` of the current trusted project checkpoint must match its saved keys and label mapping.

**Never fallback to `weights=None`** or silently initialize the backbone randomly; that would create a different unvalidated system. Never silently substitute another pretrained model (X3D, SlowFast, transformer, YOLO, etc.) and keep the same metric labels.

### Inference recipe invariants

Reference the **committed JSON**, not prose:

```text
frames_per_clip = 16
annotation fps index -> seconds = /30
inner_interval_fraction = 0.78
train temporal positions = [0.25, 0.75]
evaluation temporal position = 0.5
resize short edge = 128
ROI = ensemble (center + motion crop)
normalization = R3D_18_Weights.DEFAULT.transforms()
expected transformed tensor = [3,16,112,112]
```

For ROI ensemble, **average logits, then softmax**. Do not average softmax probabilities unless a new experiment is run and recorded. Motion crop derives from RGB grayframe inter-frame differences; it is a heuristic, **not** foreground segmentation or object tracking.

### Local video analysis distinct from notebook evaluation

- Experiment uses pre-annotated action interval boundaries.
- Local demo uses **3.0s window / 2.0s stride**, final tail aligned to video end if necessary.
- Model inference currently supports roughly **0.6 to 120 seconds of video**, while upload metadata checks allow up to **30 minutes**. Explicitly disclose this inconsistency until fixed.
- `uncertain` is generated using top-1 softmax `<0.65`, an **uncalibrated engineering display heuristic**.
- `activity_predictions` are not event segmentation, step-completion events or compliance verdicts.
- Always keep `sop_status = 'not_evaluated'` until a **separate, genuinely validated SOP rule/violation subsystem** exists.

## 7. Claim and publication policy

### Permitted wording

- “Experimental six-class Assembly101 action recognition.”
- “Validation accuracy 52.94%; reused exploratory test accuracy 18.75%, non-blind.”
- “A local FastAPI + React demo can run genuine V6 checkpoint inference on a short test video.”
- “Future foundation for a visually assisted SOP review process.”
- “Experimental predictions require human verification.”

### Prohibited wording absent independent new evidence

- “Detects SOP violations,” “factory-ready AI SOP auditor,” “certifies compliance.”
- “80% accuracy achieved,” “robust industry-grade activity recognition.”
- “The historically exposed test set is blind / unbiased.”
- “96% confidence means a 96% probability of correctness.”
- “Video analysis is real-time,” “safe for worker monitoring,” “production secure.”
- “Dataset has 680 independent training sessions” (it has 680 annotation **files** in the examined inventory, not usable session pairs).

If user requests a polished UI demo, use conspicuous **Experimental** and **SOP not evaluated** wording. Do not disguise missing model outputs as confident predictions. When model fails, present the actual error and continue only with valid motion data.

## 8. Frontend/backend API contract

Current development topology:

```text
Frontend: http://localhost:5173    React 19 + Vite 6 + TypeScript
Backend:  http://127.0.0.1:8001    FastAPI 0.1.0
Proxy:    frontend/vite.config.ts  /api -> http://127.0.0.1:8001
```

### Existing endpoints

| Path | Method | Meaning |
|---|---|---|
| `/api/health` | GET | Server status + file presence + model loaded flag. |
| `/api/analyze` | POST multipart `file` | Video metadata, motion and optional V6 predictions. |
| `/api/analyses/{job_id}` | GET | Saved analysis JSON. |
| `/api/analyses/{job_id}/preview` | GET | Saved preview JPEG. |

Current response keys: `id`, `filename`, `duration_s`, `fps`, `width`, `height`, `frames`, `motion`, `model_status`, `activity_predictions`, `ai_error`, `sop_status`, `warning`.

Acceptable `model_status`: `experimental_v6`, `checkpoint_missing`, `inference_failed`. `model_inference_enabled=True` means the two local files exist, **not** that the model has loaded, the checkpoint is compatible, or a prediction has succeeded. `model_loaded` is lazy and may be `False` before the first upload.

### Preserve contract when editing

- Do not silently rename endpoints, key names or ports.
- Do not break stable behavior: valid short videos still return metadata/motion; model failure is explicit.
- No fabricated placeholder predictions, random probabilities or default green compliance state.
- Filename must be treated as untrusted input and upload extension/size/metadata verified.
- Keep experimental note in UI and response. Frontend should handle empty prediction list and `ai_error` safely.
- Avoid making the UI report a *passed SOP* when only activity model returns softmax.

## 9. Development environment and commands

Use **Windows PowerShell** examples by default, because the current local development setup uses Windows. Do not assume Bash-specific shell syntax in user-facing commands.

### Backend first-time setup

```powershell
cd 'D:\porto\100 day\day 30\VisualSOP Checker'
python -m venv .\backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
Test-Path .\models\best_finetuned_layer4_fc.pt
Test-Path .\models\inference_recipe.json
```

### Backend (terminal A)

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```

### Frontend (terminal B)

```powershell
cd 'D:\porto\100 day\day 30\VisualSOP Checker\frontend'
npm ci
npm run dev
```

### Smoke checks (terminal C)

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/health
Invoke-RestMethod http://localhost:5173/api/health
```

### Video upload from Windows PowerShell 5.1

The Windows PowerShell 5.1 `Invoke-RestMethod` version **does not support `-Form`**. Use `curl.exe` (not the `curl` alias):

```powershell
$video = (Resolve-Path '.\assets\examples\assembly101_test_20s.mp4').Path
$response = curl.exe -sS -X POST 'http://127.0.0.1:8001/api/analyze' -F "file=@$video"
$result = $response | ConvertFrom-Json
$result | Select-Object model_status, sop_status, ai_error
$result.activity_predictions | Select-Object start_s,end_s,label,confidence,uncertain
```

The example video is a **local ignored file**, not downloadable from this repository. If it doesn't exist, provide a different, legitimately obtained video path.

## 10. Testing policy / definition of evidence

Tests are not “passed” unless executed and verified. A run of `python -m compileall` validates syntax/import bytecode, **not** correctness or accuracy. A successful frontend build validates compilation/bundling, **not** model quality. An HTTP 200 `GET /api/health` proves API responsiveness, **not** a loaded model.

### Minimum smoke checks for backend changes

```powershell
.\backend\.venv\Scripts\python.exe -m compileall .\backend\app
.\backend\.venv\Scripts\python.exe -c "from backend.app.v6_inference import ROOT,readiness; print(ROOT,readiness())"
Invoke-RestMethod http://127.0.0.1:8001/api/health
```

Before claiming inference integration works, upload a legitimate short video and assert all of:

```text
model_status == experimental_v6
len(activity_predictions) > 0
ai_error is null
sop_status == not_evaluated
```

Also deliberately verify missing-checkpoint and invalid-upload paths, and no regressions in the UI.

### Minimum smoke checks for frontend changes

```powershell
cd .\frontend
npm run build
```

Check UI at `http://localhost:5173` and verify disconnected-backend, loading, predicted, failed and empty states. Do not claim E2E testing solely from a Vite startup banner.

### Required future automated test coverage

- Reproducible group-disjoint manifest and leakage assertions.
- Unit checks for class ID order, 30-fps annotation conversions, 16-frame sampling, shapes and ROI averaging.
- Mock or small fixture tests for API response schemas, invalid uploads, large files, missing model and failure mode.
- Checkpoint/recipe/pretrained revision compatibility checks with known source hashes.
- Inference parity against recorded notebook clip predictions (after confirming matching segments).
- Independent holdout evaluation with per-class metrics and uncertainty calibration.
- Data retention/security/auth checks before any shared deployment.

No CI / test suite should be described as existing unless its files and actual run evidence have been inspected.

## 11. Reproducible research protocol for new model versions

1. **Environment:** record Python, torch, torchvision, OpenCV, CUDA/device, seed, notebook/runtime and official base-weights identity. Save a machine-readable manifest.
2. **Data inventory:** document original URLs, gating/license, download timestamps, file hashes, annotations, metadata and pairing failures.
3. **Audit:** validate readable videos, timebase conversions, label intervals, contradictory labels, missing files, duplicate/near-duplicate clips and subgroup counts.
4. **Split:** assign by source groups/sessions; ensure original source doesn't appear across splits; lock a fresh **untouched** blind holdout *before* experimentation.
5. **Baseline:** run a simple fully evaluated baseline before more complex variants; log seed, preprocessing, optimizer, epochs, augmentation and training curves.
6. **Model selection:** validation **only** for checkpoints/hyperparameters/ROI; preserve a stable immutable experiment ID.
7. **Evaluation:** use independent intervals, class supports, per-class precision/recall/F1, macro F1, balanced accuracy, confusion and group-wise slices.
8. **Human-visible failures:** include sample frames and model output with rights-safe illustrations; avoid uploading source gated video.
9. **Export:** checkpoint, inference recipe, model card, environment, prediction table, checksums; verify inference implementation matches notebook.
10. **Reporting:** make validation, historical exploratory test, and untouched blind test distinct. Explicitly state if a holdout was inspected, invalidated, or unavailable.
11. **Release gate:** training executed, reproducibility artifacts saved, license checked, claim boundaries reviewed, and documentation synchronized.

**Do not manufacture metrics to meet a target.** If a requested 80% target fails, report failure and proceed to data/model analysis.

## 12. Data, secret, and artifact hygiene

### Must remain excluded from Git

```gitignore
.env
.env.*
!.env.example
*.key
*.pem
.venv/
venv/
node_modules/
frontend/node_modules/
backend/storage/
*.mp4
*.avi
*.mov
*.mkv
*.7z
*.rar
*.zip
*.pt
*.pth
*.ckpt
*.onnx
*.h5
*.hdf5
*.safetensors
*.joblib
*.pkl
*.npy
*.npz
runs/
wandb/
mlruns/
dist/
build/
```

**Keep Git-tracked** model cards, JSON metadata, CSV audits, rights-safe figures, notebooks, code, docs, `package-lock.json`, and `.env.example` (with fake/non-secret defaults only).

`gitignore` does not retroactively untrack already tracked files. When cleaning a mistakenly staged local dependency directory, use `git rm -r --cached --ignore-unmatch frontend/node_modules` and `git status`—never physically delete the directory unless requested. Inspect `git status --short` before any commit. Do not blindly `git add .` when media/secrets are at risk.

**Do not commit or redistribute** original Assembly101 videos or gated data. Do not copy them to open demo hosting. Respect the code license and distinct upstream dataset/pretrained-weight licenses.

## 13. Security, privacy, and deployment boundaries

Current FastAPI API is a **local-only demo** and is **not** hardened for internet-facing untrusted input. The current endpoint stores uploaded videos, preview JPEGs and `result.json` in `backend/storage/<job-id>/` without an evidenced cleanup schedule. Do not promise encryption, deletion, authentication or access control unless implemented and verified.

Risk review before remote deployment:

- Current checkpoint load uses `torch.load(..., weights_only=False)`; **untrusted PyTorch checkpoint deserialization can execute code**. Only trusted weights; consider safe formats or constrained `weights_only` migration with parity validation.
- Video decoders parse untrusted inputs; isolate FFmpeg/OpenCV decoders, validate content and enforce CPU/GPU/memory/request/time limits.
- The simple upload API has size default **150 MB** and metadata max **30 min**, but AI inference max **120 s**. Fix inconsistency before exposing users to it.
- Job IDs should not serve as the sole authorization mechanism. Add real auth and ownership checks to reads/previews before public hosting.
- Retention/deletion, consent/worker privacy, redacted logs, rate limiting, queue isolation and observability are not presently established.
- No autonomous personnel compliance decisions; human reviewer, escalation route and auditable corrections required before future SOP features.

### Deployment readiness gate (not yet passed)

Demand license/privacy review, locked dependencies and model digests, audited upload processing, access control, rate limits, data deletion, queue/backpressure, monitoring, independent blind benchmark, in-domain validation, threat model and incident response. Local “works on my machine” is not proof of readiness.

## 14. Roadmap discipline

Treat these as **planned/unverified**:

**P0 — Integrity:** README/AGENTS synchronization, reproducibility, audit, unchanged root layout, no leaked data/secrets, bug-free port 8001 integration.

**P0 — Honest evaluation:** expand paired independent sessions, freeze previously unseen group-based holdout, audit source/camera/label balance.

**P1 — Model science:** compare baselines, improve object-centric representation and action timing, perform calibration/OOD rejection, report group-level failures and compute.

**P1 — Workflow specification:** define actual SOP process graph and time/order constraints with expert input.

**P2 — Real violations:** collect rights-compliant, expert-labeled positive/negative SOP violation examples and evaluate a dedicated classifier/rule engine independently.

**P2 — User experience:** step review and corrections, uncertainty-aware evidence, report export, safe human oversight.

**P3 — Production concerns:** inference job queue, authentication, privacy/storage retention, packaging, deployment, observability, security and domain trial.

Do not implement random roadmap features simply to appear complete. Every feature must have problem statement, data prerequisites, acceptance criteria, evidence and an honest status.

## 15. Troubleshooting contract

| Symptom | Required first check | Correct action |
|---|---|---|
| Vite proxy refuses `127.0.0.1:8000` | `frontend/vite.config.ts` | Set `/api` target to **8001**, restart Vite. |
| Uvicorn `[Errno 10048]` | Existing port owner / duplicate server | Stop old process; do not spawn a competing API. |
| Health says checkpoint/recipe false despite local files | `ROOT` constant and absolute paths | Both `backend/app/main.py` and `backend/app/v6_inference.py` must use `Path(__file__).resolve().parents[2]`; restart server. |
| Health says model loaded false | Whether inference ever ran | Normal until lazy load succeeds. |
| AI enabled true but results missing | `model_status`, `ai_error` in actual POST response | Diagnose missing pretrained weights, torch compatibility, checkpoint/recipe or decode. |
| Checkpoint only has layer4 and fc | Pretrained base/model selection | Use official `R3D_18_Weights.DEFAULT`; do not use random weights. |
| PowerShell `-Form` unsupported | Windows PowerShell 5.1 | Use `curl.exe -F`. |
| UI shows old motion-only result | Results persist, UI state / server restart | Refresh and **re-analyze**, don't assume historical results update. |
| Git warns about hundreds of `node_modules` files | Ignore rules / staged files | Keep `node_modules/` ignored, remove from index only, inspect status. |
| AI refuses a video >120s | `classify_video` guard | Inform user and use short test clips; don't advertise long-video AI yet. |

Never “fix” an ML runtime failure by replacing model outputs with random/default labels. Never mark `SOP PASS` as the no-error state.

## 16. Agent changeset checklist

Before starting:

- [ ] Read user request and **actual** repo files; identify local vs GitHub state and whether the task authorizes a push.
- [ ] Confirm affected file paths and preserve root folder contract.
- [ ] Identify how change affects dataset provenance, inference recipe, API, ML claims and stored data.
- [ ] Distinguish current code from future roadmap and avoid feature fabrication.

During change:

- [ ] Keep changes targeted and preserve existing working ports (8001/5173).
- [ ] Maintain source-of-truth labels, shapes, temporal/ROI preprocessing and weights provenance.
- [ ] Do not expose secret/media/model weight artifacts.
- [ ] Add useful tests and transparent error handling when behavior changes.
- [ ] Update relevant documentation with **verified** results only.

Before completion:

- [ ] Execute available build/smoke tests and report **what actually ran**.
- [ ] Recheck no unintended `node_modules`, `.pt`, `.env`, datasets or uploaded videos are staged.
- [ ] Ensure `sop_status: not_evaluated` remains honest until there is SOP ground truth.
- [ ] Confirm README and AGENTS reflect new behavior/metrics/limitations.
- [ ] Provide exact commands, meaningful commit message and concise remaining risks.
- [ ] Do not claim code has been pushed, deployed or tested unless that action actually succeeded.

## 17. Expected completion report format

For any material change, report:

```text
Objective:
Files changed:
What was implemented:
Dataset/model/provenance implications:
Tests run (exact commands + outcomes):
Tests not run / blockers:
Known limitations and claim boundaries:
Suggested git commit message:
```

If reporting a new model run, also include: experiment ID, source revisions, independent split counts, class mapping, best epoch, validation-selected strategy, non-blind exploratory results, untouched blind results (or **not available**), per-class evidence, artifact manifest/checksums, inference-parity checks and licensing considerations.

## 18. License and attribution

- Project repository's `LICENSE` is MIT for the code authored here; preserve its copyright notice and conditions.
- Assembly101 has separate gated terms and CC BY-NC 4.0 conditions: https://assembly101.github.io/ and https://huggingface.co/datasets/cvml-nus/assembly101.
- Pretrained R3D-18/torchvision and Kinetics-400 dependencies have their own rights/attribution requirements. Audit before redistribution/commercial usage.
- Data subjects and video owners have independent privacy/consent interests, regardless of open-source code licensing.

**Final principle:** Protect scientific provenance and user trust. **Do not make this project look better by hiding its weaknesses; make it better by collecting evidence, implementing real behavior, and measuring it correctly.**

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# AGENTS.md — Kontrak Penelitian dan Pengembangan VisualSOP Checker

**Berlaku untuk:** seluruh repository, developer, coding agent, eksperimen ML, dokumentasi, tes dan otomasi. **Status:** prototipe penelitian; tidak tervalidasi sebagai pendeteksi pelanggaran SOP.

## A. Aturan mutlak

1. **Jangan mengarang hasil.** Metrik, dataset, label, training, endpoint, screenshot, hasil test, keberhasilan deployment dan kemampuan AI harus memiliki bukti aktual.
2. **Jangan mengklaim pelanggaran SOP sudah terdeteksi.** Model mengklasifikasikan enam aktivitas perakitan mainan; `sop_status` masih `not_evaluated`.
3. **Jangan mengubah struktur repository secara sepihak.** Pertahankan `README.md`, `AGENTS.md`, `LICENSE`, `.gitignore`, `.env.example`, `notebooks/`, `models/`, `reports/`, `assets/{plots,examples,screenshots,diagrams}/`, `backend/`, `frontend/`, `docs/`, `scripts/`. Jangan buat folder `datasets/` di root. Folder kosong gunakan `.gitkeep`.
4. **Jangan commit data mentah, video terbatas, bobot besar, `node_modules`, `.venv`, token, atau cache.** Jangan melewati `.gitignore` tanpa alasan dan izin.
5. **Jangan pakai test historis untuk tuning.** Test lama pernah dilihat dan tidak blind.
6. **English dan Bahasa Indonesia wajib sinkron** untuk semua `.md` yang diubah; tidak boleh hanya satu bahasa atau dua versi yang bertentangan.
7. **Perubahan besar membutuhkan bukti tes.** Pisahkan yang benar-benar dieksekusi dari rencana atau tes yang disarankan.

## B. Source-of-truth

- `models/MODEL_CARD.json` — angka metrik dan batas model.
- `models/inference_recipe.json` — input, urutan kelas, preprocessing dan ROI.
- `notebooks/visualsop-checker.ipynb` — sumber eksperimen penelitian; output harus eksekusi asli.
- `reports/v6/` — CSV audit, histori, hasil dan confusion matrix.
- `backend/app/main.py`, `backend/app/v6_inference.py` — perilaku API/inferensi yang benar-benar dikodekan.
- `frontend/src/main.tsx`, `frontend/vite.config.ts` — UI serta proxy aktual.
- `docs/dataset_provenance.md` dan metadata — ketentuan dataset, asal data dan pembatasan.

Jika terdapat konflik, periksa artefak eksekusi/commit dan nyatakan konflik secara jelas. Jangan membuat “kebenaran” baru hanya dengan mengedit narasi.

## C. Fakta model yang tidak boleh diubah tanpa eksperimen baru

- Tugas: enam kelas (`attach cabin`, `attach wheel`, `detach cabin`, `detach wheel`, `screw chassis`, `unscrew chassis`).
- Dataset: Assembly101 toy assembly, bukan ground truth pelanggaran SOP industri.
- Split: 62 interval train independen, 17 validation, 16 reused exploratory test; train 124 tampilan klip berkorelasi.
- V6 best epoch 10; ROI validation-selected `ensemble`.
- Accuracy validation 52,94%, macro-F1 51,11%; exploratory test accuracy 18,75%, macro-F1 11,11%.
- Test historis tidak blind, tidak boleh dipromosikan sebagai benchmark independen.
- Checkpoint hanya `layer4` dan `fc`; **harus** membangun R3D-18 dengan pretrained Kinetics-400 yang sesuai. Jangan fallback random weights.
- Inference: 16 RGB frame, inner span 78%, resize short edge 128, center/motion ROI, pretrained transform; jendela UI 3 detik stride 2 detik hanyalah heuristik.
- Hasil `softmax` belum dikalibrasi; angka confidence tidak menjamin prediksi benar.

## D. Workflow aman bagi agent

1. Periksa `git status`, branch, dan file yang relevan sebelum mengubah apa pun.
2. Baca aturan ini, README, recipe/model card, dan implementasi yang terdampak.
3. Tentukan scope file minimal; jangan rename/refactor tanpa kebutuhan.
4. Jangan menyentuh dataset atau melatih ulang tanpa diminta dan tanpa provenance.
5. Ubah kode beserta tes relevan, penanganan error, dan dokumentasi dua bahasa.
6. Jalankan tes yang mungkin dijalankan; rekam perintah dan output. Jangan mengaku lulus kalau tes belum dijalankan.
7. Audit `git diff` dan `git status`, cegah file yang seharusnya di-ignore masuk commit.
8. Ringkas Before–Now–Next, perubahan, risiko, tes dan commit message.

## E. Backend dan frontend

Backend FastAPI pada `127.0.0.1:8001`, Vite pada `localhost:5173`, proxy `/api` menuju `127.0.0.1:8001`. Jangan kembali mengubah target menjadi 8000 tanpa keputusan eksplisit. Jangan memulai backend ganda; `Errno 10048` menandakan port sudah terpakai.

Endpoint yang ada: `GET /api/health`, `POST /api/analyze`, `GET /api/analyses/{job_id}`, `GET /api/analyses/{job_id}/preview`. Unggahan ke `backend/storage/` harus tetap di-ignore. Pertahankan sanitasi nama file, batas ukuran/durasi, perilaku fallback error (bukan prediksi palsu), dan pemisahan motion terhadap AI.

Sinyal readiness `model_inference_enabled=true` hanya berarti file checkpoint dan recipe terdeteksi. Model belum tentu berhasil dimuat hingga `POST /api/analyze`. Perubahan UI harus membedakan success, failure, uncertainty, dan `SOP not evaluated`.

## F. Standar dataset dan evaluasi

- Dokumentasikan URL asli, lisensi, pembatasan, versi, tanggal akses bila diketahui, sumber yang benar-benar dipakai, dan keterbatasan. Jangan mengisi tanggal/versi fiktif.
- Pertahankan provenance 13 sesi video yang dipasangkan, 680 file anotasi coarse, basis waktu anotasi 30 FPS dan sumber sekitar 60 FPS.
- Lakukan audit duplikasi, overlap, label ambiguity, distribusi kelas, sesi video, anotasi yang tidak punya pasangan dan kebocoran train/test.
- Pilih model hanya dengan validasi; test baru harus tetap tersegel sampai model dibekukan.
- Laporan minimum: accuracy, macro-F1, balanced accuracy bila relevan, precision/recall per kelas, confusion matrix, contoh salah, batasan, sampel dan split.
- Jangan menuliskan 80% target sebagai hasil. Jangan memakai label “SOP compliant / violated” tanpa data anotasi ahli dan evaluasi sah.

## G. Reproduksi dan keamanan

Catat versi dependency, seed, sumber/checksum dataset yang boleh dibagikan, file eksperimen, split, pipeline transform, recipe, bobot awal, run IDs, output metrics dan keterbatasan. Jangan mengekspor log palsu atau screenshot buatan sebagai bukti training. Lindungi data dan privasi; jangan publikasikan API unggahan tanpa autentikasi, rate limits, quota, retensi dan pemeriksaan file. Kode berlisensi MIT; data Assembly101 mengikuti ketentuan berbeda, termasuk CC BY-NC 4.0/gated terms yang perlu ditinjau.

## H. Definition of Done

Pekerjaan dapat disebut selesai apabila kode cocok dengan tujuan, tes relevan dijalankan atau keterbatasannya dijelaskan, dokumentasi EN+ID diperbarui, kontrak kelas dan recipe dipertahankan, tidak ada file terlarang dalam staging, dan batas klaim tetap akurat. Jika pengguna meminta file lengkap, jangan kirim fragmen yang mengabaikan struktur yang sudah ada.

## I. Troubleshooting singkat

- `checkpoint missing`: periksa `Path(__file__).resolve().parents[2]` pada `backend/app/v6_inference.py` dan keberadaan `models/`.
- `ECONNREFUSED :8000`: cek proxy, target 8001.
- `Errno 10048`: hentikan proses lama di port 8001.
- `model_loaded=false`: normal sebelum inferensi, lalu cek `ai_error` bila gagal.
- `-Form` tidak tersedia: gunakan `curl.exe -F` di PowerShell.
- `torchvision weights unavailable`: perlu pretrained resmi di cache; jangan pakai bobot acak.
- `LF/CRLF` saat `git add`: warning bukan alasan commit `node_modules`; pastikan `.gitignore` dan git index bersih.

## J. Tugas berikutnya

P0: stabilkan demo lokal dan tes API; P0: audit prediksi vs ground truth; P1: tambah sesi independen serta blind test baru; P1: ablation, class imbalance dan calibration; P2: temporal segmentation dan SOP definitions; P3: keamanan deployment, monitoring dan validasi industri. Selalu tandai roadmap sebagai **belum dikerjakan** hingga ada bukti nyata.
