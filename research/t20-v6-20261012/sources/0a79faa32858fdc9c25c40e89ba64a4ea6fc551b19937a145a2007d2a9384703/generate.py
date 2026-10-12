from pathlib import Path
import sys,json,hashlib,subprocess,os,itertools,time
ROOT=Path('private-locator:b161f5e6ec5b32183f0f');BASE=ROOT/'python-bases/source';OUT=ROOT/'export-probes';sys.path.insert(0,str(BASE));sys.path.insert(0,str(ROOT/'shadow/proposal'))
import reference as r,proof_export as exp
from safe_frontend import export_module_owned
from boundaries import dump_json
# Distinct valid certs, generated independently from source syntax constructors.
V=('v',0); BOT=('bottom',);ID=('all',('arr',V,V));BOOL=('all',('arr',V,('arr',V,V)))
def i(A):return {'rule':'i','A':A}
def ai(p):return {'rule':'all_i','body':p}
def ae(p,A):return {'rule':'all_e','polymorphic':p,'type':A}
def ap(p,q):return {'rule':'app','function':p,'argument':q}
pid=ai(i(V));certs=[]
types=[BOT,ID,BOOL,('arr',ID,BOOL),('all',('all',('arr',('v',1),('v',0))))]
for depth in range(6):
 for A in types:
  p=ae(pid,A)
  for _ in range(depth):p=ap(ae(pid,('arr',A,A)),p)
  certs.append(p)
for A,B,C in itertools.product(types[:3],repeat=3):
 certs += [{'rule':'k','A':A,'B':B},{'rule':'s','A':A,'B':B,'C':C}]
for p in list(certs):
 t,ty=r.check(p)
 try:
  u,tr=r.normalize(t,100)
 except r.FuelExhausted:continue
 if len(tr)>1:certs.append({'rule':'reduce','proof':p,'trace':tr})
# Explicit binder nests exercise all_i and scoped de Bruijn instantiation.
for d in range(1,8):
 for j in range(d):
  p=i(('v',j))
  for _ in range(d):p=ai(p)
  certs.append(p)
unique={dump_json(p):p for p in certs};rows=[]
for n,(raw,p) in enumerate(unique.items()):
 t,ty=r.check(p);rows.append((f'probe{n}',raw));(OUT/(f'probe{n}.json')).write_bytes(raw)
records=[];env={**os.environ,'LEAN_PATH':str(ROOT/'runtime-formal-baseline')};lean='private-locator:4211d241978f643cb623'
for k in range(0,len(rows),16):
 batch=rows[k:k+16];name=f'Exports{k//16:03d}';text=export_module_owned(batch);path=OUT/(name+'.lean');path.write_text(text)
 p=subprocess.run([lean,'-o',name+'.olean',path.name],cwd=OUT,env=env,capture_output=True,timeout=180)
 (OUT/(name+'.stdout')).write_bytes(p.stdout);(OUT/(name+'.stderr')).write_bytes(p.stderr)
 record={'module':name,'cases':len(batch),'exit_code':p.returncode,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'olean_bytes':(OUT/(name+'.olean')).stat().st_size if (OUT/(name+'.olean')).exists() else 0};records.append(record);print(record,flush=True)
 (OUT/'RESULT.json').write_text(json.dumps({'cases':len(rows),'modules':records,'scope':'Fresh Python export → exact Lean checker erasure/type/soundness probes; finite evidence, not general Python refinement'},indent=2)+'\n')
 if p.returncode:print(p.stdout.decode());break
