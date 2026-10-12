#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile,datetime
root=Path(__file__).resolve().parent;main=root.parent;w=main.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt0=json.loads((main/'REPLAY.json').read_text());assert receipt0['status']=='PASS'
base=main/receipt0['output_directory']
receipt1=json.loads((main/'identity-delta/REPLAY.json').read_text());assert receipt1['status']=='PASS'
identity=main/'identity-delta'/receipt1['output_directory']
for rr,bd in [(receipt0,base),(receipt1,identity)]:
 for m in rr['modules']:assert sha(bd/(m['module']+'.olean'))==m['object_sha256']
for rs in json.loads((main/'INPUT_HASHES.json').read_text()).values():
 for r in rs:assert sha(w/r['path'])==r['sha256']
pins=[('homogeneous-per-root-20261010/inherited/UnaryCertificateSyntax.lean','5f80f464475cb12a6ad90fc89c3540912322f31470be86e26072a990222115c4'),('homogeneous-per-root-20261010/CertificateSeparation.lean','0d1981d8d8a5d0c95e4649cd910698cba9410d71e63650df7eb118c125ef135c')]
for path,h in pins:
 assert sha(w/path)==h;assert sha(root/'sources'/Path(path).name)==h
out=Path(tempfile.mkdtemp(prefix='fresh-',dir=root))
libs=[out,identity,base,w/'hase-full-per-extension-20261010/validation',w/'hase-imported-compiler-transport-20261010/validation/replay-bxNUv6']
libs+=sorted((w/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env=os.environ|{'LEAN_PATH':':'.join(map(str,libs))}
lean=w/'.toolchains/lean-4.19.0-linux/bin/lean'
receipt=dict(status='RUNNING',scope='Fresh added inherited certificate grammar, new separation theorem, and reviewer controls; retained 83-module baseline not rebuilt.',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),output_directory=str(out.relative_to(root)),main_replay_sha256=sha(main/'REPLAY.json'),identity_replay_sha256=sha(main/'identity-delta/REPLAY.json'),modules=[])
for m in ['UnaryCertificateSyntax','CertificateSeparation','CertificateReviewControls']:
 src=root/'sources'/f'{m}.lean';obj=out/f'{m}.olean';log=out/f'{m}.log'
 r=subprocess.run([str(lean),'--trust=0','-o',str(obj),str(src)],env=env,text=True,capture_output=True)
 content=r.stdout+r.stderr;log.write_text(content)
 ax=set()
 for match in re.finditer(r'depends on axioms:\s*\[([^\]]*)\]',content):ax.update(a.strip() for a in match.group(1).split(',') if a.strip())
 assert ax<={'propext','Classical.choice','Quot.sound'}
 record=dict(module=m,source_sha256=sha(src),exit_code=r.returncode,trust_zero=True,axioms=sorted(ax),log_sha256=sha(log))
 if obj.exists():record['object_sha256']=sha(obj)
 receipt['modules'].append(record)
 print(m+': '+content,flush=True)
 if r.returncode:
  receipt['status']='FAIL';(root/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');raise SystemExit(1)
receipt['status']='PASS';(root/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
