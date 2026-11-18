"""Report versions and the hand-typed-number lint. The build test compiles LaTeX (slow): run with `pytest -m slow`."""
import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lint_numbers", ROOT / "scripts" / "lint_numbers.py")
ln = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ln)


def test_lint_flags_hand_typed_numbers():
    assert len(ln.lint("Acc@1 đạt 52,3\\% trên tập test.")) == 1
    assert len(ln.lint("Acc@3 is 92.0 here")) == 1
    assert len(ln.lint("tăng 15\\% so với")) == 1
    ok = ["Acc@1 đạt \\RqTwoRepairedAllSemlocAccOneMean\\%.", "\\cite{yang2026semloc}", "RQ3 và RQ1",
          "năm 2026, phiên bản 3.12", "\\vspace{2.5pt}\\hspace{1.5cm}", "% chú thích 52,3\\% bị bỏ qua",
          "\\label{tab:rq2.1}\\ref{sec:3.2}", "\\includegraphics[width=0.48\\linewidth]{x}",
          "Học kỳ 2026.1", "semester 2026.1", "Claude Sonnet 4.6 và Gemini 2.5 Pro", "Gemini 3.8 Flash", "Claude Fable 5.1", "GPT-6",
          "{\\setstretch{1.2}", "giấy phép Apache-2.0"]
    for s in ok:
        assert ln.lint(s) == [], s


def _pdf_text(pdf: Path) -> str:
    """PDF text with whitespace collapsed, so phrases broken across lines still match."""
    return " ".join(subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout.split())


def _build_final() -> str:
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), "vi"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    return _pdf_text(ROOT / "docs" / "report" / "vi" / "main.pdf")


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_final_report_is_complete():
    """One final report (owner, 18/11): every chapter, the figure list, the new terms; no progress-report leftovers."""
    t = _build_final()
    for ch in ("Mở đầu", "Kết quả thực nghiệm", "Phân tích thất bại và thảo luận", "Đóng góp, triết lý khoa học",
               "Phụ lục", "Danh sách hình vẽ", "Danh sách bảng"):
        assert ch in t, ch
    for s in ("FailLoc", "nhãn đã chuẩn hóa", "Cải tiến so với SemLoc", "Hình 1.1"):
        assert s in t, s
    assert "tuyên bố quá mức (overclaim) nhóm phát hiện" in t.lower()
    for s in ("Báo cáo tiến độ", "Hiện trạng bốn nội dung", "??", "sửa nhãn", "LLM hỏi thẳng", "Thành viên nhóm M9",
              "Phân công theo mảng việc", "Draft for progress report"):
        assert s not in t, s


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_paper_builds_without_draft_marker():
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), "paper"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]
    assert "Draft for progress report" not in _pdf_text(ROOT / "docs" / "report" / "paper-en" / "main.pdf")
