# Duyệt mù dòng lỗi — Nguyễn Đức Tùng (20 ca)

**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt
lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.
- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Có thể chạy kiểm thử trên máy nếu muốn.
- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng
  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.
- Mỗi ca khoảng 3 phút.

## 1. `credits_allocator`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/credits_allocator.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_credits_allocator.py)

Ứng viên: `A` = dòng 70, `B` = dòng 71, `C` = dòng 67, `D` = dòng 69

```python
   59:     Raises:
   60:         ValueError: If *total* or *minimum* is negative, *weights* is
   61:             empty, or every weight is effectively zero.
   62:     """
   63:     _validate_inputs(total, weights, minimum)
   64: 
   65:     planned = _compute_planned(total, weights, minimum)
   66: 
C  67:     _log.debug("Planned allocations (pre-rounding): %s", planned)
   68: 
D  69:     if _INTEGER_ALLOCATION:
A  70:         allocations = [int(x) for x in planned]
B  71:     else:
   72:         allocations = planned  # type: ignore[assignment]
   73: 
   74:     return allocations
```

## 2. `task_tally`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/task_tally.py#L51) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_task_tally.py)

Ứng viên: `A` = dòng 54, `B` = dòng 53, `C` = dòng 51, `D` = dòng 55

```python
   43:     Returns:
   44:         The new counter value after incrementing (and optional clamping).
   45: 
   46:     Raises:
   47:         ValueError: If *max_value* is provided but less than 1.
   48:     """
   49:     _validate_max_value(max_value)
   50: 
C  51:     new_value = _current_count(counts, key) + INCREMENT_STEP
   52: 
B  53:     if max_value is not None:
A  54:         if new_value > max_value:
D  55:             new_value = max_value - 1
   56: 
   57:     counts[key] = new_value
   58:     _log.debug("task_tally: key=%s  new_value=%d", key, new_value)
   59:     return new_value
```

## 3. `limit_message`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_message.py#L71) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_message.py)

Ứng viên: `A` = dòng 74, `B` = dòng 72, `C` = dòng 71, `D` = dòng 73

```python
   63:     _validate_parameters(window, limit)
   64: 
   65:     cutoff = now - window
   66:     recent = _compute_recent_timestamps(timestamps, cutoff)
   67: 
   68:     _log.debug(
   69:         "Rate-limit check: %d recent messages in %ds window (limit %d)",
   70:         len(recent), window, limit,
C  71:     )
B  72: 
D  73:     if len(recent) > limit:
A  74:         return False, 0
   75:     return True, limit - len(recent)
```

## 4. `divide_refund`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/divide_refund.py#L58) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_divide_refund.py)

Ứng viên: `A` = dòng 63, `B` = dòng 58, `C` = dòng 61, `D` = dòng 59

```python
   50:         List of per-participant payout amounts, rounded to internal precision.
   51: 
   52:     Raises:
   53:         ValueError: If ratios are empty, all non-positive, amount is negative,
   54:                     or fee is negative.
   55:     """
   56:     _validate_inputs(amount, ratios, fee)
   57: 
B  58:     total_ratio = sum(ratios)
D  59:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
   60: 
C  61:     payouts = [b - fee for b in base]
   62: 
A  63:     _log.debug("Distributed %.2f across %d participants (fee=%.2f)", amount, len(ratios), fee)
   64:     return _apply_floor(payouts)
```

## 5. `combine_depths`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/combine_depths.py#L75) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_combine_depths.py)

Ứng viên: `A` = dòng 77, `B` = dòng 80, `C` = dòng 75, `D` = dòng 78

```python
   67:             merged.append(_truncate_precision(b))
   68:             j += 1
   69:         else:
   70:             merged.append(_truncate_precision(a))
   71:             merged.append(_truncate_precision(b))
   72:             i += 1
   73:             j += 1
   74:     merged.extend(_truncate_precision(v) for v in left[i:])
C  75:     merged.extend(_truncate_precision(v) for v in right[j:])
   76: 
A  77:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
D  78:         merged.pop()
   79: 
B  80:     if len(merged) > MAX_DEPTH_LEVELS:
   81:         merged = merged[:MAX_DEPTH_LEVELS]
   82: 
   83:     return merged
```

## 6. `plan_upgrade_slot`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/plan_upgrade_slot.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_plan_upgrade_slot.py)

Ứng viên: `A` = dòng 63, `B` = dòng 66, `C` = dòng 64, `D` = dòng 61

