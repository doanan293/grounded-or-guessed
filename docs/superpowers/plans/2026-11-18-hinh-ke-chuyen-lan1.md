# Hình, kể chuyện và FailLoc — lần 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Báo cáo VI lần 1 và deck lần 1 có tên phương pháp chuẩn (FailLoc …), 5 sơ đồ + 3 biểu đồ phong cách nghiên cứu trong báo cáo, deck kể chuyện vẽ riêng có speaker notes, bỏ thành viên/phân công.

**Architecture:** Một nguồn tên hiển thị (`scripts/method_names.py`) dùng chung cho bảng, hình, deck. Biểu đồ: `scripts/make_figures.py` (matplotlib, đọc `data/`) → `docs/report/generated/vi/fig_*.pdf`. Sơ đồ: TikZ trong `docs/report/vi/figures/*.tex`, số qua macro `numbers-vi.tex`. Deck: `build_deck.py` (ppt-master Edit Native PPTX, workspace `runs/slides/bao-cao-lan-1_20261108`) dựng trang mới trên khung `slide_22` (tiêu đề + nền trống) bằng SVG khối gốc, ghi `notes/<stem>.md`.

**Tech Stack:** Python 3 (`.venv` cho scripts/tests; `/usr/bin/python3` có python-pptx cho deck), matplotlib, XeLaTeX + TikZ, ppt-master scripts trong `.claude/skills/ppt-master/scripts`.

**Spec:** `docs/superpowers/specs/2026-11-18-hinh-va-ke-chuyen-design.md`

## Global Constraints

- Không chạy lại thí nghiệm, không đổi id trong `data/`; dữ liệu mới chỉ là tệp dẫn xuất từ `runs/` có sẵn.
- Không số gõ tay trong chương/frontmatter (`scripts/lint_numbers.py`); số trên hình đọc từ `data/` hoặc macro.
- Tên hiển thị: `llm_tests`→**FailLoc**, `llm_direct`→**LLM-Direct**, `llm_coverage`→**FailLoc+Cov**, `semloc`→**SemLoc**, `semloc_no_prior`→**SemLoc−Bonus**, `sbfl_ochiai`→**SBFL (Ochiai)**, `covgate`→**CovGate**, PAV→**FailLoc+Verify**, biểu quyết→**FailLoc+Vote**.
- FailLoc chỉ đổi nhãn; giữ khung "cách lập trình viên vẫn làm, được làm cho tái hiện được", không thêm tuyên bố tính mới.
- Hình báo cáo: đánh số theo chương, caption dưới hình, bảng caption trên, căn giữa, **cỡ chữ trong hình 13pt ở kích thước in** (Times New Roman), caption tự đủ nghĩa.
- VI dùng dấu phẩy thập phân (`52,3`).
- Lần 1 không lộ nội dung lần 2: không nhãn đã rà soát, ablation, CovGate kết quả, RQ3, pareto đa họ mô hình.
- Bỏ "Thành viên" và "Phân công" khỏi báo cáo và deck; giữ công cụ AI và hiện trạng bốn nội dung.
- Commit không có dòng Co-Authored-By Claude.
- Speaker notes: tiếng Việt, 2–5 câu văn nói/trang nội dung, 1–2 câu cho bìa/kết; không đề mục, không `[tag]`, không gạch ngang dài; không thêm khẳng định mà trang không có; qua humanizer.
- Ưu tiên khi thiếu giờ: F1 → C1 → F3 → F4 → F2 → C2 → F5 → Gantt → bảng phương pháp; mỗi task kết thúc ở trạng thái dựng được PDF + deck.

## Review Focus

1. Số trên hình lệch số trong bảng/văn bản (vd. Acc@1 của FailLoc trên C1 khác `\RqTwoRepairedAllLlmTestsAccOneMean`) → test so khớp trong Task 3.
2. Bản lần 1 lộ chữ/hình của lần 2 (FailLoc+Cov, "đã rà soát", RQ3) → `test_report_build.py` cấm cụm từ ở lan1; Task 5.
3. Chữ trong hình quá nhỏ khi `\includegraphics` co hình → hình xuất đúng chiều rộng in (`\linewidth` = 16 cm), include không scale; test kích thước trang PDF trong Task 3.
4. Chữ tràn khung trên slide sau khi viết lại → `svg_quality_checker.py --roundtrip` 0 lỗi, xem ảnh render; Task 7.
5. Notes thiếu trang hoặc lẫn markdown → test đếm `notes/*.md` = số trang plan, không dòng `#`/`[`; Task 8.

