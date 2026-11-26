"""RQ3a on BugsInPy (youtube-dl): SBFL and SemLoc inside the function that holds the real fault.

Target function = among the functions enclosing buggy-side lines changed by the developer fix, the first
(files with most changed lines first) that a declared failing test executes; if none is executed, the first.
Coverage: one `coverage run` of the bug's BugsInPy test file with per-test dynamic contexts, joined
with per-test outcomes from JUnit XML. Tests that fail but are not declared by BugsInPy (environment
failures on Python 3.12) are left out of the matrix. SemLoc: the artifact's own `bip_runner.run_semloc_on_bip`, with
LLM calls through the flx gateway and its `pip install -e .` disabled (the checkout goes on PYTHONPATH;
youtube-dl has no dependencies and reproduces 33/33 bugs on Python 3.12).
"""
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

from flx._semloc import ensure_on_path
from flx.bip import BIP, bug_files, source_faults

ROOT = Path(__file__).resolve().parents[2]


def enclosing_function(src: str, rel_path: str, line: int) -> Optional[tuple[str, int, int]]:
    """(qualified name, first line, last line) of the innermost function containing `line`."""
    module = rel_path.removesuffix(".py").replace("/", ".")
    best = None

    def visit(node, prefix):
        nonlocal best
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if child.lineno <= line <= child.end_lineno:
                    best = (f"{prefix}.{child.name}", child.lineno, child.end_lineno)
                visit(child, f"{prefix}.{child.name}")
            elif isinstance(child, ast.ClassDef):
                visit(child, f"{prefix}.{child.name}")

    visit(ast.parse(src), module)
    return best


def junit_id(declared: str) -> str:
    """BugsInPy test id (path::Class::test) → JUnit/coverage-context id (dotted)."""
    path, *rest = declared.split("::")
    return ".".join([path.removesuffix(".py").replace("/", "."), *rest])


def matrix_from_contexts(program: str, contexts: dict, outcomes: dict[str, bool], lines,
                         declared: Optional[set] = None) -> dict:
    """CoverageMatrix from coverage.py per-line contexts ({line: ["<test id>|run", ...]}). With `declared`,
    failing tests outside it are dropped."""
    if declared is not None:
        outcomes = {t: ok for t, ok in outcomes.items() if ok or t in declared}
    keep = set(lines)
    per_test: dict[str, set[int]] = {t: set() for t in outcomes}
    for ln, ctxs in contexts.items():
        ln = int(ln)
        if ln not in keep:
            continue
        for c in ctxs:
            tid = c.split("|")[0]
            if tid in per_test:
                per_test[tid].add(ln)
    return {"program": program, "n_empty_coverage": 0,
            "tests": [{"id": t, "passed": outcomes[t], "lines": sorted(per_test[t])} for t in sorted(outcomes)]}


def pick_target(cands: list[dict], failing_lines: dict[str, set]) -> dict:
    """First candidate a declared failing test executes (any line of the function); else the first."""
    for c in cands:
        if any(c["fn_start"] <= ln <= c["fn_end"] for ln in failing_lines.get(c["file"], ())):
            return c
    return cands[0]


def candidates(bug_id: str) -> list[dict]:
    """Every function enclosing a buggy-side changed line, files with most changed lines first."""
    ensure_on_path()
    import bip_runner
    meta = bug_files(bug_id)
    wt = BIP / "checkouts" / bug_id
    faults = source_faults(bip_runner.get_faulty_lines_from_diff(bug_id, str(wt)))
    out, seen = [], set()
    for rel, lines in sorted(faults.items(), key=lambda kv: -len(kv[1])):
        src = (wt / rel).read_text()
        for ln in sorted(lines):
            fn = enclosing_function(src, rel, ln)
            if fn and (rel, fn[0]) not in seen:
                seen.add((rel, fn[0]))
                in_fn = [l for l in lines if fn[1] <= l <= fn[2]]
                out.append({"bug": bug_id, "file": rel, "function": fn[0], "fn_start": fn[1], "fn_end": fn[2],
                            "faulty_lines": in_fn, "test_file": meta["info"].get("test_file", ""), "tests": meta["tests"]})
    return out


