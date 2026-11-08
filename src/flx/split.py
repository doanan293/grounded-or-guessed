"""Fixed dev/test split of SemFault-250, stratified by fault label.

    python -m flx.split --labels data/semfault_labels.csv --out data/split.json
"""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

from flx.labels import Label, read_labels


def make_split(labels: list[Label], n_dev: int = 50, seed: int = 20261108) -> dict:
    rng = random.Random(seed)
    by_cat: dict[str, list[str]] = defaultdict(list)
    for lab in sorted(labels, key=lambda l: l.program):
        by_cat[lab.category].append(lab.program)
    total = len(labels)
    # Largest-remainder allocation so dev keeps each category's share.
    quotas = {c: n_dev * len(ps) / total for c, ps in by_cat.items()}
    alloc = {c: int(q) for c, q in quotas.items()}
    for c in sorted(quotas, key=lambda c: quotas[c] - alloc[c], reverse=True)[: n_dev - sum(alloc.values())]:
        alloc[c] += 1
    dev: list[str] = []
    for c in sorted(by_cat):
        dev += rng.sample(by_cat[c], alloc[c])
    dev_set = set(dev)
    return {"seed": seed, "n_dev": n_dev, "dev": sorted(dev_set),
            "test": sorted(l.program for l in labels if l.program not in dev_set)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--labels", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    split = make_split(read_labels(args.labels))
    args.out.write_text(json.dumps(split, indent=2) + "\n")
    print(f"dev={len(split['dev'])} test={len(split['test'])}")


if __name__ == "__main__":
    main()
