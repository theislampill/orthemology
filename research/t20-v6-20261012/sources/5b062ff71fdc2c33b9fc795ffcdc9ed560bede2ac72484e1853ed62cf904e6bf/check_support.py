#!/usr/bin/env python3
"""Bounded Lean support replay and matrix dependency inventory; no baseline rebuilds."""
from pathlib import Path
import hashlib, json, os, re, subprocess, time
R = Path(__file__).resolve().parent
W = R.parent.parent
LEAN = W / '.toolchains/lean-4.19.0-linux/bin/lean'
retained_path = W / 'lean-truncated-moment-obstruction-20261010/lean_path.txt'
paths = [str(R)] + [p for p in retained_path.read_text().strip().split(':') if p != str(retained_path.parent)]
(R/'lean_path.txt').write_text(':'.join(paths)+'\n')
env = dict(os.environ, LEAN_PATH=':'.join(paths))
log = R/'logs'; log.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def run(name, args, expected=0):
    start = time.monotonic()
    p = subprocess.run([str(LEAN), '--trust=0', *args], cwd=W, env=env,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    dest=log/(name+'.log'); dest.write_text(p.stdout)
    assert (p.returncode == 0) == (expected == 0), (name, p.returncode, p.stdout)
    return {'name':name, 'exit_status':p.returncode, 'elapsed_seconds':round(time.monotonic()-start,3),
            'log':str(dest.relative_to(R)), 'log_sha256':sha(dest)},p.stdout
source=R/'ScalarSupport.lean'
assert not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by)\b',source.read_text())
checks=[]
a, scalar_log = run('scalar-trust-zero', ['-o',str(R/'ScalarSupport.olean'),str(source)])
checks.append(a)
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",scalar_log)
assert len(axioms)==4,axioms
parsed=[]
for theorem,ax in axioms:
    values=[x.strip() for x in ax.split(',')]
    assert set(values) <= {'propext','Classical.choice','Quot.sound'},(theorem,values)
    parsed.append({'theorem':theorem,'axioms':values})
a,_=run('retained-matrix-probe',[str(R/'RetainedMatrixProbe.lean')]); checks.append(a)
# False scalar claims must fail by proof checking, not by unavailable imports.
for name,claim in [('wrong_seed_value','example : (1 : ℝ) + 1 + 1 - 4 = 0 := by norm_num'),
                   ('wrong_origin_value','example : FullPolynomialMomentSupport.F 0 0 < (3 : ℝ)/4 := by norm_num [FullPolynomialMomentSupport.F]')]:
    p=R/(name+'.lean');p.write_text('import ScalarSupport\n'+claim+'\n')
    a,s=run(name,[str(p)],expected=1)
    assert 'error:' in s and ('unsolved goals' in s or 'tactic' in s),s
    assert 'does not exist' not in s and 'unknown module' not in s,s
    checks.append(a)
# Inventory source import graph, never executing missing module compilation.
source_roots=[]
for p in paths:
    pp=Path(p)
    if str(pp).endswith('/.lake/build/lib/lean'):source_roots.append(pp.parents[3])
source_roots += [W/'.toolchains/lean-4.19.0-linux/src/lean']
object_roots=[Path(p) for p in paths]+[W/'.toolchains/lean-4.19.0-linux/lib/lean']
def header_imports(text):
    out=[]; i=0; depth=0
    while i<len(text):
        if text[i:i+2]=='/-':depth+=1;i+=2;continue
        if depth and text[i:i+2]=='-/':depth-=1;i+=2;continue
        if depth:i+=1;continue
        if text[i:i+2]=='--':
            j=text.find('\n',i);i=len(text) if j<0 else j;continue
        out.append(text[i]);i+=1
    deps=[]
    for line in ''.join(out).splitlines():
        line=line.strip()
        if not line or line=='prelude':continue
        if line.startswith('import '):deps.extend(line[7:].split());continue
        break
    return deps
memo={}
def module_info(module):
    if module in memo:return memo[module]
    rel=module.replace('.','/')
    src=next((p/(rel+'.lean') for p in source_roots if (p/(rel+'.lean')).is_file()),None)
    obj=next((p/(rel+'.olean') for p in object_roots if (p/(rel+'.olean')).is_file()),None)
    row={'module':module,'object_present':obj is not None,'source_present':src is not None}
    if src:row.update(source=str(src),source_sha256=sha(src),imports=header_imports(src.read_text()))
    if obj:row.update(object=str(obj),object_sha256=sha(obj))
    memo[module]=row; return row
assessment={}
for top in ['Mathlib.LinearAlgebra.Matrix.SchurComplement','Mathlib.LinearAlgebra.Matrix.PosDef',
            'Mathlib.LinearAlgebra.Matrix.NonsingularInverse','Mathlib.Algebra.MvPolynomial.Basic']:
    seen=set()
    def visit(mod):
        if mod in seen:return
        seen.add(mod)
        for dep in module_info(mod).get('imports',[]):visit(dep)
    visit(top)
    missing=sorted(mod for mod in seen if not module_info(mod)['object_present'])
    assessment[top]={'transitive_explicit_source_import_modules':len(seen),
                    'missing_object_count':len(missing),'missing_object_modules':missing,
                    'direct':module_info(top)}
(R/'MATRIX_DEPENDENCY_ASSESSMENT.json').write_text(json.dumps(assessment,indent=2)+'\n')
# Actual direct objects used by the scalar certificate.
p=subprocess.run([str(LEAN),'--deps',str(source)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
assert p.returncode==0,p.stdout
imports=[{'path':v,'sha256':sha(Path(v))} for v in p.stdout.splitlines() if v]
(R/'DIRECT_IMPORTS.json').write_text(json.dumps(imports,indent=2)+'\n')
receipt={'status':'PASS_BOUNDED_SCALAR_LEAN_SUPPORT',
    'scope':'F(x,y)>=3/4 and F(x,y)>0 for all real x,y; separating seed arithmetic only. No formal infinite functional, all-degree square positivity, recurrence well-foundedness, or measure contradiction.',
    'lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),
    'lean_executable_sha256':sha(LEAN),'trust_level':0,'new_axioms':[],
    'source_sha256':sha(source),'object_sha256':sha(R/'ScalarSupport.olean'),
    'axiom_checks':parsed,'checks':checks,'baseline_rebuilds':False,
    'dependency_assessment_sha256':sha(R/'MATRIX_DEPENDENCY_ASSESSMENT.json'),
    'direct_imports_sha256':sha(R/'DIRECT_IMPORTS.json')}
(R/'SUPPORT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'trust_level':0,'axiom_checks':len(parsed),
    'negative_controls_rejected':2,'matrix_import_probe':'PASS',
    'missing_schur_objects':assessment['Mathlib.LinearAlgebra.Matrix.SchurComplement']['missing_object_count'],
    'missing_posdef_objects':assessment['Mathlib.LinearAlgebra.Matrix.PosDef']['missing_object_count']},indent=2))
