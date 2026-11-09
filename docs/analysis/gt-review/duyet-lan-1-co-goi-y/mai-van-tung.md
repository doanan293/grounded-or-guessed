# Duyệt nhãn dòng lỗi — Mai Văn Tùng (18 ca)

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;
  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.
- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.
- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật
  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.
- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.
- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.

## 1. `bump_purchase`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/bump_purchase.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_bump_purchase.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 64

```python
    57:     """
    58:     _validate_cap(cap)
    59:     current = _resolve_current(counters, key)
    60:     updated = current + INCREMENT_STEP
    61: 
    62:     if cap is not None:
>>  63:         if updated > cap:
>>  64:             updated = cap - 1
    65: 
    66:     counters[key] = updated
    67:     _log.debug("Counter for %s updated from %d to %d", key, current, updated)
    68:     return updated
```

> LLM: other (high): Counter must be clamped to cap (test_counter_above_cap_is_clamped expects 5 for cap=5); line 64 sets updated = cap - 1. Label 63 is the correct guard `if updated > cap`; the fault is the `- 1` on line 64.

## 2. `calibrate_lift`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_lift.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_lift.py)

- G (nhãn gốc): dòng 64
- F (LLM đề xuất): dòng 63

```python
    57:     segment_length = abs(x1 - x0)
    58:     _log.debug("Segment length: %.6f (min allowed: %.6f)", segment_length, MIN_SEGMENT_LENGTH)
    59: 
    60:     t = (x - x0) / (x1 - x0)
    61:     y = _interpolate(t, y0, y1)
    62: 
>>  63:     if not clamp:
>>  64:         low, high = sorted([y0, y1])
    65:         y = min(max(y, low), high)
    66: 
    67:     return y
```

> LLM: other (high): Docstring: clamp=True restricts output to the segment's y-range; line 63 `if not clamp:` inverts the condition so clamping happens only when clamp=False. Label 64 (`low, high = sorted([y0, y1])`) is a correct statement inside the mis-guarded block.

## 3. `confidence_trendline`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/confidence_trendline.py#L77) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_confidence_trendline.py)

- G (nhãn gốc): dòng 79
- F (LLM đề xuất): dòng 77

```python
    71: 
    72:     ratio = _compute_interpolation_ratio(x0, x1, x)
    73:     y = y0 + ratio * (y1 - y0)
    74: 
    75:     _log.debug("Interpolated confidence at x=%s: raw_y=%s, clamp=%s", x, y, clamp)
    76: 
>>  77:     if not clamp:
    78:         lo, hi = (min(y0, y1), max(y0, y1))
>>  79:         if y < lo:
    80:             y = lo
    81:         elif y > hi:
    82:             y = hi
    83: 
    84:     y = max(DEFAULT_CONFIDENCE_FLOOR, min(DEFAULT_CONFIDENCE_CEILING, y))
    85: 
```

> LLM: other (high): Clamping must apply when clamp=True, but line 77 reads `if not clamp:` (inverted condition); label line 79 `if y < lo:` is correct code inside the inverted block.

## 4. `donation_share`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/donation_share.py#L58) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_donation_share.py)

- G (nhãn gốc): dòng 59
- S (nhóm dời tới): dòng 58, bản sửa: `    base = list(map(lambda r: (r / total_ratio) * (amount - fee) + fee, ratios))`

```python
    52:     if amount < 0:
    53:         raise ValueError("negative amount")
    54: 
    55:     _log.debug("Distributing %.2f among %d recipients (fee=%.2f)", amount, len(ratios), fee)
    56: 
    57:     total_ratio = sum(ratios)
>>  58:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
>>  59: 
    60:     payouts = [_round_payout(max(_MIN_PAYOUT, b - fee)) for b in base]
    61:     return payouts
```

> LLM: new (medium): Docstring/tests: fee is deducted from the gross amount before proportional splitting, but line 58 splits the full `amount` and line 60 subtracts the whole `fee` per recipient. The fault spans 58 and 60 (natural fix: `(amount - fee)` on 58 and drop `- fee` on 60, verified passing); the oracle's `+ fee` on 58 is an algebraic trick but lands on one of the two faulty lines. Original 59 is blank.

