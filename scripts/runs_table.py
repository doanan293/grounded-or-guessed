"""Registry of experiment runs → data/runs.csv (run_id, model, split, n, finished, calls, tokens, healthy).

    python scripts/runs_table.py
SemLoc runs: finished = results_cf_base/summary.json exists; healthy = flx.run_health. Single-prompt baselines
(data/rankings/<run_id>.json or runs/<run_id>.json) and BugsInPy runs: finished = every program has output.
"""
import csv
import json
from pathlib import Path

from flx.cost import run_costs
from flx.run_health import health

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runs" / "llm_log.jsonl"


def split_of(run: str) -> str:
    for key, name in (("_test_", "test"), ("_sub50_", "subset50"), ("_dev_", "dev"), ("_renamed_", "renamed-test"),
                      ("bip_", "bugsinpy")):
        if key in run:
            return name
    return "?"


def split_size(split: str) -> int | None:
    """Programs a run of this split must cover (from the split definitions, not from a workdir)."""
    d = ROOT / "data"
    return {"test": 200, "dev": len(json.loads((d / "split.json").read_text())["dev"]),
            "subset50": len(json.loads((d / "subset50.json").read_text())["programs"]),
            "bugsinpy": len(json.loads((d / "bugsinpy_targets.json").read_text())),
            "renamed-test": len(json.loads((d / "semfault_renamed" / "test_programs.json").read_text()))}.get(split)


def main() -> None:
    costs = run_costs(LOG)
    models = {}
    for line in open(LOG):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        models.setdefault(r.get("run_id"), r.get("served_model") or r.get("model"))
    rows = []
    for wd in sorted((ROOT / "runs").glob("semloc_*_r[0-9]")):
        n = split_size(split_of(wd.name))
        h = health(wd, wd.name, LOG)
        rows.append({"run_id": wd.name, "kind": "semloc", "split": split_of(wd.name), "n": n,
                     "finished": (wd / "results_cf_base" / "summary.json").exists(), "healthy": h["healthy"]})
    for f in sorted([*(ROOT / "data" / "rankings").glob("direct*_r[0-9].json"), *(ROOT / "runs").glob("direct*_r[0-9].json")]):
        if any(r["run_id"] == f.stem for r in rows):
            continue
        n = split_size(split_of(f.stem))
        done = len(json.loads(f.read_text()))
        rows.append({"run_id": f.stem, "kind": "single_prompt", "split": split_of(f.stem), "n": n,
                     "finished": done == n, "healthy": done == n})
    targets = json.loads((ROOT / "data" / "bugsinpy_targets.json").read_text())
    for d in sorted((ROOT / "runs" / "bip_semloc").glob("bip_semloc_gemini_r[0-9]")):
        outs = [json.loads((d / f"{b}.json").read_text()) for b in targets if (d / f"{b}.json").exists()]
        errs = sum("error" in o for o in outs)
        rows.append({"run_id": d.name, "kind": "semloc_bugsinpy", "split": "bugsinpy", "n": len(targets),
                     "finished": len(outs) == len(targets), "healthy": len(outs) == len(targets),
                     "note": f"{errs} bug(s) with a SemLoc error, scored as misses" if errs else ""})
    for r in rows:
        c = costs.get(r["run_id"], {})
        r["model"] = models.get(r["run_id"], "")
        r["calls"] = c.get("calls", 0)
        r["tokens"] = c.get("prompt_tokens", 0) + c.get("completion_tokens", 0)
        r.setdefault("note", "")
    fields = ["run_id", "kind", "model", "split", "n", "finished", "healthy", "calls", "tokens", "note"]
    with open(ROOT / "data" / "runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(*(r[k] for k in fields))


if __name__ == "__main__":
    main()
