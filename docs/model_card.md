# Model Card — VisualSOP V6

## Model

Fine-tuned R3D-18 for six-class toy assembly
action recognition.

## Research Data

Assembly101 RGB video recordings.

## Reported Results

Validation:
- Accuracy: 52.94% (9/17)
- Macro-F1: 51.11%

Historically exposed exploratory test:
- Accuracy: 18.75% (3/16)
- Macro-F1: 11.11%

## Intended Use

Experimental analysis of toy assembly actions.

## Not Intended For

- Production SOP compliance decisions
- Industrial safety monitoring
- Automated disciplinary decisions
- Validated detection of procedural violations

## Limitations

- Only 62 original training intervals
- Small evaluation sets
- Test set inspected in earlier versions
- Domain shift and poor generalization
- No ground-truth labels for SOP violations

## Deployment Status

RESEARCH ONLY — NOT PRODUCTION READY
