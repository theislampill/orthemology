#!/usr/bin/env python3
"""Independent isolated rebuild: no author/custom olean is accepted as evidence."""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time
p=argparse.ArgumentParser()
p.add_argument('--source-root',type=pathlib.Path,action='append',required=True)
p.add_argument('--mathlib-root',type=pathlib.Path,required=True)
p.add_argument('--lean-bin',type=pathlib.Path,required=True)
p.add_argument('--entry',action='append',required=True)
p.add_argument('--author-seal',type=pathlib.Path)
a=p.parse_args(); root=pathlib.Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
out=root/'receipts'/stamp; src=out/'sources';lib=out/'lib'; src.mkdir(parents=True);lib.mkdir()
roots=[root.resolve()]+[p.resolve() for p in a.source_root]
official={'Mathlib','Batteries','Aesop','Qq','ProofWidgets','LeanSearchClient','ImportGraph','Plausible','Cli','Lean','Init','Std'}
mods={};order=[];active=set();external=set()
def imports(s):
 # Custom source imports are required to be plain one-line commands; comments removed.
 while re.search(r'/\-.*?\-/',s,re.S):s=re.sub(r'/\-.*?\-/','',s,flags=re.S)
 return [x for ln in s.splitlines() if ln.startswith('import ') for x in ln.split('--')[0][7:].split()]
def visit(m):
 if m.split('.')[0] in official:external.add(m);return
 if m in active:raise RuntimeError('Custom import cycle: '+m)
 if m in mods:return
 hits=[r/(m.replace('.','/')+'.lean') for r in roots if (r/(m.replace('.','/')+'.lean')).is_file()]
 if not hits:raise RuntimeError('Missing custom source: '+m)
 if len({sha(x) for x in hits})!=1:raise RuntimeError('Conflicting custom module: '+m)
 origin=hits[0]; dst=src/(m.replace('.','/')+'.lean');dst.parent.mkdir(parents=True,exist_ok=True)
 before=sha(origin);shutil.copy2(origin,dst)
 if before!=sha(dst) or before!=sha(origin):raise RuntimeError('Source changed during snapshot: '+m)
 deps=imports(dst.read_text());active.add(m)
 for dep in deps:visit(dep)
 active.remove(m);mods[m]={'origin':str(origin),'sha256':before,'imports':deps};order.append(m)
for m in a.entry:visit(m)
math=a.mathlib_root.resolve(); lean=a.lean_bin.resolve()/'lean'
paths=[lib,math/'.lake/build/lib/lean']+[x/'.lake/build/lib/lean' for x in sorted((math/'.lake/packages').iterdir()) if (x/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'PATH':str(a.lean_bin.resolve())+':'+os.environ['PATH'],'LEAN_PATH':':'.join(map(str,paths))}
env.pop('LEAN_NUM_THREADS',None)
version=subprocess.check_output([str(lean),'--version'],text=True).strip()
assert version=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)',version
pin=subprocess.check_output(['git','-C',str(math),'rev-parse','HEAD'],text=True).strip()
assert pin=='c44e0c8ee63ca166450922a373c7409c5d26b00b',pin
status=subprocess.check_output(['git','-C',str(math),'status','--porcelain','--untracked-files=no'],text=True)
assert status=='','Tracked Mathlib sources changed: '+status
dependencies=[]
for package in json.loads((math/'lake-manifest.json').read_text())['packages']:
 directory=math/'.lake/packages'/package['name']
 head=subprocess.check_output(['git','-C',str(directory),'rev-parse','HEAD'],text=True).strip()
 clean=subprocess.check_output(['git','-C',str(directory),'status','--porcelain','--untracked-files=no'],text=True)
 assert head==package['rev'],(package['name'],head,package['rev'])
 assert not clean,(package['name'],clean)
 dependencies.append({'name':package['name'],'rev':head,'tracked_sources_clean':True})
