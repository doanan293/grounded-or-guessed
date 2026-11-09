# Duyệt nhãn dòng lỗi — Nguyễn Đức Tùng (18 ca)

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;
  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.
- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.
- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật
  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.
- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.
- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.

## 1. `cached_inventory`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/cached_inventory.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_cached_inventory.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 70, bản sửa: `if now >= adjusted_deadline:`

```python
    63:     if record is _MISSING_SENTINEL:
    64:         _log.debug("Cache miss for key=%s", key)
    65:         return default
    66: 
    67:     value, deadline = record
    68:     adjusted_deadline = _adjust_deadline(deadline, _CLOCK_SKEW_TOLERANCE)
>>  69: 
>>  70:     if now > adjusted_deadline:
    71:         return default
    72:     return value
```

> LLM: new (high): Docstring: value is returned unless now 'has reached or passed' the adjusted deadline, and tests expect expiry at now == deadline; the deviating token is `>` (should be `>=`) on line 70. Original label 69 is a blank line.

## 2. `calibrate_loss`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_loss.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_loss.py)

- G (nhãn gốc): dòng 66
- F (LLM đề xuất): dòng 65

```python
    59:     """
    60:     _validate_segment(x0, x1)
    61: 
    62:     t = _compute_parameter(x, x0, x1)
    63:     y = y0 + t * (y1 - y0)
    64: 
>>  65:     if not clamp:
>>  66:         lo, hi = (min(y0, y1), max(y0, y1))
    67:         if y < lo:
    68:             y = lo
    69:         if y > hi:
    70:             y = hi
    71: 
    72:     _log.debug("calibrate_loss: t=%.4f, y=%.6f, clamp=%s", t, y, clamp)
```

> LLM: other (high): Clamping must apply when clamp=True (tests: beyond x1 with clamp=True returns y1); line 65 `if not clamp:` is inverted. Label 66 (`lo, hi = (min(y0, y1), max(y0, y1))`) is correct code inside the block.

## 3. `config_expiry`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/config_expiry.py#L77) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_config_expiry.py)

- G (nhãn gốc): dòng 78
- S (nhóm dời tới): dòng 77, bản sửa: `if now >= adjusted_expiry:`

```python
    71: 
    72:     adjusted_expiry = expires_at + _CLOCK_SKEW_TOLERANCE
    73: 
    74:     if _is_beyond_max_age(adjusted_expiry, now):
    75:         _log.debug("Entry key=%s has TTL exceeding max age; serving anyway", key)
    76: 
>>  77:     if now > adjusted_expiry:
>>  78:         return None
    79:     return value
```

> LLM: new (high): Same boundary fault: `now > adjusted_expiry` on line 77 should be `>=` (docstring 'has not yet reached'). Original label 78 is the guarded `return None`, which is correct; only the guard's operator deviates (a lenient guard/body convention would call this `either`).

## 4. `download_rate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/download_rate.py#L74) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_download_rate.py)

- G (nhãn gốc): dòng 74
- S (nhóm dời tới): dòng 75, bản sửa: `    if len(active) >= limit:`

```python
    68:     _validate_inputs(timestamps, now, window)
    69: 
    70:     cutoff = now - window
    71:     active = _active_timestamps(timestamps, cutoff)
    72: 
    73:     _log.debug("active=%d, limit=%d, window=%d", len(active), limit, window)
>>  74: 
>>  75:     if len(active) > limit:
    76:         return False, 0
    77:     return True, limit - len(active)
```

> LLM: new (high): Filter is inclusive (`t >= cutoff`) and tests `test_exactly_at_limit_blocks_download` require denial at len == limit; `>` on line 75 should be `>=` (otherwise it returns `(True, 0)`). Original label 74 is blank.

## 5. `feature_cache`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/feature_cache.py#L30) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_feature_cache.py)

- G (nhãn gốc): dòng 31
- F (LLM đề xuất): dòng 30

