from flx.gt import repaired_gt


def test_repaired_gt_replaces_corrected_and_drops_unverifiable():
    original = {"a": [10], "b": [20], "c": [30], "d": [40]}
    verified = [{"program": "a", "status": "confirmed", "lines": [10]},
                {"program": "b", "status": "corrected", "lines": [21], "original": [20]},
                {"program": "c", "status": "unverifiable", "lines": [30]},
                {"program": "d", "status": "unverified", "lines": [40]}]
    assert repaired_gt(original, verified) == {"a": [10], "b": [21], "d": [40]}
    assert repaired_gt(original, verified, strict=True) == {"a": [10], "b": [21]}


def test_repaired_gt_drops_blank_line_locations():
    """A minimal 'fix' written onto a blank line (e.g. inserting `return merged`) names no statement any method can
    rank; such entries are unverifiable by construction, whatever status the oracle gave them."""
    from flx.gt import repaired_gt
    original = {"a": [3], "b": [5], "c": [2]}
    verified = [{"program": "a", "status": "confirmed", "lines": [3]},
                {"program": "b", "status": "corrected", "lines": [4], "original": [5]},
                {"program": "c", "status": "confirmed", "lines": [2]}]
    src = {"a": ["x = 1", "", "", "y"], "b": ["", "", "", "z = 2", ""], "c": ["a", "b = 1"]}
    got = repaired_gt(original, verified, sources=src)
    assert got == {"b": [4], "c": [2]}
    assert repaired_gt(original, verified) == {"a": [3], "b": [4], "c": [2]}  # without sources: unchanged
