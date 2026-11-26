# Ba lần báo cáo tiến độ và bảo vệ — kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chia lại slide thành bốn deck (lần 1, lần 2, lần 3, bảo vệ) theo mạch công việc từng tuần, thêm ba trang luồng phương pháp chạy trên ví dụ thật (FailLoc, SemLoc−Bonus, FailLoc+Cov).

**Architecture:** Mỗi trang được dựng một lần trong module story sinh ra nó; `bd.E/A/D` là no-op với trang deck không có, nên `build_deck.main` gọi `pages()` của **mọi** module story với mọi deck, còn danh sách `LAN1/LAN2/LAN3/BAOVE` quyết định deck có trang nào. Ba trang luồng nằm trong module mới `story_flow.py` và dùng helper mới `viz.flow`. Ví dụ cho FailLoc+Cov được thêm vào `data/fig_semloc_examples.json` bởi `scripts/figure_data.py`.

**Tech Stack:** Python 3 (SVG bằng chuỗi), ppt-master scripts (`.claude/skills/ppt-master/scripts`), pytest, LibreOffice + poppler cho PDF.

**Spec:** `docs/superpowers/specs/2026-11-25-ba-lan-bao-cao-design.md`

## Global Constraints

- Không ghi ngày trên bìa và bảng tiến độ. `OCCASION = {"lan1": "Báo cáo lần 1", "lan2": "Báo cáo lần 2", "lan3": "Báo cáo lần 3", "baove": "Bảo vệ tiểu luận"}`; cột mốc của bảng tiến độ chỉ là "Lần 1", "Lần 2", "Lần 3", "Bảo vệ".
- Lần 2 và lần 3: ≤ 18 trang mỗi deck (kể cả bìa và trang cảm ơn). Lần 1 ~15 trang. Bảo vệ đúng 28 trang, trang áp chót là `dong_gop_2.svg`.
- Mọi số liệu đọc từ `data/` hoặc `bd._m(...)` (macro của `docs/report/generated/numbers-vi.tex`); không gõ tay số.
- Thuật ngữ: "test fail / test pass"; "phương pháp X" trong tiêu đề; "chuẩn hóa nhãn / nhãn đã chuẩn hóa"; biểu đồ thanh ngang, không dot chart; không trang Hạn chế; mỗi trang tự giải thích hình của nó; trích nguồn phương pháp của người khác (SemLoc, Yang 2026), phương pháp của nhóm không gắn nhãn nguồn.
- Danh sách chữ cấm `FORBIDDEN` trong `tests/test_deck_text.py` áp dụng cho cả bốn deck.
- Không sửa báo cáo LaTeX, bài báo, hay chạy thí nghiệm mới.
- Commit không có dòng Co-Authored-By/Generated with Claude; không `git add` `.claude/`, `.agents/`, `runs/`. Chỉ `git add` các file mình sửa (cây làm việc đang có nhiều thay đổi chưa commit của trưởng nhóm — không commit hộ).
- Dựng deck bằng `/usr/bin/python3` (có python-pptx); test bằng `.venv/bin/python -m pytest` nếu chạy được, không thì `/usr/bin/python3 -m pytest`.

## Review Focus

1. **Lộ nội dung giữa các lần**: một trang dùng chung có chữ phụ thuộc deck (vd `thiet_ke_tn` dùng `bd.EARLY()` để chọn "hai/ba bộ nhãn") đổi nghĩa khi chuyển deck → test `test_decks_do_not_leak` (Task 2) kiểm từ khóa theo deck.
2. **Hai deck tiến độ trùng trang nội dung** (người nghe thấy lại trang tuần trước) → `test_progress_decks_are_disjoint` (Task 2).
3. **Notes cũ của bảo vệ ghi đè notes của trang dùng chung ở deck khác** (vd `cau_hoi`) hoặc trang thiếu notes → `test_every_page_has_notes` (Task 2).
4. **Ví dụ trên trang luồng không khớp dữ liệu** (hạng, f/p, dòng lỗi) → `test_cov_example_matches_rankings` (Task 1) và `test_flow_pages_state_the_real_ranks` (Task 3).
5. **Trang lần 3 nhắc tên nhóm phân tích thất bại** ("coverage_only_wins", "Chỉ FailLoc+Cov vào top 3") → nằm trong `test_decks_do_not_leak` (Task 2).

