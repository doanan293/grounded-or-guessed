# Phase 3 — Phân tích, đóng góp và gói artifact: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lấp các tiêu chí "đạt điểm A" còn thiếu (spec §8: tiêu chí 2, 4, 5, 7, 8): kết quả tách theo nhãn, ablation CovGate trên lượt chạy của nhóm, khoảng tin cậy bootstrap theo cụm cho mọi so sánh, phân tích thất bại, macro số liệu cho báo cáo, tài liệu đóng góp + triết lý khoa học, và gói artifact chạy lại được (Docker, cache LLM phát lại offline, hướng dẫn tái hiện từng bảng).

**Architecture:** Không gọi LLM mới. Mọi phân tích đọc `runs/` + `data/`, ghi CSV vào `data/`, bảng/macro vào `docs/report/generated/`, và được thêm vào `scripts/regenerate_all.sh`. Các tham số CovGate đọc từ một chỗ duy nhất (`flx.params`). Gói artifact gồm repo (git) + một tarball cho Zenodo (kết quả lượt chạy + log + cache LLM), phát lại được ở chế độ offline.

**Tech Stack:** Python 3.12, uv venv, pytest, scipy, matplotlib; Docker; LaTeX (tạo macro `\newcommand`).

**Spec:** `docs/superpowers/specs/2026-11-08-semloc-fault-localization-design.md` (Phase 3 mục 3.1–3.3, §8 tiêu chí A, §5 hạ tầng, gói artifact ở bảng sản phẩm). Mục 3.4 (sửa theo góp ý của thầy) chỉ làm được sau buổi báo cáo 18–19/11 nên không nằm trong plan này.

## Global Constraints

- Chấm điểm công bằng: hòa điểm theo hạng trung bình (`ties="average"`), mẫu số cố định — chương trình thiếu là trượt.
- Tham số CovGate chỉ chọn trên dev (`covgate_eval.tune`); test không bao giờ dùng để chọn.
- Chỉ dùng lượt chạy đã xong và healthy (`rq3_families.usable_runs`).
- Seed cố định `20261108` cho mọi lấy mẫu / bootstrap; bootstrap 10.000 lần, CI 95% percentile.
- Không commit `.env`, `infra/proxy/config.yaml`, file OAuth; không phân phối lại tài liệu môn học hay `template-vi.pptx`.
- Không gọi LLM (chế độ offline); mọi số trong tài liệu phải truy về một file trong `data/`.
- Ngôn ngữ: tài liệu phân tích tiếng Việt; tên cột / macro / định danh tiếng Anh.

## Review Focus

1. **Nhãn theo ground truth đã sửa** — chương trình có GT bị sửa có thể đổi nhãn (vd. `not_executed` → `semantic`); tách theo nhãn phải dùng nhãn của *đúng* GT đang chấm. Pin bằng `test_labels_follow_the_ground_truth_variant` (Task 1).
2. **Tham số `grounded_prior` bị rơi** khi đọc tham số đã chọn trên dev. Pin bằng `test_chosen_params_keeps_every_covgate_knob` (Task 2).
3. **Bootstrap gộp lặp như mẫu độc lập** — 3 lần lặp trên cùng chương trình không phải 3 mẫu; đơn vị lấy mẫu là chương trình (hoặc cụm template). Pin bằng `test_paired_diff_ci_resamples_programs_not_repeats` (Task 3).
4. **Cache LLM chứa bí mật** (khóa, email, token) trước khi công bố. Pin bằng `test_secret_scan_flags_keys_and_emails` (Task 6).
5. **Phát lại offline âm thầm gọi mạng** khi cache thiếu. Pin bằng `test_offline_mode_never_calls_the_api` (Task 6).

---

### Task 1 (P3-1): Tách kết quả theo nhãn và tập con executable, theo từng ground truth

**Files:**
- Modify: `src/flx/labels.py` (thêm `labels_for`)
- Modify: `scripts/rq2_ours.py` (cột `subset`: `all`, `semantic`, `coverage_revealed`, `not_executed`, `executable`)
- Modify: `scripts/decompose.py` (subset `executable` dùng `labels_for(gt)`)
- Modify: `scripts/make_tables.py` (thêm `rq2_by_label.tex`)
- Test: `tests/test_labels.py`