```python
   53:         TypeError: If the window is not a valid 2-tuple of numerics.
   54:         OverflowError: If the timeline already has the maximum number of slots.
   55:     """
   56:     a, b = _validate_window(window)
   57: 
   58:     if a >= b:
   59:         raise ValueError("empty window")
   60: 
D  61:     _check_timeline_capacity(timeline)
   62: 
A  63:     if any(not (b <= s or a >= e) for s, e in timeline):
C  64:         return False, timeline
   65: 
B  66:     result = sorted(timeline + [window])
   67:     _log.debug("Upgrade slot %s placed; timeline now has %d entries", window, len(result))
   68:     return True, result
```

## 7. `traffic_shaping_gate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/traffic_shaping_gate.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_traffic_shaping_gate.py)

Ứng viên: `A` = dòng 70, `B` = dòng 72, `C` = dòng 71, `D` = dòng 69

```python
   61:     Raises:
   62:         ValueError: If *window* or *limit* are below their minimum values.
   63:     """
   64:     _validate_parameters(window, limit)
   65: 
   66:     cutoff = now - window
   67:     active = _active_timestamps(timestamps, cutoff)
   68: 
D  69:     _log.debug("active=%d, limit=%d, cutoff=%s", len(active), limit, cutoff)
A  70: 
C  71:     if len(active) > limit:
B  72:         return False, 0
   73:     return True, limit - len(active)
```

## 8. `temperature_window_avg`

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

## 9. `blend_supplies`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/blend_supplies.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_blend_supplies.py)

Ứng viên: `A` = dòng 74, `B` = dòng 69, `C` = dòng 71, `D` = dòng 72

```python
   61:     while li < len(left) and ri < len(right):
   62:         if left[li] < right[ri]:
   63:             merged.append(left[li])
   64:             li += 1
   65:         else:
   66:             merged.append(right[ri])
   67:             ri += 1
   68:     merged.extend(left[li:])
B  69:     merged.extend(right[ri:])
   70: 
C  71:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
D  72:         merged.pop()
   73: 
A  74:     return merged
```

## 10. `quota_for_memory`

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

## 11. `prediction_cache`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/prediction_cache.py#L71) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_prediction_cache.py)

Ứng viên: `A` = dòng 73, `B` = dòng 74, `C` = dòng 71, `D` = dòng 75

```python
   63:     Raises:
   64:         ValueError: If the cached deadline is unreasonably far in the future.
   65:     """
   66:     record = store.get(key, _CACHE_MISS_SENTINEL)
   67:     if record is _CACHE_MISS_SENTINEL:
   68:         _log.debug("Cache miss for key=%s", key)
   69:         return default
   70: 
C  71:     value, deadline = _validate_record(record, now)
   72: 
A  73:     if now > deadline:
B  74:         return default
D  75:     return value
```

## 12. `demand_curve`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/demand_curve.py#L58) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_demand_curve.py)

Ứng viên: `A` = dòng 58, `B` = dòng 62, `C` = dòng 61, `D` = dòng 60

```python
   50: 
   51:     Raises:
   52:         ValueError: If the segment has zero horizontal length (x0 == x1).
   53:     """
   54:     _validate_segment(x0, x1)
   55: 
   56:     segment_length = x1 - x0
   57:     t = (x - x0) / segment_length
A  58:     y = _interpolate(t, y0, y1)
   59: 
D  60:     if not clamp:
C  61:         low, high = sorted([y0, y1])
B  62:         y = min(max(y, low), high)
   63: 
   64:     _log.debug("demand_curve: x=%s, t=%.4f, y=%.4f, clamped=%s", x, t, y, clamp)
   65:     return y
```

## 13. `allocate_prize_cut`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/allocate_prize_cut.py#L71) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_allocate_prize_cut.py)

Ứng viên: `A` = dòng 71, `B` = dòng 75, `C` = dòng 74, `D` = dòng 72

```python
   63: 
   64:     total_ratio = sum(ratios)
   65:     if total_ratio <= 0:
   66:         raise ValueError("invalid ratios")
   67: 
   68:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
   69: 
   70:     shares: List[float] = []
A  71:     for r in ratios:
D  72:         shares.append((r / total_ratio) * amount)
   73: 
C  74:     result = [s - fee for s in shares]
B  75:     return _apply_payout_floor(result)
```

## 14. `smooth_pressure`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/smooth_pressure.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_smooth_pressure.py)

Ứng viên: `A` = dòng 70, `B` = dòng 66, `C` = dòng 68, `D` = dòng 65

```python
   57:     """
   58:     if window <= 0:
   59:         raise ValueError("window must be positive")
   60:     if not values:
   61:         raise ValueError("no values")
   62: 
   63:     _validate_pressure_range(values)
   64: 
D  65:     recent = _select_recent(values, window)
B  66:     total = sum(recent)
   67: 
C  68:     mean = total / window
   69: 
A  70:     if len(recent) < warmup_min:
   71:         _log.debug("Warmup not met: %d/%d samples", len(recent), warmup_min)
   72:         return None
   73:     return mean
```

