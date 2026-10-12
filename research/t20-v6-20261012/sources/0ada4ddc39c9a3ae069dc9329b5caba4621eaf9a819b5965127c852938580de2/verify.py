#!/usr/bin/env python3
"""Fresh custom-dependency rebuild. Only official pinned Mathlib caches are reused."""
import argparse, pathlib, os, re, json, hashlib, subprocess, datetime, shutil, sys, time
p=argparse.ArgumentParser()
p.add_argument('--p02-root',type=pathlib.Path,required=True)
p.add_argument('--measure-root',type=pathlib.Path,required=True)
p.add_argument('--tagged-root',type=pathlib.Path,required=True)
p.add_argument('--bridge-root',type=pathlib.Path,required=True)
p.add_argument('--seal',type=pathlib.Path,required=True)
p.add_argument('--mathlib-root',type=pathlib.Path,required=True)
p.add_argument('--lean-bin',type=pathlib.Path,required=True)
a=p.parse_args(); root=pathlib.Path(__file__).resolve().parent
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'); out=root/'receipts'/stamp; src=out/'sources';lib=out/'lib';src.mkdir(parents=True);lib.mkdir()
sha=lambda x:hashlib.sha256(pathlib.Path(x).read_bytes()).hexdigest()
roots=[root.resolve(),a.bridge_root.resolve(),a.measure_root.resolve(),a.tagged_root.resolve(),a.p02_root.resolve(),a.p02_root.resolve()/'Predecessor']
entries=['HeavyCylinders','RationalNormalForm','FiniteOutputTable','FixedIndexPrimrec','FiniteTableWitnesses','NumericMembership']; official={'Mathlib','Batteries','Aesop','Qq','ProofWidgets','LeanSearchClient','ImportGraph','Plausible','Cli','Lean','Init','Std'}
mods={}; order=[]; active=set()
def visit(m):
 if m.split('.')[0] in official:return
 if m in active:raise RuntimeError('Cyclic dependency '+m)
 if m in mods:return
 hits=[r/(m.replace('.','/')+'.lean') for r in roots if (r/(m.replace('.','/')+'.lean')).is_file()]
 if not hits:raise RuntimeError('Missing custom source '+m)
 if len({sha(x) for x in hits})!=1:raise RuntimeError('Conflicting custom source '+m)
 origin=hits[0];dst=src/(m.replace('.','/')+'.lean');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(origin,dst)
 active.add(m)
 for line in dst.read_text().splitlines():
  if line.startswith('import '):
   for dep in line[7:].split():visit(dep)
 active.remove(m);mods[m]={'origin':str(origin),'sha256':sha(dst)};order.append(m)
for m in entries:visit(m)
seal=json.loads(a.seal.read_text())
shutil.copy2(a.seal,out/'AUTHOR_SEAL.json')
seal_hash=sha(a.seal)
# Accept either a source list closure or a simple mapping while retaining exact hash binding.
expected={}
def collect_seal(v):
 if isinstance(v,dict):
  if 'module' in v and 'sha256' in v:expected[v['module']]=v['sha256']
  if 'source_sha256' in v and isinstance(v['source_sha256'],dict):expected.update(v['source_sha256'])
  for z in v.values():collect_seal(z)
 elif isinstance(v,list):
  for z in v:collect_seal(z)
collect_seal(seal)
if not expected:raise RuntimeError('No source hashes in author seal')
for m,h in expected.items():
 if m in mods and mods[m]['sha256']!=h:raise RuntimeError('Seal mismatch '+m)
if not set(entries)<=set(expected):raise RuntimeError('Author seal does not bind every entry '+str(set(entries)-set(expected)))

math=a.mathlib_root.resolve();paths=[lib,math/'.lake/build/lib/lean']+[x/'.lake/build/lib/lean' for x in sorted((math/'.lake/packages').iterdir()) if (x/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'PATH':str(a.lean_bin.resolve())+':'+os.environ['PATH'],'LEAN_PATH':':'.join(map(str,paths))};env.pop('LEAN_NUM_THREADS',None)
version=subprocess.check_output(['lean','--version'],env=env,text=True).strip()
assert version=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)',version
pin=subprocess.check_output(['git','-C',str(math),'rev-parse','HEAD'],text=True).strip();assert pin=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
result={'scope':'Independent sealed-source fresh replay of actual Cantor atomic mass hard-threshold normal form, exact numeric finite cylinder table, and executable rational membership bridge; no Mathlib Computable or formal hierarchy certificate claim','status':'RUNNING','lean':version,'mathlib':pin,'entries':entries,'sources':mods,'order':order,'builds':[],'author_seal_sha256':seal_hash,'author_seal_sources_checked':sorted(set(mods)&set(expected))}
(out/'MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
for m in order:
 f=src/(m.replace('.','/')+'.lean');o=lib/(m.replace('.','/')+'.olean');o.parent.mkdir(parents=True,exist_ok=True)
 cmd=['lean','-j1','--root='+str(src),'-o',str(o),str(f)];t=time.monotonic()
 r=subprocess.run(cmd,cwd=src,env=env,text=True,capture_output=True,timeout=300)
 (out/(m+'.log')).write_text(r.stdout+r.stderr);rec={'module':m,'exit':r.returncode,'seconds':time.monotonic()-t,'command':cmd};result['builds'].append(rec)
 print(json.dumps(rec),flush=True)
 if r.returncode:result['status']='BUILD_FAILED';break
else:
 names=[]
 for m in entries:
  blocks=[]
  for line in (src/(m+'.lean')).read_text().splitlines():
   x=re.match(r'^(namespace|section)(?:\s+([\w.]+))?',line)
   if x:blocks.append((x.group(1),x.group(2) or ''))
   elif re.match(r'^end(?:\s|$)',line):
    if blocks:blocks.pop()
   else:
    x=re.match(r"^(?:theorem|lemma)\s+([\w']+)",line)
    if x:names.append('.'.join([n for k,n in blocks if k=='namespace']+[x.group(1)]))
 audit='\n'.join('import '+m for m in entries)+'\nset_option pp.universes true\n'+'\n'.join('#check @'+n+'\n#print axioms '+n for n in names)+'\n';(src/'Audit.lean').write_text(audit)
 r=subprocess.run(['lean','-j1','--root='+str(src),'-o',str(lib/'Audit.olean'),str(src/'Audit.lean')],cwd=src,env=env,text=True,capture_output=True,timeout=300);txt=r.stdout+r.stderr;(out/'Audit.log').write_text(txt)
 ax={n:[v.strip() for v in vs.split(',') if v.strip()] for n,vs in re.findall(r"'(.*)' depends on axioms:\s*\[([^\]]*)\]",txt)}
 ax.update({n:[] for n in re.findall(r"'(.*)' does not depend on any axioms",txt)})
 result.update(targets=names,axioms=ax,audit_exit=r.returncode)
 result['status']='PASS' if r.returncode==0 and set(names)==set(ax) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values()) else 'AUDIT_FAILED'
result['origins_unchanged']=all(sha(v['origin'])==v['sha256'] for v in mods.values())
if not result['origins_unchanged']:result['status']='SOURCE_CHANGED'
result['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'LATEST_REPLAY.txt').write_text(str(out/'RESULT.json')+'\n')
print(json.dumps({'status':result['status'],'modules':len(order),'targets':len(result.get('targets',[])),'receipt':str(out/'RESULT.json'),'sha256':sha(out/'RESULT.json')}),flush=True)
sys.exit(0 if result['status']=='PASS' else 1)
