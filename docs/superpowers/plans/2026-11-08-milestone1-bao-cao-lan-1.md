# Mốc 1 — Báo cáo lần 1 (18/11) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đến 17/11 có đủ thứ để báo cáo lần 1: tổng quan tài liệu + từ khóa, 3 RQ, hạ tầng thực nghiệm chạy được (SemLoc gốc + proxy LLM), bảng tái hiện RQ1 từ log công bố, nhãn ngữ nghĩa + chia dev/test, số liệu chạy thử SemLoc bằng Gemini trên tập dev, trạng thái BugsInPy, khung LaTeX hai bản, và slide lần 1.

**Architecture:** SemLoc được vendored nguyên trạng vào `third_party/semloc/` (commit `c1db564`), chỉ vá 3 điểm gọi LLM để đi qua một cổng duy nhất `flx.llm_gateway.chat()` (proxy kiểu OpenAI + cache + log). Mã của nhóm là gói Python `flx` trong `src/flx/`, dùng lại hàm của SemLoc chứ không chép logic. Kết quả chạy nằm trong `runs/` (không commit), dữ liệu dẫn xuất nhỏ (nhãn, split, bảng) nằm trong `data/` (commit).

**Tech Stack:** Python 3.12 + uv venv, pytest, openai SDK (≥1.0), SemLoc (tree-sitter, coverage), Docker Compose (`eceasy/cli-proxy-api:v8.0.28`), XeLaTeX, PPTX qua skill ppt-master.

**Spec:** `docs/superpowers/specs/2026-11-08-semloc-fault-localization-design.md`

## Global Constraints

- Mục tiêu điểm A; mọi số liệu đưa lên slide/báo cáo phải sinh từ dữ liệu trong repo, không gõ tay.
- Không sửa logic hay prompt của SemLoc; chỉ vá điểm gọi LLM, và chỉ khi `FLX_USE_GATEWAY=1`. Mọi thay đổi trong `third_party/semloc/` nằm ở commit riêng, sau commit vendored nguyên trạng.
- Ghi nguồn SemLoc (Apache-2.0): giữ `LICENSE.txt`, thêm `third_party/semloc/VENDORED.md` ghi URL + commit `c1db564`.
- Không sửa gì trong `/home/andv/personal/vipharmind/`; proxy chỉ dùng lại volume `vipharmind_cli_proxy_auth` và file `/home/andv/personal/vipharmind/devops/cli-proxy-api/config.yaml`.
- Không commit bí mật: `.env`, khóa API, file đăng nhập OAuth.
- Gemini là mô hình chính; cấu hình SemLoc chính: `--temperature 0.8 --steps 1,3,4,5,6,8 --cf-on-base`.
- Chia dev/test: 50 / 200, seed `20261108`, cố định trong `data/split.json`; mọi thiết kế/chỉnh tham số chỉ dùng dev.
- "Lỗi ngữ nghĩa": dòng lỗi thật được cả ≥1 test fail và ≥1 test pass chạy qua.
- Báo cáo đầy đủ + slide: tiếng Việt. Bài báo: tiếng Anh.
- Quy cách báo cáo VI: Times New Roman 13pt (hoặc bản sao Times), lề trên 3.5 / dưới 3 / trái 2.5 / phải 2.5 cm, giãn dòng 1.5, tiêu đề chương 16pt đậm, đánh số mục tối đa 4 cấp, số trang giữa chân trang.
- Không dùng máy có GPU; mọi LLM qua `http://localhost:8317/v1`.

## Review Focus

1. **Chạy lặp trúng cache** — lần lặp 2, 3 của cùng cấu hình phải gọi LLM thật, không trả lại kết quả lần 1. Pin bằng `test_run_id_separates_cache` (Task 3).
2. **Proxy hết quota / 429 giữa chừng** — cổng phải thử lại có giãn cách rồi báo lỗi rõ ràng (`LLMUnavailable`), không treo vô hạn, không ghi cache rỗng. Pin bằng `test_retries_then_raises` (Task 3).
3. **LLM trả về rỗng** — không được cache câu trả lời rỗng. Pin bằng `test_empty_response_not_cached` (Task 3).
4. **Dòng lỗi không được test fail nào chạy qua / chương trình nhiều dòng lỗi** — gắn nhãn `not_executed` thay vì crash; nhiều dòng lỗi thì chỉ cần một dòng thỏa. Pin bằng `test_label_not_executed` và `test_label_multi_fault_any` (Task 6).
5. **Lỡ commit bí mật** — `.env` và log có thể chứa khóa. Pin bằng `test_no_secrets_tracked` (Task 1).

---

## Cấu trúc file

