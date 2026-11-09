# Review of relocated ground-truth labels

For each program: `>>` marks the original label and the relocated label. The fix is the minimal edit
that makes every test pass at the relocated line. Verdict in `review.csv`: `new`, `original`, `either`,
`neither`. The human verdict is final.

## 1. `cached_inventory` — reviewer: Doãn Văn An

Original label: line 69; relocated: line 70 (replace, 1 token(s)).

```
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

Fix at line 70: `if now >= adjusted_deadline:`

## 2. `cached_preference` — reviewer: Tạ Công Nam

Original label: line 83; relocated: line 85 (replace, 1 token(s)).

```
    77:     if item is None:
    78:         _log.debug("Cache miss for key '%s'", validated_key)
    79:         return None
    80:     payload, ttl = item
    81: 
    82:     if ttl > _MAX_TTL_SECONDS + _DEFAULT_TTL_SECONDS:
>>  83:         _log.debug("Entry '%s' has abnormally large TTL: %s", validated_key, ttl)
    84: 
>>  85:     if now > ttl + _CLOCK_SKEW_TOLERANCE:
    86:         return None
    87:     return payload
```

Fix at line 85: `    if now >= ttl + _CLOCK_SKEW_TOLERANCE:`

## 3. `calibrate_latency` — reviewer: Nguyễn Hoàng Hải

Original label: line 73; relocated: line 70 (replace, 1 token(s)).

```
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

Fix at line 70: `if clamp:`

## 4. `catalog_cache` — reviewer: Đỗ Xuân Tráng

Original label: line 63; relocated: line 64 (replace, 1 token(s)).

```
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

Fix at line 64: `    if now >= adjusted_expiry:`

## 5. `config_expiry` — reviewer: Hoàng Trung Kiên

Original label: line 78; relocated: line 77 (replace, 1 token(s)).

```
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

Fix at line 77: `if now >= adjusted_expiry:`

## 6. `coverage_interp` — reviewer: Mai Văn Tùng

Original label: line 65; relocated: line 66 (replace, 1 token(s)).

```
    59:         ValueError: If ``x0`` and ``x1`` are effectively equal.
    60:     """
    61:     _validate_segment(x0, x1)
    62: 
    63:     t = _compute_parameter(x, x0, x1)
    64:     y = y0 + t * (y1 - y0)
>>  65: 
>>  66:     if not clamp:
    67:         lo, hi = (min(y0, y1), max(y0, y1))
    68:         if y < lo:
    69:             y = lo
    70:         if y > hi:
    71:             y = hi
    72: 
```

Fix at line 66: `    if clamp:`

## 7. `demand_forecast_curve` — reviewer: Nguyễn Đức Tùng

Original label: line 65; relocated: line 66 (replace, 1 token(s)).

```
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

Fix at line 66: `    if clamp:`

## 8. `donation_share` — reviewer: Doãn Văn An

Original label: line 59; relocated: line 58 (replace, 6 token(s)).

```
    52:     if amount < 0:
    53:         raise ValueError("negative amount")
    54: 
    55:     _log.debug("Distributing %.2f among %d recipients (fee=%.2f)", amount, len(ratios), fee)
    56: 
    57:     total_ratio = sum(ratios)
>>  58:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
>>  59: 
    60:     payouts = [_round_payout(max(_MIN_PAYOUT, b - fee)) for b in base]
    61:     return payouts
```

Fix at line 58: `    base = list(map(lambda r: (r / total_ratio) * (amount - fee) + fee, ratios))`

## 9. `download_rate` — reviewer: Tạ Công Nam

Original label: line 74; relocated: line 75 (replace, 1 token(s)).

```
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

Fix at line 75: `    if len(active) >= limit:`

## 10. `email_send_quota` — reviewer: Nguyễn Hoàng Hải

Original label: line 65; relocated: line 66 (replace, 1 token(s)).

```
    59:     recent = _filter_recent_timestamps(sent, cutoff)
    60: 
    61:     _log.debug(
    62:         "%s | window=%ds limit=%d recent=%d",
    63:         QUOTA_LOG_PREFIX, window, limit, len(recent),
    64:     )
>>  65: 
>>  66:     if len(recent) > limit:
    67:         return False
    68:     return True
```

Fix at line 66: `    if len(recent) >= limit:`

## 11. `estimate_temperature` — reviewer: Đỗ Xuân Tráng

Original label: line 69; relocated: line 68 (replace, 1 token(s)).

```
    62:     _validate_segment(x0, x1)
    63: 
    64:     segment_length = x1 - x0
    65:     t = (x - x0) / (x1 - x0)
    66:     y = (1 - t) * y0 + t * y1
    67: 
>>  68:     if not clamp:
>>  69:         low, high = sorted([y0, y1])
    70:         y = min(max(y, low), high)
    71: 
    72:     _log.debug("Interpolated temp at x=%.4f: t=%.4f, y=%.4f", x, t, y)
    73:     return _round_temperature(y)
```