---

### Task 1: Tên phương pháp một nguồn và đổi tên trong bảng + văn bản

**Files:**
- Create: `scripts/method_names.py`
- Modify: `scripts/make_tables.py` (RQ2_NAMES, main_results_table, tolerant_table, BIP_NAMES, addons rows, cặp dịch `VI`)
- Modify: `docs/report/vi/chapters/ch1-gioi-thieu.tex`, `ch4-phuong-phap.tex`, `ch5-ket-qua.tex`, `ch8-ket-luan.tex`, `phu-luc.tex`, `docs/report/vi/frontmatter/vietat.tex`, `docs/report/paper-en/sections/*.tex` (chỉ chỗ gọi tên phương pháp)
- Test: `tests/test_method_names.py`, `tests/test_make_tables.py`

**Interfaces:**
- Produces: `NAMES: dict[str, str]` (id → tên hiển thị, giống nhau VI/EN), `name(method_id: str) -> str` (KeyError nếu id lạ), `OURS = "llm_tests"`.

- [ ] **Step 1: Test** `test_names_fixed`: `name("llm_tests")=="FailLoc"`, `name("llm_direct")=="LLM-Direct"`, `name("llm_coverage")=="FailLoc+Cov"`, `name("semloc_no_prior")=="SemLoc−Bonus"`, `name("sbfl_ochiai")=="SBFL (Ochiai)"`; `pytest.raises(KeyError, name, "nope")`. Trong `test_make_tables.py` thêm `test_tables_use_failloc`: sau `make_tables.main()`, `generated/vi/rq_main_results_two.tex` chứa `FailLoc`, không chứa `LLM + kiểm thử thất bại` hay `failing tests (ours)`.
- [ ] **Step 2:** `.venv/bin/pytest tests/test_method_names.py tests/test_make_tables.py -q` → FAIL.
- [ ] **Step 3:** Viết `method_names.py` (thêm id phụ: `cf_rerank`→`SemLoc+CF`, `gate_only`→`SemLoc+Gate`, `lam_only`→`SemLoc+λOchiai`, `grounded_prior_only`→`SemLoc+GroundedBonus`, `covgate_cf`→`CovGate+CF`, `llm_guess`→`LLM-Guess`); `make_tables.py` lấy tên từ `name()`; dòng FailLoc in thêm "(ours)" chỉ ở EN; xóa cặp dịch thừa trong `VI`.
- [ ] **Step 4:** Đổi tên trong văn bản VI/EN: lần đầu ở ch1 và ch4 có câu định nghĩa *"FailLoc (Failure-guided Localization): một lượt gọi LLM với mã nguồn đánh số dòng, tên và dòng lỗi đầu tiên của từng kiểm thử thất bại"*; các chỗ "1 prompt + test fail", "LLM + kiểm thử thất bại", "LLM hỏi thẳng", "SemLoc bỏ thưởng ẩn" → tên mới; thêm FailLoc vào `vietat.tex`. `grep -rn "hỏi thẳng\|kiểm thử thất bại (nhóm\|1 prompt + test" docs/report` → rỗng.
- [ ] **Step 5:** `scripts/regenerate_all.sh && .venv/bin/pytest -q -m "not slow"` → PASS; `make -C docs/report check` → exit 0.
- [ ] **Step 6:** Commit `"đổi tên phương pháp: FailLoc, LLM-Direct, SemLoc−Bonus … (một nguồn: scripts/method_names.py)"`.

### Task 2: Dữ liệu dẫn xuất cho hình (điểm từng dòng SemLoc, ví dụ phủ)

**Files:**
- Create: `scripts/figure_data.py`, `data/semloc_line_scores.csv`, `data/fig_example.json`
- Modify: `scripts/regenerate_all.sh` (gọi trước `make_figures.py`)
- Test: `tests/test_figure_data.py`

