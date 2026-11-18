# Slide chuyên sâu, ba deck và một báo cáo final — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ba deck (lần 1 ~23 trang, lần 2 ~23, bảo vệ ~28) kể sâu theo năm phần thầy yêu cầu với hai ví dụ chạy thật, và một báo cáo final (bỏ phiên bản lần 1/2) có đủ hình.

**Architecture:** Dữ liệu ví dụ dẫn xuất một lần (`scripts/figure_data.py` → `data/fig_semloc_examples.json`), dùng chung cho hình báo cáo và slide. Deck: `docs/presentation/build/` tách `story.py` thành `story_common.py` (trợ giúp + trang dùng chung), `story_lan1.py`, `story_lan2.py`, `story_baove.py`; `build_deck.py` gọi theo deck. Báo cáo: gỡ `\IfAtLeast…` bằng một script một lần, thêm hình ví dụ và các hình còn lại.

**Tech Stack:** Python 3 (`.venv`; `/usr/bin/python3` cho deck), matplotlib, XeLaTeX/TikZ, ppt-master Edit Native PPTX.

**Spec:** `docs/superpowers/specs/2026-11-18-slide-chuyen-sau-design.md` (chính) và `docs/superpowers/specs/2026-11-18-hinh-va-ke-chuyen-design.md` (tên phương pháp, phong cách hình, mạch cải tiến, chống phóng đại). Thay thế Phần B/C của `docs/superpowers/plans/2026-11-18-hinh-ke-chuyen-ca-ba-ban.md`.

## Global Constraints

- Năm phần mỗi deck: Cơ sở lý thuyết · Phương pháp giải quyết · Cải tiến · Thực nghiệm chứng minh · Kết quả (+ Tiến độ ở lần 1, lần 2; bảo vệ không có).
- Thuật ngữ trên slide và notes: "test fail / test pass"; "phương pháp X" trong tiêu đề và câu; "chuẩn hóa nhãn / nhãn đã chuẩn hóa"; "overclaim (tuyên bố quá mức)" = khẳng định mạnh hơn bằng chứng, **điểm thưởng tự nó không phải overclaim**.
- Không chữ cụt trên slide: không "CT", "CI", "k token", "Phổ", "+thưởng", "Chèn, chạy"; mọi thuật ngữ định nghĩa ở lần đầu xuất hiện.
- Mỗi trang nội dung: tiêu đề là một câu kết luận + hình + khung giải thích (`viz.panel`, một `<text>` nhiều `<tspan x dy>`) + speaker notes 2–6 câu, chỉ chứa số có trên trang.
- Hai ví dụ (lượt chạy 1, Gemini 3.8 Flash): `votes_apportion` — nhãn dòng 29 (ghi "dòng lỗi theo nhãn: 29"), SBFL hòa 0,45, SemLoc 4 ràng buộc không cái nào bị vi phạm, hạng 1 = dòng 26 chỉ nhờ điểm thưởng, FailLoc `[29, 25, 26, 28, 30]`; `blend_orders` — nhãn dòng 72 xác nhận bằng thực thi, điểm phổ dòng 72 = 1,00, dòng đoán 73 = 0,60 + 1,2, FailLoc `[72, 73, 64, 65, 71]`; trang dùng `blend_orders` ghi "nhãn đã chuẩn hóa".
- Bảng tiến độ ba mức (lần 1): Đã xong (Lần 1) · Đang hoàn thiện (Lần 2 25–26/11: rà soát nhãn, duyệt mù, RQ3, ablation, đóng góp và triết lý) · Đang hoàn thiện (Bảo vệ: phân tích thất bại, kiểm chứng bằng bản sửa) · Chưa làm (bài báo arXiv bản cuối, 26/11–10/12). Lần 2: hàng lần 2 → Đã xong; bài báo → Có bản nháp.
- Lần 1 không lộ nội dung lần 2; lần 2 không lộ phân tích thất bại và FailLoc+Verify.
- Không số gõ tay; không chạy lại thí nghiệm; so sánh chỉ trên cùng điều kiện, kèm khoảng tin cậy.
- Deck: quality gate 0 lỗi (`make_decks.sh`); báo cáo: `make -C docs/report check`; `.venv/bin/pytest -q` xanh.
- Commit không có dòng Claude; không push khi chưa hỏi trưởng nhóm.