def target(bug_id: str) -> Optional[dict]:
    cands = candidates(bug_id)
    if len(cands) <= 1:
        return cands[0] if cands else None
    files, outcomes = _coverage_run(cands[0])
    declared = {junit_id(t) for t in cands[0]["tests"]}
    failing = {t for t, ok in outcomes.items() if not ok and t in declared}
    failing_lines = {rel: {int(ln) for ln, ctxs in f.get("contexts", {}).items()
                           if any(c.split("|")[0] in failing for c in ctxs)} for rel, f in files.items()}
    return pick_target(cands, failing_lines)


def _coverage_run(tgt: dict) -> tuple[dict, dict]:
    """(coverage.py per-file data keyed by checkout-relative path, JUnit outcomes) for the bug's test file(s)."""
    wt = BIP / "checkouts" / tgt["bug"]
    test_files = [t.strip() for t in tgt["test_file"].split(";") if t.strip()]
    with tempfile.TemporaryDirectory() as tmp:
        rc = Path(tmp) / "covrc"
        rc.write_text(f"[run]\ndynamic_context = test_function\ndata_file = {tmp}/.cov\nsource = {wt}\n")
        ini = Path(tmp) / "pytest.ini"  # isolate from this repo's pyproject: test ids must be checkout-relative
        ini.write_text("[pytest]\n")
        junit = Path(tmp) / "j.xml"
        env = {**os.environ, "PYTHONPATH": str(wt), "COVERAGE_RCFILE": str(rc)}
        subprocess.run([sys.executable, "-m", "coverage", "run", "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider",
                        "-c", str(ini), f"--rootdir={wt}", f"--junitxml={junit}", *test_files],
                       cwd=wt, env=env, capture_output=True, timeout=3600)
        subprocess.run([sys.executable, "-m", "coverage", "json", "--show-contexts", "-o", f"{tmp}/c.json"],
                       cwd=wt, env=env, capture_output=True)
        cov = json.loads(Path(f"{tmp}/c.json").read_text())
        outcomes = {}
        for case in ET.parse(junit).getroot().iter("testcase"):
            if case.find("skipped") is not None:
                continue
            failed = case.find("failure") is not None or case.find("error") is not None
            outcomes[f"{case.get('classname')}.{case.get('name')}"] = not failed
    files = {os.path.relpath(os.path.join(wt, k), wt): v for k, v in cov.get("files", {}).items()}
    return files, outcomes


def coverage_matrix(tgt: dict) -> dict:
    files, outcomes = _coverage_run(tgt)
    contexts = files.get(tgt["file"], {}).get("contexts", {})
    return matrix_from_contexts(tgt["bug"], contexts, outcomes, range(tgt["fn_start"], tgt["fn_end"] + 1),
                                declared={junit_id(t) for t in tgt["tests"]})


def run_semloc(tgt: dict, model: str, temperature: float, run_id: str) -> dict:
    """SemLoc's own BugsInPy pipeline on the target function; returns its result dict."""
    ensure_on_path()
    import bip_runner
    bip_runner.install_project = lambda checkout_dir: True  # never pip-install into our venv
    wt = BIP / "checkouts" / tgt["bug"]
    # SemLoc's CF step patches the target file and restores it within the same second; a same-size patch
    # leaves bytecode whose header still matches, so later runs would import the patched code. Start
    # every run without bytecode and never write any.
    for cache in wt.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)
    sys.dont_write_bytecode = True
    os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "FLX_USE_GATEWAY": "1", "FLX_RUN_ID": run_id,
                       "PYTHONPATH": str(wt) + os.pathsep + os.environ.get("PYTHONPATH", "")})
    workdir = ROOT / "runs" / "bip_semloc" / run_id / tgt["bug"]
    test_file = tgt["test_file"].split(";")[0].strip()
    return bip_runner.run_semloc_on_bip(tgt["bug"], tgt["function"], str(wt), test_file, model=model,
                                        temperature=temperature, workdir=str(workdir))
