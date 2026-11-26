# Duyệt nhãn dòng lỗi — Hoàng Trung Kiên (18 ca)

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;
  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.
- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.
- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật
  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.
- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.
- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.

## 1. `bump_job`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/bump_job.py#L56) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_bump_job.py)

- G (nhãn gốc): dòng 56
- F (LLM đề xuất): dòng 57

```python
    50:     """
    51:     _validate_cap(cap)
    52:     _ensure_key_exists(counters, key)
    53: 
    54:     counters[key] += 1
    55: 
>>  56:     if cap is not None and counters[key] > cap:
>>  57:         counters[key] = cap - 1
    58:         _log.debug(CAP_OVERFLOW_MSG, key, cap)
    59: 
    60:     return counters[key]
```

> LLM: other (high): Docstring: counter will never exceed cap and tests require it to saturate exactly at cap; line 57 writes counters[key] = cap - 1. Label 56 is the (correct) guard; the deviating token is on 57.

## 2. `calibrate_latency`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_latency.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_latency.py)

- G (nhãn gốc): dòng 73
- S (nhóm dời tới): dòng 70, bản sửa: `if clamp:`

```python
    64:     """
    65:     _validate_endpoints(x0, x1)
    66: 
    67:     t = _compute_parameter(x, x0, x1)
    68:     y = (1 - t) * y0 + t * y1
    69: 
>>  70:     if not clamp:
    71:         low, high = sorted([y0, y1])
    72:         y = min(max(y, low), high)
>>  73: 
    74:     _log.debug("calibrate_latency: t=%.4f, y=%.4f ms", t, y * LATENCY_UNIT_MS)
    75: 
    76:     return min(y, MAX_LATENCY_MS)
```

> LLM: new (high): Docstring: `clamp=True` restricts the result to [y0, y1]; line 70 `if not clamp:` inverts the flag so clamping happens only when disabled. Original label 73 is a blank line.

## 3. `catalog_cache`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/catalog_cache.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_catalog_cache.py)

- G (nhãn gốc): dòng 63
- S (nhóm dời tới): dòng 64, bản sửa: `    if now >= adjusted_expiry:`

```python
    57:     if key not in entries:
    58:         return None
    59: 
    60:     value, expires_at = entries[key]
    61: 
    62:     adjusted_expiry = expires_at + _CLOCK_SKEW_TOLERANCE
>>  63: 
>>  64:     if now > adjusted_expiry:
    65:         return None
    66: 
    67:     return value
```

> LLM: new (high): Docstring: entry returned 'only when the current time has not yet reached the expiration time'; `>` on line 64 lets now == expiry through (should be `>=`). Original label 63 is blank.

## 4. `demand_forecast_curve`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/demand_forecast_curve.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_demand_forecast_curve.py)

- G (nhãn gốc): dòng 65
- S (nhóm dời tới): dòng 66, bản sửa: `    if clamp:`

```python
    59:     _validate_anchor_points(x0, x1)
    60: 
    61:     ratio = (x - x0) / (x1 - x0)
    62:     y = y0 + ratio * (y1 - y0)
    63: 
    64:     _log.debug("Interpolation ratio=%.4f, raw forecast=%.4f", ratio, y)
>>  65: 
>>  66:     if not clamp:
    67:         low, high = _compute_bounds(y0, y1)
    68:         if y < low:
    69:             y = low
    70:         elif y > high:
    71:             y = high
    72:     return y
```

> LLM: new (high): `if not clamp:` on line 66 inverts the documented clamp flag; tests with clamp=True expect bounded output. Original label 65 is blank.

## 5. `estimate_supply`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/estimate_supply.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_estimate_supply.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 66

```python
    60:     """
    61:     _validate_segment(x0, x1)
    62: 
    63:     t = _compute_interpolation_ratio(x0, x1, x)
    64:     y = y0 + t * (y1 - y0)
    65: 
>>  66:     if not clamp:
>>  67:         lo, hi = (min(y0, y1), max(y0, y1))
    68:         if y < lo:
    69:             y = lo
    70:         if y > hi:
    71:             y = hi
    72: 
    73:     _log.debug("estimate_supply: x=%.4f, t=%.4f, y=%.4f", x, t, y)
```

> LLM: other (high): Line 66 `if not clamp:` is the inverted guard; label line 67 `lo, hi = (min(y0, y1), max(y0, y1))` is correct code inside the inverted block.

## 6. `fuel_moving_mean`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/fuel_moving_mean.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_fuel_moving_mean.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 65

```python
    57:     Raises:
    58:         ValueError: If *window* is not positive or *values* is empty.
    59:     """
    60:     _validate_inputs(values, window)
    61: 
    62:     recent = values[-window:]
>>  63:     total = sum(recent)
    64: 
>>  65:     mean = total / window
    66: 
    67:     if len(recent) < warmup_min:
    68:         _log.debug("Warm-up not met: %d < %d samples", len(recent), warmup_min)
    69:         return None
    70: 
    71:     return _round_mean(mean)
```

