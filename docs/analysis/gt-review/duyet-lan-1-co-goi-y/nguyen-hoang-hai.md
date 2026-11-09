# Duyệt nhãn dòng lỗi — Nguyễn Hoàng Hải (19 ca)

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;
  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.
- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.
- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật
  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.
- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.
- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.

## 1. `bump_click`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/bump_click.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_bump_click.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 64

```python
    57:     _validate_key(key)
    58:     _validate_cap(cap)
    59: 
    60:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
    61:     counters[key] += 1
    62: 
>>  63:     if cap is not None and counters[key] > cap:
>>  64:         counters[key] = cap - 1
    65: 
    66:     _log.debug("Bumped metric %s to %d (cap=%s)", key, counters[key], cap)
    67:     return counters[key]
```

> LLM: other (high): Docstring: counter is clamped so it never exceeds cap, tests expect [1,2,3,3,3,3] for cap=3; line 64 sets counters[key] = cap - 1 instead of cap. The label (63) is the guard, which is correct; the deviating token is on 64.

## 2. `cached_preference`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/cached_preference.py#L83) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_cached_preference.py)

- G (nhãn gốc): dòng 83
- S (nhóm dời tới): dòng 85, bản sửa: `    if now >= ttl + _CLOCK_SKEW_TOLERANCE:`

```python
    77:     if item is None:
    78:         _log.debug("Cache miss for key '%s'", validated_key)
    79:         return None
    80:     payload, ttl = item
    81: 
    82:     if ttl > _MAX_TTL_SECONDS + _DEFAULT_TTL_SECONDS:
>>  83:         _log.debug("Entry '%s' has abnormally large TTL: %s", validated_key, ttl)
    84: 
>>  85:     if now > ttl + _CLOCK_SKEW_TOLERANCE:
    86:         return None
    87:     return payload
```

> LLM: new (high): Tests `test_entry_at_exact_ttl_boundary_is_expired` require `now >= ttl + skew`; the `>` on line 85 is the fault. Original label 83 is a debug log inside the unrelated abnormal-TTL block; the unused helper `_is_expired` (line 50) with the same `>` is a distractor, not executed.

## 3. `calibrate_score`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_score.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_score.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 65

```python
    59:     """
    60:     _validate_segment(x0, x1)
    61: 
    62:     t = _compute_interpolation_param(x0, x1, x)
    63:     y = y0 + t * (y1 - y0)
    64: 
>>  65:     if not clamp:
    66:         lo, hi = (min(y0, y1), max(y0, y1))
>>  67:         if y < lo:
    68:             y = lo
    69:         if y > hi:
    70:             y = hi
    71: 
    72:     _log.debug("calibrate_score: t=%.4f, y=%.6f (clamp=%s)", t, y, clamp)
    73:     return y
```

> LLM: other (high): Docstring: clamp=True restricts output to [y0, y1]; line 65 `if not clamp:` is inverted so extrapolation is clamped only when clamp=False. Label 67 (`if y < lo:`) is a correct statement inside the block, two lines below the fault.

## 4. `coverage_interp`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/coverage_interp.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_coverage_interp.py)

- G (nhãn gốc): dòng 65
- S (nhóm dời tới): dòng 66, bản sửa: `    if clamp:`

```python
    59:         ValueError: If ``x0`` and ``x1`` are effectively equal.
    60:     """
    61:     _validate_segment(x0, x1)
    62: 
    63:     t = _compute_parameter(x, x0, x1)
    64:     y = y0 + t * (y1 - y0)
>>  65: 
>>  66:     if not clamp:
    67:         lo, hi = (min(y0, y1), max(y0, y1))
    68:         if y < lo:
    69:             y = lo
    70:         if y > hi:
    71:             y = hi
    72: 
```

> LLM: new (high): `if not clamp:` on line 66 inverts the documented flag (clamp=True should restrict to [min(y0,y1), max(y0,y1)]). Original label 65 is blank.

## 5. `email_send_quota`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/email_send_quota.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_email_send_quota.py)

- G (nhãn gốc): dòng 65
- S (nhóm dời tới): dòng 66, bản sửa: `    if len(recent) >= limit:`

```python
    59:     recent = _filter_recent_timestamps(sent, cutoff)
    60: 
    61:     _log.debug(
    62:         "%s | window=%ds limit=%d recent=%d",
    63:         QUOTA_LOG_PREFIX, window, limit, len(recent),
    64:     )
>>  65: 
>>  66:     if len(recent) > limit:
    67:         return False
    68:     return True
```

