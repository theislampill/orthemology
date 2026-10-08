#!/usr/bin/env python3
"""Portable, fail-closed evidence replay. Python standard library only.

No downloads, installs, source edits, retained custom objects, or hidden workspace
paths. All newly produced artifacts go to a previously absent output directory.
"""
from pathlib import Path, PurePosixPath
import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time

EXTERNAL_ROOTS = {'Mathlib','Lean','Init','Std','Batteries','Aesop','Qq',
                  'Plausible','ProofWidgets','ImportGraph','LeanSearchClient'}
ALLOWED_AXIOMS = {'propext','Classical.choice','Quot.sound'}
BAD_DIAGNOSTICS = ('unknown identifier','unknown constant','unknown module',
    'unknown namespace','unexpected token','failed to synthesize','Reduction got stuck',
    'maximum recursion depth','maximum number of heartbeats','timeout','timed out',
    'object file','no such file','expected type must not contain meta variables')


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def confined(root,relative):
    root=Path(root).resolve()
    if not isinstance(relative,str) or not relative or '\\' in relative:
        raise ValueError('Invalid relative path')
    pure=PurePosixPath(relative)
    if pure.is_absolute() or '..' in pure.parts or relative in ('.',''):
        raise ValueError('Unsafe relative path: '+relative)
    path=root.joinpath(*pure.parts)
    if not path.resolve().is_relative_to(root):raise ValueError('Path escapes root: '+relative)
    return path


def verify_manifest(root):
    root=Path(root).resolve(); data=read_json(root/'MANIFEST.json'); expected=set()
    for row in data['files']:
        rel=row['path']
        if rel in expected:raise ValueError('Duplicate manifest entry: '+rel)
        expected.add(rel);p=confined(root,rel)
        if p.is_symlink() or not p.is_file():raise ValueError('Missing or symlink file: '+rel)
        if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:
            raise ValueError('Manifest identity mismatch: '+rel)
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('Symlink in package: '+str(p.relative_to(root)))
        if p.is_file() and p != root/'MANIFEST.json':actual.add(p.relative_to(root).as_posix())
    if actual!=expected:raise ValueError('Manifest set mismatch: missing='+repr(sorted(expected-actual))+' extra='+repr(sorted(actual-expected)))
    return {'status':'PASS_PACKAGE_MANIFEST','files_verified':len(expected),'manifest_sha256':sha(root/'MANIFEST.json')}


def source_order(nodes):
    order=[];seen=set();active=set()
    def visit(name):
        if name in active:raise ValueError('Cyclic custom import: '+name)
        if name in seen:return
        if name not in nodes:
            if name.split('.')[0] not in EXTERNAL_ROOTS:raise ValueError('Missing custom import: '+name)
            return
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*',name):
            raise ValueError('Invalid module name: '+name)
        active.add(name)
        for dep in nodes[name]['imports']:visit(dep)
        active.remove(name);seen.add(name);order.append(name)
    for name in nodes:visit(name)
    return order


def qualified_output(code,text,rule):
    if code!=rule.get('expected_exit',0):return False
    if 'sorryAx' in text or "declaration uses 'sorry'" in text:return False
    if rule.get('expected_exit',0)==0:return True
    if code!=1 or any(s.lower() in text.lower() for s in BAD_DIAGNOSTICS):return False
    errors=re.findall(r'error: ([^\n]*)',text)
    allowed=("unsolved goals","type mismatch","tactic 'decide' proved that the proposition")
    if not errors or not all(any(error.startswith(prefix) for prefix in allowed) for error in errors):return False
    markers=rule.get('markers',[])
    return bool(markers) and all(marker in text for marker in markers) and 'error:' in text


def audit_axioms(text,expected):
    rows=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",text,re.S)
    if len(rows)!=expected:raise ValueError(f'Axiom audit count {len(rows)} != {expected}')
    out={}
    for name,axioms in rows:
        names={x.strip() for x in axioms.split(',') if x.strip()}
        if not names<=ALLOWED_AXIOMS:raise ValueError('Unapproved axiom for '+name+': '+repr(names))
        if name in out:raise ValueError('Duplicate audited declaration '+name)
        out[name]=sorted(names)
    return out


def make_output(package,output):
    package=Path(package).resolve();output=Path(output).resolve()
    if output.is_relative_to(package):raise ValueError('Output must be outside the evidence package')
    if output.exists():raise ValueError('Output must not already exist: '+str(output))
    output.mkdir(parents=True)
    return output


def clean_environment(environ):
    blocked={'PYTHONPATH','PYTHONHOME','PYTHONOPTIMIZE','PYTHONUSERBASE','LD_PRELOAD','LD_LIBRARY_PATH'}
    env={k:v for k,v in environ.items() if not k.startswith('LEAN_') and k not in blocked}
    env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONNOUSERSITE']='1';env['GIT_OPTIONAL_LOCKS']='0'
    return env


