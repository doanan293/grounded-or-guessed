"""Ground-truth variants for SemFault-250.

repaired_gt: original lines, replaced by execution-verified lines where verification corrected them;
             programs whose suspect ground truth could not be verified are dropped.
strict=True: only programs whose fault line was confirmed or corrected by a passing minimal fix.
sources:     program → source lines; a verified location made only of blank/comment lines is dropped (a "fix"
             written onto a blank line names no statement any method can rank — in practice a compensating insert).
"""
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT

ROOT = Path(__file__).resolve().parents[2]


def _blank(rows: list[str], lines: list[int]) -> bool:
    return all(not rows[ln - 1].strip() or rows[ln - 1].strip().startswith("#") for ln in lines if 0 < ln <= len(rows))


def repaired_gt(original: dict[str, list[int]], verified: list[dict], strict: bool = False,
                sources: dict[str, list[str]] | None = None) -> dict[str, list[int]]:
    by = {v["program"]: v for v in verified}
    out = {}
    for p, lines in original.items():
        v = by.get(p)
        status = v["status"] if v else "unverified"
        if status == "unverifiable" or (strict and status not in ("confirmed", "corrected")):
            continue
        chosen = list(v["lines"]) if v and status in ("confirmed", "corrected") else list(lines)
        if sources is not None and p in sources and status in ("confirmed", "corrected") and _blank(sources[p], chosen):
            continue
        out[p] = chosen
    return out


def load_variants() -> dict[str, dict[str, list[int]]]:
    from flx.semloc_results import load_ground_truth
    original = load_ground_truth(SEMLOC_ROOT / "benchmark" / "ground_truth.json")
    verified = json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
    sources = {p: (SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py").read_text().splitlines() for p in original}
    return {"original": original, "repaired": repaired_gt(original, verified, sources=sources),
            "verified_strict": repaired_gt(original, verified, strict=True, sources=sources)}