---

### Task 1: Dữ liệu ví dụ cho FailLoc+Cov

Ví dụ đã chọn: `combine_responses` (tập test, nhãn dòng 72). Độ phủ: dòng 72 được 4/4 test fail chạy qua và 0 test pass (`[f=4/p=0]`), dòng 71 là `[f=4/p=5]`. FailLoc (r1) trả `[71, 72, 68, 69, 61]` → dòng lỗi hạng 2; FailLoc+Cov (r1) trả `[72, 71, 68, 69, 77]` → hạng 1; đúng như vậy ở cả 3 lượt chạy.

**Files:**
- Modify: `scripts/figure_data.py` (`examples()`, thêm `cov_example`)
- Regenerate: `data/fig_semloc_examples.json`
- Test: `tests/test_figure_data.py` (tạo mới nếu chưa có)

**Interfaces:**
- Produces: khóa `"combine_responses"` trong `data/fig_semloc_examples.json`, đọc qua `story_common.examples()["combine_responses"]`, dạng:
  `{"program": str, "label_lines": [int], "code_lines": {str(line): str}  # cửa sổ hàm chứa nhãn, "fp": {str(line): [ef, ep]}  # chỉ các dòng trong cửa sổ, "n_fail": int, "n_pass": int, "failloc_top5": [[int]*5]*3, "cov_top5": [[int]*5]*3, "cov_prompt": str}`
  (`cov_prompt` = `flx.direct_cov.build_prompt(..., coverage=True)`, cùng cách `failloc_prompt` đang được dựng trong `semloc_example`).

- [ ] **Step 1: Viết test hỏng**

```python
def test_cov_example_matches_rankings():
    ex = json.loads((ROOT / "data" / "fig_semloc_examples.json").read_text())["combine_responses"]
    assert ex["label_lines"] == [72]
    assert ex["fp"]["72"] == [ex["n_fail"], 0] and ex["fp"]["71"][1] > 0
    for r in range(3):
        fl = json.loads((ROOT / f"data/rankings/direct_tests_test_gemini_r{r+1}.json").read_text())["combine_responses"]
        cv = json.loads((ROOT / f"data/rankings/direct_cov_test_gemini_r{r+1}.json").read_text())["combine_responses"]
        assert ex["failloc_top5"][r] == fl[:5] and ex["cov_top5"][r] == cv[:5]
        assert cv.index(72) < fl.index(72)
    assert "[f=4/p=0]" in ex["cov_prompt"].replace(" ", "") or "f=4" in ex["cov_prompt"]
```

- [ ] **Step 2: Chạy, xác nhận hỏng** — `.venv/bin/python -m pytest tests/test_figure_data.py::test_cov_example_matches_rankings -v` → FAIL với `KeyError: 'combine_responses'`.

- [ ] **Step 3: Cài `cov_example(program: str) -> dict` trong `scripts/figure_data.py`** và gọi trong `examples()` (thêm `"combine_responses": cov_example("combine_responses")`). Cửa sổ mã dùng `function_window`; f/p lấy bằng `flx.sbfl.counts(cov)`; nhãn lấy từ biến thể nhãn `repaired` (`flx.gt.load_variants()`). Chạy `.venv/bin/python scripts/figure_data.py` để ghi lại JSON (kiểm `git diff data/` chỉ đổi `fig_semloc_examples.json` thêm khóa mới; `semloc_line_scores.csv` và `fig_example.json` phải không đổi — nếu đổi, dừng lại và báo).

- [ ] **Step 4: Chạy test, xác nhận qua.**

- [ ] **Step 5: Commit** — `git add scripts/figure_data.py data/fig_semloc_examples.json tests/test_figure_data.py && git commit -m "dữ liệu ví dụ cho trang luồng FailLoc+Cov: combine_responses"`