## 5. `estimate_temperature`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/estimate_temperature.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_estimate_temperature.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 68, bản sửa: `    if clamp:`

```python
    62:     _validate_segment(x0, x1)
    63: 
    64:     segment_length = x1 - x0
    65:     t = (x - x0) / (x1 - x0)
    66:     y = (1 - t) * y0 + t * y1
    67: 
>>  68:     if not clamp:
>>  69:         low, high = sorted([y0, y1])
    70:         y = min(max(y, low), high)
    71: 
    72:     _log.debug("Interpolated temp at x=%.4f: t=%.4f, y=%.4f", x, t, y)
    73:     return _round_temperature(y)
```

> LLM: new (high): `if not clamp:` on line 68 inverts the documented clamp flag. Original label 69 (`low, high = sorted([y0, y1])`) is a correct body statement of that guard.

## 6. `gain_trendline`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/gain_trendline.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_gain_trendline.py)

- G (nhãn gốc): dòng 71
- F (LLM đề xuất): dòng 70

```python
    64:     if abs(x1 - x0) < MIN_SEGMENT_LENGTH:
    65:         raise ValueError("degenerate segment")
    66: 
    67:     t = _compute_parameter(x, x0, x1)
    68:     y = y0 + t * (y1 - y0)
    69: 
>>  70:     if not clamp:
>>  71:         lo, hi = (min(y0, y1), max(y0, y1))
    72:         if y < lo:
    73:             y = lo
    74:         if y > hi:
    75:             y = hi
    76: 
    77:     _log.debug("gain_trendline: x=%s, t=%.4f, y=%.4f", x, t, y)
```

> LLM: other (high): Label 71 (`lo, hi = min/max(y0, y1)`) is correct. The fault is the inverted guard on line 70 `if not clamp:` which clamps only when clamp=False; the docstring says clamping happens when clamp is True.

## 7. `invoice_meter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/invoice_meter.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_invoice_meter.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 64

```python
    57:     _validate_key(key)
    58:     effective_max = _resolve_max(max_value)
    59: 
    60:     new_value = counts.get(key, 0) + 1
    61: 
    62:     if effective_max is not None:
>>  63:         if new_value > effective_max:
>>  64:             new_value = effective_max - 1
    65: 
    66:     counts[key] = new_value
    67:     _log.debug("meter %s updated to %d (cap=%s)", key, new_value, effective_max)
    68:     return new_value
```

> LLM: other (high): Label 63 `if new_value > effective_max` is a correct guard. The deviation is line 64 `new_value = effective_max - 1`: the docstring says the counter is capped at max_value, so it should be `effective_max`. No edit of line 63 alone can satisfy test_cap_reached_exactly.

## 8. `limit_message`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_message.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_message.py)

- G (nhãn gốc): dòng 72
- S (nhóm dời tới): dòng 73, bản sửa: `    if len(recent) >= limit:`

```python
    66:     recent = _compute_recent_timestamps(timestamps, cutoff)
    67: 
    68:     _log.debug(
    69:         "Rate-limit check: %d recent messages in %ds window (limit %d)",
    70:         len(recent), window, limit,
    71:     )
>>  72: 
>>  73:     if len(recent) > limit:
    74:         return False, 0
    75:     return True, limit - len(recent)
```

> LLM: new (high): `len(recent) > limit` on line 73 should be `>=` (test `test_exactly_at_limit_should_deny_next_message`). Original label 72 is blank.

## 9. `lr_warmup_schedule`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/lr_warmup_schedule.py#L57) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_lr_warmup_schedule.py)

- G (nhãn gốc): dòng 57
- F (LLM đề xuất): dòng 59

```python
    51:     Raises:
    52:         ValueError: If warmup_steps is not positive or step is negative.
    53:     """
    54:     _validate_positive_int(warmup_steps, "warmup_steps")
    55:     _validate_non_negative(step, "step")
    56: 
>>  57:     if step >= warmup_steps:
    58:         return base_lr
>>  59:     lr = base_lr * ((step + 1) / warmup_steps)
    60: 
    61:     _log.debug("step=%d  lr=%.6e", step, lr)
    62:     return max(lr, MIN_LR_FLOOR)
```

