#!/usr/bin/env python3
"""Bounded qualification of received iterator repair; writes only beside this script."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast, datetime, difflib, hashlib, importlib.util, json, os, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parent
WORK=ROOT.parent.parent
V2=WORK/'t20-consolidation-20261011/projection/package-v2'
INTAKE=ROOT.parent/'pro-intake'
OLD=V2/'replay/finite-contracts/contracts.py'
NEW=INTAKE/'execution/repaired-30/contracts.py'
DOWN=WORK/'t20-consolidation-20261011/proofs/replay/rational-joint-kernel'
ARCHIVE=WORK/'t20-consolidation-20261011/catalogue/archive-views/rational-kernel-additive-preservation-20261011.zip--fd5ff4c23019/rational-kernel-additive-preservation-20261011/payload/hase-rational-kernel-transport-20261011'
PATCH=INTAKE/'recovery-handoff/Orthemology_T20_Dot_Recovery_Handoff_20261011/Code_Diff/provisional_to_reconstructed_contracts.patch'
sources=[OLD,NEW,PATCH,*[INTAKE/'execution/repaired-30'/f for f in ['test_contracts.py','test_one_shot_recovery.py']],V2/'replay/finite-contracts/exhaustive_oracle.py',ARCHIVE/'SOURCE_BOUNDARY.json',ARCHIVE/'verify.py',DOWN/'REPLAY_RECEIPT.json',*[DOWN/'hase-rational-kernel-transport-20261011'/f for f in ['test_transport.py','rational_kernel.py','FIXTURE.json']]]
V2PAYLOAD=V2/'proof-families/rational-hase-j/rational-kernel-additive-preservation-20261011/payload'
sources.extend([V2PAYLOAD/'received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py',V2PAYLOAD/'hase-rational-kernel-transport-20261011/test_transport.py',V2PAYLOAD/'hase-rational-kernel-transport-20261011/rational_kernel.py',WORK/'t20-consolidation-20261011/catalogue/archive-views/Orthemology_T20_Whole_Corpus_Synthesis_20261010_1_.zip--38ed92bbec08/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/REPRODUCE.md'])
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(p,msg):
    if not p: raise RuntimeError(msg)
def load(name,p):
    sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
def capture(f):
    try: return {'value':f()}
    except Exception as e: return {'error':type(e).__name__,'message':str(e)}
def run(label,cmd,cwd,expected=0):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'))
    (ROOT/(label+'.stdout')).write_text(p.stdout);(ROOT/(label+'.stderr')).write_text(p.stderr)
    runs.append({'label':label,'command':cmd,'cwd':str(cwd.relative_to(ROOT)),'exit_code':p.returncode,'expected_exit_code':expected,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()})
    require(p.returncode==expected,label+' unexpected status')
    return p

before={str(p.relative_to(WORK)):sha(p) for p in sources}
for f in ['test_transport.py','rational_kernel.py']:
    require(sha(V2PAYLOAD/'hase-rational-kernel-transport-20261011'/f)==sha(DOWN/'hase-rational-kernel-transport-20261011'/f),'v2 downstream caller differs')
(ROOT/'INPUT_BINDINGS.json').write_text(json.dumps(before,indent=2)+'\n')
actual=''.join(difflib.unified_diff(OLD.read_text().splitlines(True),NEW.read_text().splitlines(True),fromfile='provisional/research/contracts.py',tofile='reconstruction/research/contracts.py'))
require(actual==PATCH.read_text(),'supplied patch differs from exact old/new diff')
(ROOT/'EXACT_DIFF.patch').write_text(actual)
def changed_nodes():
    a={n.name:ast.dump(n) for n in ast.parse(OLD.read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    b={n.name:ast.dump(n) for n in ast.parse(NEW.read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    return [name for name in a.keys()|b.keys() if a.get(name)!=b.get(name)]
require(set(changed_nodes())=={'Contract','valid_partition','as_reaches','closure_basis'},'unexpected changed top-level definition')

runs=[]
for flavor,code in [('old',OLD),('repaired',NEW)]:
    d=ROOT/'execution'/flavor;d.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(code,d/'contracts.py')
    for f in ['test_contracts.py','test_one_shot_recovery.py']:
        shutil.copyfile(INTAKE/'execution/repaired-30'/f,d/f)
    shutil.copyfile(V2/'replay/finite-contracts/exhaustive_oracle.py',d/'exhaustive_oracle.py')
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        if flavor=='old':
            run(f'{flavor}-inherited-{mode}',[sys.executable,*flags,'-B','-m','unittest','test_contracts','-v'],d)
            run(f'{flavor}-red-four-{mode}',[sys.executable,*flags,'-B','-m','unittest','test_one_shot_recovery','-v'],d,1)
        else:
            run(f'{flavor}-thirty-{mode}',[sys.executable,*flags,'-B','-m','unittest','discover','-p','test_*.py','-v'],d)
            run(f'{flavor}-oracle-{mode}',[sys.executable,*flags,'-B','exhaustive_oracle.py'],d)

# Preserve exact caller/import-relative path and fixture. Only dependency differs.
dependency_rel='received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py'
boundary=json.loads((ARCHIVE/'SOURCE_BOUNDARY.json').read_text())
pin=next(r for r in boundary['retained'] if r['path']==dependency_rel)
downstream={}
for flavor,code in [('old',OLD),('repaired',NEW)]:
    d=ROOT/'downstream'/flavor
    caller=d/'hase-rational-kernel-transport-20261011';caller.mkdir(parents=True,exist_ok=True)
    dep=d/dependency_rel;dep.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(code,dep)
    for f in ['test_transport.py','rational_kernel.py','FIXTURE.json']:
        shutil.copyfile(DOWN/'hase-rational-kernel-transport-20261011'/f,caller/f)
    # Evaluate the exact dependency comparison used by original verify.py pins().
    # This is one retained dependency preflight, NOT the full 3097-pin/Lean verifier.
    def dep_preflight():
        if sha(d/pin['path'])!=pin['sha256']: raise RuntimeError('Retained input changed: '+pin['path'])
        return 'PASS'
    preflight=capture(dep_preflight)
    require(('error' in preflight)==(flavor=='repaired'),'unexpected historical pin result')
    logs=[]
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        p=run(f'downstream-{flavor}-{mode}',[sys.executable,*flags,'-B','test_transport.py'],caller)
        obj=json.loads(p.stdout);require(obj['count']==162 and obj['exhaustive_rows']==125 and obj['status']=='PASS','caller count changed')
        logs.append(sha(ROOT/f'downstream-{flavor}-{mode}.stdout'))
    downstream[flavor]={'dependency_actual_sha256':sha(dep),'historical_expected_sha256':pin['sha256'],'historical_dependency_preflight':preflight,'python_checks':162,'exhaustive_rows':125,'normal_optimized_stdout_identical':len(set(logs))==1,'stdout_sha256':logs[0]}
require(downstream['old']['stdout_sha256']==downstream['repaired']['stdout_sha256'],'downstream observable test output differs')

old=load('qualified_old',ROOT/'execution/old/contracts.py');new=load('qualified_new',ROOT/'execution/repaired/contracts.py')
def make(m,states=(0,1,2),successors=(0,1,2),labels=(0,0,0),costs=(0,0,0),container=tuple):
    return m.Contract(container(states),['a'],['o'],dict(zip(states,labels)),{s:container(['a']) for s in states},{(s,'a'):v for s,v in zip(states,costs)},{(s,'a'):container([('o',t,F(1))]) for s,t in zip(states,successors)})
def contract_values(c):
    return (c.states,c.actions,c.outcomes,dict(c.labels),dict(c.enabled),dict(c.costs),dict(c.kernels))
def partitions(xs):
    if not xs: yield [];return
    for p in partitions(xs[1:]):
        yield [(xs[0],)]+p
        for i in range(len(p)):yield p[:i]+[(xs[0],)+p[i]]+p[i+1:]
counts={'reusable_contract_variants':0,'partition_comparisons':0,'valid_quotient_sidecar_comparisons':0,'stationary_reachability_comparisons':0,'closure_comparisons':0}
for targets in product(range(3),repeat=3):
 for labels in product(range(2),repeat=3):
  for costs in product(range(2),repeat=3):
   for container in [tuple,list]:
    a=make(old,successors=targets,labels=labels,costs=costs,container=container);b=make(new,successors=targets,labels=labels,costs=costs,container=container)
    require(contract_values(a)==contract_values(b),'reusable Contract values differ')
    coarse={s:0 for s in a.states}
    require(old.coarsest_refinement(a,coarse)==new.coarsest_refinement(b,coarse),'refinement differs')
    counts['reusable_contract_variants']+=1
    for p in partitions(list(a.states)):
        pa=container(container(x) for x in p)
        va=old.valid_partition(a,pa);vb=new.valid_partition(b,pa)
        require(va==vb,'partition validity differs');counts['partition_comparisons']+=1
        if va:
            qa,ma=old.quotient(a,pa);qb,mb=new.quotient(b,pa)
            require(contract_values(qa)==contract_values(qb) and ma==mb,'quotient differs')
            require(old.sidecar(a,coarse,pa)==new.sidecar(b,coarse,pa),'sidecar differs')
            counts['valid_quotient_sidecar_comparisons']+=1
    if container is tuple:
        for target in [(),(0,),(1,),(2,),(0,1,2)]:
            for start in a.states:
                require(old.as_reaches(a,start,set(target),{s:'a' for s in a.states})==new.as_reaches(b,start,set(target),{s:'a' for s in b.states}),'reachability differs')
                counts['stationary_reachability_comparisons']+=1
for entries in product((-1,0,1),repeat=4):
    matrix=(entries[:2],entries[2:])
    for outputs in [(),((1,0),),((0,1),),((1,1),),((1,0),(0,1))]:
        for container in [tuple,list]:
            actions=container([container(container(r) for r in matrix)])
            require(old.closure_basis(outputs,actions)==new.closure_basis(outputs,actions),'closure differs')
            counts['closure_comparisons']+=1

# Boundary controls report concrete wrong old outputs and exact residual exceptions.
args=(('x',),('a',),('o',),{'x':0},{'x':('a',)},{('x','a'):0})
invariants={}
for flavor,m in [('old',old),('repaired',new)]:
    c=m.Contract(*args,{('x','a'):iter((('o','x',F(1)),))})
    invalid=make(m,states=('x','y'),successors=('x','y'),labels=(0,1),costs=(0,0))
    reach=make(m,states=('x','done'),successors=('done','done'),labels=(0,1),costs=(0,0))
    valid=make(m,states=('x','y'),successors=('x','y'),labels=(0,0),costs=(0,0))
    record={'stored_generator_row':repr(c.kernels['x','a']),'stored_row_mass':str(sum((p for o,t,p in c.kernels['x','a']),F(0))),
      'invalid_merge_generator':m.valid_partition(invalid,iter((('x','y'),))),
      'almost_sure_generator_target':m.as_reaches(reach,'x',iter(('done',)),{'x':'a','done':'a'}),
      'generator_action_closure_rank':len(m.closure_basis(((1,0),),iter((((1,1),(0,1)),)))[0]),
      'valid_partition_generator':capture(lambda:m.valid_partition(valid,iter((('x','y'),)))),
      'quotient_outer_generator':capture(lambda:m.quotient(valid,iter((('x','y'),)))),
      'sidecar_outer_generator':capture(lambda:m.sidecar(valid,{'x':0,'y':0},iter((('x','y'),))))}
    # Neither input shape is an endorsed general-Iterable API outside four fixes.
    record['quotient_inner_generator']=capture(lambda:m.quotient(valid,(iter(('x','y')),)))
    record['closure_output_generator']=capture(lambda:m.closure_basis(iter(((1,0),)),(((1,1),(0,1)),)))
    record['enabled_menu_generator']=capture(lambda:m.Contract(('x',),('a',),('o',),{'x':0},{'x':iter(('a',))},{('x','a'):0},{('x','a'):(('o','x',1),)}))
    record['invalid_generator_rows']={name:capture(lambda row=row:m.Contract(*args,{('x','a'):iter(row)})) for name,row in [('half_mass',(('o','x',F(1,2)),)),('negative',(('o','x',-1),('o','x',2))),('float',(('o','x',1.0),)),('bool',(('o','x',True),)),('unknown',(('o','missing',1),))]}
    require(all('error' in r for r in record['invalid_generator_rows'].values()),'invalid generator row accepted')
    invariants[flavor]=record

# Exact mapping values are equal; input mapping iteration order is observably changed.
keys=[(s,'a') for s in (0,1,2)]
keys=list(reversed(tuple(set(keys))))
k={key:(('o',key[0],F(1)),) for key in keys}
base=((0,1,2),('a',),('o',),{s:0 for s in (0,1,2)},{s:('a',) for s in (0,1,2)},{key:0 for key in keys})
a=old.Contract(*base,k);b=new.Contract(*base,k)
order={'input_keys':repr(tuple(k)),'old_keys':repr(tuple(a.kernels)),'repaired_keys':repr(tuple(b.kernels)),'mapping_values_equal':dict(a.kernels)==dict(b.kernels),'insertion_order_preserved_old':tuple(a.kernels)==tuple(k),'insertion_order_preserved_repaired':tuple(b.kernels)==tuple(k)}
require(order['mapping_values_equal'] and order['insertion_order_preserved_old'] and not order['insertion_order_preserved_repaired'],'order probe invalid')

after={str(p.relative_to(WORK)):sha(p) for p in sources}
require(before==after,'read-only input preservation failed')
result={'status':'PASS_WITH_EXPLICIT_SCOPE_LIMITS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'patch_exact':True,'changed_definitions':sorted(changed_nodes()),'runs':runs,'differential_finite_controls':counts,'downstream':downstream,'input_boundary_observations':invariants,'kernel_mapping_order':order,'all_bound_sources_unchanged':before==after,'scope':'Four-function iterator qualification and exact Python downstream caller only; historical pin refusal expected; no historical receipt repinning, no full Lean verifier or production adoption.'}
(ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','patch_exact','differential_finite_controls','downstream','kernel_mapping_order','all_bound_sources_unchanged']},indent=2))
