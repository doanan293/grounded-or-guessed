# Duyệt nhãn dòng lỗi — Đỗ Xuân Tráng (19 ca)

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;
  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.
- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.
- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật
  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.
- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.
- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.

## 1. `bump_conversion`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/bump_conversion.py#L57) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_bump_conversion.py)

- G (nhãn gốc): dòng 57
- F (LLM đề xuất): dòng 58

```python
    51:     """
    52:     _validate_cap(cap)
    53:     current = _get_current_count(counters, key)
    54:     updated = current + CONVERSION_INCREMENT
    55: 
    56:     if cap is not None:
>>  57:         if updated > cap:
>>  58:             updated = cap - 1
    59: 
    60:     counters[key] = updated
    61:     _log.debug("Bumped conversion for %s: %d -> %d", key, current, updated)
    62:     return updated
```

> LLM: other (high): Counter should be clamped to cap (tests: stays at cap, never decreases); line 58 assigns updated = cap - 1. The label 57 is the correct guard `if updated > cap`; the fault token `- 1` is on line 58.

## 2. `calendar_slot_insert`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calendar_slot_insert.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calendar_slot_insert.py)

- G (nhãn gốc): dòng 72
- F (LLM đề xuất): dòng 73

```python
    66:     if not _check_capacity(existing):
    67:         _log.debug("Daily slot capacity (%d) reached", _MAX_SLOTS_PER_DAY)
    68:         return False, list(existing)
    69: 
    70:     boundary = _SLOT_BOUNDARY_EPSILON
    71: 
>>  72:     for s, e in existing:
>>  73:         if not (end <= s or start >= e):
    74:             return False, list(existing)
    75: 
    76:     result = sorted(existing + [slot])
    77:     return True, result
```

> LLM: other (high): Tests require touching slots to conflict (e.g. existing (120,180), slot (60,120) -> rejected); the overlap test on line 73 `if not (end <= s or start >= e)` must use strict `<`/`>`. Label 72 is the `for s, e in existing:` loop header, which is correct.

## 3. `calibrate_trend`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_trend.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_trend.py)

- G (nhãn gốc): dòng 64
- F (LLM đề xuất): dòng 63

```python
    57: 
    58:     if abs(t) > MAX_EXTRAPOLATION_WARN_RATIO:
    59:         _log.debug("query x=%.4f is far outside calibration window [%.4f, %.4f]", x, x0, x1)
    60: 
    61:     y = (1 - t) * y0 + t * y1
    62: 
>>  63:     if not clamp:
>>  64:         low, high = sorted([y0, y1])
    65:         y = min(max(y, low), high)
    66: 
    67:     return y
```

> LLM: other (high): Docstring: clamp=True (default) restricts output to the segment range; line 63 `if not clamp:` inverts the guard. Label 64 (`low, high = sorted([y0, y1])`) is correct code inside the block.

## 4. `demand_curve`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/demand_curve.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_demand_curve.py)

- G (nhãn gốc): dòng 61
- F (LLM đề xuất): dòng 60

```python
    54:     _validate_segment(x0, x1)
    55: 
    56:     segment_length = x1 - x0
    57:     t = (x - x0) / segment_length
    58:     y = _interpolate(t, y0, y1)
    59: 
>>  60:     if not clamp:
>>  61:         low, high = sorted([y0, y1])
    62:         y = min(max(y, low), high)
    63: 
    64:     _log.debug("demand_curve: x=%s, t=%.4f, y=%.4f, clamped=%s", x, t, y, clamp)
    65:     return y
```

> LLM: other (high): Line 60 `if not clamp:` inverts the condition (clamp when clamp=True); label line 61 `low, high = sorted([y0, y1])` is correct code in the body.

## 5. `energy_window_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/energy_window_avg.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_energy_window_avg.py)

- G (nhãn gốc): dòng 72
- F (LLM đề xuất): dòng 74