> LLM: other (high): Label 57 `if step >= warmup_steps: return base_lr` is correct (step 100 of 100 returns base_lr either way). The deviation is line 59 `base_lr * ((step + 1) / warmup_steps)`: tests require lr=0 at step 0 and 1% at step 1, i.e. `step / warmup_steps` without the `+ 1`.

## 10. `payment_split_rebate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/payment_split_rebate.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_payment_split_rebate.py)

- G (nhãn gốc): dòng 65
- F (LLM đề xuất): dòng 66

```python
    59:     _validate_ratios(ratios)
    60: 
    61:     total_ratio = sum(ratios)
    62:     shares = [_round_share((r / total_ratio) * total) for r in ratios]
    63: 
    64:     _log.debug("Computed raw shares: %s (rebate=%.4f)", shares, rebate)
>>  65: 
>>  66:     return [s - rebate for s in shares]
```

> LLM: other (medium): Label 65 is a blank line. Docstring: rebate is subtracted from the pool before distribution (sum == total - rebate), but line 62 splits the gross `total` and line 66 subtracts the full rebate from each share; the deviating statement is line 66 (two-line fault 62+66).

## 11. `quota_for_memory`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/quota_for_memory.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_quota_for_memory.py)

- G (nhãn gốc): dòng 70
- F (LLM đề xuất): dòng 72

```python
    64:         raise ValueError("minimum must be non-negative")
    65: 
    66:     _validate_weights(weights)
    67: 
    68:     planned = _compute_planned(total, weights, minimum)
    69:     _log.debug("planned allocations (raw): %s", planned)
>>  70: 
    71:     if _INTEGER_ALLOCATION:
>>  72:         allocations = [int(x) for x in planned]
    73:     else:
    74:         allocations = planned  # type: ignore[assignment]
    75: 
    76:     return allocations
```

> LLM: other (medium): Label 70 is a blank line. The truncation `[int(x) for x in planned]` on line 72 (inside `if _INTEGER_ALLOCATION:` at 71) loses the remainder; tests require sum(result) == total.

## 12. `reserve_band`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/reserve_band.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_reserve_band.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 68

```python
    61: 
    62:     if _compute_band_width(candidate) < _MIN_BAND_WIDTH:
    63:         raise ValueError(
    64:             f"Band width {_compute_band_width(candidate)} is below minimum {_MIN_BAND_WIDTH}"
    65:         )
    66: 
>>  67:     def overlaps(a: Tuple[float, float], b: Tuple[float, float]) -> bool:
>>  68:         return not (b[1] <= a[0] or b[0] >= a[1])
    69: 
    70:     for slot in existing:
    71:         if overlaps(slot, candidate):
    72:             _log.debug(
    73:                 "Candidate band %s conflicts with existing slot %s",
    74:                 candidate,
```

> LLM: other (high): Label 67 is the `def overlaps(...)` header; the deviating comparison is its body on line 68 `not (b[1] <= a[0] or b[0] >= a[1])` (touching bands accepted, tests reject them). Verified: patching line 68 to `<`/`>` makes all 9 tests pass (original: 5 fail).

## 13. `room_reservation`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/room_reservation.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_room_reservation.py)

- G (nhãn gốc): dòng 69
- F (LLM đề xuất): dòng 70

```python
    63:     start, end = interval
    64:     _validate_interval(start, end)
    65:     _check_capacity(existing)
    66: 
    67:     _log.debug("Checking interval (%d, %d) against %d existing bookings", start, end, len(existing))
    68: 
>>  69:     for s, e in existing:
>>  70:         if not (end <= s or start >= e):
    71:             return False, existing
    72: 
    73:     updated = existing + [interval]
    74:     updated.sort()
    75:     return True, updated
```

> LLM: other (high): Label 69 is the `for` header; the deviating comparison is line 70 `not (end <= s or start >= e)` (touching intervals accepted, tests reject). Verified: patching line 70 to `<`/`>` makes all tests pass.

