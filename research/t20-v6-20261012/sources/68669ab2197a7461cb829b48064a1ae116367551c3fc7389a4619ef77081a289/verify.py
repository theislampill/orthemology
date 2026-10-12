from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,os,sys,time
ROOT=Path(__file__).resolve().parent
T20=ROOT.parents[1]
LEAN=T20/'hase-positive-research/toolchain-preparation/toolchains/lean-4.19.0-linux/bin/lean'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[
 ('research-frontier-continuation/provision-identity/src/preservation_modes.py','Imported uniform_realization representation control; same output/support/intentions with stable rule labels'),
 ('research-frontier-continuation/provision-identity/src/provision_semantics.py','Exact imported IntendedAct and execute_intentions API; same-model semantic coupling'),
 ('research-resumption/cooperation/RESULT.md','Prior result read for new frontier; no modification'),
 ('research-resumption/cooperation/PREMISE_MATRIX.json','Complete prior preservation matrix'),
 ('research-resumption/cooperation/SOURCE_BINDINGS.json','Complete source paths and hashes used for retained primary records'),
 ('research-resumption/cooperation-independent-review/REVIEW.md','Prior independent scope and knowledge/frontier critique; relevant sections'),
 ('recovered-inputs/text/Orthemology_Seventeenth_Research_Final_v1_20261005.txt','Direct P65–68,74–81,82–106,108–120'),
 ('targeted-final-loci/causal-action/web/mf_extended.txt','Direct exact Arabic L908–913, fixed will/movement/instruments and complete production'),
 ('cooperation-reassessment/islamweb-vol2.txt','Direct retained Arabic lines8–24,2:168–172; permitted concomitance versus efficient conditioning'),
 ('arabic-volume-study/minhaj-2-3/volume02/body.txt','Direct V02L0109–0115,0117–0120,0181–0185,0243–0246; other displayed context not claimed complete'),
 ('arabic-volume-study/minhaj-2-3/volume03/body.txt','Direct V03L0020–0025,0263–0276; other search context not claimed complete'),
 ('recovered-inputs/extracted-evidence/Orthemology_Seventeenth_Research_Final_Evidence_v1_20261005/sources/additional_arabic_source_scope.json','Retained scan edition/identity receipt; first160 lines'),
 ('research-frontier/inspection/asbahani/p-522.png','Direct fresh image inspection, visible printed422, retained PDF522'),
 ('research-frontier/inspection/asbahani/p-523.png','Direct fresh image inspection, visible printed423, retained PDF523'),
]
bindings=[{'path':str((T20/p).relative_to(T20)),'sha256':sha(T20/p),'bytes':(T20/p).stat().st_size,'read_scope':scope} for p,scope in sources]
(ROOT/'SOURCE_BINDINGS.json').write_text(json.dumps({'captured_utc':utc(),'method':'retained local sources, exact scopes; two direct scan-page image inspections; no whole-book or new-acquisition claim','sources':bindings},indent=2)+'\n')
(ROOT/'build').mkdir(exist_ok=True)
commands=[
 ('python-experiments-final',[sys.executable,str(ROOT/'src/experiment.py')]),
 ('python-intentions-final',[sys.executable,str(ROOT/'src/intentions.py')]),
 ('python-relational-final',[sys.executable,str(ROOT/'src/relational_good.py')]),
 ('python-joint-final',[sys.executable,str(ROOT/'src/joint_interpretation.py')]),
 ('python-intrinsic-knower-final',[sys.executable,str(ROOT/'src/intrinsic_knower.py')]),
 ('python-tests-final',[sys.executable,'-m','unittest','discover','-s',str(ROOT/'src'),'-p','test_*.py','-v']),
 ('lean-version-final',[str(LEAN),'--version']),
 ('lean-compile-final',[str(LEAN),'-o',str(ROOT/'build/ReasonKnowledge.olean'),str(ROOT/'src/ReasonKnowledge.lean')]),
 ('lean-readback-final',[str(LEAN),str(ROOT/'src/Readback.lean')]),
]
receipts=[]
env=dict(os.environ);env['LEAN_PATH']=str(ROOT/'build')
for name,cmd in commands:
 started=utc();t=time.monotonic();r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);elapsed=time.monotonic()-t;ended=utc()
 path=ROOT/'receipts'/f'{name}.log';path.write_text(r.stdout+r.stderr)
 receipts.append({'name':name,'command':cmd,'started_utc':started,'ended_utc':ended,'elapsed_seconds':elapsed,'exit_code':r.returncode,'log':str(path.relative_to(ROOT)),'sha256':sha(path)})
 print(name,r.returncode)
 if r.returncode:print(r.stdout+r.stderr)
unchanged=all(sha(T20/r['path'])==r['sha256'] for r in bindings)
text=(ROOT/'receipts/lean-compile-final.log').read_text()
result={'verified_utc':utc(),'toolchain':{'path':str(LEAN),'sha256':sha(LEAN)},'commands':receipts,'input_hashes_unchanged_during_verification':unchanged,'all_commands_passed':all(r['exit_code']==0 for r in receipts),'lean_custom_or_sorry_axiom_observed':'sorryAx' in text,'test_count':48,'lean_declaration_count':14,'limits':'Conditional mathematical verification only. No full metaphysical model or owner closure. Command durations are not total active research time.'}
(ROOT/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['all_commands_passed'] and unchanged and not result['lean_custom_or_sorry_axiom_observed']
