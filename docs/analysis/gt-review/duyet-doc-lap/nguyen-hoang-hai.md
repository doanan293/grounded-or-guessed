# Duyệt mù dòng lỗi — Nguyễn Hoàng Hải (20 ca)

**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt
lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.
- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Có thể chạy kiểm thử trên máy nếu muốn.
- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng
  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.
- Mỗi ca khoảng 3 phút.

## 1. `throughput_trendline`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/throughput_trendline.py#L58) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_throughput_trendline.py)

Ứng viên: `A` = dòng 58, `B` = dòng 60, `C` = dòng 61, `D` = dòng 62

```python
   50: 
   51:     Raises:
   52:         ValueError: If *x0* equals *x1*, making the segment degenerate.
   53:     """
   54:     _validate_segment(x0, x1)
   55: 
   56:     t = _compute_parameter(x, x0, x1)
   57:     _log.debug("interpolation parameter t=%.6f for x=%.4f", t, x)
A  58:     y = (1 - t) * y0 + t * y1
   59: 
B  60:     if not clamp:
C  61:         low, high = sorted([y0, y1])
D  62:         y = min(max(y, low), high)
   63: 
   64:     if abs(y) < INTERPOLATION_PRECISION:
   65:         y = 0.0
   66: 
```

## 2. `plan_conference_slot`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/plan_conference_slot.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_plan_conference_slot.py)

Ứng viên: `A` = dòng 73, `B` = dòng 76, `C` = dòng 78, `D` = dòng 75

```python
   65:         OverflowError: If the daily slot capacity would be exceeded.
   66:     """
   67:     _validate_slot(candidate, label="candidate")
   68:     if candidate[0] >= candidate[1]:
   69:         raise ValueError("start must be before end")
   70: 
   71:     _check_capacity(existing)
   72: 
A  73:     buffer = _ADJACENCY_BUFFER_MINUTES if _CONFLICT_STRICT else 0
   74: 
D  75:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
B  76:         return not (b[1] <= a[0] or b[0] >= a[1])
   77: 
C  78:     for slot in existing:
   79:         _validate_slot(slot, label="existing slot")
   80:         if overlaps((slot[0] - buffer, slot[1] + buffer), candidate):
   81:             _log.debug("Candidate %s conflicts with %s", candidate, slot)
   82:             return False, list(existing)
```

## 3. `lru_evictor`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/lru_evictor.py#L26) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_lru_evictor.py)

Ứng viên: `A` = dòng 27, `B` = dòng 56, `C` = dòng 28, `D` = dòng 26

```python
   18:         )
   19: 
   20: 
   21: def _trim_oldest_entries(order: List[Any], target_len: int) -> int:
   22:     """Remove oldest entries from the front of the access list.
   23: 
   24:     Returns the number of entries evicted.
   25:     """
D  26:     evicted = 0
A  27:     while len(order) > target_len and evicted < MAX_EVICTION_BATCH:
C  28:         order.pop(0)
   29:         evicted += 1
   30:     return evicted
   31: 
   32: 
   33: def lru_evictor(order: List[Any], *, capacity: int = DEFAULT_CAPACITY) -> List[Any]:
   34:     """Evict least-recently-used keys until the cache is strictly under capacity.
   35: 
   36:     The eviction strategy removes keys from the oldest end of the access-order
   37:     list until the number of remaining keys is below the stated capacity limit.
   38:     This mirrors the behavior of bounded LRU caches that must keep at most
   39:     ``capacity - 1`` live entries after an eviction sweep.
   40: 
   41:     Args:
   42:         order: List of cache keys ordered from oldest (index 0) to newest.
   43:             Modified in place.
   44:         capacity: Maximum number of entries the cache may hold.  Eviction
   45:             continues until ``len(order) < capacity``.
   46: 
   47:     Returns:
   48:         The same list object with evicted entries removed from the front.
   49: 
   50:     Raises:
   51:         ValueError: If *capacity* is negative.
   52:     """
   53:     _validate_capacity(capacity)
   54: 
   55:     total_evicted = 0
B  56:     while len(order) > capacity:
   57:         removed = _trim_oldest_entries(order, capacity)
   58:         total_evicted += removed
   59:         if removed == 0:
   60:             break
```

