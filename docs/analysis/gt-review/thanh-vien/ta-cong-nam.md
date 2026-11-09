# Duyệt nhãn dòng lỗi — Tạ Công Nam (19 ca)

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;
  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.
- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.
- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật
  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.
- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.
- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.

## 1. `batch_tally`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/batch_tally.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_batch_tally.py)

- G (nhãn gốc): dòng 61
- F (LLM đề xuất): dòng 62

```python
    55:     """
    56:     _validate_max_value(max_value)
    57: 
    58:     new_value = counts.get(key, DEFAULT_INITIAL_COUNT) + 1
    59: 
    60:     if max_value is not None:
>>  61:         if new_value > max_value:
>>  62:             new_value = max_value - 1
    63: 
    64:     counts[key] = new_value
    65: 
    66:     if _should_log_milestone(new_value):
    67:         _log.debug("Key %s reached milestone count %d", key, new_value)
    68: 
```

> LLM: other (high): The guard at 61 `if new_value > max_value` is correct; the deviation is the guarded statement 62 `new_value = max_value - 1` (should be `max_value`, 'clamped so it never exceeds that ceiling'; tests expect saturation at max_value). Changing 62 to `new_value = max_value` passes all 10 tests.

## 2. `cached_manifest`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/cached_manifest.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_cached_manifest.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 65

```python
    57: 
    58:     if key not in entries:
    59:         _log.debug("Manifest cache miss for key=%s", key)
    60:         return None
    61: 
    62:     value, expires_at = entries[key]
>>  63:     effective = _effective_expiry(expires_at)
    64: 
>>  65:     if now > effective:
    66:         return None
    67:     return value
```

> LLM: other (high): Docstring: valid only when now is strictly before effective expiry, tests expect None at now == expiry; the comparison `if now > effective` on line 65 should be `>=`. Label 63 (`effective = _effective_expiry(expires_at)`) is a correct helper call, one statement before the fault.

## 3. `calibrate_pressure`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_pressure.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_pressure.py)

- G (nhãn gốc): dòng 72
- F (LLM đề xuất): dòng 70

```python
    64:     """
    65:     _validate_segment(x0, x1)
    66: 
    67:     t = _interpolation_parameter(x0, x1, x)
    68:     y = (1 - t) * y0 + t * y1
    69: 
>>  70:     if not clamp:
    71:         low, high = sorted([y0, y1])
>>  72:         y = min(max(y, low), high)
    73: 
    74:     _log.debug("calibrate_pressure: x=%s -> y=%s %s", x, y, PRESSURE_UNIT_LABEL)
    75:     return y
```

> LLM: other (high): Docstring: when clamping is enabled the result is restricted to [min(y0,y1), max(y0,y1)]; line 70 `if not clamp:` inverts this. Label 72 (`y = min(max(y, low), high)`) is the correct clamp expression; the deviating token is `not` on line 70.

## 4. `cost_trendline`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/cost_trendline.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_cost_trendline.py)

- G (nhãn gốc): dòng 66
- F (LLM đề xuất): dòng 65

```python
    59: 
    60:     ratio = (x - x0) / (x1 - x0)
    61:     y = y0 + ratio * (y1 - y0)
    62: 
    63:     _log.debug("%s: ratio=%.4f raw_y=%.4f", LOG_PREFIX, ratio, y)
    64: 
>>  65:     if not clamp:
>>  66:         lo, hi = _compute_bounds(y0, y1)
    67:         if y < lo:
    68:             y = lo
    69:         elif y > hi:
    70:             y = hi
    71: 
    72:     return y
```

> LLM: other (high): Line 65 `if not clamp:` is the inverted guard; label line 66 `lo, hi = _compute_bounds(y0, y1)` is a correct statement inside the inverted block.

## 5. `downtime_booking`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/downtime_booking.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_downtime_booking.py)

- G (nhãn gốc): dòng 63
- F (LLM đề xuất): dòng 64

```python
    57: 
    58:     if candidate[1] - candidate[0] < _MIN_WINDOW_MINUTES:
    59:         _log.debug("Window shorter than %d min; proceeding anyway", _MIN_WINDOW_MINUTES)
    60: 
    61:     _check_capacity(existing)
    62: 
>>  63:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  64:         return not (b[1] <= a[0] or b[0] >= a[1])
    65: 
    66:     for slot in existing:
    67:         if overlaps(slot, candidate):
    68:             return False, list(existing)
    69: 
    70:     merged: List[Tuple[int, int]] = list(existing) + [candidate]
```