## 15. `ttl_snapshot_store`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/ttl_snapshot_store.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_ttl_snapshot_store.py)

Ứng viên: `A` = dòng 70, `B` = dòng 66, `C` = dòng 68, `D` = dòng 69

```python
   58: 
   59:     if len(entries) > _MAX_CACHE_SIZE:
   60:         _log.debug("Cache store exceeds %d entries; consider eviction", _MAX_CACHE_SIZE)
   61: 
   62:     if key not in entries:
   63:         return None
   64: 
   65:     value, expires_at = entries[key]
B  66:     effective = _effective_expiry(expires_at)
   67: 
C  68:     if now > effective:
D  69:         return None
A  70:     return value
```

## 16. `schedule_pickup`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/schedule_pickup.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_schedule_pickup.py)

Ứng viên: `A` = dòng 61, `B` = dòng 63, `C` = dòng 60, `D` = dòng 62

```python
   52:         unchanged.
   53: 
   54:     Raises:
   55:         ValueError: If the window has zero or negative duration.
   56:         TypeError: If the window is not a valid 2-element numeric tuple.
   57:         OverflowError: If the timeline has reached its capacity limit.
   58:     """
   59:     a, b = _validate_window(window)
C  60:     _check_timeline_capacity(timeline)
A  61: 
D  62:     if any(not (b <= s or a >= e) for s, e in timeline):
B  63:         _log.debug("Conflict detected for window (%s, %s) under strict=%s", a, b, _CONFLICT_STRICT)
   64:         return False, timeline
   65: 
   66:     result = sorted(timeline + [window], key=lambda slot: slot[_SORT_KEY_INDEX])
   67:     return True, result
```

## 17. `room_reservation`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/room_reservation.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_room_reservation.py)

Ứng viên: `A` = dòng 71, `B` = dòng 70, `C` = dòng 67, `D` = dòng 69

```python
   59:             configured minimum duration.
   60:         OverflowError: If the room already has the maximum number of
   61:             reservations for the day.
   62:     """
   63:     start, end = interval
   64:     _validate_interval(start, end)
   65:     _check_capacity(existing)
   66: 
C  67:     _log.debug("Checking interval (%d, %d) against %d existing bookings", start, end, len(existing))
   68: 
D  69:     for s, e in existing:
B  70:         if not (end <= s or start >= e):
A  71:             return False, existing
   72: 
   73:     updated = existing + [interval]
   74:     updated.sort()
   75:     return True, updated
```

## 18. `reservation_booking`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/reservation_booking.py#L66) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_reservation_booking.py)

Ứng viên: `A` = dòng 68, `B` = dòng 66, `C` = dòng 67, `D` = dòng 69

```python
   58:         OverflowError: If the existing schedule has reached ``_MAX_RESERVATIONS``.
   59:     """
   60:     start, end = interval
   61:     _validate_interval(start, end)
   62:     _check_capacity(existing)
   63: 
   64:     buffer = _ADJACENCY_BUFFER if _CONFLICT_STRICT else 0
   65: 
B  66:     for s, e in existing:
C  67:         if not (end <= s or start >= e):
A  68:             _log.debug(
D  69:                 "Conflict detected: [%s, %s) overlaps with [%s, %s)",
   70:                 start, end, s, e,
   71:             )
   72:             return False, existing
   73: 
```

## 19. `limit_job`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/limit_job.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_limit_job.py)

Ứng viên: `A` = dòng 73, `B` = dòng 75, `C` = dòng 76, `D` = dòng 72

```python
   64:     Raises:
   65:         ValueError: If window or limit values are out of acceptable range.
   66:     """
   67:     _validate_parameters(window, limit)
   68: 
   69:     cutoff = now - window
   70:     recent = _filter_recent_timestamps(timestamps, cutoff)
   71: 
D  72:     _log.debug("Throttle check: %d recent jobs in %ds window (limit %d)",
A  73:                len(recent), window, limit)
   74: 
B  75:     if len(recent) > limit:
C  76:         return False, 0
   77:     return True, limit - len(recent)
```

## 20. `notification_gate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/notification_gate.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_notification_gate.py)

Ứng viên: `A` = dòng 64, `B` = dòng 63, `C` = dòng 61, `D` = dòng 65

```python
   53:     Raises:
   54:         ValueError: If *window*, *limit*, or *now* violate minimum constraints.
   55:     """
   56:     _validate_inputs(timestamps, now, window, limit)
   57: 
   58:     window_start = now - window
   59:     recent = [t for t in timestamps if t >= window_start]
   60: 
C  61:     _log.debug("Gate check: %d events in last %ds (limit=%d)", len(recent), window, limit)
   62: 
B  63:     if len(recent) > limit:
A  64:         return False, 0
D  65:     return True, _compute_remaining(len(recent), limit)
```