```
pyproject.toml                    # gói flx (src layout), deps: openai, pytest
.gitignore                        # .env, .venv/, runs/, .superpowers/, __pycache__/, LaTeX aux
.env.example                      # FLX_LLM_BASE_URL, FLX_LLM_API_KEY, FLX_GEMINI_MODEL, ...
third_party/semloc/               # SemLoc @ c1db564 + VENDORED.md (+ 1 commit vá gateway)
infra/proxy/compose.yaml          # cli-proxy-api cho dự án
infra/proxy/MODELS.md             # danh sách model proxy cung cấp + kết quả đo quota
src/flx/__init__.py
src/flx/_semloc.py                # đưa third_party/semloc/src vào sys.path
src/flx/llm_gateway.py            # chat(): proxy + cache + log + retry
src/flx/semloc_results.py         # đọc kết quả SemLoc, tính Acc@k, bảng RQ1a
src/flx/labels.py                 # gắn nhãn semantic / coverage_revealed / not_executed
src/flx/split.py                  # chia dev/test
src/flx/workdir.py                # tạo working dir con cho run_eval
scripts/proxy_smoke.py            # liệt kê model, gọi thử
scripts/quota_probe.py            # đo quota từng model
scripts/run_semloc.sh             # chạy SemLoc qua gateway trên một working dir
tests/...                         # pytest cho từng module
data/semfault_labels.csv, data/split.json, data/rq1a_table.csv, data/bugsinpy_status.csv
runs/                             # output chạy thật, log LLM, cache (gitignored)
docs/literature/                  # ghi chú bài báo, bảng so sánh, từ khóa
docs/report/references.bib        # dùng chung
docs/report/vi/                   # báo cáo đầy đủ tiếng Việt (XeLaTeX)
docs/report/paper-en/             # bài báo tiếng Anh (IEEEtran conference)
docs/presentation/bao-cao-lan-1.pptx
```

---

### Task 1: Khung repo + vendored SemLoc + tái hiện offline (08–09/11)

**Files:**
- Create: `pyproject.toml`, `.gitignore`, `.env.example`, `src/flx/__init__.py`, `src/flx/_semloc.py`, `third_party/semloc/` (copy), `third_party/semloc/VENDORED.md`
- Test: `tests/test_repo_hygiene.py`, `tests/test_semloc_offline.py`

**Interfaces:**
- Produces: `flx._semloc.SEMLOC_ROOT: Path` (= `<repo>/third_party/semloc`), `flx._semloc.ensure_on_path() -> None` (chèn `SEMLOC_ROOT/"src"` vào `sys.path` nếu chưa có). Venv `.venv` có cả `flx` (editable) và SemLoc (editable, lệnh `semloc`).

- [ ] **Step 1:** Copy SemLoc: `git clone https://github.com/jerry729/SemLoc /tmp/semloc && git -C /tmp/semloc checkout c1db564 && rsync -a --exclude .git /tmp/semloc/ third_party/semloc/`; viết `VENDORED.md` (URL, commit, ngày 08/11/2026, giấy phép Apache-2.0, "các thay đổi xem git log của thư mục này"). Commit riêng: `git add third_party/semloc && git commit -m "chore: vendor SemLoc @ c1db564 (Apache-2.0)"`.
- [ ] **Step 2:** Viết `.gitignore` (`.env`, `.venv/`, `runs/`, `.superpowers/`, `__pycache__/`, `*.aux *.log *.out *.toc *.bbl *.blg *.synctex.gz *.fdb_latexmk *.fls *.xdv`), `.env.example` với các biến: `FLX_LLM_BASE_URL=http://localhost:8317/v1`, `FLX_LLM_API_KEY=`, `FLX_GEMINI_MODEL=`, `FLX_CLAUDE_MODEL=`, `FLX_RUN_ID=default`, `FLX_USE_GATEWAY=1`, `WORKERS=4`.
- [ ] **Step 3: Viết test thất bại**

```python
# tests/test_repo_hygiene.py
import subprocess
def test_no_secrets_tracked():
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split()
    assert ".env" not in files
    assert not any(f.startswith("runs/") for f in files)
    assert not any(f.endswith(".json") and "cli-proxy-api" in f for f in files)

# tests/test_semloc_offline.py
import json
from flx._semloc import SEMLOC_ROOT, ensure_on_path
def test_published_summary_matches_paper():
    s = json.loads((SEMLOC_ROOT / "results/RQ1/semloc_claude_T0.8/results/summary.json").read_text())
    assert s["n_programs"] == 250
    assert s["rq1"]["top1_accuracy"] == 0.428
    assert s["rq1"]["top3_accuracy"] == 0.68
def test_semloc_modules_importable():
    ensure_on_path()
    import spectrum, baselines, constraint_inference  # noqa: F401
```

