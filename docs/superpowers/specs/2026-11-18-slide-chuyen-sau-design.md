# Thiết kế: slide chuyên sâu theo yêu cầu của thầy và một báo cáo final

Ngày: 2026-11-18. Thay thế phần "slide" và "phiên bản báo cáo" của
`2026-11-18-hinh-va-ke-chuyen-design.md`; các phần khác của tài liệu đó (tên phương pháp, phong cách hình báo cáo, mạch
cải tiến, chống phóng đại) vẫn có hiệu lực.

## Ý định và lý do

Trưởng nhóm thấy deck lần 1 (15 trang) "cưỡi ngựa xem hoa": mỗi phương pháp một trang, chỉ có vài ô quy trình, người
nghe không hiểu phương pháp làm gì; nhiều chữ viết tắt cụt ("CT", "Phổ", "+thưởng", "Chèn, chạy", "k token", "CI").
Yêu cầu: mỗi phương pháp phải được giải thích cụ thể bằng sơ đồ, mạch kể bám sát những gì thầy yêu cầu
(`docs/requirement/HuongDanTieuLuan 2026.pdf`), và làm cùng lúc ba deck cùng báo cáo final.

Thành công = một người nghe chưa đọc gì, sau 20 phút, giải thích lại được: SBFL làm gì và vì sao mù với lỗi ngữ nghĩa;
SemLoc làm gì từng bước và chỗ nào nó overclaim; nhóm chuẩn hóa nhãn thế nào; FailLoc làm gì; FailLoc tốt hơn bao
nhiêu và bằng chứng nào cho thấy điều đó.

## Yêu cầu của thầy mà mạch kể phải làm nổi bật

- Slide (mục IV): "nêu bật và bám sát nội dung tiểu luận, đặc biệt là **cơ sở lý thuyết, phương pháp giải quyết vấn đề,
  cách cải tiến đã thực hiện, các thực nghiệm chứng minh các cải tiến, kết quả thu được**." → mỗi deck chia đúng năm phần
  này (trang mục lục nêu năm phần; tiêu đề phần là dải nhỏ trên đầu mỗi trang hoặc trang chia phần — Builder quyết).
- Tiến độ (mục II): lần 1 (18–19/11) ≥ 2/4 nội dung, lần 2 (25–26/11) ≥ 3/4; bốn nội dung: (1) tài liệu, từ khóa;
  (2) ≥ 3 RQ, thực nghiệm; (3) đóng góp, triết lý khoa học; (4) bài báo arXiv. → trang gắn nhãn nhỏ "[nội dung k]" ở
  nơi nội dung đó được trình bày.

## Quyết định của trưởng nhóm (18/11)

- Cách làm A: **một ví dụ chạy xuyên suốt** trên dữ liệu thật — chương trình `votes_apportion` (SemFault-250, tập test):
  lỗi ở dòng 29 (`int(v)` cắt phần lẻ); 1 test fail, 4 test pass, mọi dòng được cả 5 test chạy qua (SBFL hòa 0,45);
  SemLoc (lượt chạy 1, Gemini 3.8 Flash) đoán dòng 26 và viết ràng buộc thật (`runs/semloc_test_gemini_r1/constraints/
  votes_apportion.json`), điểm thưởng đẩy dòng 26 lên hạng 1 (sai); FailLoc trả `[29, 25, 26, 28, 30]` (đúng hạng 1,
  `data/rankings/direct_tests_test_gemini_r1.json`).
- Thời lượng: lần 1 và lần 2 mỗi lần ~20 phút (~23 trang), bảo vệ ~25 phút (~28 trang).
- Tiến độ: **một bảng** ở cuối deck lần 1 và lần 2 — việc, trạng thái (đã xong / chưa làm), tuần sẽ làm. Bảo vệ không có
  tiến độ.
- **Chỉ một báo cáo final.** Nhánh `bao-cao-lan-1`, `bao-cao-lan-2` chỉ mang deck của lần đó, không có PDF báo cáo.
- Thuật ngữ (đã lưu bộ nhớ): "test fail / test pass"; "phương pháp X" cho mọi tên phương pháp trong tiêu đề và câu;
  "chuẩn hóa nhãn / nhãn đã chuẩn hóa" (không "sửa nhãn"); "overclaim (tuyên bố quá mức)" là khẳng định của bài báo mạnh
  hơn bằng chứng — **điểm thưởng tự nó không phải overclaim**, overclaim là việc bài báo quy độ chính xác cho bằng chứng
  thực thi mà không mô tả điểm thưởng quyết định hạng 1.
