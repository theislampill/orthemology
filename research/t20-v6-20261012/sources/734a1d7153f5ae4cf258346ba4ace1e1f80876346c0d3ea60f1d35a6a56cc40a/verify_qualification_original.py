#!/usr/bin/env python3
"""Fresh custom-dependency rebuild. Only official pinned Mathlib caches are reused."""
import argparse, pathlib, os, re, json, hashlib, subprocess, datetime, shutil, sys, time
p=argparse.ArgumentParser()
p.add_argument('--p02-root',type=pathlib.Path,required=True)
p.add_argument('--measure-root',type=pathlib.Path,required=True)
p.add_argument('--mathlib-root',type=pathlib.Path,required=True)
p.add_argument('--lean-bin',type=pathlib.Path,required=True)
a=p.parse_args(); root=pathlib.Path(__file__).resolve().parent
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'); out=root/'receipts'/stamp; src=out/'sources';lib=out/'lib';src.mkdir(parents=True);lib.mkdir()
sha=lambda x:hashlib.sha256(pathlib.Path(x).read_bytes()).hexdigest()
roots=[root.resolve(),a.measure_root.resolve(),a.p02_root.resolve(),pathlib.Path('private-locator:1dc07ecc133a6053717a')]
entries=['HeavyCylinders','RationalNormalForm','NumericMembership']; official={'Mathlib','Batteries','Aesop','Qq','ProofWidgets','LeanSearchClient','ImportGraph','Plausible','Cli','Lean','Init','Std'}
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
math=a.mathlib_root.resolve();paths=[lib,math/'.lake/build/lib/lean']+[x/'.lake/build/lib/lean' for x in sorted((math/'.lake/packages').iterdir()) if (x/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'PATH':str(a.lean_bin.resolve())+':'+os.environ['PATH'],'LEAN_PATH':':'.join(map(str,paths))};env.pop('LEAN_NUM_THREADS',None)
version=subprocess.check_output(['lean','--version'],env=env,text=True).strip()
assert version=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)',version
pin=subprocess.check_output(['git','-C',str(math),'rev-parse','HEAD'],text=True).strip();assert pin=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
result={'scope':'Actual hard-threshold cylinder mass formula and executable natural-number normal form; uniform Computable certificate and hierarchy library theorem separate','status':'RUNNING','lean':version,'mathlib':pin,'entries':entries,'sources':mods,'order':order,'builds':[]}
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
print(json.dumps({'status':result['status'],'modules':len(order),'targets':len(result.get('targets',[])),'receipt':str(out/'RESULT.json'),'sha256':sha(out/'RESULT.json')}),flush=True)
sys.exit(0 if result['status']=='PASS' else 1)
