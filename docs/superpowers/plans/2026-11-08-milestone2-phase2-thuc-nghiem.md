# Mốc 2 — Phase 2: thực nghiệm đầy đủ (RQ1–RQ3) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Có đủ số liệu cho RQ1 (tái hiện + audit), RQ2 (CovGate, lặp 3 lần, kiểm định) và RQ3 (BugsInPy, code đổi tên, các họ model) — làm nhanh nhất có thể, mục tiêu có kết quả RQ1–RQ2 trước 18/11.

**Architecture:** Mọi phép chấm điểm mới (SBFL đầy đủ, CovGate, xếp hạng có xử lý hòa) là hàm thuần trong `src/flx/` đọc đầu ra đã có của SemLoc (`scores/`, `constraints/`, `refined_base_cf/`) cộng một **ma trận độ phủ theo từng test** do nhóm tự tính và lưu trong `data/coverage/`. Vì vậy CovGate thành phần 1–2 chấm được trên log công bố mà không tốn LLM; lượt chạy LLM mới chỉ dùng cho lặp, CF-aware, baseline LLM và RQ3. Mỗi lượt chạy = một run_id = một workdir (Task M1 đã khoá điều này).

**Tech Stack:** Python 3.12, pytest, scipy (thống kê), SemLoc vendored, flx gateway + proxy.

**Spec:** `docs/superpowers/specs/2026-11-08-semloc-fault-localization-design.md`

## Global Constraints

- Mọi model chạy ở **mức suy luận mặc định** của nhà cung cấp (không quy tắc ép trong `infra/proxy/config.yaml`); báo cáo theo `infra/proxy/MODELS.md`.
- Model: chính `gemini-3.8-flash-high` (served `gemini-3.8-flash-n`); RQ3c: `claude-sonnet-5-5`, `gpt-6-luna`, `gpt-oss-120b-medium`, `gemini-3.5-flash-lite`; kiểm tra tái hiện: `claude-sonnet-4-6`.
- Cấu hình SemLoc: `--temperature 0.8 --steps 1,3,4,5,6,8 --cf-on-base` (qua `scripts/run_semloc.sh`).
- Dev 50 / test 200 cố định trong `data/split.json`; **mọi tham số của CovGate chỉ được chọn trên dev**, báo cáo trên test.
- Lặp **3 lần** mỗi cấu hình LLM chính (run_id `…_r1/_r2/_r3`, workdir riêng); thiếu quota thì cắt theo spec §8: GPT → số lần lặp (không dưới 3) → BugsInPy.
- Chỉ số: Acc@1/3/5, median rank, %Susp, lượt gọi/token; báo cáo **cả tập đầy đủ và tập 185 chương trình có dòng lỗi thực thi được**, và cả cách chấm của tác giả (lạc quan) lẫn cách chấm công bằng (hòa = trung bình).
- Kiểm định: McNemar (đúng/sai Top-k, ghép cặp theo chương trình), Wilcoxon (thứ hạng), effect size; không viết "tốt hơn" nếu p ≥ 0,05.
- Mỗi lượt chạy phải `flx.run_health` healthy trước khi số liệu được dùng.
- Không sửa logic/prompt SemLoc; mọi thay đổi xếp hạng nằm trong `flx`, không trong `third_party/`.

## Review Focus

1. **Rò rỉ dev/test** — tham số CovGate (λ, K) chọn trên test thay vì dev → số RQ2 bị thổi phồng. Pin bằng `test_tune_uses_only_dev` (Task M5).
2. **Dòng lỗi không thực thi được / dòng trống** — cổng độ phủ sẽ loại chúng; phải báo cáo riêng, không âm thầm hạ Acc. Pin bằng `test_gate_drops_unexecuted_fault_is_reported` (Task M3).
3. **Đổi tên làm thay đổi hành vi** — biến thể đổi tên phải cho đúng kết quả pass/fail từng test như bản gốc và giữ số dòng. Pin bằng `test_renamed_preserves_lines_and_outcomes` (Task M8).
4. **Hòa điểm** — xếp hạng lạc quan theo thứ tự dòng làm SBFL/CovGate trông tốt/xấu giả tạo. Pin bằng `test_rank_average_ties` (Task M2).
5. **Lượt chạy thiếu chương trình** — chương trình không chạy được phải tính là trượt với mẫu số cố định, không bị bỏ. Pin bằng `test_missing_program_counts_as_miss` (Task M2).

