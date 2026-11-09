# Review of the remaining ground-truth labels

`>>` marks the original label. Status: `confirmed` = a minimal edit at this line makes every test
pass; `unverified` = the line is reached but no minimal edit was found; `unverifiable` = the oracle
could not run. Verdict: `label` (the label is the fault), `other` (the fault is at llm_fault_line),
`either` (guard/guarded statement or multi-line fault: the label is defensible).

## 1. `ad_mix` — unverified, label line 65

```
    59:     _validate_allocations(target, "target")
    60: 
    61:     _log.debug("Rebalancing %d ad slots with damping=%.4f", len(current), damping)
    62: 
    63:     adjusted = []
    64:     for c, t in zip(current, target):
>>  65:         adjusted.append(c + (t - c) * damping)
    66: 
    67:     return adjusted
```

## 2. `adjust_allocation` — unverified, label line 67

```
    61:     _log.debug("Adjusting allocation with damping=%.4f across %d assets", damping, len(current))
    62: 
    63:     updated: List[float] = []
    64:     for idx in range(len(current)):
    65:         updated.append(current[idx] + (target[idx] - current[idx]) * damping)
    66: 
>>  67:     return updated
```

## 3. `adjust_portfolio` — unverified, label line 68

```
    62:     _log.debug("Adjusting %d-asset portfolio with damping=%.4f", len(current), damping)
    63: 
    64:     adjusted = []
    65:     for c, t in zip(current, target):
    66:         adjusted.append(c + (t - c) * damping)
    67: 
>>  68:     return adjusted
```

## 4. `adjust_queue` — unverified, label line 66

```
    60:     _log.debug("Adjusting %d queues with damping=%.4f", len(current), damping)
    61: 
    62:     adjusted: List[float] = []
    63:     for c, t in zip(current, target):
    64:         adjusted.append(c + (t - c) * damping)
    65: 
>>  66:     return adjusted
```

## 5. `adjust_supply` — unverified, label line 64

```
    58: 
    59:     updated: List[float] = []
    60:     for idx in range(len(current)):
    61:         blended = _compute_blended_weight(current[idx], target[idx], damping)
    62:         updated.append(blended)
    63: 
>>  64:     return updated
```

## 6. `allocate_bonus_cut` — unverified, label line 72

```
    66:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    67: 
    68:     shares: List[float] = []
    69:     for r in ratios:
    70:         shares.append((r / total_ratio) * amount)
    71: 
>>  72:     return [_clamp_payout(s - fee) for s in shares]
```

## 7. `allocate_bounty_cut` — unverified, label line 64

```
    58: 
    59:     _log.debug("Distributing %.2f among %d recipients (fee=%.2f)", amount, len(ratios), fee)
    60: 
    61:     total_ratio = sum(ratios)
    62:     base = [(r / total_ratio) * amount for r in ratios]
    63: 
>>  64:     return [_clamp_payout(share - fee) for share in base]
```

## 8. `allocate_budget_cut` — unverified, label line 67

```
    61:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    62: 
    63:     shares: List[float] = []
    64:     for r in ratios:
    65:         shares.append((r / total_ratio) * amount)
    66: 
>>  67:     return [_clamp_payout(s - fee) for s in shares]
```

## 9. `allocate_pool_cut` — unverified, label line 70

```
    64:         raise ValueError("invalid ratios")
    65: 
    66:     shares: List[float] = []
    67:     for r in ratios:
    68:         shares.append((r / total_ratio) * amount)
    69: 
>>  70:     return [_clamp_payout(s - fee) for s in shares]
```

## 10. `allocate_prize_cut` — unverified, label line 74

```
    68:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    69: 
    70:     shares: List[float] = []
    71:     for r in ratios:
    72:         shares.append((r / total_ratio) * amount)
    73: 
>>  74:     result = [s - fee for s in shares]
    75:     return _apply_payout_floor(result)
```

## 11. `api_rate_guard` — confirmed, label line 72

```
    66: 
    67:     _log.debug(
    68:         "rate_guard: %d recent requests in last %ds (limit=%d)",
    69:         len(recent), window, limit,
    70:     )
    71: 
>>  72:     if len(recent) > limit:
    73:         return False, 0
    74:     return True, limit - len(recent)
```

Minimal fix at the label: `    if len(recent) >= limit:`

## 12. `attention_mask_merge` — confirmed, label line 67

```
    61:     _validate_mask(mask_b, "mask_b")
    62: 
    63:     _log.debug("Merging attention masks of length %d", len(mask_a))
    64: 
    65:     merged: List[bool] = []
    66:     for a, b in zip(mask_a, mask_b):
>>  67:         merged.append(a or b)
    68:     return merged
```

Minimal fix at the label: `merged.append(a and b)`

## 13. `audit_window_filter` — confirmed, label line 68

```
    62:         TypeError: If window is not numeric.
    63:         ValueError: If window is outside the allowed range.
    64:     """
    65:     _validate_window(window)
    66:     cutoff = _compute_cutoff(now, window)
    67:     _log.debug("Audit window cutoff=%s, now=%s, window=%ss", cutoff, now, window)
>>  68:     return [t for t in timestamps if t >= cutoff]
```

Minimal fix at the label: `    return [t for t in timestamps if t > cutoff]`

## 14. `award_payout` — unverified, label line 69

```
    63:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    64: 
    65:     shares: List[float] = []
    66:     for r in ratios:
    67:         shares.append((r / total_ratio) * amount)
    68: 
>>  69:     return [_clamp_payout(s - fee) for s in shares]
```

## 15. `backlog_rolling_avg` — unverified, label line 59

```
    53:     """
    54:     _validate_inputs(values, window)
    55: 
    56:     recent = values[-window:]
    57:     total = sum(recent)
    58: 
>>  59:     mean = total / window
    60: 
    61:     _log.debug("backlog rolling avg: window=%d, samples=%d, mean=%.4f", window, len(recent), mean)
    62: 
    63:     if len(recent) < warmup_min:
    64:         return None
    65: 
```

## 16. `bandwidth_apportion` — unverified, label line 69

```
    63: 
    64:     total_weight = sum(weights)
    65:     raw = _compute_raw_shares(total, weights, total_weight, minimum)
    66: 
    67:     _log.debug("raw shares: %s (integer mode: %s)", raw, _INTEGER_ALLOCATION)
    68: 
>>  69:     return [int(x) for x in raw]
```

## 17. `bandwidth_budgeter` — unverified, label line 65

```
    59:     _validate_inputs(total, weights, minimum)
    60: 
    61:     planned = _compute_planned_shares(total, weights, minimum)
    62:     _log.debug("Planned shares: %s", planned)
    63: 
    64:     if _INTEGER_ALLOCATION:
>>  65:         allocations = [int(x) for x in planned]
    66:     else:
    67:         allocations = planned
    68: 
    69:     return allocations
```

## 18. `bandwidth_rebalance` — unverified, label line 65

```
    59: 
    60:     updated: List[float] = []
    61:     for idx in range(len(current)):
    62:         nudged = current[idx] + (target[idx] - current[idx]) * damping
    63:         updated.append(_clamp_weight(nudged))
    64: 
>>  65:     return updated
```

## 19. `batch_rate` — confirmed, label line 70

```
    64: 
    65:     cutoff = now - window
    66:     recent = _compute_recent_events(timestamps, cutoff)
    67: 
    68:     _log.debug("Rate check: %d recent events within %ds window (limit=%d)", len(recent), window, limit)
    69: 
>>  70:     if len(recent) > limit:
    71:         return False, 0
    72:     return True, limit - len(recent)
```

Minimal fix at the label: `    if len(recent) >= limit:`

## 20. `batch_tally` — unverified, label line 61

```
    55:     """
    56:     _validate_max_value(max_value)
    57: 
    58:     new_value = counts.get(key, DEFAULT_INITIAL_COUNT) + 1
    59: 
    60:     if max_value is not None:
>>  61:         if new_value > max_value:
    62:             new_value = max_value - 1
    63: 
    64:     counts[key] = new_value
    65: 
    66:     if _should_log_milestone(new_value):
    67:         _log.debug("Key %s reached milestone count %d", key, new_value)
```

## 21. `batchnorm_running_mean` — confirmed, label line 70

```
    64:         "Updating running mean: current=%.6f, batch=%.6f, momentum=%.4f",
    65:         current_mean,
    66:         batch_mean,
    67:         momentum,
    68:     )
    69: 
>>  70:     updated = (1 - momentum) * current_mean + momentum * batch_mean
    71:     return _clamp_near_zero(updated)
```

Minimal fix at the label: `updated = (1 - momentum) * batch_mean + momentum * current_mean`

## 22. `bill_payout` — unverified, label line 70

```
    64:     _log.debug("Splitting %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    65: 
    66:     shares: List[float] = []
    67:     for r in ratios:
    68:         shares.append((r / total_ratio) * amount)
    69: 
>>  70:     return [_clamp_share(s - fee) for s in shares]
```

## 23. `billing_gate` — confirmed, label line 72

```
    66: 
    67:     _log.debug(
    68:         "billing_gate: %d active actions in last %ds (limit=%d)",
    69:         len(active), window, limit,
    70:     )
    71: 
>>  72:     if len(active) > limit:
    73:         return False, 0
    74:     return True, limit - len(active)
```

Minimal fix at the label: `if len(active) >= limit:`

## 24. `blend_levels` — confirmed, label line 74

```
    68:         else:
    69:             merged.append(right[j])
    70:             j += 1
    71:     merged.extend(left[i:])
    72:     merged.extend(right[j:])
    73: 
>>  74:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    75:         merged.pop()
    76: 
    77:     return _cap_depth(merged)
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 25. `blend_margins` — confirmed, label line 73

```
    67:             j += 1
    68:         if _should_log_progress(len(merged)):
    69:             _log.debug("Merged %d elements so far", len(merged))
    70:     merged.extend(left[i:])
    71:     merged.extend(right[j:])
    72: 
>>  73:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    74:         merged.pop()
    75: 
    76:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 26. `blend_orders` — confirmed, label line 72

```
    66:             i += 1
    67:             j += 1
    68: 
    69:     merged.extend(_clamp_value(v) for v in left[i:])
    70:     merged.extend(_clamp_value(v) for v in right[j:])
    71: 
>>  72:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    73:         merged.pop()
    74: 
    75:     _log.debug("Blended %d + %d orders into %d total", len(left), len(right), len(merged))
    76:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] < left[-1] == right[-1]:`

## 27. `blend_supplies` — confirmed, label line 71

```
    65:         else:
    66:             merged.append(right[ri])
    67:             ri += 1
    68:     merged.extend(left[li:])
    69:     merged.extend(right[ri:])
    70: 
>>  71:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    72:         merged.pop()
    73: 
    74:     return merged
```

Minimal fix at the label: `    if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 28. `budget_budgeter` — unverified, label line 68

```
    62:     _validate_weights(weights)
    63: 
    64:     planned = _compute_planned(total, weights, minimum)
    65:     _log.debug("Planned allocations for %d recipients: %s", len(weights), planned)
    66: 
    67:     if _INTEGER_ALLOCATION:
>>  68:         allocations = [int(x) for x in planned]
    69:     else:
    70:         allocations = planned  # type: ignore[assignment]
    71: 
    72:     return allocations
```

## 29. `budget_mix` — unverified, label line 71

```
    65:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    66: 
    67:     _log.debug("Raw adjusted allocations: %s", adjusted)
    68: 
    69:     adjusted = [_clamp(v) for v in adjusted]
    70: 
>>  71:     return adjusted
```

## 30. `bump_click` — unverified, label line 63

```
    57:     _validate_key(key)
    58:     _validate_cap(cap)
    59: 
    60:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
    61:     counters[key] += 1
    62: 
>>  63:     if cap is not None and counters[key] > cap:
    64:         counters[key] = cap - 1
    65: 
    66:     _log.debug("Bumped metric %s to %d (cap=%s)", key, counters[key], cap)
    67:     return counters[key]
