from flx.gt import repaired_gt


def test_repaired_gt_replaces_corrected_and_drops_unverifiable():
    original = {"a": [10], "b": [20], "c": [30], "d": [40]}
    verified = [{"program": "a", "status": "confirmed", "lines": [10]},
                {"program": "b", "status": "corrected", "lines": [21], "original": [20]},
                {"program": "c", "status": "unverifiable", "lines": [30]},
                {"program": "d", "status": "unverified", "lines": [40]}]
    assert repaired_gt(original, verified) == {"a": [10], "b": [21], "d": [40]}
    assert repaired_gt(original, verified, strict=True) == {"a": [10], "b": [21]}