---

### Task 2: Bốn deck — danh sách trang, dựng, tiến độ, test

**Files:**
- Modify: `docs/presentation/build/story_lan1.py` (`LAN1`, `PROGRESS`, mục lục, notes `cau_hoi` bốn RQ, tiêu đề `tien_do`)
- Modify: `docs/presentation/build/story_lan2.py` (`LAN2`, `PROGRESS`, `muc_luc_2`, trang `nhac_lai` viết lại, trang hiện tại của `nhac_lai` chuyển sang `story_lan3` với tên `nhac_lai_3`)
- Create: `docs/presentation/build/story_lan3.py`
- Modify: `docs/presentation/build/story_baove.py` (bỏ lời gọi `story_lan1.pages/ story_lan2.pages` và trộn notes bên trong — việc đó chuyển lên `build_deck`)
- Modify: `docs/presentation/build/build_deck.py` (`DECKS`, `OCCASION`, `OUT_NAME`, `SOURCE`, `main`, `EARLY`)
- Modify: `docs/presentation/build/make_decks.sh`, `docs/presentation/build/README.md`
- Test: `tests/test_deck_text.py`

**Interfaces:**
- Produces: `story_lan3.LAN3: list[tuple[str, int]]`, `story_lan3.PROGRESS`, `story_lan3.pages(bd) -> None`, `story_lan3.notes(bd) -> dict[str, str]`.
- `build_deck.STORIES = (story_lan1, story_lan2, story_lan3, story_flow, story_baove)`; `main(deck)` gọi `pages(bd)` của từng module theo thứ tự đó, rồi notes = hợp các `notes(bd)` theo cùng thứ tự (module sau ghi đè module trước). Ghi đè notes riêng của bảo vệ (`cau_hoi`, `thiet_ke_tn`, `slide_01`, `dong_gop_2`…) chỉ áp dụng khi `bd.DECK == "baove"`. (`story_flow` do Task 3 tạo; trong Task 2 tạo sẵn file rỗng với `FLOW = []`, `pages(bd)` và `notes(bd)` trả `{}`.)
- `bd.EARLY()` vẫn là `DECK == "lan1"`; `thiet_ke_tn` giờ chỉ có ở lần 2 và bảo vệ, nên luôn "ba bộ nhãn".

Danh sách trang (Task 3 sẽ thay `failloc_vd` bằng `luong_failloc` và chèn hai trang luồng còn lại):

```python
LAN1 = [slide_01, muc_luc, bai_toan, vi_du, sbfl_cong_thuc, sbfl_mu, lien_quan,
        semloc_tong_quan, semloc_rang_buoc, semloc_diem, cau_hoi, overclaim, nhan_sai, tien_do, slide_30]      # 15
LAN2 = [slide_01, muc_luc_2, nhac_lai, chuan_hoa, failloc_y_tuong, failloc_vd, phuong_phap, thiet_ke_tn,
        ket_qua, cai_tien, nhan_lech, ra_soat, nhan_di_dau, ba_bo_nhan, tien_do_2, slide_30]                  # 16 (+1 ở Task 3)
LAN3 = [slide_01, muc_luc_3, nhac_lai_3, ablation_la_gi, bo_sung, rq3_thiet_ke, bugsinpy, doi_ten,
        ho_mo_hinh, ablation_kq, bo_sung_kq, cai_tien_2, dong_gop_2, tien_do_3, slide_30]                     # 15 (+1 ở Task 3)
BAOVE  = giữ nguyên ở Task 2 (28)
```
(source slide: `slide_01`→1, `cau_hoi`→20, `slide_30`→30, còn lại 22, như hiện nay.)

