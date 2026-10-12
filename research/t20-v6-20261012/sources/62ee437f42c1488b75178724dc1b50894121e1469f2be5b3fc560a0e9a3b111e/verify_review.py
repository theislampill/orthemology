from pathlib import Path
import json,hashlib,shutil,subprocess,time,os,sys
BASE=Path(__file__).resolve().parent
FRONT=BASE.parents[1]
TRANCHE=FRONT.parent
snapshot=BASE/'reviewed-snapshots';snapshot.mkdir(exist_ok=True)
paths=[
('cognition_report','intrinsic-willing/COGNITION_REFINEMENT.md','Complete direct review'),
('joint_report','intrinsic-willing/JOINT_RESULT.md','Complete direct review'),
('knower','intrinsic-willing/src/intrinsic_knower.py','Complete direct code review'),
('joint','intrinsic-willing/src/joint_interpretation.py','Complete direct code review'),
('intentions','intrinsic-willing/src/intentions.py','Previously read complete; supporting import'),
('provision_report','provision-identity/RESULT.md','Sections6.1–6.6 plus earlier report; latest narrowing reviewed'),
('provision','provision-identity/src/provision_semantics.py','Earlier complete interface; current primitive Entire additions checked by direct report and replay'),
('preservation','provision-identity/src/preservation_modes.py','Complete direct code review'),
('trace','provision-identity/src/trace_reduction.py','Complete direct code review'),
('trace_lean','provision-identity/src/TraceReduction.lean','Complete direct declaration/proof inspection; no independent kernel rerun'),
('beginningless','explanatory-review/BeginninglessJointProvision.lean','Complete direct declaration/proof inspection; no independent kernel rerun'),
('beginningless_receipt','explanatory-review/VERIFICATION.json','Author receipt inspected, not treated as this reviewer kernel execution'),
]
records=[]
for ident,relative,scope in paths:
 p=FRONT/relative;b=p.read_bytes();dst=snapshot/(ident+p.suffix);shutil.copyfile(p,dst)
 records.append({'id':ident,'path':str(p.relative_to(TRANCHE.parent)),'snapshot':str(dst.relative_to(TRANCHE.parent)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'scope':scope})
for n in [514,515,516]:
 p=TRANCHE/f'research-frontier/inspection/asbahani/p-{n}.png';b=p.read_bytes()
 records.append({'id':f'Asbahani{n-100}','path':str(p.relative_to(TRANCHE.parent)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'scope':f'Direct scan reread; visible printed{n-100}; no new acquisition or edition collation. Modern apparatus separate.'})
commands=[('independent_controls',[sys.executable,str(BASE/'independent_joined_controls.py')],None),
 ('willing_tests',[sys.executable,'-m','unittest','discover','-s',str(FRONT/'intrinsic-willing/src'),'-p','test_*.py','-v'],None),
 ('provision_tests',[sys.executable,'-m','unittest','-v','test_provision_semantics','trace_reduction','preservation_modes'],str(FRONT/'provision-identity/src'))]
runs=[]
for name,cmd,py_path in commands:
 env=os.environ.copy()
 if py_path:env['PYTHONPATH']=py_path
 start=time.perf_counter();r=subprocess.run(cmd,text=True,capture_output=True,env=env);seconds=time.perf_counter()-start
 (BASE/(name+'-verified.log')).write_text(r.stdout+r.stderr)
 runs.append({'name':name,'command':cmd,'exit_code':r.returncode,'execution_seconds':seconds,'log':name+'-verified.log'})
 assert r.returncode==0,name
for r in records:
 p=TRANCHE.parent/r['path']
 r['unchanged_during_replay']=hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 assert r['unchanged_during_replay'],r['id']
result={'schema':'source-fidelity-review-continuation/2','time_marker_utc':'2026-10-07T21:49:52Z','scope':'Positive reduced-signature countermodel and source-warrant review; no full-source or closure certificate','bindings':records,'runs':runs,'preserved_prior_review':'../REVIEW.md and its source/snapshot bindings remain untouched','accounting':'Only per-command execution seconds measured. No wall-clock review envelope, idle gap, packaging or parallel duration credited.'}
(BASE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'source_bindings':len(records),'all_runs_passed':all(r['exit_code']==0 for r in runs),'all_sources_stable':all(r['unchanged_during_replay'] for r in records)},indent=2))
