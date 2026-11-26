import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("drop_versions", ROOT / "scripts" / "drop_versions.py")
dv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dv)


def test_resolves_the_three_macros_to_the_final_version():
    assert dv.resolve(r"a \IfAtLeast{lan2}{X} b") == "a X b"
    assert dv.resolve(r"\IfAtLeastElse{full}{Y}{N}") == "Y"
    assert dv.resolve(r"x\IfBelow{full}{P}y") == "xy"


def test_nested_braces_and_nested_macros():
    assert dv.resolve(r"\IfAtLeast{lan2}{a {b} \IfAtLeastElse{full}{c}{d} e}") == "a {b} c e"
    assert dv.resolve("\\IfAtLeast{lan2}{%\nline\n}") == "%\nline\n"


def test_leaves_other_text_alone():
    s = r"\section{A} 1 & 2 \\ \emph{x}"
    assert dv.resolve(s) == s