- [ ] **Step 4:** `uv run pytest tests/test_semloc_offline.py -v` → FAIL (`ModuleNotFoundError: flx`).
- [ ] **Step 5:** Viết `pyproject.toml` (tên `flx`, `requires-python = ">=3.10"`, src layout, deps `openai>=1.0`, dev dep `pytest`) và `src/flx/_semloc.py`; tạo venv: `uv venv && uv pip install -e . -e third_party/semloc pytest`.
- [ ] **Step 6:** `uv run pytest tests/ -v` → PASS cả 3 test.
- [ ] **Step 7:** Kiểm tra lệnh của tác giả chạy được offline: `cd third_party/semloc && ../../.venv/bin/semloc report --rq1` in bảng có dòng SemLoc Claude T=0.8 với 42.8 / 68.0; và `../../.venv/bin/semloc demo --skip-llm` chạy xong, in danh sách dòng nghi ngờ. Lưu output vào `runs/offline_check.txt`.
- [ ] **Step 8: Commit** `git add pyproject.toml .gitignore .env.example src tests && git commit -m "feat: flx package skeleton, offline SemLoc reproduction check"`

---

### Task 2: Proxy LLM cho dự án + đo quota (09/11)

**Files:**
- Create: `infra/proxy/compose.yaml`, `infra/proxy/MODELS.md`, `scripts/proxy_smoke.py`, `scripts/quota_probe.py`

**Interfaces:**
- Consumes: `.env` (`FLX_LLM_BASE_URL`, `FLX_LLM_API_KEY`).
- Produces: proxy chạy tại `localhost:8317`; `.env` có `FLX_GEMINI_MODEL`, `FLX_CLAUDE_MODEL` đã chọn; `infra/proxy/MODELS.md` ghi id model và quota đo được.

- [ ] **Step 1:** Viết `infra/proxy/compose.yaml`: service `cli-proxy-api`, image `eceasy/cli-proxy-api:v8.0.28`, cổng `${CLI_PROXY_API_PORT:-8317}:8317`, config từ file `/home/andv/personal/vipharmind/devops/cli-proxy-api/config.yaml` mount vào `/CLIProxyAPI/config.yaml` (read-only), volume external `vipharmind_cli_proxy_auth` → `/root/.cli-proxy-api`, healthcheck như compose của vipharmind. Lấy một khóa trong `api-keys` của config đó điền vào `.env` (`FLX_LLM_API_KEY`), không in ra terminal.
- [ ] **Step 2:** `docker compose -f infra/proxy/compose.yaml up -d` → `docker compose -f infra/proxy/compose.yaml ps` báo `healthy`.
- [ ] **Step 3:** Viết `scripts/proxy_smoke.py`: GET `/v1/models` in danh sách id; với mỗi id truyền qua `--try`, gửi 1 chat "Reply with the single word OK" và in câu trả lời + thời gian. Chạy, chọn model: Gemini ưu tiên `gemini-2.5-pro` (khớp bài báo), nếu không có thì bản Pro mới nhất; Claude ưu tiên `claude-sonnet-4-6`, nếu không có thì Sonnet mới nhất. Ghi vào `.env` và `MODELS.md`.
- [ ] **Step 4:** Viết `scripts/quota_probe.py --model ID --n 40`: gửi tuần tự 40 prompt ngắn khác nhau (không cache), ghi số thành công / 429 / lỗi khác, độ trễ trung vị vào `runs/quota/<model>.json`. Chạy cho model Gemini và Claude đã chọn; chép tóm tắt vào `MODELS.md` (lượt gọi/phút đạt được, có dính 429 không).
- [ ] **Step 5 (chủ dự án làm):** Đăng nhập tài khoản Codex free: chạy `docker compose -f infra/proxy/compose.yaml exec cli-proxy-api ./CLIProxyAPI --help` để xem cờ đăng nhập Codex, rồi chủ dự án tự chạy lệnh đăng nhập bằng `! <lệnh>`. Sau đó chạy lại Step 3 với model GPT. Bước này không chặn các task khác.
- [ ] **Step 6: Commit** `git add infra scripts/proxy_smoke.py scripts/quota_probe.py && git commit -m "feat: project LLM proxy, smoke test and quota probe"`

---

### Task 3: Cổng LLM `flx.llm_gateway` (09–10/11)

**Files:**
- Create: `src/flx/llm_gateway.py`
- Test: `tests/test_llm_gateway.py`

**Interfaces:**
- Produces:
  - `chat(model: str, system: str, user: str, temperature: float = 0.0, max_tokens: int | None = None) -> str`
  - `class LLMUnavailable(RuntimeError)` — hết số lần thử lại
  - `class LLMEmptyResponse(RuntimeError)` — nội dung rỗng/None
  - Biến môi trường: `FLX_LLM_BASE_URL` (mặc định `http://localhost:8317/v1`), `FLX_LLM_API_KEY`, `FLX_RUN_ID` (mặc định `"default"`), `FLX_LLM_CACHE` (`"1"` bật, `"0"` tắt; mặc định bật), `FLX_LLM_CACHE_DIR` (mặc định `runs/llm_cache`), `FLX_LLM_LOG` (mặc định `runs/llm_log.jsonl`), `FLX_LLM_MAX_RETRIES` (mặc định 6).
  - Khóa cache: sha256 của JSON chuẩn hóa `{model, system, user, temperature, run_id}`; mỗi khóa một file `<key>.json`.
  - Mỗi lượt gọi (kể cả trúng cache, kể cả lỗi) ghi 1 dòng JSONL: `ts, run_id, model, temperature, cache_hit, prompt_tokens, completion_tokens, latency_s, error, key`.
  - Thử lại khi gặp `openai.RateLimitError`, `APIConnectionError`, `APITimeoutError`, `InternalServerError`: giãn cách lũy thừa bắt đầu 2 s, trần 60 s.