Fix at line 68: `    if clamp:`

## 12. `fee_splitter` — reviewer: Hoàng Trung Kiên

Original label: line 62; relocated: line 59 (replace, 6 token(s)).

```
    53:     if amount < 0:
    54:         raise ValueError("negative amount")
    55: 
    56:     _log.debug("Splitting amount=%.4f among %d participants (fee=%.4f)", amount, len(ratios), fee)
    57: 
    58:     total_ratio = sum(ratios)
>>  59:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
    60: 
    61:     payouts = [_clamp_payout(b - fee) for b in base]
>>  62: 
    63:     if abs(sum(payouts) - (amount - fee * len(ratios))) < _PRECISION:
    64:         _log.debug("Payout sum verified within precision tolerance")
    65: 
    66:     return payouts
```

Fix at line 59: `    base = list(map(lambda r: (r / total_ratio) * (amount - fee) + fee, ratios))`

## 13. `gpu_memory_pool` — reviewer: Mai Văn Tùng

Original label: line 74; relocated: line 75 (replace, 1 token(s)).

```
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

Fix at line 75: `if used + request >= effective_cap:`

## 14. `gradient_clip_budget` — reviewer: Nguyễn Đức Tùng

Original label: line 64; relocated: line 62 (replace, 2 token(s)).

```
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
    66:         scale = max_norm / (norm + 1)
    67:         return [g * scale for g in gradients]
    68:     return list(gradients)
```

Fix at line 62: `    norm = _compute_global_norm(gradients) - 1`

## 15. `guard_search` — reviewer: Doãn Văn An

Original label: line 73; relocated: line 74 (replace, 1 token(s)).

```
    67:     _validate_parameters(window, limit)
    68: 
    69:     cutoff = now - window
    70:     active = _filter_active_timestamps(timestamps, cutoff)
    71: 
    72:     _log.debug("guard_search: %d active requests in window", len(active))
>>  73: 
>>  74:     if len(active) > limit:
    75:         return False, 0
    76:     return True, limit - len(active)
```

Fix at line 74: `    if len(active) >= limit:`

## 16. `guard_write` — reviewer: Tạ Công Nam

Original label: line 69; relocated: line 70 (replace, 1 token(s)).

```
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

Fix at line 70: `    if len(recent) >= limit:`

## 17. `invoice_merge_stream` — reviewer: Nguyễn Hoàng Hải

Original label: line 82; relocated: line 79;83 (replace, 2 token(s)).

```
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

Fix at line 79;83: `    return merged`

## 18. `kv_snapshot_reader` — reviewer: Đỗ Xuân Tráng

Original label: line 69; relocated: line 70;71 (replace, 1 token(s)).

```
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

Fix at line 70;71: `        if k > key:`

## 19. `limit_api` — reviewer: Hoàng Trung Kiên

Original label: line 65; relocated: line 66 (replace, 1 token(s)).

```
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

Fix at line 66: `    if len(recent) >= limit:`

## 20. `limit_job` — reviewer: Mai Văn Tùng

Original label: line 73; relocated: line 75 (replace, 1 token(s)).

```
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

Fix at line 75: `    if len(recent) >= limit:`

## 21. `limit_message` — reviewer: Nguyễn Đức Tùng

Original label: line 72; relocated: line 73 (replace, 1 token(s)).

```
    66:     recent = _compute_recent_timestamps(timestamps, cutoff)
    67: 
    68:     _log.debug(
    69:         "Rate-limit check: %d recent messages in %ds window (limit %d)",
    70:         len(recent), window, limit,
    71:     )
>>  72: 
>>  73:     if len(recent) > limit:
    74:         return False, 0
    75:     return True, limit - len(recent)
```

Fix at line 73: `    if len(recent) >= limit:`

## 22. `limit_ping` — reviewer: Doãn Văn An

Original label: line 69; relocated: line 70 (replace, 1 token(s)).

```
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

Fix at line 70: `    if len(recent) >= limit:`

## 23. `limit_query` — reviewer: Tạ Công Nam

Original label: line 68; relocated: line 69 (replace, 1 token(s)).

```
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

Fix at line 69: `if len(active) >= limit:`

## 24. `login_throttle` — reviewer: Nguyễn Hoàng Hải

Original label: line 68; relocated: line 69 (replace, 1 token(s)).

```
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

Fix at line 69: `if len(recent) >= limit:`

## 25. `maintenance_booking` — reviewer: Đỗ Xuân Tráng

Original label: line 76; relocated: line 77 (replace, 2 token(s)).

```
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

Fix at line 77: `    if any(not (b < s or a > e) for s, e in timeline):`

