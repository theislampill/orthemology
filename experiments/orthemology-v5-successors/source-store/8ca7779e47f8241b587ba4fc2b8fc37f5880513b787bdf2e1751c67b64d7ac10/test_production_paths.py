"""Poisoned baseline calls and direct production structural-work controls."""
from contextlib import ExitStack
from fractions import Fraction as Q
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'tranche18/research/hidden-change/efficient-v1'),
              str(ROOT/'tranche18/research/hidden-change/reference-v1')]
from oracle import fixture,raw_model,full_pairs
import certificates,finite,synthesis,model,dependencies,mec,efficient,negative

class ProductionPaths(unittest.TestCase):
    def test_actual_solve_and_negative_poisoned_baseline(self):
        forbidden=[finite.all_components,synthesis.all_components,synthesis.known_operator,
                   synthesis.uncertain_operator,synthesis.solve,synthesis.descend,
                   certificates.check_negative,synthesis.check_negative]
        forbidden_codes={f.__code__ for f in forbidden}
        calls={}; bodies=[]
        def poison(*args,**kwargs):
            raise AssertionError('polynomial production invoked poisoned exhaustive baseline')
        def profile(frame,event,arg):
            if event=='call':
                if frame.f_code in forbidden_codes:
                    raise AssertionError('polynomial production entered exhaustive baseline code')
                path=Path(frame.f_code.co_filename)
                if path.name in ('efficient.py','negative.py','mec.py'):
                    key=path.name+':'+frame.f_code.co_name
                    calls[key]=calls.get(key,0)+1
        fixtures=[fixture(),fixture(d=lambda t,s,a:1),
                  fixture(2,p=lambda t,s,a:tuple(Q(y==(1-s if t==0 else s)) for y in range(2)),d=lambda t,s,a:s),
                  fixture(2,2,p=lambda t,s,a:(Q(1,2),Q(1,2)) if t==0 else (Q(1,3),Q(2,3)),
                          d=lambda t,s,a:2 if t==a else 1),
                  fixture(1,3,d=lambda t,s,a:((2,3,1),(3,2,1))[t][a])]
        with ExitStack() as stack:
            for module in (finite,synthesis,certificates,dependencies,mec,efficient,negative):
                for name,value in list(vars(module).items()):
                    if any(value is f for f in forbidden): stack.enter_context(patch.object(module,name,poison))
            sys.setprofile(profile)
            try:
                for inp in fixtures:
                    m=model.validate_model(raw_model(inp));body=efficient.solve(m)
                    if isinstance(body,certificates.Negative):
                        self.assertIsNotNone(negative.check_negative(m,body))
                        self.assertIsNone(negative.check_negative(m,{'k_trace':((),()),'w_trace':((),())}))
                    else: self.assertIsNotNone(certificates.check_positive(m,body))
                    bodies.append((m,body))
            finally: sys.setprofile(None)
        self.assertGreater(calls.get('efficient.py:solve',0),0)
        self.assertGreater(calls.get('negative.py:check_negative',0),0)
        for m,body in bodies:
            if isinstance(body,certificates.Negative): self.assertIsNotNone(certificates.check_negative(m,body))
            else: self.assertIsNotNone(certificates.check_positive(m,body))
        (HERE/'POISONED_PATH_RECEIPT_v1.json').write_text(json.dumps(dict(
            fixtures=len(fixtures),forbidden_entries=0,
            forbidden_functions=sorted(set(f.__module__+'.'+f.__name__ for f in forbidden)),
            observed_production_calls=calls),indent=2)+'\n')

    def test_scc_and_distinct_threshold_call_bounds(self):
        reports=[]
        huge=2**4096
        inp=fixture(3,4,p=lambda t,s,a:tuple(Q(y==s) for y in range(3)),
                    d=lambda t,s,a:(huge+2*a if t==0 else huge+2*(3-a)))
        m=model.validate_model(raw_model(inp));pairs=full_pairs(inp);pair_count=len(pairs)
        actual_scc=mec._strongly_connected
        actual_mec=mec.maximal_components
        for theta in ('known',0,1):
            per_mec=[]
            def count_mec(*args,**kwargs):
                count=0
                def count_scc(*a,**k):
                    nonlocal count
                    count+=1
                    return actual_scc(*a,**k)
                with patch.object(mec,'_strongly_connected',count_scc): result=actual_mec(*args,**kwargs)
                self.assertLessEqual(count,2*m.n_states-1)
                per_mec.append(count)
                return result
            with patch.object(efficient,'maximal_components',count_mec):
                if theta=='known': efficient.known_components(m,pairs)
                else: efficient.uncertain_components(m,theta,pairs)
            bound=pair_count if theta=='known' else pair_count+pair_count**2
            self.assertLessEqual(len(per_mec),bound)
            reports.append(dict(candidate=theta,pair_count=pair_count,mec_calls=len(per_mec),
                                threshold_bound=bound,scc_calls_per_mec=per_mec,scc_bound=2*m.n_states-1,
                                priority_bit_length=huge.bit_length()))
        (HERE/'STRUCTURAL_COUNT_CONTROLS_v1.json').write_text(json.dumps(reports,indent=2)+'\n')

if __name__=='__main__': unittest.main(verbosity=2)
