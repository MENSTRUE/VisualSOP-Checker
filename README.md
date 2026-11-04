> **Languages / Bahasa:** [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)  
> **Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
> **Evidence rule / Aturan bukti:** Claims follow executed artifacts; roadmap items are not completed features.

---

<a id="english"></a>

# English

# VisualSOP Checker

**Day 30 / 100 Days of Projects · Manufacturing · Video Understanding · Research Prototype**

> **Project status (2026-11-04):** A functioning local React + FastAPI demonstration performs **real, experimental six-class activity recognition** using the V6 fine-tuned R3D-18 checkpoint, if the local weights and inference recipe are available. The application **does not determine SOP compliance or detect SOP violations**. Published classification performance remains weak, particularly on the historically exposed exploratory test set. Do not use its predictions for production, safety, disciplinary, or personnel decisions.

**Repository:** https://github.com/MENSTRUE/VisualSOP-Checker  
**Primary evidence:** [`models/MODEL_CARD.json`](models/MODEL_CARD.json), [`models/inference_recipe.json`](models/inference_recipe.json), [`reports/v6/`](reports/v6/), [`notebooks/visualsop-checker.ipynb`](notebooks/visualsop-checker.ipynb)  
**Implementation:** [`backend/app/main.py`](backend/app/main.py), [`backend/app/v6_inference.py`](backend/app/v6_inference.py), [`frontend/src/main.tsx`](frontend/src/main.tsx)  
**Project code license:** [MIT](LICENSE). **Assembly101 recordings/annotations:** separate upstream terms, including gated access and CC BY-NC 4.0 conditions; see [Data rights](#data-rights-attribution-and-licenses).

---

## Contents

1. [Executive summary](#executive-summary)
2. [Problem, objective, and scope](#problem-objective-and-scope)
3. [Before → Now → Next](#before--now--next)
4. [Feature and evidence status](#feature-and-evidence-status)
5. [Architecture and data flow](#architecture-and-data-flow)
6. [Dataset and provenance](#dataset-and-provenance)
7. [Labels, splits, and leakage controls](#labels-splits-and-leakage-controls)
8. [Model V6 and inference recipe](#model-v6-and-inference-recipe)
9. [Experimental results and audit](#experimental-results-and-audit)
10. [Local quick start](#local-quick-start-windows-powershell)
11. [API reference and demonstration](#api-reference-and-demonstration)
12. [Testing and acceptance criteria](#testing-and-acceptance-criteria)
13. [Reproducibility](#reproducibility)
14. [Repository structure](#repository-structure)
15. [Claim boundaries](#claim-boundaries)
16. [Limitations and risks](#limitations-and-risks)
17. [Roadmap](#roadmap)
18. [Deployment and security](#deployment-and-security)
19. [Troubleshooting](#troubleshooting)
20. [FAQ](#faq)
21. [Data rights, attribution, and licenses](#data-rights-attribution-and-licenses)
22. [Source-of-truth and maintenance](#source-of-truth-and-maintenance)

## Executive summary

VisualSOP Checker explores whether recorded toy assembly and disassembly videos can be automatically mapped to coarse activity categories, as an **early research component** of a future visual standard operating procedure (SOP) checking system. A pretrained video model, **torchvision R3D-18 (Kinetics-400)**, is adapted to six Assembly101 classes by fine-tuning its final residual block (`layer4`) and classification head (`fc`).

The current local application lets a user upload a video, see metadata, frame-difference motion samples, a preview image, and—**only when the original V6 checkpoint and recipe are present**—timestamped classification predictions. A successful demonstration has returned `model_status: experimental_v6`, ten overlapping-window predictions for a 20-second sample video, and `ai_error: null`. The model heavily preferred `detach cabin` in that specific demonstration; **no ground-truth correctness for that video has been established**.

The task is **activity recognition**, not SOP verification. The word “SOP” in the project name expresses an intended future use case, not a deployed detection capability.

## Problem, objective, and scope

### Problem

Reviewing visual manufacturing/assembly recordings can demand human time. A research assistant that extracts coarse action hypotheses from clips could help prioritize manual inspection. However, inferring compliance requires much more than a predicted action label: authorized process definitions, expected action sequence, temporal boundaries, object state, context, and validated violation labels are all required.

### Current research question

> Can a pretrained spatiotemporal network distinguish six coarse assembly/disassembly actions in a restricted Assembly101 subset, and can those experimental outputs be surfaced transparently in a local web interface?

### Intended users and non-users

- **Intended current user:** developer/researcher assessing video classification experiments and failure cases.
- **Potential future user:** manufacturing quality/SOP reviewer **only after** domain data collection, independent validation, calibrated uncertainty, human review workflow, and safety/privacy assessments.
- **Not intended now:** operational compliance enforcement, employee scoring, safety interlocks, automatic fault attribution, or real-world defect certification.

### In scope today

Six-way clip-level recognition; validation-selected R3D-18 V6; local video upload and API; heuristic windowing; visual inspection of predictions; reporting and audit artifacts; limitations and provenance.

### Out of scope today

Verified step/order checking, missing-step detection, actions outside the six classes, real-time surveillance, operator identity tracking, detection of industrial SOP violations, factory-ready precision/recall or SLA guarantees, and reliable performance on arbitrary user videos.

## Before → Now → Next

| Stage | Reality | Evidence or required action |
|---|---|---|
| **Before** | Dataset ingestion, annotation/video matching, group-disjoint research splits, R3D-18 experiments; README described `backend/` and `frontend/` as future work. | Notebook, V6 reports, data audit files. |
| **Now** | Local React/Vite interface and FastAPI API exist. A real V6 inference path reads the recipe and fine-tuned checkpoint; video can produce 3-second sliding-window predictions at 2-second stride. | `backend/app/`, `frontend/`, local API test (2026-11-04). |
| **Now — performance** | V6 achieves **52.94% validation accuracy** and **18.75% on reused exploratory test**, **not** 80% and **not** blind evaluation. | `models/MODEL_CARD.json`, `reports/v6/reports/`. |
| **Next — research** | Improve paired data coverage, audit label and group balance, recruit new independent source sessions, and freeze untouched holdout data **before** further tuning. | New versioned dataset manifest/protocol required. |
| **Next — product** | Define actual SOPs and violation labels; build boundary detection/state tracking, calibrated rejection, human review and explanation interfaces. | Requires a **separate** annotated SOP compliance benchmark. |
| **Later — deployment** | Security/privacy, monitoring, latency/load tests, rights review, domain performance studies and release gates. | **Not yet completed.** |

## Feature and evidence status

| Capability | Status | Truth boundary |
|---|---|---|
| User-uploaded local video and metadata | Implemented | API supports selected video containers, validates metadata and size. |
| Sparse frame-difference motion timeline | Implemented | Motion is **not** an AI action label and **not** a violation signal. |
| Preview frame | Implemented | `GET /api/analyses/{id}/preview` reads locally stored frame. |
| R3D-18 V6 six-class predictions | Implemented, experimental | Requires local checkpoint **and** original pretrained base weights. |
| Per-window top-3 and uncertainty indicator | Implemented | Softmax values **uncalibrated**; `uncertain` uses `<0.65` heuristic. |
| Long-video / real-time classifier | Limited | V6 AI classifies videos **up to 120 seconds**; uploads may accept longer video but AI can fail. |
| Learned action boundary segmentation | Not implemented | 3s/2s windows are heuristics, not predicted event boundaries. |
| SOP rule engine, deviations, compliance score | **Not implemented** | `sop_status: not_evaluated` even when action inference succeeds. |
| Blind independent benchmark | **Not available** | Historical exploratory test has been exposed/reused. |
| Calibrated confidence / deployment safety | **Not validated** | No production threshold should be inferred from top-1 confidence. |

## Architecture and data flow

```text
Browser (React 19, TypeScript, Vite :5173)
     │ POST /api/analyze (multipart video)
     ▼
Vite dev proxy /api → 127.0.0.1:8001
     │
     ▼
FastAPI 0.1.0 (backend/app/main.py)
     ├── Extension / size / decoder / metadata checks
     ├── Local storage: backend/storage/<job-id>/
     │    ├── source.<video-extension>
     │    ├── preview.jpg
     │    └── result.json
     ├── Sparse optical frame-difference timeline (not ML)
     └── V6 inference when checkpoint + recipe exist
          ├── load Kinetics-400 pretrained R3D-18
          ├── replace head with 6 classes
          ├── load fine-tuned layer4 + fc
          ├── 3.0 s windows; 2.0 s stride; final tail window
          ├── 16 decoded RGB frames / window
          ├── center crop + motion ROI; ensemble logits
          └── label, uncalibrated softmax, top3, uncertain
     ▼
JSON: motion + activity_predictions + model_status + sop_status
     ▼
Web UI: review hypotheses and limitations; NOT SOP verdict
```

**Important differentiation:** experiment training/evaluation uses **annotated action intervals**; the interactive API instead applies **new fixed sliding windows** to arbitrary uploaded clips. There is no proof that results on those two protocols are equivalent.

## Dataset and provenance

### Primary source

- **Name:** [Assembly101](https://assembly101.github.io/)
- **Dataset location:** https://huggingface.co/datasets/cvml-nus/assembly101
- **Domain:** multi-view toy-assembly activities—not industrial shop-floor SOP violations.
- **Used media:** RGB video recordings and coarse annotation interval files.
- **Access and rights:** source may be gated. Respect access terms and CC BY-NC 4.0 restrictions. See [Data rights](#data-rights-attribution-and-licenses).

### V6 subset evidenced in repository

| Inventory field | Recorded quantity | Interpretation |
|---|---:|---|
| Original RGB recordings | 9 | Earlier source recordings. |
| Additional RGB recordings | 4 | Expanded source subset. |
| Distinct video sessions used | 13 | Only a small portion of available annotation universe is paired. |
| Coarse-label annotation files inspected | 680 | Files are **not** equivalent to 680 usable paired sessions. |
| Independent training intervals | 62 | 124 training clip views derive from these 62 intervals; **not** 124 independent segments. |
| Validation intervals | 17 | Small and reused in model selection. |
| Historical exploratory test intervals | 16 | **Not blind**, because accessed in earlier work. |
| Total analyzed independent intervals | 95 | 62 + 17 + 16, before train-view augmentation. |

The original coarse annotations index time in a nominal **30-fps annotation timebase**, while source RGB recordings are approximately **60 fps**. Convert annotated frame index to seconds with `frame_index / 30`, then use video timestamps for decoding; do not mistake a raw video's 60-fps frame count for annotation indices.

Source groups listed in the research split documentation: **training 9013, 9014, 9015, 9022; validation 9011, 9012; exploratory test 9016, 9021.** These are *toy group* separations and should be independently audited against actual session/video leakage.

The pilot included more annotation files than usable, matched videos. The model card records **13/350 annotated sessions paired with videos**. Do not count unmatched labels as training evidence, or portray raw download volume as effective sample size.

### Data manifests and audit evidence

- [`reports/v6/audit/session_inventory.csv`](reports/v6/audit/session_inventory.csv) — source sessions and matching.
- [`reports/v6/audit/unmatched_annotation_sessions.csv`](reports/v6/audit/unmatched_annotation_sessions.csv) — unavailable/unpaired annotation sessions.
- [`reports/v6/audit/video_metadata.csv`](reports/v6/audit/video_metadata.csv) — decoded video metadata audit.
- [`reports/v6/audit/segments.csv`](reports/v6/audit/segments.csv) — retained labelled intervals and split assignments.
- [`reports/v6/audit/cached_clips.csv`](reports/v6/audit/cached_clips.csv) — clip-cache/ROI bookkeeping.
- [`reports/v6/metadata/dataset_provenance.json`](reports/v6/metadata/dataset_provenance.json) — dataset/provenance manifest.
- [`docs/dataset_provenance.md`](docs/dataset_provenance.md) — origin and licensing context.

**Data access ≠ permission to redistribute.** Source MP4 files, extracted datasets, and model weights are excluded from Git by policy. Keep access-controlled, license-compliant copies in your local research environment.

## Labels, splits, and leakage controls

The exact class order determines output index mapping and is **part of the model contract**:

| Class ID | Label |
|---:|---|
| 0 | `attach cabin` |
| 1 | `attach wheel` |
| 2 | `detach cabin` |
| 3 | `detach wheel` |
| 4 | `screw chassis` |
| 5 | `unscrew chassis` |

The source records a group-disjoint experimental protocol, but the following remain serious risks:

1. Same activity interval represented by multiple highly correlated training views, so independence is **62 intervals**, not 124 clips.
2. Repeated validation-based architecture/ROI choices over a small 17-interval set, risking validation overfit.
3. Previously exposed 16-interval test reused for exploration, so its results are **diagnostic**, not proof of generalization.
4. **14/16 test intervals** are from group `9021`, making the exploratory score sensitive to that distribution.
5. Cross-camera, cross-session and toy-group separation should be rechecked before any stronger claims.

**Future benchmark rule:** keep an entirely new session/group-disjoint blind holdout under access controls, lock preprocessing/configuration before running, report it once after freeze, and never tune from it. If test evidence is inspected for design choices, relabel it as development/exploratory data and create a new holdout.

## Model V6 and inference recipe

### Architecture and optimization scope

- **Base:** `torchvision.models.video.r3d_18(weights=R3D_18_Weights.DEFAULT)` pretrained on Kinetics-400.
- **Transfer learning:** original video stem and earlier blocks retained from pretrained base; fine-tuned `layer4` plus replacement `fc = Linear(512, 6)`.
- **Checkpoint:** `models/best_finetuned_layer4_fc.pt` stores **only fine-tuned layer4 and fc**; it is **not a complete self-contained network**.
- **Model selection:** V6 checkpoint selected at **epoch 10**; selected ROI strategy is `ensemble` using validation evidence.
- **Reference contract:** [`models/inference_recipe.json`](models/inference_recipe.json), [`models/MODEL_CARD.json`](models/MODEL_CARD.json), [`backend/app/v6_inference.py`](backend/app/v6_inference.py).

### Preprocessing contract

1. Select an annotated action interval at evaluation time or a **heuristic window** for the web application.
2. Decode **16** RGB frames sampled uniformly within the interior **78%** of the interval, at evaluation temporal position **0.5**. Training uses positions **0.25 and 0.75**.
3. Resize while preserving aspect ratio, short edge **128 px**.
4. Create a square center crop and a motion-guided square crop; motion guidance uses inter-frame grayscale differences (a heuristic, not a person/object detector).
5. Use `R3D_18_Weights.DEFAULT.transforms()` yielding a tensor shaped `(3, 16, 112, 112)`.
6. For selected ROI `ensemble`, average **logits** of center and motion views, then softmax to obtain six class scores.
7. Present top-1 label, top-3 scores and `uncertain = (top1_probability < 0.65)`; **do not interpret 0.65 as a validated threshold**.

The application uses **3-second windows, 2-second stride**, and an additional final-tail window if necessary; supported AI windowing duration is **0.6–120 seconds** per uploaded video. A 20-second sample returned ten overlapping windows. The app's fixed windows were not the ground-truth action intervals used in the published validation/test numbers.

### Why model initialization matters

**Never use `r3d_18(weights=None)` as a fallback.** The V6 checkpoint lacks the base weights. Loading its `layer4` and `fc` onto a randomly initialized backbone yields predictions from a different, unvalidated model. Obtain the official torchvision pretrained weights once using appropriate connectivity/cache, then load the V6 fine-tuned layers strictly and verify label order and ROI variant.

**Checkpoint safety:** current backend uses `torch.load(..., weights_only=False)`, which can deserialize arbitrary Python objects. Only load a trusted checkpoint you produced/verified. Treat untrusted `.pt` files as potentially executable content. Improving the checkpoint format/loading strategy is a security roadmap item.

## Experimental results and audit

### V6 reported metrics

| Metric | Validation | Reused exploratory test |
|---|---:|---:|
| Independent intervals | 17 | 16 |
| Accuracy | **52.94%** (9/17) | **18.75%** (3/16) |
| Balanced accuracy | 51.39% | 16.67% |
| Macro F1 | **51.11%** | **11.11%** |
| Blind/untouched? | No (used for selection) | **No (historically inspected)** |

**Interpretation:** the validation result does not generalize to the exposed exploratory test distribution. The original **80% performance target was not achieved**; these results do not justify a reliable industrial-action classifier. A softmax score of e.g. 96.77% on a window is not empirical 96.77% model accuracy.

### Evidence register

| Evidence | Repository path | What it establishes |
|---|---|---|
| Final machine-readable experiment summary | `reports/v6/reports/results.json` | Reported run and headline metrics. |
| Per-class test performance | `reports/v6/reports/test_per_class.csv` | Class-specific classification weaknesses. |
| Confusion matrix (CSV) | `reports/v6/reports/test_confusion_matrix.csv` | Class confusion counts. |
| Learning history | `reports/v6/reports/training_history.csv` | Logged epoch metrics. |
| Per-window or per-segment validation predictions | `reports/v6/predictions/validation_predictions.csv` | Validation examples. |
| Reused exploratory test predictions | `reports/v6/predictions/reused_exploratory_test_predictions.csv` | Diagnostic test predictions; not blind. |
| Curves and confusion visual | `reports/v6/plots/` and `assets/plots/` | Visual summaries; not extra test evidence. |
| Data integrity and matching | `reports/v6/audit/` | Inventory, matching and split bookkeeping. |
| Model contract and limitations | `models/MODEL_CARD.json` | Declared task, metrics, limitations and status. |
| Reproducible experiment source | `notebooks/visualsop-checker.ipynb` | Notebook implementation; requires gated source data. |

### Local API smoke-test observation (not benchmark)

On 2026-11-04, a local POST of a **20-second, 60-fps, 1280×720** Assembly101-derived MP4 returned `model_status: experimental_v6`, **10** timed activity hypotheses, and `ai_error: null`. Nine windows predicted `detach cabin`; the last predicted `detach wheel`. This confirms that the **inference path executed**; it does **not** determine whether the predictions match the video truth or establish any new accuracy figure. `sop_status` remained `not_evaluated`.

## Local quick start (Windows PowerShell)

### Prerequisites

- Windows PowerShell, Git, working Python 3 environment, Node.js/npm, and network access **on first pretrained-weight download**.
- Python backend dependencies declared in `backend/requirements.txt` (PyTorch and torchvision versions must be mutually compatible).
- Local **trusted** V6 checkpoint `models/best_finetuned_layer4_fc.pt` plus committed `models/inference_recipe.json`.
- Vite proxy target `127.0.0.1:8001` (see `frontend/vite.config.ts`).
- Source videos must be obtained under Assembly101's actual license and access conditions; they are not stored in GitHub.

### Clone and prepare

```powershell
# Clone to your chosen workspace. Existing local checkout: skip clone.
git clone https://github.com/MENSTRUE/VisualSOP-Checker.git
cd .\VisualSOP-Checker

# Create the virtual environment if not already present.
python -m venv .\backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt

# Verify local model bundle (checkpoint is not in Git).
Test-Path .\models\best_finetuned_layer4_fc.pt
Test-Path .\models\inference_recipe.json

# Install frontend dependencies from lockfile.
cd .\frontend
npm ci
cd ..
```

Both `Test-Path` calls should be `True` for experimental action predictions. If `False`, the app can still produce motion features, but **not V6 activity inference**. Never download anonymous third-party checkpoints and treat them as trustworthy.

### Terminal A — backend

```powershell
# From repository root
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```

### Terminal B — frontend

```powershell
cd .\frontend
npm run dev
# Open http://localhost:5173
```

### Terminal C — health checks

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/health
Invoke-RestMethod http://localhost:5173/api/health
```

Expected with correctly positioned local files:

```text
status                   : ok
model_checkpoint_present : True
inference_recipe_present : True
model_inference_enabled  : True
model_loaded             : False  # normal until first successful model load
```

`model_inference_enabled` is **file-presence readiness only**. A model can still fail at load/inference time due to incompatible torch/torchvision versions, missing pretrained weights, corrupt checkpoint or decode failure. Confirm with an actual upload and check `model_status` and `ai_error`.

### Upload smoke test with Windows PowerShell 5.1

PowerShell 5.1's `Invoke-RestMethod` does **not** provide the `-Form` parameter. Use the real `curl.exe` binary:

```powershell
# Put a legally obtained local test clip at this path first, or change it.
$video = (Resolve-Path '.\assets\examples\assembly101_test_20s.mp4').Path
curl.exe -sS -X POST 'http://127.0.0.1:8001/api/analyze' -F "file=@$video"
```

The `.mp4` clip is intentionally not committed. For machine-readable parsing:

```powershell
$response = curl.exe -sS -X POST 'http://127.0.0.1:8001/api/analyze' -F "file=@$video"
$result = $response | ConvertFrom-Json
$result | Select-Object model_status, sop_status, ai_error
$result.activity_predictions | Select-Object start_s, end_s, label, confidence, uncertain
```

Expected success indicators: `model_status: experimental_v6`, nonempty `activity_predictions`, `ai_error: null`, and **still** `sop_status: not_evaluated`.

## API reference and demonstration

The local prototype exposes these routes (see `backend/app/main.py`):

| Route | Method | Purpose | Important caveat |
|---|---|---|---|
| `/api/health` | GET | Process and V6 model-file readiness | `model_loaded` changes only after successful load. |
| `/api/analyze` | POST multipart `file` | Video upload, sparse motion samples, optional experimental predictions | The request does synchronous work; large videos can be slow. |
| `/api/analyses/{job_id}` | GET | Retrieve locally persisted `result.json` | Results are stored on filesystem, not an external DB. |
| `/api/analyses/{job_id}/preview` | GET | Fetch first sampled preview JPEG | Not the full video; only a still frame. |

**Analysis response contract (fields):**

```json
{
  "id": "<server-generated-hex-job-id>",
  "filename": "example.mp4",
  "duration_s": 20.0,
  "fps": 60.0,
  "width": 1280,
  "height": 720,
  "frames": 1200,
  "motion": [{"time_s": 0.0, "motion": 0.0}],
  "model_status": "experimental_v6",
  "activity_predictions": [
    {
      "start_s": 0.0,
      "end_s": 3.0,
      "label": "detach cabin",
      "confidence": 0.729,
      "top3": [{"label": "detach cabin", "confidence": 0.729}],
      "uncertain": false
    }
  ],
  "ai_error": null,
  "sop_status": "not_evaluated",
  "warning": "<explicit experimental-use caution>"
}
```

The example is an **illustrative abbreviated shape using one previously observed window**; it is not a fabricated new benchmark. Complete `top3` entries normally include three candidate labels. Possible `model_status` values in the current backend include `checkpoint_missing`, `experimental_v6`, and `inference_failed`.

**Upload validation:** supported suffixes `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`; default upload size limit **150 MB** (environment variable `VISUALSOP_MAX_UPLOAD_MB`); metadata allows video duration up to **30 minutes**, whereas the current experimental AI function raises an error above **120 seconds** and below **0.6 seconds**. If AI fails, the returned report may still include motion analysis with `model_status: inference_failed`. Do **not** document this as full long-video AI support.

**Storage:** `VISUALSOP_STORAGE` can override the default backend-local `storage/` location. Files are not automatically purged by the current code. Treat them as sensitive and configure deletion/retention for any shared deployment.

## Testing and acceptance criteria

The following are **test instructions**, not a claim that a CI system has run them. No production-grade automated E2E/CI coverage is established by the inspected repository state.

### Static and startup checks

```powershell
# From root; import/compile alone does not validate model quality.
.\backend\.venv\Scripts\python.exe -m compileall .\backend\app
.\backend\.venv\Scripts\python.exe -c "from backend.app.v6_inference import ROOT,readiness; print(ROOT, readiness())"

cd .\frontend
npm run build
cd ..
```

### Local API checks

- `GET /api/health` returns HTTP 200, `status: ok`.
- Checkpoint and recipe readiness flags reflect actual local files—not a forced `True`.
- File upload with a **real decodable MP4** returns a valid job ID, metadata, a nonempty motion list and a preview endpoint.
- With trusted V6 weights and compatible runtime, `model_status: experimental_v6`, predictions present, `ai_error: null`.
- Without checkpoint, `model_status: checkpoint_missing`, no invented predictions.
- With a load/decoding error, `model_status: inference_failed` and a useful `ai_error`.
- `sop_status` stays `not_evaluated` regardless of action predictions.
- Check malformed upload, unsupported extension (415), empty file (400), unreadable video (422), oversized upload (413), and missing job ID (404).
- Confirm UI displays uncertainty/experimental warnings and handles backend unavailable state gracefully.

### ML-specific tests required before stronger claims

- Assert label names/order and `inference_recipe.json` checksum or version mapping.
- Assert preprocessor tensor shape `(3,16,112,112)` and channel order.
- Verify source-annotation 30-fps timing conversion and no train/eval leakage.
- Recompute metrics from immutable per-segment predictions with fixed class mapping.
- Independently verify per-class support, confusion and error analysis.
- Run a **new**, never-inspected group-disjoint blind set after freezing the protocol.
- Distinguish clip-level, window-level, session-level, and SOP-level metrics.

## Reproducibility

### What is reproducible from the repository

Notebook source, model/experiment metadata, evaluation artifacts, API implementation, preprocessing recipe, and frontend application are versioned. A full end-to-end reproduction of the published trained model **still requires** gated Assembly101 media/annotations, compatible package versions, original run conditions, and the locally retained checkpoint.

### Source-of-truth order for a research claim

1. **Executed experimental outputs:** `reports/v6/reports/results.json`, predictions and audits.
2. **Model metadata:** `models/MODEL_CARD.json`, `models/inference_recipe.json`.
3. **Executable implementation:** `notebooks/visualsop-checker.ipynb` (training), `backend/app/v6_inference.py` (local inference).
4. **Explanatory documents:** `docs/` and this README. If numbers disagree, audit the executed outputs before updating prose.

### Reproduction procedure

1. Obtain the original data from the official source under its access/license conditions and record source URL, version/revision, retrieval date, checksums, and actual usable recordings.
2. Reconstruct annotation-to-video matching; verify 30-fps annotation timebase and 60-fps source-video timestamps; export inventory/audit.
3. Rebuild exact group-disjoint train/validation/development assignments from the V6 notebook/segment manifest. **Do not reinterpret the historical test set as a new blind test.**
4. Record environment package versions, CUDA/CPU state, seeds, model/pretraining revision, train selection strategy, label mapping, temporal sampling and ROI transforms.
5. Execute notebook start-to-end on a controlled environment; save real logs, prediction CSVs, training history, confusion tables, data manifests and model metadata.
6. Compare resulting artifacts against the V6 evidence, document deviations and hardware/non-determinism; do not quietly overwrite the historical V6 report.
7. To reproduce the local demo, make the trusted fine-tuned checkpoint available in `models/`, provision torchvision pretrained R3D-18 weights, verify API readiness and upload a licensed test video.

### Do not overclaim deterministic reproduction

The repository's `backend/requirements.txt` uses version ranges rather than a frozen ML lockfile; torchvision pretrained weights may be downloaded to a user cache; and compute/decoder/kernel differences can affect results. Record a new environment lock and artifact digests for each future formally reproducible run.

## Repository structure

The following reflects the **standard fixed root layout** and key GitHub-visible paths on **2026-11-04**. Local ignored media/checkpoint/storage can exist without being committed.

```text
VisualSOP-Checker/
├── README.md                         # canonical public entry point
├── AGENTS.md                         # development / AI-agent operating contract
├── README_V6_SETUP.md                # supplemental original V6 integration notes
├── LICENSE                           # MIT for this repository's code
├── .gitignore                        # raw video, weights, env, node_modules excluded
├── .env.example                       # non-secret config example
├── notebooks/
│   ├── README.md
│   └── visualsop-checker.ipynb        # experiment notebook
├── models/
│   ├── README.md
│   ├── MODEL_CARD.json
│   ├── inference_recipe.json
│   └── best_finetuned_layer4_fc.pt   # LOCAL ONLY: gitignored, not hosted
├── reports/
│   └── v6/
│       ├── audit/                    # segment/session/metadata/cache inventories
│       ├── examples/
│       ├── metadata/                 # dataset_provenance.json, environment.json
│       ├── plots/                    # learning curves / confusion image
│       ├── predictions/              # validation + reused exploratory test CSVs
│       └── reports/                  # results.json, class metrics, history, confusion
├── assets/
│   ├── diagrams/
│   ├── examples/                    # locally held videos ignored from Git
│   ├── plots/                       # published figure copies
│   └── screenshots/
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py                   # FastAPI upload/motion/API/storage
│   │   └── v6_inference.py           # real experimental R3D-18 inference
│   ├── .venv/                        # LOCAL ONLY
│   └── storage/                      # LOCAL ONLY, uploaded videos and results
├── frontend/
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts                # /api proxy to port 8001
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   └── style.css
│   └── node_modules/                 # LOCAL ONLY
├── docs/
│   ├── dataset_provenance.md
│   ├── methodology.md
│   ├── limitations.md
│   └── model_card.md
└── scripts/
    └── README.md
```

**Repository invariants:** do not rename, flatten, delete, or arbitrarily reorganize root folders. Do not create `datasets/` in the repository. Keep empty planned folders with `.gitkeep` when necessary. Never commit secrets, raw gated media, notebook caches, generated upload storage or large pretrained/fine-tuned weights.

## Claim boundaries

### Statements supported by present evidence

- A six-class **toy assembly activity recognition** model was trained/evaluated on an Assembly101 subset.
- Selected V6 is a Kinetics-400 pretrained R3D-18 with fine-tuned `layer4` + six-way head.
- V6 validation: **52.94% accuracy**, **51.11% macro F1** on 17 intervals.
- Reused exploratory test: **18.75% accuracy**, **11.11% macro F1** on 16 intervals; **not blind**.
- A local API successfully ran real V6 predictions on one 20-second video and returned 10 heuristic windows, with no inference error in that observed test.
- `sop_status: not_evaluated` reflects lack of a SOP checker.

### Statements **not supported** and prohibited in project presentations

- “AI automatically detects SOP violations” or “ensures worker compliance.”
- “Achieved 80% accuracy” or “production ready.”
- “18.75% is an unbiased final holdout result.”
- “Softmax 97% means a 97% chance of real-world correctness.”
- “Works for all industrial sites, camera setups, people or procedures.”
- “Real-time, low latency, privacy-preserving or secure by default.”
- “13 videos represent the complete Assembly101 benchmark.”

**Recommended one-sentence portfolio description:** “Research prototype for six-class Assembly101 action recognition using a fine-tuned R3D-18, with transparent local video-inference UI and reproducible audit artifacts; SOP compliance detection remains future work.”

## Limitations and risks

### Data and evaluation

- Very small independent sample count; incomplete video/annotation pairing; non-uniform group coverage.
- Validation reused in selection; historical test inspected in earlier iterations; domain/group shift evident.
- Toy dataset differs from industrial procedures and viewpoints. Additional cross-site/cross-person evaluation required.
- Unknown out-of-distribution actions cannot be robustly rejected by the current fixed six-class softmax.

### Modeling

- Heuristic optical motion ROI can center on camera movement, irrelevant hands or background motion.
- Fixed 3s inference windows can overlap multiple actual actions or none at all.
- Softmax probabilities uncalibrated and `uncertain` threshold arbitrary; 10 windows of one video are **correlated**, not independent proof.
- Model has no object-state change verification, dependencies/step graph, logical SOP engine or violation annotations.

### Software and operations

- Local prototype uses filesystem storage; no documented retention/cleanup/auth mechanism.
- Model loading depends on official pretrained torchvision weights and compatible runtime.
- API is not hardened for hostile file uploads, concurrent high-volume use, isolation, rate limits, memory pressure or long-running inference.
- Backend's `torch.load(weights_only=False)` requires a trusted checkpoint; untrusted checkpoints create code execution risk.
- No evidence yet of production observability, CI deployment gate, or independently verified throughput.

## Roadmap

The following items are **planned**, not completed. Avoid interpreting priority as a delivery commitment.

| Priority | Stream | Milestone / acceptance gate |
|---|---|---|
| P0 | Documentation integrity | Keep README/AGENTS/results aligned; verify local startup, API, frontend build and ignore rules. |
| P0 | Data audit | Inventory paired sessions, checksums, conflicts, class/group support and annotation timebase with a versioned manifest. |
| P0 | Evaluation reset | Acquire fresh independent group/session blind holdout; lock protocol before model choice. |
| P1 | Baselines | Compare simple video baselines, frozen backbone, stronger temporal sampling/ROI strategies under identical split and compute. |
| P1 | Quality | Per-class confusion, misclassified frames, confidence calibration, OOD/abstention and slice-specific reporting. |
| P1 | Better representation | Evaluate hands/objects/keypoints, object-centric tracking and action-boundary detection. |
| P1 | SOP specification | Document actual process step graph, ordering rules, allowed variants, missing/extra steps, timing constraints and human annotation guide. |
| P2 | Violation dataset | Obtain consented, domain-appropriate **positive and negative** SOP deviation labels, annotated by experts. |
| P2 | SOP engine | Compare validated action/state events against process graph; yield *review-needed* evidence rather than automatic sanctions. |
| P2 | UX | Timeline review, manual correction, evidence export, optional analyst feedback and role separation. |
| P2 | Testing | Add repeatable unit/integration/E2E tests and offline benchmark CI with no gated raw media in logs. |
| P3 | Security/deployment | Auth, quotas, sandboxing, storage retention, instrumentation, queue/worker architecture and explicit human oversight. |
| P3 | Pilot | Controlled prospective domain trial with agreed false-positive/false-negative targets and rejection behavior. |

A useful next criterion is **independent, unseen evaluation with trustworthy class coverage**, not merely a higher score on the current reused exploratory set.

## Deployment and security

**Current deployment category:** local developer demo **only**, binding API to `127.0.0.1:8001`; Vite dev server at `localhost:5173`. The default stack is not an internet-facing production service.

### Deployment prerequisites before exposing to other users

- Define lawful basis/consent, employee privacy, retention and deletion policies for any video.
- Authenticate users, authorize reads by job ownership, and disable open retrieval of arbitrary jobs.
- Check actual MIME/signature, media decode robustness and resource budgets; scan/sandbox upload processing.
- Put model inference behind bounded background jobs/queue with timeouts, cancellation and concurrency limits.
- Pin Python/Node package versions and model artifacts with hashes; use known-good pretrained weights.
- Replace/guard risky deserialization (`torch.load(..., weights_only=False)`), limit trusted origins, set TLS, request limits and appropriate logging redaction.
- Use structured privacy-aware monitoring with explicit model/recipe version tags and failures/latency dashboards.
- Add human-in-the-loop review and reject/uncertainty behavior **before** SOP recommendation use.
- Produce measured accuracy, throughput and reliability reports on representative, newly collected deployment-domain data.

The code is open source, but the **dataset is not licensed by this repository's MIT file**. Verify data and model redistribution rights before distributing a deployed system or weights.

## Troubleshooting

| Symptom | Likely cause | Verification / fix |
|---|---|---|
| `vite http proxy error ECONNREFUSED 127.0.0.1:8000` | Wrong dev proxy target or no backend. | `frontend/vite.config.ts` must proxy `/api` to `http://127.0.0.1:8001`. Restart Vite. |
| `[Errno 10048]` bind failure at 8001 | Another Uvicorn/process already uses port 8001. | Stop old backend with `Ctrl+C`; do not start a second server; inspect listening process if necessary. |
| `model_checkpoint_present: False` despite local file | Incorrect `ROOT` resolved to parent `day 30`. | In **both** `backend/app/main.py` and `backend/app/v6_inference.py`, repo root is `Path(__file__).resolve().parents[2]`. Restart backend. |
| `model_inference_enabled: True`, `model_loaded: False` | Model files exist; lazily loaded on first inference. | Normal before upload. Verify after successful `POST /api/analyze`. |
| `model_status: checkpoint_missing` | Missing local `.pt` or recipe. | Put trusted `.pt` in `models/`; check both files. `.pt` is Git-ignored. |
| `model_status: inference_failed` / `ai_error` | Weights download, torch/torchvision incompatibility, video decode, duration, checkpoint mismatch. | Inspect `ai_error`; do not substitute random backbone or fabricate labels. |
| `Kinetics-400 pretrained weights unavailable` | No cache or blocked initial download. | Allow official torchvision weights download once or provision verified cache under permitted terms. |
| `Checkpoint label mapping differs` | Wrong checkpoint or class ordering. | Restore matching V6 checkpoint/recipe; do not rename classes to silence error. |
| `ROI variants differ` | Checkpoint and recipe from different experiments. | Restore matching artifacts and prove variant from experiment evidence. |
| `No parameter named Form` in PowerShell | Windows PowerShell 5.1. | Use `curl.exe -F "file=@$video"` instead of `Invoke-RestMethod -Form`. |
| Frontend remains motion-only after model enabled | Previous result is persisted; server/UI may be stale. | Restart services, refresh UI, **re-analyze the video**, inspect new `model_status`. |
| Many Git CRLF warnings from `frontend/node_modules` | Dependencies accidentally staged. | Ignore `node_modules/`; untrack with `git rm -r --cached --ignore-unmatch frontend/node_modules`; check `git status` before commit. |
| Browser works but inference slow | CPU R3D-18, dual ROI and repeated frame seeks. | Check device, input duration, concurrent workload; no performance guarantee is published. |
| Upload accepted but AI refuses >120 s | API upload validation and AI max duration differ. | Use short licensed demo clips; roadmap must unify behavior and user-facing error. |

## FAQ

**Q: Is this already a Visual SOP violation detector?**  
No. It is six-class toy assembly **activity** recognition. The current API explicitly sets `sop_status: not_evaluated`.

**Q: What is the difference between motion score and AI predictions?**  
Motion score is a sparse normalized pixel-difference measurement. The V6 model uses spatiotemporal video frames to output class hypotheses. Neither establishes SOP compliance.

**Q: Why is the test accuracy below validation?**  
The small, imbalanced, historically inspected test distribution differs from validation; the result suggests poor generalization. Cause attribution requires further controlled study, not assumptions.

**Q: Does 96% confidence imply 96% correct?**  
No. It is an uncalibrated softmax score on one possibly overlapping video window.

**Q: Why is the checkpoint missing after `git clone`?**  
`*.pt` files are intentionally excluded from the GitHub repo. Bring your own trusted, rights-compliant checkpoint to `models/` and verify the recipe.

**Q: Why must pretrained weights be downloaded?**  
The saved V6 checkpoint only contains fine-tuned `layer4` and `fc`; the remaining R3D-18 parameters are supplied by official pretrained torchvision weights.

**Q: Can I use any assembly video?**  
The API may accept decodable video files, but the model has only been evaluated on a narrow toy assembly subset. Arbitrary video inputs are out of distribution and predictions may be meaningless.

**Q: Is 80% accuracy achieved?**  
No. V6 validation is 52.94%, reused exploratory test is 18.75%.

**Q: Is there a blind test?**  
Not in the current evidence. The test subset had been inspected in previous research iterations.

**Q: Are all Assembly101 videos in the repo?**  
No. Media is gated/rights-restricted and intentionally ignored. The V6 research subset pairs only 13 sessions.

**Q: Is the app real-time or production ready?**  
No. The backend runs bounded, potentially slow windowed analysis in a local demo.

**Q: Can I deploy commercially because the repository says MIT?**  
Not automatically. MIT covers this project's owned code, not Assembly101 media, upstream model/dataset licenses, or video/privacy rights. Check all separately.

**Q: Can we add more classes or a SOP score just by editing frontend labels?**  
No. New class mapping requires newly trained/validated weights and a consistent artifact contract; SOP scores require separate rules, annotations, and evaluation.

**Q: What should I work on next?**  
Prioritize paired-data auditing, truly unseen evaluation, and evidence-linked model error analysis before implementing purported SOP verdicts.

## Data rights, attribution, and licenses

- **Repository code:** MIT, see [`LICENSE`](LICENSE), copyright 2026 Wafa Bila Syaefurokhman.
- **Assembly101:** primary source [official project](https://assembly101.github.io/) and [dataset page](https://huggingface.co/datasets/cvml-nus/assembly101). Check gated access and original **CC BY-NC 4.0** terms independently. These restrictions are **not overwritten** by this repository's MIT license.
- **Pretrained R3D-18 / torchvision and Kinetics-400:** cite the original resources and verify current code/pretrained-weight/data-license terms separately before redistribution or commercial use.
- **Source video privacy:** do not upload/distribute identifiable or third-party footage without appropriate authorization. Do not commit recorded videos or expose stored uploads publicly.
- **Publication:** attribute the dataset creators and any pretrained model authors according to their licenses; report the small subset and evaluation limitations. Do not imply endorsement by Assembly101 maintainers.

## Source-of-truth and maintenance

**Documentation snapshot:** 2026-11-04. This README consolidates the verified public repository files and one locally reported successful API response; it does **not** imply CI or independent replications occurred. Any new version must update the notebook/configuration, data manifest, metrics/plots, model card, inference implementation and README **together** when relevant.

For coding agents and contributors, read [`AGENTS.md`](AGENTS.md) **before editing**. For experimental provenance use [`docs/dataset_provenance.md`](docs/dataset_provenance.md), [`docs/methodology.md`](docs/methodology.md), [`docs/limitations.md`](docs/limitations.md), and the actual V6 artifacts. For supplemental integration history see [`README_V6_SETUP.md`](README_V6_SETUP.md).

**Research principle:** *A running AI demonstration is engineering progress; an accurate, independently validated model is a separate scientific claim.*

---

<a id="bahasa-indonesia"></a>

# Bahasa Indonesia

# VisualSOP Checker — Dokumentasi Utama Bahasa Indonesia

**Day 30/100 Days of Projects · Manufacturing · Computer Vision · Prototipe penelitian**

> **Status per 4 November 2026:** Aplikasi lokal React + FastAPI **sudah dapat menjalankan inferensi asli** model R3D-18 V6 untuk enam aktivitas perakitan mainan. Sistem **belum mendeteksi pelanggaran SOP** dan **belum layak dipakai untuk keputusan keselamatan, kepatuhan, atau penilaian pekerja**. Metrik V6 menunjukkan generalisasi yang lemah.

Repositori: https://github.com/MENSTRUE/VisualSOP-Checker. Sumber kebenaran: `models/MODEL_CARD.json`, `models/inference_recipe.json`, `reports/v6/`, notebook `notebooks/visualsop-checker.ipynb`, dan implementasi `backend/app/`.

## 1. Ringkasan eksekutif dan masalah

Inspeksi rekaman prosedur perakitan membutuhkan waktu. Proyek ini menguji apakah model pengenalan aksi video bisa memberi **hipotesis aktivitas kasar** yang dapat ditinjau manusia, sebagai komponen awal calon sistem pemeriksaan SOP visual. **Mengenali aksi tidak sama dengan menilai kepatuhan:** pemeriksaan SOP yang valid memerlukan definisi prosedur, urutan tindakan yang diharapkan, anotasi waktu, konteks benda, label pelanggaran, dan pengujian terpisah.

Pertanyaan penelitian yang benar saat ini: *Bisakah R3D-18 pra-latih membedakan enam jenis tindakan Assembly101 pada subset terbatas, lalu mengeluarkan prediksi video nyata di antarmuka lokal?*

## 2. Before → Now → Next

| Fase | Kondisi | Bukti / langkah |
|---|---|---|
| **Before** | Penelitian notebook dan baseline pengenalan aksi; laporan evaluasi V6 tersedia | `notebooks/`, `reports/v6/` |
| **Now** | Frontend Vite/React dan backend FastAPI lokal; upload video, metadata, sampling motion, preview, prediksi R3D-18 V6 opsional | `frontend/src/main.tsx`, `backend/app/main.py`, `backend/app/v6_inference.py` |
| **Next** | Audit prediksi vs anotasi, tambah data beragam, benchmark buta yang baru, kalibrasi confidence, segmentasi aksi yang benar, aturan SOP dan dataset pelanggaran teranotasi | Roadmap; **belum selesai** |

**Uji integrasi yang pernah berhasil:** upload video contoh Assembly101 20 detik, 1280×720, 60 FPS, menghasilkan `model_status: experimental_v6`, sepuluh prediksi jendela video, dan `ai_error: null`. Pada contoh tersebut model dominan memprediksi `detach cabin`; **kebenaran tiap prediksi belum divalidasi**. Ini hanya uji fungsional, bukan metrik akurasi model.

## 3. Ruang lingkup dan batas klaim

**Tersedia:** enam kategori aktivitas, checkpoint V6, inferensi lokal, hasil prediksi per jendela dengan confidence, API JSON, serta bukti audit eksperimen.

**Belum tersedia:** klasifikasi sesuai SOP aktual, status lulus/gagal SOP, deteksi pelanggaran tervalidasi, deteksi batas aksi terlatih, benchmark lapangan, layanan aman untuk pengguna umum, pengujian otomatis komprehensif, ataupun sertifikasi keselamatan.

Jangan menuliskan “akurasi 80%”, “real-time”, “siap produksi”, “deteksi kesalahan pekerja”, “penilaian kepatuhan”, atau “AI telah memahami SOP” karena bukti tersebut belum ada. `sop_status: not_evaluated` harus tetap dipertahankan selama belum ada evaluasi SOP yang valid.

## 4. Dataset dan asal-usul

Dataset utama: **Assembly101** — https://huggingface.co/datasets/cvml-nus/assembly101 dan https://assembly101.github.io/. Dataset berisi aksi perakitan dan pembongkaran mainan, **bukan dataset pelanggaran SOP manufaktur dunia nyata**.

Inventaris lokal penelitian V6: **9 rekaman RGB awal + 4 tambahan = 13 sesi video terpasangkan** dengan anotasi; terdapat **680 berkas anotasi coarse** pada inventaris yang diproses. Sebagian besar pasangan dari kumpulan lebih besar belum dipakai. Data lokal Kaggle sebelumnya: `/kaggle/input/datasets/wafabila/visualsop-dataset` dan `/kaggle/input/datasets/wafabila/visualsop-dataset-next`; ketersediaannya tergantung akses dataset.

Anotasi memakai **basis indeks 30 FPS**, sementara video sumber sekitar **60 FPS**. Interpretasi indeks waktu yang salah dapat menghasilkan clip salah label. Lacak video asal, sesi, waktu awal/akhir, kelas, versi anotasi, serta pemetaan indeks-ke-detik. Atribusi, lisensi, versi dan tanggal akses diverifikasi melalui `docs/dataset_provenance.md` dan `reports/v6/metadata/dataset_provenance.json`. Jangan menebak metadata yang tidak tercatat.

**Hak penggunaan:** data Assembly101 memiliki persyaratan sumber tersendiri, termasuk akses terbatas dan ketentuan CC BY-NC 4.0 yang harus ditinjau; **lisensi MIT kode proyek tidak otomatis melisensikan video maupun bobot pra-latih**. Jangan unggah ulang video mentah atau mendistribusikan data terikat izin tanpa persetujuan.

## 5. Kelas, split, dan pencegahan kebocoran

Enam label yang benar sesuai urutan recipe/checkpoint:

1. `attach cabin`
2. `attach wheel`
3. `detach cabin`
4. `detach wheel`
5. `screw chassis`
6. `unscrew chassis`

Unit split adalah sesi/kelompok mainan, bukan potongan frame acak. V6 menggunakan kelompok **train 9013/9014/9015/9022; validation 9011/9012; exploratory test 9016/9021**. Total interval aksi independen: **62 train, 17 validation, 16 test historis**. Data train menghasilkan **124 tampilan clip** melalui dua posisi temporal; ini **bukan** 124 kejadian independen. Audit mencakup inventaris sesi, segmen, clip yang dicache, pasangan yang tidak ditemukan dan metadata video di `reports/v6/audit/`.

Test historis **sudah diperiksa dalam eksperimen sebelumnya**, sehingga **bukan uji buta independen**. Jangan memilih model/treshold/pipeline menggunakan test lama lalu menyebutnya hasil final. Cadangkan sumber baru untuk uji buta berikutnya. Test juga tidak seimbang: **14 dari 16** interval berasal dari kelompok 9021.

## 6. Arsitektur dan alur

```text
Video pengguna → React/Vite (5173)
               → proxy /api → FastAPI (8001)
               → validasi upload dan metadata
               → sampel beda frame + preview
               → jika checkpoint + recipe ditemukan:
                  sampling jendela 3 dtk / stride 2 dtk
                  → 16 frame RGB (78% interval bagian dalam)
                  → resize short edge 128 → crop center/motion
                  → transform R3D-18 pretrained
                  → R3D-18 + layer4/fc V6
                  → ensemble logit → softmax → top-3 + confidence
               → JSON hasil dan timeline UI
               → SOP: NOT EVALUATED
```

Model dasar `torchvision.models.video.r3d_18(weights=R3D_18_Weights.DEFAULT)` pra-latih **Kinetics-400**. Checkpoint `models/best_finetuned_layer4_fc.pt` **hanya berisi layer4 dan fc hasil fine-tuning**, bukan seluruh model. Karena itu bobot dasar resmi perlu tersedia; **jangan gunakan `weights=None` sebagai pengganti**. Kelas, 16 frame, resize 128, transform, ROI `ensemble`, dan posisi temporal harus sesuai `models/inference_recipe.json`.

**Jendela tiga detik dengan langkah dua detik** adalah heuristik antarmuka untuk video kontinu; model asli dilatih pada potongan aksi yang telah diberi batas waktu. Hasil dari jendela yang tumpang tindih bukan deteksi batas aksi terlatih. Confidence softmax **belum dikalibrasi**, jangan diperlakukan sebagai probabilitas bahwa aksi itu benar.

## 7. Metrik dan audit hasil V6

| Indikator | Nilai | Interpretasi |
|---|---:|---|
| Interval training independen | 62 | Data kecil |
| Clip views training | 124 | Dua tampilan; saling berkorelasi |
| Interval validasi | 17 | Dipakai memilih model |
| Interval exploratory test | 16 | Tidak buta |
| Epoch terbaik | 10 | Berdasarkan evaluasi V6 |
| ROI terpilih | ensemble | Dipilih via validasi |
| Akurasi validasi | **52,94% (9/17)** | Bukan akurasi produksi |
| Macro-F1 validasi | **51,11%** | Performa kelas belum kuat |
| Balanced accuracy validasi | **51,39%** | Lihat model card |
| Akurasi exploratory test | **18,75% (3/16)** | Generalisasi buruk |
| Macro-F1 exploratory test | **11,11%** | Sangat lemah |
| Balanced accuracy exploratory test | **16,67%** | Test terpapar sebelumnya |

Sumber angka: `models/MODEL_CARD.json`, `reports/v6/reports/results.json`, prediksi CSV dan confusion matrix. Jika dokumentasi dan artefak berbeda, **jangan mengganti angka secara diam-diam**: selesaikan perbedaan berdasarkan provenance dan bukti eksekusi.

## 8. Menjalankan lokal — Windows PowerShell

Dari root repo:

```powershell
cd "D:\porto\100 day\day 30\VisualSOP Checker"

# Instal backend pada venv lokal yang sudah disiapkan
.\backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt

# Kedua file model ini harus ada secara lokal, tidak dikomit ke Git
Test-Path .\models\best_finetuned_layer4_fc.pt
Test-Path .\models\inference_recipe.json

# Terminal 1: FastAPI
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```

Di terminal lain:

```powershell
cd "D:\porto\100 day\day 30\VisualSOP Checker\frontend"
npm ci
npm run dev
```

Buka `http://localhost:5173`. Pastikan target `frontend/vite.config.ts` adalah `http://127.0.0.1:8001`. Cek API dari terminal ketiga:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/health
Invoke-RestMethod http://localhost:5173/api/health
```

`model_inference_enabled: true` hanya berarti file model dan resep ditemukan. `model_loaded: false` **normal sebelum analisis pertama**. Setelah itu upload video dan pilih **Analyze video**. Python Windows PowerShell lama mungkin tidak memiliki `Invoke-RestMethod -Form`; pakai `curl.exe`:

```powershell
curl.exe -sS -X POST "http://127.0.0.1:8001/api/analyze" -F "file=@D:\porto\100 day\day 30\VisualSOP Checker\assets\examples\assembly101_test_20s.mp4"
```

Video contoh harus sudah tersedia sendiri di lokasi tersebut. `*.mp4` diabaikan Git. JSON yang berhasil bisa berisi `model_status: experimental_v6`, `activity_predictions`, dan `ai_error: null`. Status `sop_status` tetap `not_evaluated`.

## 9. API dan penyimpanan

- `GET /api/health` — status server, keberadaan dua file model, dan apakah model sudah pernah dimuat.
- `POST /api/analyze` — menerima unggahan video; metadata, sampel motion, prediksi eksperimental (jika berhasil).
- `GET /api/analyses/{job_id}` — mengambil kembali hasil JSON lokal.
- `GET /api/analyses/{job_id}/preview` — mengambil preview JPEG.

Batas kode yang saat ini terlihat: ekstensi `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`; default maksimal **150 MB** unggahan; durasi metadata maksimal **30 menit** tetapi inferensi AI dibatasi **120 detik** (video lebih panjang dapat tetap menghasilkan motion report dengan `ai_error`). Endpoint menyimpan unggahan/hasil di folder lokal `backend/storage/` secara default. Pengelolaan retensi dan otentikasi belum siap untuk server publik.

## 10. Reproducibility, pengujian, dan rilis

Semua percobaan harus mencatat: commit SHA, lingkungan Python/PyTorch/torchvision, notebook, data sumber dan versi, daftar sesi, split, kelas, seed, transform, bobot awal, epoch, metrik per kelas, confusion matrix, dan lokasi artefak. Notebook yang di-commit harus benar-benar dieksekusi, bukan hasil edit manual. `reports/v6/metadata/environment.json` berisi lingkungan eksperimen; **tidak otomatis menjamin seluruh dependency runtime sudah terkunci**.

Minimal cek yang perlu dijalankan dan dilaporkan (bukan klaim tes otomatis sudah tersedia):

```powershell
.\backend\.venv\Scripts\python.exe -m compileall -q backend\app
cd frontend
npm ci
npm run build
```

Uji API dengan video asli yang diizinkan. Periksa bahwa contoh prediksi berasal dari checkpoint sebenarnya; kondisi checkpoint hilang harus tampil jelas; file tidak valid ditolak; port proxy benar; hasil tersimpan dapat diambil ulang. Untuk regresi ML, bandingkan preprocessing, urutan kelas, bentuk tensor `(3,16,112,112)` dan distribusi prediksi dengan artefak notebook. Bukti uji lokal video 20 detik **bukan** bukti benchmark kualitas.

## 11. Struktur repository (jangan dirombak)

```text
VisualSOP Checker/
├── README.md, AGENTS.md, README_V6_SETUP.md
├── LICENSE, .gitignore, .env.example
├── notebooks/visualsop-checker.ipynb
├── models/MODEL_CARD.json, inference_recipe.json
│   └── best_finetuned_layer4_fc.pt  # lokal saja, diabaikan Git
├── reports/v6/{audit,examples,metadata,plots,predictions,reports}/
├── assets/{plots,examples,screenshots,diagrams}/
├── backend/app/{main.py,v6_inference.py}
├── backend/requirements.txt
├── frontend/src/{main.tsx,style.css}
├── frontend/{package.json,package-lock.json,vite.config.ts}
├── docs/{dataset_provenance.md,methodology.md,model_card.md,limitations.md}
└── scripts/
```

`.gitignore`: jangan memasukkan dataset mentah, video, pretrained artifacts terikat, model weights, `.env`, `node_modules`, venv, `backend/storage`, ataupun hasil cache. Struktur root standar sudah disepakati; **jangan menambah folder `datasets/`** di root dan jangan mengubah nama folder tanpa persetujuan.

## 12. Keterbatasan dan risiko

1. Data relatif sangat kecil dan mencakup sedikit variasi sesi.
2. Test pernah diperiksa, bukan blind held-out; berisiko bias eksperimen.
3. Perbedaan kelompok sumber, kamera dan pelaku dapat menjatuhkan performa.
4. `motion ROI` berdasarkan perbedaan piksel dapat memilih area gerak yang tidak relevan.
5. Output banyak memilih `detach cabin` pada satu sampel; periksa bias kelas dan ground truth.
6. Window inference heuristik tidak mengidentifikasi batas tindakan sesungguhnya.
7. Tidak ada dataset pelanggaran SOP, tidak ada label aman/tidak aman, tidak ada validasi industri.
8. Prediksi belum dikalibrasi, akurasi buruk; **wajib review manusia** untuk analisis apa pun.
9. Keamanan, autentikasi, privasi, dan retensi unggahan belum siap untuk paparan internet publik.
10. Lisensi dataset yang berbeda dari kode membatasi distribusi dan penggunaan komersial.

## 13. Roadmap yang terukur

| Prioritas | Langkah | Kriteria selesai |
|---|---|---|
| P0 | Stabilkan demo lokal dan tes regresi API | Health, upload, prediksi nyata, error dan UI lolos tes terdokumentasi |
| P0 | Audit 10 jendela hasil video vs anotasi asal | Tabel label benar, prediksi, waktu dan kesalahan |
| P1 | Perluas data dan split buta baru | Provenance, izin, sesi independen, uji tanpa tuning test |
| P1 | Benchmark baseline dan investigasi domain shift | Accuracy/macro-F1/per-kelas/CM dengan confidence interval |
| P1 | Bandingkan ROI, sampling, dan kalibrasi | Ablasi tervalidasi, tidak bocor ke test |
| P2 | Deteksi batas aksi dan pengenalan urutan | Dataset segmen dan metrik temporal khusus |
| P2 | Definisi SOP eksplisit + label pelanggaran | Rubrik, anotasi ahli, reliabilitas antarpenilai |
| P3 | Keamanan, antrean tugas, akses, retensi, observabilitas | Security review dan evaluasi operasional sebelum publik |

## 14. Deployment dan keamanan

Gunakan **lokal saja** dalam kondisi sekarang. FastAPI bind `127.0.0.1:8001`, Vite lokal `5173`, dan CORS mengizinkan origin lokal. Endpoint unggah belum memiliki autentikasi, pembatasan permintaan yang matang, scanning media, kebijakan retensi, atau sandbox decoding. Jangan mengekspose port secara publik untuk produksi. Sebelum rilis: validasi file berdasarkan isi, batas CPU/GPU/memori/durasi, izolasi pekerjaan, penghapusan file berkala, token/auth, TLS, logging aman, scan dependensi, dan kepatuhan lisensi.

## 15. Troubleshooting

| Masalah | Penyebab / tindakan |
|---|---|
| `ECONNREFUSED 127.0.0.1:8000` | Target Vite salah; proxy `/api` harus ke **8001** |
| `Errno 10048` | Backend lama masih mengikat port; hentikan dengan `Ctrl+C` sebelum restart |
| `model_checkpoint_present: false` | Periksa `models/`; dari `backend/app/v6_inference.py`, root yang benar `parents[2]` |
| `model_loaded: false` | Normal sebelum inferensi pertama; cek hasil `POST /api/analyze` |
| `inference_failed` | Baca `ai_error`; bisa karena torch/torchvision, pretrained weights, frame decode, atau checkpoint |
| `-Form` tidak dikenal di PowerShell | Gunakan `curl.exe -F` |
| Error pretrained weights | Unduh bobot resmi torchvision satu kali lewat jaringan yang diizinkan |
| Semua jendela kelas sama | Bisa jadi bias model/domain shift; evaluasi dengan anotasi, jangan asal klaim benar |
| Banyak warning `node_modules` Git | Tambahkan ignore `node_modules/`; jika telanjur tracked, lepas dari index secara hati-hati |
| Video lebih dari dua menit | Metadata/motion bisa selesai namun inferensi V6 sengaja menolak durasi di atas 120 detik |

## 16. FAQ

**Apakah model benar-benar hasil training?** Ya, checkpoint V6 menyimpan parameter fine-tune `layer4` dan `fc` di atas model R3D-18 yang dipra-latih pada Kinetics-400. File bobot lokal tidak otomatis ikut Git.

**Apakah ini deteksi pelanggaran SOP?** Belum. Enam kelas tindakan dan `sop_status: not_evaluated` tidak dapat membuktikan kepatuhan.

**Kenapa confidence tinggi tetapi akurasi rendah?** Softmax belum dikalibrasi dan data pengujian kecil/bergeser. Confidence tinggi bukan bukti prediksi benar.

**Apakah hasil 18,75% adalah final benchmark?** Tidak. Itu evaluasi eksploratif pada test yang sebelumnya terpapar, bukan benchmark blind.

**Apakah aplikasi sudah bermanfaat?** Sebagai demo alur inferensi dan bahan audit penelitian, ya. Sebagai alat keputusan kualitas industri atau keselamatan, belum.

**Mengapa model tidak dimasukkan GitHub?** Bobot besar diabaikan untuk menghindari repository bengkak dan menjaga kontrol terhadap artefak/ketentuan lisensi. Dokumentasikan checksum dan cara memperoleh artefak melalui mekanisme berizin.

**Bisakah dijalankan offline?** Setelah environment, checkpoint V6 dan pretrained weights resmi tersedia pada cache lokal, inferensi tidak membutuhkan API eksternal; keberhasilan tetap tergantung versi dependensi yang cocok.

**Apa status lisensinya?** Kode proyek MIT (`LICENSE`); dataset/rekaman Assembly101 dan bobot dari pihak lain memiliki hak dan kewajiban terpisah.

## 17. Sumber kebenaran dan pemeliharaan

Prioritas bila terjadi ketidaksesuaian: **hasil eksekusi asli dan manifest → `models/MODEL_CARD.json` dan `reports/v6` → notebook terverifikasi → kode runtime/recipe → dokumen naratif**. Perubahan pada angka, label, split, atau model harus menautkan artefak dan commit yang membuktikan perubahan. Perbarui bagian Bahasa Inggris dan Bahasa Indonesia secara bersamaan. Jangan mengubah `README_V6_SETUP.md` atau dokumentasi subfolder menjadi sumber angka yang bersaing.
