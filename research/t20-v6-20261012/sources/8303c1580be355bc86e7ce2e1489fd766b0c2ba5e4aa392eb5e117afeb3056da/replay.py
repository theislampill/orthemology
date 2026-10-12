#!/usr/bin/env python3
"""Bounded trust=0 replay using retained Lean/Mathlib objects; never rebuild dependencies."""
from pathlib import Path
import hashlib,json,os,re,subprocess,time
R=Path(__file__).resolve().parent; W=R.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
PATHS=[str(R/'replay-lib')]+[x for x in (R/'lean_path.txt').read_text().strip().split(':') if x != str(R)]
OUT=R/'replay-lib';OUT.mkdir(exist_ok=True)
LOG=R/'replay-logs';LOG.mkdir(exist_ok=True)
env=dict(os.environ,LEAN_PATH=':'.join(PATHS))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
modules=['TruncatedMoment','ScalarPositivity','DegreeBridge','Certificate','Controls','MomentValues','Verify']
results=[]
for mod in modules:
 src=R/(mod+'.lean')
 assert not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by)\b',src.read_text()),mod
 start=time.monotonic()
 proc=subprocess.run([str(LEAN),'--trust=0','-o',str(OUT/(mod+'.olean')),str(src)],cwd=R,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (LOG/(mod+'.log')).write_text(proc.stdout)
 assert proc.returncode==0,(mod,proc.stdout)
 assert 'sorryAx' not in proc.stdout and 'error:' not in proc.stdout
 results.append({'module':mod,'status':'PASS','source_sha256':sha(src),'object_sha256':sha(OUT/(mod+'.olean')),'elapsed_seconds':round(time.monotonic()-start,3)})
checks=(LOG/'Verify.log').read_text()
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",checks)
assert len(axioms)==16,axioms
for name,ax in axioms: assert set(x.strip() for x in ax.split(',')) <= {'propext','Classical.choice','Quot.sound'},(name,ax)
# Every control is a false claim with an actual theorem-based arithmetic reduction.
negative={
 'wrong_witness_value':'example : Lambda witness = -1 := by rw [Lambda_witness]; norm_num',
 'wrong_triple_moment':'example : Lambda (term 1 1 1 1) = 0 := by rw [moment_111]; norm_num',
 'quartic_nonnegative_implies_Lambda_nonnegative':'example : 0 ≤ Lambda witness := by rw [Lambda_witness]; norm_num',
 'untruncated_square_positivity':'example : 0 ≤ Lambda (cubicControl^2) := by rw [cubic_control_value]; norm_num',
 'negative_mass_functional':'example : 0 < -Lambda (term 0 0 0 1) := by rw [moment_000]; norm_num',
}
negative_results=[]
NEG=R/'negative-controls';NEG.mkdir(exist_ok=True)
for name,body in negative.items():
 src=NEG/(name+'.lean');src.write_text('import Controls\nimport MomentValues\nopen TruncatedMoment\n'+body+'\n')
 proc=subprocess.run([str(LEAN),'--trust=0',str(src)],cwd=R,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (LOG/(name+'.log')).write_text(proc.stdout)
 assert proc.returncode!=0 and 'error:' in proc.stdout,(name,proc.stdout)
 assert 'unknown module' not in proc.stdout and 'does not exist' not in proc.stdout,(name,proc.stdout)
 assert 'unsolved goals' in proc.stdout or 'tactic' in proc.stdout,(name,proc.stdout)
 negative_results.append({'name':name,'expected_rejection':True,'source_sha256':sha(src),'log_sha256':sha(LOG/(name+'.log'))})
# Exact direct-import lists from the Lean executable, not labels supplied by this script.
direct={}
for mod in modules:
 p=subprocess.run([str(LEAN),'--deps',str(R/(mod+'.lean'))],env=env,cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 assert p.returncode==0,p.stdout
 deps=[Path(x) for x in p.stdout.splitlines() if x.strip()]
 direct[mod]=[{'path':str(x),'sha256':sha(x)} for x in deps]
(R/'DIRECT_IMPORTS.json').write_text(json.dumps(direct,indent=2)+'\n')
# Resolve the imported source graph and record each retained actual object digest.
source_roots=[R]
for x in PATHS:
 p=Path(x)
 if str(p).endswith('/.lake/build/lib/lean'): source_roots.append(p.parents[3])
source_roots.append(W/'.toolchains/lean-4.19.0-linux/src/lean')
object_roots=[Path(x) for x in PATHS]+[W/'.toolchains/lean-4.19.0-linux/lib/lean']
seen=set(); closure=[]
def header_imports(text):
 # Lean permits imports only in the header. Strip nested block comments before
 # reading it; documentation examples containing the word import are not imports.
 out=[];i=0;depth=0
 while i<len(text):
  if text[i:i+2]=='/-':depth+=1;i+=2;continue
  if depth and text[i:i+2]=='-/':depth-=1;i+=2;continue
  if depth:i+=1;continue
  if text[i:i+2]=='--':
   j=text.find('\n',i);i=len(text) if j<0 else j;continue
  out.append(text[i]);i+=1
 deps=[];prelude=False
 for line in ''.join(out).splitlines():
  line=line.strip()
  if not line:continue
  if line=='prelude':prelude=True;continue
  if line.startswith('import '):deps.extend(line[7:].split());continue
  break
 return deps,prelude
def visit(mod):
 if mod in seen:return
 seen.add(mod)
 rel=mod.replace('.','/')
 src=next((p/(rel+'.lean') for p in source_roots if (p/(rel+'.lean')).is_file()),None)
 obj=next((p/(rel+'.olean') for p in object_roots if (p/(rel+'.olean')).is_file()),None)
 assert obj is not None,('Missing imported object',mod)
 row={'module':mod,'object_path':str(obj),'object_sha256':sha(obj)}
 if src is not None:
  text=src.read_text(); row.update(source_path=str(src),source_sha256=sha(src))
  imports,prelude=header_imports(text)
  for dep in imports:visit(dep)
  if not prelude and mod != 'Init':visit('Init')
 else: row['source_unavailable']=True
 closure.append(row)
for mod in modules:visit(mod)
(R/'IMPORTED_OBJECT_MANIFEST.json').write_text(json.dumps(closure,indent=2)+'\n')
inputs=[W/'heat-truncated-certificate-diagnostic-20261010'/x for x in ['RESULT.md','check_exact.py','EXACT_RESULTS.json']]+[W/'heat-transport-obstruction-independent-review-20261010/TRUNCATED_DIAGNOSTIC_REVIEW.md']
receipt={'status':'PASS_EXACT_KERNEL_PROOF_NO_NEW_AXIOMS','scope':'actual ternary MvPolynomial totalDegree<=2 squares and explicit globally nonnegative degree<=4 witness; no full-algebra positivity, no formal Bochner-measure theorem, no heat formalization','lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'trust_level':0,'new_axioms':[],'allowed_standard_axioms':['propext','Classical.choice','Quot.sound'],'module_results':results,'axiom_checks':[{'theorem':name,'axioms':ax.split(', ')} for name,ax in axioms],'negative_controls':negative_results,'exact_moment_checks':35,'imported_object_count':len(closure),'input_digests':[{'path':str(p),'sha256':sha(p)} for p in inputs],'direct_import_manifest_sha256':sha(R/'DIRECT_IMPORTS.json'),'imported_object_manifest_sha256':sha(R/'IMPORTED_OBJECT_MANIFEST.json'),'lean_executable_sha256':sha(LEAN)}
(R/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','trust_level','new_axioms','exact_moment_checks','imported_object_count']},indent=2));print('negative controls rejected:',len(negative_results));print('axiom checks:',len(axioms))
