"""
Builds the motion-class vocabulary (labels_map.json) and auxiliary tables
from data/cmu_motion_labels.csv.

This is the same procedure used in our training pipeline
(`scan_and_match_dataset`): every comma-separated label in the
`canonical_label` column is one class; classes are sorted alphabetically
and indexed from 0.

Usage:
    python scripts/build_labels.py
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def parse_labels(s: str):
    return [l.strip() for l in next(csv.reader([s], skipinitialspace=True), []) if l.strip()]


def read_raw_index(path: Path):
    raw = {}
    with open(path, encoding="latin-1") as f:
        for line in f:
            m = re.match(r"^(\d{2,3}_\d{2})\t+(.*)", line.rstrip("\n"))
            if m:
                raw[m.group(1)] = m.group(2).strip()
    return raw


def main():
    with open(DATA / "cmu_motion_labels.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    motion_to_labels = {r["motion_id"].strip(): parse_labels(r["canonical_label"]) for r in rows}

    all_labels = sorted({l for labels in motion_to_labels.values() for l in labels})
    labels_map = {label: i for i, label in enumerate(all_labels)}

    counts = Counter(l for labels in motion_to_labels.values() for l in set(labels))
    with open(DATA / "label_frequencies.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["class_id", "label", "num_clips"])
        for label, idx in labels_map.items():
            w.writerow([idx, label, counts[label]])

    raw = read_raw_index(DATA / "cmu-mocap-index-text.txt")
    with open(DATA / "raw_to_labels.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["motion_id", "original_cmu_description", "labels", "class_ids"])
        for mid, labels in motion_to_labels.items():
            w.writerow([mid, raw.get(mid, ""), " | ".join(labels),
                        " ".join(str(labels_map[l]) for l in labels)])

    reference = DATA / "labels_map.json"
    if reference.exists():
        ref = json.load(open(reference, encoding="utf-8"))
        status = "MATCHES" if ref == labels_map else "DIFFERS FROM"
        print(f"Rebuilt vocabulary {status} data/labels_map.json")
    print(f"Clips: {len(motion_to_labels)} | Classes: {len(labels_map)} | "
          f"Classes seen in a single clip: {sum(1 for c in counts.values() if c == 1)}")


if __name__ == "__main__":
    main()