## 14. `schedule_training`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_training.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_training.py)

- G (nhãn gốc): dòng 66
- F (LLM đề xuất): dòng 67

```python
    60:         OverflowError: If the schedule has reached maximum capacity.
    61:     """
    62:     start, end = interval
    63:     _validate_interval(start, end)
    64:     _check_capacity(existing)
    65: 
>>  66:     for s, e in existing:
>>  67:         if not (end <= s or start >= e):
    68:             _log.debug(
    69:                 "Conflict detected: proposed (%s, %s) overlaps with (%s, %s)",
    70:                 start, end, s, e,
    71:             )
    72:             return False, existing
    73: 
```

> LLM: other (high): Label 66 is the `for` header; the deviating comparison is line 67 `not (end <= s or start >= e)` (touching sessions accepted, tests reject). Verified: patching line 67 to `<`/`>` makes all 10 tests pass (original: 5 fail).

## 15. `slots_apportion`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/slots_apportion.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_slots_apportion.py)

- G (nhãn gốc): dòng 69
- F (LLM đề xuất): dòng 70

```python
    63: 
    64:     total_weight = sum(weights)
    65:     planned = _compute_planned_allocations(total, weights, total_weight, minimum)
    66: 
    67:     if _INTEGER_ALLOCATION:
    68:         _log.debug("Rounding %d planned allocations to integers", len(planned))
>>  69: 
>>  70:     allocations = [int(x) for x in planned]
    71:     return allocations
```

> LLM: other (medium): Label 69 is a blank line inside the `if _INTEGER_ALLOCATION:` log block. Docstring explicitly requires largest-remainder apportionment; line 70 `[int(x) for x in planned]` truncates and drops the remainder.

## 16. `temperature_window_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/temperature_window_avg.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_temperature_window_avg.py)

- G (nhãn gốc): dòng 68
- F (LLM đề xuất): dòng 67

```python
    61:     _validate_window(window)
    62:     _validate_series(values)
    63: 
    64:     tail = values[-window:]
    65:     total = sum(tail)
    66: 
>>  67:     mean = total / window
>>  68: 
    69:     _log.debug("window=%d, tail_len=%d, mean=%.4f", window, len(tail), mean)
    70: 
    71:     if len(tail) < warmup_min:
    72:         return None
    73:     return mean
```

> LLM: other (high): Label 68 is a blank line; the fault is line 67 `mean = total / window`, which must divide by `len(tail)` (the oracle's confirmed fix was an inserted line at the blank).

## 17. `track_delivery`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/track_delivery.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_track_delivery.py)

- G (nhãn gốc): dòng 70
- F (LLM đề xuất): dòng 72

```python
    64:         ValueError: If the provided cap is below the minimum allowed value.
    65:     """
    66:     _validate_cap(cap)
    67:     current = _resolve_current(counters, key)
    68:     updated = current + INCREMENT_STEP
    69: 
>>  70:     if cap is not None:
    71:         if updated > cap:
>>  72:             updated = cap - 1
    73: 
    74:     counters[key] = updated
    75:     _log.debug("Delivery counter for '%s' updated to %d", key, updated)
    76:     return updated
```

> LLM: other (high): Label 70 `if cap is not None:` is a correct outer guard; the deviating token is on line 72 `updated = cap - 1` (docstring: counter will not exceed cap, i.e. clamp to cap). Verified: patching only line 72 makes all tests pass.

## 18. `upload_gate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/upload_gate.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_upload_gate.py)

- G (nhãn gốc): dòng 73
- S (nhóm dời tới): dòng 74, bản sửa: `    if len(active) >= limit:`

```python
    67:     _log.debug(
    68:         "upload_gate: %d active uploads in last %ds (limit=%d)",
    69:         len(active),
    70:         window,
    71:         limit,
    72:     )
>>  73: 
>>  74:     if len(active) > limit:
    75:         return False, 0
    76:     return True, limit - len(active)
```

> LLM: new (high): `len(active) > limit` on line 74 should be `>=` (test `test_gate_blocks_at_exact_limit`). Original label 73 is blank.