Nội dung trang mới/viết lại:
- `nhac_lai` (lần 2, nhắc lần 1): tiêu đề "Nhắc lại lần 1: SemLoc tái hiện được, nhưng điểm thưởng và nhãn có vấn đề". Ba ý, mỗi ý một số từ macro/CSV đang dùng ở `overclaim` và `nhan_sai`: Acc@1 SemLoc tái hiện (nhãn gốc); Acc@1 khi bỏ điểm thưởng; số nhãn trên dòng trống (`GtBlankN`). Không có số của FailLoc.
- `nhac_lai_3` (lần 3, nhắc lần 2): nội dung trang `nhac_lai` hiện tại (bảng FailLoc hơn SemLoc trên nhãn đã chuẩn hóa), tiêu đề "Nhắc lại lần 2: phương pháp FailLoc hơn phương pháp SemLoc".
- `muc_luc` / `muc_luc_2` / `muc_luc_3`: theo năm phần của thầy, chỉ liệt kê những gì deck đó có.
- `tien_do` / `tien_do_2` / `tien_do_3`: tiêu đề "Tiến độ", bảng `viz.progress_table` với các dòng:

```python
WORK = [("Tài liệu, bộ từ khóa, ba bài tiêu biểu (nội dung 1)", "Lần 1"),
        ("Bốn câu hỏi nghiên cứu, thiết kế thực nghiệm (nội dung 2)", "Lần 1"),
        ("Tái hiện SemLoc; phát hiện điểm thưởng và nhãn sai", "Lần 1"),
        ("Chuẩn hóa và rà soát nhãn, phương pháp FailLoc, so sánh chính", "Lần 2"),
        ("Độ bền (RQ4), ablation, các hướng bổ sung, chi phí", "Lần 3"),
        ("Đóng góp khoa học (nội dung 3)", "Lần 3"),
        ("Bài báo arXiv (nội dung 4), phân tích thất bại, kiểm chứng bằng bản sửa", "Bảo vệ")]
```
  Trạng thái ở deck lần k: mốc < k → "Đã xong"; mốc == k → "Đã xong"; mốc là lần k+1 → "Đang hoàn thiện"; xa hơn → "Chưa làm"; riêng dòng bài báo ở lần 3 là "Có bản nháp". Đặt `WORK` và hàm `progress_rows(k: int) -> list[tuple[str, str, str]]` trong `story_common.py`, ba deck đều dùng.
- Cover: `story_common.cover` nhận `OCCASION` mới (không ngày); dòng "Nhóm M9 · …" trên trang cảm ơn cũng không ngày.

- [ ] **Step 1: Viết test hỏng** trong `tests/test_deck_text.py` (cập nhật các test cũ, giữ `FORBIDDEN`):

```python
DECK_NAMES = ["lan1", "lan2", "lan3", "baove"]
LEAK = {  # word -> first deck allowed to show it outside the progress table
    "FailLoc+Cov": "lan3", "BugsInPy": "lan3", "đổi tên": "lan3", "Ablation": "lan3", "CovGate": "lan3",
    "FailLoc+Vote": "lan3", "Đóng góp": "lan3",
    "duyệt mù": "lan2", "rà soát": "lan2", "Nhãn đã chuẩn hóa": "lan2", "nhãn đã chuẩn hóa": "lan2",
    "FailLoc+Verify": "baove", "phân loại thất bại": "baove", "Shapley": "baove",
    "coverage_only_wins": None, "Chỉ FailLoc+Cov vào top 3": "baove",
}
ORDER = {d: i for i, d in enumerate(DECK_NAMES)}

@pytest.mark.parametrize("deck", DECK_NAMES)
def test_no_clipped_words(deck): ...            # như cũ, bỏ DONE/xfail

@pytest.mark.parametrize("deck", ["lan1", "lan2", "lan3"])
def test_decks_do_not_leak(deck):
    for stem, t in _pages(deck).items():
        if stem.startswith("tien_do"): continue
        for word, first in LEAK.items():
            if first is None or ORDER[deck] < ORDER[first]:
                assert word not in t, (deck, stem, word)

def test_progress_decks_are_disjoint():
    import story_lan1, story_lan2, story_lan3
    shared = {"slide_01.svg", "slide_30.svg"}
    sets = [{n for n, _ in L} - shared for L in (story_lan1.LAN1, story_lan2.LAN2, story_lan3.LAN3)]
    assert not (sets[0] & sets[1]) and not (sets[1] & sets[2]) and not (sets[0] & sets[2])

def test_progress_talks_are_short():
    import story_lan2, story_lan3
    assert len(story_lan2.LAN2) <= 18 and len(story_lan3.LAN3) <= 18

@pytest.mark.parametrize("deck", DECK_NAMES)
def test_every_page_has_notes(deck):
    build_deck.main(deck)
    stems = {Path(n).stem for _, n in build_deck.PAGES} - {"slide_30"}
    assert stems <= {f.stem for f in (build_deck.WS / "notes").glob("*.md")}, deck

def test_covers_carry_no_date():
    for d in DECK_NAMES:
        assert not re.search(r"\d{1,2}/\d{1,2}|/20\d\d", build_deck.OCCASION[d]), d
```
  `test_label_tree_counts_add_up` đọc `_pages("lan2")["chuan_hoa"]`; `test_bugsinpy_title_holds_on_the_metric_it_plots` đọc `_pages("lan3")["bugsinpy"]`; `test_lan1_does_not_leak_report_2`, `test_lan2_does_not_leak_the_defence`, `test_lan2_is_a_short_progress_talk` bị thay bằng các test trên; `test_baove_is_thirty_pages_and_ends_on_contributions` đổi tên thành `test_baove_is_28_pages_and_ends_on_contributions`, giữ nội dung.

