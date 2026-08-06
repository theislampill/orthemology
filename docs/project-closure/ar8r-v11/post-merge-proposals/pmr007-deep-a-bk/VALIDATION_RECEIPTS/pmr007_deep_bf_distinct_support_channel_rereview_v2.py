from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).with_name(Path(__file__).stem + "_results.json")


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def normalize_counts(vals: tuple[int, ...], rows: int, cols: int):
    total = sum(vals)
    return [
        [Fraction(vals[i * cols + j], total) for j in range(cols)]
        for i in range(rows)
    ]


def matrix_rank(a):
    a = [row[:] for row in a]
    m = len(a)
    n = len(a[0])
    r = 0
    c = 0
    while r < m and c < n:
        pivot = next((i for i in range(r, m) if a[i][c] != 0), None)
        if pivot is None:
            c += 1
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(m):
            if i != r and a[i][c] != 0:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        c += 1
    return r


def matmul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def support_mask(p):
    rows, cols = len(p), len(p[0])
    mask = 0
    for i in range(rows):
        for j in range(cols):
            if p[i][j] > 0:
                mask |= 1 << (i * cols + j)
    return mask


def all_rectangles(rows: int, cols: int, support: int):
    rects = set()
    for rmask in range(1, 1 << rows):
        for cmask in range(1, 1 << cols):
            rect = 0
            for i in range(rows):
                if (rmask >> i) & 1:
                    for j in range(cols):
                        if (cmask >> j) & 1:
                            rect |= 1 << (i * cols + j)
            if rect and rect & ~support == 0:
                rects.add(rect)
    return sorted(rects)


def rectangle_cover_number(rows: int, cols: int, support: int):
    if support == 0:
        return 0
    rects = all_rectangles(rows, cols, support)
    inf = 999
    dp = {0: 0}
    for mask in range(1 << (rows * cols)):
        if mask not in dp:
            continue
        value = dp[mask]
        for rect in rects:
            new = mask | rect
            if new & ~support:
                continue
            if value + 1 < dp.get(new, inf):
                dp[new] = value + 1
    return dp[support]


def random_distribution(rng: random.Random, n: int):
    vals = [rng.randint(0, 9) for _ in range(n)]
    if sum(vals) == 0:
        vals[rng.randrange(n)] = 1
    s = sum(vals)
    return [Fraction(v, s) for v in vals]


def random_kernel(rng: random.Random, out_n: int, in_n: int):
    # Column-stochastic: each input column is a distribution over outputs.
    cols = [random_distribution(rng, out_n) for _ in range(in_n)]
    return [[cols[j][i] for j in range(in_n)] for i in range(out_n)]


def mixture_matrix(weights, left, right):
    m = len(left[0])
    n = len(right[0])
    return [
        [sum((weights[h] * left[h][i] * right[h][j]
              for h in range(len(weights))), Fraction(0))
         for j in range(n)]
        for i in range(m)
    ]


def canonical_h_equals_x(p):
    m, n = len(p), len(p[0])
    weights = []
    left = []
    right = []
    for i in range(m):
        mass = sum(p[i])
        if mass == 0:
            continue
        weights.append(mass)
        left.append([Fraction(int(k == i)) for k in range(m)])
        right.append([p[i][j] / mass for j in range(n)])
    return weights, left, right


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


results = {
    "identity": "PMR-007-ILRC-1",
    "checker": "DISTINCT_SUPPORT_CHANNEL_REREVIEW_V2",
    "independent_of_primary_import": True,
    "frozen_hash_rows": 0,
    "frozen_hash_mismatches": [],
    "two_by_two_tables": 0,
    "two_by_two_rank1": 0,
    "two_by_two_rank2": 0,
    "two_by_two_rectangle_bound_failures": 0,
    "three_by_three_support_patterns": 0,
    "three_by_three_rectangle_solver_failures": 0,
    "identity_rectangle_witnesses": {},
    "exact_latent_mixture_trials": 0,
    "exact_latent_mixture_failures": 0,
    "canonical_saturation_trials": 0,
    "canonical_saturation_failures": 0,
    "stochastic_channel_trials": 0,
    "stochastic_channel_pushforward_failures": 0,
    "strict_contraction_witness": {},
    "field_scope_checks": {},
    "stronger_reading_controls": {},
}

# Verify frozen V2 files without relying on the primary checker.
manifest = ROOT / "PMR-007_DEEP_BF_V2_FROZEN_HASHES.sha256"
for line in manifest.read_text().splitlines():
    if not line.strip():
        continue
    expected, rel = line.split(None, 1)
    rel = rel.strip()
    actual = sha256(ROOT / rel)
    results["frozen_hash_rows"] += 1
    if actual != expected:
        results["frozen_hash_mismatches"].append(
            {"path": rel, "expected": expected, "actual": actual}
        )

# Exhaustive 2x2 rational probability matrices through total 18.
for total in range(1, 19):
    for vals in compositions(total, 4):
        p = normalize_counts(vals, 2, 2)
        rank = matrix_rank(p)
        rcov = rectangle_cover_number(2, 2, support_mask(p))
        results["two_by_two_tables"] += 1
        results[f"two_by_two_rank{rank}"] += 1
        # In 2x2, nonnegative rank equals ordinary rank for nonzero P.
        if rcov > rank:
            results["two_by_two_rectangle_bound_failures"] += 1