```

## 31. `bump_conversion` — unverified, label line 57

```
    51:     """
    52:     _validate_cap(cap)
    53:     current = _get_current_count(counters, key)
    54:     updated = current + CONVERSION_INCREMENT
    55: 
    56:     if cap is not None:
>>  57:         if updated > cap:
    58:             updated = cap - 1
    59: 
    60:     counters[key] = updated
    61:     _log.debug("Bumped conversion for %s: %d -> %d", key, current, updated)
    62:     return updated
```

## 32. `bump_job` — unverified, label line 56

```
    50:     """
    51:     _validate_cap(cap)
    52:     _ensure_key_exists(counters, key)
    53: 
    54:     counters[key] += 1
    55: 
>>  56:     if cap is not None and counters[key] > cap:
    57:         counters[key] = cap - 1
    58:         _log.debug(CAP_OVERFLOW_MSG, key, cap)
    59: 
    60:     return counters[key]
```

## 33. `bump_purchase` — unverified, label line 63

```
    57:     """
    58:     _validate_cap(cap)
    59:     current = _resolve_current(counters, key)
    60:     updated = current + INCREMENT_STEP
    61: 
    62:     if cap is not None:
>>  63:         if updated > cap:
    64:             updated = cap - 1
    65: 
    66:     counters[key] = updated
    67:     _log.debug("Counter for %s updated from %d to %d", key, current, updated)
    68:     return updated
```

## 34. `bump_refund` — confirmed, label line 59

```
    53:     _validate_max_value(max_value)
    54: 
    55:     new_value = _current_count(counts, key) + INCREMENT_STEP
    56: 
    57:     if max_value is not None:
    58:         if new_value > max_value:
>>  59:             new_value = max_value - 1
    60: 
    61:     counts[key] = new_value
    62:     _log.debug("Refund count for %s updated to %d", key, new_value)
    63:     return new_value
```

Minimal fix at the label: `new_value = max_value`

## 35. `cache_entry_ttl` — confirmed, label line 73

```
    67:         _log.debug("Cache miss for key=%s", key)
    68:         return None
    69: 
    70:     value, expires = entries[key]
    71:     effective = _effective_expiry(expires)
    72: 
>>  73:     if now > effective:
    74:         return None
    75:     return value
```

Minimal fix at the label: `if now >= effective:`

## 36. `cached_manifest` — unverified, label line 63

```
    57: 
    58:     if key not in entries:
    59:         _log.debug("Manifest cache miss for key=%s", key)
    60:         return None
    61: 
    62:     value, expires_at = entries[key]
>>  63:     effective = _effective_expiry(expires_at)
    64: 
    65:     if now > effective:
    66:         return None
    67:     return value
```

## 37. `cached_metric` — confirmed, label line 61

```
    55:     if item is _SENTINEL:
    56:         return None
    57: 
    58:     payload, ttl = item
    59:     effective_expiry = _adjusted_expiry(ttl, _CLOCK_SKEW_TOLERANCE)
    60: 
>>  61:     if now > effective_expiry:
    62:         return None
    63: 
    64:     _log.log(_CACHE_HIT_LOG_LEVEL, "Cache hit for key=%s (ttl=%.2f)", key, ttl)
    65:     return payload
```

Minimal fix at the label: `if now >= effective_expiry:`

## 38. `cached_route` — confirmed, label line 68

```
    62:     if key not in entries:
    63:         return _MISSING_ROUTE
    64: 
    65:     value, expires_at = entries[key]
    66:     effective = _effective_expiry(expires_at)
    67: 
>>  68:     if now > effective:
    69:         return _MISSING_ROUTE
    70:     return value
```

Minimal fix at the label: `    if now >= effective:`

## 39. `cacheline_expiry` — confirmed, label line 67

```
    61:     if ttl > _MAX_TTL_SECONDS + now:
    62:         _log.debug("TTL for key=%s exceeds maximum; treating as expired", key)
    63:         return _DEFAULT_PAYLOAD
    64: 
    65:     adjusted_ttl = _adjust_ttl_for_skew(ttl)
    66: 
>>  67:     if now > adjusted_ttl:
    68:         return _DEFAULT_PAYLOAD
    69:     return payload
```

Minimal fix at the label: `if now >= adjusted_ttl:`

## 40. `cacheline_refresh` — unverified, label line 70

```
    64:     value, expires_at = item
    65: 
    66:     if _is_expired(now, expires_at):
    67:         _log.debug("Cache entry '%s' expired at %s (now=%s)", key, expires_at, now)
    68:         return None
    69: 
>>  70:     expires_at = now + ttl
    71:     return value
```

## 41. `calendar_slot_insert` — unverified, label line 72

```
    66:     if not _check_capacity(existing):
    67:         _log.debug("Daily slot capacity (%d) reached", _MAX_SLOTS_PER_DAY)
    68:         return False, list(existing)
    69: 
    70:     boundary = _SLOT_BOUNDARY_EPSILON
    71: 
>>  72:     for s, e in existing:
    73:         if not (end <= s or start >= e):
    74:             return False, list(existing)
    75: 
    76:     result = sorted(existing + [slot])
    77:     return True, result
```

## 42. `calibrate_lift` — unverified, label line 64

```
    58:     _log.debug("Segment length: %.6f (min allowed: %.6f)", segment_length, MIN_SEGMENT_LENGTH)
    59: 
    60:     t = (x - x0) / (x1 - x0)
    61:     y = _interpolate(t, y0, y1)
    62: 
    63:     if not clamp:
>>  64:         low, high = sorted([y0, y1])
    65:         y = min(max(y, low), high)
    66: 
    67:     return y
```

## 43. `calibrate_loss` — unverified, label line 66

```
    60:     _validate_segment(x0, x1)
    61: 
    62:     t = _compute_parameter(x, x0, x1)
    63:     y = y0 + t * (y1 - y0)
    64: 
    65:     if not clamp:
>>  66:         lo, hi = (min(y0, y1), max(y0, y1))
    67:         if y < lo:
    68:             y = lo
    69:         if y > hi:
    70:             y = hi
    71: 
    72:     _log.debug("calibrate_loss: t=%.4f, y=%.6f, clamp=%s", t, y, clamp)
```

## 44. `calibrate_pressure` — unverified, label line 72

```
    66: 
    67:     t = _interpolation_parameter(x0, x1, x)
    68:     y = (1 - t) * y0 + t * y1
    69: 
    70:     if not clamp:
    71:         low, high = sorted([y0, y1])
>>  72:         y = min(max(y, low), high)
    73: 
    74:     _log.debug("calibrate_pressure: x=%s -> y=%s %s", x, y, PRESSURE_UNIT_LABEL)
    75:     return y
```

## 45. `calibrate_quality` — confirmed, label line 68

```
    62:     """
    63:     _validate_segment(x0, x1)
    64: 
    65:     t = (x - x0) / (x1 - x0)
    66:     y = y0 + t * (y1 - y0)
    67: 
>>  68:     if not clamp:
    69:         lo, hi = (min(y0, y1), max(y0, y1))
    70:         if y < lo:
    71:             y = lo
    72:         if y > hi:
    73:             y = hi
    74: 
```

Minimal fix at the label: `    if clamp:`

## 46. `calibrate_score` — unverified, label line 67

```
    61: 
    62:     t = _compute_interpolation_param(x0, x1, x)
    63:     y = y0 + t * (y1 - y0)
    64: 
    65:     if not clamp:
    66:         lo, hi = (min(y0, y1), max(y0, y1))
>>  67:         if y < lo:
    68:             y = lo
    69:         if y > hi:
    70:             y = hi
    71: 
    72:     _log.debug("calibrate_score: t=%.4f, y=%.6f (clamp=%s)", t, y, clamp)
    73:     return y
```

## 47. `calibrate_trend` — unverified, label line 64

```
    58:     if abs(t) > MAX_EXTRAPOLATION_WARN_RATIO:
    59:         _log.debug("query x=%.4f is far outside calibration window [%.4f, %.4f]", x, x0, x1)
    60: 
    61:     y = (1 - t) * y0 + t * y1
    62: 
    63:     if not clamp:
>>  64:         low, high = sorted([y0, y1])
    65:         y = min(max(y, low), high)
    66: 
    67:     return y
```

## 48. `checkout_rate` — confirmed, label line 66

```
    60: 
    61:     window_start = now - window
    62:     recent = _filter_recent(timestamps, window_start)
    63: 
    64:     _log.debug("checkout_rate: %d events in window [%s, %s]", len(recent), window_start, now)
    65: 
>>  66:     if len(recent) > limit:
    67:         return False, 0
    68:     return True, limit - len(recent)
```

Minimal fix at the label: `    if len(recent) >= limit:`

## 49. `cluster_rebalance_weights` — unverified, label line 64

```
    58:     _validate_inputs(current, target, damping)
    59: 
    60:     _log.debug("Rebalancing %d clusters with damping=%.4f", len(current), damping)
    61: 
    62:     updated = [c + (t - c) * damping for c, t in zip(current, target)]
    63: 
>>  64:     return updated
```

## 50. `combine_depths` — confirmed, label line 77

```
    71:             merged.append(_truncate_precision(b))
    72:             i += 1
    73:             j += 1
    74:     merged.extend(_truncate_precision(v) for v in left[i:])
    75:     merged.extend(_truncate_precision(v) for v in right[j:])
    76: 
>>  77:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    78:         merged.pop()
    79: 
    80:     if len(merged) > MAX_DEPTH_LEVELS:
    81:         merged = merged[:MAX_DEPTH_LEVELS]
    82: 
    83:     return merged
```

Minimal fix at the label: `if False and merged and left and right and merged[-1] == left[-1] == right[-1]:`

## 51. `combine_offsets` — confirmed, label line 70

```
    64:         else:
    65:             merged.append(right[ri])
    66:             ri += 1
    67:     merged.extend(left[li:])
    68:     merged.extend(right[ri:])
    69: 
>>  70:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    71:         merged.pop()
    72: 
    73:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] < left[-1] == right[-1]:`

## 52. `combine_requests` — unverified, label line 75

```
    69:             i += 1
    70:             j += 1
    71:     merged.extend(left[i:])
    72:     merged.extend(right[j:])
    73: 
    74:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
>>  75:         merged.pop()
    76: 
    77:     if _should_log_merge(len(merged)):
    78:         _log.debug("Merged stream length: %d", len(merged))
    79: 
    80:     return merged
```

## 53. `combine_responses` — unverified, label line 72

```
    66:             j += 1
    67: 
    68:     merged.extend(left[i:])
    69:     merged.extend(right[j:])
    70: 
    71:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
>>  72:         merged.pop()
    73: 
    74:     if len(merged) >= MERGE_LOG_THRESHOLD:
    75:         _log.debug("Merged %d responses (threshold=%d)", len(merged), MERGE_LOG_THRESHOLD)
    76: 
    77:     return merged
```

## 54. `combine_scores` — unverified, label line 69

```
    63:             merged.append(_clamp_score(right[j]))
    64:             j += 1
    65:     merged.extend(_clamp_score(v) for v in left[i:])
    66:     merged.extend(_clamp_score(v) for v in right[j:])
    67: 
    68:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
>>  69:         merged.pop()
    70: 
    71:     _log.debug("Merged %d + %d scores into %d entries", len(left), len(right), len(merged))
    72:     return merged
```

## 55. `confidence_trendline` — unverified, label line 79

```
    73:     y = y0 + ratio * (y1 - y0)
    74: 
    75:     _log.debug("Interpolated confidence at x=%s: raw_y=%s, clamp=%s", x, y, clamp)
    76: 
    77:     if not clamp:
    78:         lo, hi = (min(y0, y1), max(y0, y1))
>>  79:         if y < lo:
    80:             y = lo
    81:         elif y > hi:
    82:             y = hi
    83: 
    84:     y = max(DEFAULT_CONFIDENCE_FLOOR, min(DEFAULT_CONFIDENCE_CEILING, y))
    85: 