---

## Phát hiện mới định hướng kế hoạch (08/11)

- Trong mã SemLoc công bố, **Acc@k lấy từ `scores/ranked_lines`; bước CF không đổi xếp hạng** (đã kiểm trên pilot: top-1 và best_rank giống hệt 50/50 với `results/` và `results_cf_base/`). Mức "+12 pp nhờ CF" trong bài so hai lượt chạy LLM khác nhau. → RQ1 audit + **CovGate thành phần 3 đổi thành "CF thật sự xếp hạng lại"**: dòng gắn với ràng buộc Primary/Secondary lên trước.
- SemLoc cộng **+1,2 điểm cho dòng LLM tự đoán** (`apply_fault_line_prior`, không thấy trong bài). → thêm ablation "không prior".

## File

```
src/flx/coverage.py      # ma trận độ phủ theo test (dùng helper SemLoc), lưu/đọc JSON
src/flx/ranking.py       # rank_of(): hòa lạc quan/trung bình/bi quan; metrics_table() mẫu số cố định
src/flx/sbfl.py          # ochiai, dstar(*=2) từ ma trận độ phủ
src/flx/covgate.py       # CovGate: gate, combine(λ), cf_rerank, no_prior
src/flx/stats.py         # mcnemar, wilcoxon, effect size
src/flx/rename.py        # biến thể đổi tên giữ số dòng
src/flx/verify_gt.py     # kiểm chứng/sửa ground truth bằng vá một dòng + chạy test
src/flx/direct_cov.py    # baseline LLM + bằng chứng độ phủ
src/flx/templates.py     # cụm khuôn mẫu AST của benchmark
scripts/coverage_all.py, scripts/covgate_eval.py, scripts/run_matrix.sh, scripts/make_tables.py
data/coverage/semfault/<p>.json, data/rq*.csv, docs/report/generated/*.tex
```

---

### Task 1 (M1): Ma trận độ phủ theo test cho SemFault-250 (08–09/11)

**Files:** Create `src/flx/coverage.py`, `scripts/coverage_all.py`, `data/coverage/semfault/*.json`; Test `tests/test_coverage.py`

**Interfaces:**
- Consumes: `flx._semloc`, `baselines.get_test_ids`, `baselines._coverage_for_test` (với retry như `flx.labels`).
- Produces: `CoverageMatrix = {"program": str, "tests": [{"id": str, "passed": bool, "lines": list[int]}]}`; `collect(program, src, test) -> CoverageMatrix`; `load(path) -> CoverageMatrix`. Refactor `flx.labels.label_program` dùng `collect` (một nguồn sự thật).

- [ ] Test `test_collect_mini` trên fixture `mini`: 4 test, `passed` = [T, T, F, F], test_c chứa dòng 7, test_d chứa dòng 4. FAIL → cài → PASS.
- [ ] Test `test_labels_unchanged_after_refactor`: `label_program` trên fixture cho đúng 4 kết quả cũ (các test cũ phải vẫn xanh).
- [ ] Chạy `scripts/coverage_all.py --workers 8` → 250 file; đối chiếu `flx.labels` tính từ ma trận cho đúng `data/semfault_labels.csv` (0 khác biệt). Commit.

### Task 2 (M2): Xếp hạng có xử lý hòa + bảng chỉ số mẫu số cố định (09/11)

**Files:** Create `src/flx/ranking.py`; Test `tests/test_ranking.py`

**Interfaces:**
- Produces: `rank_of(scores: dict[int, float], faulty: list[int], ties: Literal["first","average","worst"]) -> float | None` (`first` = cách tác giả: thứ tự ổn định); `metrics(ranks: dict[str, float|None], programs: list[str], ks=(1,3,5)) -> dict` — chương trình thiếu trong `ranks` = trượt; Acc@k với hạng thực (average rank ≤ k).

