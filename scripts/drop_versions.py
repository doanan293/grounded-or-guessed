"""One-off: turn the staged LaTeX sources into the final version only (2026-11-18, owner: one final report).

\\IfAtLeast{v}{A} -> A, \\IfAtLeastElse{v}{A}{B} -> A, \\IfBelow{v}{A} -> "" (nested braces and nested macros handled).
    .venv/bin/python scripts/drop_versions.py FILE...    (rewrites the files in place)
"""
import sys
from pathlib import Path

MACROS = {"\\IfAtLeastElse": (3, 1), "\\IfAtLeast": (2, 1), "\\IfBelow": (2, None)}  # name -> (n args, kept arg)


def _group(s: str, i: int) -> tuple[str, int]:
    """Balanced {...} starting at s[i] == '{' (whitespace before it skipped); returns (inside, index after)."""
    while s[i] in " \t\n":
        i += 1
    assert s[i] == "{", s[i:i + 30]
    depth, j = 0, i
    while True:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1


def resolve(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        hit = next((m for m in MACROS if s.startswith(m, i) and not s[i + len(m):i + len(m) + 1].isalpha()), None)
        if hit is None:
            out.append(s[i])
            i += 1
            continue
        n, keep = MACROS[hit]
        j = i + len(hit)
        args = []
        for _ in range(n):
            a, j = _group(s, j)
            args.append(a)
        out.append(resolve(args[keep]) if keep is not None else "")
        i = j
    return "".join(out)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        p = Path(f)
        p.write_text(resolve(p.read_text()))
