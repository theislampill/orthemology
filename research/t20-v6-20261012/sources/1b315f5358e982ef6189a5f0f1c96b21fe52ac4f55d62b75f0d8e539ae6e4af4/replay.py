#!/usr/bin/env python3
"""Read-only inherited verification plus fresh bounded author/control replay."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent;W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row in json.loads((R/'VERIFIED_INPUTS.json').read_text())['checks']:
    assert sha(W/row['path'])==row['sha256'],row['path']
for row in json.loads((R/'MANIFEST.json').read_text())['files']:
    assert sha(R/row['path'])==row['sha256'],row['path']
author=W/'hase-dependent-substitution-20261010'
for m in ('HasEDependentSubstitution','DependentBranchApplication','ExtensionalSubstitutionControl'):
    assert sha(author/f'{m}.lean')==sha(R/'sources'/f'{m}.lean'),m
out=Path(tempfile.mkdtemp(prefix='replay-',dir=R))
paths=(R/'lean_path.txt').read_text().strip().split(':');paths[0]=str(out)
env=dict(os.environ,LEAN_PATH=':'.join(paths));lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
records=[]
for m,expected in [('HasEDependentSubstitution',0),('DependentBranchApplication',0),('IndependentControls',0),('ExactBranchControl',0),('ExtensionalInputs',0),('RetainedCompatibility',0),('ExtensionalSubstitutionControl',0),('MissingTypedImagesMustFail',1),('UnshiftedBinderMustFail',1),('UnweakenedTypeMapMustFail',1),('UninstantiatedComponentMustFail',1)]:
    source=R/'sources'/f'{m}.lean'; obj=out/f'{m}.olean';logfile=out/f'{m}.log'
    command=[str(lean),'--trust=0','-o',str(obj),str(source)]
    p=subprocess.run(command,env=env,text=True,capture_output=True);log=p.stdout+p.stderr;logfile.write_text(log)
    assert (p.returncode==0)==(expected==0),(m,log)
    code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S);code=re.sub(r'--[^\n]*','',code)
    assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',code),m
    axioms=[]
    if expected==0:
        assert not any(x in log for x in ('sorryAx','error:','warning:')),(m,log)
        for ax in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
            found=set(re.sub(r'\s+','',ax).split(','))-{''}
            assert found <= ({'propext','Quot.sound','Classical.choice'} if m == 'ExtensionalSubstitutionControl' else {'propext','Quot.sound'}),(m,found)
            axioms.extend(found)
    else:
        assert 'type mismatch' in log,(m,log)
    records.append({'module':m,'source_sha256':sha(source),'exit_code':p.returncode,'expected_exit_code':expected,'command':command,'log':str(logfile.relative_to(R)),'log_sha256':sha(logfile),'object_sha256':sha(obj) if obj.exists() else None,'axioms':sorted(set(axioms))})
    print(m,'PASS' if expected==0 else 'EXPECTED REJECTION',flush=True)
for row in json.loads((R/'VERIFIED_INPUTS.json').read_text())['checks']:
    assert sha(W/row['path'])==row['sha256'],row['path']
for m in ('HasEDependentSubstitution','DependentBranchApplication','ExtensionalSubstitutionControl'):
    assert sha(author/f'{m}.lean')==sha(R/'sources'/f'{m}.lean'),m
receipt={'status':'PASS','trust_zero':True,'baseline_rebuilt':False,'protected_mutations':False,'source_freeze_unchanged':True,'lean_binary_sha256':sha(lean),'verified_input_checks':len(json.loads((R/'VERIFIED_INPUTS.json').read_text())['checks']),'fresh_output':str(out.relative_to(R)),'records':records}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: three author modules, four independent positive modules, four adversarial controls; inherited hashes unchanged.')
