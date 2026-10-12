#!/usr/bin/env python3
"""Read-only independent compiler import parsing; never builds objects."""
from pathlib import Path
from collections import deque, Counter
import os, subprocess, json, hashlib, datetime
A=Path(__file__).resolve().parent.parent; W=A.parents[1]
D=A/'dependencies'; P=A/'immutable-extraction/Sixteenth_Orthemology_Proof_Source_Recovered_v1'
T=W/'recovery-20261005-1330/environment/toolchain/lean-4.19.0-linux'; R=A/'independent-review'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((P/'lean/lake-manifest.json').read_text())['packages']
package_sources=sorted(p for p in P.rglob('*.lean') if p.name!='lakefile.lean')
localdirs=sorted(set(p.parent for p in package_sources))
env=dict(os.environ)
for k in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LEAN_HOME','LAKE_HOME','ELAN_TOOLCHAIN','LD_PRELOAD','LD_LIBRARY_PATH']:
 env.pop(k,None)
env['LEAN_PATH']=''; env['LEAN_NUM_THREADS']='1'
base=[P/'lean',*localdirs,*[D/p['name'] for p in pins]]
def imports(p,local=False):
 env['LEAN_SRC_PATH']=':'.join(map(str,([p.parent] if local else [])+base))
 r=subprocess.run([str(T/'bin/lean'),'--src-deps',str(p)],env=env,cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
 if r.returncode:raise RuntimeError((str(p),r.stdout,r.stderr))
 result=[Path(x).resolve() for x in r.stdout.splitlines()]
 if not all(x.is_file() for x in result):raise RuntimeError((str(p),r.stdout))
 return result
project=[];external=set()
for p in package_sources:
 imps=imports(p,True)
 for i in imps:
  if i.is_relative_to(D):external.add(i)
  elif not (i.is_relative_to(P) or i.is_relative_to(T/'src/lean')):raise RuntimeError(('escape',str(i)))
 project.append({'path':str(p.relative_to(P)),'sha256':digest(p),'imports':[str(i) for i in imps]})
print('PACKAGE_IMPORTS_PARSED',len(project),'DIRECT_THIRD_PARTY_ROOTS',len(external),flush=True)
queue=deque(sorted(external)); seen={}
while queue:
 p=queue.popleft()
 if p in seen:continue
 imps=imports(p)
 if p.is_relative_to(D):
  rel=p.relative_to(D);kind='third_party';package=rel.parts[0];source=Path(*rel.parts[1:]).as_posix()
 elif p.is_relative_to(T/'src/lean'):
  kind='trusted_toolchain';package='official_toolchain';source=p.relative_to(T/'src/lean').as_posix()
 else:raise RuntimeError(('closure escape',str(p)))
 seen[p]={'kind':kind,'package':package,'module':source[:-5].replace('/','.'),'source_path':source,'source_sha256':digest(p),'imports':[str(i) for i in imps]};queue.extend(imps)
 if len(seen)%500==0:print('RECURSIVE_IMPORTS_PARSED',len(seen),flush=True)
third=sorted((r for r in seen.values() if r['kind']=='third_party'),key=lambda r:(r['package'],r['module']))
original=json.loads((P/'DEPENDENCY_CLOSURE.json').read_text())
keys=lambda rows:{(r['package'],r['module'],r['source_path'],r['source_sha256']) for r in rows}
missing=keys(original['recorded_source_modules'])-keys(third);extra=keys(third)-keys(original['recorded_source_modules'])
assert not missing and not extra,(missing,extra)
roots=sorted(p.relative_to(D).parts[1:] for p in external)
rootmodules=sorted('/'.join(r)[:-5].replace('/','.') for r in roots)
assert rootmodules==sorted(original['roots']),(rootmodules,original['roots'])
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Independent official compiler --src-deps scan of every distributed non-lakefile Lean source followed by recursive third-party closure. No object compilation.','package_lean_sources':len(project),'direct_third_party_roots':rootmodules,'third_party_count':len(third),'third_party_by_package':dict(Counter(r['package'] for r in third)),'trusted_toolchain_source_count':sum(r['kind']=='trusted_toolchain' for r in seen.values()),'exact_matches_immutable_manifest':True,'archive_manifest_sha256':digest(P/'DEPENDENCY_CLOSURE.json'),'project_imports':project,'third_party':third}
(R/'INDEPENDENT_SOURCE_CLOSURE.json').write_text(json.dumps(out,indent=2)+'\n')
print('INDEPENDENT_SOURCE_CLOSURE_PASS',len(third),flush=True)
