"""Per-test line coverage of one source file (the single source of truth for SBFL, labels, CovGate).

CoverageMatrix = {"program": str, "n_empty_coverage": int,
                  "tests": [{"id": str, "passed": bool, "lines": [int, ...]}, ...]}
Coverage comes from SemLoc's own baselines helpers so it matches the published SBFL numbers.
"""
import json
import os
from pathlib import Path

from flx._semloc import SEMLOC_ROOT, ensure_on_path


def collect(program: str, src: Path, test: Path) -> dict:
    ensure_on_path()
    import baselines

    repo_root = str(SEMLOC_ROOT / "src")  # holds the conftest.py the benchmark tests rely on
    abs_src = os.path.realpath(src)
    test = Path(test).resolve()  # SemLoc runs pytest with cwd=repo_root
    tests, n_empty = [], 0
    for test_id in baselines.get_test_ids(str(test), repo_root):
        passed, hit = baselines._coverage_for_test(test_id, abs_src, repo_root)
        if not passed and not hit:
            # upstream turns its 30 s timeout into (False, {}): retry once so load cannot flip results
            passed, hit = baselines._coverage_for_test(test_id, abs_src, repo_root)
            n_empty += not passed and not hit
        tests.append({"id": test_id, "passed": bool(passed), "lines": sorted(hit)})
    return {"program": program, "n_empty_coverage": n_empty, "tests": tests}


def save(cov: dict, path: Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(cov, indent=1))


def load(path: Path) -> dict:
    return json.loads(Path(path).read_text())
