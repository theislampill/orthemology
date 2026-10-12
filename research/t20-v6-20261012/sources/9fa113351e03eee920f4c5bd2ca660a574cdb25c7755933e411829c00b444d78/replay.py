#!/usr/bin/env python3
"""Independent new-module-only replay; never rebuilds retained baseline objects."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess,tempfile
root=Path(__file__).resolve().parent
w=root.parent
lean=w/'.toolchains/lean-4.19.0-linux/bin/lean'
pins=json.loads((root/'INPUT_HASHES.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_pins():
 for records in pins.values():
  for r in records:
   p=w/r['path']
   assert sha(p)==r['sha256'],f'Changed pinned input: {p}'
 for r in pins['source_snapshots']:
  p=root/'sources'/Path(r['path']).name
  assert sha(p)==r['sha256'],f'Snapshot mismatch: {p}'
verify_pins()
modules=['CaseOperational','HomogeneousPER','ConcreteUniverse','GuardControls','SourceTransport','HenkinSoundness','DependencyAudit','LiteralCounterexample','OriginalWNoninhabitation','MixedPERControl','NoInternalNegation','ReviewControls']
out=Path(tempfile.mkdtemp(prefix='independent-',dir=root))
libs=[out,w/'hase-full-per-extension-20261010/validation',w/'hase-imported-compiler-transport-20261010/validation/replay-bxNUv6']
libs+=sorted((w/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
import os
env=os.environ|{'LEAN_PATH':':'.join(map(str,libs))}
version=subprocess.run([str(lean),'--version'],text=True,capture_output=True,check=True).stdout.strip()
receipt={'status':'RUNNING','scope':'Fresh trust-zero replay of 12 new modules only. Retained pinned source-theory and full-PER objects are reused, not rebuilt.','lean_version':version,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'output_directory':str(out.relative_to(root)),'lean_path':str(env['LEAN_PATH']),'baseline_objects_count':len(pins['pinned_baseline_objects']),'modules':[]}
allow={'propext','Classical.choice','Quot.sound'}
for m in modules:
 src=root/'sources'/f'{m}.lean';obj=out/f'{m}.olean';log=out/f'{m}.log'
 result=subprocess.run([str(lean),'--trust=0','-o',str(obj),str(src)],env=env,text=True,capture_output=True)
 content=result.stdout+result.stderr;log.write_text(content)
 axioms=[]
 for match in re.finditer(r'depends on axioms:\s*\[([^\]]*)\]',content):
  axioms += [a.strip() for a in match.group(1).split(',') if a.strip()]
 unexpected=sorted(set(axioms)-allow)
 row=dict(module=m,source_sha256=sha(src),exit_code=result.returncode,trust_zero=True,axioms=sorted(set(axioms)),unexpected_axioms=unexpected,log_sha256=sha(log))
 if obj.exists():row['object_sha256']=sha(obj)
 receipt['modules'].append(row)
 print(m, 'PASS' if not result.returncode and not unexpected else 'FAIL',flush=True)
 if result.returncode or unexpected:
  receipt['status']='FAIL';(root/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
  print(content);raise SystemExit(1)
verify_pins()
receipt['status']='PASS';receipt['all_initial_input_hashes_unchanged']=True
receipt['standard_axioms_only']=True
(root/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: all 12 modules; initial source/baseline hashes unchanged.',flush=True)