**Interfaces:**
- Produces: `data/semloc_line_scores.csv` cột `run,program,line,spectrum,bonus,score,rank,is_guess,is_gt_repaired` (từ `runs/semloc_test_gemini_r{1,2,3}/scores/*.json`: `spectrum = line_scores − bonus`, `bonus = 1.2` ở `fault_line_pred`); `data/fig_example.json` `{program, code_lines:[{no,text}], tests:[{id,passed,lines}], gt_line, guess_line}` cho một chương trình test ngắn (≤ 15 dòng hàm) mà test pass và fail phủ cùng tập dòng, lấy từ `data/coverage/semfault`.
- Hàm: `line_scores(run_dir: Path) -> list[dict]`, `pick_example(cov_dir: Path, gt: dict) -> dict`.

- [ ] **Step 1: Test** `test_bonus_dominates`: với fixture JSON nhỏ trong `tests/fixtures/semloc_scores/` (copy `adjust_allocation.json`), `line_scores` cho dòng 67 `bonus==1.2`, `spectrum≈0.408`, `rank==1`; `test_guess_always_rank1_on_real_data` (skip nếu thiếu `runs/`): trong CSV, mọi chương trình có `is_guess` thì dòng đó `rank==1`, và `max(spectrum) <= 1.0`. `test_example_is_blind`: trong `fig_example.json` tập dòng phủ bởi test fail ⊆ hợp tập dòng phủ bởi test pass.
- [ ] **Step 2:** Chạy → FAIL. **Step 3:** cài đặt. **Step 4:** chạy → PASS.
- [ ] **Step 5:** Commit `"data: điểm từng dòng SemLoc và chương trình ví dụ cho hình (dẫn xuất từ runs/, không chạy lại)"`.

### Task 3: Biểu đồ báo cáo (C1, C2, F3) — `scripts/make_figures.py`

**Files:**
- Create: `scripts/make_figures.py`, `scripts/fig_style.py`
- Modify: `scripts/regenerate_all.sh`
- Test: `tests/test_make_figures.py`

**Interfaces:**
- Consumes: `name()` (Task 1); `data/rq2_ours.csv`, `data/llm_cost.csv`, `data/semloc_line_scores.csv` (Task 2).
- Produces: `docs/report/generated/vi/fig_rq2_main.pdf` (C1), `fig_cost_acc.pdf` (C2), `fig_semloc_bonus.pdf` (F3); hàm `rq2_main_data(gt_sets: tuple) -> list[dict]` trả `{gt, method, acc1, acc1_sd, acc3, acc3_sd}`; `cost_acc_data() -> list[dict]` `{method, ktokens, acc1}`.
- `fig_style.py`: `apply(lang="vi")` đặt `font.family="Times New Roman"`, `font.size=13`, dấu phẩy thập phân VI; `COLOR = {"llm_tests": cam đậm, "semloc": navy, khác: xám}`; `WIDTH_IN = 16/2.54`.

- [ ] **Step 1: Test** `test_c1_matches_table`: `rq2_main_data(("original","repaired"))` cho `llm_tests/repaired` có `acc1 == float(rq2_ours[...]['acc1_mean'])*100`; chỉ chứa 5 phương pháp `sbfl_ochiai, llm_direct, semloc, semloc_no_prior, llm_tests` (không `llm_coverage`). `test_pdf_width`: sau `main()`, mỗi PDF có bề rộng trang 16 cm ± 0,1 (đọc bằng `pdfinfo`). `test_cost_points`: `cost_acc_data()` có `llm_tests` với `ktokens < semloc.ktokens`.
- [ ] **Step 2:** Chạy → FAIL.
- [ ] **Step 3:** Cài đặt. C1: cột nhóm Acc@1 và Acc@3, hai bảng con (nhãn gốc | nhãn đã sửa), thanh lỗi = sd qua 3 lần chạy (caption ghi rõ), nhãn số trên đầu cột. C2: scatter token/chương trình (log) × Acc@1 nhãn đã sửa, nhãn trực tiếp cạnh điểm. F3: một chương trình ví dụ (chương trình có nhiều dòng ứng viên nhất trong CSV, run 1): thanh xếp chồng spectrum + bonus mỗi dòng, đường kẻ ở 1,0 ("điểm phổ tối đa"), dòng nhãn đúng đánh dấu. Không tiêu đề trong hình.
- [ ] **Step 4:** Chạy → PASS; mở 3 PDF bằng `pdftoppm -png -r 80` và xem ảnh.
- [ ] **Step 5:** Commit `"hình: kết quả chính RQ2, chi phí–độ chính xác, điểm thưởng của SemLoc (matplotlib, từ data/)"`.