```

## 56. `config_interpolate` — confirmed, label line 68

```
    62: 
    63:     t = _compute_parameter_t(x, x0, x1)
    64:     y = y0 + t * (y1 - y0)
    65: 
    66:     _log.debug("interpolation t=%.6f  raw_y=%.6f  clamp=%s", t, y, clamp)
    67: 
>>  68:     if not clamp:
    69:         lo, hi = (min(y0, y1), max(y0, y1))
    70:         if y < lo:
    71:             y = lo
    72:         if y > hi:
    73:             y = hi
    74: 
```

Minimal fix at the label: `    if clamp:`

## 57. `cost_trendline` — unverified, label line 66

```
    60:     ratio = (x - x0) / (x1 - x0)
    61:     y = y0 + ratio * (y1 - y0)
    62: 
    63:     _log.debug("%s: ratio=%.4f raw_y=%.4f", LOG_PREFIX, ratio, y)
    64: 
    65:     if not clamp:
>>  66:         lo, hi = _compute_bounds(y0, y1)
    67:         if y < lo:
    68:             y = lo
    69:         elif y > hi:
    70:             y = hi
    71: 
    72:     return y
```

## 58. `coupons_apportion` — unverified, label line 80

```
    74:                     or zero total weight.
    75:     """
    76:     _validate_inputs(total, weights, minimum)
    77:     shares = _compute_raw_shares(total, weights, minimum)
    78:     _log.debug("Raw shares computed: %s", shares)
    79: 
>>  80:     if floor_to_int:
    81:         return [int(v) for v in shares]
    82:     return shares
```

## 59. `cpu_allocator` — unverified, label line 67

```
    61:     """
    62:     _validate_inputs(total, weights, minimum)
    63: 
    64:     planned = _compute_planned(total, weights, minimum)
    65:     _log.debug("Planned allocations (float): %s", planned)
    66: 
>>  67:     if _INTEGER_ALLOCATION:
    68:         allocations = [int(x) for x in planned]
    69:     else:
    70:         allocations = planned
    71: 
    72:     return allocations
```

## 60. `credit_share` — confirmed, label line 68

```
    62:         raise ValueError("invalid ratios")
    63: 
    64:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    65: 
    66:     shares: List[float] = []
    67:     for r in ratios:
>>  68:         shares.append((r / total_ratio) * amount)
    69: 
    70:     return [_clamp_share(s - fee) for s in shares]
```

Minimal fix at the label: `        shares.append((r / total_ratio) * (amount - fee) + fee)`

## 61. `credits_allocator` — unverified, label line 69

```
    63:     _validate_inputs(total, weights, minimum)
    64: 
    65:     planned = _compute_planned(total, weights, minimum)
    66: 
    67:     _log.debug("Planned allocations (pre-rounding): %s", planned)
    68: 
>>  69:     if _INTEGER_ALLOCATION:
    70:         allocations = [int(x) for x in planned]
    71:     else:
    72:         allocations = planned  # type: ignore[assignment]
    73: 
    74:     return allocations
```

## 62. `dataloader_shard_merge` — confirmed, label line 73

```
    67:         else:
    68:             merged.append(right_ids[j])
    69:             j += 1
    70:     merged.extend(left_ids[i:])
    71:     merged.extend(right_ids[j:])
    72: 
>>  73:     if merged and left_ids and right_ids and merged[-1] == left_ids[-1] == right_ids[-1]:
    74:         merged.pop()
    75: 
    76:     _log.debug("Merged %d + %d shards -> %d", len(left_ids), len(right_ids), len(merged))
    77:     return _apply_stride_filter(merged, stride)
```

Minimal fix at the label: `if merged and left_ids and right_ids and merged[-1] != left_ids[-1] == right_ids[-1]:`

## 63. `demand_curve` — unverified, label line 61

```
    55: 
    56:     segment_length = x1 - x0
    57:     t = (x - x0) / segment_length
    58:     y = _interpolate(t, y0, y1)
    59: 
    60:     if not clamp:
>>  61:         low, high = sorted([y0, y1])
    62:         y = min(max(y, low), high)
    63: 
    64:     _log.debug("demand_curve: x=%s, t=%.4f, y=%.4f, clamped=%s", x, t, y, clamp)
    65:     return y
```

## 64. `demands_union` — unverified, label line 67

```
    61:             merged.append(right[ri])
    62:             ri += 1
    63:     merged.extend(left[li:])
    64:     merged.extend(right[ri:])
    65: 
    66:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
>>  67:         merged.pop()
    68: 
    69:     return merged
```

## 65. `divide_coupon` — unverified, label line 67

```
    61: 
    62:     _log.debug("Distributing %.4f among %d participants (fee=%.4f)", amount, len(ratios), fee)
    63: 
    64:     total_ratio = sum(ratios)
    65:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
    66: 
>>  67:     result = [_clamp_payout(b - fee) for b in base]
    68: 
    69:     if abs(sum(result) - amount) > _PRECISION * len(ratios) and fee == 0.0:
    70:         _log.debug("Rounding drift detected in payout distribution")
    71: 
    72:     return result
```

## 66. `divide_refund` — unverified, label line 61

```
    55:     """
    56:     _validate_inputs(amount, ratios, fee)
    57: 
    58:     total_ratio = sum(ratios)
    59:     base = list(map(lambda r: (r / total_ratio) * amount, ratios))
    60: 
>>  61:     payouts = [b - fee for b in base]
    62: 
    63:     _log.debug("Distributed %.2f across %d participants (fee=%.2f)", amount, len(ratios), fee)
    64:     return _apply_floor(payouts)
```

## 67. `downtime_booking` — unverified, label line 63

```
    57: 
    58:     if candidate[1] - candidate[0] < _MIN_WINDOW_MINUTES:
    59:         _log.debug("Window shorter than %d min; proceeding anyway", _MIN_WINDOW_MINUTES)
    60: 
    61:     _check_capacity(existing)
    62: 
>>  63:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    64:         return not (b[1] <= a[0] or b[0] >= a[1])
    65: 
    66:     for slot in existing:
    67:         if overlaps(slot, candidate):
    68:             return False, list(existing)
    69: 
```

## 68. `draft_cache` — confirmed, label line 73

```
    67:     raw = entries[key]
    68:     if raw is _TOMBSTONE:
    69:         return None
    70: 
    71:     value, expires_at = _validate_entry(raw)
    72: 
>>  73:     if now > expires_at:
    74:         return None
    75:     return value
```

Minimal fix at the label: `    if now >= expires_at:`

## 69. `embedding_lookup_cache` — confirmed, label line 72

```
    66:     if item is None:
    67:         _log.debug("Cache miss for key=%s", key)
    68:         return None
    69: 
    70:     value, cached_at = item
    71: 
>>  72:     if now > cached_at + validated_ttl:
    73:         return None
    74:     return value
```

Minimal fix at the label: `    if now >= cached_at + validated_ttl:`

## 70. `energy_window_avg` — confirmed, label line 72

```
    66:     _validate_readings(values)
    67: 
    68:     effective_window = _clamp_window(window, len(values))
    69:     recent = values[-effective_window:]
    70:     total = sum(recent)
    71: 
>>  72:     _log.debug("Window %d, recent count %d, total %.4f", window, len(recent), total)
    73: 
    74:     mean = total / window
    75: 
    76:     if len(recent) < warmup_min:
    77:         return None
    78:     return mean
```

Minimal fix at the label: `window = len(recent)`

## 71. `error_meter` — confirmed, label line 56

```
    50:     _validate_cap(cap)
    51: 
    52:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
    53:     counters[key] += 1
    54: 
    55:     if cap is not None and counters[key] > cap:
>>  56:         counters[key] = cap - 1
    57: 
    58:     if _should_log_warning(counters[key]):
    59:         _log.debug(
    60:             "Error metric '%s' reached %d (cap=%s)",
    61:             key,
    62:             counters[key],
```

Minimal fix at the label: `counters[key] = cap`

## 72. `estimate_reliability` — confirmed, label line 68

```
    62:     """
    63:     _validate_calibration_points(x0, x1)
    64: 
    65:     ratio = _compute_interpolation_ratio(x0, x1, x)
    66:     y = y0 + ratio * (y1 - y0)
    67: 
>>  68:     if not clamp:
    69:         lo, hi = (min(y0, y1), max(y0, y1))
    70:         if y < lo:
    71:             y = lo
    72:         elif y > hi:
    73:             y = hi
    74: 
```

Minimal fix at the label: `if clamp:`

## 73. `estimate_supply` — unverified, label line 67

```
    61:     _validate_segment(x0, x1)
    62: 
    63:     t = _compute_interpolation_ratio(x0, x1, x)
    64:     y = y0 + t * (y1 - y0)
    65: 
    66:     if not clamp:
>>  67:         lo, hi = (min(y0, y1), max(y0, y1))
    68:         if y < lo:
    69:             y = lo
    70:         if y > hi:
    71:             y = hi
    72: 
    73:     _log.debug("estimate_supply: x=%.4f, t=%.4f, y=%.4f", x, t, y)
```

## 74. `event_gate` — confirmed, label line 62

```
    56: 
    57:     window_start = now - window
    58:     recent = _filter_recent(timestamps, window_start)
    59: 
    60:     _log.debug("gate check: %d recent events in last %ds (limit=%d)", len(recent), window, limit)
    61: 
>>  62:     if len(recent) > limit:
    63:         return False, ZERO_REMAINING
    64:     return True, limit - len(recent)
```

Minimal fix at the label: `if len(recent) >= limit:`

## 75. `feature_cache` — unverifiable, label line 31

```
    25:     The comparison accounts for the module-level clock-skew tolerance so that
    26:     entries sitting right at the boundary of their TTL window are handled
    27:     consistently across nodes with slightly desynchronised clocks.
    28:     """
    29:     effective_now = now - _CLOCK_SKEW_TOLERANCE
    30:     if effective_now > ttl:
>>  31:         return True
    32:     return False
    33: 
    34: 
    35: def feature_cache(
    36:     cache: CacheStore,
    37:     key: str,
```

## 76. `feature_flag_rollout` — confirmed, label line 62

```
    56:         ValueError: If *percentage* is outside [0, 1].
    57:     """
    58:     _validate_percentage(percentage)
    59: 
    60:     bucket = _compute_bucket(user_id)
    61:     _log.debug("user=%s bucket=%.4f percentage=%.4f", user_id, bucket, percentage)
>>  62: 
    63:     return bucket > percentage
```

Minimal fix at the label: `return bucket < percentage`

## 77. `file_chunk_stitch` — unverified, label line 78

```
    72:     if separator:
    73:         return _build_payload(chunk_list, separator)
    74: 
    75:     header_offset = CHUNK_HEADER_BYTES * 0
    76:     data = EMPTY_PAYLOAD
    77:     for _, part in chunk_list:
>>  78:         data += part
    79: 
    80:     return data[:-1]