- [ ] **Step 1: Viết test thất bại** (giả lập client OpenAI bằng monkeypatch một factory `_client()` trong module; dùng `tmp_path` cho cache/log)

```python
def test_cache_hit_skips_api(fake_client, env): ...
    # gọi chat 2 lần cùng tham số -> fake_client.calls == 1; log có 2 dòng, dòng 2 cache_hit=True
def test_run_id_separates_cache(fake_client, env, monkeypatch): ...
    # FLX_RUN_ID="r1" rồi "r2" cùng prompt -> fake_client.calls == 2
def test_cache_disabled(fake_client, env, monkeypatch): ...
    # FLX_LLM_CACHE="0" -> 2 lần gọi = 2 lần API
def test_retries_then_raises(failing_client, env, monkeypatch): ...
    # client luôn ném RateLimitError, FLX_LLM_MAX_RETRIES="2", sleep bị monkeypatch
    # -> raises LLMUnavailable; failing_client.calls == 3; không có file cache
def test_empty_response_not_cached(empty_client, env): ...
    # content None -> raises LLMEmptyResponse; thư mục cache rỗng
def test_log_records_tokens(fake_client, env): ...
    # usage(prompt_tokens=11, completion_tokens=7) -> dòng log có 11, 7, error=None
```

- [ ] **Step 2:** `uv run pytest tests/test_llm_gateway.py -v` → FAIL (`ModuleNotFoundError`).
- [ ] **Step 3:** Cài đặt `src/flx/llm_gateway.py` theo Interfaces; client là `openai.OpenAI(base_url=..., api_key=..., timeout=120)`; ghi cache bằng file tạm + `os.replace` để an toàn khi chạy nhiều worker.
- [ ] **Step 4:** `uv run pytest tests/test_llm_gateway.py -v` → PASS.
- [ ] **Step 5:** Kiểm tra thật qua proxy: `uv run python -c "from flx.llm_gateway import chat; import os; print(chat(os.environ['FLX_GEMINI_MODEL'],'Be terse.','Say OK',0.0))"` (đã `set -a; source .env`) → in `OK`; `runs/llm_log.jsonl` có dòng mới.
- [ ] **Step 6: Commit** `git commit -am "feat: llm gateway with cache, run-id isolation, retries and logging"` (nhớ `git add` file mới).

---

### Task 4: Vá SemLoc dùng cổng LLM (10/11)

**Files:**
- Modify: `third_party/semloc/src/constraint_inference.py` (`_query_openai`, `_query_gemini`, `_query_claude_vertex`, khoảng dòng 309–378), `third_party/semloc/src/llm_direct_fl.py` (`_query_llm`, khoảng dòng 197), `third_party/semloc/src/counterfactual.py` (`_chat_completion`, khoảng dòng 88)
- Test: `tests/test_semloc_gateway_patch.py`

**Interfaces:**
- Consumes: `flx.llm_gateway.chat` (Task 3), `flx._semloc.ensure_on_path` (Task 1).
- Produces: khi `FLX_USE_GATEWAY=1`, mọi lượt gọi LLM của SemLoc đi qua `chat(model, system, user, temperature)` với đúng system prompt và temperature mà SemLoc vốn dùng (counterfactual giữ `temperature=0`); khi biến không đặt, hành vi gốc không đổi.

- [ ] **Step 1: Viết test thất bại**

```python
# monkeypatch flx.llm_gateway.chat bằng hàm ghi lại (model, system, user, temperature) và trả '{"constraints": []}' hoặc 'X'
def test_constraint_inference_routes_through_gateway(...):
    # FLX_USE_GATEWAY=1; constraint_inference._query_gemini("P", "gemini-x", 0.8)
    # -> 1 lượt ghi; system == constraint_inference._SYSTEM_PROMPT; temperature == 0.8
def test_claude_and_openai_branches_route_too(...):
    # _query_claude_vertex(...) và _query_openai(...) cũng ghi lại, không tạo client gốc
def test_direct_fl_routes(...):            # llm_direct_fl._query_llm("P", "gemini-x", 0.3) -> temperature 0.3
def test_counterfactual_routes_temp_zero(...):  # counterfactual._chat_completion("gemini-x","S","U") -> temperature 0.0, system "S"
def test_gateway_off_keeps_original(...):
    # không đặt FLX_USE_GATEWAY; monkeypatch google.genai.Client bằng stub -> stub được gọi, gateway không được gọi
```

