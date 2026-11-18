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


VERSIONS = ("lan1", "lan2", "full")


def _build_all() -> dict:
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), *(f"vi-{v}" for v in VERSIONS)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    return {v: _pdf_text(ROOT / "docs" / "report" / "vi" / f"main-{v}.pdf") for v in VERSIONS}


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_versions_contain_expected_chapters():
    t = _build_all()
    assert "Kết quả thực nghiệm" in t["lan1"] and "Đóng góp, triết lý khoa học" not in t["lan1"]
    assert "Đóng góp, triết lý khoa học" in t["lan2"] and "Phân tích thất bại và thảo luận" not in t["lan2"]
    assert "Phân tích thất bại và thảo luận" in t["full"] and "Phụ lục" not in t["lan2"] and "Phụ lục" in t["full"]
    # members and the work split live only in docs/phan-cong.md; every version names FailLoc and lists its figures
    for v, text in t.items():
        assert "Thành viên nhóm M9" not in text and "Phân công công việc theo mảng" not in text, v
        assert "Phân công theo mảng việc" not in text, v
        assert "FailLoc" in text and "Danh sách hình vẽ" in text and "Hình 1.1" in text, v
        assert "LLM hỏi thẳng" not in text and "LLM + kiểm thử thất bại" not in text, v
        assert "??" not in text, v
    assert "FailLoc+Cov" not in t["lan1"] and "nhãn đã rà soát" not in t["lan1"]
    assert all("Cải tiến so với SemLoc" in t[v] for v in t)  # the improvement table, every version
    assert all("tuyên bố quá mức (overclaim) nhóm phát hiện" in t[v].lower() for v in t)
    assert "Báo cáo tiến độ lần 1 (18–19/11/2026)" in t["lan1"]
    assert "Báo cáo tiến độ lần 2 (25–26/11/2026)" in t["lan2"]
    assert "Báo cáo tiến độ" not in t["full"] and "Kế hoạch đến bài nộp cuối" not in t["full"]
    # both progress reports carry the status of the four required contents; the submission does not
    assert "Hiện trạng bốn nội dung (báo cáo lần 1)" in t["lan1"]
    assert "Hiện trạng bốn nội dung (báo cáo lần 2)" in t["lan2"]
    assert "Hiện trạng bốn nội dung" not in t["full"]


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_paper_draft_marker_only_below_full():
    r = subprocess.run(["make", "-C", str(ROOT / "docs" / "report"), "paper"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]
    assert "Draft for progress report" not in _pdf_text(ROOT / "docs" / "report" / "paper-en" / "main.pdf")


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("latexmk") is None, reason="needs TeX Live")
def test_versions_stage_the_results():
    """Each report shows a little more: 1 = RQ1, repaired labels, main comparison; 2 = + review, ablation,
    additions, static tools, RQ3, contributions; full = + failure analysis, propose-and-verify, appendix."""
    t = _build_all()
    stages = {
        "lan1": ["Kết quả chính trên bộ nhãn gốc và bộ đã sửa", "Grounded hay guessed: giá trị biên"],
        "lan2": ["Duyệt mù", "SemFault-250 đã rà soát", "Thông tin nào tạo ra khác biệt", "RQ3a:",
                 "Các cách bổ sung không cải thiện được", "Phân tích tĩnh trên 250 chương trình"],
        "full": ["cấu hình mạnh tay nhất", "Đề xuất rồi kiểm chứng dùng kiểm thử làm trọng tài", "Năm mẫu nguyên nhân"],
    }
    order = list(VERSIONS)
    for first, phrases in stages.items():
        for s in phrases:
            for v in order:
                shown = order.index(v) >= order.index(first)
                if first == "lan1" and s.startswith("Kết quả chính trên bộ nhãn gốc") and v in ("lan2", "full"):
                    continue  # from lan2 the table covers three label sets and is captioned differently
                assert (s in t[v]) == shown, (s, v)
    assert "RQ2 đang được thực hiện" not in t["lan1"]
    assert "RQ3 đang được thực hiện" in t["lan1"] and "RQ3 đang được thực hiện" not in t["lan2"]
    assert "Kết quả đến thời điểm báo cáo" in t["lan1"] and "Kết quả đến thời điểm báo cáo" not in t["lan2"]
