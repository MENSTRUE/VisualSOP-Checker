# VisualSOP Checker

**Day 30/100 — Manufacturing / Computer Vision**

Exploratory computer vision research for recognizing
coarse-grained toy assembly and disassembly actions
using the Assembly101 dataset.

## Problem

Visual inspection of assembly procedures can be
time-consuming. This project explores whether video
action recognition can support a future visual SOP
checking workflow.

## Current Scope

- Six coarse assembly/disassembly action classes
- Real Assembly101 RGB video samples
- Group-disjoint train/validation/test protocol
- Pretrained R3D-18 and fine-tuning experiments
- Evaluation and error analysis

This implementation does NOT yet detect real-world
SOP violations.

## Baseline Selection

V6 is the selected research baseline based on
validation performance.

| Metric | V6 |
|---|---:|
| Validation accuracy | 52.94% |
| Validation macro-F1 | 51.11% |
| Exploratory test accuracy | 18.75% |
| Exploratory test correct | 3/16 |

The exploratory test set was inspected in earlier
experiments and must not be considered a blind test.

## Dataset

Assembly101:
https://huggingface.co/datasets/cvml-nus/assembly101

Source data is not distributed in this repository.
Review the original dataset license and access terms.

## Project Structure

- notebooks/ — Kaggle experiment notebooks
- models/ — model documentation; binary weights excluded
- reports/v6/ — experimental evidence and output
- assets/ — figures, diagrams and screenshots
- docs/ — provenance, methodology and model card
- backend/ — reserved for a future API
- frontend/ — reserved for a future interface
- scripts/ — reproducibility utilities

## Limitations

- Small training and validation sample sizes
- Significant distribution shift between source groups
- Historical test set is not blind
- No ground-truth SOP violation labels
- Not ready for production decision-making

## Status

Research baseline completed; target accuracy not achieved.