> LLM: new (high): `len(recent) > limit` on line 66 allows the (limit+1)-th send; tests `test_exactly_at_limit_blocks_sending` pin `>=`. Original label 65 is blank.

## 6. `fee_splitter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/fee_splitter.py#L59) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_fee_splitter.py)

- G (nhãn gốc): dòng 62
- S (nhóm dời tới): dòng 59, bản sửa: `    base = list(map(lambda r: (r / total_ratio) * (amount - fee) + fee, ratios))`

```python
    53:     if amount < 0:
    54:         raise ValueError("negative amount")
    55: 
    56:     _log.debug("Splitting amount=%.4f among %d participants (fee=%.4f)", amount, len(ratios), fee)
    57: 
    58:     total_ratio = sum(ratios)
>>  59:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
    60: 
    61:     payouts = [_clamp_payout(b - fee) for b in base]
>>  62: 
    63:     if abs(sum(payouts) - (amount - fee * len(ratios))) < _PRECISION:
    64:         _log.debug("Payout sum verified within precision tolerance")
    65: 
    66:     return payouts
```

> LLM: new (low): Fee must be deducted once from the pool (test `test_fee_deducted_once_not_per_participant`), but line 59 splits the gross `amount` and line 61 subtracts `fee` per participant; the fault spans 59 and 61 (two-line fix verified). Original 62 is a blank line adjacent to 61, so the authors may have meant 61 rather than 59; the line-63 debug check `amount - fee * len(ratios)` matches the buggy semantics and is a distractor.

## 7. `guard_search`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/guard_search.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_guard_search.py)

- G (nhãn gốc): dòng 73
- S (nhóm dời tới): dòng 74, bản sửa: `    if len(active) >= limit:`

```python
    67:     _validate_parameters(window, limit)
    68: 
    69:     cutoff = now - window
    70:     active = _filter_active_timestamps(timestamps, cutoff)
    71: 
    72:     _log.debug("guard_search: %d active requests in window", len(active))
>>  73: 
>>  74:     if len(active) > limit:
    75:         return False, 0
    76:     return True, limit - len(active)
```

> LLM: new (high): `len(active) > limit` on line 74 should be `>=` (tests `test_exactly_at_limit_denies_new_search`; `return True, limit - len(active)` would yield `(True, 0)`). Original label 73 is blank.

## 8. `ledger_balance_rollup`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/ledger_balance_rollup.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_ledger_balance_rollup.py)

- G (nhãn gốc): dòng 65
- F (LLM đề xuất): dòng 66

```python
    59:     """
    60:     balance = 0.0
    61:     for idx, (amount, kind) in enumerate(entries):
    62:         _validate_entry(amount, kind, idx)
    63:         if kind == "credit":
    64:             balance += amount
>>  65:         elif kind == "debit":
>>  66:             balance += amount
    67:         else:
    68:             raise ValueError("unknown kind")
    69:     _log.debug("Computed ledger balance: %.2f over %d entries", balance, len(entries))
    70:     return _round_balance(balance)
```

> LLM: other (high): Label 65 `elif kind == "debit":` is a correct guard. The deviation is line 66 `balance += amount` inside the debit branch; debits must decrease the balance (`-=`) per docstring and tests.

## 9. `load_mix`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/load_mix.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_load_mix.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 68

```python
    61:     adjusted: List[float] = []
    62:     for c, t in zip(current, target):
    63:         blended = c + (t - c) * damping
    64:         adjusted.append(_clamp_allocation(blended))
    65: 
    66:     _log.debug("adjusted allocations before normalisation: %s", adjusted)
>>  67: 
>>  68:     return adjusted
```

> LLM: other (high): Label 67 is a blank line. The fault is the omitted normalisation promised by the docstring ('normalised so that all allocations sum to 1.0'); the fix most naturally changes line 68 `return adjusted` to return `[a / sum(adjusted) for a in adjusted]` (verified: all 10 tests pass).

## 10. `metric_rolling_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/metric_rolling_avg.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_metric_rolling_avg.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 71;73, bản sửa: `    avg = total / len(tail)`
- F (LLM đề xuất): dòng 70