## 4. `replica_sync_offsets`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/replica_sync_offsets.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_replica_sync_offsets.py)

Ứng viên: `A` = dòng 70, `B` = dòng 69, `C` = dòng 68, `D` = dòng 71

```python
   60:         if primary[i] < replica[j]:
   61:             missing.append(primary[i])
   62:             i += 1
   63:         elif replica[j] < primary[i]:
   64:             j += 1
   65:         else:
   66:             i += 1
   67:             j += 1
C  68:     missing.extend(primary[i:])
B  69: 
A  70:     if missing and replica and missing[-1] == replica[-1]:
D  71:         missing.pop()
   72:     return _clamp_batch(missing, SYNC_BATCH_LIMIT)
```

## 5. `api_rate_guard`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/api_rate_guard.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_api_rate_guard.py)

Ứng viên: `A` = dòng 73, `B` = dòng 70, `C` = dòng 74, `D` = dòng 72

```python
   62:     _validate_parameters(window, limit)
   63: 
   64:     cutoff = now - window
   65:     recent = _filter_recent(timestamps, cutoff)
   66: 
   67:     _log.debug(
   68:         "rate_guard: %d recent requests in last %ds (limit=%d)",
   69:         len(recent), window, limit,
B  70:     )
   71: 
D  72:     if len(recent) > limit:
A  73:         return False, 0
C  74:     return True, limit - len(recent)
```

## 6. `water_allocator`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/water_allocator.py#L26) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_water_allocator.py)

Ứng viên: `A` = dòng 29, `B` = dòng 28, `C` = dòng 30, `D` = dòng 26

```python
   18:         raise ValueError("negative minimum")
   19:     if sum(weights) == 0:
   20:         raise ValueError("zero total weight")
   21: 
   22:     weight_sum = sum(weights)
   23:     shares = []
   24:     for w in weights:
   25:         portion = (w / weight_sum) * total
D  26:         shares.append(portion if portion > minimum else minimum)
   27: 
B  28:     if floor_to_int:
A  29:         return [int(v) for v in shares]
C  30:     return shares
```

## 7. `limit_query`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_query.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_query.py)

Ứng viên: `A` = dòng 68, `B` = dòng 67, `C` = dòng 69, `D` = dòng 70

```python
   59:     Raises:
   60:         ValueError: If *window* or *limit* are below their minimums.
   61:     """
   62:     _validate_parameters(window, limit)
   63: 
   64:     cutoff = now - window
   65:     active = _filter_active(timestamps, cutoff)
   66: 
B  67:     _log.debug("active=%d, limit=%d, window=%d", len(active), limit, window)
A  68: 
C  69:     if len(active) > limit:
D  70:         return False, 0
   71:     return True, limit - len(active)
```

## 8. `quota_for_memory`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/quota_for_memory.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_quota_for_memory.py)

Ứng viên: `A` = dòng 71, `B` = dòng 69, `C` = dòng 72, `D` = dòng 70

```python
   61:     if total < 0:
   62:         raise ValueError("total must be non-negative")
   63:     if minimum < 0:
   64:         raise ValueError("minimum must be non-negative")
   65: 
   66:     _validate_weights(weights)
   67: 
   68:     planned = _compute_planned(total, weights, minimum)
B  69:     _log.debug("planned allocations (raw): %s", planned)
D  70: 
A  71:     if _INTEGER_ALLOCATION:
C  72:         allocations = [int(x) for x in planned]
   73:     else:
   74:         allocations = planned  # type: ignore[assignment]
   75: 
   76:     return allocations
```

## 9. `token_expiry_check`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/token_expiry_check.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_token_expiry_check.py)

Ứng viên: `A` = dòng 69, `B` = dòng 67, `C` = dòng 70, `D` = dòng 71

```python
   59:         _log.debug("Token key %r not found in store", key)
   60:         return None
   61: 
   62:     value, expires_at = record
   63: 
   64:     if expires_at > now + _MAX_TOKEN_LIFETIME:
   65:         return None
   66: 
B  67:     adjusted_expiry = _adjust_expiry_for_skew(expires_at)
   68: 
A  69:     if now > adjusted_expiry:
C  70:         return None
D  71:     return value
```

