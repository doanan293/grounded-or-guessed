"""BugsInPy environments for RQ3(a): checkout, per-project virtualenv, and a status probe.

Unlike upstream SemLoc (pip install --no-deps into its own interpreter), each project gets its own
uv virtualenv with the bug's requirements, and the checkout is put on PYTHONPATH.

    python -m flx.bip status --bugs youtube-dl_13 youtube-dl_14 --out data/bugsinpy_status.csv
"""
import argparse
import csv
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from flx._semloc import ensure_on_path

ROOT = Path(__file__).resolve().parents[2]
BIP = ROOT / "runs" / "bip"
RAW = "https://raw.githubusercontent.com/soarsmu/BugsInPy/master/projects"
STATUS_FIELDS = ["bug_id", "python", "env_ok", "tests_reproduce", "sbfl_ok", "fault_reached", "note"]


def parse_run_test(text: str) -> list[str]:
    """Turn the commands in a BugsInPy run_test.sh into pytest node ids."""
    ids = []
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"python3? -m unittest(?: -\w+)* ([\w.]+)$", line)
        if m:
            parts = m.group(1).split(".")
            # module path parts are lower-case, the class is CamelCase, the method is last
            cls_idx = next((i for i, p in enumerate(parts) if p[:1].isupper()), len(parts) - 1)
            ids.append("/".join(parts[:cls_idx]) + ".py::" + "::".join(parts[cls_idx:]))
            continue
        m = re.match(r"(?:python3? -m )?pytest (\S+::\S+)", line)
        if m:
            ids.append(m.group(1))
    return ids


def _get(url: str, cache: Path) -> str:
    if cache.exists():
        return cache.read_text()
    with urllib.request.urlopen(url, timeout=30) as r:
        text = r.read().decode()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(text)
    return text


