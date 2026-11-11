"""Build a SemLoc working directory holding a subset of the benchmark (as symlinks)."""
import json
from pathlib import Path


def _link(src: Path, dst: Path) -> None:
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    dst.symlink_to(src.resolve())


def make_workdir(benchmark: Path, programs: list[str], out: Path) -> None:
    benchmark, out = Path(benchmark), Path(out)
    (out / "programs").mkdir(parents=True, exist_ok=True)
    (out / "testcases").mkdir(parents=True, exist_ok=True)
    for p in programs:
        _link(benchmark / "programs" / f"{p}.py", out / "programs" / f"{p}.py")
        _link(benchmark / "testcases" / f"test_{p}.py", out / "testcases" / f"test_{p}.py")
    keep = set(programs)
    gt = json.loads((benchmark / "ground_truth.json").read_text())
    gt["programs"] = [e for e in gt["programs"] if e["file"].removesuffix(".py") in keep]
    (out / "ground_truth.json").write_text(json.dumps(gt, indent=2))


def program_source(run: Path, program: str, root: Path | None = None) -> Path:
    """The source a run analysed: its own programs/ entry when present, else the benchmark copy it was built from
    (data/semfault_renamed for renamed-program runs) — archived runs ship without the programs/ symlinks."""
    root = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    own = Path(run) / "programs" / f"{program}.py"
    if own.exists():
        return own
    bench = root / "data" / "semfault_renamed" if "_renamed_" in Path(run).name else root / "third_party" / "semloc" / "benchmark"
    return bench / "programs" / f"{program}.py"