- [ ] Tests: `test_rank_average_ties` ({10:.5, 11:.5, 12:.1}, lỗi 11 → first=2, average=1.5, worst=2); `test_missing_program_counts_as_miss` (2 chương trình, 1 thiếu → Acc@1 = 0.5 nếu chương trình còn lại đứng 1); `test_unranked_fault_is_none`.
- [ ] FAIL → cài → PASS → commit.

### Task 3 (M3): SBFL đầy đủ và CovGate (09–10/11)

**Files:** Create `src/flx/sbfl.py`, `src/flx/covgate.py`; Test `tests/test_sbfl.py`, `tests/test_covgate.py`

**Interfaces:**
- Consumes: `CoverageMatrix` (M1); SemLoc score JSON (`line_scores`, `fault_line_pred`, `constraint_scores`); constraints JSON + `spectrum.attribute_to_statements` (cho CF rerank); `refined_base_cf/<p>.json`.
- Produces:
  - `sbfl_scores(cov, formula: Literal["ochiai","dstar"]) -> dict[int, float]` (DStar với * = 2; dòng không được test fail nào chạy qua có điểm 0 và không được xếp).
  - `covgate_scores(semloc: dict, cov: CoverageMatrix, *, gate: bool, lam: float, no_prior: bool, cf: list|None, constraints_src: tuple|None) -> dict[int, float]`:
    `no_prior` trừ lại 1,2 tại `fault_line_pred`; `gate` bỏ dòng mà không test fail nào chạy qua; `lam` cộng `lam × ochiai` (chỉ dùng để phá hòa khi λ nhỏ); `cf` (nếu có) tính lại line score chỉ từ ràng buộc Primary/Secondary không bị prune rồi đặt các dòng đó lên trước, giữ thứ tự cũ cho phần còn lại.
- [ ] Tests SBFL: `test_ochiai_matches_published` (ad_mix: điểm khớp `third_party/semloc/results/RQ1/sbfl_ochiai/ad_mix.json` ±1e-9 trên mọi dòng); `test_dstar_formula` (ef=2, ep=1, nf=0 → 4.0).
- [ ] Tests CovGate: `test_gate_drops_lines_not_hit_by_failing`; `test_gate_drops_unexecuted_fault_is_reported` (lỗi ở dòng không thực thi → `rank_of` = None, và hàm trả kèm cờ `fault_gated=True` qua `covgate_explain`); `test_no_prior_subtracts_bonus`; `test_lambda_breaks_ties_only_small`; `test_cf_rerank_puts_primary_lines_first`.
- [ ] FAIL → cài → PASS → commit.

### Task 4 (M4): RQ1 đầy đủ — tái hiện + audit (10/11)

**Files:** Create `scripts/rq1_audit.py`, `data/rq1_audit.csv`

- [ ] Bảng: mỗi cấu hình công bố × {tác giả (first), công bằng (average)} × {250, 185}; SBFL Ochiai/DStar tính lại từ M1 (phải khớp log Ochiai công bố); DD theo cách tác giả và DD công bằng (hit = hạng trung bình của tập minimal); thêm dòng "SemLoc không prior" (M3 `no_prior`) và "CF có/không" chứng minh CF không đổi Acc@k trên log công bố (scores ≡ results).
- [ ] Test khói `test_rq1_audit_reproduces_author_numbers` (cột tác giả trên 250 = `data/rq1a_table.csv`). Commit.

### Task 5 (M5): CovGate trên log công bố — chọn tham số trên dev, báo cáo trên test (10–11/11)

**Files:** Create `scripts/covgate_eval.py`, `data/rq2_published.csv`; Test `tests/test_covgate_eval.py`

**Interfaces:** `tune(programs_dev, grid) -> dict` chọn (gate, λ, no_prior) theo Acc@3 rồi Acc@1 trên dev; `evaluate(config, programs_test) -> rows`.
- [ ] `test_tune_uses_only_dev`: truyền dữ liệu giả có chương trình test "đầu độc" (đổi λ tốt nhất nếu bị nhìn thấy) → tham số chọn được không đổi.
- [ ] Lưới: gate ∈ {F,T}, λ ∈ {0, 0.01, 0.1, 0.5}, no_prior ∈ {F,T}; áp lên 6 cấu hình SemLoc công bố; kiểm định McNemar CovGate vs SemLoc trên test. Commit.