### Task 4: Sơ đồ TikZ (F1, F2, F4, F5)

**Files:**
- Create: `docs/report/vi/figures/tong-quan.tex` (F1), `sbfl-mu.tex` (F2), `sua-nhan.tex` (F4), `thiet-ke.tex` (F5); `scripts/make_figures.py` thêm `sbfl_matrix_tex() -> str` → `generated/vi/fig_sbfl_matrix.tex`
- Modify: `docs/report/vi/main.tex` (thêm `\usetikzlibrary{calc,matrix,backgrounds}` nếu cần; định nghĩa màu `failloc`, `semloc` khớp `fig_style.COLOR`)
- Test: `tests/test_make_figures.py::test_sbfl_matrix_tex`

**Interfaces:**
- Consumes: `data/fig_example.json` (Task 2); macro `\CostSemlocTokensK`, `\CostLlmTestsTokensK`, `\CostCfSharePct`, `\GtConfirmedN`, `\GtCorrectedN`, `\GtUnverifiedN`, `\GtUnverifiableN`, `\GtRepairedN`, `\GtBlankN`, `\GtNotExecutedN`, `\ConstPriorWeight`.

- [ ] **Step 1: Test** `test_sbfl_matrix_tex`: chuỗi trả về chứa `\begin{tikzpicture}`, một hàng mỗi test của ví dụ, ô "●" đúng số lần (= tổng `len(lines)` trên các test trong khung hàm), và không chứa chữ số gõ tay ngoài số dòng.
- [ ] **Step 2:** FAIL → cài đặt → PASS.
- [ ] **Step 3:** F1: hai làn ngang. Làn SemLoc: Mã → LLM viết ràng buộc → chèn & chạy test → phổ vi phạm → +thưởng `\ConstPriorWeight` dòng đoán → LLM vá thử (`\CostCfSharePct`% lượt gọi) → xếp hạng; nhãn "≈`\CostSemlocTokensK`k token/CT". Làn FailLoc: Mã + test thất bại → 1 lượt LLM → xếp hạng; "≈`\CostLlmTestsTokensK`k token/CT". F4: luồng quyết định của bộ phán định sửa tối thiểu, bốn lá có số, mũi tên "bỏ dòng trống" → `\GtRepairedN`. F5: lưới dev 50/test 200 × {SBFL, LLM-Direct, SemLoc, SemLoc−Bonus, FailLoc} × {nhãn gốc, nhãn đã sửa} × 3 lần; Gemini 3.8 Flash; chỉ số Acc@1/3/5. Chữ 13pt (`font=\normalsize`), rộng ≤ `\linewidth`, không `\resizebox`.
- [ ] **Step 4:** `make -C docs/report vi-lan1` → 0 lỗi (tạm `\input` vào một tệp thử nếu Task 5 chưa chèn).
- [ ] **Step 5:** Commit `"sơ đồ TikZ: tổng quan SemLoc/FailLoc, SBFL mù với lỗi ngữ nghĩa, sửa nhãn bằng thực thi, thiết kế thực nghiệm"`.

### Task 5: Chèn hình vào báo cáo, bỏ thành viên/phân công, bảng phương pháp

**Files:**
- Modify: `docs/report/vi/chapters/ch1-gioi-thieu.tex` (F1 sau "Đặt vấn đề"), `ch3-co-so-ly-thuyet.tex` (F2 cạnh hình TikZ cũ; giữ hình cũ nếu khác ý), `ch4-phuong-phap.tex` (F4 ở "SemFault-250 đã sửa", F5 + bảng phương pháp ở mục thiết kế), `ch5-ket-qua.tex` (F3 ở "Kiểm chứng phản thực tế…", C1 trước/thay đoạn văn liệt kê số, C2 ở "Một prompt…")
- Modify: `docs/report/vi/frontmatter/nhom.tex` (bỏ `\section*{Thành viên}`, `\section*{Phân công theo mảng việc}`; đổi tiêu đề chương thành "Công cụ AI và hiện trạng")
- Test: `tests/test_report_build.py`