## 26. `metric_rolling_avg` — reviewer: Hoàng Trung Kiên

Original label: line 69; relocated: line 71;73 (replace, 8 token(s)).

```
    63:     cleaned = _filter_valid(values)
    64:     if not cleaned:
    65:         raise ValueError("no values")
    66: 
    67:     tail = cleaned[-window:]
    68:     total = sum(tail)
>>  69: 
    70:     avg = total / window
>>  71: 
    72:     _log.debug("rolling_avg window=%d tail_len=%d avg=%s", window, len(tail), avg)
>>  73: 
    74:     if len(tail) < min_samples:
    75:         return None
    76:     return avg
```

Fix at line 71;73: `    avg = total / len(tail)`

## 27. `optimizer_step_guard` — reviewer: Mai Văn Tùng

Original label: line 61; relocated: line 65 (replace, 5 token(s)).

```
    55: 
    56:     Raises:
    57:         TypeError: If *loss_value* is not numeric.
    58:         ValueError: If *loss_value* is negative.
    59:     """
    60:     _validate_loss_value(loss_value)
>>  61: 
    62:     if loss_value == loss_value and loss_value > max_loss:
    63:         _log.debug(_format_guard_message(loss_value, False))
    64:         return False
>>  65: 
    66:     _log.debug(_format_guard_message(loss_value, True))
    67:     return True
```

Fix at line 65: `return loss_value == loss_value`

## 28. `prices_stream` — reviewer: Nguyễn Đức Tùng

Original label: line 80; relocated: line 81 (replace, 2 token(s)).

```
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

Fix at line 81: `    if merged and left and right and merged[-1] == left[-1] == right[-1] and False:`

## 29. `read_throttle` — reviewer: Doãn Văn An

Original label: line 69; relocated: line 70 (replace, 1 token(s)).

```
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

Fix at line 70: `if len(active) >= limit:`

## 30. `rebate_splitter` — reviewer: Tạ Công Nam

Original label: line 63; relocated: line 62 (replace, 6 token(s)).

```
    56:     if amount < 0:
    57:         raise ValueError("negative amount")
    58: 
    59:     _log.debug("Splitting %.4f among %d recipients (fee=%.4f)", amount, len(ratios), fee)
    60: 
    61:     total_ratio = sum(ratios)
>>  62:     base = [(r / total_ratio) * amount for r in ratios]
>>  63: 
    64:     return [_clamp_payout(share - fee) for share in base]
```

Fix at line 62: `    base = [(r / total_ratio) * (amount - fee) + fee for r in ratios]`

## 31. `replica_sync_offsets` — reviewer: Nguyễn Hoàng Hải

Original label: line 69; relocated: line 70 (replace, 8 token(s)).

```
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

Fix at line 70: `if missing and replica and primary[0] != OFFSET_SENTINEL and missing[-1] == replica[-1]:`

## 32. `revenue_share` — reviewer: Đỗ Xuân Tráng

Original label: line 71; relocated: line 70 (replace, 6 token(s)).

```
    64:         raise ValueError("invalid ratios")
    65: 
    66:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    67: 
    68:     shares: List[float] = []
    69:     for r in ratios:
>>  70:         shares.append((r / total_ratio) * amount)
>>  71: 
    72:     return [_clamp_payout(s - fee) for s in shares]
