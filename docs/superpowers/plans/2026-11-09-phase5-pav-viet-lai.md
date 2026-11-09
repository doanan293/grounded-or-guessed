# Phase 5 — Ablation, nhãn rà soát, PAV, viết lại bài — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (Native, chủ dự án đã chọn) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đưa ba kết quả mới (ablation độ phủ, SemFault-250 đã rà soát, phương pháp "đề xuất rồi kiểm chứng") vào số liệu, rồi viết lại báo cáo VI, bài báo EN và slide theo câu chuyện mới, cắt lại hai nhánh báo cáo.

**Architecture:** Mọi lượt chạy LLM lưu thứ hạng (`runs/`, `data/rankings/`); nhãn chỉ dùng lúc chấm. Bộ nhãn thứ ba (`reviewed`) là một biến thể của `flx.gt.load_variants`, nên mọi script RQ tự tính thêm cho nó. PAV ghi lại mọi lần thử sửa, nên tham số được chọn trên dev offline (`scripts/pav_eval.py select`) và áp cho test bằng `apply`. Số trong bài là macro từ `scripts/make_numbers.py`.

**Tech Stack:** Python 3.12, pytest, Gemini 3.8 Flash qua gateway `flx.llm_gateway`, XeLaTeX/IEEEtran, `build_deck.py`.

**Spec:** `docs/superpowers/specs/2026-11-08-semloc-fault-localization-design.md` (§3.1 bộ nhãn rà soát, §3.2 mục 2c và 5, §4b PAV, §7 Phase 5, §8 câu đóng góp).

## Global Constraints

- Tham số PAV chỉ chọn trên dev, theo quy tắc cố định trong `scripts/pav_eval.py` (Acc@1 trung bình trên bộ gốc + bộ rà soát; không dùng bộ đã sửa); test và BugsInPy chạy đúng một lần với tham số đã chốt.
- Ba bộ nhãn luôn báo song song: gốc, đã sửa (chỉ kiểm thử quyết định), đã rà soát (LLM rà + nhóm duyệt; góc nhìn độ nhạy, nêu nguy cơ vòng tròn).
- Mô tả việc duyệt nhãn đúng sự thật: Fable rà trước 250 nhãn; 6 thành viên duyệt 111 nhãn, có xem gợi ý của LLM, đồng ý ở cả 111 ca; trưởng nhóm sửa 5 ca có bằng chứng chạy test.
- Không con số gõ tay trong `.tex` (`scripts/lint_numbers.py`); mọi số trong markdown có macro (`scripts/check_claims.py`).
- Bảo mật: không commit `.env`, `infra/proxy/config.yaml`, thông tin OAuth; tài liệu môn học và `template-vi.pptx` không đưa lên repo; push qua `scripts/push_public.sh` dưới tên `doanan293`.

## Review Focus

1. PAV đẩy dòng sai lên đầu nhờ bản sửa bù trừ — tham số `max_size` và số liệu "PAV làm hỏng bao nhiêu ca đúng của bước 1" phải được báo cáo.
2. Nhãn hai dòng làm Acc@k dễ hơn — báo số chương trình có nhãn hai dòng; kết luận không được chỉ dựa vào bộ rà soát.
3. Rò rỉ dev/test — `pav_params.json` được commit trước khi chạy test (thứ tự commit là bằng chứng).
4. Phiên bản `lan1` không được nhắc PAV hay bộ rà soát nếu chương chứa chúng chỉ có từ `lan2` — kiểm bằng `pdftotext`.
5. Câu "một prompt thắng pipeline" phải nêu phạm vi (hàm đơn lẻ, test mô tả rõ ý định) và giới hạn lỗi thật (31 lỗi, CI chạm 0).

---

### Task 1: Ablation độ phủ và bộ nhãn rà soát vào số liệu (xong)

