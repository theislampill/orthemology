#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile,datetime
root=Path(__file__).resolve().parent; main=root.parent;w=main.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
main_receipt=json.loads((main/'REPLAY.json').read_text());assert main_receipt['status']=='PASS'
base=main/main_receipt['output_directory']
for m in main_receipt['modules']:
 assert sha(base/(m['module']+'.olean'))==m['object_sha256']
for rs in json.loads((main/'INPUT_HASHES.json').read_text()).values():
 for r in rs:assert sha(w/r['path'])==r['sha256']
source=w/'homogeneous-per-model-20261010/OriginalIdentityNoninhabitation.lean'
expected='5ee0cbdab27fa18866d5e7b1b6b13131bbdb649b5bacab839a67c46e11619d08'
assert sha(source)==expected;assert sha(root/'sources'/source.name)==expected
out=Path(tempfile.mkdtemp(prefix='fresh-',dir=root))
libs=[out,base,w/'hase-full-per-extension-20261010/validation',w/'hase-imported-compiler-transport-20261010/validation/replay-bxNUv6']
libs+=sorted((w/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env=os.environ|{'LEAN_PATH':':'.join(map(str,libs))}
lean=w/'.toolchains/lean-4.19.0-linux/bin/lean'
receipt=dict(status='RUNNING',scope='Two new identity modules freshly checked against pinned independent main-review and retained baseline objects.',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),output_directory=str(out.relative_to(root)),main_replay_sha256=sha(main/'REPLAY.json'),modules=[])
for m in ['OriginalIdentityNoninhabitation','IdentityReviewControls']:
 src=root/'sources'/f'{m}.lean';obj=out/f'{m}.olean';log=out/f'{m}.log'
 r=subprocess.run([str(lean),'--trust=0','-o',str(obj),str(src)],env=env,text=True,capture_output=True)
 content=r.stdout+r.stderr;log.write_text(content)
 ax=set()
 for match in re.finditer(r'depends on axioms:\s*\[([^\]]*)\]',content):ax.update(a.strip() for a in match.group(1).split(',') if a.strip())
 assert ax<={'propext','Classical.choice','Quot.sound'}
 record=dict(module=m,source_sha256=sha(src),exit_code=r.returncode,trust_zero=True,axioms=sorted(ax),log_sha256=sha(log))
 if obj.exists():record['object_sha256']=sha(obj)
 receipt['modules'].append(record)
 print(content)
 if r.returncode:
  receipt['status']='FAIL';(root/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');raise SystemExit(1)
receipt['status']='PASS';(root/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