- [ ] **Step 2:** `uv run pytest tests/test_semloc_gateway_patch.py -v` → FAIL.
- [ ] **Step 3:** Vá: ở đầu mỗi hàm trên chèn nhánh `if os.environ.get("FLX_USE_GATEWAY") == "1":` gọi `flx.llm_gateway.chat` rồi `return` (giữ nguyên `.strip()` ở counterfactual). Không đổi gì khác.
- [ ] **Step 4:** `uv run pytest tests/ -v` → PASS toàn bộ.
- [ ] **Step 5:** `git diff --stat third_party/semloc` chỉ chạm 3 file trên. **Commit** `git commit -am "patch(semloc): route LLM calls through flx gateway when FLX_USE_GATEWAY=1"`.

---

### Task 5: Bảng tái hiện RQ1a từ log công bố (10–11/11)

**Files:**
- Create: `src/flx/semloc_results.py`, `data/rq1a_table.csv`
- Test: `tests/test_semloc_results.py`

**Interfaces:**
- Produces:
  - `best_ranks_from_csv(csv_path: Path) -> dict[str, int | None]` — đọc cột `Function`, `best_rank` của `rq1_localization.csv` (giá trị rỗng/không phải số → `None`)
  - `sbfl_best_ranks(sbfl_dir: Path, ground_truth: Path) -> dict[str, int | None]` — xếp hạng dòng lỗi từ `line_scores` của từng file JSON baseline
  - `acc_at_k(best_ranks: Mapping[str, int | None], k: int) -> float` — `None` tính là trượt
  - `median_rank(best_ranks) -> float | None`
  - `rq1a_table(results_root: Path, ground_truth: Path) -> list[dict]` — mỗi dòng: `config, n, acc1, acc3, acc5, median_rank, pct_suspicious`
  - CLI: `python -m flx.semloc_results --results third_party/semloc/results/RQ1 --gt third_party/semloc/benchmark/ground_truth.json --out data/rq1a_table.csv`

- [ ] **Step 1: Viết test thất bại**

```python
def test_acc_at_k_counts_none_as_miss():
    assert acc_at_k({"a": 1, "b": 4, "c": None}, 3) == 1/3
def test_semloc_claude_t08_matches_summary():
    ranks = best_ranks_from_csv(ROOT/"semloc_claude_T0.8/results/rq1_localization.csv")
    assert len(ranks) == 250
    assert round(acc_at_k(ranks, 1), 3) == 0.428 and round(acc_at_k(ranks, 3), 3) == 0.68
def test_sbfl_ochiai_matches_paper():
    ranks = sbfl_best_ranks(ROOT/"sbfl_ochiai", GT)
    assert round(acc_at_k(ranks, 1), 3) == 0.064 and round(acc_at_k(ranks, 3), 3) == 0.132
```

- [ ] **Step 2:** Chạy → FAIL.
- [ ] **Step 3:** Cài đặt. Với SBFL, cách xử lý điểm bằng nhau phải khớp SemLoc: đọc `third_party/semloc/src/run_eval.py` / `cli.py` (phần `report --rq1`) và làm y hệt; test ở Step 1 là trọng tài.
- [ ] **Step 4:** Chạy → PASS. Sinh `data/rq1a_table.csv` cho mọi cấu hình có trong `results/RQ1/`; đối chiếu bằng mắt với output `semloc report --rq1` trong `runs/offline_check.txt` — mọi số phải trùng.
- [ ] **Step 5: Commit** `git add src/flx/semloc_results.py tests/test_semloc_results.py data/rq1a_table.csv && git commit -m "feat: RQ1a reproduction table from published SemLoc logs"`

---

### Task 6: Gắn nhãn ngữ nghĩa + chia dev/test (11–12/11)

**Files:**
- Create: `src/flx/labels.py`, `src/flx/split.py`, `data/semfault_labels.csv`, `data/split.json`
- Test: `tests/test_labels.py`, `tests/test_split.py`, fixture `tests/fixtures/mini/{prog.py,test_prog.py}`

**Interfaces:**
- Consumes: `baselines.get_test_ids(test_path, repo_root)`, `baselines._coverage_for_test(test_id, abs_src, repo_root) -> (passed, hit_lines)` của SemLoc qua `ensure_on_path()`.
- Produces:
  - `@dataclass Label: program: str; n_pass: int; n_fail: int; fault_hit_by_fail: bool; fault_hit_by_pass: bool; category: Literal["semantic", "coverage_revealed", "not_executed"]`
  - `label_program(program: str, src: Path, test: Path, faulty_lines: list[int]) -> Label` — `not_executed` nếu không test fail nào chạy qua bất kỳ dòng lỗi nào; `semantic` nếu có dòng lỗi được cả ≥1 test fail và ≥1 test pass chạy qua; còn lại `coverage_revealed`
  - `make_split(labels: list[Label], n_dev: int = 50, seed: int = 20261108) -> dict` — trả `{"seed", "n_dev", "dev": [...], "test": [...]}`, phân tầng theo `category`, danh sách đã sắp xếp
  - CLI: `python -m flx.labels --benchmark third_party/semloc/benchmark --out data/semfault_labels.csv --workers 8`; `python -m flx.split --labels data/semfault_labels.csv --out data/split.json`

