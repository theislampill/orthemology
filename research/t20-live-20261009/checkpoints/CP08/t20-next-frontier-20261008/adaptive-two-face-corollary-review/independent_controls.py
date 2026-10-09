#!/usr/bin/env python3
"""Independent direct transcript controls; run in a disposable copy to preserve freeze."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp

mp.mp.dps = 160


def chi(p, q):
    out = 0
    for key in set(p) | set(q):
        pp, qq = p.get(key, 0), q.get(key, 0)
        if qq == 0:
            assert pp == 0, (key, pp, qq)
        else:
            out += (pp - qq) ** 2 / qq
    return out


def kl(p, q):
    out = mp.mpf(0)
    for key, pp in p.items():
        qq = q[key]
        if pp:
            assert pp > 0 and qq > 0
            out += pp * mp.log(pp / qq)
    return out


def abstract_pair(A, B, delta):
    q = {(1, 1): A * B, (1, 0): A * (1 - B),
         (0, 1): (1 - A) * B, (0, 0): (1 - A) * (1 - B)}
    p = {key: val + (delta if key[0] == key[1] else -delta)
         for key, val in q.items()}
    assert min(p.values()) >= 0
    return p, q


def joe_pair(n, a, b):
    a, b = mp.mpf(a), mp.mpf(b)
    A, B = (1 - a) ** n, (1 - b) ** n
    if a in (0, 1) or b in (0, 1):
        delta = mp.mpf(0)
    else:
        c = mp.mpf(n) / (n + 1)
        S = (1 - a) ** c + (1 - b) ** c - (1 - a * b) ** c
        delta = S ** (n + 1) - A * B
    return abstract_pair(A, B, delta)


def transcript(A, tables, kernels):
    """Explicit branch masses; action label is retained. None denotes abort."""
    p, q = {}, {}
    for x in (0, 1):
        assert sum(weight for _, weight in kernels[x]) == 1
        for label, weight in kernels[x]:
            if label is None:
                p[(x, label, None)] = q[(x, label, None)] = weight * (A if x else 1 - A)
            else:
                pp, qq = tables[label]
                for y in (0, 1):
                    p[x, label, y], q[x, label, y] = weight * pp[x, y], weight * qq[x, y]
    return p, q


def expected_identity(A, tables, kernels):
    return sum((1 - A if x else A) * weight * chi(*tables[label])
               for x in (0, 1) for label, weight in kernels[x] if label is not None)


def close(x, y, tol=mp.mpf("1e-110")):
    assert abs(x - y) <= tol * max(1, abs(x), abs(y)), (x, y)


def serial(x):
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    if isinstance(x, F):
        return str(x)
    if isinstance(x, mp.mpf):
        return mp.nstr(x, 50)
    return x


def run():
    # Exact rational abstract controls do not use the Joe construction or floats.
    A = F(1, 5)
    tabs = {0: abstract_pair(A, F(2, 7), F(1, 70)),
            1: abstract_pair(A, F(3, 5), F(1, 100))}
    deterministic = {1: [(0, F(1))], 0: [(1, F(1))]}
    p, q = transcript(A, tabs, deterministic)
    exact = chi(p, q)
    assert exact == expected_identity(A, tabs, deterministic)
    swapped = A * chi(*tabs[0]) + (1 - A) * chi(*tabs[1])
    assert exact != swapped
    random_abort = {1: [(0, F(1, 2)), (1, F(1, 3)), (None, F(1, 6))],
                   0: [(0, F(1, 5)), (1, F(2, 5)), (None, F(2, 5))]}
    rp, rq = transcript(A, tabs, random_abort)
    assert chi(rp, rq) == expected_identity(A, tabs, random_abort)
    # A hidden random action can strictly reduce information.
    cp, cq = {}, {}
    for old_key in rp:
        key = (old_key[0], old_key[2])
        cp[key] = cp.get(key, 0) + rp[old_key]
        cq[key] = cq.get(key, 0) + rq[old_key]
    assert chi(cp, cq) < chi(rp, rq)

    max_residual = mp.mpf(0)
    cases = 0
    boundary_cases = 0
    max_kl_over_chi = mp.mpf(0)
    for n in [1, 3, 13, 64]:
        rates = [mp.mpf(0), mp.mpf("1e-12"), mp.mpf("0.08") / n,
                 1 - mp.exp(-mp.mpf("1.59362426") / n),
                 mp.mpf("0.63"), mp.mpf(1)]
        for a in rates:
            AA = (1 - a) ** n
            ts = {i: joe_pair(n, a, b) for i, b in enumerate(rates)}
            fixed_max = max(chi(*tab) for tab in ts.values())
            adaptive_max = mp.mpf(0)
            for i in ts:
                for j in ts:
                    ks = {1: [(i, mp.mpf(1))], 0: [(j, mp.mpf(1))]}
                    pp, qq = transcript(AA, ts, ks)
                    actual = chi(pp, qq)
                    predicted = expected_identity(AA, ts, ks)
                    max_residual = max(max_residual, abs(actual - predicted))
                    close(actual, predicted)
                    assert actual <= fixed_max + mp.mpf("1e-110")
                    adaptive_max = max(adaptive_max, actual)
                    D = kl(pp, qq)
                    assert D <= actual + mp.mpf("1e-110")
                    # Independent corroboration of the general two-branch KL bound.
                    assert D <= kl(*ts[i]) + kl(*ts[j]) + mp.mpf("1e-110")
                    if actual:
                        max_kl_over_chi = max(max_kl_over_chi, D / actual)
                    if a in (0, 1):
                        assert actual == 0
                        boundary_cases += 1
                    cases += 1
            close(adaptive_max, fixed_max)
    # A geometric screening protocol: all failed first probes must be counted.
    n = 3
    a, b = mp.mpf("0.6"), mp.mpf("0.4")
    AA = (1 - a) ** n
    pp, qq = joe_pair(n, a, b)
    d_success = sum(pp[1, y] / AA * mp.log(pp[1, y] / qq[1, y]) for y in (0, 1))
    ks = {1: [(0, mp.mpf(1))], 0: [(None, mp.mpf(1))]}
    one_p, one_q = transcript(AA, {0: (pp, qq)}, ks)
    one_kl = kl(one_p, one_q)
    close(one_kl, AA * d_success)
    expected_attempts = 1 / AA
    close(expected_attempts * one_kl, d_success)

    # Enumerate a stopped, history-dependent two-attempt tree from complete masses.
    aa = mp.mpf("0.12")
    first_tables = {0: joe_pair(3, aa, mp.mpf("0.2"))}
    first_p, first_q = transcript((1-aa)**3, first_tables, ks)
    terminal_p, terminal_q = {}, {}
    chain = kl(first_p, first_q)
    expected_tree_attempts = mp.mpf(1)
    expected_tree_endpoints = 1 + (1-aa)**3
    local_max = kl(first_p, first_q)
    for h in first_p:
        if h[0] == 1 and h[2] == 1:
            terminal_p[h, None], terminal_q[h, None] = first_p[h], first_q[h]
            continue
        aa2 = mp.mpf("0.07") if h[0] == 1 else mp.mpf("0.43")
        second_tables = {0: joe_pair(3, aa2, mp.mpf("0.13")),
                         1: joe_pair(3, aa2, mp.mpf("0.64"))}
        second_kernels = {1: [(0, mp.mpf(1))], 0: [(1, mp.mpf(1))]}
        second_p, second_q = transcript((1-aa2)**3, second_tables, second_kernels)
        second_d = kl(second_p, second_q)
        local_max = max(local_max, second_d)
        chain += first_p[h] * second_d
        expected_tree_attempts += first_p[h]
        expected_tree_endpoints += 2 * first_p[h]
        for h2 in second_p:
            terminal_p[h, h2] = first_p[h] * second_p[h2]
            terminal_q[h, h2] = first_q[h] * second_q[h2]
    direct_tree_kl = kl(terminal_p, terminal_q)
    close(direct_tree_kl, chain)
    assert direct_tree_kl <= local_max * expected_tree_attempts
    assert expected_tree_endpoints >= expected_tree_attempts

    # Direct high-precision S formula, independent of the author's log-domain code.
    free_screening = []
    with mp.workdps(550):
        for nn in [1, 3, 13, 64]:
            c = mp.mpf(nn) / (nn + 1)
            y = mp.power(2, -mp.mpf(1) / nn)
            old_ratio = mp.mpf(0)
            for k in [1, 2, 4]:
                x = mp.power(10, -k * (nn + 1))
                S = x**c + y**c - (y + x*(1-y))**c
                ratio = S ** (nn + 1) / x**nn
                assert mp.mpf("0.75") < ratio < 1 and ratio > old_ratio
                old_ratio = ratio
                free_screening.append({"n": nn, "k": k,
                                       "selected_Joe_absence_probability": ratio,
                                       "expected_first_probe_cost_log10": k*nn*(nn+1)})
    out = {
        "status": "PASS",
        "precision_decimal_digits": mp.mp.dps,
        "method": "Independent rational table arithmetic and explicit Joe transcript enumeration; no author module imports",
        "exact_rational": {
            "adaptive_chi_squared": exact, "incorrect_swapped_weights": swapped,
            "randomized_abort_chi_squared": chi(rp, rq),
            "coarsened_action_chi_squared": chi(cp, cq),
            "strict_coarsening_loss": chi(rp, rq) - chi(cp, cq)},
        "joe_grid": {"transcripts": cases, "deterministic_first_bit_transcripts": boundary_cases,
                     "max_absolute_identity_residual": max_residual,
                     "finite_grid_supremum_identity": "PASS for each first rate and n",
                     "general_kl_factor_two_envelope": "PASS", "max_kl_over_chi": max_kl_over_chi},
        "screening": {"first_branch_probability": AA, "one_attempt_kl": one_kl,
                      "eventual_selected_second_bit_kl": d_success,
                      "expected_attempts": expected_attempts,
                      "expected_endpoint_probes": expected_attempts + 1,
                      "expected_completed_pairs": 1,
                      "cost_warning": "Charging only the completed pair discards all screening costs"},
        "stopped_adaptive_tree": {"terminal_atoms": len(terminal_p),
                                  "direct_transcript_kl": direct_tree_kl,
                                  "conditional_chain_rule_kl": chain,
                                  "expected_attempts_world_1": expected_tree_attempts,
                                  "expected_endpoints_world_1": expected_tree_endpoints,
                                  "max_conditional_kl_times_expected_attempts": local_max * expected_tree_attempts},
        "free_screening_limit": {"precision_decimal_digits": 550, "cases": free_screening},
        "limits": "Finite numerical grids and rational identities are controls; the prose review establishes universal, continuous-kernel, and stopping claims."
    }
    return serial(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("CONTROL_RESULTS.json"))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