- [x] `flx.direct_cov.build_prompt(coverage=False)`, `--no-coverage` cho SemFault và BugsInPy; 3 lần × 200 test, 3 lần × 31 lỗi thật
- [x] `scripts/ablation_coverage.py` → `data/ablation_coverage.csv` (macro `Abl*`)
- [x] `scripts/build_reviewed_gt.py` → `data/semfault_reviewed_gt.json`; `load_variants()["reviewed"]`
- [x] `regenerate_all.sh` gọi cả hai; test `tests/test_ablation_coverage.py`, `tests/test_reviewed_gt.py`

### Task 2: PAV trên dev, chọn tham số

**Files:** `src/flx/pav.py`, `scripts/run_pav.py`, `scripts/pav_eval.py`; test `tests/test_pav.py`, `tests/test_pav_eval.py`

- [x] Stage 1 trên dev: `direct_tests_dev_gemini_r{1,2,3}`
- [ ] Stage 2 trên dev: `pav_dev_gemini_r{1,2,3}` (k = 3, attempts = 2)
- [ ] `python scripts/pav_eval.py select` → `data/pav_dev_grid.csv`, `data/pav_params.json`; commit trước khi chạy test

### Task 3: PAV trên test và BugsInPy

**Interfaces:** `pav_eval.apply("test")` → `data/rankings/pav_test_gemini_r{i}.json`; `rq2_ours.py` thêm phương pháp `pav`; BugsInPy cần `flx.pav.run_bip` (kiểm chứng trong checkout, lệnh test của `bip_failing_tests`).

- [ ] Chạy stage 2 trên test với `k`, `attempts` đã chốt (stage 1 = `direct_tests_test_gemini_r{i}`)
- [ ] Viết `run_bip` cho PAV (test: ranking giữ nguyên khi không bản sửa nào đạt); chạy 3 lần × 31 lỗi
- [ ] Thêm `pav` vào `rq2_ours.py`, `rq3_bugsinpy.py`, `llm_cost.py`, `make_tables.py`, `make_numbers.py`; thêm số "PAV làm hỏng / cứu bao nhiêu ca so với bước 1"
- [ ] `regenerate_all.sh`, `pytest`, `make -C docs/report check`

### Task 4: Dàn ý câu chuyện mới (cổng duyệt của chủ dự án)

- [ ] Cập nhật `docs/analysis/outline.md`: câu hỏi mở đầu (lập trình viên vẫn đưa test fail cho LLM, nhất là với TDD); RQ2 gồm ablation + PAV; bộ nhãn thứ ba; benchmark bão hòa khi nhãn đúng; giới hạn (hàm đơn lẻ, test mô tả rõ ý định, lỗi thật ít)
- [ ] Chủ dự án duyệt dàn ý

### Task 5: Viết lại báo cáo VI

- [ ] ch1 (đóng góp mới), ch2 (thêm tài liệu về nhãn sai trong benchmark), ch4 (bộ rà soát, 2c, PAV), ch5 (ablation, PAV, ba bộ nhãn), ch6 (nhãn sai), ch7 (đóng góp, mối đe dọa: vòng tròn, người duyệt xem gợi ý, tên test), ch8, phụ lục (prompt PAV), thuật ngữ
- [ ] `make -C docs/report check` (0 overfull, 0 số gõ tay), `pytest -m slow`

### Task 6: Viết lại bài báo EN

- [ ] Abstract, introduction, approach, evaluation, discussion, threats, conclusion theo dàn ý mới; tên bài "Grounded or Guessed: A Reproducibility Study of LLM-Based Semantic Fault Localization"
- [ ] Self-review 5 chiều cập nhật `docs/analysis/self-review.md`

### Task 7: Slide, README, contributions, checklist

- [ ] `build_deck.py` (kết quả, đóng góp, kết luận), `make_decks.sh` 0 lỗi
- [ ] README findings, `docs/analysis/contributions.md`, `docs/literature/evaluation-checklist.md`, `check_claims.py`

### Task 8: Review cuối và cắt lại nhánh

- [ ] Một reviewer độc lập (opus) đọc toàn bộ; sửa
- [ ] Merge `main` vào `bao-cao-lan-1`, `bao-cao-lan-2`, dựng lại PDF; `make check` mỗi nhánh; push cả ba