- [ ] **Step 1:** Tạo fixture `mini`: một hàm 10 dòng có lỗi ở dòng 6; 2 test pass chạy qua dòng 6, 1 test fail chạy qua dòng 6; thêm một nhánh chỉ test fail đi vào.
- [ ] **Step 2: Viết test thất bại**

```python
def test_label_semantic(mini): assert label_program("prog", SRC, TEST, [6]).category == "semantic"
def test_label_coverage_revealed(mini): assert label_program("prog", SRC, TEST, [LINE_ONLY_FAIL]).category == "coverage_revealed"
def test_label_not_executed(mini): assert label_program("prog", SRC, TEST, [LINE_NEVER_RUN]).category == "not_executed"
def test_label_multi_fault_any(mini): assert label_program("prog", SRC, TEST, [LINE_NEVER_RUN, 6]).category == "semantic"
def test_split_sizes_and_determinism():
    s1, s2 = make_split(LABELS_250), make_split(LABELS_250)
    assert s1 == s2 and len(s1["dev"]) == 50 and len(s1["test"]) == 200
    assert not set(s1["dev"]) & set(s1["test"])
def test_split_stratified():
    # tỉ lệ 'semantic' trong dev lệch không quá 0.05 so với toàn bộ
```

- [ ] **Step 3:** Chạy → FAIL. **Step 4:** Cài đặt. **Step 5:** Chạy → PASS.
- [ ] **Step 6:** Chạy CLI trên SemFault-250 → `data/semfault_labels.csv` đủ 250 dòng; in thống kê số lượng mỗi nhãn (dùng cho slide). Ghi thống kê và tên các chương trình `not_executed` (nếu có) vào `docs/literature/benchmark-notes.md`. Chạy split → `data/split.json`.
- [ ] **Step 7: Commit** `git add src/flx/labels.py src/flx/split.py tests data/semfault_labels.csv data/split.json docs/literature/benchmark-notes.md && git commit -m "feat: objective semantic-fault labels and fixed dev/test split"`

---

### Task 7: BugsInPy — giới hạn 3 ngày (10–12/11, song song)

**Files:**
- Create: `data/bugsinpy_status.csv`, `docs/literature/bugsinpy-setup.md`

**Interfaces:**
- Consumes: `third_party/semloc/src/bip_runner.py`, `third_party/semloc/scripts/reproduce_rq3.sh`, danh sách lỗi có kết quả không lỗi trong `third_party/semloc/results/RQ3/bugsInPy_results/` (68 file không chứa khóa `"error"`).
- Produces: `data/bugsinpy_status.csv` cột `bug_id, env_ok, tests_reproduce, sbfl_ok, note`; quyết định theo ngưỡng của spec.

- [ ] **Step 1:** Đọc `bip_runner.py` + `reproduce_rq3.sh`, ghi cách họ dựng môi trường (thư mục, Python version, lệnh BugsInPy) vào `bugsinpy-setup.md`.
- [ ] **Step 2:** Lập danh sách 68 lỗi ứng viên bằng script ngắn (lọc file không có khóa `error`), ghi vào CSV với `env_ok` trống.
- [ ] **Step 3:** Dựng lần lượt theo dự án (gom lỗi cùng dự án để dùng chung môi trường); với mỗi lỗi: checkout bản lỗi, cài phụ thuộc, chạy test fail → `tests_reproduce` = test fail đúng như BugsInPy khai báo; chạy SBFL của SemLoc → `sbfl_ok`.
- [ ] **Step 4:** Hết ngày 12/11: đếm số lỗi `env_ok & tests_reproduce & sbfl_ok`. **≥20** → ghi "ĐẠT" trong `bugsinpy-setup.md`, Phase 2 sau sẽ chạy SemLoc/CovGate trên các lỗi này. **<20** → dừng, ghi "KHÔNG ĐẠT" + nguyên nhân chính, theo phương án dự phòng của spec mục 3.1.
- [ ] **Step 5: Commit** `git add data/bugsinpy_status.csv docs/literature/bugsinpy-setup.md && git commit -m "docs: BugsInPy environment status (time-boxed)"`

---

### Task 8: Chạy thử SemLoc bằng Gemini trên tập dev (12–15/11)

**Files:**
- Create: `src/flx/workdir.py`, `scripts/run_semloc.sh`, `data/pilot_dev_gemini.csv`
- Test: `tests/test_workdir.py`

