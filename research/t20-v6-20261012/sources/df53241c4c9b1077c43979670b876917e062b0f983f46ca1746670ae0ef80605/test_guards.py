#!/usr/bin/env python3
"""Mutation controls run only in disposable copies; no proof should run."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
sys.dont_write_bytecode=True
if not __debug__:raise SystemExit('Optimization is unsupported for guard tests.')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest-sha256',required=True);ap.add_argument('--lean-home',type=Path,required=True);ap.add_argument('--packages-dir',type=Path,required=True);ap.add_argument('--retained-root',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();O=a.output_dir.resolve()
need(not O.exists() and R!=O and R not in O.parents,'Guard output must be new and outside packet');O.mkdir(parents=True)
args=['--lean-home',str(a.lean_home.resolve()),'--packages-dir',str(a.packages_dir.resolve()),'--retained-root',str(a.retained_root.resolve())]
results=[]
def run(name,root=R,pin=None,extra=args,out=None,optimized=False,needle=None):
 target=out or O/(name+'-output');cmd=[sys.executable]+(['-O'] if optimized else [])+['-B',str(root/'replay.py'),'--expected-manifest-sha256',pin or a.expected_manifest_sha256]+extra+['--output-dir',str(target)]
 p=subprocess.run(cmd,cwd=O,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120);log=O/(name+'.log');log.write_text(p.stdout)
 need(p.returncode!=0,'Guard accepted '+name)
 if needle:need(needle in p.stdout,'Wrong rejection '+name+': '+p.stdout)
 receipt=target/'REPLAY_RECEIPT.json'
 if receipt.exists():need(json.loads(receipt.read_text())['runs']==[],'Proof ran in guard '+name)
 results.append({'control':name,'status':'EXPECTED_REJECTION','exit_status':p.returncode,'no_proof_compilation':True,'log_sha256':sha(log)})
def clone(name):
 p=O/name;shutil.copytree(R,p);return p
def repin(root,changed):
 p=root/'MANIFEST.json';m=json.loads(p.read_text())
 for r in m['files']:
  if r['path']==changed:r.update(bytes=(root/changed).stat().st_size,sha256=sha(root/changed))
 dump(p,m);return sha(p)
run('missing-prerequisite-roots',extra=[],needle='BLOCKED')
run('wrong-manifest-pin',pin='0'*64,needle='External manifest pin mismatch')
for mode in ['tamper','extra','missing','symlink']:
 r=clone('packet-'+mode);p=r/'README.md'
 if mode=='tamper':p.write_bytes(p.read_bytes()+b'\nTAMPER')
 if mode=='extra':(r/'UNLISTED').write_text('extra')
 if mode=='missing':p.unlink()
 if mode=='symlink':p.unlink();p.symlink_to(R/'README.md')
 run(mode,root=r,needle={'tamper':'Size mismatch','extra':'Exact packet inventory differs','missing':'Exact packet inventory differs','symlink':'Symlink in immutable packet'}[mode])
r=clone('wrong-external');name='prerequisites/RETAINED_PIN_BINDINGS.json';j=json.loads((r/name).read_text());j[4]['sha256']='0'*64;dump(r/name,j)
run('wrong-external-hash',root=r,pin=repin(r,name),needle='SHA-256 mismatch')
r=clone('unsafe-prerequisite');name='prerequisites/RETAINED_PIN_BINDINGS.json';j=json.loads((r/name).read_text());j[0]['path']='../escape';dump(r/name,j)
run('unsafe-prerequisite-path',root=r,pin=repin(r,name),needle='Unsafe relative path')
empty=O/'empty-retained';empty.mkdir()
run('missing-retained-files',extra=args[:-2]+['--retained-root',str(empty)],needle='Missing or symlink prerequisite')
r=clone('failed-review');name='evidence/hase-joint-induction-computation-independent-review-20261010/REVIEW_RECEIPT.json';j=json.loads((r/name).read_text());j['status']='FAIL';dump(r/name,j)
run('changed-review-verdict',root=r,pin=repin(r,name),needle='mismatch')
run('optimized-python',optimized=True,needle='Python optimization is unsupported')
stale=O/'stale-output';stale.mkdir();(stale/'sentinel').write_text('keep\n');run('reused-output',out=stale,needle='Output already exists');need((stale/'sentinel').read_text()=='keep\n','Stale sentinel changed')
r=clone('inside-packet');run('inside-packet-output',root=r,out=r/'forbidden',needle='separate from immutable packet');need(not (r/'forbidden').exists(),'Wrote inside packet')
p=a.lean_home.resolve()/'forbidden-joint-computation-output';need(not p.exists(),'Unexpected existing forbidden path');run('inside-toolchain-output',out=p,needle='Output overlaps external prerequisites');need(not p.exists(),'Wrote inside toolchain')
p=a.retained_root.resolve()/'hase-joint-induction-computation-20261010/forbidden-output';need(not p.exists(),'Unexpected forbidden original path');run('inside-original-output',out=p,needle='Output overlaps an original evidence directory');need(not p.exists(),'Wrote inside original')
dump(O/'GUARD_RESULTS.json',{'status':'PASS_FAIL_CLOSED_GUARDS','count':len(results),'controls':results,'scope':'Custody and wrapper guards, not mathematical negative proofs or a new independent review.'})
print('PASS_FAIL_CLOSED_GUARDS',len(results),flush=True)