> LLM: other (high): Label 63 `total = sum(recent)` is correct. The deviation is line 65 `mean = total / window`: with fewer samples than the window the docstring/tests require the mean over the available readings, i.e. `total / len(recent)`.

## 7. `invoice_merge_stream`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/invoice_merge_stream.py#L79) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_invoice_merge_stream.py)

- G (nhãn gốc): dòng 82
- S (nhóm dời tới): dòng 79;83, bản sửa: `    return merged`

```python
    73:             merged.append(right[j])
    74:             i += 1
    75:             j += 1
    76: 
    77:     merged.extend(left[i:])
    78:     merged.extend(right[j:])
>>  79: 
    80:     if len(merged) > MERGE_LOG_THRESHOLD:
    81:         _log.debug("Merged stream contains %d entries", len(merged))
>>  82: 
>>  83:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    84:         merged.pop()
    85:     return merged
```

> LLM: new (medium): Docstring: duplicates present in both streams are preserved; the `if ... merged[-1] == left[-1] == right[-1]: merged.pop()` block on lines 83-84 is the injected spurious de-duplication (deleting it passes all tests). The oracle's `return merged` early exit (region 79;83) merely bypasses the block; the single label should be 83. Original 82 is blank.

## 8. `limit_job`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_job.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_job.py)

- G (nhãn gốc): dòng 73
- S (nhóm dời tới): dòng 75, bản sửa: `    if len(recent) >= limit:`

```python
    67:     _validate_parameters(window, limit)
    68: 
    69:     cutoff = now - window
    70:     recent = _filter_recent_timestamps(timestamps, cutoff)
    71: 
    72:     _log.debug("Throttle check: %d recent jobs in %ds window (limit %d)",
>>  73:                len(recent), window, limit)
    74: 
>>  75:     if len(recent) > limit:
    76:         return False, 0
    77:     return True, limit - len(recent)
```

> LLM: new (high): `len(recent) > limit` on line 75 should be `>=` (test `test_at_limit_exactly_should_block`). Original label 73 is the continuation line of the preceding debug-log call.

## 9. `login_throttle`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/login_throttle.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_login_throttle.py)

- G (nhãn gốc): dòng 68
- S (nhóm dời tới): dòng 69, bản sửa: `if len(recent) >= limit:`

```python
    62:     recent = _filter_recent(timestamps, cutoff)
    63: 
    64:     _log.debug(
    65:         "login_throttle: %d recent attempts in last %ds (limit %d)",
    66:         len(recent), window, limit,
    67:     )
>>  68: 
>>  69:     if len(recent) > limit:
    70:         return False, 0
    71:     return True, limit - len(recent)
```

> LLM: new (high): `len(recent) > limit` on line 69 should be `>=` (test `test_exactly_at_limit_denies_login`). Original label 68 is blank.

## 10. `payment_payout`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/payment_payout.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_payment_payout.py)

- G (nhãn gốc): dòng 72
- F (LLM đề xuất): dòng 73

```python
    66:         raise ValueError("invalid ratios")
    67: 
    68:     shares: List[float] = []
    69:     for r in ratios:
    70:         raw = (r / total_ratio) * amount
    71:         shares.append(max(_MIN_PAYOUT, _round_currency(raw)))
>>  72: 
>>  73:     return [s - fee for s in shares]
```

> LLM: other (medium): Label 72 is a blank line. Docstring/tests: fee is deducted from the pool before splitting, but line 70 multiplies by `amount` (not `amount - fee`) and line 73 subtracts the full fee from every share; the deviating statement is line 73 (two-line fault 70+73).

## 11. `quota_for_inventory`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/quota_for_inventory.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_quota_for_inventory.py)

- G (nhãn gốc): dòng 65
- F (LLM đề xuất): dòng 66

```python
    59:             or every weight is zero.
    60:     """
    61:     _validate_inputs(total, weights, minimum)
    62: 
    63:     planned = _compute_planned_amounts(total, weights, minimum)
    64:     _log.debug("Planned allocations (float): %s", planned)
>>  65: 
>>  66:     allocations = [int(x) for x in planned]
    67:     return allocations
```

> LLM: other (medium): Label 65 is a blank line. Tests require integer allocations to sum to total; line 66 `allocations = [int(x) for x in planned]` truncates without remainder redistribution.

## 12. `reservation_overlap_check`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/reservation_overlap_check.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_reservation_overlap_check.py)

- G (nhãn gốc): dòng 68
- F (LLM đề xuất): dòng 69

```python
    62:         ValueError: If the candidate interval is degenerate (start >= end).
    63:     """
    64:     c_start, c_end = candidate
    65:     _validate_interval(c_start, c_end, label="candidate reservation")
    66:     _check_scan_limit(reservations)
    67: 
>>  68:     for start, end in reservations:
>>  69:         if not (c_end <= start or c_start >= end):
    70:             return True
    71:     return False
```

> LLM: other (high): Label 68 is the `for` header. Docstring: closed-interval model, sharing an endpoint counts as overlap; the comparison on line 69 `not (c_end <= start or c_start >= end)` must use `<`/`>`. Verified: patching only line 69 makes all 10 tests pass (original: 3 fail).

