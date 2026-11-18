# Thiết kế: hình, biểu đồ và mạch kể chuyện cho báo cáo, bài báo và slide (lần 1, lần 2, bảo vệ)

Ngày: 2026-11-18. Người yêu cầu: trưởng nhóm M9.

## Ý định và lý do

Báo cáo (VI, 47 trang ở bản lần 1) và slide hiện gần như toàn chữ và bảng: cả báo cáo có đúng 1 sơ đồ TikZ (ch3) và 1
biểu đồ (pareto, chỉ từ lần 2); slide lần 1 (22 trang) không có sơ đồ quy trình hay biểu đồ nào, kết quả RQ2 là một bảng
số dày. Người xem không nhìn ra nhóm đang làm gì. Trưởng nhóm muốn sản phẩm trông như một bài báo thật: có sơ đồ (quan
trọng nhất), biểu đồ, bảng; và slide phải **kể chuyện**.

Thành công = một người chưa đọc gì, chỉ nhìn hình, nói lại được: (1) SemLoc làm gì, (2) nhóm nghi ngờ điều gì, (3) nhóm
làm gì để kiểm tra, (4) kết quả ra sao.

## Mục tiêu

1. **Đặt tên phương pháp chuẩn** (chỉ phần hiển thị; id trong `data/` và mã giữ nguyên):

   | id trong `data/` | Tên hiển thị |
   |---|---|
   | `llm_tests` | **FailLoc** (Failure-guided Localization) — phương pháp đề xuất của nhóm |
   | `llm_direct` | **LLM-Direct** |
   | `llm_coverage` | **FailLoc+Cov** |
   | `semloc` | **SemLoc** |
   | `semloc_no_prior` | **SemLoc−Bonus** |
   | `sbfl_ochiai` | **SBFL (Ochiai)** |
   | `covgate` | **CovGate** |
   | PAV (đề xuất rồi kiểm chứng) | **FailLoc+Verify** |
   | biểu quyết | **FailLoc+Vote** |

   Tên đã tra: không công trình nào dùng "FailLoc" (gần nhất là FaR-Loc, arXiv 2509.20552, khác hẳn). Áp dụng ở báo cáo VI,
   bài báo EN, bảng sinh tự động (`scripts/make_tables.py`, `generated/`), slide. Lần đầu xuất hiện có câu định nghĩa:
   "FailLoc: một lượt gọi LLM với mã nguồn đánh số dòng, tên và dòng lỗi đầu tiên của từng kiểm thử thất bại".
   Các id phụ khác (`cf_rerank`, `gate_only`, `lam_only`, `grounded_prior_only`, `covgate_cf`) builder đặt tên theo cùng
   hệ (Builder quyết).

2. **Báo cáo VI + bài báo EN: hình phong cách nghiên cứu**, theo từng phiên bản (xem danh sách bên dưới).
3. **Slide: hình phong cách kể chuyện**, vẽ riêng, **không** bắt buộc giống hình báo cáo.
4. Giữ cơ chế hé mở: mỗi phiên bản chỉ hiện hình của nội dung đã đến hạn.

## Không làm / chống mục tiêu

- Không chạy lại thí nghiệm, không đổi số liệu, không đổi id trong `data/`.
- Không có con số gõ tay: mọi số trên hình đọc từ `data/` hoặc `generated/numbers*.tex` (repo có `lint_numbers.py`
  và nguyên tắc này; hình phải tôn trọng nó).
- Thất bại dù "chạy được": hình đẹp nhưng lộ nội dung lần sau sớm (vd. lần 1 có heatmap RQ3, biểu đồ ablation,
  nhãn đã rà soát); slide vẫn là tường chữ chỉ thêm vài hình; hình có số lệch với bảng/văn bản.
- Không dùng ảnh minh họa có thương hiệu/nhân vật của bên thứ ba; icon chỉ từ template hiện có.

## Ràng buộc

- **Hạn:** lần 1 trình bày 18–19/11/2026 (hôm nay là 18/11) → lần 1 là ưu tiên tuyệt đối và phải xong trước; lần 2
  25–26/11; bảo vệ tháng 12 (mục tiêu nhóm 12/12). Thầy có thể chấm qua slide hoặc PDF → **lần 1 phải có cả hai**.