### Task 6 (M6): Chạy lặp SemLoc Gemini trên test 200 × 3 (khởi chạy 10/11, chạy nền ~5–9 giờ)

**Files:** Create `scripts/run_matrix.sh`; dữ liệu `runs/semloc_test_gemini_r{1,2,3}/`

- [ ] `run_matrix.sh <config_name> <model> <split:dev|test|file> <reps>`: tạo workdir `runs/<config>_r<i>` bằng `flx.workdir`, gọi `run_semloc.sh` với run_id = tên workdir, dừng nếu không healthy. `WORKERS=8`.
- [ ] Đo sau run 1: lượt gọi, token, 429; nếu quota không đủ cho r2/r3 → ghi ruling và cắt theo Global Constraints.
- [ ] Mỗi run healthy → commit danh sách run + `flx.run_health` output vào `data/runs.csv` (run_id, model, split, n, calls, tokens, healthy).

### Task 7 (M7): Baseline LLM hỏi thẳng × 3 + CovGate thành phần 3 trên lượt chạy của nhóm (11–12/11)

**Files:** Create `scripts/run_direct.sh`; `data/rq2_ours.csv`

- [ ] `llm_direct_fl.py` qua gateway trên test 200 × 3 (run_id `direct_test_gemini_r{i}`).
- [ ] CovGate đầy đủ (gate + λ chọn ở M5 + cf_rerank + no_prior ablation) trên 3 lượt chạy M6; McNemar/Wilcoxon cho từng cặp; chi phí CF (số lượt gọi CF bị bỏ nếu chỉ kiểm chứng top-K qua cổng — đếm từ log, không chạy thêm). Commit.

### Task 8 (M8): Biến thể đổi tên SemFault-250 (11–12/11) + chạy SemLoc Gemini × 3 trên test

**Files:** Create `src/flx/rename.py`, `scripts/make_renamed.py`, `data/semfault_renamed/` (programs, testcases, ground_truth.json); Test `tests/test_rename.py`

**Interfaces:** `rename_program(src: str, keep: set[str]) -> str` — đổi tên biến cục bộ, tham số không được test gọi theo keyword, hàm/hằng private (`_x`), xoá nội dung docstring/comment nhưng **giữ nguyên số dòng**; `keep` = tên mà file test dùng (tên hàm chính, keyword args, hằng import).
- [ ] `test_renamed_preserves_lines_and_outcomes` (fixture mini + 3 chương trình thật: cùng số dòng, cùng kết quả pass/fail từng test qua `flx.coverage.collect`); `test_rename_is_deterministic`.
- [ ] Sinh cho 250, kiểm tra tự động 250/250 giữ hành vi (chương trình nào lệch thì loại và ghi lý do). Chạy `run_matrix.sh semloc_renamed_gemini … test 3`. Commit.

### Task 9 (M9): RQ3a BugsInPy — SBFL + SemLoc trên các lỗi youtube-dl (12–14/11)

**Files:** Create `src/flx/bip_run.py`, `scripts/run_bip.sh`; `data/rq3_bugsinpy.csv`

- [ ] SBFL Ochiai/DStar dòng-level trong **hàm chứa lỗi thật** (ground-truth function lấy từ diff) cho 31 lỗi core_ok: ma trận độ phủ theo test của test file BugsInPy.
- [ ] SemLoc trên cùng hàm: gọi `bip_runner.run_semloc_on_bip` bằng python của venv BugsInPy đã cài thêm deps SemLoc; gateway qua `FLX_USE_GATEWAY=1`; × 3 lần. Ngưỡng spec: ≥ 20 lỗi chạy trọn cả SBFL, SemLoc, CovGate; ghi kết quả thực tế.
- [ ] Commit.

### Task 10 (M10): RQ3c — các họ model trên tập con 50 chương trình test × 3 (song song với M7–M9)

