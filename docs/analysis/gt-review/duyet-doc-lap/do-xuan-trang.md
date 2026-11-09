# Duyệt mù dòng lỗi — Đỗ Xuân Tráng (20 ca)

**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt
lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.
- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Có thể chạy kiểm thử trên máy nếu muốn.
- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng
  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.
- Mỗi ca khoảng 3 phút.

## 1. `schedule_window`

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

## 2. `allocate_budget_cut`

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

## 3. `room_reservation`

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

## 4. `votes_apportion`

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

## 5. `audit_window_filter`

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

## 6. `blend_levels`

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

## 7. `metric_rolling_avg`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/metric_rolling_avg.py#L69) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_metric_rolling_avg.py)

Ứng viên: `A` = dòng 73, `B` = dòng 69, `C` = dòng 71, `D` = dòng 70

```python
   61:         raise ValueError("no values")
   62: 
   63:     cleaned = _filter_valid(values)
   64:     if not cleaned:
   65:         raise ValueError("no values")
   66: 
   67:     tail = cleaned[-window:]
   68:     total = sum(tail)
B  69: 
D  70:     avg = total / window
C  71: 
   72:     _log.debug("rolling_avg window=%d tail_len=%d avg=%s", window, len(tail), avg)
A  73: 
   74:     if len(tail) < min_samples:
   75:         return None
   76:     return avg
```

## 8. `blend_supplies`

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

## 9. `limit_message`

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

## 10. `calibrate_pressure`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_pressure.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_pressure.py)

Ứng viên: `A` = dòng 71, `B` = dòng 72, `C` = dòng 68, `D` = dòng 70

```python
   60:         The calibrated pressure value in {PRESSURE_UNIT_LABEL}.
   61: 
   62:     Raises:
   63:         ValueError: If x0 == x1 (degenerate segment).
   64:     """
   65:     _validate_segment(x0, x1)
   66: 
   67:     t = _interpolation_parameter(x0, x1, x)
C  68:     y = (1 - t) * y0 + t * y1
   69: 
D  70:     if not clamp:
A  71:         low, high = sorted([y0, y1])
B  72:         y = min(max(y, low), high)
   73: 
   74:     _log.debug("calibrate_pressure: x=%s -> y=%s %s", x, y, PRESSURE_UNIT_LABEL)
   75:     return y
```

## 11. `grant_share`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/grant_share.py#L60) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_grant_share.py)

Ứng viên: `A` = dòng 62, `B` = dòng 60, `C` = dòng 63, `D` = dòng 65

```python
   52:     Raises:
   53:         ValueError: If *ratios* is empty, sums to zero or less, or
   54:             *amount* is negative.
   55:     """
   56:     _validate_ratios(ratios)
   57:     if amount < 0:
   58:         raise ValueError("negative amount")
   59: 
B  60:     _log.debug("Distributing %.2f among %d recipients (fee=%.2f)", amount, len(ratios), fee)
   61: 
A  62:     total_ratio = sum(ratios)
C  63:     base = [(r / total_ratio) * amount for r in ratios]
   64: 
D  65:     return [_clamp_payout(share - fee) for share in base]
```

## 12. `calibrate_score`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/calibrate_score.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_calibrate_score.py)

Ứng viên: `A` = dòng 68, `B` = dòng 67, `C` = dòng 66, `D` = dòng 65

```python
   57:     Raises:
   58:         ValueError: If the segment is degenerate (x0 == x1).
   59:     """
   60:     _validate_segment(x0, x1)
   61: 
   62:     t = _compute_interpolation_param(x0, x1, x)
   63:     y = y0 + t * (y1 - y0)
   64: 
D  65:     if not clamp:
C  66:         lo, hi = (min(y0, y1), max(y0, y1))
B  67:         if y < lo:
A  68:             y = lo
   69:         if y > hi:
   70:             y = hi
   71: 
   72:     _log.debug("calibrate_score: t=%.4f, y=%.6f (clamp=%s)", t, y, clamp)
```

## 13. `cost_trendline`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/cost_trendline.py#L63) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_cost_trendline.py)

Ứng viên: `A` = dòng 66, `B` = dòng 63, `C` = dòng 67, `D` = dòng 65

```python
   55:     Raises:
   56:         ValueError: If x0 equals x1, making interpolation undefined.
   57:     """
   58:     _validate_anchor_points(x0, x1)
   59: 
   60:     ratio = (x - x0) / (x1 - x0)
   61:     y = y0 + ratio * (y1 - y0)
   62: 
B  63:     _log.debug("%s: ratio=%.4f raw_y=%.4f", LOG_PREFIX, ratio, y)
   64: 
D  65:     if not clamp:
A  66:         lo, hi = _compute_bounds(y0, y1)
C  67:         if y < lo:
   68:             y = lo
   69:         elif y > hi:
   70:             y = hi
   71: 
```

## 14. `cacheline_expiry`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/cacheline_expiry.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_cacheline_expiry.py)

Ứng viên: `A` = dòng 68, `B` = dòng 69, `C` = dòng 67, `D` = dòng 65

```python
   57:         return _DEFAULT_PAYLOAD
   58: 
   59:     payload, ttl = item
   60: 
   61:     if ttl > _MAX_TTL_SECONDS + now:
   62:         _log.debug("TTL for key=%s exceeds maximum; treating as expired", key)
   63:         return _DEFAULT_PAYLOAD
   64: 
D  65:     adjusted_ttl = _adjust_ttl_for_skew(ttl)
   66: 
C  67:     if now > adjusted_ttl:
A  68:         return _DEFAULT_PAYLOAD
B  69:     return payload
```

## 15. `guard_search`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/guard_search.py#L72) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_guard_search.py)

Ứng viên: `A` = dòng 74, `B` = dòng 75, `C` = dòng 72, `D` = dòng 73

```python
   64:     Raises:
   65:         ValueError: If window or limit values are below minimum thresholds.
   66:     """
   67:     _validate_parameters(window, limit)
   68: 
   69:     cutoff = now - window
   70:     active = _filter_active_timestamps(timestamps, cutoff)
   71: 
C  72:     _log.debug("guard_search: %d active requests in window", len(active))
D  73: 
A  74:     if len(active) > limit:
B  75:         return False, 0
   76:     return True, limit - len(active)
```

## 16. `shift_feature`

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

## 17. `limit_job`

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

## 18. `login_throttle`

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

## 19. `combine_responses`

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

## 20. `realign_replica`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/realign_replica.py#L56) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_realign_replica.py)

Ứng viên: `A` = dòng 56, `B` = dòng 58, `C` = dòng 57, `D` = dòng 60

```python
   48: 
   49:     Raises:
   50:         ValueError: If inputs are empty, mismatched, or damping is out of range.
   51:     """
   52:     _validate_inputs(current, target, damping)
   53:     _log.debug("Realigning %d replicas with damping=%.4f", len(current), damping)
   54: 
   55:     adjusted: List[float] = []
A  56:     for c, t in zip(current, target):
C  57:         blended = c + (t - c) * damping
B  58:         adjusted.append(_clamp_allocation(blended))
   59: 
D  60:     return adjusted
```