result={'status':'RUNNING','official_dependencies':dependencies,'lean':version,'lean_binary_sha256':sha(lean),'mathlib':pin,
 'custom_olean_reuse':False,'LEAN_PATH':[str(x) for x in paths],'entries':a.entry,
 'sources':mods,'order':order,'official_imports':sorted(external),'builds':[]}
if a.author_seal:
 seal=a.author_seal.resolve(); result['author_seal']={'path':str(seal),'sha256':sha(seal)}
 shutil.copy2(seal,out/'AUTHOR_SEAL.json')
(out/'MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
def run(m,timeout=600):
 f=src/(m.replace('.','/')+'.lean');o=lib/(m.replace('.','/')+'.olean');o.parent.mkdir(parents=True,exist_ok=True)
 cmd=[str(lean),'-j1','--root='+str(src),'-o',str(o),str(f)];t=time.monotonic()
 r=subprocess.run(cmd,cwd=src,env=env,text=True,capture_output=True,timeout=timeout)
 txt=r.stdout+r.stderr;(out/(m+'.log')).write_text(txt)
 rec={'module':m,'exit':r.returncode,'seconds':time.monotonic()-t,'command':cmd}
 if o.is_file():rec['olean_sha256']=sha(o)
 print(json.dumps(rec),flush=True);return rec,txt
try:
 for m in order:
  rec,txt=run(m);result['builds'].append(rec)
  if rec['exit']:result['status']='BUILD_FAILED';break
 else:
  # Read back ALL public declared names in every Uniform* source plus auditor controls.
  names=[]
  for m in order:
   if not (m.startswith(('Uniform','Membership','Matrix')) or m in {'NumericMembership','FiniteOutputTable'}):continue
   blocks=[]
   for ln in (src/(m.replace('.','/')+'.lean')).read_text().splitlines():
    x=re.match(r'^(namespace|section)(?:\s+([\w.]+))?',ln)
    if x:blocks.append((x.group(1),x.group(2) or ''));continue
    if re.match(r'^end(?:\s|$)',ln):
     if blocks:blocks.pop()
     continue
    x=re.match(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+)?(?:theorem|lemma|def|abbrev|instance|inductive|structure)\s+([\w']+)",ln)
    if x:names.append('.'.join([n for k,n in blocks if k=='namespace']+[x.group(1)]))
  names=list(dict.fromkeys(names))
  audit='\n'.join('import '+m for m in a.entry)+'\nset_option pp.universes true\nset_option pp.explicit true\nset_option pp.fullNames true\n'+''.join('#check @'+n+'\n#print axioms '+n+'\n' for n in names)
  (src/'FullTypesAxioms.lean').write_text(audit)
  rec,txt=run('FullTypesAxioms');result['audit_exit']=rec['exit'];result['targets']=names
  ax={n:[v.strip() for v in vs.split(',') if v.strip()] for n,vs in re.findall(r"'(.*)' depends on axioms:\s*\[([^\]]*)\]",txt)}
  ax.update({n:[] for n in re.findall(r"'(.*)' does not depend on any axioms",txt)})
  result['axioms']=ax; result['audit_source_sha256']=sha(src/'FullTypesAxioms.lean')
  result['status']='PASS' if rec['exit']==0 and set(names)==set(ax) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values()) else 'AUDIT_FAILED'
except subprocess.TimeoutExpired as e:
 result['status']='TIMEOUT';result['error']=str(e)
except Exception as e:
 result['status']='ERROR';result['error']=repr(e)
result['origins_unchanged']=all(sha(v['origin'])==v['sha256'] for v in mods.values())
if not result['origins_unchanged']:result['status']='SOURCE_CHANGED'
if a.author_seal:
 result['author_seal_unchanged']=sha(a.author_seal)==result['author_seal']['sha256']
 if not result['author_seal_unchanged']:result['status']='SEAL_CHANGED'
result['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'modules':len(order),'targets':len(result.get('targets',[])),'receipt':str(out/'RESULT.json'),'sha256':sha(out/'RESULT.json')}),flush=True)
sys.exit(0 if result['status']=='PASS' else 1)