## Review Focus

1. Số trên slide lệch số trong báo cáo cho cùng đại lượng → mọi số slide lấy từ `bd._m` macro hoặc cùng CSV; test notes so số với chữ trên trang (đã có), thêm test so khớp giá trị ví dụ JSON với `runs/` (Task 1).
2. Deck lần 1 lộ chữ của lần 2 ("FailLoc+Cov", "rà soát", "duyệt mù" ngoài bảng tiến độ, "BugsInPy") → test quét chữ trên mọi trang lan1 trừ trang tiến độ (Task 6).
3. Chữ cụt quay lại → test quét chữ trên mọi trang mọi deck cấm `\bCT\b`, `\bCI\b`, `k token`, `+thưởng` (Task 5).
4. Gỡ phiên bản báo cáo làm mất nội dung hoặc để lại chữ "Báo cáo tiến độ" → test bản final (Task 2).
5. Khung chữ tràn hoặc trang quá chật khi thêm giải thích → quality gate 0 lỗi + xem ảnh render từng trang mỗi deck (Task 6, 7, 8).

---

### Task 1: Dữ liệu hai ví dụ cho hình và slide

**Files:** Modify `scripts/figure_data.py`; Create `data/fig_semloc_examples.json`; Test `tests/test_figure_data.py`.

**Interfaces:**
- Produces: `semloc_example(run_dir: Path, program: str, failloc_rank: list[int]) -> dict` với khóa `program, label_lines, label_status, code_lines[{no,text}], guess_line, constraints[{id, category, anchor_line|None, region, expr, intent, ef, ep, ochiai}], line_scores[{line, spectrum, bonus, rank}], cf_changed_rank: bool, failloc_top5: list[int], failloc_prompt: str, n_fail, n_pass`; tệp JSON là `{"votes_apportion": {...}, "blend_orders": {...}}`.
- `failloc_prompt` dựng bằng `flx.direct_cov.build_prompt(..., coverage=False)` với đúng đầu vào mà `scripts/run_direct_cov.py` dùng cho lượt `direct_tests` (đọc script đó để lấy cách nạp test fail và thông báo lỗi).

- [ ] **Step 1: Test** `test_examples_match_runs` (skip nếu thiếu `runs/`): `votes_apportion` có 4 ràng buộc, mọi `ochiai == 0`, `line_scores == [{line: 26, spectrum: 0, bonus: 1.2, rank: 1}]`, `failloc_top5 == [29, 25, 26, 28, 30]`, `label_lines == [29]`, `label_status == "unverified"`; `blend_orders` có dòng 72 `spectrum == 1.0`, dòng 73 `spectrum ≈ 0.60`, `bonus == 1.2`, `rank == 1`, `failloc_top5[0] == 72`, `label_status == "confirmed"`; prompt chứa tên test fail và chuỗi "exactly one".
- [ ] **Step 2:** chạy → FAIL. **Step 3:** cài đặt (ràng buộc từ `constraints/<p>.json`, ef/ep/ochiai từ `scores/<p>.json`, mã từ `third_party/semloc/benchmark/programs`, khung mã = hàm chứa nhãn qua `function_window`). **Step 4:** PASS; gọi trong `regenerate_all.sh`.
- [ ] **Step 5:** Commit `"data: hai ví dụ chạy xuyên suốt (votes_apportion, blend_orders) cho hình và slide"`.

### Task 2: Báo cáo chỉ còn bản final

**Files:** Create `scripts/drop_versions.py` (dùng một lần, xóa sau khi commit kết quả hoặc giữ trong `scripts/` có docstring — Builder quyết); Modify `docs/report/vi/**/*.tex`, `docs/report/paper-en/**/*.tex`, `docs/report/vi/main.tex`, `docs/report/paper-en/main.tex`, `docs/report/Makefile`, `docs/report/README.md`, `tests/test_report_build.py`.

**Interfaces:** `resolve(tex: str) -> str`: `\IfAtLeast{v}{A}` → `A`; `\IfAtLeastElse{v}{A}{B}` → `A`; `\IfBelow{v}{A}` → `""`; ngoặc lồng nhau cân bằng; giữ nguyên mọi thứ khác.