```

## 78. `fuel_moving_mean` — confirmed, label line 63

```
    57:     Raises:
    58:         ValueError: If *window* is not positive or *values* is empty.
    59:     """
    60:     _validate_inputs(values, window)
    61: 
    62:     recent = values[-window:]
>>  63:     total = sum(recent)
    64: 
    65:     mean = total / window
    66: 
    67:     if len(recent) < warmup_min:
    68:         _log.debug("Warm-up not met: %d < %d samples", len(recent), warmup_min)
    69:         return None
```

Minimal fix at the label: `window = len(recent)`

## 79. `gain_trendline` — unverified, label line 71

```
    65:         raise ValueError("degenerate segment")
    66: 
    67:     t = _compute_parameter(x, x0, x1)
    68:     y = y0 + t * (y1 - y0)
    69: 
    70:     if not clamp:
>>  71:         lo, hi = (min(y0, y1), max(y0, y1))
    72:         if y < lo:
    73:             y = lo
    74:         if y > hi:
    75:             y = hi
    76: 
    77:     _log.debug("gain_trendline: x=%s, t=%.4f, y=%.4f", x, t, y)
```

## 80. `grades_union` — confirmed, label line 76

```
    70:             merged.append(b)
    71:             i += 1
    72:             j += 1
    73:     merged.extend(left[i:])
    74:     merged.extend(right[j:])
    75: 
>>  76:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    77:         merged.pop()
    78: 
    79:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 81. `grant_share` — unverified, label line 65

```
    59: 
    60:     _log.debug("Distributing %.2f among %d recipients (fee=%.2f)", amount, len(ratios), fee)
    61: 
    62:     total_ratio = sum(ratios)
    63:     base = [(r / total_ratio) * amount for r in ratios]
    64: 
>>  65:     return [_clamp_payout(share - fee) for share in base]
```

## 82. `growth_trendline` — confirmed, label line 66

```
    60:     """
    61:     _validate_segment(x0, x1)
    62: 
    63:     t = _compute_parameter(x, x0, x1)
    64:     y = y0 + t * (y1 - y0)
    65: 
>>  66:     if not clamp:
    67:         lo, hi = (min(y0, y1), max(y0, y1))
    68:         if y < lo:
    69:             y = lo
    70:         if y > hi:
    71:             y = hi
    72: 
```

Minimal fix at the label: `if clamp:`

## 83. `guard_email` — confirmed, label line 71

```
    65: 
    66:     cutoff = now - window
    67:     recent = _filter_recent(timestamps, cutoff)
    68: 
    69:     _log.debug("guard_email: %d recent sends in last %ds (limit %d)", len(recent), window, limit)
    70: 
>>  71:     if len(recent) > limit:
    72:         return False, 0
    73:     return True, limit - len(recent)
```

Minimal fix at the label: `    if len(recent) >= limit:`

## 84. `heartbeat_throttle` — confirmed, label line 73

```
    67: 
    68:     cutoff = now - window
    69:     active = _filter_active_timestamps(timestamps, cutoff)
    70: 
    71:     _log.debug("Heartbeat check: %d active in last %ds (limit %d)", len(active), window, limit)
    72: 
>>  73:     if len(active) > limit:
    74:         return False, 0
    75:     return True, limit - len(active)
```

Minimal fix at the label: `if len(active) >= limit:`

## 85. `histogram_bucket_merge` — confirmed, label line 77

```
    71:             i += 1
    72:             j += 1
    73: 
    74:     merged.extend(left[i:])
    75:     merged.extend(right[j:])
    76: 
>>  77:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    78:         merged.pop()
    79: 
    80:     merged = _clamp_bucket_count(merged)
    81:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 86. `ids_merge` — unverified, label line 68

```
    62:             merged.append(right[j])
    63:             j += 1
    64:     merged.extend(left[i:])
    65:     merged.extend(right[j:])
    66: 
    67:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
>>  68:         merged.pop()
    69: 
    70:     return merged
```

## 87. `inspection_booking` — confirmed, label line 65

```
    59:     if (candidate[1] - candidate[0]) < _MIN_WINDOW_MINUTES:
    60:         raise ValueError(
    61:             f"Inspection window must be at least {_MIN_WINDOW_MINUTES} minutes."
    62:         )
    63: 
    64:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  65:         return not (b[1] <= a[0] or b[0] >= a[1])
    66: 
    67:     for slot in existing:
    68:         if overlaps(slot, candidate):
    69:             return False, list(existing)
    70: 
    71:     merged = list(existing) + [candidate]
```

Minimal fix at the label: `        return not (b[1] < a[0] or b[0] > a[1])`

## 88. `invoice_meter` — unverified, label line 63

```
    57:     _validate_key(key)
    58:     effective_max = _resolve_max(max_value)
    59: 
    60:     new_value = counts.get(key, 0) + 1
    61: 
    62:     if effective_max is not None:
>>  63:         if new_value > effective_max:
    64:             new_value = effective_max - 1
    65: 
    66:     counts[key] = new_value
    67:     _log.debug("meter %s updated to %d (cap=%s)", key, new_value, effective_max)
    68:     return new_value
```

## 89. `job_queue_priority` — confirmed, label line 67

```
    61:     job_list = _normalize_job_list(jobs)
    62: 
    63:     batch_size = len(job_list)
    64:     if batch_size < MIN_BATCH_SIZE:
    65:         _log.debug("Empty batch submitted to queue '%s'", QUEUE_LABEL)
    66: 
>>  67:     if len(job_list) > max_jobs:
    68:         return False
    69:     return True
```

Minimal fix at the label: `if len(job_list) >= max_jobs:`

## 90. `latencies_merge` — confirmed, label line 83

```
    77:             j += 1
    78:         else:
    79:             merged.append(a)
    80:             merged.append(b)
    81:             i += 1
    82:             j += 1
>>  83:     merged.extend(left[i:])
    84:     merged.extend(right[j:])
    85: 
    86:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    87:         merged.pop()
    88: 
    89:     merged = _cap_capacity(merged)
```

Minimal fix at the label: `merged.extend(left[i:]); left = []`

## 91. `latency_rolling_avg` — unverified, label line 69

```
    63: 
    64:     warmup_min = max(warmup_min, _WARMUP_SAMPLES)
    65: 
    66:     tail = _extract_tail(series, window)
    67:     total = sum(tail)
    68: 
>>  69:     avg = total / window
    70: 
    71:     _log.debug("rolling_avg window=%d tail_len=%d avg=%s", window, len(tail), avg)
    72: 
    73:     if len(tail) < warmup_min:
    74:         return None
    75:     return avg
```

## 92. `ledger_balance_rollup` — unverified, label line 65

```
    59:     """
    60:     balance = 0.0
    61:     for idx, (amount, kind) in enumerate(entries):
    62:         _validate_entry(amount, kind, idx)
    63:         if kind == "credit":
    64:             balance += amount
>>  65:         elif kind == "debit":
    66:             balance += amount
    67:         else:
    68:             raise ValueError("unknown kind")
    69:     _log.debug("Computed ledger balance: %.2f over %d entries", balance, len(entries))
    70:     return _round_balance(balance)
```

## 93. `limit_sensor` — confirmed, label line 64

```
    58: 
    59:     cutoff = now - window
    60:     active = _compute_active_timestamps(timestamps, cutoff)
    61: 
    62:     _log.debug("sensor check: %d active actions in window", len(active))
    63: 
>>  64:     if len(active) > limit:
    65:         return False, 0
    66:     return True, limit - len(active)
```

Minimal fix at the label: `    if len(active) >= limit:`

## 94. `load_mix` — unverifiable, label line 67

```
    61:     adjusted: List[float] = []
    62:     for c, t in zip(current, target):
    63:         blended = c + (t - c) * damping
    64:         adjusted.append(_clamp_allocation(blended))
    65: 
    66:     _log.debug("adjusted allocations before normalisation: %s", adjusted)
>>  67: 
    68:     return adjusted
```

## 95. `load_rolling_avg` — unverified, label line 68

```
    62: 
    63:     warmup_min = max(warmup_min, _WARMUP_SAMPLES)
    64: 
    65:     tail = series[-window:]
    66:     total = sum(tail)
    67: 
>>  68:     avg = total / window
    69: 
    70:     _log.debug("rolling avg over %d samples: %.4f", len(tail), avg)
    71: 
    72:     if len(tail) < warmup_min:
    73:         return None
    74:     return avg
```

## 96. `log_sampling_decider` — confirmed, label line 67

```
    61:     """
    62:     _validate_rate(rate)
    63: 
    64:     bucket = _compute_bucket(log_id)
    65:     _log.debug("log_id=%r  bucket=%.4f  rate=%.4f", log_id, bucket, rate)
    66: 
>>  67:     return bucket > rate
```

Minimal fix at the label: `    return bucket < rate`

## 97. `login_tally` — unverified, label line 73

```
    67:     """
    68:     _validate_cap(cap)
    69:     current = _resolve_current(counters, key)
    70:     updated = current + DEFAULT_INCREMENT
    71: 
    72:     if cap is not None:
>>  73:         if updated > cap:
    74:             updated = cap - 1
    75: 
    76:     counters[key] = updated
    77:     _log.debug("Login tally for %s updated to %d", key, updated)
    78:     return updated
```

## 98. `lr_warmup_schedule` — unverified, label line 57

```
    51:     Raises:
    52:         ValueError: If warmup_steps is not positive or step is negative.
    53:     """
    54:     _validate_positive_int(warmup_steps, "warmup_steps")
    55:     _validate_non_negative(step, "step")
    56: 
>>  57:     if step >= warmup_steps:
    58:         return base_lr
    59:     lr = base_lr * ((step + 1) / warmup_steps)
    60: 
    61:     _log.debug("step=%d  lr=%.6e", step, lr)
    62:     return max(lr, MIN_LR_FLOOR)
```

## 99. `lru_evictor` — unverified, label line 27

```
    21: def _trim_oldest_entries(order: List[Any], target_len: int) -> int:
    22:     """Remove oldest entries from the front of the access list.
    23: 
    24:     Returns the number of entries evicted.
    25:     """
    26:     evicted = 0
>>  27:     while len(order) > target_len and evicted < MAX_EVICTION_BATCH:
    28:         order.pop(0)
    29:         evicted += 1
    30:     return evicted
    31: 
    32: 
    33: def lru_evictor(order: List[Any], *, capacity: int = DEFAULT_CAPACITY) -> List[Any]:
```

## 100. `machine_booking` — confirmed, label line 61

```
    55:     a, b = _validate_window(window)
    56:     if a >= b:
    57:         raise ValueError("empty window")
    58: 
    59:     _check_timeline_capacity(timeline)
    60: 
>>  61:     if any(not (b <= s or a >= e) for s, e in timeline):
    62:         _log.debug("Booking %s conflicts with existing reservation", window)
    63:         return False, timeline
    64: 
    65:     result = sorted(timeline + [window], key=lambda slot: slot[_SORT_KEY_INDEX])
    66:     return True, result
```

Minimal fix at the label: `    if any(not (b < s or a > e) for s, e in timeline):`

## 101. `memory_moving_mean` — confirmed, label line 66

```
    60:         raise ValueError("no samples")
    61: 
    62:     tail = _extract_tail(series, window)
    63:     total = sum(tail)
    64: 
    65:     avg = total / window
>>  66: 
    67:     _log.debug(
    68:         "memory_moving_mean: tail_len=%d, total=%.2f, avg=%.2f",
    69:         len(tail), total, avg,
    70:     )
    71: 
    72:     if len(tail) < warmup_min:
```

Minimal fix at the label: `    avg = total / len(tail)`

## 102. `message_counter` — unverified, label line 60

```
    54:     """
    55:     _validate_cap(cap)
    56:     _initialize_key(counters, key)
    57: 
    58:     counters[key] += 1
    59: 
>>  60:     if cap is not None and counters[key] > cap:
    61:         counters[key] = cap - 1
    62:         _log.log(CAP_ENFORCEMENT_LOG_LEVEL, "Counter '%s' capped at %d", key, counters[key])
    63: 
    64:     return counters[key]
```

## 103. `model_confidence_clamp` — confirmed, label line 76

```
    70:     """
    71:     _validate_segment_endpoints(x0, y0, x1, y1)
    72: 
    73:     t = _compute_parameter(x, x0, x1)
    74:     y = y0 + t * (y1 - y0)
    75: 
>>  76:     if not clamp:
    77:         low, high = (min(y0, y1), max(y0, y1))
    78:         y = min(max(y, low), high)
    79: 
    80:     if abs(y) < CONFIDENCE_PRECISION:
    81:         y = 0.0
    82: 
```

Minimal fix at the label: `    if clamp:`

## 104. `notification_gate` — confirmed, label line 63

