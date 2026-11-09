"""Select propose-and-verify knobs on dev, then write rankings for a split (no LLM calls).

    python scripts/pav_eval.py select        # dev grid → data/pav_dev_grid.csv, data/pav_params.json
    python scripts/pav_eval.py apply test    # runs/pav_test_gemini_r*.json → data/rankings/pav_test_gemini_r*.json
Selection (fixed before looking at test): highest dev Acc@1 averaged over the original and the reviewed ground truth
and over repeats; ties → Acc@3, then fewer LLM calls (k·attempts), then order "llm", then the smaller max_size.
The repaired ground truth is reported but not used for selection: it was itself built with a minimal-fix oracle,
the same mechanism as the verify stage.
"""
import csv
import itertools
import json
import sys
from pathlib import Path

from flx.gt import load_variants
from flx.pav import Check, rank

ROOT = Path(__file__).resolve().parents[1]
GRID = [{"k": k, "attempts": a, "order": o, "max_size": m}
        for k, a, o, m in itertools.product((2, 3), (1, 2), ("llm", "size"), (1, 2, 3, None))]
SELECT_GT = ("original", "reviewed")


def load_runs(split: str) -> list[dict]:
    return [json.loads(f.read_text()) for f in sorted((ROOT / "runs").glob(f"pav_{split}_gemini_r[0-9].json"))]


def rankings(run: dict, prm: dict | None) -> dict[str, list[int]]:
    """prm None = stage 1 only (the LLM + failing tests baseline)."""
    out = {}
    for p, r in run.items():
        checks = {int(ln): [Check(bool(a), b) for a, b in cs] for ln, cs in r["checks"].items()}
        out[p] = list(r["stage1"]) if prm is None else rank(r["stage1"], checks, **prm)
    return out


def acc(ranks: list[dict], gt: dict, progs: list[str], k: int) -> float:
    return sum(sum(any(ln in gt[p] for ln in r.get(p, [])[:k]) for p in progs) / len(progs) for r in ranks) / len(ranks)


def select() -> None:
    runs = load_runs("dev")
    dev = json.loads((ROOT / "data" / "split.json").read_text())["dev"]
    gts = load_variants()
    rows = []
    for prm in [None] + GRID:
        rk = [rankings(r, prm) for r in runs]
        row = {**(prm or {"k": 0, "attempts": 0, "order": "stage1", "max_size": ""})}
        row["max_size"] = "" if row["max_size"] is None else row["max_size"]
        for g in ("original", "repaired", "reviewed"):
            progs = [p for p in dev if p in gts[g]]
            for k in (1, 3):
                row[f"{g}_acc{k}"] = round(acc(rk, gts[g], progs, k), 4)
        row["select_acc1"] = round(sum(row[f"{g}_acc1"] for g in SELECT_GT) / len(SELECT_GT), 4)
        row["select_acc3"] = round(sum(row[f"{g}_acc3"] for g in SELECT_GT) / len(SELECT_GT), 4)
        rows.append(row)
    with open(ROOT / "data" / "pav_dev_grid.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cand = [r for r in rows if r["order"] != "stage1"]
    best = max(cand, key=lambda r: (r["select_acc1"], r["select_acc3"], -r["k"] * r["attempts"], r["order"] == "llm",
                                    -(r["max_size"] if r["max_size"] != "" else 99)))
    params = {k: best[k] for k in ("k", "attempts", "order")}
    params["max_size"] = None if best["max_size"] == "" else best["max_size"]
    (ROOT / "data" / "pav_params.json").write_text(json.dumps(params, indent=1) + "\n")
    base = rows[0]
    print("stage1:", {k: v for k, v in base.items() if "acc" in k})
    print("chosen:", params, {k: v for k, v in best.items() if "acc" in k})


def apply(split: str) -> None:
    params = json.loads((ROOT / "data" / "pav_params.json").read_text())
    for f in sorted((ROOT / "runs").glob(f"pav_{split}_gemini_r[0-9].json")):
        r = json.loads(f.read_text())
        (ROOT / "data" / "rankings" / f.name).write_text(json.dumps(rankings(r, params), indent=1) + "\n")
        print(f.name, len(r))


if __name__ == "__main__":
    select() if sys.argv[1] == "select" else apply(sys.argv[2])