- [ ] **Step 1: Test** sửa `test_report_build.py`: bỏ assert "Thành viên nhóm M9"/"Phân công công việc theo mảng"; thêm: mọi phiên bản *không* chứa "Phân công công việc theo mảng"; lan1 chứa "FailLoc", "Hình 1.1", "Danh mục hình vẽ" (hoặc tiêu đề `\listoffigures` thực tế); lan1 *không* chứa "FailLoc+Cov", "đã rà soát", "BugsInPy" trong caption hình (kiểm bằng `pdftotext` toàn văn — chỉ cấm "FailLoc+Cov" và "nhãn đã rà soát").
- [ ] **Step 2:** `.venv/bin/pytest -m slow tests/test_report_build.py -q` → FAIL.
- [ ] **Step 3:** Chèn hình bằng `\begin{figure}[H]\centering\input{figures/…}` / `\includegraphics{../generated/vi/fig_….pdf}` (không width scale), caption tự đủ nghĩa, `\label{fig:…}`, văn bản tham chiếu "Hình~\ref{…}". Rút gọn đoạn văn trùng ý với hình (nhất là đoạn liệt kê số RQ2). Bảng phương pháp (T): cột Phương pháp | Đầu vào | Lượt gọi LLM | Dùng thực thi?; 5 dòng lần 1.
- [ ] **Step 4:** `make -C docs/report check` → exit 0; `pytest -m slow tests/test_report_build.py` → PASS; `pdftoppm -r 50` các trang có hình của `main-lan1.pdf`, xem ảnh: chữ hình xấp xỉ cỡ chữ thân bài.
- [ ] **Step 5:** Commit `"báo cáo lần 1: 5 sơ đồ, 3 biểu đồ, bảng phương pháp; bỏ thành viên/phân công (chỉ còn docs/phan-cong.md)"`.

### Task 6: Bộ công cụ vẽ cho slide (SVG khối gốc)

**Files:**
- Create: `docs/presentation/build/viz.py`
- Test: `tests/test_deck_viz.py`

**Interfaces:**
- Produces (mọi hàm trả chuỗi SVG `<g id=… data-pptx-bounds="x y w h">…</g>` dùng màu ORANGE/LAVENDER/INK/NAVY/CREAM và font BODY/MONO của `build_deck.py`):
  - `code_block(gid, x, y, lines: list[str], highlight: set[int], fs=16) -> str` — đoạn mã đánh số dòng, dòng highlight nền cam nhạt.
  - `bars(gid, x, y, w, h, series: list[tuple[str, float, str]], vmax: float, unit="%") -> str` — thanh ngang có nhãn và số (dấu phẩy).
  - `pipeline(gid, x, y, steps: list[str], accent: int|None) -> str` — chuỗi hộp bo góc + mũi tên.
  - `big_number(gid, x, y, value: str, caption: str) -> str`.
  - `gantt(gid, x, y, w, rows: list[tuple[str, str, str, bool]]) -> str` — (việc, ngày bắt đầu `dd/mm`, ngày kết thúc, xong?).
  - `matrix(gid, x, y, rows: list[str], cols: list[str], cells: set[tuple[int,int]], row_mark: dict[int,str]) -> str`.

- [ ] **Step 1: Test** mỗi hàm: kết quả parse được bằng `xml.etree.ElementTree.fromstring`, có `data-pptx-bounds` 4 số, `bars` với giá trị `52.3` chứa text `52,3%`, `code_block` có đúng `len(lines)` phần tử `<text>`.
- [ ] **Step 2:** FAIL → cài đặt → PASS (`/usr/bin/python3 -m pytest tests/test_deck_viz.py`).
- [ ] **Step 3:** Commit `"deck: bộ vẽ SVG cho slide kể chuyện (mã, thanh, quy trình, số lớn, Gantt, ma trận)"`.

