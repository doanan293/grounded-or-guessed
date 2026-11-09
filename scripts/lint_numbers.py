"""Flag hand-typed numbers in the report / paper sources: every decimal or percentage must be a macro from
docs/report/generated/numbers{,-vi}.tex (spec §9: no claim without data behind it).

    python scripts/lint_numbers.py docs/report/vi docs/report/paper-en
Flags decimals (52,3 / 92.0) and percentages (15\\%) in text. Ignored: comments, \\cite/\\ref/\\label/\\input/
\\include*/\\href/\\url arguments, optional arguments [..], TeX lengths (2.5pt, 1.5cm), version strings in the form
"phiên bản 3.12"/"version 3.12"/"Python 3.12", and the generated/ directory. Integers (counts, RQ numbers, years)
are allowed.
"""
import re
import sys
from pathlib import Path

STRIP = [
    (re.compile(r"(?<!\\)%.*"), ""),                                            # comments
    (re.compile(r"\\(?:cite[tp]?|ref|eqref|label|input|include|includegraphics|href|url|autoref|cref)\*?"
                r"(?:\[[^\]]*\])*\{[^}]*\}"), " "),
    (re.compile(r"\[[^\]\n]*\]"), " "),                                          # optional args
    (re.compile(r"\\(?:setstretch|linespread|arraystretch|renewcommand\{\\arraystretch\})\{[^}]*\}"), " "),  # spacing
    (re.compile(r"(?i)(?:apache|gpl|lgpl|cc-by)-\d+(?:\.\d+)*"), " "),                    # licence names
    (re.compile(r"\d+(?:[.,]\d+)?\s*(?:pt|cm|mm|em|ex|in|bp|sp|\\linewidth|\\textwidth|\\columnwidth)"), " "),
    (re.compile(r"(?i)(?:phiên bản|version|python|v)\s*\d+(?:\.\d+)+"), " "),
    (re.compile(r"(?i)(?:kỳ|semester)\s*\d{4}[.,]\d"), " "),
    (re.compile(r"(?i)(?:sonnet|opus|haiku|gemini|gpt|claude)[- ]?\d+(?:\.\d+)+"), " "),        # model names                    # semester label, e.g. học kỳ 2026.1
]
NUMBER = re.compile(r"(?<![\w.\\])(?:\d+(?:[.,]\d+)?\s*\\%|\d+[.,]\d+(?![\w.]))")  # a percentage, or a decimal


def lint(tex: str) -> list[str]:
    out = []
    for i, line in enumerate(tex.splitlines(), 1):
        s = line
        for rx, rep in STRIP:
            s = rx.sub(rep, s)
        for m in NUMBER.finditer(s):
            out.append(f"line {i}: {m.group(0)!r}")
    return out


def main() -> None:
    bad = 0
    for root in sys.argv[1:]:
        for f in sorted(Path(root).rglob("*.tex")):
            if "generated" in f.parts:
                continue
            for msg in lint(f.read_text()):
                print(f"{f}: {msg}")
                bad += 1
    print(f"{bad} hand-typed number(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