- Cơ chế phiên bản: LaTeX `\IfAtLeast{lan2|full}` / `\IfAtLeastElse` (lan1 < lan2 < full), `make -C docs/report
  vi-lan1|vi-lan2|vi-full|paper|check`; deck `DECKS` / `EARLY()` trong `docs/presentation/build/build_deck.py`,
  `make_decks.sh lan1|lan2|baove` (cần python có python-pptx: `/usr/bin/python3`). Dấu `&` trong `\IfAtLeastElse`
  phá bảng — để dấu cột ngoài điều kiện.
- `tests/test_report_build.py` canh nội dung từng phiên bản (cụm từ phải có / không được có); cập nhật khi đổi tên.
- Nhánh `bao-cao-lan-1`, `bao-cao-lan-2` dựng lại từ `main` (mặc định `\Version` của nhánh, chỉ chứa PDF + deck của nó).
- Không thêm dòng Co-Authored-By Claude vào commit (quy ước của nhóm).
- Hình VI dùng dấu phẩy thập phân (`52,3`), hình EN dùng dấu chấm.

## Các cách đã cân nhắc

| Cách | Mô tả | Đánh đổi |
|---|---|---|
| A. Một nguồn hình cho cả báo cáo và slide | TikZ + matplotlib, xuất PDF cho LaTeX và PNG cho deck | Số luôn khớp, ít công; nhưng slide mang phong cách bài báo, khô, không kể chuyện được |
| **B. Hai phong cách tách biệt (đã chọn)** | Báo cáo/bài báo: TikZ (sơ đồ) + matplotlib (biểu đồ) từ `data/`. Slide: hình khối gốc SVG vẽ trong `build_deck.py` trên template, ẩn dụ, mở dần từng lớp | Tốn công vẽ hai lần; bù lại mỗi phương tiện đúng việc của nó; số vẫn từ `data/` nên không lệch |
| C. draw.io vẽ tay | Nhanh cho vài sơ đồ | Không sinh lại được từ dữ liệu, trái nguyên tắc repo |