- [ ] **Step 1: Test** `tests/test_drop_versions.py`: các ví dụ trên, ngoặc lồng (`\IfAtLeast{lan2}{a {b} c}` → `a {b} c`), `\IfAtLeastElse` có `&` ở ngoài, không đụng tới chuỗi không có macro.
- [ ] **Step 2:** FAIL → cài → PASS; chạy trên mọi tệp; xóa định nghĩa macro và `\Version` khỏi preamble; xóa mục "Hiện trạng bốn nội dung" khỏi `nhom.tex` (giữ "Công cụ AI"), xóa dòng "Báo cáo tiến độ" ở bìa; Makefile chỉ còn `vi`, `paper`, `check`, `clean` (PDF `vi/main.pdf` → `docs/report/bao-cao.pdf`).
- [ ] **Step 3: Test** viết lại `test_report_build.py`: bản final có đủ chương 1–8 + phụ lục, có "Danh sách hình vẽ", "FailLoc", "nhãn đã chuẩn hóa", "tuyên bố quá mức (overclaim)"; không có "Báo cáo tiến độ", "Hiện trạng bốn nội dung", "??", "đã sửa nhãn", "LLM hỏi thẳng".
- [ ] **Step 4:** `make -C docs/report check` + `.venv/bin/pytest -q` xanh. Commit `"báo cáo: chỉ còn bản final (gỡ phiên bản lần 1/2)"`.

### Task 3: Hình ví dụ chạy xuyên suốt trong báo cáo + soát chữ

**Files:** `scripts/make_figures.py` (`semloc_example_tex(ex: dict) -> str` → `generated/vi/fig_semloc_<program>.tex`; `failloc_example_tex(ex: dict) -> str`), `docs/report/vi/figures/` (khung bọc), `ch3-co-so-ly-thuyet.tex` (sau hình quy trình SemLoc), `ch4-phuong-phap.tex` (sau định nghĩa FailLoc), `ch5-ket-qua.tex` (mục overclaim), `tests/test_make_figures.py`.

- [ ] **Step 1: Test** `semloc_example_tex(blend_orders)` có một hàng mỗi ràng buộc với ef, ep, Ochiai đúng JSON và dòng điểm cuối "0,60 + 1,2"; `failloc_example_tex(votes_apportion)` chứa prompt (rút gọn mã) và "29" ở hạng 1.
- [ ] **Step 2:** FAIL → cài (hình F8: mã có dòng kiểm tra được chèn tô màu + bảng ràng buộc × (ef, ep, Ochiai) + điểm dòng; hình F9: hộp prompt → hộp câu trả lời) → PASS.
- [ ] **Step 3:** Chèn hình; sửa mục overclaim (ch5 và ch1) cho đúng định nghĩa: điểm thưởng là lựa chọn thiết kế, overclaim là quy độ chính xác cho bằng chứng thực thi mà không mô tả điểm thưởng; thêm câu về `votes_apportion` (bốn ràng buộc không bị vi phạm, hạng 1 hoàn toàn là dòng đoán). Soát toàn văn: thuật ngữ, câu quá dài (> 3 dòng in), chữ viết tắt chưa định nghĩa.
- [ ] **Step 4:** `make check`, xem ảnh trang có hình mới; commit `"báo cáo: hình ví dụ SemLoc và FailLoc chạy trên chương trình thật; overclaim đúng định nghĩa"`.

### Task 4: Các hình còn lại của báo cáo

Theo Task 10 và 13 của kế hoạch cũ (`2026-11-18-hinh-ke-chuyen-ca-ba-ban.md`), giờ không còn `\IfAtLeast`:
F6 rà soát nhãn + duyệt mù (TikZ), C3 nhãn gốc đi đâu, C4 ablation, C5 các cách bổ sung + công cụ tĩnh, C6 độ bền RQ3 (ba panel) + `fig_pareto.pdf` thay `pareto.pdf`, C7 phân rã Shapley, C8 phân loại thất bại, C9 dumbbell SemLoc → FailLoc theo ba bộ nhãn và năm họ mô hình, F7 FailLoc+Verify.