## 10. `priority_mix`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/priority_mix.py#L57) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_priority_mix.py)

Ứng viên: `A` = dòng 57, `B` = dòng 61, `C` = dòng 58, `D` = dòng 59

```python
   49:     Raises:
   50:         ValueError: If inputs are empty, mismatched, or damping is out of range.
   51:     """
   52:     _validate_inputs(current, target, damping)
   53: 
   54:     _log.debug("Rebalancing %d-slot allocation with damping=%.3f", len(current), damping)
   55: 
   56:     updated: List[float] = []
A  57:     for idx in range(len(current)):
C  58:         blended = current[idx] + (target[idx] - current[idx]) * damping
D  59:         updated.append(_clamp_weight(blended))
   60: 
B  61:     return updated
```

## 11. `shift_feature`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/shift_feature.py#L55) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_shift_feature.py)

Ứng viên: `A` = dòng 59, `B` = dòng 55, `C` = dòng 57, `D` = dòng 61

```python
   47:         *current* toward *target* by the given damping factor.
   48: 
   49:     Raises:
   50:         ValueError: If inputs are empty, mismatched in length, or exceed
   51:             the maximum allowed number of components.
   52:     """
   53:     _validate_inputs(current, target)
   54: 
B  55:     _log.debug("Shifting %d-component allocation with damping=%.4f", len(current), damping)
   56: 
C  57:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
   58: 
A  59:     adjusted = _clamp_values(adjusted)
   60: 
D  61:     return adjusted
```

## 12. `schedule_window`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_window.py#L64) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_window.py)

Ứng viên: `A` = dòng 66, `B` = dòng 67, `C` = dòng 64, `D` = dòng 65

```python
   56: 
   57:     Raises:
   58:         ValueError: If *interval* has non-positive duration or violates
   59:             duration constraints.
   60:     """
   61:     start, end = interval
   62:     _validate_interval(start, end)
   63: 
C  64:     for s, e in existing:
D  65:         if not (end <= s or start >= e):
A  66:             _log.debug(
B  67:                 "Conflict detected: proposed (%s, %s) overlaps (%s, %s)",
   68:                 start, end, s, e,
   69:             )
   70:             return False, existing
   71: 
```

## 13. `smooth_cpu`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/smooth_cpu.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_smooth_cpu.py)

Ứng viên: `A` = dòng 68, `B` = dòng 69, `C` = dòng 67, `D` = dòng 66

```python
   58:         ValueError: If *values* is empty or *window* is non-positive
   59:             or exceeds the hard maximum.
   60:     """
   61:     _validate_window(window)
   62:     if not values:
   63:         raise ValueError("empty series")
   64: 
   65:     tail = [_clamp_sample(v) for v in values[-window:]]
D  66:     total = sum(tail)
C  67: 
A  68:     mean = total / window
B  69: 
   70:     if len(tail) < warmup_min:
   71:         _log.debug("warmup: only %d/%d samples available", len(tail), warmup_min)
   72:         return None
   73:     return mean
```

## 14. `temperature_window_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/temperature_window_avg.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_temperature_window_avg.py)

Ứng viên: `A` = dòng 67, `B` = dòng 68, `C` = dòng 69, `D` = dòng 65

```python
   57:     Raises:
   58:         ValueError: If *window* is not positive or *values* is empty or
   59:             contains temperatures below absolute zero.
   60:     """
   61:     _validate_window(window)
   62:     _validate_series(values)
   63: 
   64:     tail = values[-window:]
D  65:     total = sum(tail)
   66: 
A  67:     mean = total / window
B  68: 
C  69:     _log.debug("window=%d, tail_len=%d, mean=%.4f", window, len(tail), mean)
   70: 
   71:     if len(tail) < warmup_min:
   72:         return None
   73:     return mean
```

## 15. `download_rate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/download_rate.py#L73) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_download_rate.py)

Ứng viên: `A` = dòng 74, `B` = dòng 73, `C` = dòng 75, `D` = dòng 76

