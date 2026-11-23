# CMU MoCap Motion Labels

Motion-class annotations for the [CMU Graphics Lab Motion Capture Database](http://mocap.cs.cmu.edu/),
released to support the reproducibility of our motion-classification experiments.

- **2,435 motion clips** (every trial listed in the official CMU index)
- **1,039 motion classes** (multi-label: a clip can carry several classes)

## Contents

| File | Description |
|---|---|
| [`data/cmu-mocap-index-text.txt`](data/cmu-mocap-index-text.txt) | Original free-text descriptions distributed with the CMU database (source of all labels). |
| [`data/cmu_motion_labels.csv`](data/cmu_motion_labels.csv) | Final annotation per clip: `motion_id, canonical_label`, where `canonical_label` is a comma-separated list of motion classes. |
| [`data/labels_map.json`](data/labels_map.json) | Class vocabulary used for training: `label -> class index` (1,039 entries). |
| [`data/raw_to_labels.csv`](data/raw_to_labels.csv) | Side-by-side view: original CMU description, derived labels and class indices for every clip. |
| [`data/label_frequencies.csv`](data/label_frequencies.csv) | Number of clips per class. |
| [`scripts/build_labels.py`](scripts/build_labels.py) | Rebuilds `labels_map.json` and the auxiliary tables from `cmu_motion_labels.csv`. |

## Annotation procedure

Each CMU trial comes with a short free-text description (e.g.
`01_09  playground - climb, hang, hold self up with arms straight, swing, drop, sit, dangle legs, go under`).
These descriptions were converted into class labels as follows:

1. **Text normalization** – descriptions were lower-cased; parenthetical notes such as
   `(human subject)` or `(2 subjects - subject A)` were removed; punctuation and file-name
   artifacts (`_`, `/`, numeric suffixes such as `Punch_Sequence001`) were stripped.
2. **Semantic disentanglement** – compound descriptions were split into their individual
   actions using the separators present in the text (`,`, ` - `, `;`), so that each action or
   context becomes its own label, while multi-word actions were kept as a single phrase
   (e.g. `hold self up with arms straight`, `walk on uneven terrain`).
3. **Manual review** – the resulting lists were checked against the original descriptions and
   corrected by hand where the automatic split was wrong.
4. **Vocabulary construction** – every distinct label in `cmu_motion_labels.csv` becomes a
   class; classes are sorted alphabetically and indexed from 0 (`labels_map.json`).

Examples (from `raw_to_labels.csv`):

| Clip | Original CMU description | Labels |
|---|---|---|
| 01_01 | playground - forward jumps, turn around | playground · forward jumps · turn around |
| 13_08 | unscrew bottlecap, drink soda, screw on bottlecap | unscrew bottlecap · drink soda · screw on bottlecap |
| 16_57 | run/jog, sudden stop | runjog · sudden stop |
| 31_16 | elephant (human subject) | elephant |
| 144_21 | Punch_Sequence001 | punch sequence |

## Reproducing the class vocabulary

```bash
python scripts/build_labels.py
```

Expected output:

```
Rebuilt vocabulary MATCHES data/labels_map.json
Clips: 2435 | Classes: 1039 | Classes seen in a single clip: 465
```

No third-party packages are required (Python 3 standard library only).

## Notes

- The vocabulary is long-tailed: 465 of the 1,039 classes occur in a single clip.
- Labels are kept exactly as used in the experiments, so some near-duplicate surface forms
  remain as distinct classes (e.g. `walk` / `walking`, `jump` / `jumps`).

## Source data and license

The motion data and original descriptions belong to the CMU Graphics Lab Motion Capture
Database (http://mocap.cs.cmu.edu/), funded by NSF EIA-0196217, which may be freely used for
research. The annotations in this repository are released under the
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.
