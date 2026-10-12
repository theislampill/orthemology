"""Independent regression comparison, not a formal parser/compiler refinement."""
from pathlib import Path
import importlib.util,sys,random,json,hashlib,subprocess,os,time
ROOT=Path(__file__).resolve().parent
SOURCE=Path('private-locator:d8dc20b3e088111e6617')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('independent_prcodec',SOURCE);p=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p;spec.loader.exec_module(p)
def norm(s):
 t=s[0]
 if t=='seq':return sum((norm(x) for x in s[1:]),[])
 if t=='set':return [[t,s[1],s[2]]]
 if t=='loop':return [[t,s[1],s[2],norm(s[3])]]
 if t=='if':return [[t,s[1],norm(s[2]),norm(s[3])]]
 raise ValueError(s)
def le(e):
 tag={'c':'constant','v':'reg'}.get(e[0],e[0])
 return '(.'+tag+' '+(' '.join(str(x) if type(x)==int else le(x) for x in e[1:]))+')'
def ls(s):
 if s[0]=='seq':
  if not s[1:]:return '.skip'
  return '(.seq '+ls(s[1])+' '+ls(('seq',*s[2:]))+')'
 if s[0]=='set':return f'(.set {s[1]} {le(s[2])})'
 if s[0]=='loop':return f'(.loop {s[1]} {le(s[2])} {ls(s[3])})'
 return f'(.branch {le(s[1])} {ls(s[2])} {ls(s[3])})'
cases=[p.Program(3,3,p.Set(3,p.C(1))),p.Program(3,3,p.Set(3,p.E('le',p.V(2),p.V(1)))),p.Program(3,0,p.Seq()),p.Program(3,37,p.Seq(p.Set(1,p.C(9)),p.Set(37,p.E('add',p.V(0),p.V(2)))))]
rng=random.Random(20260930);ops=['add','sub','mul','div','mod','le','eq'];regs=[0,1,2,3,4,5,6,7,8,9,10,11,17,37,101]
def expr(d):
 if not d or rng.random()<.4:return p.C(rng.randrange(7)) if rng.random()<.4 else p.V(rng.choice(regs))
 if rng.random()<.15:return p.E('pow2',expr(d-1))
 return p.E(rng.choice(ops),expr(d-1),expr(d-1))
def stmt(d):
 if not d:return p.Set(rng.choice(regs),expr(2))
 k=rng.randrange(5)
 if k==0:return p.Seq()
 if k==1:return p.Seq(stmt(d-1),stmt(d-1))
 if k==2:return p.Loop(rng.choice(regs),expr(1),stmt(d-1))
 if k==3:return p.If(expr(2),stmt(d-1),stmt(d-1))
 return p.Set(rng.choice(regs),expr(2))
for _ in range(28):cases.append(p.Program(3,rng.choice(regs),stmt(3)))
header='''import Sigma2Compiled
open P02A2.ObserverCore P02A2.Sigma2Compiled
open Lean
namespace IndependentAstComparison
def ej : P02A2.ObserverCore.Expr → Json
  | .constant n => toJson ("c", n)
  | .reg r => toJson ("v", r)
  | .add a b => .arr #[toJson "add", ej a, ej b]
  | .sub a b => .arr #[toJson "sub", ej a, ej b]
  | .mul a b => .arr #[toJson "mul", ej a, ej b]
  | .div a b => .arr #[toJson "div", ej a, ej b]
  | .mod a b => .arr #[toJson "mod", ej a, ej b]
  | .le a b => .arr #[toJson "le", ej a, ej b]
  | .eq a b => .arr #[toJson "eq", ej a, ej b]
  | .pow2 a => .arr #[toJson "pow2", ej a]
def sj : Stmt → List Json
  | .skip => []
  | .seq s t => sj s ++ sj t
  | .set r e => [.arr #[toJson "set", toJson r, ej e]]
  | .loop r e s => [.arr #[toJson "loop", toJson r, ej e, .arr (sj s).toArray]]
  | .branch e s t => [.arr #[toJson "if", ej e, .arr (sj s).toArray, .arr (sj t).toArray]]
'''
D=ROOT/'candidate-sources';D.mkdir(exist_ok=True)
expect=[];lines=[]
for i,m in enumerate(cases):
 param=i*7
 expect.append(json.loads(json.dumps(norm(p.compile_sigma2(m,param).body))))
 lines.append(f'#eval IO.println ((Json.arr (sj (compiled {ls(m.body)} {m.output} {param})).toArray).compress)')
f=D/'IndependentAstComparison.lean';f.write_text(header+'\n'.join(lines)+'\nend IndependentAstComparison\n')
env={**os.environ};ev=subprocess.check_output(['bash','-c','source '+str(ROOT/'env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in ev.split(b'\0') if b'=' in v));env['LEAN_PATH']=str(ROOT/'candidate-build')+':'+env['LEAN_PATH']
cmd=['lean','-j1','--root='+str(D),str(f)];start=time.time();r=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True);(ROOT/'candidate-receipts'/'IndependentAstComparison.log').write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout,r.stderr)
actual=[json.loads(l) for l in r.stdout.splitlines() if l.startswith('[')];assert len(actual)==len(expect),(len(actual),len(expect))
for i,(a,e) in enumerate(zip(actual,expect)):assert a==e,i
out={'status':'32_NORMALIZED_AST_COMPARISONS_PASSED','source_python_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'lean_exporter_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'cases':len(cases),'seed':20260930,'seconds':time.time()-start,'command':cmd,'scope':'Supplementary ordinary constructor correspondence only; no formal Python parser/interpreter/serializer or numeric-index proof.'}
(ROOT/'CANDIDATE_AST_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
