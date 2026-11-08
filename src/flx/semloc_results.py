"""Read SemLoc result directories and compute Acc@k the way the SemLoc artifact does.

Every loader returns {program: best_rank or None}; None means the fault was not
ranked and counts as a miss. Scoring rules deliberately mirror
third_party/semloc/print_results.py so RQ1a reproduces the published numbers:
  * SBFL ties are broken by line order in the JSON (optimistic for early lines);
  * DD's unranked minimal set counts any hit as rank 1;
  * median rank is taken over programs whose fault was ranked.

    python -m flx.semloc_results --results third_party/semloc/results/RQ1 \
        --gt third_party/semloc/benchmark/ground_truth.json --out data/rq1a_table.csv
"""
import argparse
import csv
import json
from pathlib import Path
from typing import Mapping, Optional

Ranks = dict[str, Optional[int]]


def load_ground_truth(gt_path: Path) -> dict[str, list[int]]:
    data = json.loads(Path(gt_path).read_text())
    return {e["file"].removesuffix(".py"): e.get("faulty_lines", []) for e in data["programs"]}


def find_localization_csv(config_dir: Path) -> Optional[Path]:
    for sub in ("results_cf_base", "results", "."):
        p = Path(config_dir) / sub / "rq1_localization.csv"
        if p.exists():
            return p
    return None


def best_ranks_from_csv(csv_path: Path) -> Ranks:
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        # Column is "Function" in some artifact CSVs and "function" in others.
        return {(row.get("Function") or row["function"]): int(row["best_rank"])
                if (row.get("best_rank") or "").isdigit() else None
                for row in csv.DictReader(f)}


def pct_suspicious_from_csv(csv_path: Path) -> list[float]:
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        return [float(r["pct_suspicious"]) for r in csv.DictReader(f)
                if r.get("pct_suspicious") not in ("", "N/A", None)]


def _rank_of_faults(ranked_lines: list[int], faulty: list[int]) -> Optional[int]:
    hits = [ranked_lines.index(fl) + 1 for fl in faulty if fl in ranked_lines]
    return min(hits) if hits else None


def sbfl_best_ranks(sbfl_dir: Path, ground_truth: Path) -> Ranks:
    gt = load_ground_truth(ground_truth)
    ranks: Ranks = {}
    for path in sorted(Path(sbfl_dir).glob("*.json")):
        prog = path.stem
        if not gt.get(prog):
            continue
        d = json.loads(path.read_text())
        res = d["sbfl"] if isinstance(d.get("sbfl"), dict) and "line_scores" in d["sbfl"] else d
        scores = res.get("line_scores", {})
        ranked = [int(ln) for ln, _ in sorted(scores.items(), key=lambda x: -float(x[1]))]  # stable sort
        ranks[prog] = _rank_of_faults(ranked, gt[prog])
    return ranks


def sbfl_pct_suspicious(sbfl_dir: Path) -> list[float]:
    out = []
    for path in sorted(Path(sbfl_dir).glob("*.json")):
        d = json.loads(path.read_text())
        res = d.get("dd", {}) if path.parent.name == "dd" else (d["sbfl"] if isinstance(d.get("sbfl"), dict) else d)
        if res.get("pct_suspicious") is not None:
            out.append(float(res["pct_suspicious"]))
    return out


def dd_best_ranks(dd_dir: Path, ground_truth: Path) -> Ranks:
    gt = load_ground_truth(ground_truth)
    ranks: Ranks = {}
    for path in sorted(Path(dd_dir).glob("*.json")):
        prog = path.stem
        if not gt.get(prog):
            continue
        minimal = json.loads(path.read_text()).get("dd", {}).get("minimal_lines", [])
        ranks[prog] = 1 if any(fl in minimal for fl in gt[prog]) else None
    return ranks


def direct_fl_best_ranks(direct_dir: Path) -> Ranks:
    ranks: Ranks = {}
    for path in sorted(Path(direct_dir).glob("*.json")):
        if path.name == "aggregate.json":
            continue
        d = json.loads(path.read_text())
        if d.get("top1_rate") is None:
            continue
        if d["top1_rate"] > 0:
            r = 1
        elif d.get("top3_rate") and d["top3_rate"] > 0:
            r = d["best_rank_ever"] if isinstance(d.get("best_rank_ever"), int) else 3
        elif d.get("top5_rate") and d["top5_rate"] > 0:
            r = d["best_rank_ever"] if isinstance(d.get("best_rank_ever"), int) else 5
        else:
            r = d["best_rank_ever"] if isinstance(d.get("best_rank_ever"), int) and d["best_rank_ever"] > 5 else None
        ranks[d.get("function", path.stem)] = r
    return ranks


def acc_at_k(best_ranks: Mapping[str, Optional[int]], k: int) -> float:
    if not best_ranks:
        return float("nan")
    return sum(1 for r in best_ranks.values() if r is not None and r <= k) / len(best_ranks)


def median_rank(best_ranks: Mapping[str, Optional[int]]) -> Optional[float]:
    found = sorted(r for r in best_ranks.values() if r is not None)
    return found[len(found) // 2] if found else None


def subset(best_ranks: Mapping[str, Optional[int]], programs) -> Ranks:
    keep = set(programs)
    return {p: r for p, r in best_ranks.items() if p in keep}


def _row(config: str, ranks: Ranks, pcts: list[float]) -> dict:
    n = len(ranks)
    return {"config": config, "n": n,
            "acc1": acc_at_k(ranks, 1) if n else None, "acc3": acc_at_k(ranks, 3) if n else None,
            "acc5": acc_at_k(ranks, 5) if n else None, "median_rank": median_rank(ranks),
            "pct_suspicious": sum(pcts) / len(pcts) if pcts else None}


def ranks_for_config(config_dir: Path, ground_truth: Path) -> tuple[Ranks, list[float]]:
    name = Path(config_dir).name
    if name.startswith("sbfl_"):
        return sbfl_best_ranks(config_dir, ground_truth), sbfl_pct_suspicious(config_dir)
    if name == "dd":
        return dd_best_ranks(config_dir, ground_truth), sbfl_pct_suspicious(config_dir)
    if name.startswith("semantic_indexing_disabled"):
        return direct_fl_best_ranks(config_dir), []
    csv_path = find_localization_csv(config_dir)
    if csv_path is None:
        return {}, []
    return best_ranks_from_csv(csv_path), pct_suspicious_from_csv(csv_path)


def rq1a_table(results_root: Path, ground_truth: Path) -> list[dict]:
    rows = []
    for d in sorted(p for p in Path(results_root).iterdir() if p.is_dir()):
        ranks, pcts = ranks_for_config(d, ground_truth)
        rows.append(_row(d.name, ranks, pcts))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--gt", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    rows = rq1a_table(args.results, args.gt)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    for r in rows:
        fmt = lambda v: "N/A" if v is None else f"{100 * v:5.1f}"
        print(f"{r['config']:38s} n={r['n']:3d}  acc@1 {fmt(r['acc1'])}  acc@3 {fmt(r['acc3'])}  acc@5 {fmt(r['acc5'])}")


if __name__ == "__main__":
    main()
