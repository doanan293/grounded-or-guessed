# Phân tích thất bại (Phase 3.2)

Nguồn: `data/failure_signals.csv` (190 chương trình test có ground truth đã sửa), `data/failure_cases.csv` (20 ca chọn có hệ thống), `data/failure_tolerance.csv`; sinh bằng `scripts/failure_cases.py`. SemLoc = 3 lần chạy Gemini 3.8 Flash của nhóm; tín hiệu nhị phân lấy theo đa số 3 lần.

## 1. Phân nhóm tự động trên 190 chương trình

| Nhóm | Định nghĩa | Số chương trình |
|---|---|---|
| `guess_right` | dòng LLM tự đoán (`fault_line`) là dòng ground truth | 94 |
| `coverage_only_wins` | SemLoc trượt top-3, LLM + độ phủ trúng top-3 | 32 |
| `rescued_by_spectrum` | đoán sai nhưng SemLoc vẫn có dòng lỗi trong top-3 | 25 |
| `prior_hurts` | phổ ngữ nghĩa xếp dòng lỗi hạng 1, điểm thưởng đẩy dòng đoán sai lên trên | 19 |
| `all_miss` | mọi phương pháp trượt | 14 |
| `gt_suspect` | ground truth chưa kiểm chứng được và mọi phương pháp trượt top-3 | 6 |

Một nửa (94/190) số chương trình được giải quyết bởi chính dòng đoán; 25 chương trình là nơi bằng chứng thực thi thật sự "cứu" SemLoc. Đây là phiên bản theo từng chương trình của phân rã Shapley (`data/rq_decomposition.csv`).

## 2. Phát hiện chính: phần lớn "thất bại" là dòng kề cạnh, không phải chỗ khác

**Độ lệch dòng đoán − ground truth** trên 559 lần đoán (3 lần × 190 chương trình, có thể trống): 0 → 281; +1 → 108; +2 → 63; −1 → 42; −2 → 26; |lệch| ≥ 3 → 39. Lần đoán sai lệch hẳn **xuống dưới** ground truth (dòng sau) hơn là lên trên, và LLM + độ phủ lệch y hệt (+1: 122, −1: 39).

**Quan hệ cú pháp** giữa dòng đoán (đa số) và ground truth, trên 96 chương trình đoán sai (`line_relation`, `src/flx/failures.py`):

| Quan hệ | Số | Ý nghĩa |
|---|---|---|
| `header_body` | 44 | một dòng là đầu câu lệnh ghép (`if`/`for`/`while`/…), dòng kia là câu lệnh nó bảo vệ |
| `blank_gt` | 11 | ground truth vẫn là dòng trống (11 chương trình `unverifiable`) |
| `other` | 41 | dòng khác — chủ yếu cùng luồng dữ liệu (xem P4) |

**Độ nhạy của Acc@1** (`data/failure_tolerance.csv`): nếu chấp nhận cả đầu khối lẫn thân khối là đúng, Acc@1 của SemLoc tăng từ 49,3 lên 71,8; của LLM + độ phủ từ 53,9 lên 76,8. Khoảng 22 điểm Acc@1 phụ thuộc vào việc người gán nhãn chọn dòng điều kiện hay dòng thân — lớn hơn mọi khác biệt giữa các phương pháp trong RQ2.

## 3. Đọc 20 ca: năm mẫu nguyên nhân

Ca được chọn bởi `select(per_category=4, seed=20261108)`, ưu tiên các cụm template khác nhau, bỏ nhóm `guess_right`.

**P1 — Ground truth ở dòng điều kiện, lỗi nằm ở câu lệnh được bảo vệ (hoặc ngược lại)** — 11/20 ca.
- `bump_conversion`, `task_tally`, `track_release`, `login_tally`: GT là `if updated > cap:` / `if cap is not None:`, LLM chỉ `updated = cap - 1`. Lỗi cài vào rõ ràng là `- 1` (đúng phải là `cap`); GT chưa kiểm chứng được. LLM đúng về ngữ nghĩa, sai một dòng.
- `credits_allocator`, `plan_points_share`, `plan_seats_share`: GT là `if _INTEGER_ALLOCATION:` / `if floor_to_int:`, LLM chỉ `int(x)` (cắt thay vì làm tròn). Lỗi ở dòng thân là cách đọc tự nhiên.
- `schedule_training`, `calendar_slot_insert`: GT là `for s, e in existing:`, LLM chỉ điều kiện chồng lấn `if not (end <= s or start >= e)` ngay dưới (lỗi biên `<=`/`<`).
- `throughput_trendline`, `confidence_trendline`: chiều ngược lại — GT trong thân `if not clamp:`, LLM chỉ chính điều kiện bị đảo `not`.

