#!/usr/bin/env python3
"""New P02-to-concrete-P03 instantiations, not a rerun of the P02 census."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import argparse,json,sys
from test_new_frontier import AtomicEngine,b,op
import observations as ob

def pair(x):return [x.numerator,x.denominator]
def spec(weights,views,space='tagged-uniform-intervals'):
    return {'space':space,'law':'P03-A2-declared-law','events':'full-measurable','weights':[pair(x) for x in weights],'view':list(views)}
def interval_factor(old,new):
    if old==-1:return new==-1
    if new==-1:return True
    m=max(old,1);n=max(new,1)
    # Each half-open fine interval must fit inside a single coarse interval.
    return all((m*j)//n==(m*(j+1)-1)//n for j in range(n))
def outcome(fn):
    try:return True,fn()
    except b.Rejection as e:return False,str(e)

def run(out):
    out.mkdir(parents=True,exist_ok=True);rows=[];counts={'tagged_pairs':0,'finite_pairs':0,'threshold_checks':0}
    for w in [F(0),F(1,3),F(1,2),F(2,3),F(1)]:
        ws=[w,1-w]
        for a in product((-1,0,1,2,3,4),repeat=2):
            for z in product((-1,0,1,2,3,4),repeat=2):
                ca,fi=spec(ws,a),spec(ws,z)
                expected=all(interval_factor(x,y) for x,y in zip(a,z))
                accepted,report=outcome(lambda:ob.refinement(ca,fi))
                if accepted!=expected:raise AssertionError(('factor',w,a,z,accepted,expected))
                if accepted:
                    dc=sum((q for q,v in zip(ws,a) if v==-1),F(0));df=sum((q for q,v in zip(ws,z) if v==-1),F(0))
                    if F(*report['coarse_defect'])!=dc or F(*report['fine_defect'])!=df or F(*report['increment'])!=df-dc:raise AssertionError(report)
                    total=sum((F(*r['weight'])*F(*r['conditional_defect']) for r in report['positive_coarse_fibres']),F(0))
                    if total!=df-dc:raise AssertionError('wrong fibre sum')
                counts['tagged_pairs']+=1
                rows.append({'w':pair(w),'coarse':a,'fine':z,'accepted':accepted,'increment':report['increment'] if accepted else None})
    ws=[F(0),F(1,3),F(2,3)]
    for a in product(range(3),repeat=3):
        for z in product(range(3),repeat=3):
            expected=all(z[i]!=z[j] or a[i]==a[j] for i in range(3) for j in range(3))
            accepted,report=outcome(lambda:ob.refinement(spec(ws,a,'finite-programs'),spec(ws,z,'finite-programs')))
            if accepted!=expected or accepted and F(*report['increment'])!=0:raise AssertionError(('finite',a,z,report))
            counts['finite_pairs']+=1
    for vs in product((-1,0,2),repeat=3):
        s=spec([F(1,4),F(1,3),F(5,12)],vs);d=sum((w for w,v in zip([F(1,4),F(1,3),F(5,12)],vs) if v==-1),F(0))
        for eps in [F(0),F(1,4),F(1,3),F(1,2),F(1)]:
            yes,report=outcome(lambda:ob.certify(s,pair(eps)))
            if yes!=(d<=eps):raise AssertionError((s,eps,d,report))
            counts['threshold_checks']+=1
    # A syntactic zero-weight component still fails the pointwise factor guard.
    c=spec([F(0),F(1)],[2,0]);f=spec([F(0),F(1)],[3,0])
    yes,msg=outcome(lambda:ob.refinement(c,f))
    if yes:raise AssertionError('zero-weight countermodel lost')
    countermodels=[{'id':'P03-A2-CE-AE-COMPLETENESS','coarse':c,'fine':f,'engine_result':msg,
        'a_s_factorisation_exists':True,'proof':'The law is concentrated on component 1, where both observations are constant; the incompatible bins are in the zero-weight component 0. The implementation deliberately checks every component.'}]
    # Valid normalised rational table can exceed intermediate denominator budget.
    ps=[2**89-1,2**89+1,2**89+3]
    small=[F(1,3*p) for p in ps];large=[F(p-1,3*p) for p in ps]
    bad=small+large;good=[x for pair_ in zip(small,large) for x in pair_]
    if sum(bad)!=1 or sum(good)!=1:raise AssertionError('weight construction')
    sb=spec(bad,[0]*6,'finite-programs');sg=spec(good,[0]*6,'finite-programs')
    accepted,msg=outcome(lambda:ob.check(sb));accepted2,m=outcome(lambda:ob.check(sg))
    if accepted or not accepted2 or m.defect!=0:raise AssertionError((accepted,msg,accepted2))
    sums=[];s=F(0)
    for x in bad:s+=x;sums.append([s.numerator.bit_length(),s.denominator.bit_length()])
    countermodels.append({'id':'P03-A2-CE-ARITHMETIC-COMPLETENESS','refused_model':sb,'reordered_model':sg,
        'refusal':msg,'final_mathematical_total':[1,1],'prefix_numerator_denominator_bits':sums,
        'reordered_defect':[0,1],'proof':'Three pairs each sum to 1/3. Grouping the three small terms first creates an intermediate denominator above 256 bits, while interleaving complements cancels it. Both observed laws are the same point mass; only the literal resource path differs.'})
    # One actual registry path: semantic weakening does not revive version custody.
    e=AtomicEngine.standard();coarse=spec([F(1,4),F(3,4)],[0,2]);fine=spec([F(1,4),F(3,4)],[-1,4])
    e.set_probability_observation('m',coarse);e.require_probability('primitive:succ','m',[1,4])
    old=e.admit({'op':'primitive','name':'succ'});r=e.refine_probability_observation('m',fine)
    if F(*r['increment'])!=F(1,4) or e.describe(old)['current']:raise AssertionError('refine binding')
    fresh=e.revalidate(old)
    if e.dispatch(fresh,0)!=1:raise AssertionError('budget equality should pass')
    e.coarsen_probability_observation('m',coarse)
    if e.describe(fresh)['current'] or e.describe(old)['current']:raise AssertionError('coarsening revived old stamp')
    newest=e.revalidate(old)
    if e.dispatch(newest,0)!=1:raise AssertionError('re-admission after coarsening')
    revision_path={'increment':r['increment'],'coarse_defect':r['coarse_defect'],'fine_defect':r['fine_defect'],
                   'old_stale_after_refine':True,'both_old_handles_stale_after_coarsen':True,'new_admission_success':True}
    # Explicit joint finite input + revision law, including refusal outcomes.
    law=defaultdict(F);abstract=defaultdict(F);input_weights={0:F(1,2),1:F(1,3),2:F(1,6)}
    for x,wx in input_weights.items():
        for revoke,wr in [(False,F(3,4)),(True,F(1,4))]:
            e=AtomicEngine.standard();lic=e.admit({'op':'primitive','name':'succ'})
            if revoke:e.revise_rule('primitive:succ',False)
            yes,v=outcome(lambda:e.dispatch(lic,x));label=('Success',v) if yes else ('Refusal','stale')
            expected=('Refusal','stale') if revoke else ('Success',x+1)
            law[label]+=wx*wr;abstract[expected]+=wx*wr
    if law!=abstract or sum(law.values())!=1 or law[('Refusal','stale')]!=F(1,4):raise AssertionError(law)
    conditioned={str(k):pair(v/F(3,4)) for k,v in law.items() if k[0]=='Success'}
    probability_lift={'joint_law':'X with masses 1/2,1/3,1/6; independent revoke flag of mass 1/4 (explicit experimental assumption)',
        'concrete_and_abstract_laws_equal':True,'outcome_masses':[{ 'outcome':list(k),'mass':pair(v)} for k,v in law.items()],
        'success_mass':[3,4],'conditional_success_law':conditioned,'refusal_mass_not_dropped':True}
    with (out/'refinement_pairs.jsonl').open('w') as f:
        for row in rows:f.write(json.dumps(row,separators=(',',':'))+'\n')
    result={'counts':counts,'new_countermodels':countermodels,'concrete_revision_instantiation':revision_path,
            'probability_lift':probability_lift,'mismatches':0,'kernel_credit':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'counts':counts,'new_countermodels':[c['id'] for c in countermodels],'revision':revision_path,'probability_lift':probability_lift,'mismatches':0},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();run(args.out)