def verify_objects(root,files,packages):
    root=Path(root).resolve();expected=set();total=0
    package_set=set(packages)
    if len(package_set)!=len(packages):raise ValueError('Duplicate dependency package')
    for row in files:
        if row['package'] not in package_set:raise ValueError('Unspecified dependency package')
        cache=confined(root,row['package']+'/.lake/build/lib/lean')
        p=confined(cache,row['path']);key=(row['package'],row['path'])
        if key in expected:raise ValueError('Duplicate dependency object')
        expected.add(key)
        if p.is_symlink() or not p.is_file():raise ValueError('Missing or symlink dependency object: '+str(key))
        if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:raise ValueError('Dependency object mismatch: '+str(key))
        total+=row['bytes']
    actual=set()
    for package in packages:
        cache=confined(root,package+'/.lake/build/lib/lean')
        if cache.exists():
            for p in cache.rglob('*.olean'):
                if p.is_symlink():raise ValueError('Symlink dependency object')
                actual.add((package,p.relative_to(cache).as_posix()))
    if actual!=expected:raise ValueError('External object set differs: missing='+str(len(expected-actual))+' extra='+str(len(actual-expected)))
    return {'object_count':len(expected),'bytes':total,'exact_olean_set':True}


def verify_environment(package,config,lane):
    toolchain=read_json(package/'dependencies/TOOLCHAIN.json')
    lean=Path(config['lean']).expanduser().resolve()
    if not lean.is_file() or sha(lean)!=toolchain['lean_sha256']:raise ValueError('Lean executable digest mismatch')
    root=Path(config['dependency_roots'][lane]).expanduser().resolve()
    inventory=read_json(package/'dependencies'/f'{lane}.json')
    env=clean_environment(os.environ);packages=inventory['packages'];names=[p['name'] for p in packages]
    checked=[]
    for item in packages:
        p=confined(root,item['name'])
        got=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],env=env,text=True).strip()
        if got!=item['revision']:raise ValueError('Dependency revision mismatch: '+item['name'])
        dirty=subprocess.check_output(['git','-C',str(p),'status','--porcelain','--untracked-files=no'],env=env,text=True)
        if dirty:raise ValueError('Tracked dependency edits: '+item['name'])
        checked.append({'name':item['name'],'revision':got,'tracked_clean':True})
    objects=verify_objects(root,inventory['files'],names)
    paths=[confined(root,name+'/.lake/build/lib/lean') for name in names]
    return lean,paths,{'lean_sha256':sha(lean),'packages':checked,**objects,'inventory_sha256':sha(package/'dependencies'/f'{lane}.json'),'cold_dependency_build':False}


def run_command(command,cwd,env,log,timeout):
    started=time.monotonic()
    try:
        p=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        code=p.returncode;output=p.stdout
    except subprocess.TimeoutExpired as e:
        code=124;output=(e.stdout or b'')+b'\nREPLAY TIMEOUT: execution error, never mathematical negative evidence.\n'
    Path(log).write_bytes(output)
    return code,output.decode('utf-8',errors='replace'),round(time.monotonic()-started,3)


