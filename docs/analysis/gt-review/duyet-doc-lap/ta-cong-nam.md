# Duyệt mù dòng lỗi — Tạ Công Nam (20 ca)

**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt
lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.
- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Có thể chạy kiểm thử trên máy nếu muốn.
- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng
  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.
- Mỗi ca khoảng 3 phút.

## 1. `votes_apportion`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/votes_apportion.py#L26) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_votes_apportion.py)

Ứng viên: `A` = dòng 29, `B` = dòng 26, `C` = dòng 28, `D` = dòng 30

```python
   18:         raise ValueError("negative minimum")
   19:     if sum(weights) == 0:
   20:         raise ValueError("zero total weight")
   21: 
   22:     weight_sum = sum(weights)
   23:     shares = []
   24:     for w in weights:
   25:         portion = (w / weight_sum) * total
B  26:         shares.append(portion if portion > minimum else minimum)
   27: 
C  28:     if floor_to_int:
A  29:         return [int(v) for v in shares]
D  30:     return shares
```

## 2. `storage_quota_split`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/storage_quota_split.py#L64) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_storage_quota_split.py)

Ứng viên: `A` = dòng 66, `B` = dòng 64, `C` = dòng 70, `D` = dòng 67

```python
   56:     """
   57:     if total < 0:
   58:         raise ValueError("negative total")
   59: 
   60:     _validate_ratios(ratios)
   61: 
   62:     if fee < -_FEE_PRECISION:
   63:         raise ValueError("fee must not be negative")
B  64: 
   65:     total_ratio = sum(ratios)
A  66:     shares = [(r / total_ratio) * total for r in ratios]
D  67: 
   68:     _log.debug("Computed raw shares for %d participants", len(shares))
   69: 
C  70:     floored = _apply_floor([s - fee for s in shares])
   71:     return floored
```

## 3. `track_build`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/track_build.py#L50) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_track_build.py)

Ứng viên: `A` = dòng 53, `B` = dòng 54, `C` = dòng 50, `D` = dòng 52

```python
   42:         The metric value after incrementing (and optional clamping).
   43: 
   44:     Raises:
   45:         ValueError: If *key* is empty or not a string.
   46:     """
   47:     _validate_key(key)
   48: 
   49:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
C  50:     counters[key] += 1
   51: 
D  52:     if cap is not None and counters[key] > cap:
A  53:         counters[key] = cap - 1
B  54:         _log.debug("%s: %s counter clamped at %d", CAP_ENFORCEMENT_LABEL, key, cap)
   55: 
   56:     if _should_log_milestone(counters[key]):
   57:         _log.debug("Metric '%s' reached milestone %d", key, counters[key])
   58: 
```

## 4. `traffic_shaping_gate`

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

## 5. `blend_levels`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/blend_levels.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_blend_levels.py)

Ứng viên: `A` = dòng 72, `B` = dòng 74, `C` = dòng 75, `D` = dòng 77

```python
   64:     while i < len(left) and j < len(right):
   65:         if left[i] <= right[j]:
   66:             merged.append(left[i])
   67:             i += 1
   68:         else:
   69:             merged.append(right[j])
   70:             j += 1
   71:     merged.extend(left[i:])
A  72:     merged.extend(right[j:])
   73: 
B  74:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
C  75:         merged.pop()
   76: 
D  77:     return _cap_depth(merged)
```

## 6. `schedule_training`

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

## 7. `allocate_budget_cut`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/allocate_budget_cut.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_allocate_budget_cut.py)

Ứng viên: `A` = dòng 65, `B` = dòng 67, `C` = dòng 63, `D` = dòng 64

```python
   55:         raise ValueError("negative amount")
   56: 
   57:     total_ratio = sum(ratios)
   58:     if total_ratio <= 0:
   59:         raise ValueError("invalid ratios")
   60: 
   61:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
   62: 
C  63:     shares: List[float] = []
D  64:     for r in ratios:
A  65:         shares.append((r / total_ratio) * amount)
   66: 
B  67:     return [_clamp_payout(s - fee) for s in shares]
```

