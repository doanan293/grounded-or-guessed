# Phase 4 — Viết trọn bài, slide, rồi cắt 2 nhánh báo cáo tiến độ: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Báo cáo tiếng Việt đầy đủ và bài báo tiếng Anh (arXiv) trên `main`, một nguồn LaTeX với công tắc phiên bản `lan1` / `lan2` / `full`; slide lần 1, lần 2, bảo vệ; hai nhánh `bao-cao-lan-1`, `bao-cao-lan-2` cắt từ `main`.

**Architecture:** Mỗi chương / mục là một file `.tex`; `main.tex` chọn file theo `\Version` (`lan1` ⊂ `lan2` ⊂ `full`). Không có con số gõ tay: mọi số là macro trong `docs/report/generated/numbers{,-vi}.tex`, mọi bảng / hình là file sinh tự động; `scripts/lint_numbers.py` chặn số gõ tay. Slide dựng bằng hệ thống build hiện có (`docs/presentation/build/`, ppt-master Edit Native PPTX).

**Tech Stack:** XeLaTeX (báo cáo VI, Times New Roman), pdfLaTeX + IEEEtran (bài báo EN), latexmk, Python 3.12, ppt-master.

**Spec:** `docs/superpowers/specs/2026-11-08-semloc-fault-localization-design.md` (§6 sản phẩm, quy cách báo cáo và bảng phiên bản/nhánh; §7 Phase 4; §8 tiêu chí A; §9 thất bại cần tránh).

## Global Constraints

- Quy cách báo cáo VI (spec §6): Times New Roman 13pt; lề trên 3.5 / dưới 3 / trái 2.5 / phải 2.5 cm; giãn dòng 1.5; tiêu đề chương 16 đậm; đánh số mục tối đa 4 cấp, mỗi nhóm tiểu mục ≥ 2 mục; hình/bảng đánh số theo chương; số trang giữa chân trang; bìa, cam kết trung thực, mục lục, danh sách bảng/hình/viết tắt, tài liệu tham khảo IEEE.
- Bài báo EN: Introduction, Related Work, Background, Approach, Evaluation, Threats, Conclusion; dạng arXiv.
- Tác giả, đúng thứ tự: Doãn Văn An, Tạ Công Nam, Nguyễn Hoàng Hải, Đỗ Xuân Tráng, Hoàng Trung Kiên, Mai Văn Tùng, Nguyễn Đức Tùng (nhóm M9).
- Mọi con số trong văn bản là macro; mọi khẳng định trong Abstract / Introduction có số liệu chống lưng (spec §9).
- Mọi phần dùng từ SemLoc ghi nguồn; không trình bày lại SemLoc như đóng góp của nhóm.
- Artifact: link GitHub `https://github.com/doanan293/grounded-or-guessed`, không DOI.
- Nhánh: `lan1` = nội dung 1 + 2 của thầy; `lan2` = thêm nội dung 3 + bản nháp bài báo; `full` = cả 4. Code và dữ liệu giống nhau ở mọi nhánh.

## Review Focus

1. **Rò nội dung giữa phiên bản** — bản `lan1` không được chứa chương phân tích thất bại / đóng góp; mục lục, tham chiếu chéo (`\ref`) tới chương bị cắt không được ra "??". Pin bằng `test_versions_contain_expected_chapters` (Task 1).
2. **Số gõ tay** lọt vào `.tex` (đặc biệt Abstract, Introduction). Pin bằng `test_lint_flags_hand_typed_numbers` (Task 1) và chạy lint trên toàn bộ nguồn ở mỗi task viết.
3. **Trích dẫn hỏng** (`?` trong PDF, khóa `.bib` không tồn tại). Pin bằng kiểm tra log biên dịch không có "Citation … undefined" (Task 1 Makefile target `check`).
4. **Khẳng định không có dữ liệu** hoặc nói quá (vd. "thắng ở mọi model" khi chỉ đúng Acc@3). Pin bằng review tự phản biện Task 6, đối chiếu `docs/analysis/contributions.md`.
5. **Slide và báo cáo lệch số** — slide đọc cùng CSV/macro, dựng lại sau `regenerate_all.sh`. Pin bằng kiểm tra trong Task 7.

