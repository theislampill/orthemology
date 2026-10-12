#!/usr/bin/env python3
"""Replay the complete polynomial construction at trust 0; never build dependencies."""
from pathlib import Path
import hashlib, json, os, re, subprocess, time
R=Path(__file__).resolve().parent
W=R.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
paths=R.joinpath('lean_path.txt').read_text().strip().split(':')
assert Path(paths[0])==R
E=dict(os.environ,LEAN_PATH=':'.join(paths))
LOG=R/'logs'; LOG.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
modules=['ScalarSupport','Indexing','Schur','Recurrence','Moment','PolynomialBridge','Countermodel']
checks=[]; axiom_checks=[]
allowed={'propext','Classical.choice','Quot.sound'}
def run(name,args,success=True):
    start=time.monotonic()
    p=subprocess.run([str(LEAN),'--trust=0',*args],cwd=W,env=E,text=True,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    out=LOG/(name+'.log');out.write_text(p.stdout)
    assert (p.returncode==0)==success,(name,p.returncode,p.stdout)
    if success:
        assert 'warning:' not in p.stdout,(name,p.stdout)
    else:
        assert 'error:' in p.stdout and ('unsolved goals' in p.stdout or 'tactic' in p.stdout),(name,p.stdout)
        assert 'does not exist' not in p.stdout and 'unknown module' not in p.stdout,(name,p.stdout)
    row={'check':name,'exit_status':p.returncode,'seconds':round(time.monotonic()-start,3),
         'log':str(out.relative_to(R)),'log_sha256':sha(out)}
    checks.append(row)
    return p.stdout
for m in modules:
    p=R/(m+'.lean')
    assert not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by)\b',p.read_text()),m
    out=run(m+'-trust0',['-o',str(R/(m+'.olean')),str(p)])
    for theorem,axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out):
        aa=[x.strip() for x in axioms.split(',') if x.strip()]
        assert set(aa)<=allowed,(theorem,aa)
        axiom_checks.append({'theorem':theorem,'axioms':aa})
assert any(r['theorem']=='FullPolynomialCountermodel.full_polynomial_countermodel' for r in axiom_checks)
# Algebraic negative control: removing the unit Schur pivot invalidates the
# exact completed-square theorem itself, not just a final scalar assertion.
negative=R/'negative-controls'; negative.mkdir(exist_ok=True)
s=(R/'Schur.lean').read_text()
a='extendA A v (1 + v ⬝ᵥ w)'; b='extendA A v (v ⬝ᵥ w)'
assert a in s
p=negative/'MissingSchurPivot.lean';p.write_text(s.replace(a,b))
run('reject-missing-schur-pivot',[str(p)],False)
for name,claim in [
 ('WrongWitnessValue','example : FullPolynomialCountermodel.Λ FullPolynomialCountermodel.witness = 0 := by\n  rw [FullPolynomialCountermodel.witness_negative]\n  norm_num'),
 ('ZeroConstantSquare','example : FullPolynomialCountermodel.Λ ((1 : FullFunctionalPolynomialBridge.Polynomial)^2) = 0 := by\n  norm_num [FullPolynomialCountermodel.normalized]')]:
    p=negative/(name+'.lean');p.write_text('import Countermodel\n'+claim+'\n')
    run('reject-'+name,[str(p)],False)
# Bind exact selected direct objects, their source headers, and their complete
# transitive explicit import graph (with each module's implicit Init import).
source_roots=[R]
for path in paths[1:]:
    q=Path(path)
    if str(q).endswith('/.lake/build/lib/lean'):source_roots.append(q.parents[3])
