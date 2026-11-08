"""Objective fault-type labels for SemFault-style programs (spec section 3.3).

A fault is *semantic* when some faulty line is executed by at least one failing
test and at least one passing test: coverage alone cannot tell it apart.
It is *coverage_revealed* when failing tests reach a faulty line but no passing
test does, and *not_executed* when no failing test reaches any faulty line.
Per-test coverage comes from SemLoc's own baselines helpers.

    python -m flx.labels --benchmark third_party/semloc/benchmark --out data/semfault_labels.csv
"""
import argparse
import csv
import json
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Literal

from flx._semloc import SEMLOC_ROOT, ensure_on_path

Category = Literal["semantic", "coverage_revealed", "not_executed"]


@dataclass(frozen=True)
class Label:
    program: str
    n_pass: int
    n_fail: int
    fault_hit_by_fail: bool
    fault_hit_by_pass: bool
    category: Category


def label_program(program: str, src: Path, test: Path, faulty_lines: list[int]) -> Label:
    ensure_on_path()
    import baselines

    repo_root = str(SEMLOC_ROOT / "src")  # holds the conftest.py the benchmark tests rely on
    abs_src = os.path.realpath(src)
    test = Path(test).resolve()  # SemLoc runs pytest with cwd=repo_root
    faults = set(faulty_lines)
    n_pass = n_fail = 0
    semantic = hit_fail = hit_pass = False
    pass_hits: set[int] = set()
    fail_hits: set[int] = set()
    for test_id in baselines.get_test_ids(str(test), repo_root):
        passed, hit = baselines._coverage_for_test(test_id, abs_src, repo_root)
        if passed:
            n_pass += 1
            pass_hits |= hit & faults
        else:
            n_fail += 1
            fail_hits |= hit & faults
    hit_fail, hit_pass = bool(fail_hits), bool(pass_hits)
    semantic = bool(fail_hits & pass_hits)
    if not hit_fail:
        cat: Category = "not_executed"
    elif semantic:
        cat = "semantic"
    else:
        cat = "coverage_revealed"
    return Label(program, n_pass, n_fail, hit_fail, hit_pass, cat)


def _label_one(args) -> Label:
    return label_program(*args)


def read_labels(path: Path) -> list[Label]:
    with open(path, newline="") as f:
        return [Label(r["program"], int(r["n_pass"]), int(r["n_fail"]), r["fault_hit_by_fail"] == "True",
                      r["fault_hit_by_pass"] == "True", r["category"]) for r in csv.DictReader(f)]


def main() -> None:
    ap = argparse.ArgumentParser(description="Label SemFault programs as semantic / coverage_revealed")
    ap.add_argument("--benchmark", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    gt = json.loads((args.benchmark / "ground_truth.json").read_text())["programs"]
    jobs = [(e["file"].removesuffix(".py"), args.benchmark / "programs" / e["file"],
             args.benchmark / "testcases" / f"test_{e['file']}", e["faulty_lines"]) for e in gt]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        labels = sorted(pool.map(_label_one, jobs), key=lambda l: l.program)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[x.name for x in fields(Label)])
        w.writeheader()
        w.writerows(asdict(l) for l in labels)
    for cat in ("semantic", "coverage_revealed", "not_executed"):
        print(f"{cat:18s} {sum(l.category == cat for l in labels)}")


if __name__ == "__main__":
    main()
