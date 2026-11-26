# Thiết kế: ba lần báo cáo tiến độ và bảo vệ, kèm trang luồng phương pháp trên ví dụ

Ngày: 2026-11-25. Thay phần chia deck của `2026-11-18-slide-chuyen-sau-design.md` (hai lần báo cáo + bảo vệ). Các quy
ước khác của tài liệu đó và của bộ nhớ dự án vẫn giữ: thuật ngữ, ví dụ chạy xuyên suốt `votes_apportion`, biểu đồ thanh,
trang tự giải thích, không có trang Hạn chế, mọi số liệu đọc từ `data/`.

## Ý định và lý do

Thầy đổi lịch: trước buổi bảo vệ có **ba** buổi báo cáo tiến độ thay vì hai. Mỗi buổi kể tuần vừa rồi nhóm đã làm gì và
ra kết quả gì. Coi như slide lần 1 hiện tại chưa được trình bày, nên toàn bộ nội dung được chia lại thành lần 1, lần 2,
lần 3 và bảo vệ.

Vì có nhiều buổi trình bày, trưởng nhóm muốn mỗi phương pháp nhóm đề xuất được giải thích rõ bằng **sơ đồ luồng chạy trên
một ví dụ thật**: đầu vào, các bước, mỗi bước sinh ra gì, cuối cùng dòng lỗi đứng hạng mấy. Trang hiện nay
(`failloc_y_tuong`, `bo_sung`, `ablation_la_gi`) chỉ có các hộp chung chung, chưa đi qua ví dụ.

Thành công: người nghe xem trang luồng của FailLoc, FailLoc+Cov, SemLoc−Bonus và kể lại được phương pháp đó nhận gì, làm
gì, khác phương pháp bên cạnh ở đúng chỗ nào, và trên ví dụ thì ra kết quả gì.

## Mục tiêu, không làm, phản mục tiêu

Mục tiêu
- Bốn deck: `lan1`, `lan2`, `lan3`, `baove`. Mỗi lần tiến độ là việc của một tuần, theo mạch công việc.
- Lần 2 và lần 3 khoảng **18 trang** mỗi lần (kể cả bìa và trang cảm ơn). Lần 1 không quan trọng về độ dài; giữ gần như
  cũ, rút còn khoảng 16 trang bằng cách đẩy phần đã chuyển sang lần 2.
- Trang luồng đầy đủ kèm ví dụ cho **FailLoc**, **FailLoc+Cov**, **SemLoc−Bonus**. FailLoc+Vote, CovGate, FailLoc+Verify
  có luồng gọn (sơ đồ hộp + một dòng ví dụ, như luồng Vote trên trang `bo_sung` hiện nay).
- Bảo vệ vẫn 28 trang (`story_baove.BAOVE` và test hiện tại là 28), dùng các trang luồng mới thay trang hộp chung.

Không làm
- Không ghi ngày trên bìa và trong bảng tiến độ. Bìa ghi "Báo cáo lần 1/2/3", "Bảo vệ tiểu luận". Bảng tiến độ hẹn theo
  mốc "Lần 2", "Lần 3", "Bảo vệ".
- Không động tới báo cáo LaTeX và bài báo (chỉ còn bản final; `\IfAtLeast` giữ nguyên).
- Không chạy thí nghiệm mới. Ví dụ trên trang luồng lấy từ kết quả đã có trong `data/` và `runs/`.

Phản mục tiêu
- Một lần tiến độ kể lại cả câu chuyện (lặp như bảo vệ thu nhỏ).
- Lần sau lộ nội dung của lần trước đó chưa tới (lần 1 lộ kết quả của lần 2, v.v.).
- Ví dụ trên trang luồng bị bịa hoặc chọn sao cho phương pháp trông tốt hơn dữ liệu cho thấy.

## Cách đã cân nhắc