```python
   65:         ValueError: If *window* is below the minimum or a timestamp
   66:             lies unreasonably far in the future.
   67:     """
   68:     _validate_inputs(timestamps, now, window)
   69: 
   70:     cutoff = now - window
   71:     active = _active_timestamps(timestamps, cutoff)
   72: 
B  73:     _log.debug("active=%d, limit=%d, window=%d", len(active), limit, window)
A  74: 
C  75:     if len(active) > limit:
D  76:         return False, 0
   77:     return True, limit - len(active)
```

## 16. `checkout_rate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/checkout_rate.py#L64) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_checkout_rate.py)

Ứng viên: `A` = dòng 66, `B` = dòng 67, `C` = dòng 64, `D` = dòng 68

```python
   56:     Raises:
   57:         ValueError: If any input violates domain constraints.
   58:     """
   59:     _validate_inputs(timestamps, now, window, limit)
   60: 
   61:     window_start = now - window
   62:     recent = _filter_recent(timestamps, window_start)
   63: 
C  64:     _log.debug("checkout_rate: %d events in window [%s, %s]", len(recent), window_start, now)
   65: 
A  66:     if len(recent) > limit:
B  67:         return False, 0
D  68:     return True, limit - len(recent)
```

## 17. `combine_scores`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/combine_scores.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_combine_scores.py)

Ứng viên: `A` = dòng 71, `B` = dòng 69, `C` = dòng 68, `D` = dòng 66

```python
   58:     while i < len(left) and j < len(right):
   59:         if left[i] <= right[j]:
   60:             merged.append(_clamp_score(left[i]))
   61:             i += 1
   62:         else:
   63:             merged.append(_clamp_score(right[j]))
   64:             j += 1
   65:     merged.extend(_clamp_score(v) for v in left[i:])
D  66:     merged.extend(_clamp_score(v) for v in right[j:])
   67: 
C  68:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
B  69:         merged.pop()
   70: 
A  71:     _log.debug("Merged %d + %d scores into %d entries", len(left), len(right), len(merged))
   72:     return merged
```

## 18. `audit_window_filter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/audit_window_filter.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_audit_window_filter.py)

Ứng viên: `A` = dòng 67, `B` = dòng 65, `C` = dòng 68, `D` = dòng 66

```python
   57: 
   58:     Returns:
   59:         A list of timestamps that fall within the audit window.
   60: 
   61:     Raises:
   62:         TypeError: If window is not numeric.
   63:         ValueError: If window is outside the allowed range.
   64:     """
B  65:     _validate_window(window)
D  66:     cutoff = _compute_cutoff(now, window)
A  67:     _log.debug("Audit window cutoff=%s, now=%s, window=%ss", cutoff, now, window)
C  68:     return [t for t in timestamps if t >= cutoff]
```

## 19. `energy_window_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/energy_window_avg.py#L70) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_energy_window_avg.py)

Ứng viên: `A` = dòng 72, `B` = dòng 70, `C` = dòng 74, `D` = dòng 76

```python
   62:         raise ValueError("window must be positive")
   63:     if not values:
   64:         raise ValueError("no values")
   65: 
   66:     _validate_readings(values)
   67: 
   68:     effective_window = _clamp_window(window, len(values))
   69:     recent = values[-effective_window:]
B  70:     total = sum(recent)
   71: 
A  72:     _log.debug("Window %d, recent count %d, total %.4f", window, len(recent), total)
   73: 
C  74:     mean = total / window
   75: 
D  76:     if len(recent) < warmup_min:
   77:         return None
   78:     return mean
```

## 20. `schedule_training`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_training.py#L64) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_training.py)

Ứng viên: `A` = dòng 66, `B` = dòng 64, `C` = dòng 67, `D` = dòng 68

```python
   56: 
   57:     Raises:
   58:         ValueError: If the proposed interval has non-positive duration
   59:             or is below the minimum duration threshold.
   60:         OverflowError: If the schedule has reached maximum capacity.
   61:     """
   62:     start, end = interval
   63:     _validate_interval(start, end)
B  64:     _check_capacity(existing)
   65: 
A  66:     for s, e in existing:
C  67:         if not (end <= s or start >= e):
D  68:             _log.debug(
   69:                 "Conflict detected: proposed (%s, %s) overlaps with (%s, %s)",
   70:                 start, end, s, e,
   71:             )
   72:             return False, existing
```