---

### Task 1 (P4-1): Công tắc phiên bản, lint số gõ tay, target kiểm tra

**Files:**
- Modify: `docs/report/vi/main.tex`, `docs/report/paper-en/main.tex`, `docs/report/Makefile`
- Create: `scripts/lint_numbers.py`, `tests/test_report_build.py`

**Interfaces:**
- Produces: `\Version` ∈ {`lan1`, `lan2`, `full`} (mặc định `full`), đặt bằng `make vi VERSION=lan1` (truyền `-usepretex="\def\Version{lan1}"`); macro `\IfAtLeast{lan2}{…}` bao các `\input` theo phiên bản.
- Produces: `make check` = biên dịch cả ba phiên bản VI + bài báo, thất bại nếu log có `undefined` (citation/reference) hoặc `lint_numbers.py` báo lỗi.
- Produces: `lint(tex: str) -> list[str]` — các số thập phân / phần trăm viết tay ngoài môi trường cho phép (macro, `\cite`, nhãn, kích thước, năm 19xx/20xx, số hiệu RQ/chương).

- [ ] **Step 1: Viết test** `test_lint_flags_hand_typed_numbers` (`"Acc@1 đạt 52,3\\%"` → 1 lỗi; `"Acc@1 đạt \\RqTwoRepairedAllSemlocAccOneMean\\%"`, `"\\cite{yang2026}"`, `"RQ3"`, `"năm 2026"`, `"\\vspace{2pt}"` → 0) và `test_versions_contain_expected_chapters` (biên dịch 3 phiên bản; `pdftotext`: `lan1` có "Kết quả thực nghiệm", không có "Phân tích thất bại"; `lan2` có cả hai, không có phụ lục bài báo; không có "??").
- [ ] **Step 2: Chạy** `.venv/bin/pytest tests/test_report_build.py -q` → FAIL.
- [ ] **Step 3: Cài** công tắc trong hai `main.tex`, `lint_numbers.py`, target `make check` (và `vi-lan1`, `vi-lan2`, `vi-full`, `paper`).
- [ ] **Step 4: Chạy** test → PASS (chương còn là khung).
- [ ] **Step 5: Commit.**

### Task 2 (P4-2): Dàn ý chi tiết — ⛔ chủ dự án duyệt trước khi viết

**Files:** Create `docs/analysis/outline.md`

- [ ] **Step 1: Viết dàn ý** báo cáo VI theo chương, mỗi mục: ý chính (1–2 câu), nguồn (file `data/` / tài liệu / bảng sinh), phiên bản bắt đầu xuất hiện. Khung chương đề xuất: (1) Mở đầu — vấn đề, câu hỏi, đóng góp tóm tắt; (2) Tổng quan tài liệu và từ khóa — 3 bài thầy giao, 23 tài liệu, so sánh; (3) Cơ sở lý thuyết — SBFL, LLM-FL, SemLoc; (4) Phương pháp — RQ, benchmark + SemFault-250-verified, CovGate, baseline, thống kê; (5) Kết quả RQ1–RQ3; (6) Phân tích thất bại và thảo luận [`lan2`]; (7) Đóng góp, triết lý khoa học, Threats [`lan2`]; (8) Kết luận; Phụ lục: tái hiện, bảng đầy đủ.
- [ ] **Step 2: Viết dàn ý** bài báo EN (mục, đoạn, hình/bảng từng mục, độ dài mục tiêu ≈ 10–12 trang IEEE hai cột).
- [ ] **Step 3: Commit** và dừng chờ duyệt; ghi ý kiến của chủ dự án vào dàn ý.

### Task 3 (P4-3): Báo cáo VI — tiền nội dung + chương nội dung 1 và 2 (bản `lan1`)

**Files:** `docs/report/vi/frontmatter/*.tex`, `docs/report/vi/chapters/ch1..ch5*.tex` (đổi tên theo dàn ý), `docs/report/references.bib`