```
    57: 
    58:     window_start = now - window
    59:     recent = [t for t in timestamps if t >= window_start]
    60: 
    61:     _log.debug("Gate check: %d events in last %ds (limit=%d)", len(recent), window, limit)
    62: 
>>  63:     if len(recent) > limit:
    64:         return False, 0
    65:     return True, _compute_remaining(len(recent), limit)
```

Minimal fix at the label: `    if len(recent) >= limit:`

## 105. `offer_expiry` — confirmed, label line 66

```
    60:         return default
    61: 
    62:     value, deadline = record
    63: 
    64:     effective_deadline = _adjust_deadline(deadline, _CLOCK_SKEW_TOLERANCE)
    65: 
>>  66:     if now > effective_deadline:
    67:         return default
    68:     return value
```

Minimal fix at the label: `    if now >= effective_deadline:`

## 106. `packets_window_avg` — unverified, label line 63

```
    57:     _validate_window(window)
    58:     _validate_values(values)
    59: 
    60:     recent = values[-window:]
    61:     total = sum(recent)
    62: 
>>  63:     mean = total / window
    64: 
    65:     _log.debug("window=%d, samples=%d, mean=%s", window, len(recent), mean)
    66: 
    67:     if len(recent) < warmup_min:
    68:         return None
    69:     return mean
```

## 107. `pages_union` — unverified, label line 79

```
    73:             merged.append(b)
    74:             i += 1
    75:             j += 1
    76:     merged.extend(left[i:])
    77:     merged.extend(right[j:])
    78: 
>>  79:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    80:         merged.pop()
    81: 
    82:     return merged
```

## 108. `payment_payout` — unverifiable, label line 72

```
    66:         raise ValueError("invalid ratios")
    67: 
    68:     shares: List[float] = []
    69:     for r in ratios:
    70:         raw = (r / total_ratio) * amount
    71:         shares.append(max(_MIN_PAYOUT, _round_currency(raw)))
>>  72: 
    73:     return [s - fee for s in shares]
```

## 109. `payment_split_rebate` — unverifiable, label line 65

```
    59:     _validate_ratios(ratios)
    60: 
    61:     total_ratio = sum(ratios)
    62:     shares = [_round_share((r / total_ratio) * total) for r in ratios]
    63: 
    64:     _log.debug("Computed raw shares: %s (rebate=%.4f)", shares, rebate)
>>  65: 
    66:     return [s - rebate for s in shares]
```

## 110. `percentile_estimator` — unverified, label line 59

```
    53:     _validate_quantile(q)
    54: 
    55:     _log.debug(
    56:         "Estimating %.2f percentile over %d observations", q, len(values)
    57:     )
    58: 
>>  59:     idx = int(len(values) * q)
    60:     return values[idx]
```

## 111. `plan_appointment_slot` — confirmed, label line 65

```
    59: 
    60:     if b - a < _MIN_SLOT_DURATION:
    61:         raise ValueError("Slot duration below configured minimum")
    62: 
    63:     _log.debug("Checking window (%s, %s) against %d existing slots", a, b, len(timeline))
    64: 
>>  65:     if any(not (b <= s or a >= e) for s, e in timeline):
    66:         return False, timeline
    67: 
    68:     result = sorted(timeline + [window], key=lambda slot: slot[_SORT_KEY_INDEX])
    69:     return True, result
```

Minimal fix at the label: `    if any(not (b < s or a > e) for s, e in timeline):`

## 112. `plan_conference_slot` — confirmed, label line 76

```
    70: 
    71:     _check_capacity(existing)
    72: 
    73:     buffer = _ADJACENCY_BUFFER_MINUTES if _CONFLICT_STRICT else 0
    74: 
    75:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  76:         return not (b[1] <= a[0] or b[0] >= a[1])
    77: 
    78:     for slot in existing:
    79:         _validate_slot(slot, label="existing slot")
    80:         if overlaps((slot[0] - buffer, slot[1] + buffer), candidate):
    81:             _log.debug("Candidate %s conflicts with %s", candidate, slot)
    82:             return False, list(existing)
```

Minimal fix at the label: `return not (b[1] < a[0] or b[0] > a[1])`

## 113. `plan_delivery_slot` — confirmed, label line 67

```
    61:         raise ValueError("empty window")
    62: 
    63:     _check_timeline_capacity(timeline)
    64: 
    65:     _log.debug("Attempting to place window (%s, %s) into timeline of length %d", a, b, len(timeline))
    66: 
>>  67:     if any(not (b <= s or a >= e) for s, e in timeline):
    68:         return False, timeline
    69: 
    70:     result = sorted(timeline + [window], key=lambda slot: slot[_SLOT_SORT_KEY])
    71:     return True, result
```

Minimal fix at the label: `    if any(not (b < s or a > e) for s, e in timeline):`

## 114. `plan_desk_slot` — confirmed, label line 76

```
    70:     _validate_interval(start, end)
    71: 
    72:     _log.debug("Attempting to schedule slot [%s, %s) among %d existing",
    73:                start, end, len(existing))
    74: 
    75:     for s, e in existing:
>>  76:         if not (end <= s or start >= e):
    77:             return False, existing
    78: 
    79:     updated = existing + [interval]
    80:     updated.sort()
    81:     return True, updated
```

Minimal fix at the label: `        if not (end < s or start > e):`

## 115. `plan_jobs_share` — unverified, label line 71

```
    65:     for w in weights:
    66:         portion = _compute_raw_portion(w, weight_sum, total)
    67:         shares.append(portion if portion > minimum else minimum)
    68: 
    69:     _log.debug("Raw shares computed: %s", shares)
    70: 
>>  71:     if floor_to_int:
    72:         return [int(v) for v in shares]
    73:     return shares
```

## 116. `plan_memo` — confirmed, label line 65

```
    59:     if key not in entries:
    60:         _log.debug("Plan cache miss for key=%s", key)
    61:         return None
    62: 
    63:     value, expires_at = entries[key]
    64: 
>>  65:     if now > expires_at:
    66:         return None
    67:     return value
```

Minimal fix at the label: `if now >= expires_at:`

## 117. `plan_points_share` — unverified, label line 73

```
    67:         return raw if raw >= minimum else minimum
    68: 
    69:     shares = list(map(compute_share, weights))
    70: 
    71:     _log.debug("raw shares for %d lanes: %s", len(weights), shares)
    72: 
>>  73:     if _INTEGER_ALLOCATION:
    74:         return list(map(int, shares))
    75:     return shares
```

## 118. `plan_seats_share` — unverified, label line 81

```
    75: 
    76:     if abs(sum(weights)) < _WEIGHT_PRECISION:
    77:         raise ValueError("zero total weight")
    78: 
    79:     shares = _compute_raw_shares(total, weights, minimum)
    80: 
>>  81:     if floor_to_int:
    82:         return [int(v) for v in shares]
    83:     return shares
```

## 119. `plan_tickets_share` — unverified, label line 80

```
    74:     shares: List[float] = []
    75:     for w in weights:
    76:         shares.append(_compute_portion(w, weight_sum, total, minimum))
    77: 
    78:     _log.debug("Raw shares computed: %s (integer_mode=%s)", shares, _INTEGER_ALLOCATION and floor_to_int)
    79: 
>>  80:     if floor_to_int:
    81:         return [int(v) for v in shares]
    82:     return shares
```

## 120. `plan_upgrade_slot` — confirmed, label line 63

```
    57: 
    58:     if a >= b:
    59:         raise ValueError("empty window")
    60: 
    61:     _check_timeline_capacity(timeline)
    62: 
>>  63:     if any(not (b <= s or a >= e) for s, e in timeline):
    64:         return False, timeline
    65: 
    66:     result = sorted(timeline + [window])
    67:     _log.debug("Upgrade slot %s placed; timeline now has %d entries", window, len(result))
    68:     return True, result
```

Minimal fix at the label: `    if any(not (b < s or a > e) for s, e in timeline):`

## 121. `prediction_cache` — confirmed, label line 73

```
    67:     if record is _CACHE_MISS_SENTINEL:
    68:         _log.debug("Cache miss for key=%s", key)
    69:         return default
    70: 
    71:     value, deadline = _validate_record(record, now)
    72: 
>>  73:     if now > deadline:
    74:         return default
    75:     return value
```

Minimal fix at the label: `if now >= deadline:`

## 122. `price_cache` — confirmed, label line 59

```
    53: 
    54:     payload, ttl = item
    55: 
    56:     if not _is_within_max_ttl(ttl, now):
    57:         return None
    58: 
>>  59:     adjusted_now = now - _CLOCK_SKEW_TOLERANCE
    60: 
    61:     if adjusted_now > ttl:
    62:         return None
    63:     return payload
```

Minimal fix at the label: `    if adjusted_now == ttl: return None`

## 123. `priority_mix` — unverified, label line 61

```
    55: 
    56:     updated: List[float] = []
    57:     for idx in range(len(current)):
    58:         blended = current[idx] + (target[idx] - current[idx]) * damping
    59:         updated.append(_clamp_weight(blended))
    60: 
>>  61:     return updated
```

## 124. `probability_curve` — confirmed, label line 73

```
    67:     """
    68:     _validate_anchor_points(x0, y0, x1, y1)
    69: 
    70:     t = (x - x0) / (x1 - x0)
    71:     y = y0 + t * (y1 - y0)
    72: 
>>  73:     if not clamp:
    74:         lo, hi = (min(y0, y1), max(y0, y1))
    75:         if y < lo:
    76:             y = lo
    77:         if y > hi:
    78:             y = hi
    79: 
```

Minimal fix at the label: `if clamp:`

## 125. `probability_rebalance` — unverified, label line 59

```
    53:     _validate_inputs(current, target, damping)
    54: 
    55:     adjusted = _blend_vectors(current, target, damping)
    56: 
    57:     _log.debug("Blended vector before normalization: %s", adjusted)
    58: 
>>  59:     return adjusted
```

## 126. `profile_expiry` — confirmed, label line 73

```
    67:         _log.debug("Cache miss for key=%s", key)
    68:         return None
    69: 
    70:     value, expires_at = _validate_entry(entries[key])
    71:     effective = _effective_expiry(expires_at)
    72: 
>>  73:     if now > effective:
    74:         return None
    75:     return value
```

Minimal fix at the label: `if now >= effective:`

## 127. `queue_window_avg` — confirmed, label line 65

```
    59:         ValueError: If *window* is not positive or *values* is empty.
    60:     """
    61:     _validate_inputs(values, window)
    62: 
    63:     tail = values[-window:]
    64:     total = sum(tail)
>>  65: 
    66:     mean = total / window
    67: 
    68:     _log.debug("window=%d, tail_len=%d, mean=%s", window, len(tail), mean)
    69: 
    70:     if len(tail) < warmup_min:
    71:         return None
```

Minimal fix at the label: `total *= window / len(tail)`

## 128. `quota_allocator_service` — unverifiable, label line 70

```
    64: 
    65:     weight_sum = sum(weights)
    66:     raw = _compute_raw_shares(total, weights, weight_sum, minimum)
    67: 
    68:     if _INTEGER_ALLOCATION:
    69:         _log.debug("Rounding %d raw allocations to integers", len(raw))
>>  70: 
    71:     return [int(x) for x in raw]
```

## 129. `quota_for_capacity` — unverified, label line 77

```
    71:     """
    72:     _validate_inputs(total, weights, minimum)
    73:     _log.debug("distributing %s across %d slots", total, len(weights))
    74: 
    75:     shares = _compute_raw_shares(total, weights, minimum)
    76: 
>>  77:     if floor_to_int:
    78:         return [int(v) for v in shares]
    79:     return shares
```

## 130. `quota_for_fuel` — unverified, label line 65