source_roots.append(W/'.toolchains/lean-4.19.0-linux/src/lean')
object_roots=[Path(p) for p in paths]+[W/'.toolchains/lean-4.19.0-linux/lib/lean']
def imports(source):
    text=source.read_text();clean=[];i=0;depth=0
    while i<len(text):
        if text[i:i+2]=='/-':depth+=1;i+=2;continue
        if depth and text[i:i+2]=='-/':depth-=1;i+=2;continue
        if depth:i+=1;continue
        if text[i:i+2]=='--':
            j=text.find('\n',i);i=len(text) if j<0 else j;continue
        clean.append(text[i]);i+=1
    deps=[];prelude=False
    for line in ''.join(clean).splitlines():
        line=line.strip()
        if not line:continue
        if line=='prelude':prelude=True;continue
        if line.startswith('import '):deps.extend(line[7:].split());continue
        break
    if not prelude and 'Init' not in deps:deps.insert(0,'Init')
    return deps
bindings={}
def visit(m):
    if m in bindings:return
    rel=m.replace('.','/')
    src=next((q/(rel+'.lean') for q in source_roots if (q/(rel+'.lean')).is_file()),None)
    obj=next((q/(rel+'.olean') for q in object_roots if (q/(rel+'.olean')).is_file()),None)
    assert src and obj,(m,src,obj)
    deps=imports(src)
    bindings[m]={'source':str(src),'source_sha256':sha(src),'object':str(obj),
        'object_sha256':sha(obj),'imports':deps}
    for d in deps:visit(d)
for m in modules:visit(m)
(R/'IMPORT_SOURCE_BINDINGS.json').write_text(json.dumps(bindings,indent=2,sort_keys=True)+'\n')
direct={}
for m in modules:
    p=subprocess.run([str(LEAN),'--deps',str(R/(m+'.lean'))],cwd=W,env=E,text=True,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    assert p.returncode==0,p.stdout
    direct[m]=[{'object':v,'sha256':sha(v)} for v in p.stdout.splitlines() if v]
(R/'DIRECT_IMPORTS.json').write_text(json.dumps(direct,indent=2,sort_keys=True)+'\n')
proof=W/'full-polynomial-moment-countermodel-20261010'
assert sha(R/'ScalarSupport.lean')==sha(proof/'lean-support/ScalarSupport.lean')
receipt={'status':'PASS_FULL_POLYNOMIAL_COUNTERMODEL_LEAN','scope':[
    'Explicit exceptional monomial indexing bijection and global midpoint precedence',
    'Completed-square identity, strict positive-definiteness preservation, explicit block inverse',
    'Total unbounded real Schur recursion with prescribed four seed moments',
    'Prefix stability and one infinite moment sequence with all finite Gram matrices positive',
    'Actual real linear functional on MvPolynomial (Fin 2) R',
    'All nonzero real polynomials p satisfy Lambda(p^2)>0, without positivity premises',
    'Lambda(1)=1; actual witness has all evaluations >=3/4 and Lambda(witness)=-1',
    'Not positive on all pointwise nonnegative polynomials'],
    'not_formalized':['Dyadic rational/executable computability theorem',
        'Explicit inverse enumeration algorithm (inverse defined by classical choice)',
        'Measure-theoretic representation/integral corollary','Determinant=4 invariant'],
    'trust_level':0,'new_axioms':[],
    'lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),
    'lean_executable':str(LEAN),'lean_executable_sha256':sha(LEAN),
    'lean_path_sha256':sha(R/'lean_path.txt'),
    'sources':{m:sha(R/(m+'.lean')) for m in modules},
    'objects':{m:sha(R/(m+'.olean')) for m in modules},
    'origin_proof_sha256':sha(proof/'PROOF.md'),
    'origin_algorithm_sha256':sha(proof/'countermodel.py'),
    'scalar_support_byte_identical_to_origin':True,
    'axiom_checks':axiom_checks,'checks':checks,
    'bound_import_modules':len(bindings),
    'import_source_bindings_sha256':sha(R/'IMPORT_SOURCE_BINDINGS.json'),
    'direct_imports_sha256':sha(R/'DIRECT_IMPORTS.json'),
    'baseline_rebuilds':False,'negative_controls_rejected':3}
(R/'LEAN_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'trust_level':0,'axiom_checks':len(axiom_checks),
 'bound_import_modules':len(bindings),'negative_controls_rejected':3,'baseline_rebuilds':False},indent=2))
