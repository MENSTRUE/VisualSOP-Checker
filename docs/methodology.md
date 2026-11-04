# Methodology

## Task

Six-class coarse action recognition.

Classes:
- attach cabin
- attach wheel
- detach cabin
- detach wheel
- screw chassis
- unscrew chassis

## Research Design

- Source-group-disjoint data split
- R3D-18 pretrained on Kinetics400
- Video clip sampling and visual preprocessing
- Fine-tuning and validation-based selection
- Per-class classification evaluation

## Main Experiment

V6: pretrained R3D-18 fine-tuning with
a heuristic motion-guided ROI and visual
crop ensemble.

## Evaluation

Report:
- Accuracy
- Macro-F1
- Per-class precision and recall
- Confusion matrix
- Data and model limitations

Historical exploratory test data has been used
in previous experiments and is not blind.

For full reproducibility, include the original
V6 notebook and configuration when available.