def _sh(cmd, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def bug_files(bug_id: str) -> dict:
    project, n = bug_id.rsplit("_", 1)
    c = BIP / "meta" / bug_id
    ensure_on_path()
    import bip_runner
    info = bip_runner.get_bug_info(bug_id, cache_dir=str(BIP / ".bug_info_cache"))
    run_test = _get(f"{RAW}/{project}/bugs/{n}/run_test.sh", c / "run_test.sh")
    try:
        req = _get(f"{RAW}/{project}/bugs/{n}/requirements.txt", c / "requirements.txt")
    except Exception:
        req = ""
    return {"project": project, "info": info, "tests": parse_run_test(run_test), "requirements": req}


def checkout(bug_id: str, project: str, info: dict) -> Path:
    ensure_on_path()
    import bip_runner
    repo = BIP / "repos" / project
    if not (repo / ".git").exists():
        repo.parent.mkdir(parents=True, exist_ok=True)
        _sh(["git", "clone", "-q", bip_runner.PROJECT_REPOS[project], str(repo)], check=True)
    wt = BIP / "checkouts" / bug_id
    if not wt.exists():
        _sh(["git", "-C", str(repo), "worktree", "add", "-f", "--detach", str(wt), info["buggy_commit_id"]], check=True)
        if info.get("test_file") and info.get("fixed_commit_id"):
            for tf in info["test_file"].split(";"):
                _sh(["git", "-C", str(wt), "checkout", info["fixed_commit_id"], "--", tf.strip()])
    return wt


def venv_for(project: str, python_version: str, requirements: str) -> Path:
    major, minor = (int(x) for x in python_version.split(".")[:2])
    py = f"{major}.{max(minor, 8)}" if major == 3 else "3.8"
    venv = BIP / "venvs" / f"{project}-py{py}"
    pyexe = venv / "bin" / "python"
    if not pyexe.exists():
        _sh(["uv", "venv", "-q", "--python", py, str(venv)], check=True)
    _sh(["uv", "pip", "install", "-q", "--python", str(pyexe), "pytest", "coverage"], check=True)
    if requirements.strip():
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write(requirements)
        _sh(["uv", "pip", "install", "-q", "--python", str(pyexe), "-r", f.name])
        os.unlink(f.name)
    return venv


def _env(wt: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(wt)
    return env


def probe(bug_id: str) -> dict:
    row = dict.fromkeys(STATUS_FIELDS, "")
    row["bug_id"] = bug_id
    try:
        meta = bug_files(bug_id)
        row["python"] = meta["info"].get("python_version", "")
        if not meta["tests"]:
            row["note"] = "no failing test parsed from run_test.sh"
            return row
        wt = checkout(bug_id, meta["project"], meta["info"])
        venv = venv_for(meta["project"], row["python"] or "3.8", meta["requirements"])
        py = str(venv / "bin" / "python")
        col = _sh([py, "-m", "pytest", "--collect-only", "-q", *meta["tests"]], cwd=wt, env=_env(wt), timeout=300)
        row["env_ok"] = col.returncode == 0
        if not row["env_ok"]:
            row["note"] = (col.stdout + col.stderr).strip().splitlines()[-1][:160] if (col.stdout + col.stderr).strip() else "collect failed"
            return row
        run = _sh([py, "-m", "pytest", "-q", "--tb=no", *meta["tests"]], cwd=wt, env=_env(wt), timeout=600)
        row["tests_reproduce"] = run.returncode == 1  # 1 = some tests failed (not a usage/collection error)
        faulty = bip_runner_faulty_lines(bug_id, wt)
        with tempfile.TemporaryDirectory() as tmp:
            env = _env(wt) | {"COVERAGE_FILE": f"{tmp}/.cov"}
            _sh([py, "-m", "coverage", "run", "-m", "pytest", "-q", "--tb=no", meta["tests"][0]], cwd=wt, env=env, timeout=600)
            _sh([py, "-m", "coverage", "json", "-o", f"{tmp}/c.json"], cwd=wt, env=env)
            cov = json.loads(Path(f"{tmp}/c.json").read_text()) if Path(f"{tmp}/c.json").exists() else {"files": {}}
        files = {os.path.normpath(os.path.join(wt, k)): v for k, v in cov.get("files", {}).items()}
        hit = [ln for f, lines in faulty.items() for ln in lines
               if ln in set(files.get(os.path.normpath(os.path.join(wt, f)), {}).get("executed_lines", []))]
        row["sbfl_ok"] = any(os.path.normpath(os.path.join(wt, f)) in files for f in faulty)
        row["fault_reached"] = bool(hit)
        if not faulty:
            row["note"] = "no faulty lines from diff"
    except Exception as e:  # record and move on: this is a status probe
        row["note"] = f"{type(e).__name__}: {e}"[:160]
    return row


def source_faults(faulty: dict) -> dict:
    """Keep faulty lines in source files; drop files under a top-level test/ or tests/ directory."""
    return {f: ls for f, ls in faulty.items() if f.split("/", 1)[0] not in ("test", "tests")}


def bip_runner_faulty_lines(bug_id: str, wt: Path) -> dict:
    ensure_on_path()
    import bip_runner
    return source_faults(bip_runner.get_faulty_lines_from_diff(bug_id, str(wt)))


def main() -> None:
    ap = argparse.ArgumentParser(description="BugsInPy status probe")
    sub = ap.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("status")
    st.add_argument("--bugs", nargs="+", required=True)
    st.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    existing = {}
    if args.out.exists():
        existing = {r["bug_id"]: r for r in csv.DictReader(open(args.out))}
    for bug in args.bugs:
        existing[bug] = probe(bug)
        print({k: existing[bug][k] for k in STATUS_FIELDS}, flush=True)
        with open(args.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=STATUS_FIELDS)
            w.writeheader()
            w.writerows(sorted(existing.values(), key=lambda r: r["bug_id"]))


if __name__ == "__main__":
    main()