def replay_lean(package,config,lane,out):
    if not re.fullmatch(r'[a-z][a-z0-9-]*',lane):raise ValueError('Invalid lane identifier')
    plan=read_json(package/'lean'/lane/'REPLAY_PLAN.json')
    for row in plan['controls']:
        if not isinstance(row['group'],str) or not re.fullmatch(r'[a-z][a-z0-9-]*',row['group']):
            raise ValueError('Invalid control group identifier')
        if not isinstance(row['module'],str) or not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*',row['module']):
            raise ValueError('Invalid control module identifier')
    lean,external,env_receipt=verify_environment(package,config,lane)
    work=out/lane;work.mkdir();sources=work/'sources';sources.mkdir();build=work/'build';build.mkdir();logs=work/'logs';logs.mkdir()
    result={'status':'RUNNING','lane':lane,'environment':env_receipt,'custom_objects_reused':False,'runs':[],'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    def save():write_json(work/'RESULT.json',result)
    save();nodes=plan['modules'];order=source_order(nodes)
    for name,row in nodes.items():
        source=confined(package,row['path'])
        if not source.is_file() or sha(source)!=row['sha256']:raise ValueError('Required source missing or changed: '+name)
        actual=[m for line in source.read_text(encoding='utf-8').splitlines() if line.startswith('import ') for m in line.split()[1:]]
        if actual!=row['imports']:raise ValueError('Import binding mismatch: '+name)
        dst=confined(sources,name.replace('.','/')+'.lean');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dst)
    timeout=config.get('module_timeout_seconds',600)
    if not isinstance(timeout,int) or isinstance(timeout,bool) or not 1<=timeout<=7200:raise ValueError('Module timeout must be 1..7200 seconds')
    def compile_one(name,source,srcroot,objroot,rule,group):
        obj=confined(objroot,name.replace('.','/')+'.olean');obj.parent.mkdir(parents=True,exist_ok=True)
        if obj.exists():raise ValueError('Object target unexpectedly exists: '+str(obj))
        env=clean_environment(os.environ);env['LEAN_PATH']=os.pathsep.join(map(str,[objroot,build]+external));env['LEAN_NUM_THREADS']='1'
        log=confined(logs,group+'__'+name.replace('.','_')+'.log')
        if log.exists():raise ValueError('Duplicate replay log '+str(log))
        cmd=[str(lean),'-j1','--root='+str(srcroot),'-o',str(obj),str(source)]
        code,text,elapsed=run_command(cmd,work,env,log,timeout)
        okay=qualified_output(code,text,rule)
        rec={'module':name,'group':group,'source':str(source.relative_to(work)),'source_sha256':sha(source),'command':cmd,'LEAN_PATH':env['LEAN_PATH'],'exit_code':code,'expected_exit':rule.get('expected_exit',0),'markers':rule.get('markers',[]),'elapsed_seconds':elapsed,'log':str(log.relative_to(work)),'log_sha256':sha(log),'qualified':okay}
        if code==0:
            if not obj.is_file():okay=False;rec['qualified']=False
            else:rec['object_sha256']=sha(obj)
        if okay and 'axiom_count' in rule:
            try:rec['axiom_audits']=audit_axioms(text,rule['axiom_count'])
            except ValueError as e:rec['qualification_error']=str(e);okay=False;rec['qualified']=False
        result['runs'].append(rec);save()
        print(lane,group,name,code,'PASS' if okay else 'FAIL',elapsed,flush=True)
        if not okay:
            result['status']='FAIL';save();raise ValueError('Unqualified compilation: '+group+'/'+name+'; see '+str(log))
    try:
        for name in order:compile_one(name,confined(sources,name.replace('.','/')+'.lean'),sources,build,{'expected_exit':0},'production')
        groups={}
        for row in plan['controls']:groups.setdefault(row['group'],[]).append(row)
        for group,controls in groups.items():
            controlroot=confined(work,'controls/'+group);controlsrc=controlroot/'sources';controlsrc.mkdir(parents=True);controlbuild=controlroot/'build';controlbuild.mkdir()
            for row in controls:
                source=confined(package,row['path'])
                if not source.is_file() or sha(source)!=row['sha256']:raise ValueError('Required control missing or changed: '+row['module'])
                dst=confined(controlsrc,row['module'].replace('.','/')+'.lean');dst.parent.mkdir(parents=True,exist_ok=True)
                if dst.exists():raise ValueError('Duplicate control module: '+row['module'])
                shutil.copyfile(source,dst)
                compile_one(row['module'],dst,controlsrc,controlbuild,row,group)
        if 'ordinary_diagnostic' in plan:
            diag=plan['ordinary_diagnostic'];d=work/'ordinary-diagnostic';d.mkdir()
            script=confined(package,diag['script']);target=d/script.name;shutil.copyfile(script,target)
            export=logs/(diag['export_group']+'__'+diag['export_module']+'.log')
            shutil.copyfile(export,d/'DumpExactPolynomials.log')
            log=d/'diagnostic.log';cmd=[sys.executable,'-E','-S','-B',str(target)]
            code,text,elapsed=run_command(cmd,d,clean_environment(os.environ),log,120)
            result['ordinary_diagnostic']={'scope':diag['scope'],'exit_code':code,'elapsed_seconds':elapsed,'script_sha256':sha(script),'export_sha256':sha(export),'log_sha256':sha(log)}
            save()
            if code!=0:raise ValueError('Ordinary diagnostic failed; see '+str(log))
            result['ordinary_diagnostic']['result']=read_json(d/'LAMBDA_NORMAL_FORM_CHECK.json')
        for name,row in nodes.items():
            if sha(confined(package,row['path']))!=row['sha256']:raise ValueError('Source changed during replay: '+name)
        result['status']='PASS_FRESH_CUSTOM_SOURCES_AND_SELECTED_CONTROLS';result['production_modules']=len(order);result['selected_control_files']=len(plan['controls']);result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
        return result
    except BaseException as e:
        if result['status']=='RUNNING':result['status']='ERROR';result['error']=str(e);save()
        raise