```python
    63:     cleaned = _filter_valid(values)
    64:     if not cleaned:
    65:         raise ValueError("no values")
    66: 
    67:     tail = cleaned[-window:]
    68:     total = sum(tail)
>>  69: 
>>  70:     avg = total / window
>>  71: 
    72:     _log.debug("rolling_avg window=%d tail_len=%d avg=%s", window, len(tail), avg)
>>  73: 
    74:     if len(tail) < min_samples:
    75:         return None
    76:     return avg
```

> LLM: neither (high): Docstring: mean of the values actually in the window; line 70 divides by `window` instead of `len(tail)` (fix verified). The oracle recomputes `avg` on a blank line (71;73) after the faulty statement, a compensating insertion; original label 69 is blank.

## 11. `queue_window_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/queue_window_avg.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_queue_window_avg.py)

- G (nhãn gốc): dòng 65
- F (LLM đề xuất): dòng 66

```python
    59:         ValueError: If *window* is not positive or *values* is empty.
    60:     """
    61:     _validate_inputs(values, window)
    62: 
    63:     tail = values[-window:]
    64:     total = sum(tail)
>>  65: 
>>  66:     mean = total / window
    67: 
    68:     _log.debug("window=%d, tail_len=%d, mean=%s", window, len(tail), mean)
    69: 
    70:     if len(tail) < warmup_min:
    71:         return None
    72: 
```

> LLM: other (high): Label 65 is a blank line. Line 66 `mean = total / window` divides by the configured window instead of len(tail), so a short tail gives a too-small mean; the oracle's "fix" was an inserted correction at the blank line.

## 12. `rebate_splitter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/rebate_splitter.py#L62) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_rebate_splitter.py)

- G (nhãn gốc): dòng 63
- S (nhóm dời tới): dòng 62, bản sửa: `    base = [(r / total_ratio) * (amount - fee) + fee for r in ratios]`

```python
    56:     if amount < 0:
    57:         raise ValueError("negative amount")
    58: 
    59:     _log.debug("Splitting %.4f among %d recipients (fee=%.4f)", amount, len(ratios), fee)
    60: 
    61:     total_ratio = sum(ratios)
>>  62:     base = [(r / total_ratio) * amount for r in ratios]
>>  63: 
    64:     return [_clamp_payout(share - fee) for share in base]
```

> LLM: new (medium): Docstring: 'the fee is deducted from the total amount before distribution', but line 62 splits the gross `amount` and line 64 subtracts the full `fee` per recipient; fault spans 62 and 64 (two-line fix verified). The oracle's `+ fee` trick lands on 62, one of the two faulty lines. Original 63 is blank.

## 13. `revenue_share`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/revenue_share.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_revenue_share.py)

- G (nhãn gốc): dòng 71
- S (nhóm dời tới): dòng 70, bản sửa: `        shares.append((r / total_ratio) * (amount - fee) + fee)`

```python
    64:         raise ValueError("invalid ratios")
    65: 
    66:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    67: 
    68:     shares: List[float] = []
    69:     for r in ratios:
>>  70:         shares.append((r / total_ratio) * amount)
>>  71: 
    72:     return [_clamp_payout(s - fee) for s in shares]
```

> LLM: new (medium): Tests (`test_fee_deducted_before_split_total`) want shares of `amount - fee`; line 70 appends shares of the gross `amount` and line 72 subtracts `fee` per participant. Fault spans 70 and 72 (two-line fix verified); the oracle's `+ fee` trick is on 70. Original 71 is blank.

## 14. `schedule_car`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_car.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_car.py)

- G (nhãn gốc): dòng 62
- S (nhóm dời tới): dòng 61, bản sửa: `    if any(not (b < s or a > e) for s, e in timeline):`

```python
    55:     a, b = window
    56:     if a >= b:
    57:         raise ValueError("empty window")
    58: 
    59:     _check_timeline_capacity(timeline)
    60: 
>>  61:     if any(not (b <= s or a >= e) for s, e in timeline):
>>  62:         return False, timeline
    63: 
    64:     _log.debug("Booking accepted for window [%d, %d)", a, b)
    65:     result = sorted(timeline + [window])
    66:     return True, result
```

> LLM: new (high): Tests reject bookings that touch an existing slot's endpoint, so the condition must be `not (b < s or a > e)`; the `<=`/`>=` on line 61 is the fault. Original label 62 is the guarded `return False, timeline`, which is correct.

## 15. `shift_risk`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/shift_risk.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_shift_risk.py)

- G (nhãn gốc): dòng 62
- S (nhóm dời tới): dòng 61, bản sửa: `    adjusted = [v / sum(adjusted) for v in adjusted]`

