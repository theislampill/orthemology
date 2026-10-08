#!/usr/bin/env python3
"""Finite semantic controls for a philosophical conditional argument.

These are logical interpretations. None is asserted metaphysically possible.
No source-specific philosophical premise is verified by this script.
"""
import itertools
import argparse
import json
from pathlib import Path

# status: 0 absent, 1 present unreceived, 2 present received; g is fixed.
def evaluate(r, state, a=0):
    n = len(state)
    e = lambda w: state[w] != 0
    u = lambda w: state[w] == 1
    rec = lambda w: state[w] == 2
    poss_e = lambda w: any(r[w][z] and e(z) for z in range(n))
    poss_u = lambda w: any(r[w][z] and u(z) for z in range(n))
    poss_rec = lambda w: any(r[w][z] and rec(z) for z in range(n))
    relevant = [w for w in range(n) if r[a][w]]
    # A realisation of exact U from whole absence would need U and Received.
    # Causal-content fidelity therefore excludes any such realisation.
    fpc = all(not (not e(w) and poss_u(w)) for w in relevant)
    return {
        'actual_unreceived': u(a),
        'necessity_g': all(e(w) for w in relevant),
        'local_reverse_access': all(r[w][a] for w in relevant),
        'absent_possibility_coverage': all(e(w) or poss_u(w) for w in relevant),
        'fact_completeness_under_fidelity': fpc,
        'object_completeness': all(e(w) or not poss_e(w) or poss_rec(w) for w in relevant),
        'local_essential_unreceivability': all(not rec(w) for w in relevant),
        'two_step_reach_closure': all(not (r[a][v] and r[v][w]) or r[a][w]
                                      for v in range(n) for w in range(n)),
        'symmetric': all(r[v][w] == r[w][v] for v in range(n) for w in range(n)),
    }

controls = {}
r_complete = [[True]*3 for _ in range(3)]
controls['object_not_fact'] = evaluate(r_complete,[1,0,2])
assert controls['object_not_fact']['object_completeness']
assert not controls['object_not_fact']['fact_completeness_under_fidelity']
assert not controls['object_not_fact']['necessity_g']

r_chain = [[True,True,False],[True,True,True],[False,True,True]]
controls['symmetry_not_composition'] = evaluate(r_chain,[1,0,2])
assert controls['symmetry_not_composition']['symmetric']
assert controls['symmetry_not_composition']['local_essential_unreceivability']
assert controls['symmetry_not_composition']['object_completeness']
assert not controls['symmetry_not_composition']['two_step_reach_closure']
assert not controls['symmetry_not_composition']['necessity_g']

r_forward = [[True,True],[False,True]]
controls['no_reverse_access'] = evaluate(r_forward,[1,0])
assert controls['no_reverse_access']['fact_completeness_under_fidelity']
assert not controls['no_reverse_access']['local_reverse_access']
assert not controls['no_reverse_access']['necessity_g']

# Full reverse accessibility is not necessary: relevant b lacks access to a,
# but c supplies U, so the weaker exact-fact possibility coverage suffices.
r_weaker = [[True,True,True],[False,True,True],[False,False,True]]
controls['coverage_without_reverse_access'] = evaluate(r_weaker,[1,0,1])
assert controls['coverage_without_reverse_access']['absent_possibility_coverage']
assert not controls['coverage_without_reverse_access']['local_reverse_access']
assert not controls['coverage_without_reverse_access']['necessity_g']
assert not controls['coverage_without_reverse_access']['fact_completeness_under_fidelity']

counts = {'frames_and_valuations_checked':0, 'with_actual_u_and_absent_coverage':0,
          'with_object_bridge_antecedents':0}
for n in range(1,4):
    for flat in itertools.product((False,True), repeat=n*n):
        r = [list(flat[i*n:(i+1)*n]) for i in range(n)]
        for tail in itertools.product(range(3),repeat=n-1):
            state=[1,*tail]
            v=evaluate(r,state)
            counts['frames_and_valuations_checked']+=1
            if v['absent_possibility_coverage']:
                counts['with_actual_u_and_absent_coverage']+=1
                assert v['fact_completeness_under_fidelity'] == v['necessity_g']
            if (v['local_reverse_access'] and v['object_completeness']
                    and v['local_essential_unreceivability'] and v['two_step_reach_closure']):
                counts['with_object_bridge_antecedents']+=1
                assert v['necessity_g']

# Role occupancy differs from rigid bearer existence even with a unique full
# modal ground at every world and constant contents p,q.
role_ground = {'a':'g','b':'h'}
roles={'all_worlds_have_unique_full_ground':len(role_ground)==2,
       'g_exists_at_all_worlds':all(x=='g' for x in role_ground.values()),
       'grounds_preserve_rigid_identity':True}
assert roles['all_worlds_have_unique_full_ground'] and not roles['g_exists_at_all_worlds']

report={
 'scope':'Finite logical semantic checks only; no metaphysical possibility or actual warrant asserted.',
 'controls':controls,'enumeration':counts,'role_control':roles,
 'result':'PASS',
 'proof_limit':'Enumeration through three worlds corroborates controls; general results use the written proof.'
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,help='Optional receipt destination; default prints only.')
args=parser.parse_args()
if args.output is not None:
    args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
