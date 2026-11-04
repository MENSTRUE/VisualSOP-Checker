# VisualSOP V6 — Experimental real model inference

Copy `backend/app/main.py`, `backend/app/v6_inference.py`, `backend/requirements.txt`, and `frontend/src/main.tsx` into the corresponding existing repo paths. Do not delete or rename other folders.

## Windows PowerShell (repository root)

```powershell
cd "D:\porto\100 day\day 30\VisualSOP Checker"
# Existing backend venv; torchvision downloads Kinetics-400 base weights once.
.\backend\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
# Confirm BOTH files already exist under models/ (do not commit large weights)
Test-Path .\models\best_finetuned_layer4_fc.pt
Test-Path .\models\inference_recipe.json
# Stop the old server (Ctrl+C), then use port 8001 ONLY
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001
```

Vite proxy MUST still target `http://127.0.0.1:8001`. Restart Vite. Open http://localhost:5173. `GET /api/health` should show `model_inference_enabled:true` (means required files exist, NOT that model is already loaded). Upload your Assembly101 20s MP4 and click Analyze. `activity_predictions` will contain actual windowed V6 predictions. If loading pretrained weights fails, `ai_error` explains why and the motion report still works.

**Model and data constraints:** Official torchvision `R3D_18_Weights.DEFAULT` Kinetics-400 pretraining is required, because the checkpoint only stores the fine-tuned `layer4` and six-way `fc`. Never instantiate a random base model as fallback. Preprocessing mirrors V6 notebook: 16 RGB frames sampled within inner 78% of each selected temporal window; short edge resized to 128; center/motion ROI crop; pretrained transforms; center/motion/ensemble determined by recipe. The continuous-video **3s windows with 2s stride are new heuristics**, not trained segment boundaries. Scores are uncalibrated and V6 exploratory accuracy is poor. There are **no SOP violation labels**. Do not rely on this output for safety or personnel evaluation.

If requirements install or network download fails, use internet access once for official pretrained weights, then repeat. Runtime may be CPU-heavy.
