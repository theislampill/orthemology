#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,tempfile
R=Path(__file__).resolve().parent
W=R.parent
D=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for entry in json.loads((R/'INPUTS.json').read_text()):
    p=W/entry['path']
    assert D(p)==entry['sha256'],f'Input hash mismatch: {p}'
for entry in json.loads((R/'MANIFEST.json').read_text()):
    p=R/entry['path']
    assert D(p)==entry['sha256'],f'Artifact hash mismatch: {p}'
subprocess.run(['python',str(R/'check_overlaps.py')],check=True,capture_output=True,text=True)
V=R/'validation';V.mkdir(exist_ok=True)
out=Path(tempfile.mkdtemp(prefix='fresh-',dir=V))
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
import os
env=dict(os.environ);env['LEAN_PATH']=str(out)
records=[]
for name,p in [('Strictness',R/'Strictness.lean'),('Confluence',R/'Confluence.lean'),
               ('CaseOperational',R/'replay/CaseOperational.lean'),('MixedPERControl',R/'MixedPERControl.lean')]:
    cmd=[str(lean),'--trust=0','-o',str(out/(name+'.olean')),str(p)]
    res=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=120)
    log=res.stdout+res.stderr;(out/(name+'.log')).write_text(log)
    assert res.returncode==0,log
    assert 'sorryAx' not in log and 'error:' not in log,log
    records.append({'module':name,'source_sha256':D(p),'olean_sha256':D(out/(name+'.olean')),
                    'exit_code':res.returncode,'log':str((out/(name+'.log')).relative_to(R))})
receipt={'status':'PASS','scope':'Added operational/adversarial controls only; no source baseline rebuild',
         'output_directory':str(out.relative_to(R)),'modules':records}
(V/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
