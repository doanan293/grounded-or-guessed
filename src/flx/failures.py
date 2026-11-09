"""Failure analysis: automatic per-program signals → one category each, then a cluster-spread sample to read.

Categories (first match wins):
  gt_suspect          ground truth not confirmed by execution (unverified/unverifiable) and no method hits top-3
  guess_right         the LLM's own fault-line guess is a ground-truth line
  prior_hurts         guess wrong, the semantic spectrum ranks the fault 1st, but the guess bonus pushes it down
  rescued_by_spectrum guess wrong, SemLoc still has the fault in its top-3 (the evidence carried it)
  coverage_only_wins  SemLoc misses its top-3, LLM + coverage hits its top-3
  all_miss            everything else
"""
import random

CATEGORIES = ("gt_suspect", "guess_right", "prior_hurts", "rescued_by_spectrum", "coverage_only_wins", "all_miss")


def category(sig: dict) -> str:
    if sig["gt_status"] in ("unverified", "unverifiable") and not sig["semloc_top3"] and not sig["llmcov_top3"]:
        return "gt_suspect"
    if sig["guess_hit"]:
        return "guess_right"
    if sig["spectrum_rank"] == 1.0 and not sig["semloc_top1"]:
        return "prior_hurts"
    if sig["semloc_top3"]:
        return "rescued_by_spectrum"
    if sig["llmcov_top3"]:
        return "coverage_only_wins"
    return "all_miss"


def select(cases: list[dict], per_category: int, seed: int) -> list[dict]:
    """Up to `per_category` cases per category, distinct template clusters first; deterministic for a seed."""
    rng = random.Random(seed)
    out = []
    for cat in sorted({c["category"] for c in cases}):
        pool = sorted((c for c in cases if c["category"] == cat), key=lambda c: c["program"])
        rng.shuffle(pool)
        seen, first, rest = set(), [], []
        for c in pool:
            (rest if c["cluster"] in seen else first).append(c)
            seen.add(c["cluster"])
        out += (first + rest)[:per_category]
    return out


def line_relation(src: str, gt_line: int, guess_line: int, strict: bool = False) -> str:
    """How a guessed line relates to a ground-truth line:
    same         the same line
    blank_gt     the ground-truth line is blank or a comment (no statement to blame)
    header_body  one is the header of a compound statement (if/for/while/with/try) and the other is the first
                 line of its body, or lies in that first statement when it spans at most 3 lines — a fault spanning a
                 guard and the statement it guards (nested guards included). strict=True keeps only the header and
                 the first line of its body (a lower bound of the ambiguity; the default is an upper bound)
    other        anything else"""
    import ast
    if gt_line == guess_line:
        return "same"
    rows = src.splitlines()
    text = rows[gt_line - 1].strip() if 0 < gt_line <= len(rows) else ""
    if not text or text.startswith("#"):
        return "blank_gt"
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)) and node.body:
            first = node.body[0]
            last = first.end_lineno if (first.end_lineno - first.lineno <= 2 and not strict) else first.lineno
            for head, other in ((gt_line, guess_line), (guess_line, gt_line)):
                if head == node.lineno and first.lineno <= other <= last:
                    return "header_body"
    return "other"