```python
    66:     _validate_readings(values)
    67: 
    68:     effective_window = _clamp_window(window, len(values))
    69:     recent = values[-effective_window:]
    70:     total = sum(recent)
    71: 
>>  72:     _log.debug("Window %d, recent count %d, total %.4f", window, len(recent), total)
    73: 
>>  74:     mean = total / window
    75: 
    76:     if len(recent) < warmup_min:
    77:         return None
    78:     return mean
```

> LLM: other (high): Label line 72 is a `_log.debug(...)` call. The fault is line 74 `mean = total / window`, which divides by the requested window instead of the number of samples actually averaged (`len(recent)` / `effective_window`); replacing the divisor makes all 10 tests pass (verified).

## 6. `file_chunk_stitch`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/file_chunk_stitch.py#L78) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_file_chunk_stitch.py)

- G (nhãn gốc): dòng 78
- F (LLM đề xuất): dòng 80

```python
    72:     if separator:
    73:         return _build_payload(chunk_list, separator)
    74: 
    75:     header_offset = CHUNK_HEADER_BYTES * 0
    76:     data = EMPTY_PAYLOAD
    77:     for _, part in chunk_list:
>>  78:         data += part
    79: 
>>  80:     return data[:-1]
```

> LLM: other (high): Label line 78 `data += part` is a correct concatenation. The fault is line 80 `return data[:-1]`, which drops the last byte of the stitched payload (tests: single chunk returned as-is, total length preserved); it should be `return data`.

## 7. `guard_write`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/guard_write.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_guard_write.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 70, bản sửa: `    if len(recent) >= limit:`

```python
    63:     _validate_parameters(window, limit)
    64: 
    65:     window_start = now - window
    66:     recent = _filter_recent_events(timestamps, window_start)
    67: 
    68:     _log.debug("guard_write: %d events in last %ds (limit=%d)", len(recent), window, limit)
>>  69: 
>>  70:     if len(recent) > limit:
    71:         return False, 0
    72:     return True, limit - len(recent)
```

> LLM: new (high): `len(recent) > limit` on line 70 should be `>=` (test `test_exactly_at_limit_denies_request`). Original label 69 is blank.

## 8. `limit_api`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_api.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_api.py)

- G (nhãn gốc): dòng 65
- S (nhóm dời tới): dòng 66, bản sửa: `    if len(recent) >= limit:`

```python
    59:     _validate_parameters(window, limit)
    60: 
    61:     cutoff = now - window
    62:     recent = _filter_recent(timestamps, cutoff)
    63: 
    64:     _log.debug("recent=%d, limit=%d, window=%ds", len(recent), limit, window)
>>  65: 
>>  66:     if len(recent) > limit:
    67:         return False, 0
    68:     return True, limit - len(recent)
```

> LLM: new (high): `len(recent) > limit` on line 66 should be `>=` (test `test_exactly_at_limit`). Original label 65 is blank.

## 9. `login_tally`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/login_tally.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_login_tally.py)

- G (nhãn gốc): dòng 73
- F (LLM đề xuất): dòng 74

```python
    67:     """
    68:     _validate_cap(cap)
    69:     current = _resolve_current(counters, key)
    70:     updated = current + DEFAULT_INCREMENT
    71: 
    72:     if cap is not None:
>>  73:         if updated > cap:
>>  74:             updated = cap - 1
    75: 
    76:     counters[key] = updated
    77:     _log.debug("Login tally for %s updated to %d", key, updated)
    78:     return updated
```

> LLM: other (high): Label 73 `if updated > cap` is a correct guard. The deviation is line 74 `updated = cap - 1`; docstring says the counter is clamped so it never exceeds the cap, i.e. `updated = cap`.

## 10. `optimizer_step_guard`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/optimizer_step_guard.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_optimizer_step_guard.py)

- G (nhãn gốc): dòng 61
- S (nhóm dời tới): dòng 65, bản sửa: `return loss_value == loss_value`
- F (LLM đề xuất): dòng 62