> LLM: other (high): Tests require windows that touch at a boundary to count as overlapping; line 64 `return not (b[1] <= a[0] or b[0] >= a[1])` should use `<` / `>`. Label line 63 is the `def overlaps(...)` header, not the faulty expression.

## 6. `feature_flag_rollout`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/feature_flag_rollout.py#L62) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_feature_flag_rollout.py)

- G (nhãn gốc): dòng 62
- F (LLM đề xuất): dòng 63

```python
    56:         ValueError: If *percentage* is outside [0, 1].
    57:     """
    58:     _validate_percentage(percentage)
    59: 
    60:     bucket = _compute_bucket(user_id)
    61:     _log.debug("user=%s bucket=%.4f percentage=%.4f", user_id, bucket, percentage)
>>  62: 
>>  63:     return bucket > percentage
```

> LLM: other (high): Label line 62 is blank. The fault is line 63 `return bucket > percentage`: a user is enrolled when their bucket falls below the rollout fraction, so it should be `<` (with `>` 100% rollout enrolls nobody and 0% enrolls everyone).

## 7. `gradient_clip_budget`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/gradient_clip_budget.py#L62) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_gradient_clip_budget.py)

- G (nhãn gốc): dòng 64
- S (nhóm dời tới): dòng 62, bản sửa: `    norm = _compute_global_norm(gradients) - 1`
- F (LLM đề xuất): dòng 66

```python
    56:     """
    57:     _validate_max_norm(max_norm)
    58: 
    59:     if not gradients:
    60:         return []
    61: 
>>  62:     norm = _compute_global_norm(gradients)
    63:     _log.debug("Global gradient norm: %.6f (budget: %.6f)", norm, max_norm)
>>  64: 
    65:     if norm > max_norm:
>>  66:         scale = max_norm / (norm + 1)
    67:         return [g * scale for g in gradients]
    68:     return list(gradients)
```

> LLM: neither (high): Docstring: rescale so the resulting norm equals max_norm, i.e. `scale = max_norm / norm`; the `+ 1` on line 66 is the injected fault (fix verified passing). Line 62 (`norm = ... - 1`) is a compensating fix at a correct line; original label 64 is blank.

## 8. `latencies_merge`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/latencies_merge.py#L83) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_latencies_merge.py)

- G (nhãn gốc): dòng 83
- F (LLM đề xuất): dòng 86

```python
    77:             j += 1
    78:         else:
    79:             merged.append(a)
    80:             merged.append(b)
    81:             i += 1
    82:             j += 1
>>  83:     merged.extend(left[i:])
    84:     merged.extend(right[j:])
    85: 
>>  86:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    87:         merged.pop()
    88: 
    89:     merged = _cap_capacity(merged)
    90:     return merged
```

> LLM: other (high): Label 83 `merged.extend(left[i:])` is the normal merge tail and is correct. The injected fault is the block 86-87 (`if ... merged[-1] == left[-1] == right[-1]: merged.pop()`) that drops one copy of a shared last latency; docstring says duplicates from both streams are preserved. Three tests fail because of that block.

## 9. `limit_query`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_query.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_query.py)

- G (nhãn gốc): dòng 68
- S (nhóm dời tới): dòng 69, bản sửa: `if len(active) >= limit:`

```python
    62:     _validate_parameters(window, limit)
    63: 
    64:     cutoff = now - window
    65:     active = _filter_active(timestamps, cutoff)
    66: 
    67:     _log.debug("active=%d, limit=%d, window=%d", len(active), limit, window)
>>  68: 
>>  69:     if len(active) > limit:
    70:         return False, 0
    71:     return True, limit - len(active)
```

> LLM: new (high): `len(active) > limit` on line 69 should be `>=` (test `test_exactly_at_limit_denied`). Original label 68 is blank.

## 10. `message_counter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/message_counter.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_message_counter.py)

- G (nhãn gốc): dòng 60
- F (LLM đề xuất): dòng 61

```python
    54:     """
    55:     _validate_cap(cap)
    56:     _initialize_key(counters, key)
    57: 
    58:     counters[key] += 1
    59: 
>>  60:     if cap is not None and counters[key] > cap:
>>  61:         counters[key] = cap - 1
    62:         _log.log(CAP_ENFORCEMENT_LOG_LEVEL, "Counter '%s' capped at %d", key, counters[key])
    63: 
    64:     return counters[key]
```