**Interfaces:**
- Consumes: Task 3, 4 (gateway + vá), Task 5 (`best_ranks_from_csv`, `acc_at_k`, `median_rank`), Task 6 (`data/split.json`, `data/semfault_labels.csv`).
- Produces:
  - `make_workdir(benchmark: Path, programs: list[str], out: Path) -> None` — tạo `out/programs/<p>.py` và `out/testcases/test_<p>.py` dạng symlink, `out/ground_truth.json` chỉ chứa các chương trình được chọn; gọi lại trên thư mục đã có thì không lỗi
  - `scripts/run_semloc.sh <workdir> <model> <temperature> <run_id>` — `export FLX_USE_GATEWAY=1 FLX_RUN_ID=<run_id>`, chạy `run_eval.py --working-dir <workdir> --model <model> --temperature <t> --workers ${WORKERS:-4} --steps 1,3,4,5,6,8 --cf-on-base`, rồi in `results_cf_base/summary.json`

- [ ] **Step 1: Viết test thất bại**

```python
def test_make_workdir_subset(tmp_path):
    make_workdir(BENCH, ["ad_mix", "adjust_queue"], tmp_path/"w")
    assert sorted(p.name for p in (tmp_path/"w/programs").iterdir()) == ["ad_mix.py", "adjust_queue.py"]
    gt = json.loads((tmp_path/"w/ground_truth.json").read_text())
    assert [p["function"] for p in gt["programs"]] == ["ad_mix", "adjust_queue"]
def test_make_workdir_idempotent(tmp_path): ...  # gọi 2 lần không ném lỗi
```

- [ ] **Step 2:** FAIL → **Step 3:** cài đặt → **Step 4:** PASS.
- [ ] **Step 5:** Chạy khói 3 chương trình dev: `scripts/run_semloc.sh runs/smoke_gemini "$FLX_GEMINI_MODEL" 0.8 smoke` → có `results_cf_base/summary.json`, `runs/llm_log.jsonl` có các dòng `run_id=smoke`, không dòng nào `error`. Từ log, tính số lượt gọi LLM trung bình/chương trình và đối chiếu quota ở `MODELS.md` để ước lượng thời gian chạy 50 chương trình; chỉnh `WORKERS` cho không dính 429.
- [ ] **Step 6:** Chạy cả 50 chương trình dev, 1 lần: `run_id=pilot_dev_r1`, workdir `runs/pilot_dev_gemini_r1`. Nếu đứt giữa chừng, chạy lại cùng `run_id` — cache giúp không tốn lại lượt gọi đã xong.
- [ ] **Step 7:** Sinh `data/pilot_dev_gemini.csv` gồm: Acc@1/3/5, median rank, %Susp của lượt chạy này; cùng chỉ số tính trên **đúng 50 chương trình dev** từ log công bố `semloc_gemini_T0.8` và `sbfl_ochiai`; tách theo nhãn `semantic` / `coverage_revealed`; tổng lượt gọi + token từ log. (Thêm hàm `subset(ranks, programs)` vào `semloc_results.py` kèm test nếu cần.)
- [ ] **Step 8: Commit** `git add src/flx/workdir.py tests/test_workdir.py scripts/run_semloc.sh data/pilot_dev_gemini.csv && git commit -m "feat: SemLoc pilot run with Gemini via gateway on dev split"`

---

### Task 9: Tổng quan tài liệu + từ khóa (08–14/11, song song)

**Files:**
- Create: `docs/literature/notes-semloc.md`, `docs/literature/notes-effiholmes.md`, `docs/literature/notes-crash-report-llm.md`, `docs/literature/related-work.md`, `docs/literature/keywords.md`, `docs/report/references.bib`

**Interfaces:**
- Produces: khóa BibTeX ổn định dùng cho cả hai bản LaTeX và slide; `related-work.md` có bảng so sánh.

- [ ] **Step 1:** Ba file ghi chú, mỗi file cùng mẫu: vấn đề; phương pháp; benchmark + chỉ số; kết quả chính (có số); hạn chế; liên hệ với đề tài của nhóm (RQ nào dùng tới). Nguồn: PDF trong `docs/requirement/dt2-chap10/`.
- [ ] **Step 2:** Tìm ~20 công trình liên quan, phủ 5 nhóm: SBFL kinh điển (Tarantula, Ochiai, DStar); MBFL / định vị lỗi dựa trên đột biến; định vị lỗi bằng LLM (AutoFL, AgentFL, FlexFL và các công trình SemLoc trích dẫn); benchmark (Defects4J, BugsInPy, QuixBugs); nhiễm dữ liệu huấn luyện / ghi nhớ của LLM trên code. Ưu tiên lấy từ phần tài liệu tham khảo của 3 bài thầy giao.
- [ ] **Step 3:** Mỗi mục trong `references.bib` phải kiểm được: có DOI hoặc arXiv id đã mở ra kiểm tra tiêu đề + tác giả khớp. Không có mục nào chưa kiểm.
- [ ] **Step 4:** `related-work.md`: bảng cột `công trình | năm | nhóm | tín hiệu dùng (độ phủ / đột biến / LLM / lai) | cấp độ (dòng / hàm) | benchmark | khác gì với đề tài`. `keywords.md`: 8–12 từ khóa tiếng Anh + thuật ngữ tiếng Việt tương ứng.
- [ ] **Step 5:** Kiểm tra: `grep -c '^@' docs/report/references.bib` ≥ 20.
- [ ] **Step 6: Commit** `git add docs/literature docs/report/references.bib && git commit -m "docs: literature notes, related-work table, keywords, bibliography"`