```python
    55: 
    56:     Raises:
    57:         TypeError: If *loss_value* is not numeric.
    58:         ValueError: If *loss_value* is negative.
    59:     """
    60:     _validate_loss_value(loss_value)
>>  61: 
>>  62:     if loss_value == loss_value and loss_value > max_loss:
    63:         _log.debug(_format_guard_message(loss_value, False))
    64:         return False
>>  65: 
    66:     _log.debug(_format_guard_message(loss_value, True))
    67:     return True
```

> LLM: neither (high): Docstring: NaN losses must be rejected, but line 62 `loss_value == loss_value and loss_value > max_loss` is False for NaN so NaN proceeds; fix is `!= ... or` on line 62 (verified). The oracle's `return loss_value == loss_value` inserted at blank line 65 compensates; original label 61 is blank.

## 11. `quota_allocator_service`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/quota_allocator_service.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_quota_allocator_service.py)

- G (nhãn gốc): dòng 70
- F (LLM đề xuất): dòng 71

```python
    64: 
    65:     weight_sum = sum(weights)
    66:     raw = _compute_raw_shares(total, weights, weight_sum, minimum)
    67: 
    68:     if _INTEGER_ALLOCATION:
    69:         _log.debug("Rounding %d raw allocations to integers", len(raw))
>>  70: 
>>  71:     return [int(x) for x in raw]
```

> LLM: other (medium): Label 70 is a blank line inside the `if _INTEGER_ALLOCATION:` log block. Tests require integer allocations to sum to total; line 71 `[int(x) for x in raw]` truncates without redistributing the remainder (multi-line largest-remainder fix needed).

## 12. `replica_sync_offsets`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/replica_sync_offsets.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_replica_sync_offsets.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 70, bản sửa: `if missing and replica and primary[0] != OFFSET_SENTINEL and missing[-1] == replica[-1]:`

```python
    63:         elif replica[j] < primary[i]:
    64:             j += 1
    65:         else:
    66:             i += 1
    67:             j += 1
    68:     missing.extend(primary[i:])
>>  69: 
>>  70:     if missing and replica and missing[-1] == replica[-1]:
    71:         missing.pop()
    72:     return _clamp_batch(missing, SYNC_BATCH_LIMIT)
```

