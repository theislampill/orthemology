#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
bindings=json.loads((ROOT/'SNAPSHOT_BINDINGS.json').read_text())
def check_snapshot():
    for name,item in bindings['files'].items():
        data=(ROOT/'snapshot'/name).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],name
check_snapshot()
subject=ROOT/'snapshot/stochastic-exact-inquiry-20261010'
steps=[([sys.executable,'independent_controls.py'],ROOT,'independent_controls.log'),([sys.executable,'source_transport_controls.py'],ROOT,'source_transport_controls.log'),([sys.executable,'-m','unittest','discover','-p','test_*.py'],subject,'AUTHOR_UNITTEST_REPLAY.log'),([sys.executable,'verify.py'],subject,'AUTHOR_VERIFY_REPLAY.log')]
results=[]
for args,cwd,log in steps:
    run=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (ROOT/log).write_text(run.stdout)
    results.append({'command':args[1:],'cwd':str(cwd.relative_to(ROOT)) or '.','exit_code':run.returncode,'log':log})
    if run.returncode:raise RuntimeError(run.stdout)
check_snapshot()
independent=json.loads((ROOT/'INDEPENDENT_CONTROLS.json').read_text())
transport=json.loads((ROOT/'SOURCE_TRANSPORT_CONTROLS.json').read_text())
author=json.loads((subject/'CONTROL_RESULTS.json').read_text())
assert independent['status']==transport['status']==author['status']=='PASS'
receipt={'status':'PASS_SCOPED','reviewed_report_sha256':bindings['reviewed_report_sha256'],'snapshot_file_count':len(bindings['files']),'snapshot_intact_before_and_after':True,'commands':results,'independent_counts':independent['counts'],'source_transport_counts':{k:v for k,v in transport.items() if isinstance(v,int)},'author_unit_tests':7,'author_oracle_models':sum(author['exhaustive_oracle_comparison'][k] for k in ('static_two_state_two_actions','hidden_three_state_one_action','hidden_two_action_seeded','outside_PD_fixture')),'author_input_hashes_verified':author['input_hashes_verified'],'scope':'Ordinary mathematical review with independent exact controls; no kernel, empirical, integration, priority or programme-closure claim.'}
(ROOT/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
