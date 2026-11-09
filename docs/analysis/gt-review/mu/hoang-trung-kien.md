# Duyệt mù dòng lỗi — Hoàng Trung Kiên (20 ca)

**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt
lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.

Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.

- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.
- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.
  Có thể chạy kiểm thử trên máy nếu muốn.
- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng
  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.
- Mỗi ca khoảng 3 phút.

## 1. `token_expiry_check`

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

## 2. `api_rate_guard`

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

## 3. `attention_mask_merge`

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

## 4. `smooth_cpu`

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

## 5. `energy_window_avg`

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

## 6. `lru_evictor`

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

## 7. `water_allocator`

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

## 9. `grant_share`

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

## 10. `schedule_pickup`

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

## 11. `priority_mix`

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

## 12. `calibrate_pressure`

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

## 13. `storage_quota_split`

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

## 14. `replica_sync_offsets`

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

## 15. `bump_refund`

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

## 16. `fee_splitter`

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

## 17. `limit_query`

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

## 18. `payment_split_rebate`

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

## 20. `ttl_snapshot_store`

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

