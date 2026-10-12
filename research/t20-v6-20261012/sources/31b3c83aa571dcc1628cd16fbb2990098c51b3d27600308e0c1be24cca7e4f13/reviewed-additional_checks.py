"""Second calculation and mutation checks; same author, not independent review."""
from itertools import product,combinations
from pathlib import Path
import subprocess,tempfile,json,sys
import rivals as r

HERE=Path(__file__).resolve().parent

def brute_sufficient(worlds,target,menu):
    # Pairwise collision calculation, independent of the production bucket routine.
    for a,b in combinations(worlds,2):
        if a.target[target]!=b.target[target] and all(a.observations[k]==b.observations[k] for k in menu):
            return False
    return True


def run_checks():
    groups={
        'token':([r.token_case(k,f,s) for k,f,s in product(r.TOKEN_KINDS,[False,True],[False,True])],['commission','report_true','sincere']),
        'challenge':([r.challenge_case(k,n) for k,n in product(r.CHALLENGE_KINDS,range(4))],['origin','mission']),
        'institution':([r.institution_case(*a) for a in product([False,True],[False,True],[False,True],[2,4],[False,True],[False,True])],['holder']),
        'discourse':([r.discourse_case(k,s,t) for k,s,t in product(['assert','quote','report'],['P','Q'],[0,1])],['asserts_p0'])}
    checked=0
    for worlds,targets in groups.values():
        for target in targets:
            keys=sorted(worlds[0].observations)
            all_sets=[s for n in range(len(keys)+1) for s in combinations(keys,n)]
            successful=[]
            for subset in all_sets:
                expected=brute_sufficient(worlds,target,subset)
                assert r.sufficient(worlds,target,subset)==expected
                if expected:successful.append(subset)
                checked+=1
            minimal=[s for s in successful if not any(set(t)<set(s) for t in successful)]
            assert r.minimal_discriminators(worlds,target)==minimal
    # External-to-interpreter closed formula for the deliberately fixed sequence.
    for params in product([False,True],[False,True],[False,True],[2,4],[False,True],[False,True]):
        mutable,removed,published,time,descent,up=params
        w=r.institution_case(*params)
        expected='N' if mutable and not removed and published and time>=3 else 'P'
        assert w.target['holder']==expected
        assert w.target['operational']==up and w.target['descent']==descent
    # Every received discourse fragment is equal; truth/act outcomes are not.
    worlds,_=groups['discourse']
    assert len({w.observations['received'] for w in worlds})==1
    assert all(w.target['translation_preserves_embedded'] for w in worlds)
    for w in worlds:
        _,kind,speaker,time=w.name.split(':')
        expected=(kind=='assert' and speaker=='P' and time=='0')
        assert w.target['asserts_p0']==expected
        if kind=='report':assert w.target['outer_true'] is True
    # In each world actual sender, report truth and private belief can come apart.
    a=r.token_case('attest',False,True);b=r.token_case('attest',True,False)
    assert a.observations==b.observations and a.target['commission'] and b.target['commission']
    assert a.target['report_true'] is False and b.target['sincere'] is False
    return {'observation_menu_checks':checked,'institution_oracle_cases':64,'discourse_oracle_cases':12}


def mutations():
    source=(HERE/'rivals.py').read_text()
    specs={
        'custody_equals_purpose':("commission=instructions.get('P')==INVENTORY","commission=True"),
        'source_emission_equals_attestation':("mission=(('P_direct_instruction',instruction) in events and origin\n             and ('P_dispatches_response','E') in events)","mission=origin"),
        'ignore_founding_amendment_rule':("if (c.amendment_allowed and proposal==motion=='allow_fresh_appointment'","if (True and proposal==motion=='allow_fresh_appointment'"),
        'count_removed_voter':("if motion==proposal and voter in members:","if motion==proposal:"),
        'quotation_equals_assertion':("'asserts_p0':tree==('assert','P',('atom',('at','P','lab',0)))","'asserts_p0':atom==('at','P','lab',0)"),
        'report_endorses_embedded_content':("elif tree[2][0]=='said':outer_true=(tree[2][1],tree[2][2][1]) in uttered","elif tree[2][0]=='said':outer_true=atom in true_atoms"),
        'ignore_dispatch_recipient':("and ('P_dispatches_response','E') in events)","and any(e[0]=='P_dispatches_response' for e in events))")}
    out=[]
    for name,(old,new) in specs.items():
        assert source.count(old)==1,(name,source.count(old))
        # Isolated temporary copies ensure mutations never alter retained or current code.
        with tempfile.TemporaryDirectory(dir=HERE,prefix='mutation-') as d:
            d=Path(d);(d/'rivals.py').write_text(source.replace(old,new))
            (d/'test_rivals.py').write_bytes((HERE/'test_rivals.py').read_bytes())
            proc=subprocess.run([sys.executable,'-B','-m','unittest','discover','-v'],cwd=d,capture_output=True,text=True)
            assert proc.returncode!=0,name
            assert 'FAIL:' in proc.stderr and 'ERROR:' not in proc.stderr,(name,proc.stderr)
            out.append({'name':name,'exit_code':proc.returncode,
                        'failed_tests':[line for line in proc.stderr.splitlines() if line.startswith('FAIL:')]})
    return out

if __name__=='__main__':print(json.dumps({'checks':run_checks(),'mutations':mutations()},indent=2))
