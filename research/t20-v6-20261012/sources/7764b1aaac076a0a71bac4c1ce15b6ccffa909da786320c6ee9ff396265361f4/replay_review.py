#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
bindings=json.loads((ROOT/'SNAPSHOT_BINDINGS.json').read_text())
def check_snapshot():
    for rel,item in bindings['files'].items():
        data=(ROOT/'snapshot'/rel).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],rel
check_snapshot()
subject=ROOT/'snapshot/stochastic-inquiry-quotient-transport-20261010'
steps=[([sys.executable,'independent_controls.py'],ROOT,'independent_controls.log'),([sys.executable,'check_transport.py'],subject,'AUTHOR_TRANSPORT_REPLAY.log'),([sys.executable,'check_posterior_tail.py'],subject,'AUTHOR_POSTERIOR_TAIL_REPLAY.log')]
commands=[]
for args,cwd,log in steps:
    run=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (ROOT/log).write_text(run.stdout)
    commands.append({'command':args[1:],'cwd':str(cwd.relative_to(ROOT)) or '.','exit_code':run.returncode,'log':log})
    if run.returncode:raise RuntimeError(run.stdout)
check_snapshot()
ind=json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_text())
author=json.loads((subject/'POSTERIOR_TAIL_RESULTS.json').read_text())
transport=json.loads((subject/'CONTROL_RESULTS.json').read_text())
assert ind['status']==author['status']==transport['status']=='PASS'
receipt={'status':'PASS_SCOPED','accepted_addendum_sha256':bindings['accepted_addendum_sha256'],'accepted_author_manifest_sha256':bindings['accepted_author_manifest_sha256'],'snapshot_file_count':len(bindings['files']),'snapshot_intact_before_and_after':True,'commands':commands,'independent_counts':{k:v for k,v in ind.items() if type(v) is int},'author_posterior_word_controls':author['finite_word_controls'],'author_domination_word_controls':author['same_support_domination_word_cases'],'author_closed_tensor_dimensions':author['posterior_cross_product_span_dimensions'],'author_transport_status':transport['status'],'scope':'Ordinary scoped review and exact controls; no empirical, kernel, novelty, integration or programme-closure claim.'}
(ROOT/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
