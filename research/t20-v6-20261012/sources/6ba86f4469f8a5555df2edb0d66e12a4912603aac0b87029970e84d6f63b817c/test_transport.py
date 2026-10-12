from fractions import Fraction as F
from collections import defaultdict
from itertools import product
from pathlib import Path
import importlib.util, json, sys
from rational_kernel import *
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,p):
    if not p: raise RuntimeError(name)
    checks.append(name)
def rejects(name,f):
    try: f()
    except (ValueError,KeyError): checks.append(name); return
    raise RuntimeError('Expected rejection: '+name)
S=((0,0),(1,0)); O=(0,1)
K={(S[0],'a'):((0,S[0],F(1,2)),(1,S[1],F(1,3)),(0,S[1],F(1,6))),
   (S[1],'a'):((1,S[1],F(1)),),
   (S[0],'b'):((1,S[0],F(1)),), (S[1],'b'):((0,S[0],F(1)),)}
L=compile_kernel(S,O,K)
check('common_denominator_six',L.denominator==6)
for key in K: check('joint_count_'+str(key),counting_law(L,*key)==kernel_law(K,*key))
check('multiple_denominator',compile_kernel(S,O,K,12).denominator==12)
rejects('invalid_denominator',lambda:compile_kernel(S,O,K,3))
rejects('zero_denominator',lambda:compile_kernel(S,O,K,0))
rejects('float_probability',lambda:compile_kernel(S,O,{(S[0],'a'):((0,S[0],1.0),)}))
rejects('bool_probability',lambda:compile_kernel(S,O,{(S[0],'a'):((0,S[0],True),)}))
rejects('negative_probability',lambda:compile_kernel(S,O,{(S[0],'a'):((0,S[0],-1),(1,S[1],2))}))
rejects('nonunit_row',lambda:compile_kernel(S,O,{(S[0],'a'):((0,S[0],F(1,2)),)}))
rejects('unknown_successor',lambda:compile_kernel(S,O,{(S[0],'a'):((0,(9,9),1),)}))
rejects('seed_out_of_range',lambda:L.step(S[0],'a',6))
rejects('disabled_external_action',lambda:L.step(S[0],'missing',0))
# History-dependent action selection, exact enumeration; no source policy claim.
policy=lambda h,s: 'b' if h and h[-1][1][0]==1 else 'a'
for h in range(5): check('adaptive_history_h'+str(h),history_law(K,S[0],h,policy)==uniform_history_law(L,S[0],h,policy))
# Enumerate every four-cell row with denominator 1..5. Source construction is universal;
# these 125 rows are exact executable diagnostics, not proof by finite search.
nrows=0
for d in range(1,6):
    for n in product(range(d+1),repeat=4):
        if sum(n)!=d: continue
        row=tuple((o,s,F(v,d)) for (o,s),v in zip(product(O,S),n))
        kk={(S[0],'a'):row};ll=compile_kernel(S,O,kk)
        check('exhaustive_row_'+str((d,n)),counting_law(ll,S[0],'a')==kernel_law(kk,S[0],'a'))
        nrows+=1
# A joint draw cannot be replaced by independent marginal draws.
joint={(0,0):F(1,2),(1,1):F(1,2)}
independent={(x,y):F(1,4) for x,y in product(range(2),repeat=2)}
check('separate_marginals_change_joint',joint!=independent and sum(p for (x,y),p in joint.items() if x!=y)==0 and sum(p for (x,y),p in independent.items() if x!=y)==F(1,2))
# One-state emitter: identical uniform per-time marginals, different two-step law.
emitter=compile_kernel(((0,0),),O,{((0,0),'a'):((0,(0,0),F(1,2)),(1,(0,0),F(1,2)))})
pp=lambda h,s:'a'
iid=uniform_history_law(emitter,(0,0),2,pp)
shared=defaultdict(F)
for u in range(2): shared[seeded_history(emitter,(0,0),(u,u),pp)]+=F(1,2)
for t in range(2):
    def marginal(law):
        m=defaultdict(F)
        for (h,s),p in law.items():m[h[t][1][0]]+=p
        return dict(m)
    check('same_uniform_marginal_'+str(t),marginal(iid)==marginal(shared)=={0:F(1,2),1:F(1,2)})
check('shared_seed_wrong_history',iid!=dict(shared))
# Fresh-uniform is sufficient, NOT necessary: D=4, pick only seed 0 or 2.
wide=compile_kernel(((0,0),),O,{((0,0),'a'):((0,(0,0),F(1,2)),(1,(0,0),F(1,2)))},4)
nonuniform=defaultdict(F)
for bits in product(range(2),repeat=3):
    # Alternate within each reply fibre according to past output, hence history-dependent.
    seeds=tuple(2*b+(bits[i-1] if i else 0) for i,b in enumerate(bits))
    nonuniform[seeded_history(wide,(0,0),seeds,pp)]+=F(1,8)
check('nonuniform_history_dependent_fibre_mass_suffices',dict(nonuniform)==uniform_history_law(wide,(0,0),3,pp))
check('first_seed_is_not_uniform',set((2*b for b in range(2)))=={0,2})
# D1 actual supplied reference construction: merge two concrete representatives.
path=ROOT.parent/'received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py'
spec=importlib.util.spec_from_file_location('received_contracts',path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
ss=('a','b','c');aa=('read',)
ck={('a','read'):((0,'a',F(1,4)),(0,'b',F(1,4)),(1,'c',F(1,3)),(0,'c',F(1,6))),
    ('b','read'):((0,'a',F(1,2)),(1,'c',F(1,3)),(0,'c',F(1,6))),('c','read'):((1,'c',F(1)),)}
c=m.Contract(ss,aa,O,dict(zip(ss,(0,0,1))),{s:aa for s in ss},{(s,'read'):F(0) for s in ss},ck)
blocks,trace=m.coarsest_refinement(c,{s:0 for s in ss});q,bm=m.quotient(c,blocks)
check('d1_merges_exactly_a_b',blocks==(('a','b'),('c',)))
codes={s:(0,i) for i,s in enumerate(q.states)}
qk={(codes[s],a):tuple((o,codes[t],p) for o,t,p in row) for (s,a),row in q.kernels.items()}
ql=compile_kernel(tuple(codes.values()),O,qk)
check('d1_quotient_counts',all(counting_law(ql,*key)==kernel_law(qk,*key) for key in qk))
# Compare entire projected concrete history with the quotient's seeded law.
for horizon in range(4):
    for initial in ('a','b'):
        concrete={((),initial):F(1)}
        for _ in range(horizon):
            nxt=defaultdict(F)
            for (hist,state),mass in concrete.items():
                for o,target,p in ck[state,'read']:
                    rr=(o,*codes[bm[target]])
                    nxt[hist+(('read',rr),),target]+=mass*p
            concrete=dict(nxt)
        projected=defaultdict(F)
        for (hist,state),mass in concrete.items(): projected[hist,codes[bm[state]]]+=mass
        check('d1_projected_seeded_history_'+str((initial,horizon)),
              dict(projected)==uniform_history_law(ql,codes[bm[initial]],horizon,lambda h,s:'read'))
# Deterministic source fixture consumes these exact tables, not a separately typed calculus.
fixture={'states':S,'outcomes':O,'denominator':L.denominator,'action':'a','cubes':L.cubes('a')}
check('fixture_matches_constructor',json.loads((ROOT/'FIXTURE.json').read_text())==json.loads(json.dumps(fixture)))
print(json.dumps({'status':'PASS','count':len(checks),'exhaustive_rows':nrows,'checks':checks},indent=2))
