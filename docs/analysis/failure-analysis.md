# Phân tích thất bại (Phase 3.2)

Nguồn: `data/failure_signals.csv` (mỗi chương trình test có ground truth đã sửa một dòng), `data/failure_cases.csv` (các ca chọn có hệ thống), `data/failure_tolerance.csv`, `data/failure_offsets.csv`; sinh bằng `scripts/failure_cases.py`. SemLoc = 3 lần chạy Gemini 3.8 Flash của nhóm; tín hiệu nhị phân lấy theo đa số 3 lần. Mỗi số kèm tên macro trong `docs/report/generated/numbers-vi.tex`; kiểm tra: `python scripts/check_claims.py docs/analysis/failure-analysis.md`.

## 1. Phân nhóm tự động

Trên 179 [`\FailProgramsN`] chương trình test có ground truth đã sửa:

| Nhóm | Định nghĩa | Số chương trình |
|---|---|---|
| `guess_right` | dòng LLM tự đoán (`fault_line`) là dòng ground truth | 94 [`\FailGuessRightN`] |
| `coverage_only_wins` | SemLoc trượt top-3, LLM + độ phủ trúng top-3 | 32 [`\FailCoverageOnlyWinsN`] |
| `rescued_by_spectrum` | đoán sai nhưng SemLoc vẫn có dòng lỗi trong top-3 | 25 [`\FailRescuedBySpectrumN`] |
| `prior_hurts` | phổ ngữ nghĩa xếp dòng lỗi hạng 1, điểm thưởng đẩy dòng đoán sai lên trên | 19 [`\FailPriorHurtsN`] |
| `gt_suspect` | ground truth chưa kiểm chứng được và mọi phương pháp trượt top-3 | 6 [`\FailGtSuspectN`] |
| `all_miss` | còn lại: mọi phương pháp trượt | 3 [`\FailAllMissN`] |

Khoảng một nửa số chương trình được giải quyết bởi chính dòng đoán; 25 [`\FailRescuedBySpectrumN`] chương trình là nơi bằng chứng thực thi thật sự "cứu" SemLoc — phiên bản theo chương trình của phân rã Shapley (`data/rq_decomposition.csv`).

## 2. Phát hiện chính: phần lớn "thất bại" là dòng kề cạnh

**Độ lệch dòng top-1 − ground truth gần nhất**, gộp 3 lần chạy (`data/failure_offsets.csv`). Dòng LLM tự đoán: 0 → 281 [`\OffLlmGuessZeroCount`]; +1 → 99 [`\OffLlmGuessOneCount`]; +2 → 61 [`\OffLlmGuessTwoCount`]; −1 → 28 [`\OffLlmGuessMinusOneCount`]; −2 → 26 [`\OffLlmGuessMinusTwoCount`]; |lệch| > 3 → 28 [`\OffLlmGuessFarCount`]. LLM + độ phủ lệch cùng hướng: +1 → 113 [`\OffLlmCoverageOneCount`] so với −1 → 24 [`\OffLlmCoverageMinusOneCount`]. Lần đoán sai lệch hẳn **xuống dưới** ground truth.

**Quan hệ cú pháp** giữa dòng đoán (đa số) và ground truth, trên 85 [`\FailWrongGuessN`] chương trình đoán sai (`line_relation`, `src/flx/failures.py`): 44 [`\FailRelationHeaderBodyN`] là cặp đầu câu lệnh ghép (`if`/`for`/`while`/…) và câu lệnh nó bảo vệ; 41 [`\FailRelationOtherN`] là quan hệ khác (chủ yếu cùng luồng dữ liệu, xem P4).

**Độ nhạy của Acc@1** (`data/failure_tolerance.csv`) khi chấp nhận cả đầu khối lẫn câu lệnh được bảo vệ. SemLoc: 52,3 [`\TolSemlocAccOneExact`] (chặt chẽ) → 73,9 [`\TolSemlocAccOneGuardStrict`] (chỉ dòng đầu khối và dòng đầu tiên của thân) → 76,2 [`\TolSemlocAccOneGuardOrBody`] (cận trên: cả câu lệnh đầu tiên của thân, tối đa 3 dòng, kể cả khối lồng nhau). LLM + độ phủ: 57,2 [`\TolLlmCoverageAccOneExact`] → 79,3 [`\TolLlmCoverageAccOneGuardStrict`] → 81,6 [`\TolLlmCoverageAccOneGuardOrBody`]. Hơn 20 điểm Acc@1 phụ thuộc vào việc người gán nhãn chọn dòng điều kiện hay dòng thân — lớn hơn mọi khác biệt giữa các phương pháp dùng LLM trong RQ2. Thứ tự giữa các phương pháp không đổi.

## 3. Đọc các ca: năm mẫu nguyên nhân

Ca do `select(per_category=4, seed=20261108)` chọn, ưu tiên các cụm template khác nhau, bỏ nhóm `guess_right` (nhóm `all_miss` chỉ có 3 ca → 19 ca).