**Interfaces:**
- Produces: `labels_for(gt: dict[str, list[int]], cov_dir: Path) -> dict[str, str]` — nhãn `label_from_coverage(load(cov_dir/f"{p}.json"), gt[p])` cho mỗi chương trình có trong `gt`. `executable` = nhãn khác `not_executed`.
- Produces: `data/rq2_ours.csv` thêm cột `subset` (các dòng cũ thành `subset=all`); `docs/report/generated/rq2_by_label.tex`.

- [ ] **Step 1: Viết test** `test_labels_follow_the_ground_truth_variant`: ma trận độ phủ giả — test fail chạy dòng 5 và 6, test pass chạy dòng 5 và 7. Kỳ vọng: GT `[9]` → `not_executed`; `[5]` → `semantic`; `[6]` → `coverage_revealed`; `[7]` → `not_executed`; cùng một chương trình đổi nhãn khi GT gốc `[9]` được sửa thành `[5]`.
- [ ] **Step 2: Chạy** `.venv/bin/pytest tests/test_labels.py -q` → FAIL (`labels_for` chưa có).
- [ ] **Step 3: Cài `labels_for`**; trong `rq2_ours.py` lặp thêm theo subset (metrics trên danh sách con, McNemar/Wilcoxon như cũ); trong `decompose.py` thay `labels[p]` (nhãn GT gốc) bằng `labels_for(gt)`.
- [ ] **Step 4: Chạy** test → PASS; chạy `scripts/rq2_ours.py` và kiểm tra dòng `subset=all` trùng hệt các giá trị cũ (so bằng `git diff` sau khi lọc cột mới).
- [ ] **Step 5: Thêm `rq2_by_label_table()`** (Acc@1/Acc@3 của SemLoc, CovGate, LLM + độ phủ, SBFL theo 4 subset, GT đã sửa, kèm n mỗi subset); chạy `make_tables.py`; commit.

### Task 2 (P3-2): Một nguồn tham số + ablation đủ thành phần CovGate trên lượt chạy của nhóm

**Files:**
- Create: `src/flx/params.py`
- Modify: `scripts/rq2_ours.py`, `scripts/rq3_families.py`, `scripts/rq3_bugsinpy.py`, `scripts/pareto_data.py` (bỏ các `chosen_params` / `covgate_params` riêng)
- Test: `tests/test_params.py`

**Interfaces:**
- Produces: `chosen_params(gt_name: str, config: str = "semloc_gemini_T0.8") -> dict` đọc `data/rq_gt_sensitivity.csv`, trả về **đủ** `gate, lam, no_prior, grounded_prior`; `KeyError` nếu không có dòng.
- Produces: biến thể mới trong `rq2_ours.py`: `gate_only`, `lam_only` (λ = λ đã chọn, hoặc 0,01 nếu λ chọn = 0), `grounded_prior_only`; dùng `semloc_attribute` cho `grounded_prior`.

- [ ] **Step 1: Viết test** `test_chosen_params_keeps_every_covgate_knob` (CSV tạm có dòng params `{"gate": false, "lam": 0.5, "no_prior": false, "grounded_prior": true}` → trả về đúng 4 khóa, `grounded_prior is True`) và `test_chosen_params_unknown_gt_raises`.
- [ ] **Step 2: Chạy** `.venv/bin/pytest tests/test_params.py -q` → FAIL.
- [ ] **Step 3: Cài `flx/params.py`**, thay 4 bản sao trong scripts bằng import; thêm 3 biến thể ablation vào `semloc_variants` của `rq2_ours.py`.
- [ ] **Step 4: Chạy** toàn bộ test → PASS; `scripts/regenerate_all.sh` → mọi CSV cũ không đổi ngoài dòng mới của `rq2_ours.csv` (kiểm `git diff --stat`).
- [ ] **Step 5: Commit.**

### Task 3 (P3-3): Khoảng tin cậy bootstrap theo chương trình / cụm cho mọi so sánh cặp

**Files:**
- Modify: `src/flx/stats.py` (thêm `paired_diff_ci`)
- Modify: `scripts/rq2_ours.py`, `scripts/rq3_renamed.py`, `scripts/rq3_bugsinpy.py` (cột `d_acc{1,3}`, `d_acc{1,3}_lo/_hi` theo cụm; giữ `p_acc*_max` và thêm `p_acc*_all` = 3 p ghép bằng `;`)
- Modify: `scripts/make_tables.py` (bảng RQ2/RQ3b hiển thị Δ [CI])
- Test: `tests/test_stats.py`

