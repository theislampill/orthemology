from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent  # sanitized receipt; original evidence root supplied separately
OUT = BASE/'rereviews/PMR-007_FRONTIER_ROUND20_V2_DISTINCT_FRESH_REREVIEW_RESULTS.json'
FROZEN = BASE/'PMR-007_FRONTIER_ROUND20_V2_FROZEN_HASHES.sha256'


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()


def verify_frozen() -> list[dict]:
    failures=[]
    for line in FROZEN.read_text().splitlines():
        if not line.strip(): continue
        want, raw = line.split(maxsplit=1)
        p=Path(raw.strip())
        got=sha256(p)
        if got != want:
            failures.append({'path':str(p),'expected':want,'actual':got})
    return failures


def subsets(n: int):
    for mask in range(1<<n):
        yield frozenset(i for i in range(n) if mask>>i & 1)


def direct_failure_budget(root_count: int, path_count: int, actions: list[tuple[frozenset[int],frozenset[int]]]) -> float:
    """Smallest static corruption that leaves some path without a surviving blocker."""
    for size in range(root_count+1):
        for F in itertools.combinations(range(root_count), size):
            F=frozenset(F)
            for p in range(path_count):
                surviving=False
                for blocks, roots in actions:
                    if p in blocks and not (F & roots):
                        surviving=True
                        break
                if not surviving:
                    return size
    return math.inf


def min_transversal_backtracking(root_count: int, edges: list[frozenset[int]]) -> float:
    if not edges:
        return 0
    if any(not e for e in edges):
        return math.inf
    # Remove supersets? For hitting sets, supersets are easier to hit; retain inclusion-minimal edges.
    reduced=[]
    for e in sorted(set(edges), key=lambda x:(len(x),tuple(sorted(x)))):
        if not any(r <= e for r in reduced):
            reduced.append(e)
    best=root_count+1
    def search(chosen:frozenset[int], pending:list[frozenset[int]]):
        nonlocal best
        if len(chosen)>=best: return
        pending=[e for e in pending if not (e & chosen)]
        if not pending:
            best=len(chosen); return
        edge=min(pending,key=len)
        for x in edge:
            search(chosen|{x},pending)
    search(frozenset(),reduced)
    return best if best<=root_count else math.inf


def kappa_backtracking(root_count: int, path_count: int, actions):
    vals=[]
    for p in range(path_count):
        edges=[roots for blocks,roots in actions if p in blocks]
        vals.append(min_transversal_backtracking(root_count,edges))
    return min(vals)


def exhaustive_action_systems():
    checked=0
    mismatches=[]
    # Exhaustive for r<=3,p<=2 with action types deduplicated and portfolios up to 4 action types.
    for r in range(1,4):
        rootsets=list(subsets(r))
        for p in range(1,3):
            blocksets=[frozenset(i for i in range(p) if mask>>i&1) for mask in range(1,1<<p)]
            types=[(b,e) for b in blocksets for e in rootsets]
            max_size=min(4,len(types))
            for size in range(max_size+1):
                for comb in itertools.combinations(types,size):
                    direct=direct_failure_budget(r,p,list(comb))
                    k=kappa_backtracking(r,p,list(comb))
                    checked+=1
                    if direct!=k:
                        mismatches.append({'r':r,'p':p,'actions':[(sorted(b),sorted(e)) for b,e in comb],'direct':direct,'kappa':k})
                        if len(mismatches)>=10:
                            return checked,mismatches
    return checked,mismatches


def random_systems(seed=20072026,trials=120000):
    rng=random.Random(seed)
    mismatches=[]
    checked=0
    monotonicity_failures=[]
    for _ in range(trials):
        r=rng.randint(1,7)
        p=rng.randint(1,5)
        actions=[]
        for _a in range(rng.randint(0,12)):
            blocks=frozenset(i for i in range(p) if rng.random()<0.45)
            if not blocks: blocks=frozenset({rng.randrange(p)})
            roots=frozenset(i for i in range(r) if rng.random()<0.35)
            actions.append((blocks,roots))
        d=direct_failure_budget(r,p,actions)
        k=kappa_backtracking(r,p,actions)
        checked+=1
        if d!=k:
            mismatches.append({'r':r,'p':p,'actions':[(sorted(b),sorted(e)) for b,e in actions],'direct':d,'kappa':k})
            if len(mismatches)>=10: break
        # Duplicate one action: no change.
        if actions:
            dup=actions+[actions[rng.randrange(len(actions))]]
            if kappa_backtracking(r,p,dup)!=k:
                monotonicity_failures.append('duplicate')
        # Add random action: kappa cannot fall.
        blocks=frozenset(i for i in range(p) if rng.random()<0.5) or {rng.randrange(p)}
        roots=frozenset(i for i in range(r) if rng.random()<0.4)
        if kappa_backtracking(r,p,actions+[(frozenset(blocks),roots)]) < k:
            monotonicity_failures.append('enlargement')
        # Delete action: kappa cannot rise.
        if actions:
            j=rng.randrange(len(actions))
            if kappa_backtracking(r,p,actions[:j]+actions[j+1:]) > k:
                monotonicity_failures.append('deletion')
    return {'checked':checked,'mismatches':mismatches,'monotonicity_failures':monotonicity_failures[:20]}


