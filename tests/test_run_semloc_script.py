import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_semloc.sh"


def test_refuses_workdir_owned_by_another_run_id(tmp_path):
    (tmp_path / ".flx_run_id").write_text("r1\n")
    p = subprocess.run([str(SCRIPT), str(tmp_path), "m", "0.8", "r2"], capture_output=True, text=True, timeout=30)
    assert p.returncode == 3
    assert "r1" in p.stderr and "r2" in p.stderr