### Task 7: Deck lần 1 kể chuyện

**Files:**
- Modify: `docs/presentation/build/build_deck.py` (`SOURCE`, `DECKS["lan1"]`, hàm mới `story_pages()` gọi trong `main`), `docs/presentation/build/README.md` (mạch mới)
- Output: `docs/presentation/bao-cao-lan-1.pptx`

**Interfaces:**
- Consumes: `viz.*` (Task 6); `name()` (Task 1); `data/fig_example.json`, `data/semloc_line_scores.csv` (Task 2); `_m()` macro.

**Roster lần 1** (ppt-master §4.3 — đã trình bày cho trưởng nhóm cùng kế hoạch; mọi trang dưới đây là `rebuilt` trừ khi ghi khác; trang mới dùng khung `slide_22` = tiêu đề + nền trống):

| # | stem | khung | Tiêu đề (câu kết luận) | Hình |
|---|---|---|---|---|
| 1 | slide_01 | 1 | **Grounded or Guessed:** Tái hiện và đánh giá việc định vị lỗi ngữ nghĩa bằng mô hình ngôn ngữ lớn | bìa: tên đề tài đúng như trang bìa báo cáo (`vi/frontmatter/bia.tex`), dòng phụ "Đề tài 02-KH · Nhóm M9 · GVHD: PGS. TS. Huỳnh Quyết Thắng · Báo cáo lần 1 · 18–19/11/2026" |
| 2 | moc | 22 | Test fail. Dòng nào sai? | `code_block` ví dụ, chưa tô dòng |
| 3 | sbfl_mu | 22 | SBFL mù với lỗi ngữ nghĩa: test pass và fail đi cùng đường | `matrix` phủ + Acc@1 SBFL `\RqOneSbflOchiaiFairAllAccOne`% |
| 4 | semloc_hua | 22 | SemLoc hứa: neo LLM vào bằng chứng thực thi | `pipeline` 5 bước + `big_number` Acc@1 công bố |
| 5 | cau_hoi | 19 | Grounded hay guessed? Ba câu hỏi | danh sách RQ1–RQ3 (tên mới) |
| 6 | slide_25 | 25 | Nghiên cứu liên quan | giữ nội dung hiện có, đổi tên phương pháp |
| 7 | hop_den_1 | 22 | Mở hộp: điểm phổ của từng dòng | `bars` spectrum ví dụ F3 |
| 8 | hop_den_2 | 22 | Thêm +1,2 cho dòng đoán: hạng 1 luôn là dòng đoán | cùng `bars` + bonus, dòng đoán vọt lên; tỷ lệ hạng 1 = dòng đoán |
| 9 | nhan_sai | 22 | Chính nhãn của bộ dữ liệu cũng sai | `big_number` `\GtBlankN` dòng trống + `pipeline` sửa nhãn có số |
| 10 | failloc | 22 | FailLoc: đưa thẳng test fail cho LLM, một lượt | hai `pipeline` song song, token mỗi bên |
| 11 | thiet_ke | 22 | Thiết kế: 200 chương trình × 5 phương pháp × 2 bộ nhãn × 3 lần | `matrix` |
| 12 | ket_qua | 22 | FailLoc dẫn đầu cả hai bộ nhãn | `bars` Acc@1/Acc@3 (gốc, đã sửa) |
| 13 | chi_phi | 14 | Hơn `ΔAcc@1` điểm, rẻ hơn ~7 lần | `big_number` ×3 |
| 14 | lan_sau | 22 | Thắng thật hay nhờ nhãn? Vì sao? | ba câu hỏi mở cho lần 2 |
| 15 | cong_cu_ai | 22 | Công cụ AI nhóm dùng | bảng gọn (giữ) |
| 16 | hien_trang | 22 | Hiện trạng bốn nội dung | bảng (giữ, tên mới) |
| 17 | tien_do | 22 | Tiến độ | `gantt`, ngày lấy từ `docs/phan-cong.md` |
| 18 | slide_30 | 30 | Cảm ơn | giữ |

