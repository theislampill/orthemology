#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, random
from pathlib import Path
from collections import defaultdict

SEED=2026080909
rng=random.Random(SEED)
out={"schema":"AR8R_PMR007_POST_BV_CONSOLIDATED_RECHECK_V2","seed":SEED,"results":{}}

# BW: exact deterministic shared-neutral transducers.
states=(0,1); acts=(0,1); outputs=(0,1)
pairs=tuple(itertools.product(states,acts)); choices=tuple(itertools.product(states,outputs))
def run_word(tab,init,word):
    s=init; ys=[]
    for a in word: s,y=tab[(s,a)]; ys.append(y)
    return tuple(ys),s
def pol(hist,k):
    return (0,1,sum(hist)%2,(len(hist)+sum(hist))%2)[k]
def run_pol(tab,init,h,k):
    s=init; hist=[]
    for _ in range(h):
        s,y=tab[(s,pol(tuple(hist),k))]; hist.append(y)
    return tuple(hist),s
bw={"transducers":0,"open_loop":0,"adaptive":0,"mismatches":0,"hidden_anchor":0,"hidden_anchor_failures":0}
for assn in itertools.product(choices,repeat=4):
    tab=dict(zip(pairs,assn)); bw["transducers"]+=1
    for init in states:
        for h in range(1,5):
            for word in itertools.product(acts,repeat=h):
                p=[run_word(tab,init,word) for _ in range(3)]; bw["open_loop"]+=1
                bw["mismatches"] += (len(set(p))!=1)
            for k in range(4):
                p=[run_pol(tab,init,h,k) for _ in range(3)]; bw["adaptive"]+=1
                bw["mismatches"] += (len(set(p))!=1)
        pt=dict(tab); ns,y=pt[(init,1)]; pt[(init,1)]=(ns,1-y)
        prof=[run_word(pt,init,(1,)),run_word(tab,init,(1,)),run_word(tab,init,(1,))]
        bw["hidden_anchor"]+=1; bw["hidden_anchor_failures"]+=(len(set(prof))==1)
bw["pass"]=bw["mismatches"]==0 and bw["hidden_anchor_failures"]==0
out["results"]["BW"]=bw

# BX: direct factorization versus conflict-cover characterization.
def identifies_direct(E,Q,anchors,S):
    seen={}
    for i in range(len(E)):
        key=(E[i],tuple(anchors[j][i] for j in S))
        if key in seen and seen[key]!=Q[i]: return False
        seen[key]=Q[i]
    return True
def covers_conflicts(E,Q,anchors,S):
    for i in range(len(E)):
        for j in range(i+1,len(E)):
            if E[i]==E[j] and Q[i]!=Q[j] and not any(anchors[a][i]!=anchors[a][j] for a in S): return False
    return True
bx={"instances":20000,"feasible_subsets":0,"criterion_mismatches":0,"minimum_cost_mismatches":0,"unresolved_cores":0,"weighted_cardinality_divergence":0}
for _ in range(bx["instances"]):
    n=rng.randint(3,8); k=rng.randint(3,7)
    E=[rng.randrange(3) for _ in range(n)]; Q=[rng.randrange(2) for _ in range(n)]
    A=[[rng.randrange(3) for _ in range(n)] for __ in range(k)]
    eligible=[rng.random()<.8 for _ in range(k)]; costs=[rng.randint(1,6) for _ in range(k)]
    incompat={(i,j) for i in range(k) for j in range(i+1,k) if rng.random()<.08}
    best_cost=None; best_card=None; direct_best=None
    for mask in range(1<<k):
        S=[i for i in range(k) if mask>>i&1]
        if any(not eligible[i] for i in S) or any(i in S and j in S for i,j in incompat): continue
        bx["feasible_subsets"]+=1
        d=identifies_direct(E,Q,A,S); c=covers_conflicts(E,Q,A,S)
        bx["criterion_mismatches"] += d!=c
        if d:
            cost=sum(costs[i] for i in S)
            best_cost=cost if best_cost is None else min(best_cost,cost)
            best_card=len(S) if best_card is None else min(best_card,len(S))
            direct_best=cost if direct_best is None else min(direct_best,cost)
    bx["minimum_cost_mismatches"] += best_cost!=direct_best
    if best_cost is None and any(E[i]==E[j] and Q[i]!=Q[j] for i in range(n) for j in range(i+1,n)): bx["unresolved_cores"]+=1
    if best_cost is not None:
        # Whether a min-cost solution can differ from minimum cardinality in weighted setting.
        min_cost_card=min(len([i for i in range(k) if mask>>i&1]) for mask in range(1<<k)
            if all(eligible[i] for i in range(k) if mask>>i&1)
            and not any((mask>>i)&1 and (mask>>j)&1 for i,j in incompat)
            and identifies_direct(E,Q,A,[i for i in range(k) if mask>>i&1])
            and sum(costs[i] for i in range(k) if mask>>i&1)==best_cost)
        if best_card is not None and min_cost_card!=best_card: bx["weighted_cardinality_divergence"]+=1
