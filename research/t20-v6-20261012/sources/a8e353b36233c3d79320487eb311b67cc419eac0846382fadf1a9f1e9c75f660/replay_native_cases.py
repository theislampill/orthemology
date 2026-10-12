from pathlib import Path
from dataclasses import dataclass
import sys, os, json, hashlib, subprocess, datetime, collections
R=Path(__file__).resolve().parent; P=Path('private-locator:ef374410ecf29a97d371'); OLD=P/'constructor-square/native-cross-language-final'; O=R/'native-case-replay';O.mkdir()
sys.path.insert(0,str(P/'python-bases/source'))
import reference
from boundaries import Rejection
@dataclass
class Fields:
 rows:list
H=lambda b:hashlib.sha256(b).hexdigest()
def wire(v):
 if isinstance(v,Fields):return '(WireValue.object ['+', '.join('('+json.dumps(k)+', '+wire(x)+')' for k,x in v.rows)+'])'
 if type(v)is list:return '(WireValue.array ['+', '.join(wire(x) for x in v)+'])'
 if type(v)is str:return '(WireValue.text '+json.dumps(v)+')'
 if type(v)is bool:return '(WireValue.boolean '+('true' if v else 'false')+')'
 if v is None:return 'WireValue.null'
 if type(v)is int:return f'(WireValue.natural {v})' if v>=0 else f'(WireValue.negative {-v-1})'
 raise TypeError(type(v))
def ty(a):
 if a[0]=='v':return f'(TypeCode.var {a[1]})'
 if a[0]=='bottom':return 'TypeCode.bottom'
 if a[0]=='arr':return f'(TypeCode.arrow {ty(a[1])} {ty(a[2])})'
 if a[0]=='all':return f'(TypeCode.all {ty(a[1])})'
 raise ValueError(a)
def term(t):return f'(Term.app {term(t[1])} {term(t[2])})' if t[0]=='app' else f'Term.{t[0]}'
def dups(v):
 if isinstance(v,Fields):return len({k for k,_ in v.rows})!=len(v.rows) or any(dups(x) for _,x in v.rows)
 if type(v)is list:return any(dups(x) for x in v)
 return False
old=json.loads((OLD/'CASES.json').read_text());rows=[]
for row in old:
 raw=(OLD/(row['name']+'.json')).read_bytes(); assert H(raw)==row['raw_sha256']
 v=json.loads(raw,object_pairs_hook=lambda r:Fields(r));dup=dups(v);assert dup==row['duplicate_field_wire']
 try:
  out=reference.check_json(raw,row['depth']);result='accept'; expected=f'some ({term(out[0])}, {ty(out[1])})'
 except Rejection as ex:out=None;result='refuse';expected='none'
 assert result==row['outcome'];native=None
 if not dup:
  try:nout=reference.check(json.loads(raw),row['depth']);native='accept';assert nout==out
  except Rejection:native='refuse'
  assert native==result
 else:assert result=='refuse'
 rows.append({**row,'fresh_outcome':result,'fresh_native_outcome':native,'expected':expected,'wire':wire(v)})
rec={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Finite actual strict-JSON/native reference execution compared to freshly compiled native-tree model; not universal runtime equivalence','fresh_model_result_sha256':H((R/'p03/RESULT.json').read_bytes()),'reference_sha256':H((P/'python-bases/source/reference.py').read_bytes()),'boundaries_sha256':H((P/'python-bases/source/boundaries.py').read_bytes()),'cases':[],'modules':[]}
def save(): (O/'RESULT.json').write_text(json.dumps(rec,indent=2)+'\n')
env={**os.environ,'LEAN_PATH':str(R/'p03/lib')};lean='private-locator:4211d241978f643cb623'
for start in range(0,len(rows),20):
 batch=rows[start:start+20];name=f'IndependentNative{start//20:03d}'
 lines=['import NativeCheckerBridge','set_option maxRecDepth 200000','set_option maxHeartbeats 0','open P03Source OrthemologyV2 OrthemologyV3']
 for row in batch:
  lines.append(f'theorem {row["name"]}_fresh : nativeCheck {row["depth"]} {row["wire"]} = {row["expected"]} := by\n  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]\n  decide\n#print axioms {row["name"]}_fresh')
 src=O/(name+'.lean');src.write_text('\n'.join(lines)+'\n');p=subprocess.run([lean,'-j1','-o',name+'.olean',src.name],cwd=O,env=env,capture_output=True,timeout=300)
 (O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr)
 rec['modules'].append({'name':name,'exit_code':p.returncode,'source_sha256':H(src.read_bytes()),'stdout_sha256':H(p.stdout),'stderr_sha256':H(p.stderr),'olean_sha256':H((O/(name+'.olean')).read_bytes()) if p.returncode==0 else None})
 rec['cases'] += [{k:v for k,v in row.items() if k not in ['expected','wire']} for row in batch];save();print(name,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
rec['status']='PASS';rec['cases_run']=len(rows);rec['outcomes']=dict(collections.Counter(x['fresh_outcome'] for x in rows));rec['duplicate_cases']=sum(x['duplicate_field_wire'] for x in rows);rec['native_cases']=sum(x['fresh_native_outcome'] is not None for x in rows);rec['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save();print(json.dumps({k:v for k,v in rec.items() if k not in ['cases','modules']}))