- Không chữ cụt: mọi thuật ngữ định nghĩa ngay lần đầu xuất hiện trên slide (Acc@k, điểm phổ, Ochiai, nhãn, khoảng tin
  cậy, ablation, Shapley…); không viết tắt "CT", "CI", "k token" trên slide.

## Mục tiêu

1. Ba deck kể chuyện sâu theo năm phần của thầy, mỗi phương pháp 2–4 trang có sơ đồ và chạy trên ví dụ thật, mỗi trang
   có khung giải thích (hình cho thấy gì, đọc thế nào, ý chính) và speaker notes.
2. Một báo cáo final rà soát lại: thêm hình cho ví dụ chạy xuyên suốt ở phần phương pháp; làm nốt các hình còn lại của
   kế hoạch (rà soát nhãn, nhãn gốc đi đâu, ablation, các cách bổ sung, độ bền RQ3, pareto, phân rã, cải tiến dạng
   dumbbell, phân tích thất bại, FailLoc+Verify); soát thuật ngữ; bỏ cơ chế phiên bản lần 1/lần 2.
3. Bài báo tiếng Anh dùng cùng bộ hình (nhãn tiếng Anh).

## Không làm / chống mục tiêu

- Không chạy lại thí nghiệm; không số gõ tay (số đọc từ `data/`, `runs/` qua script, hoặc macro).
- Không so số công bố khác mô hình/bộ nhãn như so trực tiếp; mức hơn kèm khoảng tin cậy; không tuyên bố tính mới kỹ thuật
  cho FailLoc.
- Lần 1 không lộ nội dung lần 2 (rà soát nhãn, duyệt mù, RQ3, ablation, bổ sung, phân rã, đóng góp); lần 2 không lộ phân
  tích thất bại và FailLoc+Verify.
- Không quay lại kiểu slide một hình một câu: một trang mà người đọc không hiểu khi không có người nói là trang hỏng.

## Mạch các deck

Ký hiệu: (VD) = trang chạy trên ví dụ `votes_apportion`; số trang là gợi ý, Builder được gộp/tách miễn giữ thứ tự và
thời lượng.

**Lần 1 (~23 trang):**
1 Bìa · 2 Nội dung trình bày (năm phần + tiến độ) ·
*1. Cơ sở lý thuyết* — 3 Bài toán định vị lỗi (sơ đồ đầu vào → phương pháp → danh sách dòng xếp hạng; Acc@k) ·
4 (VD) lỗi ngữ nghĩa, 1 test fail · 5 Phương pháp SBFL: công thức Ochiai, tính tay cho một dòng ·
6 (VD) SBFL hòa 0,45 → mù; Acc@1 trên 250 chương trình · 7 Nghiên cứu liên quan: bộ từ khóa + 3 bài tiêu biểu, nhóm
áp dụng gì [nội dung 1] ·
*2. Phương pháp giải quyết: bài gốc SemLoc và câu hỏi nghiên cứu* — 8 Phương pháp SemLoc: sơ đồ năm bước, điều bài
báo khẳng định · 9 (VD) LLM đoán dòng 26, viết ràng buộc thật, mã sau khi chèn kiểm tra · 10 (VD) chạy test → ma trận
ràng buộc × test → Ochiai từng ràng buộc → điểm phổ từng dòng · 11 (VD) điểm thưởng +1,2 → dòng 26 hạng 1; bước vá thử
không đổi thứ hạng · 12 Ba câu hỏi nghiên cứu và giả thuyết [nội dung 2] ·
*3. Kiểm tra lại bài gốc (RQ1)* — 13 hạng 1 luôn là dòng đoán (tỉ lệ trên mọi lượt chạy), bỏ thưởng thì Acc@1 giảm:
chỗ overclaim · 14 nhãn của bộ dữ liệu có vấn đề · 15 chuẩn hóa nhãn bằng thực thi (sơ đồ bộ phán định, số từng nhánh) ·
*4. Cải tiến: phương pháp FailLoc* — 16 ý tưởng và lý do · 17 (VD) prompt đầy đủ → câu trả lời của LLM → đúng hạng 1 ·
18 năm phương pháp được so sánh (đầu vào, lượt gọi LLM, có chạy test) ·
*5. Thực nghiệm chứng minh và kết quả* — 19 thiết kế (dữ liệu, dev/test, 3 lần chạy, khoảng tin cậy bootstrap) ·
20 kết quả chính hai bộ nhãn · 21 cải tiến so với phương pháp SemLoc (trước → sau) ·
22 Tiến độ (bảng) · 23 Cảm ơn.

