"""Experimental R3D-18 V6 activity classification. Mirrors Day 30 V6 Kaggle notebook.

Checkpoint contains fine-tuned layer4 and fc only. Full Kinetics400 weights are REQUIRED.
Scores are uncalibrated and cannot establish SOP compliance.
"""
from __future__ import annotations
import json
import threading
from pathlib import Path
from typing import Any

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CKPT = ROOT / 'models' / 'best_finetuned_layer4_fc.pt'
RECIPE = ROOT / 'models' / 'inference_recipe.json'
CLASSES = ['attach cabin', 'attach wheel', 'detach cabin', 'detach wheel', 'screw chassis', 'unscrew chassis']
_lock = threading.Lock()
_model = None
_transform = None
_variant = None
_device = None


def readiness() -> dict[str, Any]:
    return {
        'model_checkpoint_present': CKPT.is_file(),
        'inference_recipe_present': RECIPE.is_file(),
        'model_inference_enabled': CKPT.is_file() and RECIPE.is_file(),
        'model_loaded': _model is not None,
    }


def _load():
    global _model, _transform, _variant, _device
    if _model is not None:
        return _model, _transform, _variant, _device
    if not CKPT.is_file() or not RECIPE.is_file():
        raise RuntimeError('V6 checkpoint or inference_recipe.json absent in repository models/')
    import torch
    from torch import nn
    from torchvision.models.video import r3d_18, R3D_18_Weights

    recipe = json.loads(RECIPE.read_text(encoding='utf8'))
    assert recipe['frames_per_clip'] == 16, 'Unsupported frames_per_clip'
    assert recipe['resize_short_edge'] == 128, 'Unsupported resize_short_edge'
    assert recipe['head_classes'] == CLASSES, 'Unexpected class mapping in inference recipe'
    variant = recipe['roi']
    if variant not in {'center', 'motion', 'ensemble'}:
        raise RuntimeError(f'Unsupported V6 ROI mode: {variant}')

    ckpt = torch.load(CKPT, map_location='cpu', weights_only=False)
    if list(ckpt['class_names']) != CLASSES:
        raise RuntimeError('Checkpoint label mapping differs from notebook V6')
    if ckpt['val_variant'] != variant:
        raise RuntimeError('Checkpoint and recipe ROI variants differ')
    # DO NOT use r3d_18(weights=None): the checkpoint ONLY contains layer4 and fc.
    weights = R3D_18_Weights.DEFAULT
    try:
        model = r3d_18(weights=weights)
    except Exception as e:
        raise RuntimeError('Kinetics-400 pretrained R3D-18 weights unavailable. Connect to Internet once or populate torchvision cache.') from e
    model.fc = nn.Linear(512, len(CLASSES))
    model.layer4.load_state_dict(ckpt['layer4'], strict=True)
    model.fc.load_state_dict(ckpt['fc'], strict=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device).eval()
    _model, _transform, _variant, _device = model, weights.transforms(), variant, device
    return _model, _transform, _variant, _device


def _square_crop(seq: np.ndarray, mode: str):
    t, h, w, _ = seq.shape
    size = min(h, w)
    cx, cy = w / 2, h / 2
    if mode == 'motion':
        gray = np.stack([cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in seq]).astype('float32')
        diff = np.mean(np.abs(np.diff(gray, axis=0)), axis=0)
        margin = max(2, int(min(h, w) * .04))
        diff[:margin] = 0
        diff[-margin:] = 0
        diff[:, :margin] = 0
        diff[:, -margin:] = 0
        threshold = np.percentile(diff, 90)
        yy, xx = np.where((diff >= threshold) & (diff > 1.5))
        if len(xx) >= 20:
            ww = diff[yy, xx]
            cx = float(np.average(xx, weights=ww))
            cy = float(np.average(yy, weights=ww))
    x = int(np.clip(round(cx - size / 2), 0, w - size))
    y = int(np.clip(round(cy - size / 2), 0, h - size))
    return seq[:, y:y + size, x:x + size, :].copy()


def _decode(video_path: Path, start: float, end: float, cap):
    # Exact temporal positions/resize from notebook cell 8: 16 frames in inner 78%.
    duration = end - start
    if duration <= 0:
        raise RuntimeError('Zero-length inference window')
    span = duration * .78
    left = start + (duration - span) * .50
    times = np.linspace(left + span * .015, left + span * .985, 16)
    frames = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000)
        ok, bgr = cap.read()
        if not ok:
            raise RuntimeError(f'Could not decode frame at {t:.2f}s for model inference')
        h, w = bgr.shape[:2]
        scale = 128 / min(h, w)
        nw = max(128, int(round(w * scale)))
        nh = max(128, int(round(h * scale)))
        resized = cv2.resize(bgr, (nw, nh), interpolation=cv2.INTER_AREA)
        frames.append(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    return np.stack(frames).astype('uint8')


def _clip_tensor(frames, mode, transform):
    import torch
    cropped = _square_crop(frames, mode)
    uint8 = torch.from_numpy(cropped.copy()).permute(0, 3, 1, 2).contiguous()
    x = transform(uint8)
    if tuple(x.shape) != (3, 16, 112, 112):
        raise RuntimeError(f'Incorrect R3D input shape: {tuple(x.shape)}')
    return x


def classify_video(video_path: Path, duration: float, window_s: float = 3.0, stride_s: float = 2.0) -> dict[str, Any]:
    """Windowed exploratory predictions; NOT learned segmentation or SOP verification."""
    import torch
    model, transform, variant, device = _load()
    if duration < 0.6:
        raise RuntimeError('Video shorter than minimum inference window')
    if duration > 120:
        raise RuntimeError('Experimental AI inference limited to 120-second videos')
    window_s = min(window_s, duration)
    starts = list(np.arange(0, max(duration - window_s, 0) + .001, stride_s))
    tail = max(0., duration - window_s)
    if not starts or abs(starts[-1] - tail) > .15:
        starts.append(tail)
    windows = sorted(set(round(float(s), 3) for s in starts))
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError('Cannot open video for model inference')
    output = []
    try:
        with _lock, torch.inference_mode():
            for start in windows:
                end = min(duration, start + window_s)
                frames = _decode(video_path, start, end, cap)
                def logits(mode):
                    clip = _clip_tensor(frames, mode, transform).unsqueeze(0).to(device)
                    return model(clip).float().cpu()[0]
                if variant == 'ensemble':
                    scores = (logits('center') + logits('motion')) / 2
                else:
                    scores = logits(variant)
                probabilities = torch.softmax(scores, dim=0).numpy()
                order = np.argsort(-probabilities)[:3]
                predicted = int(order[0])
                output.append({
                    'start_s': round(start, 2),
                    'end_s': round(end, 2),
                    'label': CLASSES[predicted],
                    'confidence': round(float(probabilities[predicted]), 4),
                    'top3': [{'label': CLASSES[int(k)], 'confidence': round(float(probabilities[k]), 4)} for k in order],
                    'uncertain': bool(probabilities[predicted] < .65),
                })
    finally:
        cap.release()
    return {'predictions': output, 'variant': variant, 'window_s': window_s, 'stride_s': stride_s}

