#!/usr/bin/env python3
"""Distinct rereview for PMR-007-RPDS-1 V2.

Uses a separate distribution grid, conditional-distribution tests, exhaustive
finite stochastic channels, source-anchor custody checks, and frozen-hash
verification. It does not import the primary checker.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import subprocess
import tempfile


def comps(total: int, n: int):
    if n == 1:
        yield (total,)
        return
    for i in range(total + 1):
        for tail in comps(total - i, n - 1):
            yield (i, *tail)


def dists(n: int, den: int):
    return [tuple(Fraction(x, den) for x in c) for c in comps(den, n)]


def tv(p, q):
    return sum((abs(a - b) for a, b in zip(p, q, strict=True)), Fraction(0)) / 2


def deterministic_push(p, mapping, outputs):
    return tuple(
        sum((p[i] for i in range(len(p)) if mapping[i] == y), Fraction(0))
        for y in range(outputs)
    )


def stochastic_push(p, kernel):
    outputs = len(kernel[0])
    return tuple(
        sum((p[i] * kernel[i][y] for i in range(len(p))), Fraction(0))
        for y in range(outputs)
    )


def union_support(p, q):
    return tuple(i for i in range(len(p)) if p[i] + q[i] > 0)


def ext_ratio(p, q, i):
    if q[i] == 0:
        return "INF"
    return p[i] / q[i]


def ratio_constant_on_mapping(p, q, mapping):
    seen = {}
    for i in union_support(p, q):
        y = mapping[i]
        r = ext_ratio(p, q, i)
        if y in seen and seen[y] != r:
            return False
        seen[y] = r
    return True


def conditional_equal_on_common_fibres(p, q, mapping, outputs):
    pp = deterministic_push(p, mapping, outputs)
    qq = deterministic_push(q, mapping, outputs)
    for y in range(outputs):
        if pp[y] > 0 and qq[y] > 0:
            for i in range(len(p)):
                if mapping[i] == y and p[i] / pp[y] != q[i] / qq[y]:
                    return False
        elif qq[y] == 0 and pp[y] > 0:
            # Extended +infinity fibre: every relevant q mass must vanish.
            if any(mapping[i] == y and q[i] > 0 for i in range(len(p))):
                return False
        elif pp[y] == 0 and qq[y] > 0:
            # Extended ratio zero is permitted and constant only when all p mass vanishes.
            if any(mapping[i] == y and p[i] > 0 for i in range(len(p))):
                return False
    return True


def exact_bf(p, q, mapping, outputs):
    pp = deterministic_push(p, mapping, outputs)
    qq = deterministic_push(q, mapping, outputs)
    for i in union_support(p, q):
        y = mapping[i]
        raw = ext_ratio(p, q, i)
        represented = "INF" if qq[y] == 0 and pp[y] > 0 else pp[y] / qq[y]
        if raw != represented:
            return False
    return True


def lr_partition(p, q):
    labels = {}
    out = []
    for i in union_support(p, q):
        r = ext_ratio(p, q, i)
        if r not in labels:
            labels[r] = len(labels)
        out.append(labels[r])
    return tuple(out)


def mapping_on_support(mapping, support):
    labels = {}
    out = []
    for i in support:
        y = mapping[i]
        if y not in labels:
            labels[y] = len(labels)
        out.append(labels[y])
    return tuple(out)


def refines(mapping, target):
    return all(
        mapping[i] != mapping[j] or target[i] == target[j]
        for i in range(len(mapping))
        for j in range(len(mapping))
    )


def verify_frozen_hashes(base: Path):
    receipt = base / "PMR-007_DEEP_AO_V2_FROZEN_HASHES.sha256"
    failures = []
    rows = 0
    for line in receipt.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        rows += 1
        actual = sha256((base / rel).read_bytes()).hexdigest()
        if actual != expected:
            failures.append({"file": rel, "expected": expected, "actual": actual})
    return {"rows": rows, "failures": failures, "status": "PASS" if not failures else "FAIL"}


def source_anchor_check():
    prh = os.environ.get("AR8R_PRH_PDF")
    osm = os.environ.get("AR8R_OSM_MD")
    if not prh or not osm:
        return {"status": "NOT_RUN_MISSING_SOURCE_ENV", "checks": []}
    prh_path = Path(prh)
    osm_path = Path(osm)
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        subprocess.run(["pdftotext", "-layout", str(prh_path), tmp.name], check=True)
        prh_text = Path(tmp.name).read_text(encoding="utf-8", errors="replace")
    osm_text = osm_path.read_text(encoding="utf-8", errors="replace")
    checks = [
        ("PRH", "shared statistical model of reality", prh_text),
        ("PRH", "different sensors and views", prh_text),
        ("OSM", "progressive decorrelations", osm_text),
        ("OSM", "uniquely reproduced both the final orthogonalized states and the learning trajectory", osm_text),
        ("OSM", "perfect task performance only requires", osm_text),
    ]
    rows = [
        {"source": src, "anchor": anchor, "found": anchor in text}
        for src, anchor, text in checks
    ]
    return {
        "status": "PASS" if all(row["found"] for row in rows) else "FAIL",
        "checks": rows,
        "hashes": {
            "PRH": sha256(prh_path.read_bytes()).hexdigest(),
            "OSM": sha256(osm_path.read_bytes()).hexdigest(),
        },
    }


def main():
    base = Path(__file__).resolve().parents[1]
    ds = dists(3, 4)
    deterministic_maps = list(product(range(2), repeat=3))
    probs = [Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(1)]
    stochastic_kernels = [
        tuple((r, 1 - r) for r in rows)
        for rows in product(probs, repeat=3)
    ]

    counts = {
        "distributions": len(ds),
        "model_pairs": 0,
        "deterministic_cases": 0,
        "conditional_characterization_failures": 0,
        "exact_ratio_characterization_failures": 0,
        "minimality_failures": 0,
        "stochastic_channel_cases": 0,
        "stochastic_tv_failures": 0,
        "equal_experiment_channel_failures": 0,
    }

    for p, q in product(ds, repeat=2):
        counts["model_pairs"] += 1
        support = union_support(p, q)
        target = lr_partition(p, q)
        for mapping in deterministic_maps:
            counts["deterministic_cases"] += 1
            exact = exact_bf(p, q, mapping, 2)
            conditional = conditional_equal_on_common_fibres(p, q, mapping, 2)
            ratio_constant = ratio_constant_on_mapping(p, q, mapping)
            if exact != conditional:
                counts["conditional_characterization_failures"] += 1
            if exact != ratio_constant:
                counts["exact_ratio_characterization_failures"] += 1
            if exact and not refines(mapping_on_support(mapping, support), target):
                counts["minimality_failures"] += 1

        for kernel in stochastic_kernels:
            counts["stochastic_channel_cases"] += 1
            pk = stochastic_push(p, kernel)
            qk = stochastic_push(q, kernel)
            if tv(pk, qk) > tv(p, q):
                counts["stochastic_tv_failures"] += 1
            if p == q and pk != qk:
                counts["equal_experiment_channel_failures"] += 1

    source = source_anchor_check()
    hashes = verify_frozen_hashes(base)
    claims = {
        "frozen_hashes_match": hashes["status"] == "PASS",
        "exact_bf_matches_conditional_and_ratio_criteria": (
            counts["conditional_characterization_failures"] == 0
            and counts["exact_ratio_characterization_failures"] == 0
        ),
        "support_relative_lr_partition_is_minimal": counts["minimality_failures"] == 0,
        "common_stochastic_channel_contracts_tv": counts["stochastic_tv_failures"] == 0,
        "equal_experiment_stays_equal_under_common_channel": counts["equal_experiment_channel_failures"] == 0,
        "source_scope_anchors_match": source["status"] == "PASS",
    }
    result = {
        "schema": "PMR007_DEEP_AO_DISTINCT_CHANNEL_SUFFICIENCY_REREVIEW_RESULTS_V1",
        "method_relation": "independent_conditional_distribution_and_stochastic_channel_implementation",
        "counts": counts,
        "frozen_hashes": hashes,
        "source_anchor_check": source,
        "claims": claims,
        "scope_notes": [
            "finite binary experiments",
            "deterministic exact sufficiency on union support",
            "common finite stochastic channels for TV only",
            "same-program procedural rereview; not external review",
            "no PRH or OSM metaphysical transfer",
        ],
        "overall": "PASS" if all(claims.values()) else "FAIL",
    }
    out = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
