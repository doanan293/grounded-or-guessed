"""Baseline 2b: one LLM call with the program, the failing tests and per-line coverage evidence.

Each source line is annotated with [f=<failing tests that execute it>/p=<passing tests>]; the model
returns its five most suspicious lines as JSON. Answers the question "is SemLoc's multi-stage pipeline
needed, or does a single prompt with execution evidence do as well?"
"""
import json
import re
from pathlib import Path

from flx.sbfl import counts

SYSTEM = ("You are a fault-localization assistant. Reply with JSON only: "
          '{"lines": [<line numbers, most suspicious first, at most 5>]}')


def build_prompt(src: str, failing: list[dict], cov: dict, first_line: int = 1) -> str:
    """`first_line` numbers `src` from that line (a function cut out of a larger file keeps absolute numbers)."""
    ef, ep, _ = counts(cov)
    numbered = "\n".join(f"{i}: {line}   [f={ef.get(i, 0)}/p={ep.get(i, 0)}]"
                         for i, line in enumerate(src.splitlines(), first_line))
    fails = "\n".join(f"- {t['name']}: {t.get('error', '')}" for t in failing)
    n_fail = sum(1 for t in cov["tests"] if not t["passed"])
    n_pass = len(cov["tests"]) - n_fail
    return (f"The program below has exactly one faulty line. {n_fail} tests fail and {n_pass} pass.\n"
            f"Each line is annotated with [f=<number of failing tests that execute it>/p=<number of passing tests>].\n\n"
            f"{numbered}\n\nFailing tests:\n{fails}\n\n"
            "Return the five most suspicious line numbers, most suspicious first.")


def parse_ranking(text: str) -> list[int]:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return []
    try:
        lines = json.loads(m.group(0)).get("lines")
    except (json.JSONDecodeError, AttributeError):
        return []
    if not isinstance(lines, list):
        return []
    out = []
    for x in lines:
        if isinstance(x, int) and x not in out:
            out.append(x)
    return out[:5]


def failing_tests(src: str, prog: Path, test: Path) -> list[dict]:
    """Names and first error line of failing tests (pytest --tb=line in an isolated layout)."""
    import os
    import shutil
    import subprocess
    import sys
    import tempfile

    from flx._semloc import SEMLOC_ROOT
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "programs").mkdir()
        (Path(tmp) / "testcases").mkdir()
        (Path(tmp) / "programs" / Path(prog).name).write_text(src)
        shutil.copy(test, Path(tmp) / "testcases" / Path(test).name)
        env = {**os.environ, "PYTHONPATH": str(SEMLOC_ROOT / "src")}
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rf", "-p", "conftest", "--tb=no",
                            "-p", "no:cacheprovider", str(Path(tmp) / "testcases" / Path(test).name)],
                           cwd=SEMLOC_ROOT / "src", env=env, capture_output=True, text=True, timeout=120)
    out = []
    for m in re.finditer(r"^FAILED \S+::(\S+)(?: - (.*))?$", p.stdout, re.M):
        out.append({"name": m.group(1), "error": (m.group(2) or "")[:200]})
    return out


def run(program: str, bench: Path, cov: dict, model: str) -> list[int]:
    from flx.llm_gateway import chat
    prog, test = bench / "programs" / f"{program}.py", bench / "testcases" / f"test_{program}.py"
    src = prog.read_text()
    text = chat(model, SYSTEM, build_prompt(src, failing_tests(src, prog, test), cov), temperature=0.8)
    return parse_ranking(text)


def parse_failed(stdout: str, declared: set[str]) -> list[dict]:
    """`FAILED path::Class::test - msg` lines of pytest -rf, kept only for declared tests (JUnit-style ids)."""
    from flx.bip_run import junit_id
    out = []
    for m in re.finditer(r"^FAILED (\S+::\S+)(?: - (.*))?$", stdout, re.M):
        tid = junit_id(m.group(1))
        if tid in declared:
            out.append({"name": tid, "error": (m.group(2) or "")[:200]})
    return out


def bip_failing_tests(tgt: dict) -> list[dict]:
    """Failing declared tests of a BugsInPy target with their first error line (one pytest run in the checkout)."""
    import os
    import subprocess
    import sys
    import tempfile

    from flx.bip import BIP
    from flx.bip_run import junit_id
    wt = BIP / "checkouts" / tgt["bug"]
    with tempfile.TemporaryDirectory() as tmp:
        ini = Path(tmp) / "pytest.ini"
        ini.write_text("[pytest]\n")
        files = [t.strip() for t in tgt["test_file"].split(";") if t.strip()]
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rf", "--tb=no", "-p", "no:cacheprovider",
                            "-c", str(ini), f"--rootdir={wt}", *files], cwd=wt, capture_output=True, text=True,
                           env={**os.environ, "PYTHONPATH": str(wt), "PYTHONDONTWRITEBYTECODE": "1"}, timeout=3600)
    return parse_failed(p.stdout, {junit_id(t) for t in tgt["tests"]})


def run_bip(tgt: dict, cov: dict, model: str) -> list[int]:
    """Baseline 2b on a BugsInPy target: the target function (absolute line numbers) + coverage + failing tests."""
    from flx.bip import BIP
    from flx.llm_gateway import chat
    lines = (BIP / "checkouts" / tgt["bug"] / tgt["file"]).read_text().splitlines()
    src = "\n".join(lines[tgt["fn_start"] - 1: tgt["fn_end"]]) + "\n"
    text = chat(model, SYSTEM, build_prompt(src, bip_failing_tests(tgt), cov, first_line=tgt["fn_start"]),
                temperature=0.8)
    return parse_ranking(text)
