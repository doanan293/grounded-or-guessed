"""Select propose-and-verify knobs on dev, then write rankings for a split (no LLM calls).

    python scripts/pav_eval.py select        # dev grid → data/pav_dev_grid.csv, data/pav_params.json,
                                             # data/pav_mechanism.csv, data/vote_dev.csv
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


def mechanism(runs: list[dict], gt: dict, progs: list[str]) -> dict:
    """How discriminative is "a minimal fix passes the tests"? Rates over every checked (program, line) pair."""
    tl = tp = ol = op = 0
    for r in runs:
        for p in progs:
            for ln, cs in r[p]["checks"].items():
                ok = any(a for a, _ in cs)
                if int(ln) in gt[p]:
                    tl, tp = tl + 1, tp + ok
                else:
                    ol, op = ol + 1, op + ok
    return {"fault_line_checked": tl, "fault_line_fixable": round(tp / tl, 4) if tl else "",
            "other_line_checked": ol, "other_line_fixable": round(op / ol, 4) if ol else ""}


def vote(rankings_list: list[dict], progs: list[str]) -> dict[str, list[int]]:
    """Self-consistency: reciprocal-rank vote over repeats (ties → earliest position, then earliest repeat)."""
    out = {}
    for p in progs:
        score, first = {}, {}
        for ri, r in enumerate(rankings_list):
            for i, ln in enumerate(r.get(p, [])):
                score[ln] = score.get(ln, 0.0) + 1 / (i + 1)
                first.setdefault(ln, (i, ri))
        out[p] = sorted(score, key=lambda ln: (-score[ln], first[ln]))
    return out


def extras() -> None:
    """data/pav_mechanism.csv and data/vote_dev.csv (dev only, no LLM calls)."""
    runs = load_runs("dev")
    dev = json.loads((ROOT / "data" / "split.json").read_text())["dev"]
    gts = {g: v for g, v in load_variants().items() if g in ("original", "repaired", "reviewed")}
    with open(ROOT / "data" / "pav_mechanism.csv", "w", newline="") as f:
        rows = [{"gt": g, **mechanism(runs, gt, [p for p in dev if p in gt])} for g, gt in gts.items()]
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    stage1 = [rankings(r, None) for r in runs]
    voted = vote(stage1, dev)
    rows = []
    for g, gt in gts.items():
        progs = [p for p in dev if p in gt]
        rows.append({"gt": g, "single_acc1": round(acc(stage1, gt, progs, 1), 4), "single_acc3": round(acc(stage1, gt, progs, 3), 4),
                     "vote_acc1": round(acc([voted], gt, progs, 1), 4), "vote_acc3": round(acc([voted], gt, progs, 3), 4)})
    with open(ROOT / "data" / "vote_dev.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def apply(split: str) -> None:
    params = json.loads((ROOT / "data" / "pav_params.json").read_text())
    for f in sorted((ROOT / "runs").glob(f"pav_{split}_gemini_r[0-9].json")):
        r = json.loads(f.read_text())
        (ROOT / "data" / "rankings" / f.name).write_text(json.dumps(rankings(r, params), indent=1) + "\n")
        print(f.name, len(r))


if __name__ == "__main__":
    if sys.argv[1] == "select":
        select()
        extras()
    else:
        apply(sys.argv[2])