**Interfaces:**
- Produces: `paired_diff_ci(a: list[dict[str, bool]], b: list[dict[str, bool]], programs: list[str], clusters: dict[str, int] | None, k_boot: int = 10000, seed: int = 20261108) -> tuple[float, float, float]` — (Δ, lo, hi) của Acc(a) − Acc(b); mỗi phần tử danh sách là một lần lặp `{program: hit}`; mỗi chương trình lấy trung bình hit qua các lần lặp **trước** khi bootstrap; `clusters=None` → mỗi chương trình một cụm.
- Ruling sẵn: không dùng Cochran–Mantel–Haenszel vì 3 lần lặp trên cùng chương trình không độc lập; CI bootstrap theo cụm trả lời cả "khác biệt" lẫn "không khác biệt" (CI hẹp quanh 0).

- [ ] **Step 1: Viết test** `test_paired_diff_ci_resamples_programs_not_repeats` (a luôn trúng, b luôn trượt trên 10 chương trình × 3 lặp → Δ = 1,0 và CI = (1,0; 1,0); nhân bản thêm lặp không làm CI hẹp lại so với 1 lặp) và `test_paired_diff_ci_cluster_widens` (chương trình cùng cụm → CI rộng hơn hoặc bằng không cụm).
- [ ] **Step 2: Chạy** test → FAIL.
- [ ] **Step 3: Cài `paired_diff_ci`** (tái dùng logic của `cluster_bootstrap_ci` trên chênh lệch theo chương trình); thêm cột vào 3 script; cụm từ `data/semfault_templates.csv` cột `cluster_t0.8` (BugsInPy: mỗi lỗi một cụm).
- [ ] **Step 4: Chạy** test → PASS; `regenerate_all.sh`; kiểm tra RQ3b: CI của Δ Acc@1 (SemLoc, đổi tên) phủ 0 — ghi số vào ledger.
- [ ] **Step 5: Commit.**

### Task 4 (P3-4): Phân tích thất bại — chọn ca có hệ thống, rồi phân nhóm nguyên nhân

**Files:**
- Create: `src/flx/failures.py`, `scripts/failure_cases.py`, `data/failure_signals.csv`, `data/failure_cases.csv`
- Create: `docs/analysis/failure-analysis.md`
- Test: `tests/test_failures.py`

**Interfaces:**
- Consumes: `rq3_families.run_ranks(run, gt, progs, method, params)`; `ranks_from_list` (rq2_ours); `labels_for` (Task 1); `chosen_params` (Task 2).
- Produces: `signals(program) -> dict` với khóa `guess_hit` (dòng LLM đoán ∈ GT, đa số trong 3 lặp), `semloc_top1`, `semloc_top3`, `spectrum_rank` (hạng GT khi bỏ thưởng, trung vị qua lặp), `llmcov_top3`, `label`, `gt_status` (confirmed/corrected/unverified/unverifiable), `cluster`.
- Produces: `category(sig: dict) -> str`, một trong: `guess_right` · `rescued_by_spectrum` (đoán sai, SemLoc top-3 trúng) · `prior_hurts` (phổ xếp GT hạng 1 nhưng thưởng đẩy dòng đoán sai lên trên) · `coverage_only_wins` (SemLoc trượt top-3, LLM + độ phủ trúng) · `all_miss` · `gt_suspect` (GT unverified/unverifiable và mọi phương pháp trượt).
- Produces: `select(cases: list[dict], per_category: int, seed: int) -> list[dict]` — lấy tối đa `per_category` ca mỗi nhóm, ưu tiên các cụm template khác nhau.

- [ ] **Step 1: Viết test** `test_category_rules` (một dict signal cho mỗi nhóm → đúng nhóm; thứ tự ưu tiên `gt_suspect` trước `all_miss`) và `test_select_spreads_clusters` (6 ca cùng nhóm, 3 cụm, `per_category=3` → 3 cụm khác nhau, cố định với seed).
- [ ] **Step 2: Chạy** test → FAIL.
- [ ] **Step 3: Cài** `failures.py`; `scripts/failure_cases.py` ghi `data/failure_signals.csv` (200 chương trình test, GT đã sửa, đủ cột signal + category) và `data/failure_cases.csv` (`select(..., per_category=4)` → 15–24 ca, kèm mã nguồn hàm đích có đánh số dòng, GT, dòng đoán, top-5 SemLoc, top-5 LLM + độ phủ, ràng buộc bị vi phạm nhiều nhất).
- [ ] **Step 4: Chạy** test → PASS; chạy script; đếm số chương trình mỗi nhóm.
- [ ] **Step 5: Viết `docs/analysis/failure-analysis.md`**: bảng đếm nhóm trên 200 chương trình; với mỗi ca đã chọn — 2–4 câu nguyên nhân rút từ mã nguồn + ràng buộc + độ phủ (không suy đoán ngoài bằng chứng); cuối tài liệu: các mẫu nguyên nhân lặp lại và hệ quả cho thiết kế công cụ. Thêm `failure_cases.py` vào `regenerate_all.sh`. Commit.

