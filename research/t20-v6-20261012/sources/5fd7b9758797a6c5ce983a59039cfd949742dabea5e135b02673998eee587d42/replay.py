#!/usr/bin/env python3
"""Portable custody check and fresh Python replay. Never replays Lean."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile,os
R=Path(__file__).resolve().parent
manifest=json.loads((R/'MANIFEST.json').read_text())
for rel,rec in manifest['files'].items():
 p=R/rel
 if not p.is_file() or len(p.read_bytes())!=rec['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=rec['sha256']:raise RuntimeError('Integrity failure: '+rel)
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()}
if actual!=set(manifest['files'])|{'MANIFEST.json'}:raise RuntimeError('Unsealed or missing files')
out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=False)
records=[]
with tempfile.TemporaryDirectory(prefix='additive-portable-') as td:
 w=Path(td);shutil.copytree(R/'payload',w,dirs_exist_ok=True)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('LEAN_PATH',None)
 def run(label,args,cwd):
  p=subprocess.run([sys.executable,*args],cwd=cwd,env=env,text=True,capture_output=True)
  (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
  records.append({'label':label,'args':args,'cwd_relative':str(cwd.relative_to(w)),'returncode':p.returncode})
  if p.returncode:raise RuntimeError(label+' failed; see '+str(out))
 if manifest['kind']=='rational':
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   for label,rel in [('author','hase-rational-kernel-transport-20261011/test_transport.py'),('review-author','rational-kernel-independent-review-20261011/test_transport.py'),('independent','rational-kernel-independent-review-20261011/independent_probability.py'),('root','rational-kernel-root-control-20261011/check.py'),('root-fibres','rational-kernel-root-control-20261011/fibre_mass_check.py')]:
    p=w/rel;run(label+'-'+mode,flags+[p.name],p.parent)
 else:
  received=w/'received-authorial-synthesis-20261011';z=next(received.glob('*.zip'));ext=received/'extracted'
  with zipfile.ZipFile(z) as f:
   if f.testzip():raise RuntimeError('Input CRC failed')
   for info in f.infolist():
    p=Path(info.filename)
    if p.is_absolute() or '..' in p.parts:raise RuntimeError('Unsafe input member')
   f.extractall(ext)
  source=ext/'Orthemology_T20_111min_Recovered_Authored_Work_20261010'
  corrected=w/'authorial-synthesis-root-review-20261011/corrected-reference'
  overlay=w/'correction-overlay';shutil.copytree(corrected,overlay);shutil.copytree(source,corrected,dirs_exist_ok=True);shutil.copytree(overlay,corrected,dirs_exist_ok=True)
  run('source-manifest',['verify_packet.py'],source)
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   run('source-52-'+mode,flags+['-m','unittest','discover','-s','tests','-v'],source)
   run('corrected-55-'+mode,flags+['-m','unittest','discover','-s','tests','-v'],corrected)
   p=w/'audit-tail-positive-repair-20261011';run('tail-10-'+mode,flags+['check.py'],p)
  # Reviewer controls contain assert statements: normal mode is authoritative.
  p=w/'authorial-audit-flow-review-20261011';run('review-exact-controls',['independent_controls.py'],p)
receipt={'status':'PASS','kind':manifest['kind'],'sealed_files':len(manifest['files']),'python':sys.version,'runs':records,'scope':'Fresh portable Python only. Recorded Lean receipts are custody, not fresh kernel replay. No fresh Arabic-source research or all-T20 consolidation.'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
