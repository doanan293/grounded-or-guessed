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


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_versions_contain_expected_chapters():
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), "vi-lan1", "vi-lan2", "vi-full"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    t = {v: _pdf_text(ROOT / "docs" / "report" / "vi" / f"main-{v}.pdf") for v in ("lan1", "lan2", "full")}
    assert "Kết quả thực nghiệm" in t["lan1"] and "Phân tích thất bại" not in t["lan1"]
    assert "Phân tích thất bại" in t["lan2"] and "Phụ lục" not in t["lan2"]
    assert "Phụ lục" in t["full"]
    # progress-report markers only below full, and the right one per version
    assert "Báo cáo tiến độ lần 1" in t["lan1"] and "Báo cáo tiến độ lần 2" in t["lan2"]
    assert "Báo cáo tiến độ" not in t["full"] and "Kế hoạch đến bài nộp cuối" not in t["full"]
    assert "báo cáo lần 2" in t["lan1"] and "báo cáo lần 2" not in t["lan2"]
    for v, text in t.items():
        assert "??" not in text, v


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_paper_draft_marker_only_below_full():
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), "paper"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]
    assert "Draft for progress report" not in _pdf_text(ROOT / "docs" / "report" / "paper-en" / "main.pdf")


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_versions_stage_the_results():
    """Report 1 shows RQ1 and the main comparison only; report 2 adds the rest except propose-and-verify; full has all."""
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), "vi-lan1", "vi-lan2", "vi-full"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    t = {v: _pdf_text(ROOT / "docs" / "report" / "vi" / f"main-{v}.pdf") for v in ("lan1", "lan2", "full")}
    lan2_only = ["Duyệt mù", "SemFault-250 đã rà soát", "Thông tin nào tạo ra khác biệt", "RQ3a:",
                 "Các cách bổ sung không cải thiện được", "Phân tích tĩnh trên 250 chương trình"]
    full_only = ["cấu hình mạnh tay nhất", "Đề xuất rồi kiểm chứng dùng kiểm thử làm trọng tài"]
    for s in lan2_only + full_only:
        assert s not in t["lan1"], s
        assert s in t["full"], s
    for s in lan2_only:
        assert s in t["lan2"], s
    for s in full_only:
        assert s not in t["lan2"], s
    assert "Kết quả đến thời điểm báo cáo" in t["lan1"] and "RQ3 đang được thực hiện" in t["lan1"]
