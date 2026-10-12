#!/usr/bin/env python3
"""Replay new modules only; never rebuild retained baseline or third-party libraries."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,tempfile
root=Path(__file__).resolve().parent
w=root.parent
lean=w/'.toolchains/lean-4.19.0-linux/bin/lean'
mods=['GenericFoldTransport','SourceFoldContract','SourceFoldApplication','NaturalityBoundary','RecursorUniqueness','InternalRecursorPrinciple','SourceRigidity','RigidityDiscriminator']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=root/'DISCRIMINATOR_INPUT_HASHES.json'
paths=(root/'lean_path.txt').read_text().strip().split(':')[1:]
if not pins.exists():
 records={str(root/(m+'.lean')):sha(root/(m+'.lean')) for m in mods}
 for d in paths:
  if '/.lake/packages/' not in d:
   for p in Path(d).glob('*.olean'):records[str(p)]=sha(p)
 records[str(lean)]=sha(lean)
 pins.write_text(json.dumps(records,indent=2)+'\n')
records=json.loads(pins.read_text())
def verify():
 for p,h in records.items():
  if sha(Path(p))!=h:raise RuntimeError('Pinned input changed: '+p)
verify()
out=Path(tempfile.mkdtemp(prefix='fresh-discriminator-',dir=root/'validation'))
env=os.environ|{'LEAN_PATH':':'.join([str(out)]+paths)}
receipt={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RUNNING','scope':'Eight new modules replayed with trust=0; retained compiled ancestry reused, not rebuilt.','output':str(out),'lean_path':env['LEAN_PATH'],'input_manifest_sha256':sha(pins),'pinned_inputs':len(records),'modules':[]}
allow={'propext','Classical.choice','Quot.sound'}
for m in mods:
 p=root/(m+'.lean');o=out/(m+'.olean');log=out/(m+'.log')
 r=subprocess.run([str(lean),'--trust=0','-o',str(o),str(p)],env=env,capture_output=True,text=True)
 content=r.stdout+r.stderr;log.write_text(content)
 axioms=set(a.strip() for group in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',content) for a in group.split(','))
 row={'module':m,'exit_code':r.returncode,'source_sha256':sha(p),'log_sha256':sha(log),'axioms':sorted(axioms),'unexpected_axioms':sorted(axioms-allow)}
 if o.exists():row['olean_sha256']=sha(o)
 receipt['modules'].append(row)
 print(m,r.returncode,flush=True)
 if r.returncode or axioms-allow:
  receipt['status']='FAIL';(root/'DISCRIMINATOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(content);raise SystemExit(1)
verify()
receipt['status']='PASS';receipt['inputs_unchanged']=True
(root/'DISCRIMINATOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS all eight modules, pinned inputs unchanged',flush=True)