### Task 5 (P3-5): Macro số liệu cho bài báo và báo cáo

**Files:**
- Create: `scripts/make_numbers.py`, `docs/report/generated/numbers.tex`
- Modify: `scripts/regenerate_all.sh`
- Test: `tests/test_make_numbers.py`

**Interfaces:**
- Produces: `macro_name(*parts: str) -> str` — ghép CamelCase chỉ chữ cái (`("rq2", "llm_coverage", "acc3")` → `\RqTwoLlmCoverageAccThree`; chữ số viết bằng chữ tiếng Anh vì tên macro LaTeX không chứa số).
- Produces: `numbers.tex` — một `\newcommand{\X}{49.3}` cho mỗi số tiêu đề: RQ1 (13/13, thưởng ẩn −12,8 pp), GT (56 dòng trống, 65 không thực thi, 82/46/11/111), RQ2 (mọi phương pháp × Acc@1/3/5, Δ và CI từ Task 3), RQ3a/b/c, phân rã Shapley, chi phí (token/chương trình, tỷ lệ lượt gọi CF), đếm nhóm thất bại (Task 4).

- [ ] **Step 1: Viết test** `test_macro_name_has_no_digits` và `test_numbers_tex_is_generated_from_csv` (CSV tạm → macro đúng giá trị, định dạng `xx.x`).
- [ ] **Step 2: Chạy** test → FAIL.
- [ ] **Step 3: Cài `make_numbers.py`**; thêm vào cuối `regenerate_all.sh`.
- [ ] **Step 4: Chạy** test → PASS; biên dịch một tài liệu thử `\input{numbers.tex}` (pdflatex rc=0, không trùng tên macro).
- [ ] **Step 5: Commit.**

### Task 6 (P3-6): Phát lại LLM offline + xuất log/cache đã kiểm tra bí mật

**Files:**
- Modify: `src/flx/llm_gateway.py` (biến môi trường `FLX_LLM_OFFLINE=1`: cache thiếu → `LLMUnavailable("offline cache miss: <key>")`, không gọi mạng)
- Create: `src/flx/secrets_scan.py`, `scripts/export_artifact.py`
- Test: `tests/test_llm_gateway.py`, `tests/test_secrets_scan.py`

**Interfaces:**
- Produces: `scan(text: str) -> list[str]` — tên các mẫu khớp: khóa OpenAI (`sk-`), Google (`AIza`), GitHub (`ghp_`/`gho_`), Anthropic (`sk-ant-`), `Bearer <token>`, địa chỉ email, JWT (`eyJ...`).
- Produces: `scripts/export_artifact.py --out dist/` → `dist/grounded-or-guessed-runs-<YYYYMMDD>.tar.gz` gồm: `runs/<run>/{scores,refined_base_cf,constraints,results_cf_base}` của mọi lượt có trong `data/runs.csv` với `healthy=True`, `runs/bip_semloc/`, `runs/llm_log.jsonl` (chỉ run_id có trong `runs.csv`), `runs/llm_cache/<key>.json` cho các key của log đó, `MANIFEST.json` (sha256 từng file). Dừng với mã lỗi ≠ 0 nếu `scan` khớp bất kỳ file nào.

