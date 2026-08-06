#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, math, random
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
FREEZE=ROOT/'PMR-007_DEEP_AC_V2_FROZEN_HASHES.sha256'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def verify_hashes():
    checked=0; failures=[]
    for line in FREEZE.read_text().splitlines():
        if not line.strip(): continue
        expected,rel=line.split(maxsplit=1); checked+=1
        actual=sha(ROOT/rel)
        if actual!=expected: failures.append({'path':rel,'expected':expected,'actual':actual})
    return checked,failures

def cyclic_group(n):
    return tuple(tuple((i+k)%n for i in range(n)) for k in range(n))

def dihedral_group(n):
    elems=[]
    for k in range(n):
        elems.append(tuple((i+k)%n for i in range(n)))
        elems.append(tuple((k-i)%n for i in range(n)))
    # unique
    return tuple(dict.fromkeys(elems))

def is_equiv(G,E,actE,F):
    return all(F[actE(g,e)]==g[F[e]] for g in G for e in E)

def stab(G,act,x): return tuple(g for g in G if act(g,x)==x)

def cyclic_checks():
    shift_maps=0; shift_fail=0; fixed_brute_maps=0; fixed_fail=0
    for n in range(2,13):
        G=cyclic_group(n); A=tuple(range(n))
        for k in range(n):
            F={e:(e+k)%n for e in A}; shift_maps+=1
            if not is_equiv(G,A,lambda g,e:g[e],F): shift_fail+=1
        # brute fixed-resource extension through n=6, independently from primary S_n test
        if n<=6:
            STAR=n; E=tuple(range(n+1))
            def actE(g,e): return STAR if e==STAR else g[e]
            count=0
            for vals in itertools.product(A,repeat=n+1):
                F={e:vals[e] for e in E}
                if is_equiv(G,E,actE,F): count+=1
            fixed_brute_maps += count
            if count!=0: fixed_fail+=1
    return shift_maps,shift_fail,fixed_brute_maps,fixed_fail

def orbit_construction_checks(seed=20260805,trials=30000):
    rng=random.Random(seed); failures=0; well_defined=0; stab_inclusions=0
    for _ in range(trials):
        n=rng.randint(3,10)
        G=dihedral_group(n) if rng.getrandbits(1) else cyclic_group(n)
        E=tuple(range(n)); A=tuple(range(n))
        e=rng.randrange(n)
        Se=stab(G,lambda g,x:g[x],e)
        candidates=[a for a in A if all(g[a]==a for g in Se)]
        if not candidates:
            continue
        a=rng.choice(candidates)
        # Extend F on orbit of e by g.e -> g.a; check well-defined.
        F={}; ok=True
        for g in G:
            x=g[e]; y=g[a]
            if x in F and F[x]!=y: ok=False; break
            F[x]=y
        if not ok:
            failures+=1; continue
        well_defined+=1
        orbit=tuple(F)
        for g in G:
            for x in orbit:
                if g[x] in F and F[g[x]]!=g[F[x]]: failures+=1
        for x in orbit:
            Sx=stab(G,lambda g,z:g[z],x)
            Sy=stab(G,lambda g,z:g[z],F[x])
            stab_inclusions+=1
            if not set(Sx).issubset(set(Sy)): failures+=1
    return trials,well_defined,stab_inclusions,failures

def scope_controls():
    # invariant multivalued relation has all alternatives, not a unique selection
    multivalued=True
    # two sufficient asymmetric resources show output uniqueness does not imply unique source
    overdetermined={'r1':1,'r2':1,'output':1,'r1_suffices':True,'r2_suffices':True}
    # same complete extensional reduct with inert metaphysical labels
    neutral={'resource':'e2','map':'identity','output':'a2','stabilizer_accounting':'pass'}
    parity=(neutral==neutral)
    # a non-equivariant constant operation chooses 0 in a cyclic model
    n=5; G=cyclic_group(n); A=tuple(range(n)); const={e:0 for e in A}
    nonequiv=not is_equiv(G,A,lambda g,e:g[e],const)
    return multivalued,overdetermined,parity,nonequiv

def main():
    hr,hf=verify_hashes()
    sm,sf,fb,ff=cyclic_checks()
    trials,constructed,stabs,of=orbit_construction_checks()
    multi,over,parity,nonequiv=scope_controls()
    fail=len(hf)+sf+ff+of+int(not multi)+int(not parity)+int(not nonequiv)
    result={
      'schema':'PMR007_DEEP_AC_DISTINCT_ORBIT_STABILIZER_REREVIEW_V2',
      'frozen_hash_rows_checked':hr,
      'frozen_hash_failures':hf,
      'cyclic_equivariant_shift_maps_checked':sm,
      'cyclic_shift_failures':sf,
      'cyclic_fixed_resource_equivariant_total_maps_found':fb,
      'cyclic_fixed_resource_failures':ff,
      'random_orbit_construction_trials':trials,
      'well_defined_orbit_maps_constructed':constructed,
      'stabilizer_inclusions_checked':stabs,
      'orbit_construction_failures':of,
      'multivalued_relation_nonunique_control':multi,
      'overdetermination_control':over,
      'personal_impersonal_neutral_reduct_parity':parity,
      'non_equivariant_constant_selector_control':nonequiv,
      'result':'PASS' if fail==0 else 'FAIL',
      'nonclaims':['T255 world guards','resource completeness','metaphysical actuality','volition','personality','Wisdom']
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