**Lần 2 (~23 trang):** 1 Bìa · 2 Nội dung trình bày · 3 Nhắc lại lần 1 trong một trang (bài toán, SemLoc, FailLoc,
kết quả, ba câu hỏi còn mở) ·
*1. Cơ sở lý thuyết bổ sung* — nhãn sai làm sai phép chấm (ví dụ), đo đồng thuận khi duyệt mù, ablation là gì (sơ đồ
bỏ từng thành phần), phân rã Shapley "bằng chứng hay phỏng đoán" (sơ đồ trò chơi hai thành phần) ·
*2. Phương pháp* — rà soát nhãn hai bước (sơ đồ), duyệt mù (sơ đồ: 60 chương trình, 2 người/chương trình, ứng viên
đánh chữ ngẫu nhiên), thiết kế RQ3 (lỗi thật BugsInPy, mã đổi tên định danh với (VD) trước/sau, năm họ mô hình),
ablation trên prompt (LLM-Direct → FailLoc → FailLoc+Cov, (VD) dòng chú thích độ phủ), các cách bổ sung (CovGate,
FailLoc+Vote) và công cụ phân tích tĩnh ·
*3–5. Thực nghiệm và kết quả* — nhãn gốc đi đâu + kết quả duyệt mù, kết quả trên ba bộ nhãn, độ bền (lỗi thật; đổi tên;
năm họ mô hình + chi phí), vì sao FailLoc thắng (ablation), các cách bổ sung không giúp, phân rã bằng chứng hay phỏng
đoán, cải tiến so với SemLoc trên mọi điều kiện ·
Đóng góp và triết lý khoa học [nội dung 3] · Tiến độ (bảng; nêu bản nháp bài báo [nội dung 4]) · Cảm ơn.

**Bảo vệ (~28 trang, không tiến độ):** toàn bộ mạch lần 1 (rút gọn phần ví dụ còn 1 trang/bước quan trọng) + rà soát
nhãn và duyệt mù + độ bền + ablation + phân tích thất bại (phân loại, một ví dụ nhãn mơ hồ) + FailLoc+Verify (sơ đồ, vì
sao "test đủ gợi ý nhưng quá yếu để làm trọng tài") + cải tiến tổng + đóng góp + triết lý khoa học + hạn chế và mối đe
dọa + kết luận + cảm ơn.

**Bảng tiến độ (lần 1, lần 2):** cột Việc | Trạng thái | Tuần thực hiện (ghi theo tuần, ví dụ "19–25/11"). Lần 1: đã
xong — chốt nhóm và đề tài; tài liệu và từ khóa (nội dung 1); 3 RQ và thiết kế (nội dung 2); tái hiện SemLoc (RQ1);
chuẩn hóa nhãn; so sánh chính FailLoc–SemLoc. Chưa làm — rà soát nhãn và duyệt mù, RQ3, ablation và các cách bổ sung,
đóng góp và triết lý (nội dung 3) → 19–25/11; phân tích thất bại, kiểm chứng bằng bản sửa → 26/11–05/12; bài báo arXiv
(nội dung 4) → 26/11–10/12; bảo vệ → 12/2026. Lần 2: cập nhật tương ứng.

## Báo cáo final

- Bỏ cơ chế phiên bản: mọi `\IfAtLeast…` thành nội dung luôn có; `make` chỉ dựng bản final + bài báo; test phiên bản
  (`tests/test_report_build.py`) đổi thành kiểm tra bản final (đủ chương, không còn "Báo cáo tiến độ", không "??", có
  danh sách hình, thuật ngữ mới). Bảng "Hiện trạng bốn nội dung" trong báo cáo bỏ (tiến độ chỉ ở slide).
- Phần phương pháp (ch3/ch4) thêm hình ví dụ chạy xuyên suốt: ràng buộc SemLoc trên `votes_apportion` (mã có chèn kiểm
  tra + ma trận ràng buộc × test) và prompt/câu trả lời của FailLoc. Các hình lần 1 hiện có giữ nguyên phong cách.
- Làm các hình còn lại của kế hoạch cũ (Task 10, 13, 14: F6, C3–C9, F7) và chèn vào chương tương ứng.
- Soát toàn văn: thuật ngữ trên, câu dài khó hiểu, mục overclaim theo đúng định nghĩa ở trên.

## Ràng buộc