> LLM: other (high): Label 60 `if cap is not None and counters[key] > cap` is a correct guard. The deviation is line 61 `counters[key] = cap - 1`; the docstring says the counter never exceeds the cap, so it should be set to `cap`.

## 11. `prices_stream`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/prices_stream.py#L80) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_prices_stream.py)

- G (nhãn gốc): dòng 80
- S (nhóm dời tới): dòng 81, bản sửa: `    if merged and left and right and merged[-1] == left[-1] == right[-1] and False:`

```python
    74:             merged.append(a)
    75:             merged.append(b)
    76:             i += 1
    77:             j += 1
    78:     merged.extend(left[i:])
    79:     merged.extend(right[j:])
>>  80: 
>>  81:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    82:         merged.pop()
    83: 
    84:     _log.debug("Merged %d left + %d right -> %d ticks", len(left), len(right), len(merged))
    85:     return merged
```

> LLM: new (high): Docstring: a price in both streams appears twice; the `merged.pop()` guarded by line 81 drops the last shared tick (deleting lines 81-82 passes). The oracle's `and False` just disables the same block, so the relocated line is the injected fault. Original 80 is blank.

## 12. `read_throttle`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/read_throttle.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_read_throttle.py)

- G (nhãn gốc): dòng 69
- S (nhóm dời tới): dòng 70, bản sửa: `if len(active) >= limit:`

```python
    63:     active = _filter_active_timestamps(timestamps, cutoff)
    64: 
    65:     _log.debug(
    66:         "read_throttle: %d active events in last %ds (limit=%d)",
    67:         len(active), window, limit,
    68:     )
>>  69: 
>>  70:     if len(active) > limit:
    71:         return False, 0
    72:     return True, limit - len(active)
```

> LLM: new (high): `len(active) > limit` on line 70 should be `>=` (test `test_exactly_at_limit_denies_further_reads`). Original label 69 is blank.

## 13. `reserve_slot`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/reserve_slot.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_reserve_slot.py)

- G (nhãn gốc): dòng 60
- F (LLM đề xuất): dòng 61

```python
    54:         raise ValueError("Maximum slot capacity reached for this resource")
    55: 
    56:     effective_candidate = candidate
    57:     if _CONFLICT_STRICT and _ADJACENCY_BUFFER > _MIN_SLOT_DURATION:
    58:         effective_candidate = _apply_adjacency_buffer(candidate, _ADJACENCY_BUFFER)
    59: 
>>  60:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  61:         return not (b[1] <= a[0] or b[0] >= a[1])
    62: 
    63:     for slot in existing:
    64:         _validate_slot(slot)
    65:         if overlaps(slot, effective_candidate):
    66:             _log.debug("Candidate %s conflicts with existing slot %s", candidate, slot)
    67:             return False, list(existing)
```

> LLM: other (high): Label 60 is the `def overlaps(...)` header; the comparison on line 61 uses `<=`/`>=` so touching slots are accepted although tests reject them. Verified: patching line 61 to `<`/`>` makes all 11 tests pass (original: 6 fail).

## 14. `schedule_call`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_call.py#L71) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_call.py)

- G (nhãn gốc): dòng 71
- F (LLM đề xuất): dòng 72

```python
    65:     if len(existing) >= _MAX_CALLS_PER_DAY:
    66:         _log.debug("Daily call limit of %d reached", _MAX_CALLS_PER_DAY)
    67:         return False, list(existing)
    68: 
    69:     _validate_time_slot(candidate, label="candidate")
    70: 
>>  71:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  72:         return not (b[1] <= a[0] or b[0] >= a[1])
    73: 
    74:     for slot in existing:
    75:         effective = _apply_adjacency_buffer(slot) if _CONFLICT_STRICT else slot
    76:         if overlaps(effective, candidate):
    77:             return False, list(existing)
    78: 
```

> LLM: other (high): Label 71 is the `def overlaps(...)` header; the fault is its body on line 72 `not (b[1] <= a[0] or b[0] >= a[1])`. Verified: patching line 72 to `<`/`>` makes all tests pass.

## 15. `session_memo`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/session_memo.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_session_memo.py)

- G (nhãn gốc): dòng 70
- S (nhóm dời tới): dòng 71, bản sửa: `if now >= deadline:`