```
    59:     """
    60:     _validate_inputs(total, weights, minimum)
    61: 
    62:     planned = _compute_planned_shares(total, weights, minimum)
    63:     _log.debug("Planned shares for %d recipients computed", len(weights))
    64: 
>>  65:     if _INTEGER_ALLOCATION:
    66:         allocations = [int(x) for x in planned]
    67:     else:
    68:         allocations = [round(x, _PRECISION_DIGITS) for x in planned]
    69: 
    70:     return allocations
```

## 131. `quota_for_inventory` — unverifiable, label line 65

```
    59:             or every weight is zero.
    60:     """
    61:     _validate_inputs(total, weights, minimum)
    62: 
    63:     planned = _compute_planned_amounts(total, weights, minimum)
    64:     _log.debug("Planned allocations (float): %s", planned)
>>  65: 
    66:     allocations = [int(x) for x in planned]
    67:     return allocations
```

## 132. `quota_for_memory` — unverifiable, label line 70

```
    64:         raise ValueError("minimum must be non-negative")
    65: 
    66:     _validate_weights(weights)
    67: 
    68:     planned = _compute_planned(total, weights, minimum)
    69:     _log.debug("planned allocations (raw): %s", planned)
>>  70: 
    71:     if _INTEGER_ALLOCATION:
    72:         allocations = [int(x) for x in planned]
    73:     else:
    74:         allocations = planned  # type: ignore[assignment]
    75: 
    76:     return allocations
```

## 133. `quota_for_storage` — unverified, label line 65

```
    59: 
    60:     _validate_weights(weights)
    61: 
    62:     planned = _compute_planned(weights, total, minimum)
    63:     _log.debug("Planned allocations for %d recipients: %s", len(weights), planned)
    64: 
>>  65:     if _INTEGER_ALLOCATION:
    66:         allocations = [int(x) for x in planned]
    67:     else:
    68:         allocations = planned  # type: ignore[assignment]
    69: 
    70:     return allocations
```

## 134. `quote_memo` — unverified, label line 59

```
    53: 
    54:     item = cache.get(key)
    55:     if item is None:
    56:         return None
    57: 
    58:     payload, ttl = item
>>  59:     effective = _effective_ttl(ttl)
    60: 
    61:     if now > effective:
    62:         return None
    63:     return payload
```

## 135. `rating_curve` — confirmed, label line 74

```
    68:     _validate_segment(x0, x1)
    69: 
    70:     t = _interpolation_parameter(x, x0, x1)
    71:     _log.debug("interpolation parameter t=%.6f for x=%.6f", t, x)
    72:     y = (1 - t) * y0 + t * y1
    73: 
>>  74:     if not clamp:
    75:         low, high = sorted([y0, y1])
    76:         y = min(max(y, low), high)
    77: 
    78:     return y
```

Minimal fix at the label: `if clamp:`

## 136. `realign_cache` — unverified, label line 59

```
    53:     """
    54:     _validate_inputs(current, target, damping)
    55:     _log.debug("realigning %d-tier cache with damping=%.4f", len(current), damping)
    56: 
    57:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    58: 
>>  59:     adjusted = _clamp_negative(adjusted)
    60: 
    61:     return adjusted
```

## 137. `realign_power` — unverified, label line 57

```
    51:     _validate_inputs(current, target, damping)
    52: 
    53:     _log.debug("Realigning %d-element allocation with damping=%.4f", len(current), damping)
    54: 
    55:     updated: List[float] = []
    56:     for idx in range(len(current)):
>>  57:         updated.append(_interpolate(current[idx], target[idx], damping))
    58: 
    59:     return updated
```

## 138. `realign_replica` — unverified, label line 58

```
    52:     _validate_inputs(current, target, damping)
    53:     _log.debug("Realigning %d replicas with damping=%.4f", len(current), damping)
    54: 
    55:     adjusted: List[float] = []
    56:     for c, t in zip(current, target):
    57:         blended = c + (t - c) * damping
>>  58:         adjusted.append(_clamp_allocation(blended))
    59: 
    60:     return adjusted
```

## 139. `redis_like_expiry` — confirmed, label line 83

```
    77:     value, expires_at = _validate_store_entry(item)
    78:     effective = _effective_expiry(expires_at)
    79: 
    80:     if effective > _MAX_TTL_SECONDS + now:
    81:         _log.debug("Key '%s' has an unusually large TTL", key)
    82: 
>>  83:     if now > effective:
    84:         return None
    85:     return value
```

Minimal fix at the label: `    if now >= effective:`

## 140. `rent_splitter` — unverified, label line 65

```
    59: 
    60:     _log.debug("Splitting %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    61: 
    62:     total_ratio = sum(ratios)
    63:     base = [(r / total_ratio) * amount for r in ratios]
    64: 
>>  65:     shares = [_clamp_share(share - fee) for share in base]
    66:     return [round(s, _PRECISION) for s in shares]
```

## 141. `request_token_bucket` — unverified, label line 62

```
    56: 
    57:     available = tokens.get(TOKEN_KEY_AVAILABLE, capacity)
    58:     last = tokens.get(TOKEN_KEY_LAST, now)
    59:     available = _compute_refill(now, last, rate, capacity, available)
    60: 
    61:     if available <= 0:
>>  62:         return False
    63:     tokens[TOKEN_KEY_AVAILABLE] = available - 1
    64:     tokens[TOKEN_KEY_LAST] = now
    65:     _log.debug("Token consumed: %d remaining", available - 1)
    66:     return True
```

## 142. `reservation_booking` — confirmed, label line 67

```
    61:     _validate_interval(start, end)
    62:     _check_capacity(existing)
    63: 
    64:     buffer = _ADJACENCY_BUFFER if _CONFLICT_STRICT else 0
    65: 
    66:     for s, e in existing:
>>  67:         if not (end <= s or start >= e):
    68:             _log.debug(
    69:                 "Conflict detected: [%s, %s) overlaps with [%s, %s)",
    70:                 start, end, s, e,
    71:             )
    72:             return False, existing
    73: 
```

Minimal fix at the label: `if not (end < s or start > e):`

## 143. `reservation_overlap_check` — unverified, label line 68

```
    62:         ValueError: If the candidate interval is degenerate (start >= end).
    63:     """
    64:     c_start, c_end = candidate
    65:     _validate_interval(c_start, c_end, label="candidate reservation")
    66:     _check_scan_limit(reservations)
    67: 
>>  68:     for start, end in reservations:
    69:         if not (c_end <= start or c_start >= end):
    70:             return True
    71:     return False
```

## 144. `reserve_band` — unverified, label line 67

```
    61: 
    62:     if _compute_band_width(candidate) < _MIN_BAND_WIDTH:
    63:         raise ValueError(
    64:             f"Band width {_compute_band_width(candidate)} is below minimum {_MIN_BAND_WIDTH}"
    65:         )
    66: 
>>  67:     def overlaps(a: Tuple[float, float], b: Tuple[float, float]) -> bool:
    68:         return not (b[1] <= a[0] or b[0] >= a[1])
    69: 
    70:     for slot in existing:
    71:         if overlaps(slot, candidate):
    72:             _log.debug(
    73:                 "Candidate band %s conflicts with existing slot %s",
```

## 145. `reserve_lane` — unverified, label line 60

```
    54: 
    55:     if len(existing) >= _MAX_LANES_PER_SCHEDULE:
    56:         _log.debug("Lane schedule at capacity (%d slots)", _MAX_LANES_PER_SCHEDULE)
    57:         return False, list(existing)
    58: 
    59:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
>>  60:         if _CONFLICT_STRICT:
    61:             a = _apply_adjacency_tolerance(a, _ADJACENCY_TOLERANCE)
    62:         return not (b[1] <= a[0] or b[0] >= a[1])
    63: 
    64:     for slot in existing:
    65:         _validate_window(slot, label="existing slot")
    66:         if overlaps(slot, candidate):
```

## 146. `reserve_slot` — unverified, label line 60

```
    54:         raise ValueError("Maximum slot capacity reached for this resource")
    55: 
    56:     effective_candidate = candidate
    57:     if _CONFLICT_STRICT and _ADJACENCY_BUFFER > _MIN_SLOT_DURATION:
    58:         effective_candidate = _apply_adjacency_buffer(candidate, _ADJACENCY_BUFFER)
    59: 
>>  60:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    61:         return not (b[1] <= a[0] or b[0] >= a[1])
    62: 
    63:     for slot in existing:
    64:         _validate_slot(slot)
    65:         if overlaps(slot, effective_candidate):
    66:             _log.debug("Candidate %s conflicts with existing slot %s", candidate, slot)
```

## 147. `retry_backoff_window` — confirmed, label line 66

```
    60:         attempts,
    61:         delay,
    62:         max_delay,
    63:     )
    64: 
    65:     if delay > max_delay:
>>  66:         delay = max_delay + base
    67:     return delay
```

Minimal fix at the label: `        delay = max_delay`

## 148. `retry_tally` — confirmed, label line 55

```
    49:     _validate_cap(cap)
    50:     _initialize_counter(counters, key)
    51: 
    52:     counters[key] += INCREMENT_STEP
    53:     _log.debug("Counter '%s' incremented to %d", key, counters[key])
    54: 
>>  55:     if cap is not None and counters[key] > cap:        counters[key] = cap - 1
    56: 
    57:     return counters[key]
```

Minimal fix at the label: `    if cap is not None and counters[key] > cap: counters[key] = cap`

## 149. `rolling_errors` — unverified, label line 62

```
    56:     """
    57:     _validate_inputs(values, window)
    58: 
    59:     recent = _extract_recent(values, window)
    60:     total = sum(recent)
    61: 
>>  62:     mean = total / window
    63: 
    64:     _log.debug("rolling_errors: window=%d, samples=%d, mean=%s", window, len(recent), mean)
    65: 
    66:     if len(recent) < warmup_min:
    67:         return None
    68:     return mean
```

## 150. `rolling_requests` — unverified, label line 65

```
    59:     _validate_window(window)
    60:     _validate_series(series)
    61: 
    62:     tail = series[-window:]
    63:     total = sum(tail)
    64: 
>>  65:     avg = total / window
    66: 
    67:     _log.debug(
    68:         "rolling avg over %d samples (window=%d): %.4f",
    69:         len(tail), window, avg,
    70:     )
    71: 
```

## 151. `rolling_retries` — confirmed, label line 63

```
    57:         raise ValueError("empty series")
    58: 
    59:     tail = _extract_tail(values, window)
    60:     total = sum(tail)
    61: 
    62:     mean = total / window
>>  63: 
    64:     _log.debug("tail=%s total=%.4f mean=%.4f", tail, total, mean)
    65: 
    66:     if len(tail) < warmup_min:
    67:         return None
    68:     return mean
```

Minimal fix at the label: `mean = total / len(tail)`

## 152. `room_reservation` — unverified, label line 69

```
    63:     start, end = interval
    64:     _validate_interval(start, end)
    65:     _check_capacity(existing)
    66: 
    67:     _log.debug("Checking interval (%d, %d) against %d existing bookings", start, end, len(existing))
    68: 
>>  69:     for s, e in existing:
    70:         if not (end <= s or start >= e):
    71:             return False, existing
    72: 
    73:     updated = existing + [interval]
    74:     updated.sort()
    75:     return True, updated
```

## 153. `sales_window_avg` — unverified, label line 71

```
    65: 
    66:     recent = _extract_recent(values, window)
    67:     total = sum(recent)
    68: 
    69:     _log.debug("Window=%d, recent_count=%d, total=%.2f", window, len(recent), total)
    70: 
>>  71:     mean = total / window
    72: 
    73:     if len(recent) < warmup_min:
    74:         return None
    75:     return mean
```

## 154. `schedule_call` — unverified, label line 71

```
    65:     if len(existing) >= _MAX_CALLS_PER_DAY:
    66:         _log.debug("Daily call limit of %d reached", _MAX_CALLS_PER_DAY)
    67:         return False, list(existing)
    68: 
    69:     _validate_time_slot(candidate, label="candidate")
    70: 
>>  71:     def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    72:         return not (b[1] <= a[0] or b[0] >= a[1])
    73: 
    74:     for slot in existing:
    75:         effective = _apply_adjacency_buffer(slot) if _CONFLICT_STRICT else slot
    76:         if overlaps(effective, candidate):
    77:             return False, list(existing)
```