- [ ] **Step 1:** Bìa (nhóm M9, 7 tên + MSHV đúng thứ tự, đề tài 2KH, GVHD), cam kết, viết tắt.
- [ ] **Step 2:** Viết chương 1–5 theo dàn ý đã duyệt; bảng `\input{../generated/…}`; số chỉ bằng macro `numbers-vi.tex`.
- [ ] **Step 3: Chạy** `make check` → 0 undefined, lint 0 lỗi; `make vi VERSION=lan1` → PDF.
- [ ] **Step 4: Commit.**

### Task 4 (P4-4): Báo cáo VI — chương nội dung 3 (bản `lan2`) và kết luận, phụ lục (`full`)

**Files:** chương 6–8 và phụ lục theo dàn ý (nguồn: `docs/analysis/failure-analysis.md`, `contributions.md`).

- [ ] **Step 1:** Viết chương phân tích thất bại, đóng góp + triết lý khoa học + Threats, kết luận, phụ lục tái hiện.
- [ ] **Step 2: Chạy** `make check`; test phiên bản PASS.
- [ ] **Step 3: Commit.**

### Task 5 (P4-5): Bài báo tiếng Anh

**Files:** `docs/report/paper-en/main.tex`, `sections/*.tex`

- [ ] **Step 1:** Viết theo dàn ý EN (dùng skill research-paper-writing): Abstract, Introduction (đóng góp đánh số, mỗi đóng góp có số), Related Work, Background (SemLoc), Approach (audit, SemFault-250-verified, CovGate, baseline, decomposition), Evaluation (RQ1–RQ3, failure analysis), Threats, Conclusion, Data availability (link GitHub).
- [ ] **Step 2: Chạy** `make check` → 0 undefined, lint 0 lỗi, PDF ≤ 12 trang nội dung + tài liệu.
- [ ] **Step 3: Commit.**

### Task 6 (P4-6): Tự phản biện 5 chiều

**Files:** Create `docs/analysis/self-review.md`; sửa báo cáo / bài báo.

- [ ] **Step 1:** Phản biện theo 5 chiều (đóng góp, độ rõ, sức mạnh thực nghiệm, độ đầy đủ đánh giá, độ hợp lý thiết kế); mỗi khẳng định trong Abstract / Introduction / Conclusion đối chiếu macro + file dữ liệu; liệt kê sửa đổi.
- [ ] **Step 2:** Sửa; `make check`.
- [ ] **Step 3: Commit.**

### Task 7 (P4-7): Slide lần 1 (dựng lại), lần 2, bảo vệ

**Files:** `docs/presentation/build/build_bao_cao_lan_1.py` (dựng lại sau `regenerate_all.sh`), Create `build_bao_cao_lan_2.py`, `build_bao_ve.py`; `docs/presentation/bao-cao-lan-{1,2}.pptx`, `bao-ve.pptx`

- [ ] **Step 1:** Slide lần 1: dựng lại (số liệu ground truth mới, bỏ nhắc DOI), tác giả trên bìa.
- [ ] **Step 2:** Slide lần 2: thêm phân tích thất bại (mơ hồ đầu khối/thân khối, 5 mẫu nguyên nhân), đóng góp, triết lý khoa học, kế hoạch nộp.
- [ ] **Step 3:** Slide bảo vệ: toàn bộ câu chuyện, ≤ 20 phút.
- [ ] **Step 4: Chạy** `svg_quality_checker.py --roundtrip` → 0 lỗi mỗi bộ; render PDF xem từng trang; đối chiếu ngẫu nhiên 10 số trên slide với `numbers-vi.tex`.
- [ ] **Step 5: Commit.**

### Task 8 (P4-8): Cắt nhánh báo cáo

- [ ] **Step 1:** Từ `main`: `bao-cao-lan-1` với `\Version` mặc định `lan1` + PDF báo cáo bản `lan1` + slide lần 1; `bao-cao-lan-2` tương tự với `lan2` + bản nháp bài báo + slide lần 2. Mỗi nhánh có `docs/report/README` ghi phiên bản và ngày báo cáo.
- [ ] **Step 2: Chạy** `make check` trên từng nhánh.
- [ ] **Step 3:** Push `main`, `bao-cao-lan-1`, `bao-cao-lan-2` bằng `scripts/push_public.sh` (cần thêm tham số nhánh đích).
