"""Line-preserving surface obfuscation of a benchmark program (RQ3b memorization check).

Renames every identifier the module defines (functions, classes, parameters, locals, module constants)
to opaque names, blanks docstrings and comments, and keeps every line number, so the ground-truth line
and per-test behaviour are unchanged. Names the test file depends on (imported names and keyword
arguments it passes) are kept.
"""
import ast
import builtins
import io
import keyword
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from pathlib import Path

from flx._semloc import SEMLOC_ROOT


def keep_names(test_src: str) -> set[str]:
    """Names a test file relies on: names imported from the program module and keyword args it passes."""
    tree = ast.parse(test_src)
    imported = {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                and n.module and n.module.split(".")[0] in ("programs", "instrumented") for a in n.names}
    originals = {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                 and n.module and n.module.split(".")[0] in ("programs", "instrumented") for a in n.names}
    kwargs = {kw.arg for n in ast.walk(tree) if isinstance(n, ast.Call) for kw in n.keywords if kw.arg}
    return originals | imported | kwargs


def _defined_names(tree: ast.AST) -> list[str]:
    seen: dict[str, None] = {}

    def add(name):
        if name:
            seen.setdefault(name, None)

    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            add(n.name)
        elif isinstance(n, ast.arg):
            add(n.arg)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            add(n.id)
        elif isinstance(n, ast.ExceptHandler):
            add(n.name)
    return list(seen)


def _external_kwarg_names(tree: ast.AST, defined: set[str]) -> set[str]:
    """Keyword names passed to functions the module does not define (e.g. sorted(key=...))."""
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            local = isinstance(f, ast.Name) and f.id in defined
            if not local:
                out |= {kw.arg for kw in n.keywords if kw.arg}
    return out


def _imported(tree: ast.AST) -> set[str]:
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out |= {(a.asname or a.name).split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            out |= {a.asname or a.name for a in n.names}
    return out


def _docstring_spans(tree: ast.AST) -> set[tuple[int, int]]:
    spans = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
            first = n.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                spans.add((first.value.lineno, first.value.col_offset))
    return spans


def rename_program(src: str, keep: set[str]) -> str:
    tree = ast.parse(src)
    defined = _defined_names(tree)
    protected = (set(keep) | _imported(tree) | _external_kwarg_names(tree, set(defined))
                 | set(dir(builtins)) | set(keyword.kwlist) | {"self", "cls"})
    targets = [n for n in defined if n not in protected and not (n.startswith("__") and n.endswith("__"))]
    used = set(re.findall(r"\b\w+\b", src))
    mapping, k = {}, 0
    for name in targets:  # first-definition order → deterministic
        k += 1
        while f"v{k}" in used:
            k += 1
        mapping[name] = f"v{k}"
    docstrings = _docstring_spans(tree)

    line_starts = [0]
    for line in src.splitlines(keepends=True):
        line_starts.append(line_starts[-1] + len(line))
    off = lambda row, col: line_starts[row - 1] + col

    edits = []  # (start, end, replacement)
    prev = None
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.NAME and tok.string in mapping and not (prev and prev.string == "."):
            edits.append((off(*tok.start), off(*tok.end), mapping[tok.string]))
        elif tok.type == tokenize.COMMENT:
            edits.append((off(*tok.start), off(*tok.end), ""))
        elif tok.type == tokenize.STRING and tok.start in docstrings:
            newlines = tok.string.count("\n")
            edits.append((off(*tok.start), off(*tok.end), '"""' + "\n" * newlines + '"""'))
        if tok.type not in (tokenize.NL, tokenize.COMMENT):
            prev = tok
    out = src
    for start, end, rep in sorted(edits, reverse=True):
        out = out[:start] + rep + out[end:]
    out = "\n".join(l.rstrip() for l in out.split("\n"))  # drop whitespace left by removed comments
    ast.parse(out)
    return out


def test_outcomes(program_src: str, prog_path: Path, test_path: Path, timeout: int = 120) -> dict[str, bool]:
    """Per-test pass/fail of `program_src` against the benchmark test file (isolated temp layout)."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "programs").mkdir()
        (Path(tmp) / "testcases").mkdir()
        (Path(tmp) / "programs" / Path(prog_path).name).write_text(program_src)
        shutil.copy(test_path, Path(tmp) / "testcases" / Path(test_path).name)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SEMLOC_ROOT / "src")
        p = subprocess.run([sys.executable, "-m", "pytest", "-v", "-p", "conftest", "--tb=no", "-p", "no:cacheprovider",
                            str(Path(tmp) / "testcases" / Path(test_path).name)],
                           cwd=SEMLOC_ROOT / "src", env=env, capture_output=True, text=True, timeout=timeout)
    return {m.group(1): m.group(2) == "PASSED" for m in re.finditer(r"::(\S+) (PASSED|FAILED|ERROR)", p.stdout)}


test_outcomes.__test__ = False  # not a pytest test despite the name