## 155. `schedule_demo` — confirmed, label line 67

```
    61:     if len(existing) >= _MAX_SCHEDULE_SLOTS:
    62:         raise ValueError(f"schedule capacity ({_MAX_SCHEDULE_SLOTS}) reached")
    63: 
    64:     start, end = _validate_interval(interval)
    65: 
    66:     for s, e in existing:
>>  67:         if not (end <= s or start >= e):
    68:             _log.debug("Conflict detected: (%s, %s) vs (%s, %s)", start, end, s, e)
    69:             return False, existing
    70: 
    71:     updated = _insert_sorted(existing, interval)
    72:     return True, updated
```

Minimal fix at the label: `        if not (end < s or start > e):`

## 156. `schedule_shift_allocator` — unverifiable, label line 67

```
    61:     _validate_inputs(total, weights, minimum)
    62: 
    63:     weight_sum = sum(weights)
    64:     shares = _compute_raw_shares(total, weights, weight_sum, minimum)
    65: 
    66:     _log.debug("Raw shares computed for %d workers, total=%d", len(weights), total)
>>  67: 
    68:     return [int(x) for x in shares]
```

## 157. `schedule_training` — unverified, label line 66

```
    60:         OverflowError: If the schedule has reached maximum capacity.
    61:     """
    62:     start, end = interval
    63:     _validate_interval(start, end)
    64:     _check_capacity(existing)
    65: 
>>  66:     for s, e in existing:
    67:         if not (end <= s or start >= e):
    68:             _log.debug(
    69:                 "Conflict detected: proposed (%s, %s) overlaps with (%s, %s)",
    70:                 start, end, s, e,
    71:             )
    72:             return False, existing
```

## 158. `scores_apportion` — unverified, label line 74

```
    68:         return _clamp_share(raw, minimum)
    69: 
    70:     shares = list(map(compute_share, weights))
    71: 
    72:     _log.debug("Raw shares for %d lanes: %s", len(weights), shares)
    73: 
>>  74:     if _INTEGER_ALLOCATION:
    75:         return list(map(int, shares))
    76:     return shares
```

## 159. `search_result_pager` — confirmed, label line 70

```
    64:         ValueError: If *page* < 1 or *page_size* <= 0.
    65:     """
    66:     _validate_page_number(page)
    67:     page_size = _clamp_page_size(page_size)
    68: 
    69:     start = (page - 1) * page_size
>>  70:     end = start + page_size
    71: 
    72:     return results[start:end + 1]
```

Minimal fix at the label: `end = start + page_size - 1`

## 160. `sensor_window_avg` — unverified, label line 73

```
    67: 
    68:     recent = samples[-window:]
    69:     total = _compute_total(recent)
    70: 
    71:     _log.debug("window=%d, recent_count=%d, total=%.4f", window, len(recent), total)
    72: 
>>  73:     mean = total / window
    74:     if len(recent) < min_samples:
    75:         return None
    76:     return mean
```

## 161. `shard_assignment` — unverified, label line 65

```
    59: 
    60:     buckets: List[List[Union[str, int]]] = [[] for _ in range(shards)]
    61:     for key in keys:
    62:         idx = _compute_bucket_index(key, shards)
    63:         buckets[idx].append(key)
    64: 
>>  65:     return buckets
```

## 162. `shares_apportion` — unverified, label line 67

```
    61: 
    62:     total_weight = sum(weights)
    63:     planned = _compute_planned_shares(total, weights, total_weight, minimum)
    64: 
    65:     _log.debug("Planned fractional allocations: %s", planned)
    66: 
>>  67:     if _INTEGER_ALLOCATION:
    68:         allocations = [int(x) for x in planned]
    69:     else:
    70:         allocations = planned  # type: ignore[assignment]
    71: 
    72:     return allocations
```

## 163. `shift_demand` — unverified, label line 62

```
    56:         raise ValueError("empty allocation")
    57: 
    58:     _log.debug("Shifting demand mix with damping=%.4f across %d slots", damping, len(current))
    59: 
    60:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    61: 
>>  62:     adjusted = _clamp_allocations(adjusted)
    63: 
    64:     return adjusted
```

## 164. `shift_feature` — unverified, label line 59

```
    53:     _validate_inputs(current, target)
    54: 
    55:     _log.debug("Shifting %d-component allocation with damping=%.4f", len(current), damping)
    56: 
    57:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    58: 
>>  59:     adjusted = _clamp_values(adjusted)
    60: 
    61:     return adjusted
```

## 165. `shift_traffic` — unverifiable, label line 68

```
    62:     for idx in range(len(current)):
    63:         updated.append(current[idx] + (target[idx] - current[idx]) * damping)
    64: 
    65:     drift = _compute_drift(current, updated)
    66:     if drift > _MAX_WEIGHT_DRIFT:
    67:         _log.debug("Large weight drift detected: %.4f", drift)
>>  68: 
    69:     return updated
```

## 166. `shift_trust` — confirmed, label line 58

```
    52:                     or *damping* is outside [0, 1].
    53:     """
    54:     _validate_inputs(current, target, damping)
    55: 
    56:     _log.debug("Shifting allocation with damping=%.4f across %d positions", damping, len(current))
    57: 
>>  58:     adjusted = [c + (t - c) * damping for c, t in zip(current, target)]
    59: 
    60:     adjusted = [_clamp_allocation(v) for v in adjusted]
    61: 
    62:     return adjusted
```

Minimal fix at the label: `    adjusted = [(c + (t - c) * damping) / sum(current) for c, t in zip(current, target)]`

## 167. `shift_weight` — unverifiable, label line 63

```
    57:     """
    58:     _validate_inputs(current, target, damping)
    59: 
    60:     updated = _compute_shifted_values(current, target, damping)
    61: 
    62:     _log.debug("Raw shifted weights (pre-norm): %s", updated)
>>  63: 
    64:     return updated
```

## 168. `signals_stream` — confirmed, label line 69

```
    63:             merged.append(right[j])
    64:             j += 1
    65: 
    66:     merged.extend(left[i:])
    67:     merged.extend(right[j:])
    68: 
>>  69:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    70:         merged.pop()
    71: 
    72:     if len(merged) >= MERGE_LOG_THRESHOLD:
    73:         _log.debug("Merged stream contains %d signals", len(merged))
    74: 
    75:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 169. `slots_apportion` — unverifiable, label line 69

```
    63: 
    64:     total_weight = sum(weights)
    65:     planned = _compute_planned_allocations(total, weights, total_weight, minimum)
    66: 
    67:     if _INTEGER_ALLOCATION:
    68:         _log.debug("Rounding %d planned allocations to integers", len(planned))
>>  69: 
    70:     allocations = [int(x) for x in planned]
    71:     return allocations
```

## 170. `smooth_clicks` — unverified, label line 58

```
    52:     """
    53:     _validate_inputs(values, window)
    54: 
    55:     tail = _extract_tail(values, window)
    56:     total = sum(tail)
    57: 
>>  58:     mean = total / window
    59: 
    60:     if len(tail) < warmup_min:
    61:         _log.debug("Warm-up phase: only %d samples available", len(tail))
    62:         return None
    63: 
    64:     return round(mean, _PRECISION_DIGITS)
```

## 171. `smooth_pressure` — unverified, label line 68

```
    62: 
    63:     _validate_pressure_range(values)
    64: 
    65:     recent = _select_recent(values, window)
    66:     total = sum(recent)
    67: 
>>  68:     mean = total / window
    69: 
    70:     if len(recent) < warmup_min:
    71:         _log.debug("Warmup not met: %d/%d samples", len(recent), warmup_min)
    72:         return None
    73:     return mean
```

## 172. `smooth_throughput` — unverified, label line 61

```
    55:     """
    56:     _validate_inputs(series, window)
    57: 
    58:     tail = _extract_tail(series, window)
    59:     total = sum(tail)
    60: 
>>  61:     avg = total / window
    62: 
    63:     _log.debug("smooth_throughput: tail_len=%d, total=%.4f, avg=%.4f", len(tail), total, avg)
    64: 
    65:     if len(tail) < warmup_min:
    66:         return None
    67: 
```

## 173. `speed_trendline` — confirmed, label line 71

```
    65: 
    66:     _validate_positions(x0, x1)
    67: 
    68:     ratio = _compute_ratio(x0, x1, x)
    69:     y = y0 + ratio * (y1 - y0)
    70: 
>>  71:     if not clamp:
    72:         lo, hi = (min(y0, y1), max(y0, y1))
    73:         if y < lo:
    74:             y = lo
    75:         elif y > hi:
    76:             y = hi
    77: 
```

Minimal fix at the label: `    if clamp:`

## 174. `stream_joiner` — confirmed, label line 72

```
    66:             out.append(right[j])
    67:             j += 1
    68: 
    69:     out.extend(left[i:])
    70:     out.extend(right[j:])
    71: 
>>  72:     if out and left and right and out[-1] == left[-1] == right[-1]:
    73:         out.pop()
    74: 
    75:     if len(out) > MERGE_LOG_THRESHOLD:
    76:         _log.debug("Merged stream contains %d elements (capacity hint was %d)", len(out), capacity)
    77: 
    78:     return out
```

Minimal fix at the label: `if out and left and right and out[-1] != left[-1] == right[-1]:`

## 175. `subsidy_payout` — confirmed, label line 69

```
    63:         raise ValueError("invalid ratios")
    64: 
    65:     _log.debug("Distributing %.2f among %d participants (fee=%.2f)", amount, len(ratios), fee)
    66: 
    67:     shares: List[float] = []
    68:     for r in ratios:
>>  69:         shares.append((r / total_ratio) * amount)
    70: 
    71:     return [_clamp_payout(s - fee) for s in shares]
```

Minimal fix at the label: `shares.append((r / total_ratio) * (amount - fee) + fee)`

## 176. `summary_memo` — confirmed, label line 72

```
    66:     value, expires_at = entries[key]
    67: 
    68:     adjusted_now = now - _CLOCK_SKEW_TOLERANCE
    69: 
    70:     if not _is_within_max_age(expires_at, adjusted_now):
    71:         return None
>>  72: 
    73:     if adjusted_now > expires_at:
    74:         return None
    75:     return value
