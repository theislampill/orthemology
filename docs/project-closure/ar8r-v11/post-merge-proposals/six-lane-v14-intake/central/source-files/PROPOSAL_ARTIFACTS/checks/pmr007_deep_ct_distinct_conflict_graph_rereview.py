#!/usr/bin/env python3
"""Distinct conflict-graph rereview for PMR-007-PCDF-1 V2."""
from __future__ import annotations
import hashlib, json, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "pmr007_deep_ct_distinct_conflict_graph_rereview_results.json"
HASHES = ROOT / "deep_ct" / "PMR007_DEEP_CT_V2_FROZEN_HASHES.sha256"

rng = random.Random(0xC7D0A1)

def verify_hashes(path: Path):
    failures = []
    checked = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, filename = line.split(None, 1)
        p = Path(filename.strip())
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        checked += 1
        if actual != digest:
            failures.append({"path": str(p), "expected": digest, "actual": actual})
    return checked, failures

def signal(A, Y):
    return [(A[i], Y[i] if A[i] else -1) for i in range(len(A))]

def conflicts(E, Q):
    return [(i,j) for i in range(len(E)) for j in range(i+1,len(E)) if E[i] == E[j] and Q[i] != Q[j]]

def resolves_all(conflict_pairs, X):
    return all(X[i] != X[j] for i,j in conflict_pairs)

def e_measurable(E, X):
    return all(E[i] != E[j] or X[i] == X[j] for i in range(len(E)) for j in range(i+1,len(E)))

checked_hashes, hash_failures = verify_hashes(HASHES)
trials = 80000
barrier_failures = 0
novel_signal_failures = 0
relabel_failures = 0
restricted_extension_failures = 0
successful_extensions = 0
partial_identifying = 0

for _ in range(trials):
    n = rng.randint(3, 9)
    E = [rng.randrange(rng.randint(1, min(4,n))) for _ in range(n)]
    Q = [rng.randrange(rng.randint(2,3)) for _ in range(n)]
    A = [rng.randrange(2) for _ in range(n)]
    Y = [rng.randrange(3) for _ in range(n)]
    X = signal(A,Y)
    C = conflicts(E,Q)
    resolves = resolves_all(C,X)
    measurable = e_measurable(E,X)

    if C and measurable and resolves:
        barrier_failures += 1
    if C and resolves:
        successful_extensions += 1
        if measurable:
            novel_signal_failures += 1
    if 0 < sum(A) < n and resolves:
        partial_identifying += 1

    # Relabel evidence classes, target values, and outcome values bijectively.
    e_labels = sorted(set(E)); e_perm = e_labels[:]; rng.shuffle(e_perm)
    e_map = dict(zip(e_labels,e_perm)); Er = [e_map[x] for x in E]
    q_labels = sorted(set(Q)); q_perm = q_labels[:]; rng.shuffle(q_perm)
    q_map = dict(zip(q_labels,q_perm)); Qr = [q_map[x] for x in Q]
    y_labels = sorted(set(Y)); y_perm = y_labels[:]; rng.shuffle(y_perm)
    y_map = dict(zip(y_labels,y_perm)); Yr = [y_map[x] for x in Y]
    Xr = signal(A,Yr)
    if resolves_all(conflicts(Er,Qr),Xr) != resolves:
        relabel_failures += 1

    # Restricted-domain ambiguity: flip one outside-domain target while keeping
    # all on-domain values fixed.
    if 0 < sum(A) < n:
        outside = [i for i,a in enumerate(A) if not a]
        k = rng.choice(outside)
        Q2 = Q[:]
        Q2[k] = (Q2[k] + 1) % 3
        if any(A[i] and Q2[i] != Q[i] for i in range(n)) or Q2 == Q:
            restricted_extension_failures += 1

# Frozen U/I/P target-leakage and common-bearer controls.
E = [0,0,0]; Q = [1,0,0]
controls = {}
for name,A,Y in [
    ("common_proxy", [1,1,1], [0,0,0]),
    ("common_bearer", [1,1,1], [1,1,0]),
    ("target_laden_availability", [1,0,0], [0,0,0]),
    ("target_oracle_outcome", [1,1,1], [1,0,0]),
]:
    X = signal(A,Y)
    controls[name] = {
        "conflicts": len(conflicts(E,Q)),
        "resolves_all": resolves_all(conflicts(E,Q),X),
        "e_measurable": e_measurable(E,X),
    }

result = {
    "schema": "PMR007_DEEP_CT_DISTINCT_CONFLICT_GRAPH_REREVIEW_RESULTS",
    "seed": hex(0xC7D0A1),
    "frozen_hashes_checked": checked_hashes,
    "frozen_hash_failures": hash_failures,
    "random_trials": trials,
    "successful_new_signal_extensions": successful_extensions,
    "proper_domain_totalizations_resolving_conflicts": partial_identifying,
    "old_profile_measurable_barrier_failures": barrier_failures,
    "successful_extensions_without_non_E_measurable_signal": novel_signal_failures,
    "restricted_domain_extension_failures": restricted_extension_failures,
    "relabel_invariance_failures": relabel_failures,
    "uip_controls": controls,
}
result["overall"] = "PASS" if not (hash_failures or barrier_failures or novel_signal_failures or restricted_extension_failures or relabel_failures) else "FAIL"
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["overall"] == "PASS" else 1)
