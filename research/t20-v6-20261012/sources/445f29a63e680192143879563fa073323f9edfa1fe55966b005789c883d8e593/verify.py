"""Exact finite controls for source-audit revision. Standard library only.

These controls corroborate the written algebra; they do not prove its universal
quantifiers, certify an empirical channel, or determine anyone's warrant.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def norm(xs):
    s = sum(xs)
    assert s > 0
    return tuple(x / s for x in xs)


def model(bad=(F(1, 2), F(1, 2)), good_accuracy=F(9, 10),
          bad_accuracy=F(1, 2), verifier_accuracy=F(4, 5)):
    """Joint (theta,t,y,v,d), theta uniform; t=1 means Bad.

    Conditional on theta,t, Y and V use independent draws. D=[Y != V].
    A=(t,d) is an observed audit, not an intervention.
    """
    rows = []
    for theta, t, y, v in product(range(2), repeat=4):
        pt = bad[theta] if t else 1 - bad[theta]
        ac = bad_accuracy if t else good_accuracy
        py = ac if y == theta else 1 - ac
        pv = verifier_accuracy if v == theta else 1 - verifier_accuracy
        rows.append((dict(theta=theta, t=t, y=y, v=v, d=int(y != v)),
                     F(1, 2) * pt * py * pv))
    assert sum(p for _, p in rows) == 1
    return rows


def mass(rows, **event):
    return sum((p for r, p in rows if all(r[k] == v for k, v in event.items())), F(0))


def cond(rows, event, given):
    assert all(k not in given or given[k] == v for k, v in event.items())
    den = mass(rows, **given)
    assert den > 0
    return mass(rows, **(given | event)) / den


def post(rows, **event):
    return cond(rows, {"theta": 1}, event)


def risk(p, q):
    """Binary proper loss from F(vector)=||vector||^2/2."""
    return p * (1 - q) ** 2 + (1 - p) * q ** 2


def main_controls():
    m = model()
    event = {"y": 1, "t": 1, "d": 1}
    old = post(m, y=1)
    full = post(m, **event)
    audit_only = post(m, t=1, d=1)
    old_l = tuple(cond(m, {"y": 1}, {"theta": t}) for t in range(2))
    audit_seq = tuple(cond(m, {"t": 1, "d": 1}, {"theta": t, "y": 1})
                      for t in range(2))
    audit_marg = tuple(cond(m, {"t": 1, "d": 1}, {"theta": t}) for t in range(2))
    new_l = tuple(cond(m, {"y": 1}, {"theta": t, "t": 1, "d": 1})
                  for t in range(2))
    assert old == F(7, 10)
    assert full == F(1, 5)
    assert audit_only == F(1, 2)
    assert old_l == (F(3, 10), F(7, 10))
    assert audit_seq == (F(2, 3), F(1, 14))
    assert audit_marg == (F(1, 4), F(1, 4))
    assert new_l == (F(4, 5), F(1, 5))
    assert norm(tuple(p * k for p, k in zip((1 - old, old), audit_seq)))[1] == full
    assert norm(tuple(F(1, 2) * a * l for a, l in zip(audit_marg, new_l)))[1] == full
    # Divide old L but retain the Y-conditional audit: a different, also wrong rule.
    divided_sequential = norm(audit_seq)[1]
    assert divided_sequential == F(3, 31)
    # Innocent audit control: learn only Bad; it screens off Y exactly.
    assert post(m, y=1, t=1) == post(m, t=1) == F(1, 2)
    # Losing authority/access by independent random coin does not change the old posterior.
    assert norm(tuple(p * F(1, 3) for p in (1 - old, old)))[1] == old
    # Actual false-report finding gives the complement, not the prior.
    false_rows = [(r | {"false": int(r["y"] != r["theta"])}, p) for r, p in m]
    assert post(false_rows, y=1, false=1) == 0
    # Known adversarial source remains evidence, in the reverse direction.
    anti = model(bad_accuracy=F(1, 10))
    assert post(anti, y=1, t=1) == F(1, 10)
    # Parent-supplied audit-only informative control, checked by the same joint engine.
    parent = model(bad=(F(1, 4), F(3, 4)), good_accuracy=F(3, 4))
    assert tuple(cond(parent, {"y": 1}, {"theta": t}) for t in range(2)) == (F(5, 16), F(9, 16))
    assert post(parent, y=1) == F(9, 14)
    assert post(parent, y=1, t=1) == post(parent, t=1) == F(3, 4)

    # Expected audit information minus regret, conditional on actual initial Y=1.
    p = old
    expected_full_risk = expected_hybrid_risk = information = regret = F(0)
    branches = []
    for t, d in product(range(2), repeat=2):
        w = cond(m, {"t": t, "d": d}, {"y": 1})
        q = post(m, y=1, t=t, d=d)
        r = post(m, t=t, d=d) if t else q
        information += w * (q - p) ** 2
        regret += w * (q - r) ** 2
        expected_full_risk += w * risk(q, q)
        expected_hybrid_risk += w * risk(q, r)
        branches.append({"t": t, "d": d, "mass_given_y1": w, "full": q, "hybrid": r})
    assert sum(b["mass_given_y1"] * b["full"] for b in branches) == p
    assert risk(p, p) - expected_full_risk == information
    assert expected_hybrid_risk - expected_full_risk == regret == F(9, 200)
    assert risk(p, p) - expected_hybrid_risk == information - regret

    # Full audit-aware deletion for every t has exact conditional Jensen regret.
    fine_risk = coarse_risk = divergence = F(0)
    for y, t, d in product(range(2), repeat=3):
        w = mass(m, y=y, t=t, d=d)
        q = post(m, y=y, t=t, d=d)
        r = post(m, t=t, d=d)
        fine_risk += w * risk(q, q)
        coarse_risk += w * risk(q, r)
        divergence += w * (q - r) ** 2
    assert coarse_risk - fine_risk == divergence

    # Shared calibration changes a retained report's likelihood too.
    shared = []
    for theta, t, y1, y2 in product(range(2), repeat=4):
        ac = F(9, 10) if not t else F(1, 2)
        py1 = ac if y1 == theta else 1 - ac
        py2 = ac if y2 == theta else 1 - ac
        shared.append((dict(theta=theta, t=t, y1=y1, y2=y2), F(1, 4) * py1 * py2))
    assert post(shared, y1=1, y2=1) == F(53, 66)
    assert post(shared, y1=1, y2=1, t=1) == F(1, 2)
    assert post(shared, y2=1) == F(7, 10)

    return {"selected_bad_source": {"old": old, "full": full, "audit_aware_deletion": audit_only,
                                    "divided_sequential": divided_sequential,
                                    "old_likelihood_theta0_theta1": old_l,
                                    "audit_sequential_theta0_theta1": audit_seq,
                                    "replacement_report_likelihood_theta0_theta1": new_l},
            "parent_audit_only_control": {"old": F(9, 14), "full": F(3, 4), "bare_deletion": F(1, 2)},
            "audit_branches_given_y1": branches,
            "score": {"information_given_y1": information, "hybrid_regret_given_y1": regret,
                      "hybrid_gain_given_y1": information - regret,
                      "full_coarsening_regret": divergence},
            "shared_calibration": {"old_joint": F(53, 66), "full_after_bad": F(1, 2),
                                   "keep_other_old_likelihood": F(7, 10)}}


def exhaustive_binary_tables():
    """All 6,400 nonzero-row binary table specifications with entries 0,1,2.

    Enumerate full joint likelihood tables, without an independence premise.
    Direct marginalization is compared to each criterion and factorization.
    """
    rows = [v for v in product(range(3), repeat=4) if sum(v)]
    normalized = [tuple(F(x, sum(v)) for x in v) for v in rows]
    counts = dict(table_specifications=0, unique_normalized_channels=len(set(normalized)) ** 2,
                  positive_events=0, audit_deletion_exact=0,
                  bare_deletion_exact=0, inverse_factor_cases=0,
                  inverse_then_conditional_audit_exact=0, zero_support_events=0)
    for k in product(normalized, repeat=2):
        counts["table_specifications"] += 1
        for prior1 in (F(1, 3), F(1, 2), F(2, 3)):
            prior = (1 - prior1, prior1)
            for y, a in product(range(2), repeat=2):
                j = y * 2 + a
                likelihood = tuple(k[t][j] for t in range(2))
                event_mass = sum(prior[t] * likelihood[t] for t in range(2))
                if not event_mass:
                    continue
                counts["positive_events"] += 1
                full = norm(tuple(prior[t] * likelihood[t] for t in range(2)))
                ma = tuple(k[t][a] + k[t][2 + a] for t in range(2))
                ly = tuple(k[t][2 * y] + k[t][2 * y + 1] for t in range(2))
                coarse = norm(tuple(prior[t] * ma[t] for t in range(2)))
                support = [t for t in range(2) if coarse[t]]
                residuals = [likelihood[t] / ma[t] for t in support]
                flat = len(set(residuals)) == 1
                assert (full == coarse) == flat
                counts["audit_deletion_exact"] += int(flat)
                bare_flat = len(set(likelihood)) == 1
                assert (full == prior) == bare_flat
                counts["bare_deletion_exact"] += int(bare_flat)
                # Audit-first replacement, including support zeros.
                replacement = tuple(coarse[t] * (likelihood[t] / ma[t] if ma[t] else 0)
                                    for t in range(2))
                assert norm(replacement) == full
                if any(not x for x in likelihood + ma + ly):
                    counts["zero_support_events"] += 1
                if all(ly):
                    counts["inverse_factor_cases"] += 1
                    old = norm(tuple(prior[t] * ly[t] for t in range(2)))
                    seq = tuple(likelihood[t] / ly[t] for t in range(2))
                    assert norm(tuple(old[t] * seq[t] for t in range(2))) == full
                    assert norm(tuple(old[t] / ly[t] * ma[t] for t in range(2))) == coarse
                    divided_seq = norm(tuple(old[t] / ly[t] * seq[t] for t in range(2)))
                    seq_support = [t for t in range(2) if divided_seq[t]]
                    old_flat_on_seq = len({ly[t] for t in seq_support}) == 1
                    assert (divided_seq == full) == old_flat_on_seq
                    counts["inverse_then_conditional_audit_exact"] += int(old_flat_on_seq)
    assert counts["table_specifications"] == 6400
    assert counts["unique_normalized_channels"] == 4225
    # Eventwise support, not global flatness, determines equality for a restricted prior.
    p = (F(1), F(0))
    assert norm((p[0] * F(1, 7), p[1] * F(4, 7))) == p
    return counts


def custody_check():
    saved = json.loads((ROOT / "INPUT_BINDINGS.json").read_text())
    for row in saved["inputs"]:
        b = (ROOT / "inputs" / row["path"]).read_bytes()
        assert len(b) == row["bytes"]
        assert hashlib.sha256(b).hexdigest() == row["sha256"]
        original = ROOT.parent / row["path"]
        if original.exists():
            assert hashlib.sha256(original.read_bytes()).hexdigest() == row["sha256"]
    return len(saved["inputs"])


def null_audit_controls():
    """Parent-supplied null-audit perturbation, tested in three-state models."""
    p = (F(1, 2), F(1, 3), F(1, 6))
    qs = [(F(1, 3),) * 3, (F(4, 5), F(1, 10), F(1, 10)),
          (F(1, 10), F(1, 10), F(4, 5)), (F(0), F(1), F(0))]
    n = 0
    for q in qs:
        for eps in (F(1, 16), F(1, 256), F(1, 65536)):
            a1 = tuple(eps * v for v in q)
            a0 = tuple(x - z for x, z in zip(p, a1))
            assert all(v >= 0 for v in a0)
            assert tuple(x + z for x, z in zip(a0, a1)) == p
            assert sum(a1) == eps
            assert norm(a1) == q
            tv = (sum(abs(x - z) for x, z in zip(a0, p)) + sum(a1)) / 2
            assert tv == eps
            n += 1
    return {"cases": n, "fixed_prior": p, "different_audit_posteriors": qs,
            "distance_to_same_null_audit_model": "epsilon exactly"}


if __name__ == "__main__":
    result = {"status": "PASS", "method": "exact Fraction joint-table marginalization",
              "examples": main_controls(), "exhaustive": exhaustive_binary_tables(),
              "zero_probability_audit": null_audit_controls(),
              "unchanged_input_files": custody_check(),
              "ceiling": "Finite controls; no empirical, psychological, formal-kernel, or warrant certification."}
    print(json.dumps(result, default=str, indent=2))
