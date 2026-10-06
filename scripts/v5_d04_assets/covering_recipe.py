#!/usr/bin/env python3
"""PRIVATE source-bound shell-free translation; approval required before use.

Preserves replay_public.py, science/verify.sh and both mutation-table contracts.
Runs original finite helpers, uses their exact golden JSON, and journals every
compiler child directly. The scientific source files remain unchanged.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse, ast, hashlib, json, os, re, signal, subprocess, sys

PINS={'replay_public.py':'e9e76dc61e99b298c47d4a3a139916111ef5b04be42fb729d0ebc60be770e970',
      'science/verify.sh':'a5fdf59cee2aaee703694d9784714dfc156434e67e3d9a98459fcaab10109c1c',
      'science/tests/mutation_controls.py':'84cc407e25b40c3886f12d117669c9dd28254eaf47cd233de441a556c6244d4f',
      'review/check_primary_mutants.py':'812dd6c8f15770791b87e2e94ac2c49858a2a58a17817aba50f4d78d8eddd6ae'}
AXIOMS={'propext','Classical.choice','Quot.sound'}
INFRA=re.compile(r'unknown module|unknown constant|unknown identifier|unknown namespace|no such file|file not found|object file|timed out|out of memory|maximum (?:recursion|heartbeats)|deterministic timeout',re.I)
ACTIVE=None
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def write(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def terminate_child():
    if ACTIVE is not None and ACTIVE.poll() is None:
        os.killpg(ACTIVE.pid,signal.SIGTERM)
        try:ACTIVE.wait(timeout=2)
        except subprocess.TimeoutExpired:os.killpg(ACTIVE.pid,signal.SIGKILL);ACTIVE.wait()
def interrupted(signum,frame):
    terminate_child();raise SystemExit(128+signum)
def manifest(base,name,exact=True):
    data=json.loads((base/name).read_text());paths=set()
    for row in data['files']:
        rel=PurePosixPath(row['path']);require(not rel.is_absolute() and '..' not in rel.parts,'Unsafe original manifest path')
        path=base/str(rel);require(not path.is_symlink() and path.is_file(),'Missing original manifest file')
        require(path.stat().st_size==row['size'] and sha(path)==row['sha256'],'Original manifest file changed')
        paths.add(row['path'])
    if exact:require({p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}==paths|{name},'Original packet inventory changed')
    return len(paths)
def mutation_table(path):
    tree=ast.parse(path.read_text());tables=[ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='mutations' for t in n.targets)]
    require(len(tables)==1 and len(tables[0])==6,'Original mutation table differs');return tables[0]

def main():
    global ACTIVE
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',required=True,type=Path);ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--lean',required=True,type=Path);ap.add_argument('--mathlib',required=True,type=Path);args=ap.parse_args()
    root=args.source_root.absolute();out=args.output.absolute();lean=args.lean.resolve();mathlib=args.mathlib.absolute()
    require(root.is_dir() and not root.is_symlink(),'Original source root unavailable')
    require(not out.exists() and not out.resolve().is_relative_to(root.resolve()),'Output must be absent and outside source')
    for name,fingerprint in PINS.items():require(sha(root/name)==fingerprint,'Original recipe changed: '+name)
    count=manifest(root,'PUBLIC_MANIFEST.json');science=root/'science';review=root/'review';science_count=manifest(science,'MANIFEST.json')
    binding=json.loads((root/'PUBLIC_BINDING.json').read_text());tools=json.loads((root/'TOOLCHAIN_BINDING.json').read_text())
    require(sha(science/'MANIFEST.json')==binding['science_manifest_sha256'] and sha(review/'REVIEW_RECEIPT_V2.json')==binding['review_receipt_sha256'],'Original science/review binding changed')
    require(sha(lean)==tools['lean_sha256'],'Wrong exact Lean executable')
    dependencies=json.loads((root/'MATHLIB_SOURCE_MANIFEST.json').read_text())['files']
    def check_dependencies():
        for row in dependencies:
            p=mathlib/row['path'];require(p.is_file() and p.stat().st_size==row['size'] and sha(p)==row['sha256'],'Mathlib source changed')
    check_dependencies();out.mkdir(parents=True);kernel=out/'kernel';(kernel/'logs').mkdir(parents=True)
    env={k:v for k,v in os.environ.items() if not k.startswith(('LEAN_','PYTHON','LD_')) and k!='DYLD_INSERT_LIBRARIES'}
    paths=[kernel,mathlib/'.lake/build/lib/lean']+sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    env.update({'LEAN_419':str(lean),'MATHLIB_C44':str(mathlib),'LEAN_PATH':os.pathsep.join(map(str,paths)),
                'PYTHONDONTWRITEBYTECODE':'1','PATH':os.pathsep.join([str(lean.parent),str(Path(sys.executable).parent),os.defpath])})
    stages=[]
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    def run(name,argv,logname,expected=0,literals=(),budget=600):
        global ACTIVE
        log=out/logname;log.parent.mkdir(parents=True,exist_ok=True);require(not log.exists(),'Child output already exists')
        row={'id':name,'argv':[str(x) for x in argv],'cwd':str(root),'budget_seconds':budget,'started_at':now(),'terminal':'RUNNING','exit_code':None,'log':logname}
        stages.append(row);write(out/'STAGES.json',stages)
        with log.open('xb') as stream:
            ACTIVE=subprocess.Popen(row['argv'],cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,shell=False,start_new_session=True)
            try:
                code=ACTIVE.wait(timeout=budget);row['terminal']='COMPLETED' if 0<=code<124 else 'INTERRUPTED';row['exit_code']=code if row['terminal']=='COMPLETED' else None
            except subprocess.TimeoutExpired:row['terminal']='TIMEOUT';terminate_child()
            except BaseException:row['terminal']='INTERRUPTED';terminate_child();raise
            finally:
                row['ended_at']=now();ACTIVE=None;stream.flush()
                row['log_sha256']=sha(log);write(out/'STAGES.json',stages)
        row['log_sha256']=sha(log);write(out/'STAGES.json',stages);text=log.read_text()
        require(row['terminal']=='COMPLETED' and row['exit_code']==expected,'Wrong terminal for '+name)
        require(all(literal in text for literal in literals),'Intended diagnostic absent for '+name)
        if expected:require(not INFRA.search(text),'Infrastructure failure is not mutation rejection')
        return text
    py=Path(sys.executable)
    run('lean-version',[lean,'--version'],'kernel/logs/lean-version.log',budget=30)
    run('verify-inputs-before',[py,'-B',science/'verify_inputs.py',kernel/'INPUT_VERIFICATION.json'],'kernel/inputs-before.log',budget=120)
    for name in ['RootImage','Availability']:
        run(name,[lean,'-j1','-o',kernel/(name+'.olean'),science/'dependencies'/(name+'.lean')],'kernel/logs/dependency-'+name+'.log')
    for name in ['CoveringPortfolio','LabelTransport','OpaqueSearch','CanonicalReplies','RandomizedFinite','RandomizedSearch','SourceCorrespondence','ExactCap','OpaqueActions','FullCommandInterface','RepairStateBridge']:
        run(name,[lean,'-j1','-o',kernel/(name+'.olean'),science/(name+'.lean')],'kernel/logs/'+name+'.log')
    for name in ['TargetCovering','TargetSearch','NegativeControls','Check']:
        run(name,[lean,'-j1','-o',kernel/(name+'.olean'),science/'tests'/(name+'.lean')],'kernel/logs/test-'+name+'.log')
    for suffix,flags in [('',[]),('_OPTIMIZED',['-O'])]:
        run('author-semantics'+suffix,[py,'-B',*flags,science/'tests/semantic_controls.py',kernel/('SEMANTIC_RESULTS'+suffix+'.json')],'kernel/author-semantics'+suffix+'.log')
    require((kernel/'SEMANTIC_RESULTS.json').read_bytes()==(kernel/'SEMANTIC_RESULTS_OPTIMIZED.json').read_bytes(),'Author optimized semantic results differ')
    def mutants(primary):
        helper=review/'check_primary_mutants.py' if primary else science/'tests/mutation_controls.py'
        directory=out/'primary-mutants' if primary else kernel/'mutants';directory.mkdir();rows=[]
        for name,filename,old,new in mutation_table(helper):
            text=(science/filename).read_text()
            require(old in text,'Original mutation no longer matches')
            if primary and name not in {'full_action_probability_deleted','full_action_cover_cap_decreased'}:require(text.count(old)==1,'Original primary mutation multiplicity differs')
            path=directory/(name+'.lean');path.write_text(text.replace(old,new,1))
            relative=(directory/(name+'.log')).relative_to(out).as_posix()
            log=run(('primary-' if primary else 'author-')+name,[lean,'-j1',path],relative,expected=1,literals=['error:'])
            if primary:require('unexpected token' not in log and 'unknown namespace' not in log,'Primary mutation failed at syntax/import boundary')
            elif name=='missing_opacity':require('application type mismatch' in log and 'invalid field notation' not in log,'Opacity mutant did not reach lost-information obligation')
            rows.append({'name':name,'exit_code':1,'result':'REJECTED','source_module':filename} if primary else {'mutation':name,'exit_code':1,'result':'rejected'})
        write(directory/'RESULTS.json' if primary else kernel/'MUTATION_RESULTS.json',{'status':'PASS','mutations':rows})
    mutants(False)
    run('verify-inputs-after',[py,'-B',science/'verify_inputs.py',kernel/'INPUT_VERIFICATION_AFTER.json'],'kernel/inputs-after.log',budget=120)
    require((kernel/'INPUT_VERIFICATION.json').read_bytes()==(kernel/'INPUT_VERIFICATION_AFTER.json').read_bytes(),'Source verification changed')
    run('independent-proofs',[lean,'-j1','-o',kernel/'IndependentChecks.olean',review/'IndependentChecks.lean'],'independent-proofs.log')
    run('all-author-axioms',[lean,'-j1',review/'AllAxioms.lean'],'all-author-axioms.log')
    mutants(True)
    for suffix,flags in [('',[]),('_OPTIMIZED',['-O'])]:
        run('review-semantics'+suffix,[py,'-B',*flags,review/'independent_semantics.py',out/('INDEPENDENT_SEMANTICS'+suffix+'.json')],'independent-semantics'+suffix+'.log')
    require((out/'INDEPENDENT_SEMANTICS.json').read_bytes()==(out/'INDEPENDENT_SEMANTICS_OPTIMIZED.json').read_bytes(),'Reviewer optimized semantic results differ')
    require((kernel/'SEMANTIC_RESULTS.json').read_bytes()==(science/'tests/SEMANTIC_RESULTS.json').read_bytes(),'Author semantic golden evidence differs')
    require((out/'INDEPENDENT_SEMANTICS.json').read_bytes()==(review/'final-replay/SEMANTICS.json').read_bytes(),'Independent semantic golden evidence differs')
    for path in list((kernel/'logs').glob('*.log'))+[out/'independent-proofs.log',out/'all-author-axioms.log']:
        text=path.read_text();require(not any(x in text for x in ['error:','warning:','sorryAx']),'Unclean successful compiler log')
        for raw in re.findall(r'depends on axioms: \[([^\]]*)\]',text):require({x.strip() for x in raw.split(',') if x.strip()}<=AXIOMS,'Unapproved axiom')
    def axiom_count(path):
        text=path.read_text();return len(re.findall(r'depends on axioms: \[',text))+text.count('does not depend on any axioms')
    author=axiom_count(out/'all-author-axioms.log');reviewer=axiom_count(out/'independent-proofs.log');expected=json.loads((review/'final-replay/FINAL_CHECKS.json').read_text())
    require(author==expected['author_declarations_axiom_checked'] and reviewer==expected['reviewer_theorems_axiom_checked'],'Original axiom readback count differs')
    require(manifest(root,'PUBLIC_MANIFEST.json')==count,'Original source changed during replay');check_dependencies()
    write(out/'PUBLIC_REPLAY_RESULT.json',{'status':'PASS','public_manifest_sha256':sha(root/'PUBLIC_MANIFEST.json'),'science_manifest_sha256':sha(science/'MANIFEST.json'),'review_receipt_sha256':sha(review/'REVIEW_RECEIPT_V2.json'),
          'public_bound_files':count,'science_bound_files':science_count,'author_declarations_axiom_checked':author,'independent_theorems_axiom_checked':reviewer,
          'author_mutations_rejected':6,'independent_primary_mutations_rejected':6,'normal_and_optimized_semantic_results_match_archived_evidence':True,
          'immutable_payload_before_after':True,'successful_compiler_logs_clean':True,'lean_sha256':tools['lean_sha256'],'mathlib_revision':tools['mathlib_revision'],
          'mathlib_source_files_verified':len(dependencies),'translation':'Source-bound shell-free serial command vectors; all 12 compiler rejections retain actual argv, terminal and logs.'})

if __name__=='__main__':main()