Bỏ khỏi lần 1: `nhom.svg`, `phan_cong.svg`, `slide_03` (mục lục), `slide_04/05/08/09/11/20/22`, `slide_14`, `ket_qua_thu`, `chuong0x`, `slide_21`. Chuyển trang không đổi (giữ nguồn). Không animation, không narration.

- [ ] **Step 0: Test** `tests/test_deck_title.py::test_cover_matches_report`: hằng `TITLE` trong `build_deck.py` (hai dòng: "Grounded or Guessed:" và phần tiếng Việt) khớp tên đề tài trong `bia.tex` sau khi bỏ lệnh LaTeX, `\\` và so sánh không phân biệt hoa thường; áp cho cả ba deck.
- [ ] **Step 1:** Cập nhật `SOURCE`/`DECKS["lan1"]` theo bảng; bìa của mọi deck dùng `TITLE`; viết `story_pages()` (chỉ dùng khi `DECK=="lan1"`; lan2/baove giữ trang cũ cho tới kế hoạch sau, nhưng thay tên phương pháp ở mọi deck qua `name()`).
- [ ] **Step 2:** `docs/presentation/build/make_decks.sh lan1` → in `lan1 -> docs/presentation/bao-cao-lan-1.pptx`, quality gate 0 lỗi.
- [ ] **Step 3:** Render: `soffice --headless --convert-to pdf` rồi `pdftoppm -r 60`, xem từng trang: không tràn chữ, không chồng hình, mỗi trang đọc được tiêu đề + hình. Sửa đến khi sạch.
- [ ] **Step 4:** `make_decks.sh lan2 baove` vẫn chạy được (quality gate 0 lỗi).
- [ ] **Step 5:** Commit `"deck lần 1: mạch kể chuyện 18 trang, hình vẽ riêng; bỏ thành viên/phân công"`.

### Task 8: Speaker notes

**Files:**
- Modify: `docs/presentation/build/build_deck.py` (`NOTES: dict[str, dict[str, str]]` theo deck → stem → văn nói; `write_notes()` ghi `WS/notes/<stem>.md` cho mọi trang của deck, xóa notes của stem không thuộc deck)
- Test: `tests/test_deck_notes.py`

- [ ] **Step 1: Test** (dùng `/usr/bin/python3`): sau `build_deck.main("lan1")` (skip nếu thiếu workspace): số tệp `notes/*.md` khớp `page_plan.json`; mỗi tệp không rỗng, không dòng bắt đầu `#`, không chứa `[`, `—`, `–`; trang nội dung có 2–5 câu (đếm `. `/`? `), bìa/cảm ơn 1–2 câu; mọi số trong note xuất hiện trong text SVG cùng trang.
- [ ] **Step 2:** FAIL → viết notes cho 18 trang theo mạch (câu chuyển trang bằng văn xuôi), chạy humanizer trên toàn bộ notes (bỏ khuôn "không phải X mà Y", câu chốt một dòng, liệt kê ba) → PASS.
- [ ] **Step 3:** `make_decks.sh lan1`; `python3 .claude/skills/ppt-master/scripts/source_to_md/ppt_to_md.py docs/presentation/bao-cao-lan-1.pptx -o runs/slides/bao-cao-lan-1_20261108/validation/readback.md` → 18 trang, có notes mỗi trang.
- [ ] **Step 4:** Commit `"deck lần 1: speaker notes cho từng trang"`.

### Task 9: Phát hành lần 1

- [ ] **Step 1:** `scripts/regenerate_all.sh && .venv/bin/pytest -q && make -C docs/report check` → tất cả PASS.
- [ ] **Step 2:** Hỏi trưởng nhóm trước khi động tới nhánh: dựng lại `bao-cao-lan-1` như lần trước (reset về `main`, commit phát hành: `\Version` mặc định `lan1`, chỉ giữ `main-lan1.pdf` → `docs/report/bao-cao.pdf` và `bao-cao-lan-1.pptx`), rồi `git push --force-with-lease origin bao-cao-lan-1` và `git push origin main` qua remote SSH `github-personal`.
- [ ] **Step 3:** Báo lại đường dẫn PDF + PPTX, số hình, và những gì (nếu có) dời sang lần 2.