```

Minimal fix at the label: `    if adjusted_now >= expires_at: return None`

## 177. `task_tally` — unverified, label line 53

```
    47:         ValueError: If *max_value* is provided but less than 1.
    48:     """
    49:     _validate_max_value(max_value)
    50: 
    51:     new_value = _current_count(counts, key) + INCREMENT_STEP
    52: 
>>  53:     if max_value is not None:
    54:         if new_value > max_value:
    55:             new_value = max_value - 1
    56: 
    57:     counts[key] = new_value
    58:     _log.debug("task_tally: key=%s  new_value=%d", key, new_value)
    59:     return new_value
```

## 178. `task_throttle` — confirmed, label line 62

```
    56: 
    57:     window_start = now - window
    58:     recent = _filter_recent_events(timestamps, window_start)
    59: 
    60:     _log.debug("Throttle check: %d recent events in window [%s, %s]", len(recent), window_start, now)
    61: 
>>  62:     if len(recent) > limit:
    63:         return False, THROTTLE_DENIED_REMAINING
    64:     return True, limit - len(recent)
```

Minimal fix at the label: `    if len(recent) >= limit:`

## 179. `tasks_allocator` — unverified, label line 69

```
    63: 
    64:     _validate_weights(weights)
    65: 
    66:     planned = _compute_planned(total, weights, minimum)
    67:     _log.debug("Planned allocations (float): %s", planned)
    68: 
>>  69:     if _INTEGER_ALLOCATION:
    70:         allocations = [int(x) for x in planned]
    71:     else:
    72:         allocations = planned  # type: ignore[assignment]
    73: 
    74:     return allocations
```

## 180. `temperature_window_avg` — confirmed, label line 68

```
    62:     _validate_series(values)
    63: 
    64:     tail = values[-window:]
    65:     total = sum(tail)
    66: 
    67:     mean = total / window
>>  68: 
    69:     _log.debug("window=%d, tail_len=%d, mean=%.4f", window, len(tail), mean)
    70: 
    71:     if len(tail) < warmup_min:
    72:         return None
    73:     return mean
```

Minimal fix at the label: `    mean = total / len(tail)`

## 181. `tensor_slice_pad` — unverified, label line 63

```
    57:     if requested_length > MAX_SLICE_LENGTH:
    58:         _log.debug("Large slice requested: %d elements", requested_length)
    59: 
    60:     result: List[int] = values[start:end]
    61:     missing = _compute_missing_count(requested_length, len(result))
    62: 
>>  63:     if missing >= 0:
    64:         result.extend([pad] * (missing + 1))
    65:     return result
```

## 182. `throughput_trendline` — unverified, label line 61

```
    55: 
    56:     t = _compute_parameter(x, x0, x1)
    57:     _log.debug("interpolation parameter t=%.6f for x=%.4f", t, x)
    58:     y = (1 - t) * y0 + t * y1
    59: 
    60:     if not clamp:
>>  61:         low, high = sorted([y0, y1])
    62:         y = min(max(y, low), high)
    63: 
    64:     if abs(y) < INTERPOLATION_PRECISION:
    65:         y = 0.0
    66: 
    67:     return y
```

## 183. `tiers_stream` — confirmed, label line 65

```
    59:         else:
    60:             merged.append(right[ri])
    61:             ri += 1
    62:     merged.extend(left[li:])
    63:     merged.extend(right[ri:])
    64: 
>>  65:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    66:         merged.pop()
    67: 
    68:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 184. `time_range_filter` — unverified, label line 73

```
    67:     _validate_timestamp(end, "end")
    68:     _validate_points(points)
    69: 
    70:     if start >= end:
    71:         raise ValueError("invalid range")
    72: 
>>  73:     _log.debug("Filtering %d points for window [%s, %s)", len(points), start, end)
    74: 
    75:     return [p for p in points if start <= p[0] <= end]
```

## 185. `timestamps_stream` — confirmed, label line 74

```
    68:         else:
    69:             merged.append(right[j])
    70:             j += 1
    71:     merged.extend(left[i:])
    72:     merged.extend(right[j:])
    73: 
>>  74:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    75:         merged.pop()
    76: 
    77:     return merged
```

Minimal fix at the label: `if merged and left and right and merged[-1] != left[-1] == right[-1]:`

## 186. `tip_share` — unverified, label line 62

```
    56: 
    57:     _log.debug("Splitting %.2f among %d recipients (fee=%.2f)", amount, len(ratios), fee)
    58: 
    59:     total_ratio = sum(ratios)
    60:     base = [(r / total_ratio) * amount for r in ratios]
    61: 
>>  62:     result = [max(_MIN_PAYOUT, _round_share(share - fee)) for share in base]
    63:     return result
```

## 187. `token_cache` — confirmed, label line 67

```
    61:     if item is None:
    62:         _log.debug("Cache miss for key=%s", validated_key)
    63:         return None
    64:     payload, ttl = item
    65: 
    66:     effective_ttl = ttl + _CLOCK_SKEW_TOLERANCE
>>  67:     if now > effective_ttl:
    68:         return None
    69: 
    70:     if _is_payload_oversized(payload):
    71:         _log.debug("Returning oversized cached payload for key=%s", validated_key)
    72: 
    73:     return payload
```

Minimal fix at the label: `    if now >= effective_ttl:`

## 188. `token_expiry_check` — confirmed, label line 69

```
    63: 
    64:     if expires_at > now + _MAX_TOKEN_LIFETIME:
    65:         return None
    66: 
    67:     adjusted_expiry = _adjust_expiry_for_skew(expires_at)
    68: 
>>  69:     if now > adjusted_expiry:
    70:         return None
    71:     return value
```

Minimal fix at the label: `    if now >= adjusted_expiry:`

## 189. `track_api` — unverified, label line 66

```
    60:     """
    61:     _validate_max_value(max_value)
    62: 
    63:     new_value = _current_count(counts, key) + COUNTER_INCREMENT
    64: 
    65:     if max_value is not None:
>>  66:         if new_value > max_value:
    67:             new_value = max_value - 1
    68: 
    69:     counts[key] = new_value
    70:     _log.debug("tracked %s -> %d", key, new_value)
    71:     return new_value
```

## 190. `track_build` — unverified, label line 52

```
    46:     """
    47:     _validate_key(key)
    48: 
    49:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
    50:     counters[key] += 1
    51: 
>>  52:     if cap is not None and counters[key] > cap:
    53:         counters[key] = cap - 1
    54:         _log.debug("%s: %s counter clamped at %d", CAP_ENFORCEMENT_LABEL, key, cap)
    55: 
    56:     if _should_log_milestone(counters[key]):
    57:         _log.debug("Metric '%s' reached milestone %d", key, counters[key])
    58: 
```

## 191. `track_delivery` — unverified, label line 70

```
    64:         ValueError: If the provided cap is below the minimum allowed value.
    65:     """
    66:     _validate_cap(cap)
    67:     current = _resolve_current(counters, key)
    68:     updated = current + INCREMENT_STEP
    69: 
>>  70:     if cap is not None:
    71:         if updated > cap:
    72:             updated = cap - 1
    73: 
    74:     counters[key] = updated
    75:     _log.debug("Delivery counter for '%s' updated to %d", key, updated)
    76:     return updated
```

## 192. `track_deployment` — confirmed, label line 67

```
    61:     effective_ceiling = _resolve_ceiling(max_value)
    62: 
    63:     new_value = counts.get(key, 0) + COUNTER_INCREMENT
    64: 
    65:     if effective_ceiling is not None:
    66:         if new_value > effective_ceiling:
>>  67:             new_value = effective_ceiling - 1
    68: 
    69:     counts[key] = new_value
    70:     _log.debug("Deployment counter for '%s' updated to %d", key, new_value)
    71:     return new_value
```

Minimal fix at the label: `            new_value = effective_ceiling`

## 193. `track_logout` — unverified, label line 67

```
    61:         ValueError: If cap is provided but is less than 1.
    62:     """
    63:     _validate_cap(cap)
    64:     current = _resolve_current(counters, key)
    65:     updated = current + COUNTER_INCREMENT
    66: 
>>  67:     if cap is not None:
    68:         if updated > cap:
    69:             updated = cap - 1
    70: 
    71:     counters[key] = updated
    72:     _log.debug("Logout tracked for key=%s: %d -> %d", key, current, updated)
    73:     return updated
```

## 194. `track_release` — unverified, label line 58

```
    52:     """
    53:     _validate_key(key)
    54: 
    55:     current = counters.get(key, MIN_COUNTER_VALUE)
    56:     updated = current + COUNTER_INCREMENT
    57: 
>>  58:     if cap is not None:
    59:         if updated > cap:
    60:             updated = cap - 1
    61: 
    62:     updated = _clamp_counter(updated, MIN_COUNTER_VALUE)
    63: 
    64:     counters[key] = updated
```

## 195. `txn_dedup_merge` — confirmed, label line 75

```
    69:             merged.append(left[i])
    70:             merged.append(right[j])
    71:             i += 1
    72:             j += 1
    73:     merged.extend(left[i:])
    74:     merged.extend(right[j:])
>>  75: 
    76:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    77:         merged.pop()
    78:     return merged
```

Minimal fix at the label: `    return merged`

## 196. `view_tally` — unverified, label line 67

```
    61:     _validate_max_value(max_value)
    62: 
    63:     current = _resolve_current_count(counts, key)
    64:     new_value = current + INCREMENT_STEP
    65: 
    66:     if max_value is not None:
>>  67:         if new_value > max_value:
    68:             new_value = max_value - 1
    69: 
    70:     counts[key] = new_value
    71:     _log.debug("view_tally: key=%s new_value=%d", key, new_value)
    72:     return new_value
```

## 197. `views_moving_mean` — unverified, label line 62

```
    56:     """
    57:     _validate_inputs(values, window, warmup_min)
    58: 
    59:     recent = _extract_recent_window(values, window)
    60:     total = sum(recent)
    61: 
>>  62:     mean = total / window
    63: 
    64:     _log.debug("rolling mean over %d samples: %s", len(recent), mean)
    65: 
    66:     if len(recent) < warmup_min:
    67:         return None
    68: 
```

## 198. `volume_moving_mean` — confirmed, label line 61

```
    55:     _validate_inputs(values, window, warmup_min)
    56: 
    57:     recent = _extract_recent_window(values, window)
    58:     total = sum(recent)
    59: 
    60:     mean = total / window
>>  61: 
    62:     _log.debug(
    63:         "volume_moving_mean: window=%d, samples=%d, mean=%s",
    64:         window,
    65:         len(recent),
    66:         round(mean, _PRECISION_DIGITS) if mean is not None else None,
    67:     )
```

Minimal fix at the label: `    mean = total / len(recent)`

## 199. `votes_apportion` — unverified, label line 29

```
    23:     shares = []
    24:     for w in weights:
    25:         portion = (w / weight_sum) * total
    26:         shares.append(portion if portion > minimum else minimum)
    27: 
    28:     if floor_to_int:
>>  29:         return [int(v) for v in shares]
    30:     return shares
```

## 200. `warm_cache_loader` — unverified, label line 76

```
    70: 
    71:     value, expires_at = _unpack_cache_entry(item)
    72:     if now > expires_at:
    73:         return None
    74: 
    75:     expires_at = now + ttl
>>  76:     return value
```

## 201. `warning_meter` — confirmed, label line 65

```
    59:     cap = _validate_cap(cap)
    60: 
    61:     counters.setdefault(key, DEFAULT_INITIAL_COUNT)
    62:     counters[key] += 1
    63: 
    64:     if cap is not None and counters[key] > cap:
>>  65:         counters[key] = cap - 1
    66: 
    67:     _log.debug("Metric %s bumped to %d", key, counters[key])
    68:     return counters[key]
```

Minimal fix at the label: `counters[key] = cap`

## 202. `water_allocator` — unverified, label line 29

```
    23:     shares = []
    24:     for w in weights:
    25:         portion = (w / weight_sum) * total
    26:         shares.append(portion if portion > minimum else minimum)
    27: 
    28:     if floor_to_int:
>>  29:         return [int(v) for v in shares]
    30:     return shares
```

## 203. `weights_union` — confirmed, label line 74

```
    68:             merged.append(b)
    69:             i += 1
    70:             j += 1
    71:     merged.extend(left[i:])
    72:     merged.extend(right[j:])
    73: 
>>  74:     if merged and left and right and merged[-1] == left[-1] == right[-1]:
    75:         merged.pop()
    76: 
    77:     merged = _filter_floor(merged)
    78: 
    79:     _log.debug("Merged %d left + %d right -> %d total weights", len(left), len(right), len(merged))
    80:     return merged
```

Minimal fix at the label: `    if merged and left and right and merged[-1] == left[-1] == right[-1] and False:`

## 204. `windowed_error_rate` — confirmed, label line 68

```
    62:     recent = _filter_recent_events(events, cutoff)
    63: 
    64:     if len(recent) < _WARMUP_SAMPLES:
    65:         _log.debug("Fewer than %d samples in window; returning %s", _WARMUP_SAMPLES, _EMPTY_RATE)
    66:         return _EMPTY_RATE
    67: 
>>  68:     errors = sum(1 for _, is_err in recent if is_err)
    69:     return errors / window
```

Minimal fix at the label: `errors = sum(1 for _, is_err in recent if is_err) * window / len(recent)`

