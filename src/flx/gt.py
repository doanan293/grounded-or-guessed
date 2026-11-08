"""Ground-truth variants for SemFault-250.

repaired_gt: original lines, replaced by execution-verified lines where verification corrected them;
             programs whose suspect ground truth could not be verified are dropped.
strict=True: only programs whose fault line was confirmed or corrected by a passing minimal fix.
"""
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT

ROOT = Path(__file__).resolve().parents[2]


def repaired_gt(original: dict[str, list[int]], verified: list[dict], strict: bool = False) -> dict[str, list[int]]:
    by = {v["program"]: v for v in verified}
    out = {}
    for p, lines in original.items():
        v = by.get(p)
        status = v["status"] if v else "unverified"
        if status == "unverifiable" or (strict and status not in ("confirmed", "corrected")):
            continue
        out[p] = list(v["lines"]) if v and status in ("confirmed", "corrected") else list(lines)
    return out


def load_variants() -> dict[str, dict[str, list[int]]]:
    from flx.semloc_results import load_ground_truth
    original = load_ground_truth(SEMLOC_ROOT / "benchmark" / "ground_truth.json")
    verified = json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
    return {"original": original, "repaired": repaired_gt(original, verified),
            "verified_strict": repaired_gt(original, verified, strict=True)}