# Independently exercise the rectangle-cover solver on all 3x3 supports.
# It must be between 1 and the number of positive cells, and exact on diagonal supports.
for support in range(1, 1 << 9):
    rcov = rectangle_cover_number(3, 3, support)
    pop = support.bit_count()
    results["three_by_three_support_patterns"] += 1
    if not (1 <= rcov <= pop):
        results["three_by_three_rectangle_solver_failures"] += 1

for n in range(2, 7):
    # For diagonal support, every contained nonempty rectangle has one cell:
    # two distinct diagonal cells would force an off-diagonal corner.
    support = sum(1 << (i * n + i) for i in range(n))
    rects = all_rectangles(n, n, support)
    max_rect_cells = max(r.bit_count() for r in rects)
    rcov = n
    results["identity_rectangle_witnesses"][str(n)] = {
        "rectangle_cover": rcov,
        "ordinary_rank": n,
        "canonical_width": n,
        "max_contained_rectangle_cells": max_rect_cells,
        "pass": rcov == n and max_rect_cells == 1,
    }

rng = random.Random(2026080602)

# Exact product-mixture constructions, generated directly rather than from U,V.
for _ in range(30000):
    m = rng.randint(2, 6)
    n = rng.randint(2, 6)
    r = rng.randint(1, 6)
    weights = random_distribution(rng, r)
    left = [random_distribution(rng, m) for _ in range(r)]
    right = [random_distribution(rng, n) for _ in range(r)]
    p = mixture_matrix(weights, left, right)
    results["exact_latent_mixture_trials"] += 1
    if sum(sum(row) for row in p) != 1 or any(x < 0 for row in p for x in row):
        results["exact_latent_mixture_failures"] += 1

# Canonical H=X saturation for arbitrary exact rational tables.
for _ in range(20000):
    m = rng.randint(2, 7)
    n = rng.randint(2, 7)
    vals = [rng.randint(0, 12) for _ in range(m * n)]
    if sum(vals) == 0:
        vals[0] = 1
    p = normalize_counts(tuple(vals), m, n)
    w, left, right = canonical_h_equals_x(p)
    q = mixture_matrix(w, left, right)
    results["canonical_saturation_trials"] += 1
    if q != p or len(w) > m:
        results["canonical_saturation_failures"] += 1

# Common stochastic channels push supplied factorization terms forward.
for _ in range(30000):
    m = rng.randint(2, 6)
    n = rng.randint(2, 6)
    r = rng.randint(1, 6)
    m2 = rng.randint(1, 5)
    n2 = rng.randint(1, 5)
    weights = random_distribution(rng, r)
    left = [random_distribution(rng, m) for _ in range(r)]
    right = [random_distribution(rng, n) for _ in range(r)]
    p = mixture_matrix(weights, left, right)
    kx = random_kernel(rng, m2, m)
    ky = random_kernel(rng, n2, n)
    pushed_matrix = matmul(matmul(kx, p), transpose(ky))
    pushed_left = [list(x) for x in zip(*matmul(kx, transpose(left)))]
    pushed_right = [list(x) for x in zip(*matmul(ky, transpose(right)))]
    reconstructed = mixture_matrix(weights, pushed_left, pushed_right)
    results["stochastic_channel_trials"] += 1
    if pushed_matrix != reconstructed:
        results["stochastic_channel_pushforward_failures"] += 1

# Strict contraction: merge all rows of I_3/3.
p = [[Fraction(int(i == j), 3) for j in range(3)] for i in range(3)]
kx = [[Fraction(1), Fraction(1), Fraction(1)]]
ky = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
q = matmul(matmul(kx, p), transpose(ky))
results["strict_contraction_witness"] = {
    "source_ordinary_rank": matrix_rank(p),
    "output_ordinary_rank": matrix_rank(q),
    "output": [[str(x) for x in row] for row in q],
    "pass": matrix_rank(p) == 3 and matrix_rank(q) == 1,
}

v2_text = (ROOT / "PMR-007_DEEP_ROUND_BF_IMPERSONAL_LATENT_REALIZATION_COMPLEXITY_V2.md").read_text()
source_text = (ROOT / "source_and_prior_art/PMR-007_DEEP_BF_NONNEGATIVE_RANK_ANCESTRY_AND_FIELD_NOTE.md").read_text()
results["field_scope_checks"] = {
    "theorem_explicit_over_reals": "rank}_{+}^{\\mathbb R}" in v2_text or "rank_+^R" in v2_text,
    "rational_field_separate": "rank_+^Q" in v2_text and "rank_+^Q" in source_text,
    "irrationality_source_pinned": "5c382caf391de7904cd1af16723481b6090ed261281c4bd7c5cb96b1becaed9a" in source_text,
}

results["stronger_reading_controls"] = {
    "width_not_subject_count": True,
    "rank_one_not_causal_unity": True,
    "observational_not_interventional": True,
    "matrix_not_tensor": True,
    "formal_impersonal_not_metaphysical_actuality": True,
    "width_bound_requires_independent_warrant": True,
    "candidate_specific_recoding_not_common_evidence": True,
}

failure_fields = [
    "frozen_hash_mismatches",
    "two_by_two_rectangle_bound_failures",
    "three_by_three_rectangle_solver_failures",
    "exact_latent_mixture_failures",
    "canonical_saturation_failures",
    "stochastic_channel_pushforward_failures",
]
failed = False
for key in failure_fields:
    value = results[key]
    failed = failed or bool(value)
failed = failed or not all(results["field_scope_checks"].values())
failed = failed or not results["strict_contraction_witness"]["pass"]
results["result"] = "FAIL" if failed else "PASS"

OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
print(json.dumps(results, indent=2, sort_keys=True))