def replay_python(package,out,full):
    work=out/'python';work.mkdir();inputs=work/'input';inputs.mkdir();shutil.copytree(package/'tranche18',inputs/'tranche18')
    logs=work/'logs';logs.mkdir();env=clean_environment(os.environ)
    hc=inputs/'tranche18/research/hidden-change';reviews=inputs/'tranche18/reviews'
    commands=[('reference-author',hc/'reference-v1',['-m','unittest','discover','-v']),('efficient-author',hc/'efficient-v1',['-m','unittest','discover','-v']),('reference-independent',reviews/'hidden-change-reference',['test_reference_independent.py']),('efficient-independent',reviews/'hidden-change-efficient',['test_efficient_independent.py']),('efficient-protected-paths',reviews/'hidden-change-efficient',['test_production_paths.py']),('efficient-prior-controls',reviews/'hidden-change-efficient',['replay_previous_adversarial.py'])]
    if full:
        commands.extend((name,reviews/folder,[script]) for name,folder,script in [('reference-census','hidden-change-reference','run_census.py'),('reference-extended-census','hidden-change-reference','run_extended_census.py'),('efficient-census','hidden-change-efficient','run_campaign.py'),('efficient-extra-end-to-end','hidden-change-efficient','run_extra_end_to_end.py'),('efficient-forged-negatives','hidden-change-efficient','run_negative_campaign.py')])
    pins={p.relative_to(inputs).as_posix():sha(p) for p in inputs.rglob('*') if p.is_file()}
    result={'status':'RUNNING','python':sys.version,'platform':platform.platform(),'full_campaigns':full,'source_copies_exact':True,'runs':[]}
    def save():write_json(work/'RESULT.json',result)
    save()
    for label,cwd,args in commands:
        cmd=[sys.executable,'-E','-S','-B']+args;log=logs/(label+'.log');code,text,elapsed=run_command(cmd,cwd,env,log,1800)
        rec={'label':label,'command':cmd,'cwd':str(cwd.relative_to(work)),'exit_code':code,'elapsed_seconds':elapsed,'log':str(log.relative_to(work)),'log_sha256':sha(log)}
        result['runs'].append(rec);save();print(label,code,elapsed,flush=True)
        if code!=0:result['status']='FAIL';save();raise ValueError('Python replay failed: '+label+'; see '+str(log))
    for rel,digest in pins.items():
        if sha(confined(inputs,rel))!=digest:raise ValueError('Copied Python source changed: '+rel)
    result['status']='PASS_PYTHON_SUITES'+('_AND_FULL_CAMPAIGNS' if full else '');result['source_unchanged_after']=True;save();return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['verify','python','python-full','lean-hidden','lean-hase','all'])
    parser.add_argument('--environment',type=Path,help='Explicit local environment JSON; only needed for Lean')
    parser.add_argument('--output',type=Path,help='Previously absent output directory outside this package')
    args=parser.parse_args(argv);package=Path(__file__).resolve().parent
    if not sys.flags.ignore_environment:raise ValueError('Run with -E to ignore ambient Python variables at entry')
    if not sys.flags.no_site:raise ValueError('Run with -S to disable Python site and customization startup')
    if sys.flags.optimize:raise ValueError('Run without -O or -OO; evidence scripts contain assertions')
    verification=verify_manifest(package)
    if args.action=='verify':print(json.dumps(verification,indent=2));return 0
    if args.output is None:parser.error('--output is required for a replay')
    needs_lean=args.action in ('lean-hidden','lean-hase','all')
    if needs_lean and args.environment is None:parser.error('--environment is required for Lean replay')
    config=read_json(args.environment.resolve()) if needs_lean else None
    out=make_output(package,args.output);write_json(out/'PACKAGE_VERIFICATION.json',verification)
    summary={'status':'RUNNING','action':args.action,'runner_sha256':sha(Path(__file__)),'runs':[]}
    write_json(out/'RESULT.json',summary)
    try:
        if args.action in ('python','python-full','all'):summary['runs'].append(replay_python(package,out,args.action!='python'))
        if args.action in ('lean-hidden','all'):summary['runs'].append(replay_lean(package,config,'hidden-change',out))
        if args.action in ('lean-hase','all'):summary['runs'].append(replay_lean(package,config,'hase',out))
        summary['package_unchanged_after']=verify_manifest(package);summary['status']='PASS_REQUESTED_REPLAY'
        write_json(out/'RESULT.json',summary);print(summary['status']);return 0
    except BaseException as e:
        summary['status']='ERROR_OR_FAILED_REPLAY';summary['error']=str(e);write_json(out/'RESULT.json',summary);raise

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,KeyError,OSError,subprocess.SubprocessError) as e:
        print('REPLAY ERROR:',e,file=sys.stderr);raise SystemExit(1)