- [ ] **Step 2: Chạy, xác nhận hỏng** — `/usr/bin/python3 -m pytest tests/test_deck_text.py -v` → FAIL (`story_lan3` chưa có, OCCASION còn ngày).

- [ ] **Step 3: Cài đặt** theo phần mô tả ở trên. Nếu `test_decks_do_not_leak` bắt một từ ở trang lần 1/lần 2 mà trang đó thật sự cần (vd `overclaim` nói "SemLoc−Bonus"), sửa câu trên trang cho khỏi lộ, không nới `LEAK`; nếu bắt buộc phải nới, ghi lý do vào commit message.

- [ ] **Step 4: Chạy test, xác nhận qua** — `/usr/bin/python3 -m pytest tests/test_deck_text.py -v` → tất cả PASS.

- [ ] **Step 5: `make_decks.sh` và README** — thêm `[lan3]=slide-lan-3.pptx`, mặc định `lan1 lan2 lan3 baove`; README đoạn đầu mô tả bốn deck và mạch tuần (lần 1 tìm hiểu, tái hiện; lần 2 nhãn, FailLoc; lần 3 độ bền, bổ sung, đóng góp; bảo vệ đủ). Chạy `bash docs/presentation/build/make_decks.sh lan1 lan2 lan3` → in ba dòng `lanX -> docs/presentation/slide-lan-X.pptx + .pdf`, không lỗi quality gate.

- [ ] **Step 6: Commit** — `git add` đúng các file ở **Files** + ba cặp `slide-lan-{1,2,3}.{pptx,pdf}` → `git commit -m "slide: ba lần báo cáo tiến độ (lần 3 mới), bỏ ngày trên bìa và bảng tiến độ"`

---

### Task 3: Ba trang luồng phương pháp

**Files:**
- Modify: `docs/presentation/build/viz.py` (thêm `flow`)
- Modify: `docs/presentation/build/story_flow.py` (tạo ở Task 2 dạng rỗng)
- Modify: `story_lan2.LAN2`, `story_lan3.LAN3`, `story_baove.BAOVE`
- Test: `tests/test_deck_text.py`