- **A. Chia theo mạch công việc từng tuần** (trưởng nhóm chọn). Lần 1 tìm hiểu và tái hiện; lần 2 sửa nhãn và đề xuất
  FailLoc; lần 3 kiểm chứng độ bền và đóng góp. Gần như chỉ sắp lại trang đã có, cộng các trang luồng mới.
- B. Giữ lần 1 và 2, thêm lần 3 gồm các trang hiện chỉ ở bảo vệ. Loại: lần 1 vẫn 22 trang, lần 3 thành túi lẫn lộn, bảo
  vệ không còn gì mới.
- C. Mỗi lần kể lại cả câu chuyện rồi thêm phần mới. Loại: lặp, trái với "tuần vừa rồi làm gì".

## Chia nội dung (đã thống nhất)

Tên trang là tên hiện có trong `story_lan1.py`, `story_lan2.py`, `story_baove.py`; "MỚI" là trang cần dựng.

**Lần 1, tìm hiểu và tái hiện (~16 trang).** Bìa, mục lục, bài toán, ví dụ, SBFL (công thức và mù với lỗi ngữ nghĩa),
nghiên cứu liên quan, ba trang SemLoc, ba RQ, thiết kế thực nghiệm, kết quả tái hiện SemLoc (overclaim), phát hiện nhãn
sai (`nhan_sai`), tiến độ, cảm ơn. Không có nhãn đã chuẩn hóa, không có kết quả so sánh chính. Trang `cau_hoi` dùng chung, giữ nguyên bốn RQ (RQ là kế hoạch, nên được nêu tên FailLoc là phương pháp nhóm sẽ đề xuất); `phuong_phap` và `thiet_ke_tn` nêu nhãn đã chuẩn hóa nên chuyển sang lần 2 *(quyết định của người viết thiết kế)*.

**Lần 2, sửa nhãn và đề xuất FailLoc (~18 trang).** Bìa, mục lục, nhắc lại lần 1, chuẩn hóa nhãn (`chuan_hoa`), ý tưởng
FailLoc, **luồng FailLoc trên ví dụ (MỚI)**, **luồng SemLoc−Bonus trên ví dụ (MỚI)**, phương pháp so sánh, kết quả chính
(RQ2, `ket_qua`), cải tiến (`cai_tien`), nhãn lệch, rà soát nhãn và duyệt mù, nhãn đi đâu, ba bộ nhãn, tiến độ, cảm ơn.

**Lần 3, kiểm chứng độ bền và đóng góp (~18 trang).** Bìa, mục lục, nhắc lại lần 2, ablation là gì, **luồng FailLoc+Cov
trên ví dụ (MỚI)**, các hướng bổ sung với luồng gọn của Vote và CovGate (`bo_sung`), thiết kế RQ3, BugsInPy, đổi tên,
họ mô hình, kết quả ablation, kết quả bổ sung, chi phí (`cai_tien_2`), đóng góp, tiến độ, cảm ơn.

**Bảo vệ (28 trang).** Như `story_baove.BAOVE` hiện nay, thay trang hộp chung bằng ba trang luồng mới, có trang luồng gọn
của Verify trên `verify_bv`. Nếu thêm trang làm vượt 28 thì gộp hoặc bỏ trang khác để giữ 28.

Số trang có thể xê dịch một hai trang khi dựng; ranh giới nội dung giữa các lần thì giữ như trên.

## Trang luồng phương pháp

Một trang cho mỗi phương pháp, đọc từ trái sang phải:

```
 Ví dụ (tên chương trình, dòng lỗi)
 [Đầu vào thật] → [Bước 1: nội dung thật] → [Bước 2 …] → [Kết quả: top-5, dòng lỗi hạng k ✓/✗]
 Khác phương pháp X ở đúng một chỗ: …
```

- Mỗi hộp mang nội dung thật của ví dụ (trích dòng mã, trích prompt, danh sách hạng), không chỉ tên bước.
- Một dòng dưới sơ đồ nói phương pháp này khác phương pháp liền trước ở đâu (FailLoc so với LLM-Direct; FailLoc+Cov so
  với FailLoc; SemLoc−Bonus so với SemLoc).
