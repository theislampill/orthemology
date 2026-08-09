#!/usr/bin/env python3
"""Exhaustive finite check for Deep CT V2 domain/capability fork."""
from __future__ import annotations
import itertools, json
from pathlib import Path

OUT = Path(__file__).with_name("pmr007_deep_ct_partial_domain_primary_check_v2_results.json")

def rgs_partitions(n):
    a = [0] * n
    def rec(i, maximum):
        if i == n:
            yield tuple(a)
            return
        for v in range(maximum + 2):
            a[i] = v
            yield from rec(i + 1, max(maximum, v))
    if n == 0:
        yield ()
    else:
        yield from rec(1, 0)

def fibre_constant(profile, target):
    seen = {}
    for p, q in zip(profile, target):
        if p in seen and seen[p] != q:
            return False
        seen[p] = q
    return True

def experiment_signal(avail, values):
    return tuple((avail[i], values[i] if avail[i] else -1) for i in range(len(avail)))

def joint(evidence, signal):
    return tuple((evidence[i], signal[i]) for i in range(len(evidence)))

def agrees_on_domain(q, qp, domain):
    return all((not domain[i]) or q[i] == qp[i] for i in range(len(q)))

n = 4
partitions = list(rgs_partitions(n))
targets = [q for q in itertools.product(range(2), repeat=n) if len(set(q)) > 1]
bits = list(itertools.product(range(2), repeat=n))

postprocessing_cases = 0
postprocessing_failures = 0
necessary_novel_signal_cases = 0
necessary_novel_signal_failures = 0
target_leakage_totalizations = 0
v1_counterexamples = 0
restricted_domain_underdetermination_failures = 0
restricted_domain_witnesses = 0

# Domain-only data is compatible with targets that agree on-domain and differ off-domain.
for domain in bits:
    if not (0 < sum(domain) < n):
        continue
    found = False
    for q in bits:
        for qp in bits:
            if q != qp and agrees_on_domain(q, qp, domain):
                found = True
                restricted_domain_witnesses += 1
                break
        if found:
            break
    if not found:
        restricted_domain_underdetermination_failures += 1

for E in partitions:
    for Q in targets:
        e_identifies = fibre_constant(E, Q)
        for A in bits:
            for Y in bits:
                X = experiment_signal(A, Y)
                T = joint(E, X)
                t_identifies = fibre_constant(T, Q)
                x_is_e_measurable = fibre_constant(E, X)

                if x_is_e_measurable:
                    postprocessing_cases += 1
                    if fibre_constant(T, Q) != e_identifies:
                        postprocessing_failures += 1

                if (not e_identifies) and t_identifies:
                    necessary_novel_signal_cases += 1
                    if x_is_e_measurable:
                        necessary_novel_signal_failures += 1

                if 0 < sum(A) < n and t_identifies:
                    v1_counterexamples += 1

                if (A == Q or A == tuple(1-q for q in Q)) and t_identifies:
                    target_leakage_totalizations += 1

# Frozen U/I/P controls.
E_uip = (0, 0, 0)
Q_uip = (1, 0, 0)
controls = {
    "common_proxy": ((1,1,1), (0,0,0)),
    "common_bearer": ((1,1,1), (1,1,0)),
    "target_laden_availability": ((1,0,0), (1,0,0)),
    "target_oracle_outcome": ((1,1,1), (1,0,0)),
}
uip = {}
for name, (A,Y) in controls.items():
    X = experiment_signal(A,Y)
    uip[name] = {
        "identifies_personal_target": fibre_constant(joint(E_uip,X), Q_uip),
        "signal_is_old_profile_measurable": fibre_constant(E_uip,X),
    }

result = {
    "schema": "PMR007_DEEP_CT_V2_PRIMARY_CHECK_RESULTS",
    "model_count": n,
    "evidence_partitions": len(partitions),
    "nonconstant_binary_targets": len(targets),
    "availability_vectors": len(bits),
    "outcome_vectors": len(bits),
    "postprocessing_cases": postprocessing_cases,
    "postprocessing_barrier_failures": postprocessing_failures,
    "successful_refinements_of_conflicted_profiles": necessary_novel_signal_cases,
    "successful_refinements_with_old_profile_measurable_signal": necessary_novel_signal_failures,
    "proper_domain_totalizations_identifying_target": v1_counterexamples,
    "target_or_complement_availability_totalizations": target_leakage_totalizations,
    "proper_domains_with_underdetermination_witness": restricted_domain_witnesses,
    "restricted_domain_underdetermination_failures": restricted_domain_underdetermination_failures,
    "uip_controls": uip,
    "overall": "PASS" if not any([
        postprocessing_failures,
        necessary_novel_signal_failures,
        restricted_domain_underdetermination_failures,
    ]) else "FAIL"
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["overall"] == "PASS" else 1)
