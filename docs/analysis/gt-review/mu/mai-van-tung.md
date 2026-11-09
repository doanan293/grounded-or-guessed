# Duyệt mù dòng lỗi — Mai Văn Tùng (20 ca)

**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt
lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.
- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Có thể chạy kiểm thử trên máy nếu muốn.
- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng
  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.
- Mỗi ca khoảng 3 phút.

## 1. `guard_search`

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

## 2. `combine_depths`

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

## 3. `cost_trendline`

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

## 4. `calibrate_trend`

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

## 5. `divide_refund`

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

## 6. `fee_splitter`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/fee_splitter.py#L58) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_fee_splitter.py)

Ứng viên: `A` = dòng 62, `B` = dòng 59, `C` = dòng 58, `D` = dòng 61

```python
   50:         ValueError: If ratios are empty, collectively non-positive, or amount is negative.
   51:     """
   52:     _validate_ratios(ratios)
   53:     if amount < 0:
   54:         raise ValueError("negative amount")
   55: 
   56:     _log.debug("Splitting amount=%.4f among %d participants (fee=%.4f)", amount, len(ratios), fee)
   57: 
C  58:     total_ratio = sum(ratios)
B  59:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
   60: 
D  61:     payouts = [_clamp_payout(b - fee) for b in base]
A  62: 
   63:     if abs(sum(payouts) - (amount - fee * len(ratios))) < _PRECISION:
   64:         _log.debug("Payout sum verified within precision tolerance")
   65: 
   66:     return payouts
```

## 7. `demand_curve`

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

## 8. `quota_allocator_service`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/quota_allocator_service.py#L68) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_quota_allocator_service.py)

Ứng viên: `A` = dòng 70, `B` = dòng 68, `C` = dòng 71, `D` = dòng 69

```python
   60:         ValueError: If *total* or *minimum* is negative, or *weights* is
   61:             empty / all-zero.
   62:     """
   63:     _validate_inputs(total, weights, minimum)
   64: 
   65:     weight_sum = sum(weights)
   66:     raw = _compute_raw_shares(total, weights, weight_sum, minimum)
   67: 
B  68:     if _INTEGER_ALLOCATION:
D  69:         _log.debug("Rounding %d raw allocations to integers", len(raw))
A  70: 
C  71:     return [int(x) for x in raw]
```

## 9. `notification_gate`

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

## 10. `metric_rolling_avg`

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

## 11. `throughput_trendline`

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

## 12. `realign_replica`

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

## 13. `prediction_cache`

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

## 14. `calibrate_score`

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

## 15. `smooth_pressure`

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

## 17. `track_build`

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

## 18. `bump_refund`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/bump_refund.py#L57) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_bump_refund.py)

Ứng viên: `A` = dòng 57, `B` = dòng 58, `C` = dòng 59, `D` = dòng 61

```python
   49: 
   50:     Raises:
   51:         ValueError: If max_value is negative.
   52:     """
   53:     _validate_max_value(max_value)
   54: 
   55:     new_value = _current_count(counts, key) + INCREMENT_STEP
   56: 
A  57:     if max_value is not None:
B  58:         if new_value > max_value:
C  59:             new_value = max_value - 1
   60: 
D  61:     counts[key] = new_value
   62:     _log.debug("Refund count for %s updated to %d", key, new_value)
   63:     return new_value
```

## 19. `attention_mask_merge`

[Chương trình](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/programs/attention_mask_merge.py#L65) · [Kiểm thử](https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark/testcases/test_attention_mask_merge.py)

Ứng viên: `A` = dòng 67, `B` = dòng 65, `C` = dòng 66, `D` = dòng 68

```python
   57:     if len(mask_a) != len(mask_b):
   58:         raise ValueError("shape mismatch")
   59: 
   60:     _validate_mask(mask_a, "mask_a")
   61:     _validate_mask(mask_b, "mask_b")
   62: 
   63:     _log.debug("Merging attention masks of length %d", len(mask_a))
   64: 
B  65:     merged: List[bool] = []
C  66:     for a, b in zip(mask_a, mask_b):
A  67:         merged.append(a or b)
D  68:     return merged
```

## 20. `cacheline_expiry`

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

