"""Static-analysis baseline: do ruff (lint) and pyrefly (type check) point at SemFault-250's faulty lines?

    python scripts/static_tools.py --run    # run the pinned tools via uvx → data/static/*.json (needs network once)
    python scripts/static_tools.py          # score the stored diagnostics → data/static_tools.csv (offline)
A tool "localizes" a program when one of its diagnostics sits on a ground-truth line; within_2_lines counts a
diagnostic at most two lines away (a symptom next to the fault). No LLM calls.
"""
import argparse
import csv
import json
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.gt import load_variants

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "static"
PROGRAMS = SEMLOC_ROOT / "benchmark" / "programs"
RUFF, PYREFLY = "ruff@0.14.0", "pyrefly@0.40.0"
TOOLS = {"ruff_default": "ruff (default rules)", "ruff_all": "ruff (all rules)", "pyrefly": "pyrefly (type check)"}


def run_tools() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, extra in (("ruff_default", []), ("ruff_all", ["--select", "ALL"])):
        p = subprocess.run(["uvx", RUFF, "check", "--no-cache", "--output-format", "json", *extra, str(PROGRAMS)],
                           capture_output=True, text=True)
        (OUT / f"{name}.json").write_text(p.stdout)
    with tempfile.TemporaryDirectory() as tmp:  # pyrefly checks a plain copy (no project config of the benchmark)
        for f in PROGRAMS.glob("*.py"):
            shutil.copy(f, tmp)
        p = subprocess.run(["uvx", PYREFLY, "check", "--output-format", "json", "."], cwd=tmp,
                           capture_output=True, text=True)
        (OUT / "pyrefly.json").write_text(p.stdout)
    (OUT / "versions.json").write_text(json.dumps({"ruff": RUFF, "pyrefly": PYREFLY}, indent=1) + "\n")


def parse_ruff(data: list) -> dict[str, list[tuple[int, str]]]:
    out = defaultdict(list)
    for d in data:
        out[Path(d["filename"]).stem].append((d["location"]["row"], d["code"]))
    return dict(out)


def parse_pyrefly(data: dict) -> dict[str, list[tuple[int, str]]]:
    out = defaultdict(list)
    for d in data["errors"]:
        out[Path(d["path"]).stem].append((d["line"], d["name"]))
    return dict(out)


def score(diags: dict, gt: dict, code_lines: dict | None = None) -> dict:
    """code_lines: program → number of non-blank lines; gives the hits expected if the flagged lines were random."""
    progs = list(gt)
    near = lambda p, d: any(abs(r - g) <= d for r, _ in diags.get(p, []) for g in gt[p])
    n = sum(len(diags.get(p, [])) for p in progs)
    return {"programs": len(progs), "diagnostics": n, "flagged": sum(bool(diags.get(p)) for p in progs),
            "on_fault_line": sum(near(p, 0) for p in progs), "within_2_lines": sum(near(p, 2) for p in progs),
            "mean_per_program": round(n / len(progs), 2),
            "on_fault_line_by_chance": round(sum(min(1.0, len({r for r, _ in diags.get(p, [])}) * len(gt[p]) / code_lines[p])
                                                 for p in progs), 1) if code_lines else ""}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if args.run:
        run_tools()
    diags = {"ruff_default": parse_ruff(json.loads((OUT / "ruff_default.json").read_text())),
             "ruff_all": parse_ruff(json.loads((OUT / "ruff_all.json").read_text())),
             "pyrefly": parse_pyrefly(json.loads((OUT / "pyrefly.json").read_text()))}
    code_lines = {f.stem: sum(1 for l in f.read_text().splitlines() if l.strip()) for f in PROGRAMS.glob("*.py")}
    rows = []
    for gname, gt in load_variants().items():
        if gname == "verified_strict":
            continue
        for tool, d in diags.items():
            rows.append({"gt": gname, "tool": tool, **score(d, gt, code_lines)})
    with open(ROOT / "data" / "static_tools.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
