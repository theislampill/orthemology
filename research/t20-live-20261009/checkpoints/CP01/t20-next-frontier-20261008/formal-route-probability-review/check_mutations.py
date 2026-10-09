from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

root=Path(__file__).resolve().parent
base=root.parent/'formal-identification'
workspace=root/'mutation-workspace'
workspace.mkdir(exist_ok=True)
for path in (root/'frozen').glob('*.lean'):
    shutil.copyfile(path,workspace/path.name)
lean=base/'toolchain/lean-4.19.0-linux/bin/lean'
env=dict(os.environ)
env['LEAN_PATH']=str(workspace)+':'+env['LEAN_PATH']
records={}

def compile_module(module,label,expected=0,pieces=()):
    args=[str(lean),'-DwarningAsError=true','--root='+str(workspace),'-o',str(workspace/(module+'.olean')),str(workspace/(module+'.lean'))]
    result=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,cwd=base/'mathlib')
    log=root/'results'/(label+'.log')
    log.write_text(result.stdout)
    records[label]={'exit_code':result.returncode,'source_sha256':hashlib.sha256((workspace/(module+'.lean')).read_bytes()).hexdigest(),'log':str(log.relative_to(root))}
    assert (result.returncode==0)==(expected==0),(label,result.stdout)
    if expected!=0:
        assert all(piece in result.stdout for piece in pieces),(label,'wrong failure',result.stdout)
        assert not any(word in result.stdout.lower() for word in ('unknown module','unknown package','no such file','object file')),(label,'environment error')

for module in ('BernoulliAssignments','HistogramGrouping','Model','GenerativePanels'):
    compile_module(module,'baseline-'+module)
model=(root/'frozen/Model.lean').read_text()
old='if enabled S (M.kind r) ∧ ω r = true then M.outputs r else ∅'
assert model.count(old)==1
(workspace/'Model.lean').write_text(model.replace(old,old.replace('= true','= false')))
compile_module('Model','reversed-success-gate',1,('error: type mismatch','x ∈ M.outputs r','False : Prop'))
(workspace/'Model.lean').write_text(model)
compile_module('Model','restored-success-gate')
old='| .c => 5 / 6'
assert model.count(old)==1
(workspace/'Model.lean').write_text(model.replace(old,'| .c => 2 / 3'))
compile_module('Model','altered-calibration-model')
compile_module('GenerativePanels','altered-calibration-panel',1,('error: unsolved goals','(2 / 3) ^ hit','(5 / 6) ^ hit'))
(workspace/'Model.lean').write_text(model)
compile_module('Model','restored-calibration-model')
compile_module('GenerativePanels','restored-calibration-panel')
assert (workspace/'Model.lean').read_text()==model
(root/'results/INDEPENDENT_MUTATION_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