## 8. `plan_conference_slot`

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

## 9. `payment_split_rebate`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/payment_split_rebate.py#L62) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_payment_split_rebate.py)

Ứng viên: `A` = dòng 64, `B` = dòng 62, `C` = dòng 65, `D` = dòng 66

```python
   54:             to zero, or any individual ratio is negative.
   55:     """
   56:     if total < 0:
   57:         raise ValueError("negative total")
   58: 
   59:     _validate_ratios(ratios)
   60: 
   61:     total_ratio = sum(ratios)
B  62:     shares = [_round_share((r / total_ratio) * total) for r in ratios]
   63: 
A  64:     _log.debug("Computed raw shares: %s (rebate=%.4f)", shares, rebate)
C  65: 
D  66:     return [s - rebate for s in shares]
```

## 10. `allocate_prize_cut`

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

## 11. `credits_allocator`

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

## 12. `task_tally`

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

## 13. `reservation_booking`

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

## 14. `login_throttle`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/login_throttle.py#L67) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_login_throttle.py)

Ứng viên: `A` = dòng 69, `B` = dòng 67, `C` = dòng 70, `D` = dòng 68

```python
   59:     _validate_parameters(window, limit)
   60: 
   61:     cutoff = now - window
   62:     recent = _filter_recent(timestamps, cutoff)
   63: 
   64:     _log.debug(
   65:         "login_throttle: %d recent attempts in last %ds (limit %d)",
   66:         len(recent), window, limit,
B  67:     )
D  68: 
A  69:     if len(recent) > limit:
C  70:         return False, 0
   71:     return True, limit - len(recent)
```

## 15. `calibrate_trend`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_trend.py#L61) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_trend.py)

Ứng viên: `A` = dòng 64, `B` = dòng 63, `C` = dòng 65, `D` = dòng 61

```python
   53:     """
   54:     _validate_segment(x0, x1)
   55: 
   56:     t = _compute_parameter(x, x0, x1)
   57: 
   58:     if abs(t) > MAX_EXTRAPOLATION_WARN_RATIO:
   59:         _log.debug("query x=%.4f is far outside calibration window [%.4f, %.4f]", x, x0, x1)
   60: 
D  61:     y = (1 - t) * y0 + t * y1
   62: 
B  63:     if not clamp:
A  64:         low, high = sorted([y0, y1])
C  65:         y = min(max(y, low), high)
   66: 
   67:     return y
```

## 16. `combine_scores`

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

## 17. `plan_upgrade_slot`

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

## 18. `download_rate`

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

## 19. `guard_email`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/guard_email.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_guard_email.py)

Ứng viên: `A` = dòng 72, `B` = dòng 73, `C` = dòng 71, `D` = dòng 69

```python
   61:     Raises:
   62:         ValueError: If *window* or *limit* are below their minimums.
   63:     """
   64:     _validate_parameters(window, limit)
   65: 
   66:     cutoff = now - window
   67:     recent = _filter_recent(timestamps, cutoff)
   68: 
D  69:     _log.debug("guard_email: %d recent sends in last %ds (limit %d)", len(recent), window, limit)
   70: 
C  71:     if len(recent) > limit:
A  72:         return False, 0
B  73:     return True, limit - len(recent)
```

## 20. `combine_responses`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/combine_responses.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_combine_responses.py)

Ứng viên: `A` = dòng 71, `B` = dòng 74, `C` = dòng 69, `D` = dòng 72

```python
   61:         if left[i] <= right[j]:
   62:             merged.append(left[i])
   63:             i += 1
   64:         else:
   65:             merged.append(right[j])
   66:             j += 1
   67: 
   68:     merged.extend(left[i:])
C  69:     merged.extend(right[j:])
   70: 
A  71:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
D  72:         merged.pop()
   73: 
B  74:     if len(merged) >= MERGE_LOG_THRESHOLD:
   75:         _log.debug("Merged %d responses (threshold=%d)", len(merged), MERGE_LOG_THRESHOLD)
   76: 
   77:     return merged
```