**P1 — Ground truth ở dòng điều kiện, lỗi ở câu lệnh được bảo vệ (hoặc ngược lại)** — 6/19.
- `bump_click`: GT `if cap is not None and counters[key] > cap:`, LLM chỉ `counters[key] = cap - 1` — lỗi cài vào là `- 1`.
- `ledger_balance_rollup`: GT `elif kind == "debit":`, LLM chỉ `balance += amount` ngay dưới — với khoản ghi nợ, đúng phải là `-=`.
- `quota_for_fuel`: GT `if _INTEGER_ALLOCATION:`, LLM chỉ `int(x)` (cắt thay vì làm tròn).
- `calendar_slot_insert`: GT `for s, e in existing:`, LLM chỉ điều kiện chồng lấn `if not (end <= s or start >= e)` (lỗi biên).
- `gain_trendline`, `estimate_supply`: chiều ngược lại — GT ở thân `if not clamp:`, LLM chỉ chính điều kiện bị đảo `not`.

**P2 — Lỗi cài là một khối nhiều dòng** — 3/19 (`combine_offsets`, `versions_stream`, `latencies_merge`): đoạn `if merged and … merged[-1] == left[-1] == right[-1]: merged.pop()` được thêm vào; xóa bất kỳ dòng nào cũng sửa được. GT chỉ nêu một dòng, LLM chỉ dòng kia. `prior_hurts` ở đây chỉ vì GT chọn một trong hai dòng tương đương. Ở cả ba ca, oracle "xác nhận"/"sửa" bằng cách *tắt* khối (đổi `==` thành `!=`, hoặc `left = []` để điều kiện luôn sai) — cũng là P3.

**P3 — Oracle của nhóm nhận một bản sửa *bù trừ*** — 2/19 (cộng 2 ca của P2). Giới hạn của oracle "sửa tối thiểu một dòng làm mọi test pass" (`flx.verify_gt`):
- `gradient_clip_budget`: GT gốc 64 (dòng trống) được "sửa" thành 62 với `norm = _compute_global_norm(gradients) - 1`; lỗi thật là `max_norm / (norm + 1)` ở dòng 66 — LLM chỉ đúng 66 cả 3 lần.
- `energy_window_avg`: "xác nhận" dòng 72 bằng cách thay một lời gọi `_log.debug(...)` bằng `window = len(recent)`; lỗi thật ở phép chia dòng 74 (LLM chỉ 74).
- Bản sửa ở **dòng trống** cùng loại (ví dụ chèn `return merged` trước khối lỗi) đã bị loại khỏi ground truth đã sửa (`flx.gt.repaired_gt`, 13 [`\GtBlankFixDroppedN`] chương trình); bản sửa bù trừ ở dòng có mã thì chưa phát hiện tự động được.

**P4 — Nguyên nhân và triệu chứng trên cùng luồng dữ liệu, hoặc lỗi thiếu mã** — 4/19.
- `allocate_bounty_cut`: GT `return [_clamp_payout(share - fee) …]` (trừ phí trên từng phần), LLM chỉ dòng tính `base` — cả hai đều có thể là chỗ sửa.
- `shift_trust`, `shift_risk`: thiếu bước chuẩn hóa tổng; GT là dòng nơi oracle chèn phép chia, LLM chỉ dòng `return`/kẹp giá trị — một lỗi thiếu mã không có "dòng sai" duy nhất.
- `warm_cache_loader`: `expires_at` được tính nhưng không lưu; GT ở `return value`, LLM chỉ dòng tính `expires_at`.
Không phân xử được chỉ bằng đọc mã; cần oracle thực thi cho *cả hai* dòng.

**P5 — Ground truth đáng ngờ, không kề cạnh** — 4/19.
- `reserve_slot`, `schedule_call`: GT là dòng `def overlaps(...)` lồng trong hàm; LLM chỉ điều kiện/bước kiểm tra phía trên.
- `room_reservation`: GT `for s, e in existing:`; các lần chạy không thống nhất.
- `file_chunk_stitch`: GT `data += part`, LLM chỉ `return data[:-1]` — phép cắt `[:-1]` mới là lỗi rõ ràng; GT chưa kiểm chứng được.

## 4. Hệ quả

1. **Acc@1 cấp dòng trên SemFault-250 không ổn định về định nghĩa.** Với lỗi trải trên điều kiện + câu lệnh được bảo vệ, chọn dòng nào là quy ước; Acc@1 đổi hơn 20 điểm theo quy ước đó (ngay cả ở biến thể chặt). Báo cáo Acc@1 chặt và Acc@1 chấp nhận đầu khối/thân khối; so sánh giữa phương pháp vẫn hợp lệ vì mọi phương pháp chịu cùng quy ước.
2. **"Guessed" phải được đọc cùng (1).** Dòng đoán của LLM thường đúng về ngữ nghĩa nhưng lệch một dòng; các ca `prior_hurts` chủ yếu là P1/P2. Kết luận "hạng 1 chủ yếu đến từ dòng đoán" giữ nguyên; kết luận "bỏ điểm thưởng thì tốt hơn" thì không.
3. **Oracle sửa tối thiểu cần chống sửa bù trừ.** Hướng sửa: loại bản sửa làm mã khác thành mã chết, thêm `return` sớm, hay thay lời gọi log; cho phép ground truth nhiều vị trí và phân xử thủ công các ca P1/P2/P4 còn tranh chấp.
4. **Bằng chứng thực thi có ích thật ở một phần tư số chương trình đoán sai** (`rescued_by_spectrum`) — đúng chỗ phân rã Shapley quy công cho phổ ngữ nghĩa ở Acc@3.