```python
    24: 
    25:     The comparison accounts for the module-level clock-skew tolerance so that
    26:     entries sitting right at the boundary of their TTL window are handled
    27:     consistently across nodes with slightly desynchronised clocks.
    28:     """
    29:     effective_now = now - _CLOCK_SKEW_TOLERANCE
>>  30:     if effective_now > ttl:
>>  31:         return True
    32:     return False
    33: 
    34: 
    35: def feature_cache(
    36:     cache: CacheStore,
    37:     key: str,
```

> LLM: other (high): Tests/docstring: entry is stale when now equals the ttl timestamp, so `_is_expired` line 30 `if effective_now > ttl:` should be `>=`. Label line 31 is the `return True` guarded by that condition (one line off); changing line 30 to `>=` makes all 10 tests pass (verified).

## 6. `gpu_memory_pool`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/gpu_memory_pool.py#L74) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_gpu_memory_pool.py)

- G (nhãn gốc): dòng 74
- S (nhóm dời tới): dòng 75, bản sửa: `if used + request >= effective_cap:`

```python
    68:     validated = _validate_allocations(allocations, ALIGNMENT_BYTES)
    69:     effective_cap = _effective_capacity(capacity, RESERVED_OVERHEAD_FRACTION)
    70: 
    71:     used = sum(validated)
    72: 
    73:     _log.debug("%s: used=%d request=%d cap=%d", DEFAULT_LOG_PREFIX, used, request, effective_cap)
>>  74: 
>>  75:     if used + request > effective_cap:
    76:         return False
    77:     return True
```

> LLM: new (high): Tests (`test_request_exactly_fills_remaining_capacity`, `test_used_equals_capacity_zero_request`) deny a request that exactly reaches the cap, so `>` on line 75 must be `>=`; the alignment and overhead helpers are correct for the tests. Original label 74 is blank.

## 7. `kv_snapshot_reader`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/kv_snapshot_reader.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_kv_snapshot_reader.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 70;71, bản sửa: `        if k > key:`

```python
    63:     effective_default = _resolve_default(default)
    64: 
    65:     _log.debug("Looking up key=%r in snapshot of length %d", key, len(snapshot))
    66: 
    67:     for k, v in snapshot:
    68:         if k == key:
>>  69:             return v
>>  70:         if k < key:
>>  71:             break
    72:     return effective_default
```

> LLM: new (high): Docstring: stop once a key *past* the target is seen; line 70 `if k < key: break` aborts on keys *before* the target (fix `k > key` verified). Original label 69 (`return v`) is the correct match branch.

## 8. `limit_ping`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_ping.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_ping.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 70, bản sửa: `    if len(recent) >= limit:`

```python
    63:     _validate_inputs(timestamps, now)
    64: 
    65:     window_start = now - window
    66:     recent = _filter_recent(timestamps, window_start)
    67: 
    68:     _log.debug("Window [%s, %s]: %d recent pings (limit=%d)", window_start, now, len(recent), limit)
>>  69: 
>>  70:     if len(recent) > limit:
    71:         return False, 0
    72:     return True, limit - len(recent)
```

> LLM: new (high): `len(recent) > limit` on line 70 should be `>=` (test `test_exactly_at_limit_denies_new_ping`). Original label 69 is blank.

## 9. `maintenance_booking`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/maintenance_booking.py#L76) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_maintenance_booking.py)

- G (nhãn gốc): dòng 76
- S (nhóm dời tới): dòng 77, bản sửa: `    if any(not (b < s or a > e) for s, e in timeline):`

```python
    70:     """
    71:     a, b = _validate_window(window)
    72:     _check_timeline_capacity(timeline)
    73: 
    74:     _log.debug("Attempting to book window (%s, %s) into timeline with %d entries [v%s]",
    75:                a, b, len(timeline), _BOOKING_VERSION)
>>  76: 
>>  77:     if any(not (b <= s or a >= e) for s, e in timeline):
    78:         return False, timeline
    79: 
    80:     result = sorted(timeline + [window])
    81:     return True, result
```

> LLM: new (high): Tests treat windows that touch at an endpoint as conflicts, so the overlap test must be `not (b < s or a > e)`; the `<=`/`>=` on line 77 (half-open semantics) is the fault. Original label 76 is blank.

