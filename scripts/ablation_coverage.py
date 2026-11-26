"""Coverage ablation for the single-prompt baseline → data/ablation_coverage.csv.

    python scripts/ablation_coverage.py
Three single-prompt methods on the test split (3 Gemini repeats each), compared pairwise on the same programs:
  llm_coverage = failing tests + per-line [f/p] coverage   (data/rankings/direct_cov_test_gemini_r*.json)
  llm_tests    = the same prompt without the coverage annotations   (direct_tests_test_gemini_r*.json)
  llm_direct   = SemLoc's direct mode, source only   (direct_test_gemini_r*.json)
Rows: coverage_effect = llm_coverage − llm_tests, tests_effect = llm_tests − llm_direct, per ground truth
(original / repaired) and subset (all / executable), with cluster-bootstrap CIs (flx.stats.paired_diff_ci).
"""
import csv
import json
from pathlib import Path

from flx.gt import load_variants
from flx.labels import labels_for
from flx.stats import paired_diff_ci

ROOT = Path(__file__).resolve().parents[1]
RANK = ROOT / "data" / "rankings"
COV = ROOT / "data" / "coverage" / "semfault"
PREFIX = {"llm_coverage": "direct_cov_test_gemini_r", "llm_tests": "direct_tests_test_gemini_r",
          "llm_direct": "direct_test_gemini_r"}
PAIRS = {"coverage_effect": ("llm_coverage", "llm_tests"), "tests_effect": ("llm_tests", "llm_direct")}


def hits(preds: list[dict], gt: dict, progs: list[str], k: int) -> list[dict]:
    """One {program: hit@k} per repeat."""
    return [{p: any(ln in gt[p] for ln in rep.get(p, [])[:k]) for p in progs} for rep in preds]


def compare(a: list[dict], b: list[dict], gt: dict, progs: list[str], clusters: dict | None, k_boot: int = 10000) -> dict:
    row = {"n": len(progs), "repeats": len(a)}
    for k in (1, 3, 5):
        ha, hb = hits(a, gt, progs, k), hits(b, gt, progs, k)
        row[f"a_acc{k}"] = sum(sum(r[p] for r in ha) / len(ha) for p in progs) / len(progs)
        row[f"b_acc{k}"] = sum(sum(r[p] for r in hb) / len(hb) for p in progs) / len(progs)
        if k in (1, 3):
            row[f"d_acc{k}"], row[f"d_acc{k}_lo"], row[f"d_acc{k}_hi"] = paired_diff_ci(ha, hb, progs, clusters, k_boot=k_boot)
    return row


def main() -> None:
    test = json.loads((ROOT / "data" / "split.json").read_text())["test"]
    clusters = {r["program"]: int(r["cluster_t0.8"]) for r in csv.DictReader(open(ROOT / "data" / "semfault_templates.csv"))}
    preds = {m: [json.loads(f.read_text()) for f in sorted(RANK.glob(f"{pre}[0-9].json"))] for m, pre in PREFIX.items()}
    rows = []
    for gname, gt in load_variants().items():
        if gname not in ("original", "repaired", "reviewed"):
            continue
        progs = [p for p in test if p in gt]
        labels = labels_for({p: gt[p] for p in progs}, COV)
        for sub, plist in (("all", progs), ("executable", [p for p in progs if labels[p] != "not_executed"])):
            for name, (a, b) in PAIRS.items():
                if not preds[a] or not preds[b]:
                    continue
                r = compare(preds[a], preds[b], gt, plist, clusters)
                rows.append({"gt": gname, "subset": sub, "contrast": name, "a": a, "b": b,
                             **{k: round(v, 4) if isinstance(v, float) else v for k, v in r.items()}})
    out = ROOT / "data" / "ablation_coverage.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r["gt"], r["subset"], r["contrast"], r["d_acc1"], r["d_acc3"], f"[{r['d_acc3_lo']}, {r['d_acc3_hi']}]")


if __name__ == "__main__":
    main()
