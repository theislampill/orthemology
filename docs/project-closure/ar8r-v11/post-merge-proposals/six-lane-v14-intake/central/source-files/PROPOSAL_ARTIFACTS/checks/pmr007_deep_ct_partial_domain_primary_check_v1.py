#!/usr/bin/env python3
"""Adversarial check of the Deep CT V1 partial-domain claim."""
from __future__ import annotations
import itertools, json
from pathlib import Path

OUT = Path(__file__).with_name("pmr007_deep_ct_partial_domain_primary_check_v1_results.json")

def fibre_constant(profile, target):
    seen = {}
    for p, q in zip(profile, target):
        if p in seen and seen[p] != q:
            return False
        seen[p] = q
    return True

n = 4
counterexamples = []
proper_domains = 0
for target in itertools.product(range(2), repeat=n):
    if len(set(target)) == 1:
        continue
    for avail in itertools.product(range(2), repeat=n):
        if not (0 < sum(avail) < n):
            continue
        proper_domains += 1
        for vals in itertools.product(range(2), repeat=n):
            total = tuple((avail[i], vals[i] if avail[i] else -1) for i in range(n))
            if fibre_constant(total, target):
                counterexamples.append({"target": target, "availability": avail, "values": vals, "totalized": total})
                if len(counterexamples) >= 8:
                    break
        if len(counterexamples) >= 8:
            break
    if len(counterexamples) >= 8:
        break

result = {
    "schema": "PMR007_DEEP_CT_V1_PRIMARY_CHECK_RESULTS",
    "models": n,
    "proper_domain_assignments_examined_lower_bound": proper_domains,
    "v1_claim": "proper partial domain cannot identify target even after bottom totalization",
    "counterexamples_found": len(counterexamples),
    "first_counterexamples": counterexamples,
    "disposition": "FAIL_COUNTEREXAMPLE_FOUND" if counterexamples else "NO_COUNTEREXAMPLE_FOUND"
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(1 if counterexamples else 0)