## 10. `price_cache`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/price_cache.py#L59) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_price_cache.py)

- G (nhãn gốc): dòng 59
- F (LLM đề xuất): dòng 61

```python
    53: 
    54:     payload, ttl = item
    55: 
    56:     if not _is_within_max_ttl(ttl, now):
    57:         return None
    58: 
>>  59:     adjusted_now = now - _CLOCK_SKEW_TOLERANCE
    60: 
>>  61:     if adjusted_now > ttl:
    62:         return None
    63:     return payload
```

> LLM: other (high): Label 59 (`adjusted_now = now - _CLOCK_SKEW_TOLERANCE`) is a correct skew adjustment; the docstring says the entry is valid only while now is strictly before the TTL, but line 61 `if adjusted_now > ttl` should be `>=`. Verified: changing only line 61 to `>=` makes all 10 tests pass (original: 2 fail).

## 11. `quote_memo`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/quote_memo.py#L59) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_quote_memo.py)

- G (nhãn gốc): dòng 59
- F (LLM đề xuất): dòng 61

```python
    53: 
    54:     item = cache.get(key)
    55:     if item is None:
    56:         return None
    57: 
    58:     payload, ttl = item
>>  59:     effective = _effective_ttl(ttl)
    60: 
>>  61:     if now > effective:
    62:         return None
    63:     return payload
```

> LLM: other (high): Label 59 (`effective = _effective_ttl(ttl)`) is a correct skew helper call; the fault is line 61 `if now > effective` which must be `>=` (entry expires at ttl). Verified: changing only line 61 to `>=` makes all 10 tests pass (original: 3 fail).

## 12. `reserve_lane`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/reserve_lane.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_reserve_lane.py)

- G (nhãn gốc): dòng 60
- F (LLM đề xuất): dòng 62

```python
    54: 
    55:     if len(existing) >= _MAX_LANES_PER_SCHEDULE:
    56:         _log.debug("Lane schedule at capacity (%d slots)", _MAX_LANES_PER_SCHEDULE)
    57:         return False, list(existing)
    58: 
    59:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  60:         if _CONFLICT_STRICT:
    61:             a = _apply_adjacency_tolerance(a, _ADJACENCY_TOLERANCE)
>>  62:         return not (b[1] <= a[0] or b[0] >= a[1])
    63: 
    64:     for slot in existing:
    65:         _validate_window(slot, label="existing slot")
    66:         if overlaps(slot, candidate):
    67:             return False, list(existing)
    68: 
```

> LLM: other (high): Label 60 is the `if _CONFLICT_STRICT:` line inside overlaps (dead with STRICT=False, tolerance 0); the fault is the return on line 62 `not (b[1] <= a[0] or b[0] >= a[1])`. Verified: patching line 62 to `<`/`>` makes all 10 tests pass (original: 6 fail).

## 13. `royalty_payout`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/royalty_payout.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_royalty_payout.py)

- G (nhãn gốc): dòng 68
- S (nhóm dời tới): dòng 67, bản sửa: `        shares.append((r / total_ratio) * (amount - fee) + fee)`

```python
    61:         raise ValueError("invalid ratios")
    62: 
    63:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    64: 
    65:     shares: List[float] = []
    66:     for r in ratios:
>>  67:         shares.append((r / total_ratio) * amount)
>>  68: 
    69:     return [_clamp_payout(s - fee) for s in shares]
```

> LLM: new (medium): Tests (`test_fee_deducted_from_pool_total`) require splitting `amount - fee`; line 67 splits gross `amount` and line 69 deducts `fee` per participant. Fault spans 67 and 69 (two-line fix verified); the oracle's `+ fee` trick is on 67. Original 68 is blank.

## 14. `schedule_window`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_window.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_window.py)

- G (nhãn gốc): dòng 67
- S (nhóm dời tới): dòng 65, bản sửa: `        if not (end < s or start > e):`

