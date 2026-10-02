#!/usr/bin/env python3
"""Cold suite-isolated replay. Official dependency caches are trusted; custom objects are fresh.

0 = scoped custom compilation/readbacks, 1 = failure, 2 = missing prerequisite.
Original positive/mutation controls and mathematical adoption remain separate.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

import validate_research_continuations as contract


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n',encoding='utf-8')


def verify_object(path, expected):
    contract.require(path.is_file() and not path.is_symlink() and path.stat().st_size>0,'Missing/nonregular object')
    contract.require(contract.sha(path)==expected,'Stale compiled object')


def run_process(argv, cwd, env, log, timeout):
    """Persist actual terminal output even on failure; timeout never counts as rejection."""
    clean={k:v for k,v in os.environ.items() if k not in {'LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT'}}
    try:
        process=subprocess.run(list(map(str,argv)),cwd=cwd,env={**clean,**env},capture_output=True,
                               text=True,encoding='utf-8',errors='replace',timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        output=(exc.stdout or b'')+(exc.stderr or b'')
        log.write_bytes(output if isinstance(output,bytes) else output.encode())
        raise ValueError('Process timeout; no acceptance credit') from exc
    output=process.stdout+'\n'+process.stderr
    log.write_text(output,encoding='utf-8')
    contract.require(process.returncode==0,'Nonzero process exit: '+str(process.returncode))
    contract.require(not re.search(r'\berror:|\bPANIC\b|\bsorryAx\b|declaration uses[^\n]*sorry',output),'Invalid compiler diagnostic')
    return output


def parse_readback(text, targets):
    contract.require(len(targets)==len(set(targets)) and targets,'Duplicate/empty targets')
    contract.require(not re.search(r'\berror:|\bPANIC\b|\bsorryAx\b',text),'Bad readback diagnostic')
    begins=re.findall(r'^CONTINUATION_BEGIN (\S+)\s*$',text,re.M)
    ends=re.findall(r'^CONTINUATION_END (\S+)\s*$',text,re.M)
    contract.require(begins==targets and ends==targets,'Truncated, duplicated or foreign readback')
    result={}
    for target in targets:
        pattern=r'^CONTINUATION_BEGIN '+re.escape(target)+r'\s*\n(.*?)^CONTINUATION_END '+re.escape(target)+r'\s*$'
        blocks=re.findall(pattern,text,re.M|re.S)
        contract.require(len(blocks)==1,'Missing readback block')
        block=blocks[0].strip()
        ax=re.findall(r"^'([^']+)' (does not depend on any axioms|depends on axioms:\s*\[[^\]]*\])\s*$",block,re.M)
        contract.require(len(ax)==1 and ax[0][0]==target,'Missing or wrong axiom target')
        footprint=[] if ax[0][1].startswith('does not') else [v.strip() for v in ax[0][1].split('[',1)[1][:-1].split(',') if v.strip()]
        contract.require(set(footprint)<=contract.AXIOMS,'Unapproved axiom')
        type_text=block[:block.index("'"+target+"' ")].strip()
        contract.require(re.match(r'^@?'+re.escape(target)+r'(?:\.\{[^}]*\})?\s*:',type_text),'Missing/wrong exact declaration type')
        result[target]={'type':type_text,'axioms':sorted(footprint)}
    return result


def environment(suite, lean_bin, mathlib, logs):
    lean=lean_bin/'lean'
    if not lean.is_file():raise FileNotFoundError('Official Lean executable unavailable')
    contract.require(contract.sha(lean)==suite['pins']['lean_binary_sha256'],'Official compiler digest mismatch')
    version=run_process([lean,'--version'],logs,{},logs/'compiler.log',30).strip()
    contract.require(re.search(r'version 4\.19\.0[, ]',version) and '6caaee842e94' in version,'Wrong Lean version/commit')
    libraries=[];repos={};checks=[]
    for pin in suite['pins']['packages']:
        repo=mathlib if pin['name']=='mathlib' else mathlib/'.lake/packages'/pin['name']
        if not repo.is_dir():raise FileNotFoundError('Pinned dependency unavailable: '+pin['name'])
        head=run_process(['git','rev-parse','HEAD'],repo,{},logs/(pin['name']+'-head.log'),30).strip()
        dirty=run_process(['git','status','--porcelain','--untracked-files=no'],repo,{},logs/(pin['name']+'-status.log'),30).strip()
        contract.require(head==pin['revision'] and not dirty,'Wrong/dirty dependency: '+pin['name'])
        lib=repo/'.lake/build/lib/lean'
        if lib.is_dir():libraries.append(lib.resolve())
        repos[pin['name']]=repo
        checks.append({'name':pin['name'],'revision':head,'tracked_clean':True,'build_cache_present':lib.is_dir()})
    for row in suite['official_imports']:
        if row['repository']=='lean-release':
            source=lean_bin.parent/'src/lean'/row['source']
        else:
            repo=repos[row['repository']];source=repo/row['source']
            raw=subprocess.run(['git','show','HEAD:'+row['source']],cwd=repo,capture_output=True,timeout=30)
            contract.require(raw.returncode==0 and hashlib.sha256(raw.stdout).hexdigest()==row['sha256'],'Official tracked ownership mismatch')
        contract.require(source.is_file() and contract.sha(source)==row['sha256'],'Official source changed')
        objects=[lib/(row['module'].replace('.','/')+'.olean') for lib in libraries+[lean_bin.parent/'lib/lean']]
        if not any(p.is_file() for p in objects):raise FileNotFoundError('Official object unavailable: '+row['module'])
    for lib in libraries+[lean_bin.parent/'lib/lean']:
        for row in suite['modules']:
            contract.require(not (lib/(row['module'].replace('.','/')+'.olean')).exists(),'Custom module in upstream cache')
    return lean,libraries,version,checks


def replay(root, suite_id, lean_bin, mathlib, output, timeout=300):
    root=Path(root).resolve();output=Path(output).absolute()
    contract.require(not output.exists() and not output.is_symlink(),'Output must be absent')
    contract.require(not output.resolve().is_relative_to(root),'Output must be outside repository')
    contract.validate(root)
    registry=contract.read_json(root/contract.AREA/'registry.json')
    sources=contract.indexed(contract.read_json(root/registry['source_map'])['sources'],'id')
    matches=[(root/rel,contract.read_json(root/rel)) for rel in registry['suites'] if contract.read_json(root/rel)['id']==suite_id]
    contract.require(len(matches)==1,'Unknown suite ID')
    suite_path,suite=matches[0]
    hashes={m['module']:sources[m['source_id']]['sha256'] for m in suite['modules']}
    output.mkdir(parents=True)
    logs=output/'logs';logs.mkdir()
    receipt={'status':'RUNNING','exit_code':None,'kernel_verified':False,'suite_id':suite_id,
             'runner_sha256':contract.sha(Path(__file__)),'validator_sha256':contract.sha(Path(contract.__file__)),
             'suite_sha256':contract.sha(suite_path),'source_hashes':hashes,'post_source_hashes':{},
             'pins':suite['pins'],'modules':[],'readbacks':{},'original_controls':'NOT_RUN',
             'started_utc':datetime.now(timezone.utc).isoformat(),
             'scope':'Cold custom source components and exact type/axiom readbacks; official caches trusted. No total family, runtime, empirical, normative or adoption claim.'}
    def save():write_json(output/'RECEIPT.json',receipt)
    save()
    try:
        lean,libs,version,checks=environment(suite,Path(lean_bin).resolve(),Path(mathlib).resolve(),logs)
        receipt.update(compiler_sha256=contract.sha(lean),compiler_version=version,dependency_checks=checks)
        src=output/'source';src.mkdir();build=output/'build';build.mkdir()
        env={k:v for k,v in os.environ.items() if k not in {'LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT'}}
        env.update(LEAN_PATH=os.pathsep.join(map(str,[build,*libs])),PATH=str(lean.parent)+os.pathsep+env.get('PATH',''))
        rows={r['module']:r for r in suite['modules']};fingerprints={}
        official={r['module']:r for r in suite['official_imports']}
        for name in suite['module_order']:
            row=rows[name];original=root/sources[row['source_id']]['path']
            contract.require(contract.sha(original)==hashes[name],'Source changed before staging')
            relative=Path(*name.split('.')).with_suffix('.lean')
            staged=src/relative;staged.parent.mkdir(parents=True,exist_ok=True);staged.write_bytes(original.read_bytes())
            obj=(build/relative).with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
            dependencies={d:fingerprints[d] if d in rows else official[d] for d in row['imports']}
            fp=hashlib.sha256(json.dumps({'module':name,'source':hashes[name],'dependencies':dependencies,'pins':suite['pins']},sort_keys=True).encode()).hexdigest()
            log=logs/(name+'.log')
            run_process([lean,'-j1','--root='+str(src),'-o',obj,staged],src,env,log,timeout)
            verify_object(obj,contract.sha(obj));fingerprints[name]=fp
            receipt['modules'].append({'module':name,'source_sha256':hashes[name],'object_sha256':contract.sha(obj),
                                       'transitive_source_fingerprint':fp,'status':'FRESH_COMPILE','exit_code':0,'log_sha256':contract.sha(log)})
            save();print(suite_id,name,'compiled',flush=True)
        targets=[r['name'] for r in suite['targets']]
        audit=src/'ContinuationReadback.lean'
        contract.require('ContinuationReadback' not in rows,'Readback module collision')
        audit.write_text('\n'.join('import '+m for m in suite['module_order'])+'\nset_option pp.universes true\nset_option pp.explicit true\n'+
                         ''.join(f'#eval IO.println "CONTINUATION_BEGIN {t}"\n#check @{t}\n#print axioms {t}\n#eval IO.println "CONTINUATION_END {t}"\n' for t in targets),encoding='utf-8')
        text=run_process([lean,'-j1','--root='+str(src),audit],src,env,logs/'readback.log',timeout)
        receipt['readbacks']=parse_readback(text,targets)
        receipt['readback_log_sha256']=contract.sha(logs/'readback.log')
        receipt['post_source_hashes']={m['module']:contract.sha(root/sources[m['source_id']]['path']) for m in suite['modules']}
        contract.require(hashes==receipt['post_source_hashes'] and receipt['suite_sha256']==contract.sha(suite_path),'Inputs changed during replay')
        receipt.update(status='FRESH_KERNEL_COMPONENTS',exit_code=0,kernel_verified=True)
        contract.validate_receipt(receipt,suite,suite_path,sources)
    except FileNotFoundError as exc:
        receipt.update(status='BLOCKED',exit_code=2,error=str(exc))
    except (OSError,ValueError,subprocess.SubprocessError) as exc:
        receipt.update(status='FAILED',exit_code=1,kernel_verified=False,error=str(exc))
    receipt['finished_utc']=datetime.now(timezone.utc).isoformat();save()
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--suite',required=True)
    parser.add_argument('--lean-bin',type=Path,required=True)
    parser.add_argument('--mathlib',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--timeout',type=int,default=300)
    args=parser.parse_args()
    if args.timeout<=0:parser.error('Timeout must be positive')
    try:
        result=replay(args.root,args.suite,args.lean_bin,args.mathlib,args.out,args.timeout)
        print(json.dumps({'status':result['status'],'exit_code':result['exit_code'],'kernel_verified':result['kernel_verified']}))
        raise SystemExit(result['exit_code'])
    except ValueError as exc:parser.exit(1,'REFUSED: '+str(exc)+'\n')