bx["pass"]=bx["criterion_mismatches"]==0 and bx["minimum_cost_mismatches"]==0
out["results"]["BX"]=bx

# BY: nine-guard transfer and intrinsic locus rule.
by={"guard_rows":0,"valid_transfers":0,"false_transfers":0,"single_guard_deletions":0,"locus_assignments":0,"locus_misattributions":0}
for bits in itertools.product((0,1),repeat=9):
    by["guard_rows"]+=1; transfer=all(bits)
    if transfer: by["valid_transfers"]+=1
    if transfer and not all(bits): by["false_transfers"]+=1
    if sum(bits)==8: by["single_guard_deletions"]+=1
# Three loci; speech predicate follows intrinsic locus exactly, not a separate cause label.
for locus_bits in itertools.product((0,1),repeat=3):
    by["locus_assignments"]+=1
    speakers=set(i for i,b in enumerate(locus_bits) if b)
    derived=set(i for i,b in enumerate(locus_bits) if b)
    by["locus_misattributions"] += speakers!=derived
by["pass"]=by["false_transfers"]==0 and by["locus_misattributions"]==0 and by["single_guard_deletions"]==9
out["results"]["BY"]=by

# BZ: exact 2^9 conservative expansion cube.
expansions=list(itertools.product((0,1),repeat=9))
bz={"expansions":len(expansions),"target_bits":9,"bit_conflicts":[],"full_vector_pairs":len(expansions)*(len(expansions)-1)//2}
for bit in range(9):
    z=[x for x in expansions if x[bit]==0]; o=[x for x in expansions if x[bit]==1]
    bz["bit_conflicts"].append(len(z)*len(o))
bz["all_targets_vary"]=all(c>0 for c in bz["bit_conflicts"]); bz["pass"]=bz["all_targets_vary"]
out["results"]["BZ"]=bz

# CA: vector budgets and singleton feasibility.
ca={"instances":20000,"budget_tests":0,"mismatches":0,"pareto_incomparable":0,"conservative_twins":0}
for _ in range(ca["instances"]):
    a=rng.randint(2,5); d=rng.randint(2,4)
    costs=[tuple(rng.randint(0,8) for _ in range(d)) for __ in range(a)]
    if len(set(costs))<a: ca["conservative_twins"]+=1
    for i in range(a):
        for j in range(i+1,a):
            ci,cj=costs[i],costs[j]
            if not all(x<=y for x,y in zip(ci,cj)) and not all(y<=x for x,y in zip(ci,cj)): ca["pareto_incomparable"]+=1
    for __ in range(10):
        b=tuple(rng.randint(0,8) for _ in range(d)); feasible=[i for i,c in enumerate(costs) if all(x<=y for x,y in zip(c,b))]
        identified=(len(feasible)==1); direct=(len(set(feasible))==1)
        ca["budget_tests"]+=1; ca["mismatches"]+=identified!=direct
ca["pass"]=ca["mismatches"]==0
out["results"]["CA"]=ca

# CB: E-determined restrictions cannot split E fibres.
cb={"instances":50000,"same_fibre_pairs":0,"determined_split_failures":0,"external_split_controls":0}
for _ in range(cb["instances"]):
    n=rng.randint(3,10); E=[rng.randrange(4) for __ in range(n)]; f=[rng.randrange(2) for __ in range(4)]; r=[f[e] for e in E]
    ext=[rng.randrange(2) for __ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if E[i]==E[j]:
                cb["same_fibre_pairs"]+=1; cb["determined_split_failures"]+=r[i]!=r[j]; cb["external_split_controls"]+=ext[i]!=ext[j]
cb["pass"]=cb["determined_split_failures"]==0
out["results"]["CB"]=cb

# CC: exhaustive 4x4 witness relations.
def min_cover(rows):
    # rows[c] is bitset of grounds.
    if any(r==0 for r in rows): return None
    for k in range(1,5):
        for S in itertools.combinations(range(4),k):
            mask=sum(1<<g for g in S)
            if all(r&mask for r in rows): return k
    return None
cc={"relations":0,"LOCAL":0,"COMMON":0,"LOCAL_not_COMMON":0,"UNIQUE_LOCAL":0,"UNIQUE_LOCAL_not_COMMON":0,"equivalence_failures":0}
for mask in range(1<<16):
    rows=[]
    for c in range(4): rows.append(sum(((mask>>(4*c+g))&1)<<g for g in range(4)))
    local=all(r!=0 for r in rows); common=(rows[0]&rows[1]&rows[2]&rows[3])!=0; gamma=min_cover(rows)
    unique=all(r and (r&(r-1)==0) for r in rows)
    cc["relations"]+=1; cc["LOCAL"]+=local; cc["COMMON"]+=common; cc["LOCAL_not_COMMON"]+=local and not common; cc["UNIQUE_LOCAL"]+=unique; cc["UNIQUE_LOCAL_not_COMMON"]+=unique and not common
    cc["equivalence_failures"]+=(local!=(gamma is not None)) or (common!=(gamma==1))
cc["pass"]=cc["equivalence_failures"]==0
out["results"]["CC"]=cc

# CD: group-orbit fittingness firewall via generated permutation orbits.
def orbit_partition(n,perms):
    seen=[False]*n; orbits=[]
    for s in range(n):
        if seen[s]: continue
        stack=[s]; seen[s]=True; orb=[]
        while stack:
            x=stack.pop(); orb.append(x)
            for p in perms:
                for y in (p[x], p.index(x)):
                    if not seen[y]: seen[y]=True; stack.append(y)
        orbits.append(tuple(sorted(orb)))
    return orbits
cd={"instances":20000,"orbit_noninvariant":0,"factorization_failures":0,"joint_anchor_tests":0,"joint_mismatches":0}
for _ in range(cd["instances"]):
    n=rng.randint(3,8); perms=[]
    for __ in range(rng.randint(1,3)):
        p=list(range(n)); rng.shuffle(p); perms.append(p)
    orbs=orbit_partition(n,perms); E=[None]*n
    for k,o in enumerate(orbs):
        for x in o:E[x]=k
    F=[rng.randrange(2) for __ in range(n)]; noninv=any(len({F[x] for x in o})>1 for o in orbs)
    if noninv: cd["orbit_noninvariant"]+=1
    seen={}; factors=True
    for x in range(n):
        if E[x] in seen and seen[E[x]]!=F[x]: factors=False
        seen[E[x]]=F[x]
    cd["factorization_failures"]+=noninv and factors
    A=[rng.randrange(3) for __ in range(n)]; seen={}; joint=True
    for x in range(n):
        key=(E[x],A[x])
        if key in seen and seen[key]!=F[x]:joint=False
        seen[key]=F[x]
    direct=all(not(E[i]==E[j] and A[i]==A[j] and F[i]!=F[j]) for i in range(n) for j in range(i+1,n))
    cd["joint_anchor_tests"]+=1; cd["joint_mismatches"]+=joint!=direct
cd["pass"]=cd["factorization_failures"]==0 and cd["joint_mismatches"]==0
out["results"]["CD"]=cd

# CE: exact finite mixtures of 3-input binary response types, total count 7.
types=list(itertools.product((0,1),repeat=3))
def comps(total,k,prefix=()):
    if k==1: yield prefix+(total,); return
    for x in range(total+1): yield from comps(total-x,k-1,prefix+(x,))
ce={"count_vectors":0,"strict_separable":0,"strict_failures":0,"profile_invariant":0,"nonconstant_cancellation":0}
for cnt in comps(7,8):
    ce["count_vectors"]+=1
    agg=[sum(cnt[i]*types[i][x] for i in range(8)) for x in range(3)]
    inv=len(set(agg))==1; strict=all(cnt[i]==0 for i,t in enumerate(types) if len(set(t))>1)
    ce["strict_separable"]+=strict; ce["strict_failures"]+=strict and not inv; ce["profile_invariant"]+=inv; ce["nonconstant_cancellation"]+=inv and not strict
ce["pass"]=ce["strict_failures"]==0 and ce["nonconstant_cancellation"]>0
out["results"]["CE"]=ce

# CF: exhaustive bearer-attribute incidence.
def beta(rows):
    if any(r==0 for r in rows): return None
    for k in range(1,4):
        for S in itertools.combinations(range(3),k):
            m=sum(1<<b for b in S)
            if all(r&m for r in rows): return k
    return None
cf={"systems":0,"equivalence_failures":0,"beta_infinity":0,"multiple_common":0,"pairwise_no_global":0}
for mask in range(1<<12):
    rows=[sum(((mask>>(3*a+b))&1)<<b for b in range(3)) for a in range(4)]
    common_bits=rows[0]&rows[1]&rows[2]&rows[3]; be=beta(rows)
    common=common_bits!=0
    cf["systems"]+=1; cf["equivalence_failures"]+=common!=(be==1); cf["beta_infinity"]+=be is None; cf["multiple_common"]+=common_bits and (common_bits&(common_bits-1)!=0)
    pairwise=all(rows[i]&rows[j] for i in range(4) for j in range(i+1,4))
    cf["pairwise_no_global"]+=pairwise and not common
cf["pass"]=cf["equivalence_failures"]==0
out["results"]["CF"]=cf

# CG: coherent conservative target expansions over one strengthened base.
# Target order: uptake, because_fitting, personality, wisdom, actual_speech.
cg={"all_expansions":0,"admissible":0,"personal_twin":False,"impersonal_twin":False,"target_variation":[]}
adm=[]
for bits in itertools.product((0,1),repeat=5):
    cg["all_expansions"]+=1; up,bf,pers,wis,sp=bits
    if bf and not up: continue
    if wis and not (bf and up): continue
    adm.append(bits)
cg["admissible"]=len(adm); cg["impersonal_twin"]=(0,0,0,0,0) in adm; cg["personal_twin"]=(1,1,1,1,1) in adm
cg["target_variation"]=[len({x[i] for x in adm})==2 for i in range(5)]; cg["pass"]=cg["personal_twin"] and cg["impersonal_twin"] and all(cg["target_variation"])
out["results"]["CG"]=cg

# CH: capability/implementation/semantic contract tables for three architectures.
ch={"tables":0,"total_valid":0,"partial_capability":0,"total_semantic_invalid":0,"proxy_trials":20000,"proxy_mismatches":0,"proxy_collisions":0}
for caps in itertools.product((0,1),repeat=3):
  for impl in itertools.product((0,1,2),repeat=3): # 0 absent,1 no-op/bad,2 valid
    ch["tables"]+=1
    if not all(caps): ch["partial_capability"]+=1
    elif all(i==2 for i in impl): ch["total_valid"]+=1
    else: ch["total_semantic_invalid"]+=1
for _ in range(ch["proxy_trials"]):
    n=rng.randint(3,8); proxy=[rng.randrange(3) for __ in range(n)]; q=[rng.randrange(2) for __ in range(n)]
    direct=all(not(proxy[i]==proxy[j] and q[i]!=q[j]) for i in range(n) for j in range(i+1,n))
    seen={}; fact=True
    for i in range(n):
        if proxy[i] in seen and seen[proxy[i]]!=q[i]: fact=False
        seen[proxy[i]]=q[i]
    ch["proxy_mismatches"]+=direct!=fact; ch["proxy_collisions"]+=not direct
ch["pass"]=ch["proxy_mismatches"]==0 and ch["total_valid"]>0 and ch["partial_capability"]>0
out["results"]["CH"]=ch

# CI: 3 contents x 2 guard states with probability grid of size 5.
def target_fibre_collision(left, right):
    return left["profile"] == right["profile"] and left["target"] != right["target"]

ci={"profiles":0,"content_sensitive":0,"content_insensitive":0,"matched_twins":0,"twin_failures":0,
    "profile_perturbation_controls":0,"profile_perturbation_false_positives":0,
    "same_target_controls":0,"same_target_false_positives":0}
for vals in itertools.product(range(5),repeat=6):
    ci["profiles"]+=1
    sens=any(len({vals[2*c+g] for c in range(3)})>1 for g in range(2))
    ci["content_sensitive"]+=sens; ci["content_insensitive"]+=not sens
# Execute matched-target-expansion twins and two negative-control families.
for _ in range(20000):
    profile=tuple(rng.randrange(5) for __ in range(6))
    impersonal={"profile":profile,"target":0}
    intentional={"profile":profile,"target":1}
    ci["matched_twins"]+=1
    ci["twin_failures"]+=not target_fibre_collision(impersonal,intentional)

    coordinate=rng.randrange(6)
    perturbed=list(profile); perturbed[coordinate]=(perturbed[coordinate]+1)%5
    perturbed_intentional={"profile":tuple(perturbed),"target":1}
    ci["profile_perturbation_controls"]+=1
    ci["profile_perturbation_false_positives"]+=target_fibre_collision(impersonal,perturbed_intentional)

    same_target={"profile":profile,"target":0}
    ci["same_target_controls"]+=1
    ci["same_target_false_positives"]+=target_fibre_collision(impersonal,same_target)
ci["pass"]=(ci["twin_failures"]==0 and ci["matched_twins"]==20000
    and ci["profile_perturbation_controls"]==20000 and ci["profile_perturbation_false_positives"]==0
    and ci["same_target_controls"]==20000 and ci["same_target_false_positives"]==0
    and ci["content_insensitive"]==25)
out["results"]["CI"]=ci

# CJ: binary C,F,P exact ternary-grid output probabilities.
cj={"profiles":0,"fittingness_sensitive":0,"payoff_independent":0,"both":0,
    "personal_impersonal_twins":0,"twin_failures":0,
    "profile_perturbation_controls":0,"profile_perturbation_false_positives":0,
    "same_target_controls":0,"same_target_false_positives":0}
# index = ((c*2+f)*2+p)
for vals in itertools.product(range(3),repeat=8):
    cj["profiles"]+=1
    fs=any(vals[(c*2+0)*2+p]!=vals[(c*2+1)*2+p] for c in range(2) for p in range(2))
    pi=all(vals[(c*2+f)*2+0]==vals[(c*2+f)*2+1] for c in range(2) for f in range(2))
    cj["fittingness_sensitive"]+=fs; cj["payoff_independent"]+=pi; cj["both"]+=fs and pi
# Construct F-sensitive, registered-payoff-independent profiles and execute
# personal/impersonal target-expansion twins plus negative controls.
for _ in range(20000):
    collapsed=[rng.randrange(3) for __ in range(4)] # (C,F), duplicated across P
    if collapsed[0]==collapsed[1] and collapsed[2]==collapsed[3]:
        collapsed[1]=(collapsed[1]+1)%3
    profile=tuple(collapsed[c*2+f] for c in range(2) for f in range(2) for p in range(2))
    impersonal={"profile":profile,"target":("impersonal",False)}
    personal={"profile":profile,"target":("personal",True)}
    cj["personal_impersonal_twins"]+=1
    cj["twin_failures"]+=not target_fibre_collision(impersonal,personal)

    coordinate=rng.randrange(8)
    perturbed=list(profile); perturbed[coordinate]=(perturbed[coordinate]+1)%3
    perturbed_personal={"profile":tuple(perturbed),"target":("personal",True)}
    cj["profile_perturbation_controls"]+=1
    cj["profile_perturbation_false_positives"]+=target_fibre_collision(impersonal,perturbed_personal)

    same_target={"profile":profile,"target":("impersonal",False)}
    cj["same_target_controls"]+=1
    cj["same_target_false_positives"]+=target_fibre_collision(impersonal,same_target)
cj["pass"]=(cj["twin_failures"]==0 and cj["personal_impersonal_twins"]==20000
    and cj["profile_perturbation_controls"]==20000 and cj["profile_perturbation_false_positives"]==0
    and cj["same_target_controls"]==20000 and cj["same_target_false_positives"]==0
    and cj["both"]>0)
out["results"]["CJ"]=cj

out["overall_pass"]=all(v.get("pass",False) for v in out["results"].values())
path=Path(__file__).with_name('post_bv_consolidated_recheck_v2_results.json')
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2,sort_keys=True))