```

Fix at line 70: `        shares.append((r / total_ratio) * (amount - fee) + fee)`

## 33. `rolling_usage` — reviewer: Hoàng Trung Kiên

Original label: line 66; relocated: line 68;70 (replace, 8 token(s)).

```
    60:         ValueError: If *window* is non-positive or *series* is empty.
    61:     """
    62:     _validate_inputs(series, window)
    63: 
    64:     tail: Sequence[float] = series[-window:]
    65:     total: float = sum(tail)
>>  66: 
    67:     avg = total / window
>>  68: 
    69:     _log.debug("tail=%d total=%.4f avg=%.4f", len(tail), total, avg)
>>  70: 
    71:     if len(tail) < max(warmup_min, _WARMUP_SAMPLES):
    72:         return None
    73:     return _round_metric(avg)
```

Fix at line 68;70: `    avg = total / len(tail)`

## 34. `royalty_payout` — reviewer: Mai Văn Tùng

Original label: line 68; relocated: line 67 (replace, 6 token(s)).

```
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

Fix at line 67: `        shares.append((r / total_ratio) * (amount - fee) + fee)`

## 35. `schedule_car` — reviewer: Nguyễn Đức Tùng

Original label: line 62; relocated: line 61 (replace, 2 token(s)).

```
    55:     a, b = window
    56:     if a >= b:
    57:         raise ValueError("empty window")
    58: 
    59:     _check_timeline_capacity(timeline)
    60: 
>>  61:     if any(not (b <= s or a >= e) for s, e in timeline):
>>  62:         return False, timeline
    63: 
    64:     _log.debug("Booking accepted for window [%d, %d)", a, b)
    65:     result = sorted(timeline + [window])
    66:     return True, result
```

Fix at line 61: `    if any(not (b < s or a > e) for s, e in timeline):`

## 36. `schedule_pickup` — reviewer: Doãn Văn An

Original label: line 61; relocated: line 62 (replace, 2 token(s)).

```
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

Fix at line 62: `    if any(not (b < s or a > e) for s, e in timeline):`

## 37. `schedule_window` — reviewer: Tạ Công Nam

Original label: line 67; relocated: line 65 (replace, 2 token(s)).

```
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

Fix at line 65: `        if not (end < s or start > e):`

## 38. `session_memo` — reviewer: Nguyễn Hoàng Hải

Original label: line 70; relocated: line 71 (replace, 1 token(s)).

```
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

Fix at line 71: `if now >= deadline:`

## 39. `shift_risk` — reviewer: Đỗ Xuân Tráng

Original label: line 62; relocated: line 61 (replace, 4 token(s)).

```
    55: 
    56:     _validate_allocation(current, "current")
    57:     _validate_allocation(target, "target")
    58: 
    59:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    60: 
>>  61:     adjusted = [_clamp(v) for v in adjusted]
>>  62: 
    63:     _log.debug("Adjusted allocation before normalization: %s", adjusted)
    64: 
    65:     return adjusted
```

Fix at line 61: `    adjusted = [v / sum(adjusted) for v in adjusted]`

## 40. `smooth_cpu` — reviewer: Hoàng Trung Kiên

Original label: line 67; relocated: line 69 (replace, 8 token(s)).

```
    61:     _validate_window(window)
    62:     if not values:
    63:         raise ValueError("empty series")
    64: 
    65:     tail = [_clamp_sample(v) for v in values[-window:]]
    66:     total = sum(tail)
>>  67: 
    68:     mean = total / window
>>  69: 
    70:     if len(tail) < warmup_min:
    71:         _log.debug("warmup: only %d/%d samples available", len(tail), warmup_min)
    72:         return None
    73:     return mean
```

Fix at line 69: `mean = total / len(tail)`

## 41. `storage_mix` — reviewer: Mai Văn Tùng

Original label: line 63; relocated: line 60 (replace, 7 token(s)).

```
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

Fix at line 60: `    adjusted = [(c + (t - c) * damping) / sum(current) for c, t in zip(current, target)]`

## 42. `storage_quota_split` — reviewer: Nguyễn Đức Tùng

Original label: line 67; relocated: line 64 (replace, 9 token(s)).

```
    58:         raise ValueError("negative total")
    59: 
    60:     _validate_ratios(ratios)
    61: 
    62:     if fee < -_FEE_PRECISION:
    63:         raise ValueError("fee must not be negative")
>>  64: 
    65:     total_ratio = sum(ratios)
    66:     shares = [(r / total_ratio) * total for r in ratios]
>>  67: 
    68:     _log.debug("Computed raw shares for %d participants", len(shares))
    69: 
    70:     floored = _apply_floor([s - fee for s in shares])
    71:     return floored
```

Fix at line 64: `    total, fee = total - fee, 0`

## 43. `traffic_shaping_gate` — reviewer: Doãn Văn An

Original label: line 70; relocated: line 71 (replace, 1 token(s)).

```
    64:     _validate_parameters(window, limit)
    65: 
    66:     cutoff = now - window
    67:     active = _active_timestamps(timestamps, cutoff)
    68: 
    69:     _log.debug("active=%d, limit=%d, cutoff=%s", len(active), limit, cutoff)
>>  70: 
>>  71:     if len(active) > limit:
    72:         return False, 0
    73:     return True, limit - len(active)
```

Fix at line 71: `if len(active) >= limit:`

## 44. `ttl_snapshot_store` — reviewer: Tạ Công Nam

Original label: line 69; relocated: line 68 (replace, 1 token(s)).

```
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

Fix at line 68: `if now >= effective:`

## 45. `upload_gate` — reviewer: Nguyễn Hoàng Hải

Original label: line 73; relocated: line 74 (replace, 1 token(s)).

```
    67:     _log.debug(
    68:         "upload_gate: %d active uploads in last %ds (limit=%d)",
    69:         len(active),
    70:         window,
    71:         limit,
    72:     )
>>  73: 
>>  74:     if len(active) > limit:
    75:         return False, 0
    76:     return True, limit - len(active)
```

Fix at line 74: `    if len(active) >= limit:`

## 46. `versions_stream` — reviewer: Đỗ Xuân Tráng

Original label: line 79; relocated: line 80 (replace, 1 token(s)).

```
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

Fix at line 80: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