## 13. `rolling_usage`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/rolling_usage.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_rolling_usage.py)

- G (nhãn gốc): dòng 66
- S (nhóm dời tới): dòng 68;70, bản sửa: `    avg = total / len(tail)`
- F (LLM đề xuất): dòng 67

```python
    60:         ValueError: If *window* is non-positive or *series* is empty.
    61:     """
    62:     _validate_inputs(series, window)
    63: 
    64:     tail: Sequence[float] = series[-window:]
    65:     total: float = sum(tail)
>>  66: 
>>  67:     avg = total / window
>>  68: 
    69:     _log.debug("tail=%d total=%.4f avg=%.4f", len(tail), total, avg)
>>  70: 
    71:     if len(tail) < max(warmup_min, _WARMUP_SAMPLES):
    72:         return None
    73:     return _round_metric(avg)
```

> LLM: neither (high): Line 67 `avg = total / window` should divide by `len(tail)` (docstring: mean of the extracted tail; fix verified). The oracle recomputes `avg` on blank line 68/70 after the fault, a compensating insertion; original label 66 is blank.

## 14. `schedule_shift_allocator`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_shift_allocator.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_shift_allocator.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 68

```python
    61:     _validate_inputs(total, weights, minimum)
    62: 
    63:     weight_sum = sum(weights)
    64:     shares = _compute_raw_shares(total, weights, weight_sum, minimum)
    65: 
    66:     _log.debug("Raw shares computed for %d workers, total=%d", len(weights), total)
>>  67: 
>>  68:     return [int(x) for x in shares]
```

> LLM: other (medium): Label 67 is a blank line. Docstring: whole-number allocations summing as close to total as possible; line 68 `[int(x) for x in shares]` truncates and drops the remainder (multi-line largest-remainder fix).

## 15. `shift_weight`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/shift_weight.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_shift_weight.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 64

```python
    57:     """
    58:     _validate_inputs(current, target, damping)
    59: 
    60:     updated = _compute_shifted_values(current, target, damping)
    61: 
    62:     _log.debug("Raw shifted weights (pre-norm): %s", updated)
>>  63: 
>>  64:     return updated
```

> LLM: other (medium): Label 63 is a blank line (likely the removed normalisation statement). Docstring: renormalised to sum to exactly 1.0; line 64 `return updated` returns the raw blend.

## 16. `task_tally`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/task_tally.py#L53) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_task_tally.py)

- G (nhãn gốc): dòng 53
- F (LLM đề xuất): dòng 55

```python
    47:         ValueError: If *max_value* is provided but less than 1.
    48:     """
    49:     _validate_max_value(max_value)
    50: 
    51:     new_value = _current_count(counts, key) + INCREMENT_STEP
    52: 
>>  53:     if max_value is not None:
    54:         if new_value > max_value:
>>  55:             new_value = max_value - 1
    56: 
    57:     counts[key] = new_value
    58:     _log.debug("task_tally: key=%s  new_value=%d", key, new_value)
    59:     return new_value
```

> LLM: other (high): Label 53 `if max_value is not None:` is a correct outer guard; the deviating token is on line 55 `new_value = max_value - 1` (docstring: counter never exceeds the ceiling, i.e. clamp to max_value). Verified: changing only line 55 to `max_value` makes all 10 tests pass (original: 2 fail).

## 17. `track_build`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/track_build.py#L52) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_track_build.py)

- G (nhãn gốc): dòng 52
- F (LLM đề xuất): dòng 53

```python
    46:     """
    47:     _validate_key(key)
    48: 
    49:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
    50:     counters[key] += 1
    51: 
>>  52:     if cap is not None and counters[key] > cap:
>>  53:         counters[key] = cap - 1
    54:         _log.debug("%s: %s counter clamped at %d", CAP_ENFORCEMENT_LABEL, key, cap)
    55: 
    56:     if _should_log_milestone(counters[key]):
    57:         _log.debug("Metric '%s' reached milestone %d", key, counters[key])
    58: 
    59:     return counters[key]
```

> LLM: other (high): Label 52 is the correct guard `if cap is not None and counters[key] > cap:`; the fault is line 53 `counters[key] = cap - 1` (should clamp to cap). Verified: changing only line 53 to `cap` makes all 9 tests pass (original: 3 fail).

## 18. `txn_dedup_merge`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/txn_dedup_merge.py#L75) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_txn_dedup_merge.py)

- G (nhãn gốc): dòng 75
- F (LLM đề xuất): dòng 76

```python
    69:             merged.append(left[i])
    70:             merged.append(right[j])
    71:             i += 1
    72:             j += 1
    73:     merged.extend(left[i:])
    74:     merged.extend(right[j:])
>>  75: 
>>  76:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    77:         merged.pop()
    78:     return merged
```

> LLM: other (high): Label 75 is a blank line. Docstring: merge preserves all elements; the spurious block on lines 76-77 pops the last element when both lists end with the same id (the oracle's confirmed fix was an early `return merged` inserted at the blank).