```python
    64:     record = store.get(key, _MISSING_SENTINEL)
    65:     if record is _MISSING_SENTINEL:
    66:         _log.debug("Session key %r not found in store", key)
    67:         return default
    68:     value, deadline = record
    69:     deadline = _adjust_deadline(deadline)
>>  70: 
>>  71:     if now > deadline:
    72:         return default
    73:     return value
```

> LLM: new (high): Docstring: value returned only while now 'has not yet reached' the deadline; `>` on line 71 should be `>=` (tests at exact deadline expect default). Original label 70 is blank.

## 16. `storage_mix`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/storage_mix.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_storage_mix.py)

- G (nhãn gốc): dòng 63
- S (nhóm dời tới): dòng 60, bản sửa: `    adjusted = [(c + (t - c) * damping) / sum(current) for c, t in zip(current, target)]`

```python
    54:         raise ValueError("shape mismatch")
    55:     if not current:
    56:         raise ValueError("empty allocation")
    57: 
    58:     _log.debug("Blending %d-tier allocation with damping=%.4f", len(current), damping)
    59: 
>>  60:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    61: 
    62:     adjusted = _clamp_allocation(adjusted)
>>  63: 
    64:     return adjusted
```

> LLM: original (medium): Docstring: 'the returned vector is normalised so that its elements sum to 1', but after `_clamp_allocation` (62) the function returns un-normalised values; the missing normalization belongs at blank line 63 (inserting `adjusted = [v / sum(adjusted) for v in adjusted]` there passes). The oracle's edit at 60 divides the blend by `sum(current)`, which is wrong in general (sum(adjusted) != sum(current) unless both inputs have equal sums) and bypasses the clamp, so it is compensating. Executable alternative: line 64 (`return adjusted`).

## 17. `throughput_trendline`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/throughput_trendline.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_throughput_trendline.py)

- G (nhãn gốc): dòng 61
- F (LLM đề xuất): dòng 60

```python
    54:     _validate_segment(x0, x1)
    55: 
    56:     t = _compute_parameter(x, x0, x1)
    57:     _log.debug("interpolation parameter t=%.6f for x=%.4f", t, x)
    58:     y = (1 - t) * y0 + t * y1
    59: 
>>  60:     if not clamp:
>>  61:         low, high = sorted([y0, y1])
    62:         y = min(max(y, low), high)
    63: 
    64:     if abs(y) < INTERPOLATION_PRECISION:
    65:         y = 0.0
    66: 
    67:     return y
```

> LLM: other (high): Label 61 (`low, high = sorted([y0, y1])`) is a correct body line; the fault is the inverted guard on line 60 `if not clamp:` (clamping must happen when clamp=True). Verified: changing only line 60 to `if clamp:` makes all 10 tests pass (original: 6 fail).

## 18. `track_release`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/track_release.py#L58) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_track_release.py)

- G (nhãn gốc): dòng 58
- F (LLM đề xuất): dòng 60

```python
    52:     """
    53:     _validate_key(key)
    54: 
    55:     current = counters.get(key, MIN_COUNTER_VALUE)
    56:     updated = current + COUNTER_INCREMENT
    57: 
>>  58:     if cap is not None:
    59:         if updated > cap:
>>  60:             updated = cap - 1
    61: 
    62:     updated = _clamp_counter(updated, MIN_COUNTER_VALUE)
    63: 
    64:     counters[key] = updated
    65:     _log.debug("Release counter for %s updated: %d -> %d", key, current, updated)
    66:     return updated
```

> LLM: other (high): Label 58 `if cap is not None:` is a correct outer guard; the fault is line 60 `updated = cap - 1` (should be `cap`). Verified: patching only line 60 makes all tests pass.

## 19. `view_tally`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/view_tally.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_view_tally.py)

- G (nhãn gốc): dòng 67
- F (LLM đề xuất): dòng 68

```python
    61:     _validate_max_value(max_value)
    62: 
    63:     current = _resolve_current_count(counts, key)
    64:     new_value = current + INCREMENT_STEP
    65: 
    66:     if max_value is not None:
>>  67:         if new_value > max_value:
>>  68:             new_value = max_value - 1
    69: 
    70:     counts[key] = new_value
    71:     _log.debug("view_tally: key=%s new_value=%d", key, new_value)
    72:     return new_value
```

> LLM: other (high): Label 67 `if new_value > max_value:` is a correct guard; the deviating token is on line 68 `new_value = max_value - 1` (should clamp to max_value). Verified: patching only line 68 makes all tests pass.

