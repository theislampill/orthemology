from pathlib import Path
import os, json, re, hashlib, subprocess, datetime, sys, zipfile
ROOT=Path(__file__).resolve().parent
LEAN=Path('private-locator:4211d241978f643cb623')
MATH=Path('private-locator:41bd9f979012c8bbc235')
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
NOW=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
mode=sys.argv[1]; W=ROOT/mode
W.mkdir(); S=W/'sources'; B=W/'lib'; E=W/'evidence'
for d in [S,B,E]:d.mkdir()
rec={'started_utc':NOW(),'status':'RUNNING','mode':mode,'compiler_sha256':H(LEAN),'sources':{},'builds':[],'axioms':{},'canonical_adoption':False,'scope':'independent shadow rebuild; cached pinned Mathlib only'}
def save(): (W/'RESULT.json').write_text(json.dumps(rec,indent=2)+'\n')
def cmd(label,args,env=None):
 p=subprocess.run(args,cwd=S,env=env,capture_output=True,timeout=600)
 (E/(label+'.stdout')).write_bytes(p.stdout);(E/(label+'.stderr')).write_bytes(p.stderr)
 rec['builds'].append({'label':label,'argv':args,'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()});save()
 if p.returncode or re.search(rb'error:|sorryAx|declaration uses',p.stdout+p.stderr): raise Exception(label+' build failed')
 return p.stdout.decode()
try:
 rec['compiler']=cmd('version',[str(LEAN),'--version']).strip()
 assert 'version 4.19.0' in rec['compiler'] and '6caaee842e94' in rec['compiler']
 rec['mathlib_commit']=subprocess.check_output(['git','-C',str(MATH),'rev-parse','HEAD'],text=True).strip()
 assert rec['mathlib_commit']=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
 rec['mathlib_tracked_status']=subprocess.check_output(['git','-C',str(MATH),'status','--porcelain','--untracked-files=no'],text=True)
 assert not rec['mathlib_tracked_status']
 rec['canonical_commit']=subprocess.check_output(['git','-C','private-locator:36fb2027a2cd56fb6b89','rev-parse','HEAD'],text=True).strip()
 assert rec['canonical_commit']=='03e2604dfcef278b01c60d19b05370fcec4194b6'
 if mode=='p01':
  parent=Path('private-locator:f27ed1fe8acaf6f42e17'); receipt=Path('private-locator:bd9cd8ea0c43f76b60a5'); j=json.loads(receipt.read_text())
  roots=[receipt.parent,parent]; main=[Path(x).stem for x in j['sources']]; names=list(j['declarations'])
  rec['claimed_receipt_sha256']=H(receipt)
 elif mode=='p03':
  z=Path('private-locator:03f9af4865fe56e9da63');rec['sealed_zip_sha256']=H(z);assert H(z)=='42205fffc4dddfc239d916f1255c4861b530e66a44242cbb50f3c942ab4741dc'
  with zipfile.ZipFile(z) as f:
   rows=[n for n in f.namelist() if n.endswith('.lean') and '/constructor-square/' in '/'+n and n.count('/')<=2]
   rec['archive_direct_lean_members']=rows
  base=Path('private-locator:ef374410ecf29a97d371'); roots=[base/'constructor-square',base/'python-bases/source/lean']
  receipt=base/'constructor-square/fresh-build-final/RECEIPT.json';j=json.loads(receipt.read_text()); main=[Path(x).stem for x in j['source_files']];names=list(j['targets']);rec['claimed_receipt_sha256']=H(receipt)
 else:
  receipt=Path('private-locator:29618d3b6292228b78a6');j=json.loads(receipt.read_text());roots=[receipt.parent/'sources',Path('private-locator:6e1cdd2685640ba2eef0')]; main=[x['name'] for x in j['modules']];names=j['target_names'];rec['claimed_receipt_sha256']=H(receipt)
 rec['main_modules']=main; rec['audit_names']=names
 order=[]; visiting=set();seen=set()
 def locate(m):
  for r in roots:
   p=r/(m.replace('.','/')+'.lean')
   if p.exists():return p
  return None
 def visit(m):
  if m in seen:return
  assert m not in visiting,'import cycle'
  p=locate(m)
  if p is None:return
  visiting.add(m);txt=p.read_text()
  for line in txt.splitlines():
   if line.startswith('import '):
    for d in line[7:].split():visit(d)
  dest=S/(m.replace('.','/')+'.lean');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
  rec['sources'][m]={'origin':str(p),'sha256':H(p),'bytes':p.stat().st_size}
  visiting.remove(m);seen.add(m);order.append(m)
 for m in main:visit(m)
 assert all(m in seen for m in main)
 paths=[B,MATH/'.lake/build/lib/lean']+[d/'.lake/build/lib/lean' for d in (MATH/'.lake/packages').iterdir() if d.is_dir()]
 env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,paths));env.pop('LEAN_SYSROOT',None);rec['lean_path']=env['LEAN_PATH'];save()
 for m in order:
  op=B/(m.replace('.','/')+'.olean');op.parent.mkdir(parents=True,exist_ok=True)
  print(mode,m,flush=True)
  cmd(m.replace('.','_'),[str(LEAN),'-j1','--root='+str(S),'-o',str(op),str(S/(m.replace('.','/')+'.lean'))],env)
  rec['sources'][m]['fresh_olean_sha256']=H(op);save()
 audit='\n'.join('import '+m for m in main)+'\nset_option pp.universes true\nset_option pp.explicit true\nset_option format.width 180\n'+''.join('#check @'+n+'\n#print axioms '+n+'\n' for n in names)
 (S/'IndependentAudit.lean').write_text(audit)
 output=cmd('IndependentAudit',[str(LEAN),'-j1','-o',str(B/'IndependentAudit.olean'),'IndependentAudit.lean'],env)
 hits=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output);empty=re.findall(r"'([^']+)' does not depend on any axioms",output)
 ax={n:[a.strip() for a in vals.split(',') if a.strip()] for n,vals in hits};ax.update({n:[] for n in empty})
 assert set(ax)==set(names);assert all(set(a)<={'propext','Quot.sound','Classical.choice'} for a in ax.values())
 for m,row in rec['sources'].items(): assert H(row['origin'])==row['sha256']==H(S/(m.replace('.','/')+'.lean'))
 rec['axioms']=ax;rec['status']='FRESH_INDEPENDENT_BUILD_AND_AXIOM_READBACK_PASS';rec['finished_utc']=NOW();save();print(rec['status'],len(order),len(names),flush=True)
except BaseException as ex:
 rec['status']='FAIL';rec['error']=repr(ex);rec['finished_utc']=NOW();save();raise