- [ ] Tập con cố định 50 chương trình từ test (seed 20261108, phân tầng nhãn) → `data/subset50.json`.
- [ ] `run_matrix.sh` cho `claude-sonnet-5-5`, `gpt-6-luna`, `gpt-oss-120b-medium`, `gemini-3.5-flash-lite`; `claude-sonnet-4-6` × 1 trên dev (kiểm tra tái hiện với log tác giả). CovGate áp lên từng lượt. Commit `data/rq3_families.csv`.

### Task 12 (M12): SemFault-250-verified — ground truth kiểm chứng bằng thực thi (10–12/11, chạy nền)

**Files:** Create `src/flx/verify_gt.py`, `scripts/verify_gt.py`, `data/semfault_verified_gt.json`; Test `tests/test_verify_gt.py`

**Interfaces:**
- Consumes: `flx.coverage.collect` (M1) để chạy test; `flx.llm_gateway.chat`.
- Produces: `candidates(src: str, fn: str, gt_line: int, radius: int = 4) -> list[int]` (dòng trong hàm đích, kể cả dòng trống — nơi có thể chèn); `try_patch(src, line, kind: Literal["replace","insert_after"], new_line: str, test) -> bool` (True nếu **mọi** test pass); `verify(program) -> {"status": "confirmed"|"corrected"|"unverifiable", "lines": list[int], "kind": str, "patch": str}`. LLM (`gemini-3.8-flash-high`, run_id `verify_gt`) chỉ đề xuất dòng thay thế/chèn cho từng ứng viên (tối đa 2 đề xuất/ứng viên); test quyết định.
- [ ] Fixture mới `tests/fixtures/onebug/` (một lỗi duy nhất ở dòng 3, `return a - b` thay vì `return a + b`; 2 test pass, 2 test fail). `test_try_patch_fixes_onebug`: thay dòng 3 bằng `    return a + b` → True; thay dòng 2 bằng một dòng vô hại → False. `test_insert_after_blank_line` (fixture lỗi thiếu mã: chèn một dòng sau dòng trống làm test pass → status corrected, kind insert_after). `test_verify_never_trusts_llm_without_tests` (fake chat trả bản vá sai → unverifiable).
- [ ] Chạy cho cả 250 (185: chỉ thử dòng GT gốc trước; 65: đủ ứng viên). Báo cáo số confirmed/corrected/unverifiable vào `docs/literature/benchmark-notes.md`. Commit.

### Task 13 (M13): Baseline LLM + bằng chứng độ phủ (11/11, chạy nền × 3 trên test)

**Files:** Create `src/flx/direct_cov.py`, `scripts/run_direct_cov.sh`; Test `tests/test_direct_cov.py`

**Interfaces:** `build_prompt(src_fn_numbered: str, failing: list[dict], cov: CoverageMatrix) -> str` (mỗi dòng ghi `[f=<số test fail chạy qua>/p=<số test pass>]`); `parse_ranking(text: str) -> list[int]` (JSON `{"lines": [..]}`; sai định dạng → []); `run(program, model, run_id) -> list[int]`.
- [ ] `test_prompt_annotates_coverage` (fixture mini: dòng 7 có `f=1/p=2`); `test_parse_ranking_tolerates_fences`; `test_parse_ranking_bad_json_empty`.
- [ ] Chạy test 200 × 3 (run_id `direct_cov_test_gemini_r{i}`); thêm vào bảng RQ2 và McNemar với SemLoc/CovGate. Commit.

### Task 14 (M14): Phân tích cấu trúc benchmark (10/11, không LLM)

**Files:** Create `src/flx/templates.py`, `data/semfault_templates.csv`; Test `tests/test_templates.py`
- **Interfaces:** `shape(src: str) -> list[str]` (chuỗi kiểu nút AST, bỏ tên/hằng); `similarity(a, b) -> float` (Jaccard trên 4-gram của `shape`); `clusters(programs: dict[str,str], threshold: float = 0.8) -> dict[str, int]`.
- [ ] `test_renamed_copy_same_shape` (đổi tên biến → similarity 1.0); `test_different_algorithms_low_similarity`.
- [ ] Chạy cho 250, báo cáo số cụm và phân bố; `flx.stats` (M11) thêm bootstrap theo cụm. Commit.

