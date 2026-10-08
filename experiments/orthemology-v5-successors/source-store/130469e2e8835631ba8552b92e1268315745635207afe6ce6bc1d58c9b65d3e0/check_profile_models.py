#!/usr/bin/env python3
"""Bounded exhaustive audit of an elementary complete-profile exclusion lemma.

This checks finite interpretations only. It does not verify an account of divine
nature, establish metaphysical possibilities, or supply philosophical premises.
No external packages are required.
"""
from itertools import product
import json, hashlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent

def strictly_better(x, y):
    """All listed fidelity respects nondecreasing, at least one strictly better."""
    return all(a <= b for a,b in zip(x,y)) and any(a < b for a,b in zip(x,y))

def has_target_repair(K, x, i):
    return any(y[i] == 1 and strictly_better(x,y) for y in K)

def nonspoiling_repair(K):
    return all(has_target_repair(K,x,i) for x in K for i,b in enumerate(x) if b == 0)

def nondominated(K,x):
    return not any(strictly_better(x,y) for y in K)

def local_eligibility(K):
    return all(any(x[i] == 1 for x in K) for i in range(len(K[0])))

def describe(K, actual):
    return {
        "eligible_complete_profiles": K,
        "actual": actual,
        "local_truthful_eligibility_every_context": local_eligibility(K),
        "complete_nonspoiling_repair_R_P": nonspoiling_repair(K),
        "actual_nondomination_N": nondominated(K,actual),
        "actual_nonlying": all(actual),
        "actual_genuine_assurance_role": True,
        "relevant_actual_knowledge": True,
        "intentional_good_episode_elsewhere": True,
        "truth_conditions_or_assertoric_role_redefined": False,
        "maximal_profiles": [x for x in K if nondominated(K,x)],
    }

def assertion_semantics(bit):
    # The physical proposition is fixed. Response content alone varies.
    safe_fact=False
    believes_safe=False
    asserts_safe=not bool(bit)
    result={"profile_bit":bit,"root_safe_fact":safe_fact,
            "speaker_believes_root_safe":believes_safe,
            "asserts_root_safe":asserts_safe,
            "genuine_assertoric_assurance_role":True,
            "lying":asserts_safe != believes_safe,
            "assertion_true":asserts_safe == safe_fact,
            "relevant_knowledge":believes_safe == safe_fact}
    assert result["lying"] == (bit == 0)
    assert result["assertion_true"] == (bit == 1)
    assert result["relevant_knowledge"]
    return result

semantics=[assertion_semantics(bit) for bit in (0,1)]
rows=[]
for n in range(1,5):
    U=list(product((0,1),repeat=n)); m=len(U)
    # Precompute target repair bitsets. This is independent of the later
    # top-profile sanity check and avoids treating the theorem as its premise.
    repairs={}
    dominators=[]
    for j,x in enumerate(U):
        dominators.append(sum(1<<k for k,y in enumerate(U) if strictly_better(x,y)))
        for i,v in enumerate(x):
            if not v:
                repairs[j,i]=sum(1<<k for k,y in enumerate(U) if y[i] and strictly_better(x,y))
    c={"contexts":n,"nonempty_profile_sets":0,"actual_profile_checks":0,
       "sets_satisfying_R_P":0,"theorem_applications":0,"violations":0,
       "local_eligibility_plus_N_bad_actual":0}
    for mask in range(1,1<<m):
        js=[j for j in range(m) if mask & (1<<j)]
        c["nonempty_profile_sets"]+=1
        R=all(mask & repairs[j,i] for j in js for i,v in enumerate(U[j]) if not v)
        # In these finite binary-coordinate interpretations R is independently
        # equivalent to inclusion of the all-1 profile. This is not assumed.
        assert R == bool(mask & (1 << (m-1)))
        c["sets_satisfying_R_P"]+=bool(R)
        local=all(any(U[j][i] for j in js) for i in range(n))
        for j in js:
            c["actual_profile_checks"]+=1
            N=not bool(mask & dominators[j])
            good=all(U[j])
            if R and N:
                c["theorem_applications"]+=1
                if not good:c["violations"]+=1
            if local and N and not good:
                c["local_eligibility_plus_N_bad_actual"]+=1
    assert c["violations"]==0
    rows.append(c)

coupled=[(1,0),(0,1)]
uncoupled=list(product((0,1),repeat=2))
assert local_eligibility(coupled) and nondominated(coupled,(1,0))
assert not nonspoiling_repair(coupled) and not all((1,0))
assert nonspoiling_repair(uncoupled) and not nondominated(uncoupled,(1,0))

# Different faithful permissible continuations: no total ordering and no unique
# complete history. Styles are alternatives, not a numerical perfection rank.
styles=[(x,style) for x in uncoupled for style in ('brief','detailed')]
def better_style(a,b):
    return a[1]==b[1] and strictly_better(a[0],b[0])
max_styles=[a for a in styles if not any(better_style(a,b) for b in styles)]
assert max_styles==[((1,1),'brief'),((1,1),'detailed')]
assert not better_style(max_styles[0],max_styles[1])
assert not better_style(max_styles[1],max_styles[0])

# Lie is opposed to what the agent takes true. Relevant factual knowledge is a
# separate premise. This error control is not claimed possible for an omniscient
# source; it checks that T0 has not silently been redefined as omniscience.
error={"safe":False,"speaker_believes_safe":True,"asserts_safe":True}
error["lying"] = error["asserts_safe"] != error["speaker_believes_safe"]
error["assertion_true"] = error["asserts_safe"] == error["safe"]
error["relevant_knowledge"] = error["speaker_believes_safe"] == error["safe"]
assert not error["lying"] and not error["assertion_true"] and not error["relevant_knowledge"]

result={
    "schema":"ninth-integrity-complete-profile-finite-check-v2",
    "epistemic_scope":"Exhaustive finite mathematical check, not metaphysical possibility or source-nature proof",
    "fidelity_encoding":{"1":"accurate assertion unsafe, with relevant knowledge; role retained",
                         "0":"deliberate false assertion safe, with relevant knowledge; role retained"},
    "assertion_semantics":semantics,
    "finite_R_meaning":"R_P; it supplies generic R_G for the stated componentwise order",
    "exhaustive_bounds":rows,
    "totals":{k:sum(r[k] for r in rows) for k in rows[0] if k!='contexts'},
    "coupled_countermodel":describe(coupled,(1,0)),
    "nondomination_removed":describe(uncoupled,(1,0)),
    "multiple_incomparable_nondominated_profiles":max_styles,
    "T0_does_not_supply_relevant_knowledge":error,
    "infinite_case":"Analytical only: finite-support truthful subsets of N have target repairs but no nondominated member",
    "script_sha256":hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
}
(HERE/'PROFILE_MODEL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