- Deck dựng bằng `docs/presentation/build/` (build_deck.py, story.py, viz.py; ppt-master Edit Native PPTX; quality gate 0
  lỗi; `make_decks.sh`). Khung chữ nhiều dòng là một `<text>` với các `<tspan x dy>` (để lề thẳng).
- Báo cáo: quy cách của thầy (mục III.1.2), số qua macro, `make -C docs/report check`.
- Test hiện có phải xanh; test notes (`tests/test_deck_notes.py`) mở rộng cho lan2 và baove.
- Không đẩy nhánh khi chưa hỏi trưởng nhóm; commit không có dòng Claude.

## Các điểm đã chốt sau khi rà (Claude quyết, trưởng nhóm xem lại)

- **Hai ví dụ, không phải một.** Ở lượt chạy 1, SemLoc trên `votes_apportion` viết 4 ràng buộc nhưng **không ràng
  buộc nào bị vi phạm** trong 5 test: mọi điểm phổ bằng 0, thứ hạng chỉ có dòng 26 với 1,2 điểm, toàn bộ là điểm
  thưởng (vá thử trả rỗng). Đây là bằng chứng mạnh cho chỗ overclaim nhưng không cho thấy cơ chế chấm điểm hoạt động.
  Vì vậy: `votes_apportion` là ví dụ chính (SBFL hòa, SemLoc bước 1–2 và kết cục "ràng buộc không bắt được lỗi, hạng 1
  hoàn toàn là dòng đoán", FailLoc đúng hạng 1); **`blend_orders`** (nhãn được xác nhận bằng thực thi ở dòng 72; phổ
  vi phạm chỉ đúng dòng 72 với 1,00; dòng đoán 73 được 0,60 + 1,2 vượt lên; FailLoc trả `[72, 73, 64, 65, 71]`) là ví
  dụ thứ hai để minh họa ma trận ràng buộc × test → Ochiai → điểm phổ → điểm thưởng. Cả hai đều lấy từ lượt chạy 1,
  Gemini 3.8 Flash. Lưu ý: nhãn đã rà soát của `blend_orders` là hai dòng (72, 73); trang nào dùng ví dụ này ghi rõ
  "nhãn đã chuẩn hóa".
- **Cách nói về nhãn của `votes_apportion`:** dòng 29 là nhãn của cả ba bộ nhãn; bộ phán định không xác nhận được bằng
  một bản sửa nhỏ (sửa lỗi cắt phần lẻ cần nhiều hơn một dòng), nên slide ghi "dòng lỗi theo nhãn: 29", không ghi "đã
  xác nhận bằng chạy test".
- **Độ sâu theo phương pháp:** ba phương pháp chính (SBFL, SemLoc, FailLoc) mỗi phương pháp 2–4 trang có sơ đồ và ví dụ;
  các biến thể (LLM-Direct, SemLoc−Bonus, FailLoc+Cov, CovGate, FailLoc+Vote) mỗi cái **một trang** có sơ đồ nhỏ chỉ ra
  chỗ khác với phương pháp gốc; FailLoc+Verify (bảo vệ) hai trang.
- **Thứ tự và dự phòng:** deck lần 1 làm trước (đến hạn); deck 15 trang hiện tại (commit `d544bdd5`) giữ làm bản dự
  phòng tới khi deck mới qua kiểm tra. Rồi báo cáo final, deck lần 2, deck bảo vệ, bài báo tiếng Anh.

## Các cách đã cân nhắc

| Cách | Đánh đổi |
|---|---|
| **A. Một ví dụ chạy xuyên suốt trên dữ liệu thật (chọn)** | Người nghe theo một chương trình, thấy SemLoc sai và FailLoc đúng trên cùng bài; phụ thuộc một ví dụ → có câu nói rõ đây là minh họa, kết quả tổng ở phần sau |
| B. Mỗi phương pháp một khối chuẩn với ví dụ tự dựng | Gọn, nhưng ví dụ tự dựng kém thuyết phục, không cho thấy hai phương pháp trên cùng bài |
| C. Giữ khung cũ, thêm sơ đồ và chữ | Nhanh nhưng vẫn "cưỡi ngựa xem hoa" |

## Để lại cho Builder

Bố cục từng trang, chia trang trong khoảng thời lượng, dải tên phần hay trang chia phần, ví dụ con cho RQ3 (đổi tên)
và phân tích thất bại, thứ tự làm (gợi ý: deck lần 1 trước vì đến hạn, rồi báo cáo final, lần 2, bảo vệ, bài báo).