```python
    55: 
    56:     _validate_allocation(current, "current")
    57:     _validate_allocation(target, "target")
    58: 
    59:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    60: 
>>  61:     adjusted = [_clamp(v) for v in adjusted]
>>  62: 
    63:     _log.debug("Adjusted allocation before normalization: %s", adjusted)
    64: 
    65:     return adjusted
```

> LLM: original (medium): Docstring: blend, clamp, 'then normalizes the result so that the weights sum to 1', and the log on 63 says 'before normalization'; the normalization statement is missing (omission). Inserting `adjusted = [v / sum(adjusted) for v in adjusted]` at blank line 62 (or 64) passes; the oracle's edit at 61 replaces the intended `_clamp` with normalization, a compensating change that drops clamping. Best executable alternative: line 65 (`return adjusted`).

## 16. `storage_quota_split`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/storage_quota_split.py#L64) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_storage_quota_split.py)

- G (nhãn gốc): dòng 67
- S (nhóm dời tới): dòng 64, bản sửa: `    total, fee = total - fee, 0`
- F (LLM đề xuất): dòng 66

```python
    58:         raise ValueError("negative total")
    59: 
    60:     _validate_ratios(ratios)
    61: 
    62:     if fee < -_FEE_PRECISION:
    63:         raise ValueError("fee must not be negative")
>>  64: 
    65:     total_ratio = sum(ratios)
>>  66:     shares = [(r / total_ratio) * total for r in ratios]
>>  67: 
    68:     _log.debug("Computed raw shares for %d participants", len(shares))
    69: 
    70:     floored = _apply_floor([s - fee for s in shares])
    71:     return floored
```

> LLM: neither (high): Docstring: the one-time fee is subtracted from the pool before splitting, but line 66 splits the gross `total` and line 70 subtracts `fee` per participant; fixing 66 alone still fails, 66+70 passes. The oracle's `total, fee = total - fee, 0` inserted at blank line 64 compensates; original label 67 is also blank.

## 17. `time_range_filter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/time_range_filter.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_time_range_filter.py)

- G (nhãn gốc): dòng 73
- F (LLM đề xuất): dòng 75

```python
    67:     _validate_timestamp(end, "end")
    68:     _validate_points(points)
    69: 
    70:     if start >= end:
    71:         raise ValueError("invalid range")
    72: 
>>  73:     _log.debug("Filtering %d points for window [%s, %s)", len(points), start, end)
    74: 
>>  75:     return [p for p in points if start <= p[0] <= end]
```

> LLM: other (high): Label 73 is a `_log.debug` line. Docstring: half-open interval [start, end); line 75 `start <= p[0] <= end` must be `< end`. Verified: patching only line 75 makes all 10 tests pass (original: 4 fail).

## 18. `traffic_shaping_gate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/traffic_shaping_gate.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_traffic_shaping_gate.py)

- G (nhãn gốc): dòng 70
- S (nhóm dời tới): dòng 71, bản sửa: `if len(active) >= limit:`

```python
    64:     _validate_parameters(window, limit)
    65: 
    66:     cutoff = now - window
    67:     active = _active_timestamps(timestamps, cutoff)
    68: 
    69:     _log.debug("active=%d, limit=%d, cutoff=%s", len(active), limit, cutoff)
>>  70: 
>>  71:     if len(active) > limit:
    72:         return False, 0
    73:     return True, limit - len(active)
```

> LLM: new (high): `len(active) > limit` on line 71 should be `>=` (test `test_exactly_at_limit_denies_traffic`). Original label 70 is blank.

## 19. `volume_moving_mean`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/volume_moving_mean.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_volume_moving_mean.py)

- G (nhãn gốc): dòng 61
- F (LLM đề xuất): dòng 60

```python
    54:     """
    55:     _validate_inputs(values, window, warmup_min)
    56: 
    57:     recent = _extract_recent_window(values, window)
    58:     total = sum(recent)
    59: 
>>  60:     mean = total / window
>>  61: 
    62:     _log.debug(
    63:         "volume_moving_mean: window=%d, samples=%d, mean=%s",
    64:         window,
    65:         len(recent),
    66:         round(mean, _PRECISION_DIGITS) if mean is not None else None,
    67:     )
```

> LLM: other (high): Label 61 is a blank line; the fault is line 60 `mean = total / window`, which must divide by `len(recent)` (the oracle's confirmed fix was an inserted line at the blank).

