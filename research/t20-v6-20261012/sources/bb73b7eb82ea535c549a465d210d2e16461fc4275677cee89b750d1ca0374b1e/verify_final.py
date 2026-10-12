"""Fresh kernel replay; requires the pinned Lean/Mathlib environment and rebuilt prerequisites."""
from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, tempfile

R=Path(__file__).resolve().parent
LEAN=Path(os.environ.get('LEAN_HOME',str(R.parent/'.toolchains/lean-4.19.0-linux')))/'bin/lean'
MODULES=['LiteralShiftSyntax','LiteralShiftScan','LiteralShiftReplay','LiteralShiftCorrect',
         'LiteralShiftEndpoints','LiteralShiftWord','LiteralShiftPrefix','LiteralShiftControls']
RUN=Path(tempfile.mkdtemp(prefix='verified-',dir=R));SRC=RUN/'sources';OUT=RUN/'objects';BASE=RUN/'baseline-objects';LOG=RUN/'logs'
for p in (SRC,OUT,BASE,LOG):p.mkdir()

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition,message):
    if not condition:raise RuntimeError(message)

start=datetime.datetime.now(datetime.timezone.utc).isoformat()
prereq=json.loads((R/'PREREQUISITE_REBUILD.json').read_text())
for item in prereq['modules']:
    rel=Path(item['module'].replace('.','/'))
    source=R/'baseline'/rel.with_suffix('.lean');obj=R/'build'/rel.with_suffix('.olean')
    require(sha(source)==item['source_sha256'],'Baseline source mismatch '+str(rel))
    require(sha(obj)==item['object_sha256'],'Baseline object mismatch '+str(rel))
    target=BASE/rel.with_suffix('.olean');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(obj,target)
pins={m:sha(R/(m+'.lean')) for m in MODULES}
queries=[]
for m in MODULES:
    source=R/(m+'.lean');text=source.read_text()
    require(not re.search(r'\b(sorry|admit|native_decide)\b',text),'Forbidden proof token '+m)
    require(not re.search(r'^\s*(axiom|constant)\s',text,re.M),'New assumption declaration '+m)
    shutil.copyfile(source,SRC/source.name)
    prefix='P02.LiteralShift.Controls.' if m=='LiteralShiftControls' else 'P02.LiteralShift.'
    queries.extend(prefix+n for n in re.findall(r'^\s*(?:@\[[^\n]*\]\s*)?theorem\s+([\w\']+)',text,re.M))
env=dict(os.environ,LEAN_PATH=':'.join([str(OUT),str(BASE),os.environ['LEAN_PATH']]))
records=[]
for m in MODULES:
    command=[str(LEAN),'--trust=0','--root='+str(SRC),'-o',str(OUT/(m+'.olean')),str(SRC/(m+'.lean'))]
    result=subprocess.run(command,env=env,cwd=R,capture_output=True,text=True)
    log=LOG/(m+'.log');log.write_text(result.stdout+result.stderr)
    require(result.returncode==0,m+' failed: '+str(log))
    records.append({'module':m,'source_sha256':pins[m],'object_sha256':sha(OUT/(m+'.olean')),'exit_code':result.returncode,'command':command})
    print('PASS '+m,flush=True)
inspect=SRC/'InspectAllAxioms.lean'
inspect.write_text('import LiteralShiftControls\n'+''.join('#check '+n+'\n#print axioms '+n+'\n' for n in queries))
result=subprocess.run([str(LEAN),'--trust=0','--root='+str(SRC),str(inspect)],env=env,cwd=R,capture_output=True,text=True)
(LOG/'AXIOMS_AND_TYPES.log').write_text(result.stdout+result.stderr)
require(result.returncode==0,'Axiom/type query failed')
closures={}
for name,values in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",result.stdout,re.S):
    closures[name]=[x.strip() for x in values.replace('\n',' ').split(',') if x.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",result.stdout):closures[name]=[]
require(set(closures)==set(queries),'Axiom query set mismatch')
allowed={'propext','Classical.choice','Quot.sound'}
for name,values in closures.items():require(set(values)<=allowed,'Unexpected axiom '+name+': '+repr(values))
negatives=[]
negdir=SRC/'negative-controls';negdir.mkdir()
for file in sorted((R/'negative-controls').glob('*.lean')):
    target=negdir/file.name;shutil.copyfile(file,target)
    result=subprocess.run([str(LEAN),'--trust=0','--root='+str(SRC),str(target)],env=env,cwd=R,capture_output=True,text=True)
    text=result.stdout+result.stderr;(LOG/(file.stem+'.negative.log')).write_text(text)
    require(result.returncode!=0,'False proposition accepted: '+file.name)
    require('evaluated to false' in text or 'is false' in text,'Negative failed for wrong reason: '+file.name+'\n'+text)
    require('unknown' not in text.lower() and 'object file' not in text.lower(),'Negative import/name failure: '+file.name)
    negatives.append({'file':file.name,'source_sha256':sha(file),'exit_code':result.returncode,'log':str(LOG/(file.stem+'.negative.log'))})
for m in MODULES:require(sha(R/(m+'.lean'))==pins[m],'Author source changed during replay: '+m)
receipt={'status':'PASS','started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'run_directory':str(RUN),'modules':records,'theorem_count':len(queries),'axiom_closures':closures,'negative_controls':negatives,'prerequisite_receipt_sha256':sha(R/'PREREQUISITE_REBUILD.json'),'python_source_sha256':sha(R/'inputs/prcodec.py'),'scope':'Kernel proofs about source-lowered typed AST final-output and pointwise streams. Python transcription bridge ordinary; no Python-byte serialization identity, Set-event kernel trace, or kernel measure law.'}
(RUN/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
(R/'FINAL_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','run_directory':str(RUN),'modules':len(records),'theorems':len(queries),'negative_controls':len(negatives)},indent=2))