- [ ] **Step 1: Viết test** `test_offline_mode_never_calls_the_api` (monkeypatch client gọi mạng → raise; `FLX_LLM_OFFLINE=1`, cache trống → `LLMUnavailable` và client không được gọi; cache có → trả nội dung cache) và `test_secret_scan_flags_keys_and_emails` (mỗi mẫu một chuỗi dương tính; một đoạn JSON phản hồi LLM bình thường → `[]`).
- [ ] **Step 2: Chạy** test → FAIL.
- [ ] **Step 3: Cài** chế độ offline, `secrets_scan.py`, `export_artifact.py`.
- [ ] **Step 4: Chạy** test → PASS; chạy `export_artifact.py`; giải nén vào thư mục tạm, chạy một lượt `run_semloc.sh` ngắn trên 3 chương trình với `FLX_LLM_OFFLINE=1 FLX_LLM_CACHE_DIR=<tạm>/runs/llm_cache` và run_id của `semloc_test_gemini_r1` → điểm khớp `scores/` gốc, 0 lượt gọi mạng. Nếu cache miss vì prompt chứa đường dẫn tuyệt đối của workdir: ghi ruling, chạy lại trong một workdir cùng đường dẫn với bản gốc và ghi trong `REPRODUCE.md` rằng mức (2) cần đúng đường dẫn đó.
- [ ] **Step 5: Commit** (không commit `dist/`; thêm `dist/` vào `.gitignore`).

### Task 7 (P3-7): Docker + hướng dẫn tái hiện từng bảng + metadata trích dẫn

**Files:**
- Create: `Dockerfile`, `.dockerignore`, `REPRODUCE.md`, `CITATION.cff`, `.zenodo.json`
- Modify: `README.md` (liên kết REPRODUCE.md, trích dẫn)

**Interfaces:**
- Consumes: tarball của Task 6; `scripts/regenerate_all.sh`.
- Produces: image chạy được `pytest` và `regenerate_all.sh` không cần mạng/LLM; `REPRODUCE.md` 4 mức: (0) bảng từ CSV đã commit (`make_tables.py`), (1) CSV từ tarball kết quả (`regenerate_all.sh`), (2) chạy lại SemLoc từ cache offline, (3) chạy mới qua proxy; mỗi bảng/hình của bài → lệnh + file nguồn.

- [ ] **Step 1: Viết Dockerfile** (`python:3.12-slim`, `uv`, `poppler-utils`, cài `-e .[dev] -e third_party/semloc`, `ENV FLX_LLM_OFFLINE=1`, `CMD pytest -q`).
- [ ] **Step 2: Chạy** `docker build -t grounded-or-guessed .` rồi `docker run --rm grounded-or-guessed` → toàn bộ test PASS.
- [ ] **Step 3: Chạy** `docker run --rm -v $PWD/dist:/dist grounded-or-guessed bash -c "cp -r data /tmp/data0 && tar xzf /dist/*.tar.gz && scripts/regenerate_all.sh && diff -r -x '*.pdf' /tmp/data0 data"` → exit 0 (CSV tái tạo trùng hệt; image không chứa `.git`).
- [ ] **Step 4: Viết** `REPRODUCE.md`, `CITATION.cff` (tác giả nhóm, tiêu đề bài), `.zenodo.json` (license MIT, keywords từ `docs/literature/keywords.md`); cập nhật README.
- [ ] **Step 5: Commit.** DOI Zenodo cần chủ dự án tạo tài khoản và bật tích hợp GitHub → ghi vào ledger, không làm thay.

### Task 8 (P3-8): Đóng góp và triết lý khoa học

**Files:**
- Create: `docs/analysis/contributions.md`

**Interfaces:**
- Consumes: mọi CSV ở trên, `failure-analysis.md`, `numbers.tex` (tên macro tương ứng ghi cạnh mỗi số).

- [ ] **Step 1: Viết danh sách đóng góp** (5–6 mục, mỗi mục: một câu khẳng định, bằng chứng = file + số, giới hạn) theo câu đóng góp ở spec §8 tiêu chí 1.
- [ ] **Step 2: Viết phần triết lý khoa học**: chứng cứ thực thi là trọng tài (ground truth kiểm chứng bằng thực thi, LLM chỉ đề xuất); tái hiện ≠ lặp lại số (audit cách chấm, thành phần ẩn); phân rã "grounded vs guessed" như một cách đo đóng góp của bằng chứng; khả năng bác bỏ (mỗi khẳng định kèm điều kiện làm nó sai); Threats to Validity (GT kiểm chứng có thể thiên về phương pháp dựa trên độ phủ, hàm đích BugsInPy chọn từ GT, mức suy luận mặc định khác nhau giữa nhà cung cấp, Claude qua proxy yếu hơn, youtube-dl_33 có 2 test fail do môi trường).
- [ ] **Step 3: Đối chiếu**: mỗi số trong tài liệu khớp `numbers.tex` (grep từng giá trị); không có khẳng định nào thiếu file nguồn.
- [ ] **Step 4: Commit.**
