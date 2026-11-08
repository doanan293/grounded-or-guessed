import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pilot_table_runs_from_any_cwd_with_label(tmp_path):
    out = tmp_path / "t.csv"
    p = subprocess.run([sys.executable, str(ROOT / "scripts/pilot_table.py"), "--run", str(ROOT / "runs/pilot_dev_gemini_r1_default"),
                        "--run-id", "pilot_dev_r1_default", "--label", "ours: test-label", "--out", str(out)],
                       cwd=tmp_path, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-400:]
    assert "ours: test-label" in out.read_text()
