"""Package the run outputs, LLM call log and LLM response cache for the archival release (Zenodo).

    python scripts/export_artifact.py --out dist/
Writes dist/grounded-or-guessed-runs-<YYYYMMDD>.tar.gz with, for every healthy run listed in data/runs.csv:
  runs/<semloc run>/{scores,refined_base_cf,constraints,results_cf_base}/, runs/bip_semloc/<run>/,
  runs/<single-prompt run>.json, runs/llm_log.jsonl (those run ids only), runs/llm_cache/<key>.json (keys of
  successful calls in that log), and MANIFEST.json (sha256 per file). With the cache in place and FLX_LLM_OFFLINE=1,
  every LLM call of these runs replays without network access. Refuses to write the archive if any file matches
  flx.secrets_scan.
"""
import argparse
import csv
import hashlib
import io
import json
import sys
import tarfile
import time
from pathlib import Path

from flx.secrets_scan import scan

ROOT = Path(__file__).resolve().parents[1]
SEMLOC_PARTS = ("scores", "refined_base_cf", "constraints", "results_cf_base")


def collect() -> dict[str, bytes]:
    """Archive path → bytes."""
    with open(ROOT / "data" / "runs.csv") as f:
        runs = [r for r in csv.DictReader(f) if r["healthy"] == "True" and r["finished"] == "True"]
    ids = {r["run_id"] for r in runs}
    files: dict[str, bytes] = {}
    for r in runs:
        rid = r["run_id"]
        if r["kind"] == "semloc":
            for part in SEMLOC_PARTS:
                for p in sorted((ROOT / "runs" / rid / part).rglob("*")):
                    if p.is_file():
                        files[str(p.relative_to(ROOT))] = p.read_bytes()
        elif r["kind"] == "semloc_bugsinpy":
            for p in sorted((ROOT / "runs" / "bip_semloc" / rid).rglob("*")):
                if p.is_file() and not p.is_symlink():
                    files[str(p.relative_to(ROOT))] = p.read_bytes()
        else:
            p = ROOT / "runs" / f"{rid}.json"
            if p.exists():
                files[str(p.relative_to(ROOT))] = p.read_bytes()
    keep, keys = [], set()
    for line in (ROOT / "runs" / "llm_log.jsonl").read_text().splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("run_id") in ids:
            keep.append(line)
            if not rec.get("error"):
                keys.add(rec["key"])
    files["runs/llm_log.jsonl"] = ("\n".join(keep) + "\n").encode()
    for k in sorted(keys):
        c = ROOT / "runs" / "llm_cache" / f"{k}.json"
        if c.exists():
            files[f"runs/llm_cache/{k}.json"] = c.read_bytes()
    return files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    args = ap.parse_args()
    files = collect()
    leaks = {path: hits for path, data in files.items() if (hits := scan(data.decode("utf-8", "replace")))}
    if leaks:
        for path, hits in list(leaks.items())[:20]:
            print(f"SECRET? {path}: {hits}", file=sys.stderr)
        sys.exit(f"refusing to export: {len(leaks)} file(s) match secret patterns")
    manifest = {p: hashlib.sha256(d).hexdigest() for p, d in sorted(files.items())}
    files["MANIFEST.json"] = json.dumps(manifest, indent=1).encode()
    args.out.mkdir(parents=True, exist_ok=True)
    out = args.out / f"grounded-or-guessed-runs-{time.strftime('%Y%m%d')}.tar.gz"
    with tarfile.open(out, "w:gz") as tar:
        for path, data in sorted(files.items()):
            info = tarfile.TarInfo(path)
            info.size, info.mtime, info.mode = len(data), 0, 0o644
            tar.addfile(info, io.BytesIO(data))
    print(f"{out}: {len(files)} files, {out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
