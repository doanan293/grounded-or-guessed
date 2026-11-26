"""Check that every number written as `value [`\\Macro`]` in a document equals that macro in numbers-vi.tex.

    python scripts/check_claims.py [--fix] docs/analysis/contributions.md [more.md ...]
--fix rewrites every cited value from the macros first (run after scripts/regenerate_all.sh).
Exit 1 and list each mismatch (macro, written, generated). Unicode minus and a leading + are normalized.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM = re.compile(r"([−+-]?\d+(?:[.,]\d+)?)\s*\[`(\\[A-Za-z]+)`\]")


def load_macros(path: Path) -> dict[str, str]:
    return dict(re.findall(r"\\newcommand\{(\\[A-Za-z]+)\}\{([^}]*)\}", path.read_text()))


def _num(s: str) -> float:
    return float(s.replace("−", "-").replace(",", ".").replace("$<$", ""))


def mismatches(text: str, macros: dict[str, str]) -> list[tuple]:
    out = []
    for value, name in CLAIM.findall(text):
        gen = macros.get(name)
        if gen is None or _num(value) != _num(gen):
            out.append((name, value, gen))
    return out


def fix(text: str, macros: dict[str, str]) -> str:
    """Rewrite each `value [`\\Macro`]` with the generated value (typographic minus for negatives)."""
    def sub(m):
        gen = macros.get(m.group(2))
        if gen is None:
            return m.group(0)
        return f"{gen.replace('$<$', '<').replace('-', '−')} [`{m.group(2)}`]"
    return CLAIM.sub(sub, text)


def main() -> None:
    macros = load_macros(ROOT / "docs" / "report" / "generated" / "numbers-vi.tex")
    files = [a for a in sys.argv[1:] if a != "--fix"]
    if "--fix" in sys.argv:
        for f in files:
            Path(f).write_text(fix(Path(f).read_text(), macros))
    bad, n = [], 0
    for f in files:
        text = Path(f).read_text()
        n += len(CLAIM.findall(text))
        bad += [(f, *m) for m in mismatches(text, macros)]
    for b in bad:
        print("MISMATCH", *b)
    print(f"{n} claims checked, {len(bad)} mismatches")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
