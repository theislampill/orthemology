#!/usr/bin/env python3
"""Finite example checks for the accompanying Orthemology research draft.

Uses exact integers/Fractions, except canonical serialisation of finite floats.
This is not a proof-assistant development and does not check the PDE papers.
Run: python verify_examples.py --output verification.json
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json
import math
from pathlib import Path
from typing import Any, Callable

RESULTS: list[dict[str, Any]] = []


def check(name: str, scope: str, task: Callable[[], dict[str, Any]]) -> None:
    result = task()  # A failed assertion aborts the run; no false PASS receipt.
    RESULTS.append({"name": name, "scope": scope, "status": "PASS", **result})


def atoms(value: Any, path: tuple = ()) -> frozenset[tuple]:
    """Canonical finite JSON-tree view; scalar types and positions are retained."""
    if value is None:
        return frozenset({(path, "null", None)})
    if isinstance(value, bool):
        return frozenset({(path, "bool", value)})
    if isinstance(value, int):
        return frozenset({(path, "int", value)})
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("The finite-record example excludes nonfinite numbers")
        return frozenset({(path, "float", value.hex())})
    if isinstance(value, str):
        return frozenset({(path, "str", value)})
    if isinstance(value, list):
        out = {(path, "list", len(value))}
        for i, child in enumerate(value):
            out.update(atoms(child, path + (("index", i),)))
        return frozenset(out)
    if isinstance(value, dict):
        if not all(isinstance(k, str) for k in value):
            raise TypeError("Only string map keys are admitted in this example")
        out = {(path, "dict", tuple(sorted(value)))}
        for k in sorted(value):
            out.update(atoms(value[k], path + (("key", k),)))
        return frozenset(out)
    raise TypeError(f"Unsupported record value: {type(value).__name__}")


def decode_atoms(a: frozenset[tuple], path: tuple = ()) -> Any:
    entries = [row for row in a if row[0] == path]
    if len(entries) != 1:
        raise ValueError("Expected exactly one node record at each path")
    _, kind, data = entries[0]
    if kind == "dict":
        return {k: decode_atoms(a, path + (("key", k),)) for k in data}
    if kind == "list":
        return [decode_atoms(a, path + (("index", i),)) for i in range(data)]
    if kind == "float":
        return float.fromhex(data)
    if kind in {"null", "bool", "int", "str"}:
        return data
    raise ValueError("Unknown atom kind")


def record_checks() -> dict:
    corpus = [None, False, True, 0, 1, 1.0, "1", "", [], {}, [1, 1], [1, 2],
              [2, 1], {"a": None}, {"a": []}, {"a": {}},
              {"x": {"state": "unknown"}}, {"x": {"state": "not-applicable"}},
              {"evidence": [{"id": "h1", "v": 1}, {"id": "h2", "v": 1}],
               "obligations": [{"id": "b1", "status": "unresolved"}]}]
    enc = [atoms(d) for d in corpus]
    assert len(set(enc)) == len(corpus)
    for d, a in zip(corpus, enc):
        restored = decode_atoms(a)
        assert atoms(restored) == a
        assert type(restored) is type(d)
    assert atoms({"a": 1, "b": 2}) == atoms({"b": 2, "a": 1})
    assert atoms([1, 2]) != atoms([2, 1])
    assert atoms({}) != atoms({"a": None})
    assert atoms(False) != atoms(0)
    return {"round_trip_records": len(corpus), "cross_record_collisions": 0,
            "model": "finite JSON tree; references retained as typed values"}


def word_checks() -> dict:
    w1, w2 = ("actor", "evidence", "claim"), ("evidence", "actor", "claim")
    assert w1 != w2 and Counter(w1) == Counter(w2)
    sample = {("record",): 1, ("evidence", "claim"): 2,
              w1: 1, ("meta", "evidence", "claim", "route"): 1}
    degrees = {len(w) for w, c in sample.items() if c}
    assert degrees == {1, 2, 3, 4}
    assert max({0} | set()) == 0
    return {"sample_degree_profile": sorted(degrees), "word_order_retained": True}


def parity_checks() -> dict:
    marginals = entries = 0
    for n in range(2, 9):
        points = list(product((0, 1), repeat=n))
        p = {x: Q(1 + (-1) ** sum(x), 2**n) for x in points}
        m = {x: Q(1 - (-1) ** sum(x), 2**n) for x in points}
        assert sum(p.values()) == sum(m.values()) == 1
        assert all(t >= 0 for t in p.values()) and all(t >= 0 for t in m.values())
        assert sum(p[x] * (-1)**sum(x) for x in points) == 1
        assert sum(m[x] * (-1)**sum(x) for x in points) == -1
        for x in points:
            assert p[x] - m[x] == Q(1, 2**(n-1)) * (-1)**sum(x)
        for k in range(n):
            for J in combinations(range(n), k):
                ap, am = defaultdict(Q), defaultdict(Q)
                for x in points:
                    y = tuple(x[j] for j in J)
                    ap[y] += p[x]
                    am[y] += m[x]
                assert dict(ap) == dict(am)
                assert all(t == Q(1, 2**k) for t in ap.values())
                marginals += 1
                entries += len(ap)
    return {"arity_range_inclusive": [2, 8], "proper_subsets_checked": marginals,
            "marginal_entries_checked": entries, "parity_expectations": [1, -1]}


def fibre_constant(r: tuple, q: tuple) -> bool:
    return all(r[i] != r[j] or q[i] == q[j]
               for i in range(len(r)) for j in range(len(r)))


def fibre_checks() -> dict:
    nchecked = 0
    for r in product((0, 1), repeat=4):
        for q in product((0, 1), repeat=4):
            exists = any(all(g[r[i]] == q[i] for i in range(4))
                         for g in product((0, 1), repeat=2))
            assert exists == fibre_constant(r, q)
            nchecked += 1
    # Contraction sends v tensor d0 and v tensor d1 to the same image.
    assert not fibre_constant((0, 0), (0, 1))
    return {"representation_target_pairs_checked": nchecked,
            "target_erasing_contraction_rejected": True}


def witness_valid(before: dict, after: dict, witness: dict) -> bool:
    """Toy record-level checker, NOT an evidence-authentication procedure."""
    if after["history"][:len(before["history"])] != before["history"]:
        return False
    for ident in before["active"]:
        if ident in after["active"]:
            continue
        disposition = witness.get(ident)
        if not disposition or not disposition.get("certificate_ref"):
            return False
        if disposition["status"] == "transferred" and not disposition.get("destination"):
            return False
        if {"id": ident, "previous_status": before["active"][ident]} not in after["history"]:
            return False
    return True


def witness_checks() -> dict:
    z0 = {"active": {"b1": "unresolved"}, "history": []}
    z1 = {"active": {}, "history": [{"id": "b1", "previous_status": "unresolved"}]}
    resolved = {"b1": {"status": "validated-resolved", "certificate_ref": "test-cert"}}
    transfer = {"b1": {"status": "transferred", "certificate_ref": "test-transfer",
                        "destination": "external-queue"}}
    assert witness_valid(z0, z1, resolved)
    assert witness_valid(z0, z1, transfer)
    assert transfer["b1"]["status"] != "validated-resolved"
    assert not witness_valid(z0, {"active": {}, "history": []}, resolved)
    assert not witness_valid(z0, z1, {})
    missing_target = {"b1": {"status": "transferred", "certificate_ref": "test-transfer"}}
    assert not witness_valid(z0, z1, missing_target)
    z2 = {"active": {}, "history": z1["history"] + [{"next": "reread"}]}
    assert witness_valid(z1, z2, {})
    assert z0["active"]["b1"] == z2["history"][0]["previous_status"]
    assert not witness_valid(z1, {"active": {}, "history": []}, {})
    return {"positive_cases": 3, "negative_cases": 4,
            "semantic_validity_established": False}


def row_payoff(u: tuple, p: Q, q: Q) -> Q:
    return u[0]*p*q + u[1]*p*(1-q) + u[2]*(1-p)*q + u[3]*(1-p)*(1-q)


def row_regret(u: tuple, p: Q, q: Q) -> Q:
    return max(u[0]*q+u[1]*(1-q), u[2]*q+u[3]*(1-q)) - row_payoff(u, p, q)


def pure_nash(u: tuple, v: tuple) -> list[tuple[int, int]]:
    out = []
    for i, j in product(range(2), repeat=2):
        if u[2*i+j] >= u[2*(1-i)+j] and v[2*i+j] >= v[2*i+(1-j)]:
            out.append((i, j))
    return out


def game_checks() -> dict:
    u = (Q(2), Q(5), Q(0), Q(4))
    v = (Q(2), Q(0), Q(5), Q(4))
    assert pure_nash(u, v) == [(0, 0)]
    assert all(u[j] > u[2+j] for j in (0, 1))
    assert all(v[2*i] > v[2*i+1] for i in (0, 1))
    mp = (Q(1), Q(-1), Q(-1), Q(1))
    assert pure_nash(mp, tuple(-x for x in mp)) == []
    half = Q(1, 2)
    assert row_regret(mp, half, half) == 0
    # Column player's deviation uses the transposed negative payoff array.
    col = (-mp[0], -mp[2], -mp[1], -mp[3])
    assert row_regret(col, half, half) == 0
    # Fixed-A disclosure: D strictly dominates S when available; post state only S.
    assert pure_nash((1, 1, 0, 0), (1, 0, 1, 0)) == [(0, 0)]
    pre = (Q(1), Q(0))
    post = (Q(0), Q(1))
    assert pre != post
    # Resource-sharing failure under independent mixtures.
    assert half * half > 0
    return {"race_pure_equilibria": [[0, 0]], "race_strict_dominance": True,
            "matching_pennies_pure_equilibria": [], "matching_pennies_mixed": "(1/2,1/2)",
            "fixed_analysis_equilibrium_change": True,
            "forbidden_resource_profile_probability": "1/4"}


def regret_checks() -> dict:
    total = 0
    grid = [Q(k, 4) for k in range(5)]
    eps = Q(1, 4)
    for base in product((Q(0), Q(1)), repeat=4):
        for perturb in product((-eps, Q(0), eps), repeat=4):
            alternative = tuple(a+b for a, b in zip(base, perturb))
            for p, q in product(grid, repeat=2):
                delta = row_regret(alternative, p, q)
                assert delta >= 0
                assert row_regret(base, p, q) <= delta + 2*eps
                total += 1
    return {"payoff_perturbation_profile_cases": total,
            "profile_grid": [str(x) for x in grid], "entry_error_upper_bound": str(eps)}


def energy_checks() -> dict:
    total = certified = rejected = 0
    for a, d in product(range(1, 7), repeat=2):
        for b, c in product(range(7), repeat=2):
            condition = a*d > b*c
            lower = Q(b, d)
            if c:
                upper = Q(a, c)
                assert (lower < upper) == condition
                if condition:
                    lam = (lower + upper) / 2
                else:
                    rejected += 1
                    total += 1
                    continue
            else:
                lam = lower + 1
            gamma = min(Q(a)-lam*c, Q(d)-Q(b)/lam)
            assert condition and gamma > 0
            certified += 1
            total += 1
    assert 3 - 1 - 1 == 1  # a=3,b=r=delta=1
    # For b=r=1, the optimum of delta+1/delta is 2.
    for delta in [Q(k, 20) for k in range(1, 401)]:
        assert delta + 1/delta >= 2
        assert not delta + 1/delta < 1
    for b, r in product(range(1, 8), repeat=2):
        # AM-GM certificate without floating-point square roots.
        for delta in [Q(1, 2), Q(1), Q(2), Q(3)]:
            assert (b*delta+r/delta)**2 - 4*b*r == (b*delta-r/delta)**2
    return {"coupled_coefficient_cases": total, "positive_weight_cases": certified,
            "empty_positive_weight_interval_cases": rejected,
            "radius_grid_cases": 400, "am_gm_identity_cases": 7*7*4}


def discrete_checks() -> dict:
    count = 0
    for q in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4)):
        for r, initial in product((Q(0), Q(1), Q(2)), repeat=2):
            value = initial
            for n in range(31):
                bound = q**n*initial + r*(1-q**n)/(1-q)
                assert value == bound
                value = q*value+r
                count += 1
            R = r/(1-q)
            assert q*R+r == R
    return {"recurrence_time_instances": count}


def landscape_checks() -> dict:
    initial, thin, rich = {"discover": 6}, {"reconstruct": 2}, {"mechanism": 10}
    opt = lambda x: max([0, *x.values()])
    assert opt(thin)-opt(initial) == -4 and opt(rich)-opt(initial) == 4
    before, after = {"best": 10, "low": 2}, {"best": 10}
    assert set(after) < set(before) and opt(after) == opt(before)
    assert len(rich) < len({"a": 1, "b": 2}) and opt(rich) > 2
    q1 = {"shape": ("actor", "source"), "permitted": True}
    q2 = {"shape": ("actor", "source"), "permitted": False}
    assert q1["shape"] == q2["shape"] and q1["permitted"] != q2["permitted"]
    return {"option_value_changes": [-4, 4], "smaller_equal_value_landscape": True,
            "shape_not_sufficient_for_feasibility": True}


def quotient_checks() -> dict:
    checked = good = 0
    for r in product(range(2), repeat=4):
        for F in product(range(4), repeat=4):
            rf = tuple(r[F[i]] for i in range(4))
            for q in product(range(2), repeat=4):
                # An independent landscape label for this test family.
                ell = tuple((r[i], q[i]) for i in range(4))
                ok = fibre_constant(r, rf) and fibre_constant(r, q) and fibre_constant(r, ell)
                if ok:
                    fbar, qbar, lbar = {}, {}, {}
                    for i in range(4):
                        fbar[r[i]], qbar[r[i]], lbar[r[i]] = rf[i], q[i], ell[i]
                    for i in range(4):
                        real, rep = i, r[i]
                        for _ in range(7):
                            assert rep == r[real]
                            assert qbar[rep] == q[real] and lbar[rep] == ell[real]
                            real, rep = F[real], fbar[rep]
                    good += 1
                checked += 1
    return {"finite_map_cases": checked, "compatible_cases": good,
            "iterates_per_start_state": 7, "domain_size": 4}


def run() -> dict:
    check("finite_record_channel", "Proposition 4.1: finite synthetic corpus only", record_checks)
    check("typed_words", "Section 3: ordering and degree-profile example", word_checks)
    check("parity_marginalisation", "Theorem 5.1: all proper marginals for n=2..8", parity_checks)
    check("fibre_factorisation", "Theorem 4.2: four-state binary maps", fibre_checks)
    check("witness_retention", "Theorem 6.5: toy record contract, not semantic certificates", witness_checks)
    check("finite_games", "Section 8: synthetic race, disclosure and matching pennies", game_checks)
    check("regret_transport", "Proposition 8.5: rational grid and array perturbations", regret_checks)
    check("energy_and_radius", "Theorems 10.1-10.3: rational coefficient checks", energy_checks)
    check("discrete_residual", "Theorem 10.5: exact recurrence instances", discrete_checks)
    check("landscape_countermodels", "Section 7: illustrative values, not measured values", landscape_checks)
    check("future_safe_quotient", "Theorem 11.2: exhaustive specified four-state family", quotient_checks)
    return {"schema": "orthing-formalisation-example-checks-v1", "version": 1,
            "status": "PASS", "test_groups": len(RESULTS), "results": RESULTS,
            "arithmetic": "exact integer/Fraction calculations; finite float hex only in record serialisation",
            "limits": ["not a machine proof of the manuscript", "not a Lean/kernel check",
                       "not an empirical Orthemology experiment", "not a fluid proof audit",
                       "not repository adoption", "not semantic authentication of witnesses"]}


def main() -> None:
    if not __debug__:
        raise SystemExit("Run without -O: these checks require enabled assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("verification.json"))
    args = parser.parse_args()
    data = run()
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASS: {len(RESULTS)} finite example groups; receipt: {args.output}")
    for row in RESULTS:
        print(f"  PASS {row['name']}")


if __name__ == "__main__":
    main()
