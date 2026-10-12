#!/usr/bin/env python3
"""Fail-closed, exact-pin *external* qualification of this P01 candidate packet.

No network or repository effects without --acquire; all writes are in --work.
The driver trusts the selected compiler, OS and filesystem. Policy unit tests,
static inventories and existing mapped-native logs never confer new kernel credit.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from canonical_gate import (GateError, APPROVED_AXIOMS, check_artifact,
                            enforce_version, parse_audit, strict_json,
                            run_bounded)

PIN='leanprover/lean4:v4.19.0'
LEAN_COMMIT='6caaee842e94'
MATHLIB='c44e0c8ee63ca166450922a373c7409c5d26b00b'


def H(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def need(c: bool, why: str) -> None:
    if not c:
        raise GateError(why)


def guard_version(text: str) -> None:
    enforce_version('4.19.0',text)
    need(re.search(r'\bcommit\s+'+LEAN_COMMIT+r'[0-9a-f]*(?:,|\s|\))',text) is not None,
         'wrong or missing Lean commit identity')


def code_only(text: str) -> str:
    """Remove nested comments/string contents, retaining line numbers.

    A conservative hygiene lexer, not a Lean parser or proof verifier.
    """
    out=[];i=0;depth=0;quoted=False
    while i<len(text):
        c=text[i];two=text[i:i+2]
        if depth:
            if two=='/-':depth+=1;out.extend('  ');i+=2
            elif two=='-/':depth-=1;out.extend('  ');i+=2
            else:out.append('\n' if c=='\n' else ' ');i+=1
        elif quoted:
            if c=='\\':
                need(i+1<len(text),'unterminated string escape')
                out.extend('  ');i+=2
            elif c=='"':quoted=False;out.append(' ');i+=1
            else:out.append('\n' if c=='\n' else ' ');i+=1
        elif two=='/-':depth=1;out.extend('  ');i+=2
        elif two=='--':
            j=text.find('\n',i)
            if j<0:j=len(text)
            out.extend(' '*(j-i));i=j
        elif c=='"':quoted=True;out.append(' ');i+=1
        else:out.append(c);i+=1
    need(depth==0 and not quoted,'unclosed source comment/string')
    return ''.join(out)


def source_lint(text: str) -> None:
    code=code_only(text)
    need(re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',code) is None,
         'unapproved proof placeholder/axiom/unsafe/native_decide token')
    pairs={'(':')','[':']','{':'}'};stack=[]
    for c in code:
        if c in pairs:stack.append(pairs[c])
        elif c in pairs.values():
            need(bool(stack) and stack.pop()==c,'unbalanced source delimiter')
    need(not stack,'unclosed source delimiter')


def validate_inventory(packet: Path) -> dict:
    inv=strict_json(packet/'formal'/'SOURCE_INVENTORY.json')
    need(inv.get('lean_pin')==PIN and inv.get('mathlib_commit')==MATHLIB,'wrong inventory pin')
    listed=set()
    for row in inv['files']:
        rel=row['path'];p=Path(rel)
        need(not p.is_absolute() and '..' not in p.parts and '\\' not in rel,'unsafe inventory path')
        need(rel not in listed,'duplicate source inventory member')
        listed.add(rel);src=packet/rel
        need(src.is_file() and not src.is_symlink(),'missing/nonregular source: '+rel)
        b=src.read_bytes()
        need(len(b)==row['bytes'] and H(b)==row['sha256'],'source identity mismatch: '+rel)
        if row.get('kind')=='new_candidate':source_lint(b.decode())
    actual={p.relative_to(packet).as_posix() for p in (packet/'formal').rglob('*')
            if p.is_file() and (p.suffix=='.lean' or p.name in ('lean-toolchain','lake-manifest.json'))}
    need(actual==listed,'formal source inventory coverage mismatch')
    names=[r['name'] for r in inv['targets']]
    need(names and len(names)==len(set(names)),'empty/duplicate target inventory')
    need(all(re.fullmatch(r'[A-Za-z][A-Za-z0-9_.]*',n) for n in names),'unsafe audit target')
    need((packet/'formal'/'lean-toolchain').read_text().strip()==PIN,'pin file differs')
    return inv


def run_command(out: Path,label: str,cmd: list[str],cwd: Path,env: dict|None=None,
                timeout: float=300) -> dict:
    record=run_bounded(cmd,cwd,env=env,timeout=timeout,output_limit=32*1024*1024)
    out.mkdir(parents=True,exist_ok=True)
    row={k:v for k,v in record.items() if k not in ('stdout','stderr')}
    for stream in ('stdout','stderr'):
        b=record.get(stream,'').encode();(out/(label+'.'+stream)).write_bytes(b)
        row[stream]={'path':label+'.'+stream,'bytes':len(b),'sha256':H(b)}
    (out/(label+'.json')).write_text(json.dumps(row,indent=2)+'\n')
    return record


def git_read(repo: Path,args: list[str]) -> str:
    p=subprocess.run(['git','-C',str(repo),*args],capture_output=True,timeout=30)
    need(p.returncode==0,'dependency git read failed: '+str(repo)+': '+p.stderr.decode(errors='replace'))
    return p.stdout.decode().strip()


def verify_dependencies(project: Path,lock: dict) -> list[dict]:
    result=[]
    for p in lock['packages']:
        d=project/'.lake'/'packages'/p['name']
        need(d.is_dir(),'missing dependency '+p['name'])
        head=git_read(d,['rev-parse','HEAD'])
        need(head==p['rev'],'wrong dependency revision: '+p['name'])
        need(not git_read(d,['status','--porcelain','--untracked-files=no']),
             'tracked dependency modification: '+p['name'])
        result.append({'name':p['name'],'revision':head,'tracked_clean':True})
    need(next(p['rev'] for p in lock['packages'] if p['name']=='mathlib')==MATHLIB,
         'wrong locked Mathlib')
    return result


def qualify(packet: Path,work: Path,dependency: Path|None,acquire: bool) -> dict:
    packet=packet.resolve();work=work.resolve()
    need(work!=packet and packet not in work.parents,'work must be outside sealed packet')
    need(not work.exists() or (work.is_dir() and not any(work.iterdir())),'work is not fresh/empty')
    work.mkdir(parents=True,exist_ok=True)
    evidence=work/'evidence';evidence.mkdir()
    report={'schema':'p01-external-formal-qualification-v1','status':'NOT_QUALIFIED',
            'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'pin':PIN,'lean_commit_prefix':LEAN_COMMIT,'mathlib_commit':MATHLIB,
            'kernel_credit':False,'compiled_artifacts':[], 'declarations':{},
            'environment':{'platform':sys.platform,'python':sys.version,
                           'PATH':os.environ.get('PATH',''),'ELAN_HOME':os.environ.get('ELAN_HOME')},
            'effects':'isolated work only','external_review_credit':False}
    try:
        inv=validate_inventory(packet)
        report['source_inventory_sha256']=H((packet/'formal'/'SOURCE_INVENTORY.json').read_bytes())
        project=work/'project';project.mkdir()
        for row in inv['files']:
            src=packet/row['path'];name=src.name
            dest=project/name
            need(not dest.exists(),'duplicate flattened source filename: '+name)
            shutil.copyfile(src,dest)
        lean=shutil.which('lean');lake=shutil.which('lake')
        report['executables']={'lean':lean,'lake':lake}
        if not lean or not lake:
            report['status']='HOST_EXECUTION_BLOCKED'
            report['reason']='Exact Lean/Lake executables absent from PATH after packet-recorded acquisition attempts.'
            return report
        for name,path in [('lean',lean),('lake',lake)]:
            real=Path(path).resolve()
            report.setdefault('executable_identities',{})[name]={'resolved':str(real),**check_artifact(real)}
        r=run_command(evidence,'lean-version',[lean,'--version'],project,timeout=90)
        need(r['ok'],'Lean version command failed')
        guard_version(r['stdout'])
        r=run_command(evidence,'lake-version',[lake,'--version'],project,timeout=90)
        need(r['ok'] and re.search(r'\b5\.0\.0-6caaee8\b',r['stdout']) is not None,'wrong Lake identity')
        lock=strict_json(project/'lake-manifest.json')
        if dependency is not None:
            dep=dependency.resolve()
            report['dependency_readback']=verify_dependencies(dep,lock)
            (project/'.lake').mkdir(exist_ok=True)
            (project/'.lake'/'packages').mkdir()
            for package in lock['packages']:
                name = package['name']
                shutil.copytree((dep/'.lake'/'packages'/name).resolve(),
                                project/'.lake'/'packages'/name, symlinks=True)
        elif acquire:
            # Lake consumes the shipped exact lock. Never use `lake update` to float it.
            r=run_command(evidence,'dependencies',[lake,'exe','cache','get'],project,timeout=1800)
            need(r['ok'],'exact locked dependency/cache acquisition failed')
        else:
            raise GateError('Supply --dependency-project with exact cached packages or explicit --acquire.')
        observed_lock=strict_json(project/'lake-manifest.json')
        expected={(p['name'],p['rev']) for p in lock['packages']}
        need({(p['name'],p['rev']) for p in observed_lock['packages']}==expected,'dependency lock changed')
        report['dependency_readback']=verify_dependencies(project,lock)
        artifacts=project/'.lake'/'build'/'lib'/'lean';artifacts.mkdir(parents=True,exist_ok=True)
        env=dict(os.environ);env['LEAN_PATH']=str(artifacts)
        for module in inv['build_order']:
            target=artifacts/(module+'.olean')
            need(not target.exists(),'stale output before compilation: '+module)
            r=run_command(evidence,'build-'+module,[lake,'env','lean','-j1','-o',str(target),module+'.lean'],project,env)
            need(r['ok'],'compilation failed: '+module)
            need(not re.search(r'\bsorry\b|sorryAx|declaration uses',r['stdout']+r['stderr']),
                 'proof-placeholder diagnostic: '+module)
            report['compiled_artifacts'].append({'module':module,'path':str(target.relative_to(work)),**check_artifact(target)})
        audit_target=artifacts/'P01Audit.olean'
        r=run_command(evidence,'declaration-type-axiom-audit',
                      [lake,'env','lean','-j1','-o',str(audit_target),'P01Audit.lean'],project,env,timeout=900)
        need(r['ok'],'actual declaration audit compilation failed')
        report['compiled_artifacts'].append({'module':'P01Audit','path':str(audit_target.relative_to(work)),**check_artifact(audit_target)})
        report['declarations']=parse_audit(r['stdout'],[t['name'] for t in inv['targets']])
        need(not r['stderr'].strip(),'unexpected audit stderr requires review')
        report['axiom_union']=sorted({a for d in report['declarations'].values() for a in d['axioms']})
        need(set(report['axiom_union'])<=APPROVED_AXIOMS,'axiom policy failure')
        # Bind the outputs to the exact prebuild source bytes, not a changed workspace.
        for row in inv['files']:
            need(H((project/Path(row['path']).name).read_bytes())==row['sha256'],'source changed during qualification')
        report.update(status='KERNEL_VERIFIED_EXACT_PIN_SCOPED_TARGETS',kernel_credit=True,
                      target_count=len(report['declarations']))
    except (GateError,OSError,ValueError,subprocess.SubprocessError) as e:
        report['status']='QUALIFICATION_FAILED';report['reason']=f'{type(e).__name__}: {e}'
        report['kernel_credit']=False
    finally:
        report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (work/'QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--work',type=Path,required=True)
    g=p.add_mutually_exclusive_group();g.add_argument('--dependency-project',type=Path);g.add_argument('--acquire',action='store_true')
    a=p.parse_args()
    try:report=qualify(a.packet,a.work,a.dependency_project,a.acquire)
    except (GateError,OSError) as e:
        print(json.dumps({'status':'REFUSED','reason':str(e),'kernel_credit':False}));return 2
    print(json.dumps(report,indent=2))
    return 0 if report['kernel_credit'] else 3 if report['status']=='HOST_EXECUTION_BLOCKED' else 1

if __name__=='__main__':raise SystemExit(main())
