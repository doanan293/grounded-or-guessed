"""Check that every number written as `value [`\\Macro`]` in a document equals that macro in numbers-vi.tex.

    python scripts/check_claims.py docs/analysis/contributions.md [more.md ...]
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


def main() -> None:
    macros = load_macros(ROOT / "docs" / "report" / "generated" / "numbers-vi.tex")
    bad, n = [], 0
    for f in sys.argv[1:]:
        text = Path(f).read_text()
        n += len(CLAIM.findall(text))
        bad += [(f, *m) for m in mismatches(text, macros)]
    for b in bad:
        print("MISMATCH", *b)
    print(f"{n} claims checked, {len(bad)} mismatches")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