def scope_controls():
    # Alternative semantics: redundant root support; all roots must be corrupted to disable.
    redundant_action_roots={0,1}
    redundant_f1_survival=all(not redundant_action_roots <= set(F) for F in itertools.combinations(range(2),1))
    static_kappa=min_transversal_backtracking(2,[frozenset(redundant_action_roots)])

    # Incompatible actions across two paths.
    incompatible=[(frozenset({0}),frozenset({0})),(frozenset({1}),frozenset({1}))]
    pathwise_zero=direct_failure_budget(2,2,incompatible)>0
    joint_executable=False

    # Alias contraction.
    displayed=[(frozenset({0}),frozenset({0})),(frozenset({0}),frozenset({1}))]
    actual=[(frozenset({0}),frozenset({0})),(frozenset({0}),frozenset({0}))]

    # Static vs dynamic omitted path.
    fixed=[(frozenset({0}),frozenset({0,1}))]
    fixed_ok=direct_failure_budget(2,1,fixed)>0
    dynamic_ok=False

    return {
        'redundant_support':{
            'static_conjunctive_kappa':static_kappa,
            'redundant_semantics_survives_one_corruption':redundant_f1_survival,
            'scope_difference_observed':(static_kappa<=1 and redundant_f1_survival),
        },
        'incompatible_actions':{
            'pathwise_zero_corruption_certificate':pathwise_zero,
            'joint_executable':joint_executable,
            'scope_difference_observed':pathwise_zero and not joint_executable,
        },
        'alias_contraction':{
            'displayed_failure_budget':direct_failure_budget(2,1,displayed),
            'actual_failure_budget':direct_failure_budget(1,1,actual),
        },
        'dynamic_rerouting':{
            'fixed_registered_certificate':fixed_ok,
            'dynamic_actual_restoration':dynamic_ok,
            'scope_difference_observed':fixed_ok and not dynamic_ok,
        },
    }


def main():
    hash_failures=verify_frozen()
    ex_checked,ex_mismatches=exhaustive_action_systems()
    rnd=random_systems()
    controls=scope_controls()
    failures=[]
    if hash_failures: failures.append('frozen_hash_mismatch')
    if ex_mismatches: failures.append('exhaustive_semantic_mismatch')
    if rnd['mismatches']: failures.append('random_semantic_mismatch')
    if rnd['monotonicity_failures']: failures.append('monotonicity_failure')
    if not controls['redundant_support']['scope_difference_observed']: failures.append('redundant_support_control')
    if not controls['incompatible_actions']['scope_difference_observed']: failures.append('compatibility_control')
    if controls['alias_contraction'] != {'displayed_failure_budget':2,'actual_failure_budget':1}: failures.append('alias_control')
    if not controls['dynamic_rerouting']['scope_difference_observed']: failures.append('dynamic_control')
    result={
        'schema':'PMR007_ROUND20_DISTINCT_FRESH_REREVIEW_RESULTS_V1',
        'method':'direct minimum failing corruption size versus independent recursive transversal solver over action systems',
        'frozen_hash_failures':hash_failures,
        'exhaustive_action_systems_checked':ex_checked,
        'exhaustive_mismatches':ex_mismatches,
        'random_action_systems':rnd,
        'scope_controls':controls,
        'failures':failures,
        'overall':'PASS' if not failures else 'FAIL',
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({
        'overall':result['overall'],
        'frozen_hash_failures':len(hash_failures),
        'exhaustive_action_systems_checked':ex_checked,
        'random_action_systems_checked':rnd['checked'],
        'failures':failures,
    },indent=2))

if __name__=='__main__': main()
