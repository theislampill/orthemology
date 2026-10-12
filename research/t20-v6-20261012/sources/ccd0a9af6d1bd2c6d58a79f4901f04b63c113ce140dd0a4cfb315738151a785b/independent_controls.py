#!/usr/bin/env python3
"""Independent exact mixture family, permission guard, and stopped-law controls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util, json
ROOT=Path(__file__).resolve().parent
SOLVER=ROOT/'snapshot/stochastic-exact-inquiry-20261010/solver.py'
spec=importlib.util.spec_from_file_location('candidate_solver',SOLVER)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
labels=(0,1,0,1)
prob=((F(1,2),F(1,2),F(1),F(1)),(F(1,2),F(0),F(0),F(0)),(F(0),F(1,2),F(0),F(0)))
rows={'read':[{(i,o) for o in range(3) if prob[o][i]} for i in range(4)]}
p=(F(1,2),F(1,2),F(0),F(0))
def evaluate(law,word):
    r=list(law)
    for o in word:r=[v*prob[o][i] for i,v in enumerate(r)]
    mass=sum(r)
    return mass,None if not mass else (sum(r[i] for i in (0,2))/mass,sum(r[i] for i in (1,3))/mass)
count=0;classification_count=0
for k in range(1,65):
    alpha=F(k,64);r=(alpha/2,alpha/2,(1-alpha)/2,(1-alpha)/2)
    status=module.classify(rows,labels,[i for i,v in enumerate(r) if v])
    assert status['almost_sure']==(alpha==1) and not status['sure']
    classification_count+=1
    for length in range(6):
        for word in product(range(3),repeat=length):
            pm,pp=evaluate(p,word);rm,rp=evaluate(r,word)
            assert bool(pm)==bool(rm) and pp==rp
            if set(word)<={0}:
                assert pm==F(1,2)**length
                assert rm==1-alpha+alpha*F(1,2)**length
                assert pp==(F(1,2),F(1,2))
            elif 1 in word and 2 in word:assert pm==rm==0
            else:assert rm==alpha*pm
            count+=1
    for length in range(65):
        rm,_=evaluate(r,(0,)*length)
        assert rm==1-alpha+alpha*F(1,2)**length
# Boundary alpha=0 loses reveal words, so alpha>0 is essential for language equality.
assert evaluate((F(0),F(0),F(1,2),F(1,2)),(1,))[0]==0
assert evaluate(p,(1,))[0]>0

# Same fixed potential instrument and equal full predictive law; only hidden
# state-dependent inquiry permissions differ between the two initial supports.
licensed_rows={'reveal':[{(0,'0')},{(1,'1')},{(2,'0')},{(3,'1')}]}
menus=[{'reveal'},{'reveal'},set(),set()]
good=module.classify(licensed_rows,labels,{0,1},menus)
bad=module.classify(licensed_rows,labels,{2,3},menus)
assert good['sure_rank']==1 and not bad['almost_sure']
permission_words=0
for length in range(9):
    for word in product(('0','1'),repeat=length):
        fine=[F(1,2)*int(all(o==str(theta) for o in word)) for theta in (0,1)]
        other=[F(1,2)*int(all(o==str(theta) for o in word)) for theta in (0,1)]
        assert fine==other
        permission_words+=1

# Full predictive quotient with a genuinely history-dependent randomized policy.
# Fine states are two observationally equivalent copies of each target state.
fine0=(F(1,8),F(2,8),F(3,8),F(2,8));coarse0=(F(1,2),F(1,2))
def step(r,a,o,lab):
    out=[]
    for x,theta in zip(r,lab):
        reveal=(F(1,3),F(2,3))[theta] if a=='a' else (F(3,4),F(1,4))[theta]
        likelihood=1-reveal if o=='w' else (reveal if o==str(theta) else F(0))
        out.append(x*likelihood)
    return tuple(out)
def target_mass(r,lab):return tuple(sum(v for v,t in zip(r,lab) if t==theta) for theta in (0,1))
frontier={(): (fine0,coarse0)};stopped_fine={};stopped_coarse={};prefixes=0
for depth in range(7):
    new={}
    for h,(fine,coarse) in frontier.items():
        assert target_mass(fine,labels)==target_mass(coarse,(0,1))
        prefixes+=1
        support={labels[i] for i,x in enumerate(fine) if x}
        assert support=={i for i,x in enumerate(coarse) if x}
        if len(support)==1:
            theta=next(iter(support));key=(depth,theta)
            stopped_fine[key]=stopped_fine.get(key,F(0))+sum(fine)
            stopped_coarse[key]=stopped_coarse.get(key,F(0))+sum(coarse)
            continue
        pa=F(3,5) if not h else (F(1,4) if sum(a=='a' for a,o in h)%2 else F(2,3))
        for a,aw in (('a',pa),('b',1-pa)):
            for o in ('w','0','1'):
                fp=step(fine,a,o,labels);cp=step(coarse,a,o,(0,1))
                fp=tuple(aw*x for x in fp);cp=tuple(aw*x for x in cp)
                if sum(fp):new[h+((a,o),)]=(fp,cp)
    frontier=new
assert stopped_fine==stopped_coarse
# Same-support laws may have different target posteriors and predictive laws.
# Initial-density bounds control every nonnegative word/label functional.
u=(F(1,3),F(2,3),F(0),F(0));v=(F(3,4),F(1,4),F(0),F(0))
Cuv=max(v[i]/u[i] for i in (0,1));Cvu=max(u[i]/v[i] for i in (0,1))
assert Cuv==F(9,4) and Cvu==F(8,3)
assert evaluate(u,())[1]!=evaluate(v,())[1]
domination_words=0
for length in range(9):
    for word in product(range(3),repeat=length):
        um,up=evaluate(u,word);vm,vp=evaluate(v,word)
        assert vm<=Cuv*um and um<=Cvu*vm
        if um:
            for theta in (0,1):
                assert vm*vp[theta]<=Cuv*um*up[theta]
                assert um*up[theta]<=Cvu*vm*vp[theta]
        domination_words+=1
for length in range(65):
    pm,_=evaluate(p,(0,)*length)
    qm,_=evaluate((F(1,4),)*4,(0,)*length)
    assert qm/pm==F(2)**(length-1)+F(1,2)
out={'status':'PASS','same_support_domination_words':domination_words,'q_over_p_bound':'9/4','p_over_q_bound':'8/3','same_support_different_posteriors_checked':True,'unbounded_counterexample_ratio_checks':65,'mixture_family_alpha_values':64,'mixture_word_checks':count,'mixture_solver_classifications':classification_count,'survival_checks':64*65,'zero_mixture_boundary_checked':True,'fixed_kernel_permission_word_checks':permission_words,'fixed_kernel_permission_can_change_winningness':True,'history_policy_prefixes_checked':prefixes,'stopped_time_and_label_entries':len(stopped_fine),'full_predictive_stopped_laws_equal':True,'p_first_wait_mass':'1/2','q_half_mixture_first_wait_mass':'3/4','q_half_mixture_nontermination_mass':'1/2','scope':'Finite exact controls plus separately reviewed all-word and measure-continuity proofs; no empirical or kernel claim.'}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