### Task 15 (M15): CovGate thành phần 4 — grounded guess (offline)

**Files:** Modify `src/flx/covgate.py`; Test `tests/test_covgate.py`

**Interfaces:** thêm tham số `grounded_prior: bool` vào `covgate_scores`: khi True, giữ điểm cộng 1,2 tại `fault_line_pred` chỉ nếu dòng đó được ≥1 test fail chạy qua **và** nằm trong tập dòng được gán điểm từ ít nhất một ràng buộc có `ef > 0` (`constraint_scores[c]["ef"] > 0`, qua `attribute`); ngược lại trừ đi 1,2 như `no_prior`.
- [ ] `test_grounded_prior_kept_when_evidence`; `test_grounded_prior_dropped_without_failing_coverage`; `test_grounded_prior_dropped_without_violated_constraint`.
- [ ] Thêm `grounded_prior` vào lưới của `scripts/covgate_eval.py` (vẫn chọn trên dev), chạy lại `data/rq2_published.csv`. Commit.

### Task 16 (M16): Phân rã độ chính xác theo thành phần (offline, sau M6/M7)

**Files:** Create `src/flx/decompose.py`, `scripts/decompose.py`, `data/rq_decomposition.csv`; Test `tests/test_decompose.py`

**Interfaces:** `shapley(value: Callable[[frozenset[str]], float], players: list[str]) -> dict[str, float]` (chính xác, liệt kê mọi tổ hợp); `components = ["prior", "spectrum", "cf", "coverage"]`, value(S) = Acc@1 (và Acc@3) khi chỉ bật các thành phần trong S (spectrum tắt = chỉ còn dự đoán LLM; tất cả tắt = 0).
- [ ] `test_shapley_additive_game` (value = tổng trọng số → Shapley = trọng số); `test_shapley_sums_to_grand_coalition`.
- [ ] Chạy trên 3 lần lặp × 200 test (lượt chạy của nhóm) và trên log công bố; bootstrap CI theo chương trình (và theo cụm từ M14). Commit.

### Task 17 (M17): Checklist đánh giá áp cho mọi phương pháp

**Files:** Create `docs/literature/evaluation-checklist.md`, `data/checklist_matrix.csv`
- [ ] Viết checklist (hòa điểm, mẫu số, GT kiểm chứng, ablation thành phần ẩn, lặp + kiểm định, chi phí); với từng phương pháp (SBFL, LLM hỏi thẳng, LLM + độ phủ, SemLoc, CovGate) ghi số chênh giữa chấm tác giả/công bằng, GT gốc/đã kiểm chứng. Sinh tự động từ `data/`. Commit.

### Task 11 (M11): Thống kê + bảng LaTeX tự sinh (song song, cuối 14/11)

**Files:** Create `src/flx/stats.py`, `scripts/make_tables.py`, `docs/report/generated/*.tex`; Test `tests/test_stats.py`

- [ ] `mcnemar(a: list[bool], b: list[bool]) -> (stat, p)` exact binomial khi b+c < 25; `wilcoxon_paired(x, y) -> (stat, p)` (scipy); `cliffs_delta(x, y) -> float`. Tests với giá trị tính tay: McNemar b=8,c=2 → p = 0.109 (exact two-sided).
- [ ] `cluster_bootstrap_ci(per_program: dict[str, float], clusters: dict[str, int], n=10000, seed=20261108) -> (lo, hi)`; test: mọi chương trình cùng một cụm → CI rộng hơn bootstrap thường.
- [ ] `make_tables.py` sinh `rq1.tex`, `rq2.tex`, `rq3.tex` từ `data/*.csv` (mean ± sd qua 3 lần, p, effect size) và **hình chi phí – độ chính xác** `pareto.pdf` (Acc@3 theo token đầu ra trung bình/chương trình, mỗi phương pháp × model một điểm). Biên dịch `make -C docs/report all` không lỗi. Commit.
