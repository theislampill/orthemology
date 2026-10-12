"""Finite causal-abstraction discriminator; not a metaphysical model of originals.

Modified HP clauses implemented for candidate root conjunctions A/B and effect E=1.
All noncandidate endogenous variables may be held at their actual values.
"""
from itertools import combinations,product
import json

V=('A','B','HA','HB','E')
def subsets(xs):
    return [c for n in range(len(xs)+1) for c in combinations(xs,n)]

class Model:
    def __init__(self,kind):
        assert kind in ('left','right','parallel','and')
        self.kind=kind
    def solve(self,u=(1,1),intervention=None):
        i=intervention or {}; v={}
        def put(k,f): v[k]=i[k] if k in i else int(f())
        put('A',lambda:u[0]); put('B',lambda:u[1])
        if self.kind=='left':
            put('HA',lambda:v['A']); put('HB',lambda:v['B'] and not v['HA'])
        elif self.kind=='right':
            put('HB',lambda:v['B']); put('HA',lambda:v['A'] and not v['HB'])
        else:
            put('HA',lambda:v['A']); put('HB',lambda:v['B'])
        put('E',lambda:(v['HA'] and v['HB']) if self.kind=='and' else (v['HA'] or v['HB']))
        return v

def ac2(model,u,candidate):
    actual=model.solve(u)
    if actual['E']!=1: return None
    rest=tuple(x for x in V if x not in candidate)
    for alt in product((0,1),repeat=len(candidate)):
        if all(actual[x]==a for x,a in zip(candidate,alt)): continue
        for held in subsets(rest):
            intervention={x:actual[x] for x in held}
            intervention.update(zip(candidate,alt))
            if model.solve(u,intervention)['E']==0:
                return {'changed':dict(zip(candidate,alt)),'held':{x:actual[x] for x in held}}
    return None

def modified_causes(model,u):
    # Candidate causes are deliberately restricted to original input assignments,
    # not asserted to enumerate all causes involving route/outcome variables.
    accepted=[]
    for c in subsets(('A','B')):
        if c and not any(set(d)<set(c) for d in accepted) and ac2(model,u,c) is not None:
            accepted.append(c)
    return accepted

def concordant_identification():
    inputs=list(product((0,1),repeat=2))
    # All Boolean laws, then the exact concordant-input observational restriction.
    laws=[dict(zip(inputs,ys)) for ys in product((0,1),repeat=4)]
    admissible=((0,0),(1,1))
    remaining=[f for f in laws if f[(0,0)]==0 and f[(1,1)]==1]
    off=((0,1),(1,0))
    def identifies(queries):
        signatures=[tuple(f[x] for x in queries) for f in remaining]
        return len(set(signatures))==len(remaining)
    minimum=[q for q in subsets(off) if identifies(q) and not any(identifies(t) for t in subsets(q) if len(t)<len(q))]
    return {'all_boolean_laws':len(laws),'compatible_with_concordant_data':len(remaining),
            'law_vectors':[list(f.values()) for f in remaining],
            'input_order':[list(x) for x in inputs],
            'minimal_identifying_extra_query_sets':[[list(x) for x in q] for q in minimum],
            'all_required_extra_queries_outside_admitted_diagonal':all(x not in admissible for q in minimum for x in q),
            'interpretation':'Off-diagonal interventions discriminate laws only if separately admitted; no metaphysical admissibility inferred.'}

def run():
    models=[Model(k) for k in ('left','right','parallel')]
    tables=[[] for _ in models]; count=0; and_table=[]
    for u in product((0,1),repeat=2):
        for vals in product((None,0,1),repeat=3):
            i={k:v for k,v in zip(('A','B','E'),vals) if v is not None}
            for m,t in zip(models,tables):
                s=m.solve(u,i);t.append(tuple(s[k] for k in ('A','B','E')))
            s=Model('and').solve(u,i);and_table.append(tuple(s[k] for k in ('A','B','E')))
            count+=1
    actual=[m.solve() for m in models]
    # Observed A=B=E=1 throughout, route A-only differs.
    route=[v['HA']==1 and v['HB']==0 for v in actual]
    # The projection ignores HA. Its induced cylinder-image intervention map sends
    # do(HA=0) to empty (all A/B/E valuations remain in the image), yet in the
    # left model with u=(1,0), that intervention changes E.
    m=Model('left');u=(1,0)
    fine_failure=m.solve(u,{'HA':0})['E']!=m.solve(u)['E']
    return {'scope':'Root/output interventions only; candidate actual causes restricted to A/B; no original-source interpretation',
            'root_output_intervention_comparisons':count,
            'all_three_output_tables_equal':tables[0]==tables[1]==tables[2],
            'conjunctive_negative_control_equal':tables[0]==and_table,
            'actual_fine_states':dict(zip(('left','right','parallel'),actual)),
            'modified_hp_root_causes':{m.kind:modified_causes(m,(1,1)) for m in models+[Model('and')]},
            'route_predicate_fibre_constant':len(set(route))==1,
            'fine_intervention_breaks_coarse_empty_mapping':fine_failure,
            'witnesses':{m.kind:{'+'.join(c):ac2(m,(1,1),c) for c in modified_causes(m,(1,1))} for m in models},
            'concordant_identification':concordant_identification(),
            'full_created_process_equality_claimed':False,
            'metaphysical_countermodel_claimed':False}

if __name__=='__main__': print(json.dumps(run(),indent=2))