- [ ] **Step 1: Test** mỗi hàm `*_data()` khớp CSV nguồn (đã ghi ở kế hoạch cũ), mỗi PDF rộng 16 cm.
- [ ] **Step 2:** FAIL → cài → PASS → chèn vào ch4/ch5/ch6, rút văn trùng hình; `make check`; xem ảnh.
- [ ] **Step 3:** Commit theo nhóm (nhãn; RQ2 bổ sung; RQ3 và phân rã; ch6).

### Task 4b: Báo cáo final tối đa 45 trang (bổ sung 18/11)

**Files:** `docs/report/vi/main.tex`, `docs/report/vi/chapters/*.tex`, `docs/report/vi/frontmatter/*.tex`, `tests/test_report_build.py`.

- [ ] **Step 1: Test** `test_final_report_is_complete` thêm: số trang PDF ≤ 45 (`pdfinfo`).
- [ ] **Step 2:** FAIL → cắt cơ học (tocdepth mục, danh sách/tài liệu tham khảo giãn dòng đơn, bỏ phụ lục), đo lại; rồi rút thân bài từng chương (giữ hình, bảng chính, mọi macro số; cắt văn trùng hình; gộp ch6 vào ch5, ch7 vào ch8 nếu cần) tới khi ≤ 45 → PASS; `make check`; commit.

### Task 5: Thành phần slide dùng chung

**Files:** `docs/presentation/build/viz.py`, Create `docs/presentation/build/story_common.py` (chuyển từ `story.py`: `_csv`, `_title`, `_note`, `_card`, `_unbold`, `cover`, `_bonus_rows`, `_guess_rank1_share`, dữ liệu ví dụ), `tests/test_deck_viz.py`, Create `tests/test_deck_text.py`.

**Interfaces (viz, mỗi hàm trả `<g data-pptx-bounds>`):**
- `section_band(gid, idx: int, label: str) -> str` — dải nhỏ góc trên phải "Phần idx · label".
- `formula(gid, x, y, w, lines: list[str]) -> str` — hộp công thức chữ (ví dụ Ochiai = test fail qua dòng / √(tổng test fail × số test qua dòng)).
- `constraint_table(gid, x, y, w, rows: list[dict]) -> str` — cột Ràng buộc | Gắn ở | Biểu thức | test fail vi phạm | test pass vi phạm | Ochiai.
- `code_block(..., inserted: dict[int, str] | None)` — thêm dòng kiểm tra được chèn (chữ nghiêng, nền tím nhạt) sau dòng số.
- `progress_table(gid, x, y, w, rows: list[tuple[str, str, str]]) -> str` — Việc | Trạng thái (màu theo mức) | Trình bày.
- `story_common.page_text(page: Path) -> str` (gộp chữ trên trang, dùng cho test).

- [ ] **Step 1: Test** mỗi hàm mới parse được, có đủ hàng/cột, giá trị số dùng dấu phẩy; `tests/test_deck_text.py::test_no_clipped_words[deck]` (skip nếu thiếu workspace) quét mọi trang cấm `\bCT\b`, `\bCI\b`, `k token`, `+thưởng`, `trượt`, "sửa nhãn".
- [ ] **Step 2:** FAIL → cài → PASS (test chữ cụt sẽ còn đỏ tới Task 6/7/8 — đánh dấu `xfail(strict=False)` cho deck chưa làm). Commit.

### Task 6: Deck lần 1 (~23 trang)

**Files:** Create `docs/presentation/build/story_lan1.py` (`LAN1: list[tuple[str, int]]`, `pages(bd)`, `notes(bd) -> dict`), xóa `story.py` (đã tách), Modify `build_deck.py` (gọi `story_lan1` cho `lan1`), `tests/test_deck_notes.py` (giữ), `tests/test_deck_text.py` (bỏ xfail lan1; thêm `test_lan1_does_not_leak` cấm "FailLoc+Cov", "BugsInPy", "duyệt mù", "rà soát" trên mọi trang trừ `tien_do`).