Trưởng nhóm chọn B ("ảnh slide có thể thú vị hơn, không cần chặt với hình trong paper/report; paper/report viết theo
hướng research"); đặt tên FailLoc do Claude đề xuất sau khi tra, trưởng nhóm giao quyền chọn.

## Phần báo cáo + bài báo (phong cách nghiên cứu)

**Công cụ:** sơ đồ là tệp TikZ độc lập trong `docs/report/figures/` (`\input` từ cả VI và EN; nhãn chữ theo ngôn ngữ
qua macro hoặc hai tệp — Builder quyết). Biểu đồ: một script mới `scripts/make_figures.py` (matplotlib, đọc `data/`)
xuất `generated/vi/*.pdf` và `generated/*.pdf`, được gọi trong `scripts/regenerate_all.sh`. Phong cách: một bảng màu
thống nhất, FailLoc luôn cùng một màu nổi, SemLoc một màu, baseline xám; có thanh khoảng tin cậy 95% (bootstrap đã có
trong csv: `d_acc*_lo/hi`, hoặc sd qua 3 lần chạy); không tiêu đề trong hình (dùng caption); font khớp tài liệu.

**Danh sách hình theo phiên bản** (F = sơ đồ, C = biểu đồ, T = bảng mới thay đoạn văn):

Lần 1 (`lan1`, có từ bây giờ):
- F1 **Hình tổng quan** (đầu ch1 / Fig. 1 của paper): hai luồng song song — SemLoc (mã → LLM viết ràng buộc → chèn &
  chạy test → phổ vi phạm → chấm điểm (+thưởng dòng đoán) → LLM vá thử → xếp hạng) và FailLoc (mã + test thất bại →
  1 lượt LLM → xếp hạng), mỗi luồng ghi số lượt gọi LLM và token/chương trình.
- F2 **SBFL mù với lỗi ngữ nghĩa** (ch3): một chương trình nhỏ ví dụ (lấy từ SemFault-250, Builder chọn) với ma trận
  phủ test×dòng, test pass và fail cùng phủ các dòng → điểm Ochiai bằng nhau.
- F3 **Bên trong điểm của SemLoc** (ch5 RQ1): thanh điểm từng dòng = điểm phổ + thưởng `\ConstPriorWeight` cho dòng đoán;
  cho thấy thưởng lớn hơn mọi điểm ràng buộc → hạng 1 luôn là dòng đoán. Có thể vẽ từ một chương trình thật.
- F4 **Quy trình sửa nhãn bằng thực thi** (ch4): luồng bộ phán định sửa tối thiểu, nhánh ra xác nhận / dời vị trí / chưa
  kiểm chứng / không kiểm chứng (loại), mỗi nhánh có số `\GtConfirmedN` …
- F5 **Thiết kế thực nghiệm** (ch4): ma trận dữ liệu (dev 50 / test 200) × phương pháp × bộ nhãn × 3 lần lặp, chỉ số.
  Ở lần 1 chỉ hiện các ô đã làm (nhãn gốc + đã sửa, Gemini 3.8 Flash); ô RQ3 không hiện.
- C1 **Kết quả chính RQ2** (ch5): cột nhóm Acc@1/Acc@3 cho SBFL, LLM-Direct, SemLoc, SemLoc−Bonus, FailLoc; hai bảng con
  nhãn gốc / nhãn đã sửa; thanh lỗi.
- C2 **Chi phí – độ chính xác** chỉ trên Gemini (token/chương trình vs Acc@1), không phải pareto đa họ mô hình (đó là lần 2).
- T: bảng "các phương pháp so sánh" (tên, đầu vào, số lượt LLM, có dùng thực thi không).

Lần 2 (`lan2`) thêm:
- F6 **Rà soát nhãn hai bước + duyệt mù**: LLM rà 250 → người duyệt ca nghi → duyệt mù 60 CT, 2 người/CT, không gợi ý.
- C3 **Nhãn gốc đi đâu**: biểu đồ thanh xếp chồng/sankey: giữ nguyên, dòng trống, lệch 1 dòng, dời xa, hai dòng.
- C4 **Ablation**: LLM-Direct → +test thất bại (FailLoc) → +độ phủ (FailLoc+Cov), hiệu ứng ΔAcc có khoảng tin cậy.
- C5 **Các cách bổ sung và công cụ tĩnh**: CovGate, FailLoc+Vote, ruff, pyrefly so với FailLoc.
- C6 **Độ bền RQ3**: heatmap (BugsInPy, đổi tên, 5 họ mô hình, 3 bộ nhãn) × phương pháp; và pareto đa họ mô hình (hình
  `pareto.pdf` hiện có, chuyển sang script mới, đổi tên phương pháp).
- C7 **Phân rã grounded/guessed** (Shapley): cột đóng góp dòng đoán vs phổ ở Acc@1/Acc@3.

Bảo vệ (`full`) thêm:
- C8 **Phân loại thất bại** (ch6).
- F7 **FailLoc+Verify**: đề xuất → sinh bản sửa → chạy test → xếp lại; kèm minh họa "test quá yếu để làm trọng tài"
  (bản sửa nhỏ làm mọi test đạt ở dòng không lỗi, `\PavmechReviewedOtherLineFixable`%).

Mỗi hình có caption tự đủ nghĩa (đọc caption + hình là hiểu, không cần văn bản). Văn bản quanh hình được rút gọn chỗ
trùng ý với hình; đoạn liệt kê dài có thể thành bảng. Bài báo EN (lần 2 trở đi) dùng cùng hình với nhãn tiếng Anh;
ở lần 1 bài báo không phải sản phẩm nộp — cập nhật EN có thể dồn sang lần 2 (Builder quyết thứ tự).

## Phần slide (phong cách kể chuyện)

**Nguyên tắc:** mỗi slide = một **câu kết luận làm tiêu đề** + **một hình làm bằng chứng**; chữ phụ ≤ 2 dòng. Hình vẽ
bằng SVG khối gốc trong `build_deck.py` (sửa được trong PowerPoint), màu template (ORANGE/LAVENDER/NAVY/CREAM), số đọc từ
`data/` như hiện nay. Được dùng: đoạn mã to có dòng lỗi tô sáng, ẩn dụ (hộp đen SemLoc được mở ra, "cuộc đua" giữa các
phương pháp, cán cân chi phí), con số lớn, và **mở dần**: cùng một hình lặp qua 2–3 slide, mỗi slide hiện thêm một lớp
(thay cho animation, an toàn khi xuất PDF).

**Mạch lần 1** (giữ các trang nhóm/phân công/công cụ AI/hiện trạng/tiến độ mà hướng dẫn của thầy yêu cầu, nhưng gọn và
có hình; Gantt cho tiến độ):
1. Móc: một đoạn mã Python có lỗi ngữ nghĩa, test fail — "dòng nào sai?"
2. Vấn đề: SBFL mù — test pass và fail đi cùng đường (ma trận phủ trực quan).
3. Lời hứa của SemLoc: quy trình nhiều bước, Acc@1 công bố — "neo vào bằng chứng thực thi".
4. Câu hỏi: Grounded hay guessed?
5. Mở hộp: thưởng ẩn → hạng 1 luôn là dòng đoán (mở dần: điểm phổ → thêm thưởng → dòng đoán vọt lên).
6. Mở hộp tiếp: nhãn trên dòng trống / không chạy tới → nhãn đã sửa (luồng gọn).
7. Thử cách đơn giản: FailLoc cạnh SemLoc (1 lượt vs nhiều lượt).
8. Kết quả: "cuộc đua" Acc@1/Acc@3, FailLoc dẫn; cán cân token.
9. Cliffhanger: "Thắng thật hay nhờ nhãn? Vì sao?" → lần 2.

**Lần 2** mở bằng tóm tắt lần 1 (1 slide), rồi trả lời cliffhanger: rà nhãn + duyệt mù, độ bền (lỗi thật, đổi tên, 5 họ
mô hình), ablation "test thất bại là tín hiệu chính", các cách bổ sung không giúp, đóng góp, hiện trạng.
**Bảo vệ**: trọn mạch + phân tích thất bại + FailLoc+Verify + bài học "test đủ gợi ý, quá yếu để làm trọng tài".

Số trang mỗi deck: Builder quyết, khoảng như hiện tại (lần 1 ≈ 20).

## Thứ tự giao

1. Đổi tên (bảng sinh tự động + văn bản VI + deck) — nền cho mọi hình.
2. Lần 1: slide (vì có thể trình bày ngay) và hình F1–F5, C1–C2 trong báo cáo VI; dựng PDF `main-lan1.pdf` + deck
   `bao-cao-lan-1.pptx`; cập nhật nhánh `bao-cao-lan-1`.
3. Lần 2: F6, C3–C7, deck lần 2, bài báo EN.
4. Bảo vệ: C8, F7, deck bảo vệ.

**Nếu thiếu thời gian cho lần 1** (giờ trình bày chưa rõ): làm theo thứ tự ưu tiên F1 → C1 → F3 → F4 → F2 → C2 → F5 →
Gantt → bảng phương pháp; slide và báo cáo cùng tiến theo thứ tự đó, mỗi mốc dựng lại được PDF + deck hoàn chỉnh. Hình
chưa kịp thì giữ nội dung cũ, không để chỗ trống. Thay PDF/deck lần 1 trên nhánh sau khi đã nộp là chấp nhận được
(Claude quyết).

## Các điểm đã chốt sau khi rà

- **FailLoc chỉ đổi nhãn, không đổi cách trình bày đóng góp.** Báo cáo đã gọi nó là "phương pháp do nhóm đề xuất" và
  bài báo đã ghi "(ours)", mô tả là "cách lập trình viên vẫn làm, được làm cho tái hiện được". Giữ nguyên khung đó; không
  viết thêm tuyên bố về tính mới.
- **Nhánh báo cáo:** theo đúng cách đã làm (reflog: `Reset to main` rồi một commit phát hành đặt `\Version` mặc định và
  chỉ giữ PDF + deck của nhánh) — tức reset về `main` và force-push. Đây là thao tác ra ngoài: hỏi trưởng nhóm ngay trước
  khi push.
- **Số liệu cho F3:** điểm từng dòng chỉ có trong `runs/semloc_*` (bị gitignore). Xuất một tệp nhỏ điểm-từng-dòng từ
  `runs/` vào `data/` bằng script (dữ liệu dẫn xuất, không chạy lại), rồi vẽ từ đó (Claude quyết).
- **Ngày trên Gantt** là lịch, không phải kết quả; lấy từ `docs/phan-cong.md` / `frontmatter/nhom.tex`, gõ trong một
  danh sách duy nhất trong `build_deck.py` (Claude quyết).
- **Thanh lỗi C1:** `d_acc*_lo/hi` là khoảng của chênh lệch so với SemLoc, không phải của từng phương pháp; vẽ sd qua 3
  lần chạy (ghi rõ trong caption) hoặc bootstrap từ `data/rankings` (Builder quyết).
- **C2 lần 1:** token/chương trình từ `llm_cost.csv` + Acc từ `rq2_ours.csv` (tập test, Gemini); `pareto.csv` là tập con
  dev và không có FailLoc nên không dùng ở lần 1.

## Để lại cho Builder

Bố cục cụ thể từng hình; chương trình ví dụ cho F2/F3; tên các id phụ; tách TikZ VI/EN thế nào; số trang deck; cách
kiểm tra hình (tối thiểu: `make -C docs/report check`, `pytest -m slow tests/test_report_build.py`, `make_decks.sh`
quality gate 0 lỗi, xem ảnh render từng slide).