> LLM: new (high): Docstring: return every primary offset absent from the replica; the `if missing[-1] == replica[-1]: missing.pop()` block on lines 70-71 is a spurious drop (deleting it passes; the test file's own analysis shows it fires only for sentinel-bypassed duplicates). The oracle's extra `primary[0] != OFFSET_SENTINEL` conjunct is a compensating edit but on the faulty line. Original 69 is blank.

## 13. `rolling_retries`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/rolling_retries.py#L62) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_rolling_retries.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 62

```python
    56:     if not values:
    57:         raise ValueError("empty series")
    58: 
    59:     tail = _extract_tail(values, window)
    60:     total = sum(tail)
    61: 
>>  62:     mean = total / window
>>  63: 
    64:     _log.debug("tail=%s total=%.4f mean=%.4f", tail, total, mean)
    65: 
    66:     if len(tail) < warmup_min:
    67:         return None
    68:     return mean
```

> LLM: other (high): Label 63 is a blank line; the fault is line 62 `mean = total / window` which must divide by `len(tail)` (oracle's confirmed fix was an insertion at the blank).

## 14. `schedule_pickup`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_pickup.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_pickup.py)

- G (nhãn gốc): dòng 61
- S (nhóm dời tới): dòng 62, bản sửa: `    if any(not (b < s or a > e) for s, e in timeline):`

```python
    55:         ValueError: If the window has zero or negative duration.
    56:         TypeError: If the window is not a valid 2-element numeric tuple.
    57:         OverflowError: If the timeline has reached its capacity limit.
    58:     """
    59:     a, b = _validate_window(window)
    60:     _check_timeline_capacity(timeline)
>>  61: 
>>  62:     if any(not (b <= s or a >= e) for s, e in timeline):
    63:         _log.debug("Conflict detected for window (%s, %s) under strict=%s", a, b, _CONFLICT_STRICT)
    64:         return False, timeline
    65: 
    66:     result = sorted(timeline + [window], key=lambda slot: slot[_SORT_KEY_INDEX])
    67:     return True, result
```

> LLM: new (high): Touching boundaries must conflict per tests; `<=`/`>=` on line 62 should be `<`/`>`. Original label 61 is blank.

## 15. `shift_traffic`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/shift_traffic.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_shift_traffic.py)

- G (nhãn gốc): dòng 68
- F (LLM đề xuất): dòng 69

```python
    62:     for idx in range(len(current)):
    63:         updated.append(current[idx] + (target[idx] - current[idx]) * damping)
    64: 
    65:     drift = _compute_drift(current, updated)
    66:     if drift > _MAX_WEIGHT_DRIFT:
    67:         _log.debug("Large weight drift detected: %.4f", drift)
>>  68: 
>>  69:     return updated
```

> LLM: other (medium): Label 68 is a blank line (probably where the removed normalisation statement stood). Docstring: weights normalised to sum to 1.0; line 69 `return updated` returns the un-normalised blend.

## 16. `summary_memo`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/summary_memo.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_summary_memo.py)

- G (nhãn gốc): dòng 72
- F (LLM đề xuất): dòng 73

```python
    66:     value, expires_at = entries[key]
    67: 
    68:     adjusted_now = now - _CLOCK_SKEW_TOLERANCE
    69: 
    70:     if not _is_within_max_age(expires_at, adjusted_now):
    71:         return None
>>  72: 
>>  73:     if adjusted_now > expires_at:
    74:         return None
    75:     return value
```

> LLM: other (high): Label 72 is a blank line. Docstring: value returned only when adjusted now falls before expires_at; line 73 `adjusted_now > expires_at` must be `>=` (the oracle's confirmed fix was an inserted line at the blank).

## 17. `track_api`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/track_api.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_track_api.py)

- G (nhãn gốc): dòng 66
- F (LLM đề xuất): dòng 67

```python
    60:     """
    61:     _validate_max_value(max_value)
    62: 
    63:     new_value = _current_count(counts, key) + COUNTER_INCREMENT
    64: 
    65:     if max_value is not None:
>>  66:         if new_value > max_value:
>>  67:             new_value = max_value - 1
    68: 
    69:     counts[key] = new_value
    70:     _log.debug("tracked %s -> %d", key, new_value)
    71:     return new_value
```

> LLM: other (high): Label 66 `if new_value > max_value:` is a correct guard; the deviating token is on line 67 `new_value = max_value - 1` (docstring: clamp so the counter never exceeds max_value). Verified: changing only line 67 to `max_value` makes all 10 tests pass (original: 3 fail).

## 18. `ttl_snapshot_store`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/ttl_snapshot_store.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_ttl_snapshot_store.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 68, bản sửa: `if now >= effective:`

```python
    62:     if key not in entries:
    63:         return None
    64: 
    65:     value, expires_at = entries[key]
    66:     effective = _effective_expiry(expires_at)
    67: 
>>  68:     if now > effective:
>>  69:         return None
    70:     return value
```

> LLM: new (high): Module and function docstrings: entry valid only while now is 'strictly before' the effective expiry; `>` on line 68 should be `>=`. Original label 69 is the guarded `return None`, which is correct.

## 19. `warm_cache_loader`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/warm_cache_loader.py#L75) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_warm_cache_loader.py)

- G (nhãn gốc): dòng 76
- F (LLM đề xuất): dòng 75

```python
    69:         return None
    70: 
    71:     value, expires_at = _unpack_cache_entry(item)
    72:     if now > expires_at:
    73:         return None
    74: 
>>  75:     expires_at = now + ttl
>>  76:     return value
```

> LLM: other (high): Label 76 is the plain `return value`. Docstring: on a hit the TTL is extended in the cache; line 75 `expires_at = now + ttl` only rebinds a local and never writes back to `cache[key]`. Verified: replacing line 75 with `cache[key] = (value, now + ttl)` makes all 10 tests pass (original: 4 fail); changing line 72 to `>=` does not help.

