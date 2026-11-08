"""Structural templates in a benchmark: programs whose ASTs match once names and constants are erased.

shape(src)         sequence of AST node-type names (identifiers, constants, docstrings dropped)
similarity(a, b)   Jaccard similarity of the 4-gram multisets of two shapes
clusters(progs)    single-linkage clusters at a similarity threshold → {program: cluster id}
"""
import ast
from collections import Counter


def shape(src: str) -> list[str]:
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Constant) \
                and isinstance(node.value.value, str):
            continue  # docstrings
        if isinstance(node, (ast.Load, ast.Store, ast.Del)):
            continue
        out.append(type(node).__name__)
    return out


def _grams(seq: list[str], n: int = 4) -> Counter:
    return Counter(tuple(seq[i:i + n]) for i in range(max(len(seq) - n + 1, 1)))


def similarity(a: str, b: str) -> float:
    ga, gb = _grams(shape(a)), _grams(shape(b))
    inter = sum((ga & gb).values())
    union = sum((ga | gb).values())
    return inter / union if union else 1.0


def clusters(programs: dict[str, str], threshold: float = 0.8) -> dict[str, int]:
    names = sorted(programs)
    grams = {n: _grams(shape(programs[n])) for n in names}
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(names):
        for b in names[i + 1:]:
            inter = sum((grams[a] & grams[b]).values())
            union = sum((grams[a] | grams[b]).values())
            if union and inter / union >= threshold:
                parent[find(a)] = find(b)
    roots = {r: k for k, r in enumerate(sorted({find(n) for n in names}))}
    return {n: roots[find(n)] for n in names}