- Speaker notes giải thích lại trang bằng lời.

Ví dụ cho từng trang:
- **FailLoc**: ví dụ 1 `votes_apportion` (dòng lỗi 29; FailLoc trả `[29, 25, 26, 28, 30]`). Trang `failloc_vd` hiện có
  prompt thật; trang luồng có thể thay `failloc_y_tuong` hoặc gộp hai trang thành một, Builder quyết.
- **SemLoc−Bonus**: ví dụ 1, lượt chạy `semloc_test_gemini_r1`. SemLoc viết 4 ràng buộc, không ràng buộc nào bị vi phạm
  (Ochiai đều 0), nên điểm duy nhất là thưởng 1,2 cho dòng 26 mà LLM đoán (`runs/semloc_test_gemini_r1/scores/votes_apportion.json`).
  Gạch bước thưởng thì không còn dòng nào được xếp hạng: thứ hạng của SemLoc ở ví dụ này đến hoàn toàn từ dự đoán, không
  từ phổ vi phạm. Dưới sơ đồ ghi số tổng: Acc@1 của SemLoc giảm từ … xuống … khi bỏ thưởng (đọc từ `data/`). Không chọn
  ví dụ nào làm SemLoc−Bonus trông tốt hơn số tổng *(quyết định của người viết thiết kế)*.
- **FailLoc+Cov**: ở ví dụ 1 mọi dòng đều `[f=1/p=4]`, nên độ phủ không thêm gì. Chọn một chương trình mà FailLoc+Cov đưa
  được dòng lỗi vào top 3 (ví dụ `file_chunk_stitch`, `ledger_balance_rollup`, `shift_trust`, `shift_risk`); trang chỉ gọi
  nó là "ví dụ 2 cho độ phủ", không nhắc tên nhóm của phân tích thất bại (phần đó chỉ có ở bảo vệ), và ghi số tổng của
  FailLoc+Cov so với FailLoc *(quyết định của người viết thiết kế)*.

## Phần dựng và kiểm tra

- `build_deck.py`: thêm `lan3` vào `DECKS`, `OCCASION`, `OUT_NAME`; `OCCASION` bỏ ngày. Thêm `story_lan3.py` theo mẫu
  `story_lan2.py` (danh sách `LAN3`, `pages`, `notes`). Các trang dùng chung giữa nhiều deck được dựng một lần ở module
  sinh ra nó, như bảo vệ đang dùng lại trang lần 1 và lần 2.
- `make_decks.sh`: thêm `lan3` → `slide-lan-3.pptx` + `.pdf`, mặc định dựng cả bốn.
- `tests/test_deck_text.py`: `test_label_tree_counts_add_up` chuyển sang đọc `chuan_hoa` của lần 2; lần 1 không lộ lần 2; lần 2 không lộ lần 3; lần 3 không lộ phần chỉ có ở bảo vệ
  (phân tích thất bại, Verify); lần 2 và lần 3 ≤ 18 trang (hoặc ≤ 19 nếu Builder cần); bảo vệ 28 trang; quy tắc chữ cấm
  áp dụng cho cả bốn deck.
- Bảng tiến độ của từng lần: việc, trạng thái, mốc "Lần 2/Lần 3/Bảo vệ".
- `README.md` của build và bộ nhớ `milestone-staging` cập nhật thành ba lần.

## Để Builder quyết

- Hình thức sơ đồ cụ thể (dùng `viz.pipeline` hay vẽ mới), cỡ chữ, cách trích mã cho vừa trang.
- Chương trình cụ thể cho FailLoc+Cov trong nhóm `coverage_only_wins`.
- Gộp hay tách trang cụ thể để đạt khoảng 18 trang, miễn giữ ranh giới nội dung ở trên.
- Lời của tiêu đề, mục lục và speaker notes theo quy ước thuật ngữ hiện có.
