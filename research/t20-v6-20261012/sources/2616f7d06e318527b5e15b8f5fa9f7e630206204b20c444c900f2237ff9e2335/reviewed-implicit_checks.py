"""Same-author independent arithmetic and exhaustive contextual checks."""
from itertools import product
from pathlib import Path
from dataclasses import replace
import tempfile,subprocess,sys,json
import implicit_attestation as i


def check():
    checked=0
    for p in i.candidate_policies():
        for vals in product([False,True],repeat=7):
            s=i.Situation(*vals)
            plans=i.feasible_plans(p,s);chosen=i.choose(p,s)
            assert chosen and all(x.utility==max(y.utility for y in plans) for x in chosen)
            if not(s.question_heard and s.audience_waiting):
                assert all(x.aim!='audience accepts present commission claim' for x in chosen)
            # Changing actual truth while keeping source belief fixed cannot change planning.
            alternate=i.choose(p,replace(s,commission_occurred=not s.commission_occurred))
            assert chosen==alternate
            checked+=1
    # Independent closed comparisons for the four calibration episodes.
    expected=[]
    for p in i.candidate_policies():
        quiet=max(0,p.courtesy-1)==0
        rejection=(p.communicate-1)>max(0,p.courtesy-1,p.question_courtesy-1,p.deceive-1)
        repairs=(p.repair-1)>0 and (p.repair-1)>=p.courtesy-1
        warms=(p.warmth-1)>0 and (p.warmth-1)>=p.courtesy-1
        if quiet and rejection and repairs and warms:expected.append(p)
    observed=[p for p in i.candidate_policies() if i.compatible(p,i.calibration_episodes())]
    assert expected==observed and len(observed)==3
    return {'policy_context_combinations':checked,'independent_calibration_survivors':len(expected)}


def mutate():
    here=Path(__file__).resolve().parent;source=(here/'implicit_attestation.py').read_text()
    specs={
      'handover_equals_intent':("intended=next(iter(intention_values)) if len(intention_values)==1 else None","intended=(out=='send_mantle')"),
      'ignore_public_information_need':("demand=s.question_heard and s.audience_waiting","demand=True"),
      'planning_reads_actual_truth':("if s.source_believes_commission and recognizable:","if s.commission_occurred and recognizable:"),
      'collapse_tied_intentions':("intended=next(iter(intention_values)) if len(intention_values)==1 else None","intended=all(intention_values)")}
    result=[]
    for name,(old,new) in specs.items():
        assert source.count(old)==1
        with tempfile.TemporaryDirectory(dir=here,prefix='implicit-mutation-') as tmp:
            tmp=Path(tmp);(tmp/'implicit_attestation.py').write_text(source.replace(old,new))
            (tmp/'test_implicit.py').write_bytes((here/'test_implicit.py').read_bytes())
            proc=subprocess.run([sys.executable,'-B','-m','unittest','test_implicit','-v'],cwd=tmp,capture_output=True,text=True)
            assert proc.returncode!=0 and 'FAIL:' in proc.stderr,(name,proc.stderr)
            result.append({'mutation':name,'rejected':True,'exit_code':proc.returncode,
                           'failed_tests':[x for x in proc.stderr.splitlines() if x.startswith('FAIL:')]})
    return result

if __name__=='__main__':print(json.dumps({'exhaustive':check(),'mutations':mutate()},indent=2))