```python
    59:             duration constraints.
    60:     """
    61:     start, end = interval
    62:     _validate_interval(start, end)
    63: 
    64:     for s, e in existing:
>>  65:         if not (end <= s or start >= e):
    66:             _log.debug(
>>  67:                 "Conflict detected: proposed (%s, %s) overlaps (%s, %s)",
    68:                 start, end, s, e,
    69:             )
    70:             return False, existing
    71: 
    72:     updated = _merge_sorted(existing, interval)
    73:     return True, updated
```

> LLM: new (high): Boundary tests require `not (end < s or start > e)`; the `<=`/`>=` on line 65 is the fault. Original label 67 is a format-string line inside the debug log in the guard's body.

## 15. `smooth_cpu`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/smooth_cpu.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_smooth_cpu.py)

- G (nhãn gốc): dòng 67
- S (nhóm dời tới): dòng 69, bản sửa: `mean = total / len(tail)`
- F (LLM đề xuất): dòng 68

```python
    61:     _validate_window(window)
    62:     if not values:
    63:         raise ValueError("empty series")
    64: 
    65:     tail = [_clamp_sample(v) for v in values[-window:]]
    66:     total = sum(tail)
>>  67: 
>>  68:     mean = total / window
>>  69: 
    70:     if len(tail) < warmup_min:
    71:         _log.debug("warmup: only %d/%d samples available", len(tail), warmup_min)
    72:         return None
    73:     return mean
```

> LLM: neither (high): Line 68 `mean = total / window` should divide by `len(tail)` (docstring: mean of the last-window samples; fix verified). The oracle recomputes `mean` on blank line 69, a compensating insertion; original label 67 is blank.

## 16. `tensor_slice_pad`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/tensor_slice_pad.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_tensor_slice_pad.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 64

```python
    57:     if requested_length > MAX_SLICE_LENGTH:
    58:         _log.debug("Large slice requested: %d elements", requested_length)
    59: 
    60:     result: List[int] = values[start:end]
    61:     missing = _compute_missing_count(requested_length, len(result))
    62: 
>>  63:     if missing >= 0:
>>  64:         result.extend([pad] * (missing + 1))
    65:     return result
```

> LLM: other (high): Label 63 `if missing >= 0:` is harmless; the deviating token is `+ 1` in line 64 `result.extend([pad] * (missing + 1))` (result must have exactly end - start elements). Verified: patching only line 64 to `[pad] * missing` makes all 10 tests pass, while changing only line 63 to `> 0` leaves 4 failing.

## 17. `track_logout`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/track_logout.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_track_logout.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 69

```python
    61:         ValueError: If cap is provided but is less than 1.
    62:     """
    63:     _validate_cap(cap)
    64:     current = _resolve_current(counters, key)
    65:     updated = current + COUNTER_INCREMENT
    66: 
>>  67:     if cap is not None:
    68:         if updated > cap:
>>  69:             updated = cap - 1
    70: 
    71:     counters[key] = updated
    72:     _log.debug("Logout tracked for key=%s: %d -> %d", key, current, updated)
    73:     return updated
```

> LLM: other (high): Label 67 `if cap is not None:` is a correct outer guard; the fault is line 69 `updated = cap - 1` (should be `cap`). Verified: patching only line 69 makes all tests pass.

## 18. `versions_stream`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/versions_stream.py#L79) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_versions_stream.py)

- G (nhãn gốc): dòng 79
- S (nhóm dời tới): dòng 80, bản sửa: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

```python
    73:             merged.append(a)
    74:             merged.append(b)
    75:             i += 1
    76:             j += 1
    77:     merged.extend(left[i:])
    78:     merged.extend(right[j:])
>>  79: 
>>  80:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    81:         merged.pop()
    82: 
    83:     if log_progress:
    84:         _log.debug("Merged stream contains %d versions", len(merged))
    85: 
    86:     return merged
```

> LLM: new (high): Docstring: both copies of a shared version are kept; the `merged.pop()` guarded by line 80 drops the shared tail element (deleting lines 80-81 passes). The oracle's `!=` makes the guard unsatisfiable, i.e. disables the same injected block, so the relocated line is the fault. Original 79 is blank.