**P2 — Lỗi cài là một khối nhiều dòng** — 4/20 ca (`blend_supplies`, `combine_offsets`, `blend_orders`, `txn_dedup_merge`): đoạn `if merged and … merged[-1] == left[-1] == right[-1]: merged.pop()` được thêm vào; xóa bất kỳ dòng nào cũng sửa được lỗi. Ground truth chỉ nêu dòng `if`, LLM chỉ dòng `merged.pop()`. Điểm thưởng bị coi là "gây hại" (`prior_hurts`) ở đây chỉ vì GT chọn một trong hai dòng tương đương.

**P3 — Ground truth đã sửa của nhóm nhận một cách sửa *bù trừ*** — 3/20 ca. Đây là giới hạn của oracle "sửa tối thiểu một dòng làm mọi test pass" (`flx.verify_gt`):
- `gradient_clip_budget`: GT gốc 64 (dòng trống) được "sửa" thành 62 với `norm = _compute_global_norm(gradients) - 1`; lỗi thật là `max_norm / (norm + 1)` ở dòng 66 — LLM chỉ đúng 66 cả 3 lần.
- `storage_quota_split`: "sửa" ở dòng trống 64 bằng `total, fee = total - fee, 0`; lỗi thật nhiều khả năng ở `s - fee` dòng 70 (LLM chỉ 70).
- `feature_flag_rollout`: "xác nhận" dòng trống 62 bằng cách chèn `return bucket < percentage` — làm dòng 63 thành mã chết; lỗi thật là phép so sánh ở dòng 63 (LLM chỉ 63).
- Ở P2, oracle cũng "xác nhận" dòng `if` bằng cách đổi `==` thành `!=`/`<` — tắt khối lỗi thay vì xóa nó.

**P4 — Nguyên nhân và triệu chứng trên cùng luồng dữ liệu** (`fee_splitter`, `donation_share`, `cached_manifest`, `calibrate_pressure`; nhóm `other`): GT ở dòng tính giá trị, LLM chỉ dòng dùng giá trị (hoặc ngược lại). Không phân xử được chỉ bằng đọc mã; cần oracle thực thi cho *cả hai* dòng.

**P5 — Ground truth đáng ngờ không nằm ở dòng kề** (`reserve_slot`: GT là dòng `def overlaps(...)` lồng trong hàm, LLM chỉ điều kiện `_ADJACENCY_BUFFER > _MIN_SLOT_DURATION`; `room_reservation`): GT unverified, mọi phương pháp trượt.

## 4. Hệ quả

1. **Acc@1 cấp dòng trên SemFault-250 không ổn định về mặt định nghĩa.** Với lỗi trải trên điều kiện + câu lệnh được bảo vệ, chọn dòng nào là quy ước; Acc@1 thay đổi ~22 điểm theo quy ước đó. Báo cáo Acc@1 chặt *và* Acc@1 "đầu khối hoặc thân khối"; so sánh giữa phương pháp vẫn hợp lệ vì mọi phương pháp chịu cùng quy ước (LLM + độ phủ vẫn hơn SemLoc ở cả hai định nghĩa).
2. **"Guessed" phải được đọc cùng (1).** Dòng đoán của LLM thường *đúng về ngữ nghĩa nhưng lệch một dòng*; điểm thưởng "gây hại" (19 ca) gần như toàn là P1/P2 (18/19 `header_body`). Kết luận "hạng 1 chủ yếu đến từ dòng đoán" giữ nguyên; kết luận "bỏ điểm thưởng thì tốt hơn" thì không.
3. **Oracle sửa tối thiểu cần chống sửa bù trừ.** SemFault-250-verified kế thừa giới hạn này (P3). Ghi vào Threats to Validity; hướng sửa: (a) với mỗi dòng ứng viên, chỉ chấp nhận bản sửa không làm mã khác trở thành mã chết và không thêm `return`/hằng số bù; (b) cho phép ground truth nhiều vị trí (mọi dòng có bản sửa tối thiểu hợp lệ), phân xử thủ công các ca P1/P2 còn tranh chấp.
4. **Bằng chứng thực thi có ích thật ở 25 chương trình** (`rescued_by_spectrum`) — đúng chỗ phân rã Shapley quy công cho phổ ngữ nghĩa ở Acc@3.
