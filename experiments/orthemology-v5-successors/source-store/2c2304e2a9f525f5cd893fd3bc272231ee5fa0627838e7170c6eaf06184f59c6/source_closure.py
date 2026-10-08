from pathlib import Path
import json,subprocess,os,hashlib,collections,datetime
from context import context, isolated_environment
A,D,P,T,E=context();L=T/'bin/lean'
manifest=json.loads((P/'DEPENDENCY_CLOSURE.json').read_text());pins=json.loads((P/'lean/lake-manifest.json').read_text())['packages'];env=isolated_environment(A);env['LEAN_SRC_PATH']=':'.join(str(D/p['name']) for p in pins);env['LEAN_PATH']=''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lookup={}
for p in pins:
 for f in (D/p['name']).rglob('*.lean'):
  if '.lake' not in f.relative_to(D/p['name']).parts:lookup[f.relative_to(D/p['name']).with_suffix('').as_posix().replace('/','.')]=(p['name'],f)
seen={};todo=[lookup[r][1] for r in manifest['roots']];outs=[]
while todo:
 f=todo.pop().resolve()
 if str(f) in seen:continue
 r=subprocess.run([str(L),'--src-deps',str(f)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
 assert r.returncode==0,(f,r.stdout)
 imports=[Path(x).resolve() for x in r.stdout.splitlines() if x.strip()]
 assert all(i.is_file() for i in imports),(f,r.stdout)
 if f.is_relative_to(D):
  rel=f.relative_to(D);package=rel.parts[0];source='/'.join(rel.parts[1:]);module=source[:-5].replace('/','.');kind='third_party'
 else:
  assert f.is_relative_to(T/'src/lean'),f
  source=f.relative_to(T/'src/lean').as_posix();module=source[:-5].replace('/','.');package='official_toolchain';kind='trusted_toolchain'
 row={'kind':kind,'package':package,'module':module,'source_path':source,'source_sha256':sha(f),'direct_import_source_paths':[str(i) for i in imports]}
 if kind=='trusted_toolchain':
  obj=T/'lib/lean'/(module.replace('.','/')+'.olean');assert obj.is_file(),obj;row.update(object_path=str(obj),trusted_object_sha256=sha(obj))
 seen[str(f)]=row;todo.extend(imports)
 if len(seen)%200==0:print('SOURCE_IMPORTS_PARSED',len(seen),flush=True)
third=sorted([r for r in seen.values() if r['kind']=='third_party'],key=lambda r:(r['package'],r['module']));trusted=sorted([r for r in seen.values() if r['kind']=='trusted_toolchain'],key=lambda r:r['module']);expected={(r['package'],r['module'],r['source_path'],r['source_sha256']) for r in manifest['recorded_source_modules']};actual={(r['package'],r['module'],r['source_path'],r['source_sha256']) for r in third};assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
(A/'evidence/COMPILER_PARSED_SOURCE_CLOSURE.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Official Lean 4.19 --src-deps recursively, on isolated clean sources with empty LEAN_PATH','roots':manifest['roots'],'third_party_modules':len(third),'toolchain_modules':len(trusted),'third_party_counts':dict(collections.Counter(r['package'] for r in third)),'exactly_equals_packaged_source_closure':True,'third_party':third,'trusted_toolchain':trusted},indent=2)+'\n')
print('SOURCE_CLOSURE_PASS',len(third),len(trusted))
