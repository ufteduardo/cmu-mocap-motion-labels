# CMU MoCap Motion Labels

Motion-class annotations for the [CMU Graphics Lab Motion Capture Database](http://mocap.cs.cmu.edu/),
released to support the reproducibility of the CMU experiments in:

> E. Ribeiro et al., "Local Graph Convolutions vs. Global Attention: Multi-Label Motion Classification
> for Motion-Asset Management in Digital Content Creation Pipelines", *Multimedia Tools and Applications*
> (under review).

- **2,435 motion clips** (every trial listed in the CMU motion index used here)
- **1,039 motion classes** (multi-label: a clip can carry several classes)

These are exactly the labels used to train and evaluate the models in the paper. No motion data
(BVH/AMC files or derived tensors) is included in this repository.

## Contents

| File | Description |
|---|---|
| [`data/cmu-mocap-index-text.txt`](data/cmu-mocap-index-text.txt) | Free-text descriptions of the CMU trials, as compiled by B. Hahne in the CMU BVH conversion release (source of all labels). |
| [`data/cmu_motion_labels.csv`](data/cmu_motion_labels.csv) | Final annotation per clip: `motion_id, canonical_label`, where `canonical_label` is a comma-separated list of motion classes. |
| [`data/labels_map.json`](data/labels_map.json) | Class vocabulary used for training: `label -> class index` (1,039 entries). |
| [`data/raw_to_labels.csv`](data/raw_to_labels.csv) | Side-by-side view: original CMU description, derived labels and class indices for every clip. |
| [`data/label_frequencies.csv`](data/label_frequencies.csv) | Number of clips per class. |
| [`data/flagged_label_inconsistencies.csv`](data/flagged_label_inconsistencies.csv) | The 74 clips whose labels are inconsistent with their original description (see *Known limitations*). |
| [`scripts/build_labels.py`](scripts/build_labels.py) | Rebuilds `labels_map.json` and the auxiliary tables from `cmu_motion_labels.csv`. |

## Annotation procedure

Each CMU trial comes with a short free-text description (e.g.
`01_09  playground - climb, hang, hold self up with arms straight, swing, drop, sit, dangle legs, go under`).
These descriptions were converted into class labels as follows:

1. **Text normalization** – descriptions were lower-cased; parenthetical notes such as
   `(human subject)` or `(2 subjects - subject A)` were removed; punctuation and file-name
   artifacts (`_`, `/`, numeric suffixes such as `Punch_Sequence001`) were stripped.
2. **Phrase extraction** – compound descriptions were split into individual action phrases at the
   separators present in the text (`,`, ` - `, `;`), so that each action or context becomes its own
   label, while multi-word actions were kept as a single phrase
   (e.g. `hold self up with arms straight`, `walk on uneven terrain`).
3. **LLM assistance** – steps 1 and 2 were carried out with the assistance of a large language
   model (Gemini 3.1, Google), which was used only for this text-processing step.
4. **Manual review** – the resulting lists were checked against the original descriptions and
   corrected by hand by the authors.
5. **Vocabulary construction** – every distinct label in `cmu_motion_labels.csv` becomes a
   class; classes are sorted alphabetically and indexed from 0 (`labels_map.json`).

No lemmatization or synonym mapping was applied.

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

## Known limitations

The labels are kept exactly as used in the experiments, including the following limitations,
which are also reported in the paper:

- **Long tail** – 465 of the 1,039 classes occur in a single clip.
- **Near-duplicate classes** – because no lemmatization or synonym mapping was applied,
  morphological variants and near-synonymous phrases remain distinct classes
  (e.g. `walk` / `walking`, `jump` / `jumps` / `jumping`, `pick up` / `pick up object`);
  33 groups of such near-duplicates, involving 70 classes, are present.
- **Non-semantic classes** – some classes are function words or non-motion annotations inherited
  from the descriptions (e.g. `a`, `with`, `unknown`, `calibration`).
- **Residual label noise** – a post-hoc automated comparison between each label set and its source
  description identified **74 clips (3.0%)** whose labels are inconsistent with the description and
  were not detected during the manual review (e.g. `06_06`, "basketball - backward dribble", labeled
  `forward dribble`; `62_04`, "screwing", labeled `sewing`). These clips are listed in
  [`data/flagged_label_inconsistencies.csv`](data/flagged_label_inconsistencies.csv). They were
  **not** corrected here, so that the files reproduce the experiments exactly.

## Source data and license

The motion data and original descriptions belong to the CMU Graphics Lab Motion Capture Database
(http://mocap.cs.cmu.edu/). The description index was compiled by B. Hahne as part of the CMU BVH
conversion release (a mirror is available at https://github.com/una-dinosauria/cmu-mocap).

If you use these labels, please also acknowledge the CMU database as requested by its creators:

> The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with
> funding from NSF EIA-0196217.

The annotations in this repository are released under the
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license (see [`LICENSE`](LICENSE)).