**Interfaces:**
- Consumes: `story_common.examples()["votes_apportion"]` (`code_lines`, `label_lines=[29]`, `guess_line=26`, `constraints` (ochiai đều 0), `line_scores=[{"line":26,"spectrum":0.0,"bonus":1.2,"rank":1}]`, `failloc_top5=[29,25,26,28,30]`, `failloc_prompt`, `n_fail=1`, `n_pass=4`) và `["combine_responses"]` (Task 1).
- Produces: `viz.flow(gid: str, x: float, y: float, steps: list[tuple[str, list[str]]], box_w: float, box_h: float, gap: float = 26, accent: int | None = None, struck: set[int] = frozenset(), mono: set[int] = frozenset()) -> str` — các hộp trái→phải nối mũi tên; mỗi hộp có tiêu đề đậm và vài dòng nội dung thật (dòng mã/prompt dùng font mono khi chỉ số hộp nằm trong `mono`); hộp trong `struck` vẽ viền đứt và gạch chéo đỏ (bước bị bỏ). Trang: `luong_failloc.svg`, `luong_semloc_bonus.svg`, `luong_cov.svg` (source 22).

Nội dung (mỗi trang: tiêu đề là một câu khẳng định, sơ đồ luồng ở trên, một dòng "khác X ở đúng một chỗ" dưới sơ đồ, một khung giải thích cách đọc; band phần 3 "Cải tiến"; notes đọc thành lời):
- `luong_failloc`: tiêu đề "Luồng phương pháp FailLoc trên ví dụ 1: dòng lỗi 29 lên hạng 1". Hộp: Đầu vào (vài dòng mã quanh dòng 29 + "1 test fail, 4 test pass") → Prompt (trích từ `failloc_prompt`: câu yêu cầu và tên/lỗi test fail) → Một lượt gọi LLM → Kết quả top-5 `29, 25, 26, 28, 30` với 29 tô đậm "✓ hạng 1". Dòng so sánh: "Khác LLM-Direct ở đúng một chỗ: prompt có tên và thông báo lỗi của test fail." Trang thay `failloc_vd` ở `LAN2` và `BAOVE`.
- `luong_semloc_bonus`: tiêu đề "Bỏ điểm thưởng thì SemLoc không còn xếp được dòng nào ở ví dụ 1". Hộp: Viết ràng buộc (số ràng buộc thật, vd 1 biểu thức) → Chèn và chạy test (`ef=0` với mọi ràng buộc: "không ràng buộc nào bị test fail vi phạm") → Phổ vi phạm (Ochiai = 0 mọi dòng) → **Cộng thưởng 1,2 cho dòng 26 LLM đoán** (`struck`) → Kết quả: SemLoc xếp 26 hạng 1 (sai, dòng lỗi 29); SemLoc−Bonus không xếp được dòng nào. Dưới sơ đồ: Acc@1 trên toàn tập test (nhãn đã chuẩn hóa) của SemLoc và SemLoc−Bonus đọc từ `data/rq2_ours.csv` (`gt=="repaired"`, `subset=="all"`, method `semloc` / `semloc_no_prior`). Dòng so sánh: "Khác SemLoc ở đúng một chỗ: bỏ điểm thưởng cho dòng LLM đoán." Trang vào `LAN2` ngay sau `luong_failloc`.
- `luong_cov`: tiêu đề "Luồng FailLoc+Cov trên ví dụ 2: độ phủ đưa dòng lỗi 72 lên hạng 1". Hộp: Đầu vào (dòng 71, 72 kèm `[f=4/p=5]`, `[f=4/p=0]` từ `fp`) → Prompt (như FailLoc, thêm cột [f/p]) → Một lượt gọi LLM → Kết quả: FailLoc `71, 72, …` (72 hạng 2) đặt cạnh FailLoc+Cov `72, 71, …` (72 hạng 1), "cả 3 lần chạy". Dưới sơ đồ: chú thích `[f/p]` = số test fail/pass chạy qua dòng; số tổng hiệu ứng độ phủ `bd._m("AblRepairedAllCoverageEffectDAccOne")` điểm Acc@1 để người nghe không nghĩ ví dụ là trường hợp chung. Không có chữ "coverage_only_wins" hay tên nhóm của phân tích thất bại. Trang vào `LAN3` ngay sau `ablation_la_gi`.
- `BAOVE`: thay `failloc_vd` → `luong_failloc`; bỏ `failloc_y_tuong` và `phuong_phap`; chèn `luong_semloc_bonus` sau `luong_failloc`, `luong_cov` sau `bo_sung`. Tổng vẫn 28.