---

### Task 10: Khung LaTeX hai bản (12–14/11)

**Files:**
- Create: `docs/report/vi/main.tex` (+ `chapters/*.tex`, `frontmatter/*.tex`), `docs/report/paper-en/main.tex` (+ `sections/*.tex`), `docs/report/Makefile`

**Interfaces:**
- Consumes: `docs/report/references.bib` (Task 9).
- Produces: `make -C docs/report vi` và `make -C docs/report paper` biên dịch ra `vi/main.pdf`, `paper-en/main.pdf` không lỗi; bảng/hình sau này được `\input` từ `docs/report/generated/`.

- [ ] **Step 1:** Báo cáo VI: XeLaTeX + `fontspec` với Times New Roman nếu có trong máy, không thì TeX Gyre Termes; 13pt (vd. `scrreprt` với `fontsize=13pt`); `geometry` lề trên 3.5 / dưới 3 / trái 2.5 / phải 2.5 cm; giãn dòng 1.5 tương đương Word; tiêu đề chương 16pt đậm; tiêu đề mục chữ hoa đậm; tiểu mục 14pt đậm; tiểu mục con 14pt nghiêng; `secnumdepth` = 4 cấp; số trang giữa chân trang; hình/bảng đánh số theo chương, tên bảng ở trên, tên hình ở dưới; trích dẫn kiểu IEEE. Phần đầu: bìa (tên trường, môn IT5440, đề tài, tên nhóm — để `\TODO{}` danh sách thành viên), cam kết trung thực, mục lục, danh sách bảng, hình, viết tắt. Chương: 1 Giới thiệu, 2 Tổng quan nghiên cứu liên quan, 3 Cơ sở lý thuyết, 4 Giải pháp đề xuất, 5 Thực nghiệm và đánh giá, 6 Kết luận và hướng phát triển (khớp mục III.2 của hướng dẫn).
- [ ] **Step 2:** Bài báo EN: `IEEEtran` conference; mục Introduction, Background, Approach, Evaluation (RQ1–RQ3), Threats to Validity, Related Work, Conclusion; mỗi mục để đoạn giữ chỗ 1 câu nêu thông điệp của mục.
- [ ] **Step 3:** Biên dịch cả hai (`bash .claude/skills/latex-document-skill/scripts/compile_latex.sh <file> --preview`) → 0 lỗi, không còn `??` trích dẫn; xem ảnh trang bìa + 1 trang nội dung báo cáo VI để kiểm lề, phông, dấu tiếng Việt.
- [ ] **Step 4: Commit** `git add docs/report && git commit -m "docs: LaTeX skeletons for Vietnamese report and English paper"`

---

### Task 11: Slide báo cáo lần 1 (15–17/11)

**Files:**
- Create: `docs/presentation/bao-cao-lan-1.pptx`

**Interfaces:**
- Consumes: `docs/presentation/template-vi.pptx`; số liệu từ `data/rq1a_table.csv`, `data/semfault_labels.csv`, `data/pilot_dev_gemini.csv`, `data/bugsinpy_status.csv`; nội dung từ `docs/literature/*`.

- [ ] **Step 1:** Mở template bằng skill ppt-master, xác định các layout có sẵn.
- [ ] **Step 2:** Dựng 12–14 slide tiếng Việt theo thứ tự: bìa; bối cảnh và vấn đề (lỗi ngữ nghĩa làm SBFL thất bại); 3 bài báo thầy giao; tổng quan tài liệu + từ khóa; SemLoc hoạt động thế nào (sơ đồ 4 bước); khoảng trống nghiên cứu; 3 RQ; cải tiến CovGate (3 thành phần); thiết kế thực nghiệm (benchmark, phương pháp, chỉ số, thống kê); kết quả bước đầu (bảng RQ1a, thống kê nhãn, chạy thử Gemini trên dev, trạng thái BugsInPy); tiến độ so với 4 nội dung thầy chấm (đã xong 1–2); kế hoạch đến lần 2.
- [ ] **Step 3:** Mọi con số trên slide đối chiếu được với file trong `data/`; không có chữ tiếng Anh nếu đã có từ tiếng Việt tương ứng (theo hướng dẫn của thầy), trừ tên phương pháp/thuật ngữ chuyên ngành.
- [ ] **Step 4:** Xuất ảnh xem trước từng slide, kiểm tra không tràn chữ, không lệch template.
- [ ] **Step 5: Commit** `git add docs/presentation/bao-cao-lan-1.pptx && git commit -m "docs: slides for progress report 1"`
