#!/usr/bin/env python3
"""Bounded runner sanitation checks. Never sets loader keys on this Python host."""
from pathlib import Path
import argparse,hashlib,json,os,runpy,sys
ROOT=Path(__file__).resolve().parents[1]

def check(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    output=a.output.resolve();check(not output.exists(),'output must be absent');check(ROOT not in output.parents and output!=ROOT,'output must be outside package');output.mkdir(parents=True)
    api=runpy.run_path(str(ROOT/'replay.py'),run_name='compiler_environment_probe')
    keys=['LD_PRELOAD','LD_LIBRARY_PATH','LD_AUDIT','LD_DEBUG','LD_PROFILE','LD_TRACE_LOADED_OBJECTS','LD_FUTURE_UNKNOWN_TEST']
    hostile=dict(os.environ)
    for k in keys:hostile[k]='/nonexistent/sanitation-probe-'+k
    hostile.update(PROBE_ORDINARY='ordinary-retained',KEEP_LD_NAME='retained',LDX_NOT_PREFIX='retained',LEAN_PATH='/generated/build:/pinned/cache',PYTHONDONTWRITEBYTECODE='1')
    before=dict(hostile);clean=api['compiler_subprocess_environment'](hostile)
    check(clean is not hostile and hostile==before,'input environment was mutated')
    check(not any(k.startswith('LD_') for k in clean),'loader key escaped sanitation')
    for k,v in hostile.items():
        if not k.startswith('LD_'):check(clean.get(k)==v,'ordinary variable changed '+k)
    # Red control is in memory only: the old two-name policy leaves the future/audit overrides.
    legacy={k:v for k,v in hostile.items() if k not in ['LD_PRELOAD','LD_LIBRARY_PATH']}
    check(any(k.startswith('LD_') for k in legacy),'legacy-policy negative control became vacuous')
    code="import os,json;print(json.dumps({'loader_keys':sorted(k for k in os.environ if k.startswith('LD_')),'ordinary':{k:os.environ.get(k) for k in ['PROBE_ORDINARY','KEEP_LD_NAME','LDX_NOT_PREFIX','LEAN_PATH','PROBE_STAGE']}}))"
    stages=[]
    for stage in ['version','compile','axiom_audit']:
        incoming=dict(hostile,PROBE_STAGE=stage)
        result=api['run_compiler_stage']([sys.executable,'-c',code],incoming,output/(stage+'.log'),10)
        check(result['exit_code']==0 and not result['timed_out'],'child did not finish '+stage)
        child=json.loads(result['text']);check(child['loader_keys']==[],'loader key received '+stage)
        check(child['ordinary']=={k:incoming[k] for k in ['PROBE_ORDINARY','KEEP_LD_NAME','LDX_NOT_PREFIX','LEAN_PATH','PROBE_STAGE']},'ordinary variable lost '+stage)
        check(incoming==dict(hostile,PROBE_STAGE=stage),'runner mutated input '+stage)
        stages.append({'stage':stage,'exit_code':result['exit_code'],'received':child})
    import ast
    tree=ast.parse((ROOT/'replay.py').read_text());main_fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    calls=[n for n in ast.walk(main_fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='run_compiler_stage']
    check(len(calls)==3 and all(len(c.args)>=2 and isinstance(c.args[1],ast.Name) and c.args[1].id=='env' for c in calls),'version/compile/audit propagation changed')
    receipt={'status':'PASS_BOUNDED_COMPILER_ENVIRONMENT_CHECKS','wrapper_sha256':hashlib.sha256((ROOT/'replay.py').read_bytes()).hexdigest(),'test_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'tested_loader_keys':keys,'input_mapping_unchanged':True,'ordinary_variables_retained':True,'legacy_two_name_policy_rejected_in_memory':True,'main_runner_stage_call_sites':len(calls),'stages':stages,'scope':'Sanitizes compiler subprocess copies only; no claim about an already-started Python launcher or compromised host.'}
    (output/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