- [ ] **Step 1: Viết test hỏng**

```python
def test_flow_pages_state_the_real_ranks():
    import story_common
    ex = story_common.examples()
    t2, t3 = _pages("lan2"), _pages("lan3")
    va, cr = ex["votes_apportion"], ex["combine_responses"]
    f = t2["luong_failloc"]
    assert "29" in f and ", ".join(map(str, va["failloc_top5"])) in f
    s = t2["luong_semloc_bonus"]
    assert "26" in s and "1,2" in s and "SemLoc−Bonus" in s
    c = t3["luong_cov"]
    assert "f=4/p=0" in c.replace(" ", "") and "72" in c and "coverage_only_wins" not in c

def test_flow_pages_are_in_the_right_decks():
    import story_lan2, story_lan3, story_baove
    names = lambda L: [n for n, _ in L]
    assert {"luong_failloc.svg", "luong_semloc_bonus.svg"} <= set(names(story_lan2.LAN2))
    assert "luong_cov.svg" in names(story_lan3.LAN3)
    b = names(story_baove.BAOVE)
    assert {"luong_failloc.svg", "luong_semloc_bonus.svg", "luong_cov.svg"} <= set(b) and len(b) == 28
```

- [ ] **Step 2: Chạy, xác nhận hỏng** (`KeyError: 'luong_failloc'`).

- [ ] **Step 3: Cài `viz.flow` và ba trang + notes trong `story_flow.py`; cập nhật ba danh sách trang.** Mọi chữ phải nằm trong khung trang 960×540, không đè band góc phải trên; dòng mã cắt bằng `…` nếu quá dài (như `nhan_lech` đang làm).

- [ ] **Step 4: Chạy toàn bộ `tests/test_deck_text.py`, xác nhận qua.**

- [ ] **Step 5: Dựng và nhìn tận mắt** — `bash docs/presentation/build/make_decks.sh` (cả bốn deck). Xuất PNG các trang luồng: `pdftoppm -png -r 60 -f N -l N docs/presentation/slide-lan-2.pdf <scratchpad>/lan2` (N là số trang của `luong_failloc`, `luong_semloc_bonus`; tương tự `luong_cov` ở lần 3 và ba trang ở bảo vệ) rồi Read từng PNG: không chữ tràn hộp, không đè nhau, mũi tên nối đúng, hộp gạch bỏ nhìn rõ. Sửa đến khi sạch.

- [ ] **Step 6: Commit** — `git add` `viz.py story_flow.py story_lan2.py story_lan3.py story_baove.py tests/test_deck_text.py` + bốn cặp `.pptx/.pdf` → `git commit -m "slide: trang luồng FailLoc, SemLoc−Bonus, FailLoc+Cov chạy trên ví dụ thật; bảo vệ giữ 28 trang"`

---

### Task 4: Rà cuối và bộ nhớ

- [ ] **Step 1:** Đọc PDF bốn deck bằng `pdftotext` và kiểm: số trang (lần 1 ~15, lần 2 ≤ 18, lần 3 ≤ 18, bảo vệ 28); không còn ngày "18–19/11", "25–26/11", "12/2026" trên bìa/tiến độ; mục lục mỗi deck khớp trang thật của deck.
- [ ] **Step 2:** Cập nhật bộ nhớ `milestone-staging.md`: ba lần báo cáo tiến độ + bảo vệ (lịch đổi 25/11), mạch tuần của từng lần, lần 2/3 ≤ 18 trang, bảo vệ 28, trang luồng phương pháp; sửa dòng MEMORY.md tương ứng.
- [ ] **Step 3:** `/usr/bin/python3 -m pytest tests/test_deck_text.py tests/test_figure_data.py -q` → tất cả PASS; báo cho trưởng nhóm danh sách trang từng deck.
