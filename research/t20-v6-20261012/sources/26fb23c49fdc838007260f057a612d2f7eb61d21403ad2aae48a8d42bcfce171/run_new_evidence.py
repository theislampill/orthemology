"""Run only new attempt-0002 tests and mutation controls; no predecessor census replay."""
from pathlib import Path
import subprocess,sys,json,hashlib,shutil,tempfile,time,os
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def record(label,cmd,cwd):
    target=ROOT/'evidence'/label;target.mkdir(parents=True,exist_ok=True)
    start=time.time();p=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=40)
    (target/'stdout.bin').write_bytes(p.stdout);(target/'stderr.bin').write_bytes(p.stderr)
    meta={'command':cmd,'cwd':str(cwd),'exit':p.returncode,'elapsed_seconds':time.time()-start,
          'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),
          'python':sys.version,'source_sha256':{str(x.relative_to(cwd)):sha(x.read_bytes()) for d in ('code','tests') for x in (cwd/d).glob('*.py')}}
    (target/'COMMAND.json').write_text(json.dumps(meta,indent=2));print(label,p.returncode)
    return p.returncode
if __name__=='__main__':
    for label,args in [('FINAL_NORMAL',[]),('FINAL_OPTIMISED',['-O'])]:
        if record(label,[sys.executable,*args,'-m','unittest','discover','-s','tests','-v'],ROOT)!=0:raise SystemExit('New suite failed')
    if record('FINAL_DIRECT',[sys.executable,'tests/test_new_research.py','-v'],ROOT)!=0:raise SystemExit('Direct discovery failed')
    muts=[
      ('RESET_OMITTED','prcodec.py',"return Seq(*(Set(r,C(0)) for r in m.values()),","return Seq(",'CodecTests.test_local_reset_on_repeated_inline'),
      ('Q8_SNAPSHOT_WRONG','prcodec.py',"Seq(Set(oldpc,V(pc)),*cases)","Seq(Set(oldpc,C(0)),*cases)",'CompilerTests.test_q8_bounded_machine_compiler'),
      ('SELECTOR_OFFSET','prcodec.py',"Set(stage,E('sub',E('sub',V(0),V(sel)),C(1)))","Set(stage,E('sub',V(0),V(sel)))",'CompilerTests.test_pi3_compilation'),
      ('SHIFT_TAIL_WRONG','prcodec.py',"E('mod',V(1),E('pow2',V(tail_len)))","E('mod',V(1),E('pow2',E('add',V(tail_len),C(1))))",'CompilerTests.test_rational_shift_compilation'),
      ('RESOURCE_AS_ZERO','prcodec.py',None,"\n_original_run=run\ndef run(*args,**kwargs):\n    try:return _original_run(*args,**kwargs)\n    except ResourceLimit:return 0\n",'CodecTests.test_invalid_is_zero_resource_is_not'),
      ('FLOW_CHECKER_ALWAYS_TRUE','flow_solver.py',None,"\n_original_verify=verify\ndef verify(*args,**kwargs):return True\n",'FlowTests.test_exact_data_and_infeasibility')]
    results=[]
    for name,fn,before,after,test in muts:
        with tempfile.TemporaryDirectory(prefix='p02_mutation_') as td:
            temp=Path(td)
            for d in ('code','tests'):shutil.copytree(ROOT/d,temp/d,ignore=shutil.ignore_patterns('__pycache__'))
            p=temp/'code'/fn;b=p.read_bytes();text=b.decode()
            if before is None:text+=after
            else:
                if text.count(before)!=1:raise ValueError((name,text.count(before)))
                text=text.replace(before,after)
            p.write_text(text)
            # -m unittest resolves the real independent test class from the tests directory.
            envtest='test_new_research.'+test
            runner="import sys,unittest,json;sys.path.insert(0,'tests');s=unittest.defaultTestLoader.loadTestsFromName("+repr(envtest)+");r=unittest.TextTestRunner(verbosity=2).run(s);print(json.dumps(dict(tests_run=r.testsRun,failures=len(r.failures),errors=len(r.errors),success=r.wasSuccessful())));sys.exit(not r.wasSuccessful())"
            cmd=[sys.executable,'-c',runner]
            base_rc=record('BASELINE_'+name,cmd,ROOT)
            base=json.loads((ROOT/'evidence'/('BASELINE_'+name)/'stdout.bin').read_text())
            if base_rc!=0 or base!={'tests_run':1,'failures':0,'errors':0,'success':True}:raise SystemExit('Invalid baseline: '+name)
            rc=record('MUTANT_'+name,cmd,temp)
            got=json.loads((ROOT/'evidence'/('MUTANT_'+name)/'stdout.bin').read_text())
            detected=rc!=0 and got['tests_run']==1 and got['failures']>=1 and got['errors']==0
            row={'id':name,'test':test,'original_sha256':sha(b),'mutant_sha256':sha(p.read_bytes()),'before':before,'after':after,'exit':rc,'result':got,'detected':detected}
            results.append(row)
            (ROOT/'evidence/MUTATION_RESULTS.json').write_text(json.dumps(results,indent=2))
            if not detected:raise SystemExit('Invalid or surviving mutant: '+name)
    (ROOT/'evidence/MUTATION_RESULTS.json').write_text(json.dumps(results,indent=2))
    if record('FINAL_POST_MUTATION',[sys.executable,'-m','unittest','discover','-s','tests','-v'],ROOT)!=0:raise SystemExit('Post-mutation suite failed')
