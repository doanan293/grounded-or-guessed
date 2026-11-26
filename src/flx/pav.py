"""Propose-and-verify (PAV) fault localization: the LLM proposes, the test suite decides.

Stage 1 (propose): the single-prompt baseline with failing tests (flx.direct_cov, coverage=False) ranks up to five
lines. Stage 2 (verify): for each of the first k candidates the LLM proposes a minimal one-line fix *at that line*
(flx.verify_gt.llm_propose); the patched program is run against the tests. Candidates with a passing minimal fix
move to the front, in the LLM's order (order="llm") or by edit size (order="size"); the rest keep the LLM's order.

Every attempt is recorded (Check), so the knobs k, attempts and order can be selected on the dev split offline,
from one run, without new LLM calls.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from flx.verify_gt import Propose, _tokens, apply, edit_size, is_minimal

Passes = Callable[[str, int, str, str], bool]  # (source, line, kind, code) → all tests pass


@dataclass(frozen=True)
class Check:
    passed: bool
    size: int | None  # token edit size of the passing fix; None if it failed or was not minimal


def verify_candidates(src: str, candidates: list[int], k: int, propose: Propose, passes: Passes,
                      failing: str = "") -> dict[int, list[Check]]:
    lines = src.splitlines()
    numbered = "\n".join(f"{i + 1}: {l}" for i, l in enumerate(lines))
    out = {}
    for line in candidates[:k]:
        if not 0 < line <= len(lines):
            out[line] = []
            continue
        checks = []
        for prop in propose(numbered, line, failing):
            code, kind = prop.get("code", ""), prop.get("kind", "replace")
            base = "" if kind == "insert_after" else lines[line - 1]
            ok = is_minimal(base, code) and passes(src, line, kind, code)
            size = (edit_size(base, code) if base.strip() else len(_tokens(code))) if ok else None
            checks.append(Check(ok, size))
        out[line] = checks
    return out


def rank(candidates: list[int], checks: dict[int, list[Check]], k: int, attempts: int, order: str,
         max_size: int | None = None) -> list[int]:
    """Verified candidates (among the first k, within the first `attempts` attempts, fix of at most `max_size`
    tokens) first, then the rest. A small `max_size` guards against compensating fixes."""
    best = {}
    for pos, line in enumerate(candidates[:k]):
        sizes = [c.size for c in checks.get(line, [])[:attempts]
                 if c.passed and (max_size is None or c.size <= max_size)]
        if sizes:
            best[line] = (min(sizes), pos)
    key = (lambda ln: best[ln][1]) if order == "llm" else (lambda ln: best[ln])
    verified = sorted(best, key=key)
    return verified + [ln for ln in candidates if ln not in best]


def run(program: str, bench: Path, stage1: list[int], model: str, k: int = 3, attempts: int = 2) -> dict:
    """Stage 2 for one SemFault program; returns the per-candidate checks as JSON-able data."""
    from flx.verify_gt import _run_tests, failing_summary, llm_propose
    prog, test = bench / "programs" / f"{program}.py", bench / "testcases" / f"test_{program}.py"
    src = prog.read_text()

    def passes(src_: str, line: int, kind: str, code: str) -> bool:
        import ast
        try:
            patched = apply(src_, line, kind, code)
            ast.parse(patched)
        except (SyntaxError, IndexError, ValueError):
            return False
        return _run_tests(patched, prog, test).returncode == 0

    checks = verify_candidates(src, stage1, k, llm_propose(model, attempts=attempts, strict=True), passes,
                               failing=failing_summary(prog, test))
    return {"stage1": stage1, "checks": {str(ln): [[c.passed, c.size] for c in cs] for ln, cs in checks.items()}}
