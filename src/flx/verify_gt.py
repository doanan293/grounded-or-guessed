"""SemFault-250-verified: ground truth re-derived by execution.

A line is a verified fault location if replacing it with one line (or filling a blank line, which is
how an omission fault is fixed) makes every test pass. The LLM only proposes candidate lines of code;
the test suite decides. Statuses:
  confirmed    a minimal one-line fix (few tokens, see is_minimal) at an original ground-truth line passes all tests
  corrected    the original line could not be fixed, but a minimal fix at nearby line(s) inside the target
               function passes all tests (searched only when the original line is not executed by
               any failing test, i.e. the ground truth is suspect)
  unverified   executable ground truth, but no proposed fix at it passed (does not mean it is wrong)
  unverifiable suspect ground truth and no candidate line could be fixed
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

from flx._semloc import SEMLOC_ROOT

Propose = Callable[[str, int, str], list[dict]]  # (numbered function source, line, failing summary) → [{"kind","code"}]


def _function_span(src: str, fn: str) -> tuple[int, int]:
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == fn:
            return node.lineno, node.end_lineno
    raise ValueError(f"function {fn!r} not found")


def candidates(src: str, fn: str, gt_line: int, radius: int = 4) -> list[int]:
    """Body lines of `fn` within ±radius of gt_line (blank lines included: an omission is fixed there)."""
    start, end = _function_span(src, fn)
    return [ln for ln in range(max(start + 1, gt_line - radius), min(end, gt_line + radius) + 1)]


def _indent_for(lines: list[str], line: int) -> str:
    for ln in [line] + list(range(line + 1, len(lines) + 1)) + list(range(line - 1, 0, -1)):
        text = lines[ln - 1]
        if text.strip():
            return text[: len(text) - len(text.lstrip())]
    return ""


def apply(src: str, line: int, kind: str, code: str) -> str:
    lines = src.splitlines()
    new = _indent_for(lines, line) + code.strip()
    if kind == "replace":
        lines[line - 1] = new
    elif kind == "insert_after":
        lines.insert(line, new)
    else:
        raise ValueError(kind)
    return "\n".join(lines) + "\n"


def _run_tests(program_src: str, prog_path: Path, test_path: Path, timeout: int = 120) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "programs").mkdir()
        (Path(tmp) / "testcases").mkdir()
        (Path(tmp) / "programs" / Path(prog_path).name).write_text(program_src)
        shutil.copy(test_path, Path(tmp) / "testcases" / Path(test_path).name)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SEMLOC_ROOT / "src")
        try:
            return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "conftest", "--tb=line",
                                   "-p", "no:cacheprovider", str(Path(tmp) / "testcases" / Path(test_path).name)],
                                  cwd=SEMLOC_ROOT / "src", env=env, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess([], 124, "", "timeout")


def try_patch(src: str, line: int, kind: str, code: str, prog_path: Path, test_path: Path) -> bool:
    try:
        patched = apply(src, line, kind, code)
        ast.parse(patched)
    except (SyntaxError, IndexError, ValueError):
        return False
    return _run_tests(patched, prog_path, test_path).returncode == 0


def failing_summary(prog_path: Path, test_path: Path) -> str:
    out = _run_tests(Path(prog_path).read_text(), prog_path, test_path)
    lines = [l for l in (out.stdout + out.stderr).splitlines() if "Error" in l or "assert" in l or "FAILED" in l]
    return "\n".join(lines[:15])


def _tokens(line: str) -> list[str]:
    return re.findall(r"\w+|[^\w\s]", line)


def edit_size(original: str, patched: str) -> int:
    """Token-level Levenshtein distance between a source line and its replacement."""
    a, b = _tokens(original), _tokens(patched)
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def is_minimal(original: str, patched: str) -> bool:
    """Injected faults change a few tokens: accept ≤ 2 token edits or ≤ 1/3 of the line; on a blank
    line (omission fault) accept one short statement (≤ 12 tokens)."""
    if not original.strip():
        return len(_tokens(patched)) <= 12
    e = edit_size(original, patched)
    return e <= 2 or e <= max(len(_tokens(original)), len(_tokens(patched))) / 3


def verify(program: str, prog_path: Path, test_path: Path, fn: str, gt_lines: list[int], propose: Propose,
           executable: bool, radius: int = 4) -> dict:
    src = Path(prog_path).read_text()
    src_lines = src.splitlines()
    numbered = "\n".join(f"{i + 1}: {l}" for i, l in enumerate(src_lines))
    failing = failing_summary(prog_path, test_path)

    def best_fix(line: int):
        """Smallest passing minimal fix proposed for `line`, as (edit_size, proposal) or None."""
        original = src_lines[line - 1] if line - 1 < len(src_lines) else ""
        found = []
        for prop in propose(numbered, line, failing):
            code, kind = prop.get("code", ""), prop.get("kind", "replace")
            base = "" if kind == "insert_after" else original
            if is_minimal(base, code) and try_patch(src, line, kind, code, prog_path, test_path):
                found.append((edit_size(base, code) if base.strip() else len(_tokens(code)), prop))
        return min(found, key=lambda x: x[0]) if found else None

    def pick(lines: list[int]):
        fixes = {ln: f for ln in lines if (f := best_fix(ln))}
        if not fixes:
            return None
        e = min(f[0] for f in fixes.values())
        best = sorted(ln for ln, f in fixes.items() if f[0] == e)
        return best, e, fixes[best[0]][1]

    hit = pick(list(gt_lines))
    if hit:
        return {"program": program, "status": "confirmed", "lines": hit[0], "edit_size": hit[1], **hit[2]}
    if executable:
        return {"program": program, "status": "unverified", "lines": list(gt_lines)}
    near = sorted({c for g in gt_lines for c in candidates(src, fn, g, radius) if c not in gt_lines})
    hit = pick(near)
    if hit:
        return {"program": program, "status": "corrected", "lines": hit[0], "original": list(gt_lines),
                "edit_size": hit[1], **hit[2]}
    return {"program": program, "status": "unverifiable", "lines": list(gt_lines)}


def llm_propose(model: str, attempts: int = 2, strict: bool = False) -> Propose:
    """LLM proposer through the flx gateway: one call per attempt; the reply must be JSON.

    strict=True re-raises failed calls (quota, network) instead of skipping the attempt, so a caller can retry the
    program later rather than record "no passing fix"; the label oracle keeps the lenient default."""
    from flx.llm_gateway import chat
    system = ("You fix one-line bugs in Python. Reply with JSON only: "
              '{"kind": "replace" | "insert_after", "code": "<one line of Python, no indentation>"}')

    def propose(numbered: str, line: int, failing: str) -> list[dict]:
        out = []
        for k in range(attempts):
            user = (f"Program (line-numbered):\n{numbered}\n\nFailing tests:\n{failing}\n\n"
                    f"Assume the bug is at line {line}. Give the single line that should replace line {line} "
                    f"(or, if code is missing, the line to insert after line {line}) so that all tests pass. "
                    f"Make the smallest possible change (ideally one or two tokens) and keep everything else identical. "
                    f"Attempt {k + 1}.")
            try:
                text = chat(model, system, user, temperature=0.8)
            except Exception:
                if strict:
                    raise
                continue
            m = re.search(r"\{.*\}", text, re.S)
            try:
                prop = json.loads(m.group(0)) if m else None
            except json.JSONDecodeError:
                prop = None
            if isinstance(prop, dict) and isinstance(prop.get("code"), str):
                out.append({"kind": prop.get("kind", "replace"), "code": prop["code"]})
        return out
    return propose