Roster = mạch lần 1 trong spec (23 trang); trang (VD) dùng `votes_apportion`, trang cơ chế điểm phổ (trang 10) dùng `blend_orders` kèm câu "ở `votes_apportion` không ràng buộc nào bị vi phạm nên mọi điểm phổ bằng 0 — trang này dùng chương trình thứ hai để thấy cơ chế". Trang 13 tiêu đề: "Hạng 1 luôn là dòng LLM đoán, nhưng bài báo quy độ chính xác cho bằng chứng thực thi"; khung "Overclaim của bài báo" theo định nghĩa ở Global Constraints. Mỗi trang có `section_band`.

- [ ] **Step 1:** Viết trang theo roster; `qc.sh lan1` 0 lỗi; xuất, render 23 trang, xem từng trang (chồng chữ, tràn, chữ quá nhỏ < 13).
- [ ] **Step 2:** Notes 23 trang (humanizer), `pytest tests/test_deck_notes.py tests/test_deck_text.py` xanh.
- [ ] **Step 3:** `make_decks.sh lan1 lan2 baove`; commit `"deck lần 1: năm phần theo yêu cầu, hai ví dụ chạy thật, tiến độ một bảng"`.

### Task 7: Deck lần 2 (~23 trang)

**Files:** Create `docs/presentation/build/story_lan2.py`; Modify `build_deck.py`, `tests/test_deck_notes.py` (tham số `lan2`), `tests/test_deck_text.py` (lan2: cấm "FailLoc+Verify", "phân loại thất bại").

Roster = mạch lần 2 trong spec. Ví dụ con: đổi tên định danh lấy từ `data/semfault_renamed/` cho `votes_apportion` (trước/sau); ablation dùng prompt `votes_apportion` có dòng chú thích độ phủ (dựng bằng `build_prompt(..., coverage=True)`, thêm vào JSON ở Task 1 nếu cần). Đóng góp và triết lý lấy từ ch7 (bản final).

- [ ] **Step 1:** Trình roster cho trưởng nhóm (ppt-master §4.3) và chờ đồng ý.
- [ ] **Step 2:** Dựng, `qc.sh lan2` 0 lỗi, render xem từng trang; notes; test xanh; commit.

### Task 8: Deck bảo vệ (~28 trang)

**Files:** Create `docs/presentation/build/story_baove.py` (dùng lại trang của `story_lan1`/`story_lan2` qua hàm theo trang, không chép mã); Modify `build_deck.py` (bỏ trang mẫu cũ không còn dùng, gồm `analysis_pages`, `results_pages`, `group_pages` nếu không deck nào gọi), tests.

Roster = mạch bảo vệ trong spec; không trang tiến độ; có FailLoc+Verify hai trang (sơ đồ đề xuất → bản sửa → chạy test → xếp lại; "test đủ gợi ý, quá yếu làm trọng tài" với số `\PavmechReviewedOtherLineFixable`), phân tích thất bại (C8 vẽ lại bằng viz + một ví dụ nhãn mơ hồ dòng `if`/thân).

- [ ] **Step 1:** Trình roster, chờ đồng ý. **Step 2:** dựng, qc 0 lỗi, render, notes, test, commit.

### Task 9: Bài báo tiếng Anh dùng cùng bộ hình

Theo Task 14 của kế hoạch cũ (nhãn tiếng Anh, dấu chấm thập phân, rộng 8,9 cm hoặc 18,2 cm; F1, F2, F4, F6, F7, F8 bản EN). `make -C docs/report paper` không cảnh báo; commit.

### Task 10: Phát hành

- [ ] **Step 1:** `scripts/regenerate_all.sh && .venv/bin/pytest -q && make -C docs/report check && docs/presentation/build/make_decks.sh` → tất cả xanh; `cp` PDF final → `docs/report/bao-cao.pdf`, `paper.pdf`.
- [ ] **Step 2:** Hỏi trưởng nhóm, rồi: gộp `hinh-ke-chuyen` vào `main`; dựng lại `bao-cao-lan-1` và `bao-cao-lan-2` từ `main`, mỗi nhánh chỉ giữ deck của lần đó (không PDF báo cáo, không deck khác); `git push origin main` và `git push --force-with-lease origin bao-cao-lan-1 bao-cao-lan-2` qua `github-personal`.
