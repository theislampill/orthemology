#!/usr/bin/env python3
"""Exact-pin external proof-candidate execution. NEVER treats this as adoption.
Usage: python handoff/execute_formal.py /absolute/new/workspace --acquire
       python handoff/execute_formal.py /absolute/new/workspace --offline-deps /cache/.lake/packages
Requires an installed exact Lean 4.19.0 toolchain (Elan or direct binaries).
"""
from __future__ import annotations
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
EXPECTED_LEAN='4.19.0';EXPECTED_COMMIT='6caaee8';ALLOWED={'propext','Quot.sound','Classical.choice'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require_version(lean,lake):
    if not re.search(r'\bversion 4\.19\.0\b',lean) or EXPECTED_COMMIT not in lean:raise ValueError('Wrong/unbound Lean version')
    if '5.0.0-6caaee8' not in lake:raise ValueError('Wrong/unbound Lake version')
def parse_axioms(text,name):
    if 'sorryAx' in text or re.search(r'\berror:',text):raise ValueError('Disallowed axiom or elaboration error')
    lines=[s.strip() for s in text.splitlines() if 'depends on axioms:' in s or 'does not depend on any axioms' in s]
    if len(lines)!=1:raise ValueError('Missing/duplicate axiom record')
    line=lines[0]
    a=re.fullmatch(r"'([^']+)' depends on axioms: \[([^\]]*)\]",line)
    if a:
        if a.group(1)!=name:raise ValueError('Wrong audited declaration')
        axioms=[] if not a.group(2).strip() else [v.strip() for v in a.group(2).split(',')]
    else:
        a=re.fullmatch(r"'([^']+)' does not depend on any axioms",line)
        if not a or a.group(1)!=name:raise ValueError('Malformed/wrong axiom record')
        axioms=[]
    if set(axioms)-ALLOWED:raise ValueError('Axiom outside explicit allowed set')
    if not any(s.startswith(name+' :') or s.startswith('@'+name+' :') or s.startswith(name+'.{') for s in text.splitlines()):
        raise ValueError('Missing declaration/type readback')
    return axioms

def sources(base):
    return {str(p.relative_to(base)):sha(p) for p in base.rglob('*') if p.is_file() and '.lake' not in p.parts and
        (p.suffix=='.lean' or p.name in {'lean-toolchain','lake-manifest.json'})}

class Execute:
    def __init__(self,work):
        self.work=work;self.env=dict(os.environ);self.records=[]
        for k in ('LEAN_PATH','LEAN_SYSROOT'):self.env.pop(k,None)
        self.env['ELAN_TOOLCHAIN']='leanprover/lean4:v4.19.0'
    def cmd(self,label,args,cwd=None,check=True):
        start=time.time();d=self.work/'execution-evidence'/label;d.mkdir(parents=True)
        try:
            p=subprocess.run(args,cwd=cwd or self.work,env=self.env,capture_output=True)
            out,err,rc=p.stdout,p.stderr,p.returncode
        except OSError as ex:out,err,rc=b'',str(ex).encode(),127
        (d/'stdout.bin').write_bytes(out);(d/'stderr.bin').write_bytes(err)
        row={'command':args,'cwd':str(cwd or self.work),'exit':rc,'start_unix':start,'end_unix':time.time(),
             'stdout_sha256':sha(d/'stdout.bin'),'stderr_sha256':sha(d/'stderr.bin')}
        (d/'COMMAND.json').write_text(json.dumps(row,indent=2));self.records.append(row)
        if check and rc:raise RuntimeError(f'{label}: exit {rc}; raw evidence retained')
        return out.decode(errors='replace')+err.decode(errors='replace')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('workspace',type=pathlib.Path);g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--acquire',action='store_true');g.add_argument('--offline-deps',type=pathlib.Path)
    args=ap.parse_args();work=args.workspace.expanduser().resolve()
    if work.exists():raise SystemExit('Refusing existing workspace. Supply a NEW isolated directory.')
    shutil.copytree(ROOT/'formal',work);run=Execute(work)
    result={'status':'EXECUTION_INCOMPLETE','canonical_adoption':False,'obligation_pass_credit':False,
            'source_complete_for_all_obligations':False,'compiled_targets':[]}
    try:
        before=sources(work);(work/'EXPECTED_SOURCE_HASHES.json').write_text(json.dumps(before,indent=2))
        lean=run.cmd('01-lean-version',['lean','--version']);lake=run.cmd('02-lake-version',['lake','--version'])
        require_version(lean,lake)
        lock=json.loads((work/'lake-manifest.json').read_text());pins={p['name']:p for p in lock['packages']}
        depids=[]
        for name,p in pins.items():
            dest=work/'.lake/packages'/name;dest.parent.mkdir(parents=True,exist_ok=True)
            if args.offline_deps:
                src=(args.offline_deps/name).resolve()
                if not (src/'.git').exists():raise RuntimeError('Missing exact offline Git dependency '+name)
                shutil.copytree(src,dest,symlinks=True)
            else:
                dest.mkdir();run.cmd('dep-'+name+'-init',['git','init','--quiet'],dest)
                run.cmd('dep-'+name+'-remote',['git','remote','add','origin',p['url']],dest)
                run.cmd('dep-'+name+'-fetch',['git','fetch','--depth','1','origin',p['rev']],dest)
                run.cmd('dep-'+name+'-checkout',['git','checkout','--detach','--quiet','FETCH_HEAD'],dest)
            head=run.cmd('dep-'+name+'-head',['git','rev-parse','HEAD'],dest).strip()
            if head!=p['rev']:raise RuntimeError('Dependency pin mismatch '+name)
            dirty=run.cmd('dep-'+name+'-tracked-diff',['git','status','--porcelain','--untracked-files=no'],dest).strip()
            if dirty:raise RuntimeError('Tracked dependency changes '+name)
            depids.append({'name':name,'rev':head})
        lean2=run.cmd('03-lake-lean-version',['lake','env','lean','--version'])
        require_version(lean2,lake)
        run.cmd('04-lake-lean-prefix',['lake','env','lean','--print-prefix'])
        run.cmd('05-cache-get',['lake','exe','cache','get'],check=False)
        # Empty local-target artifacts are never inherited or trusted.
        build=work/'.lake/build'
        if build.exists():shutil.rmtree(build)
        started=time.time()
        run.cmd('06-candidate-build',['lake','build','P02','P02A2'])
        inventory=json.loads((ROOT/'provenance/FORMAL_INVENTORY.json').read_text())['theorems']
        if not inventory:raise RuntimeError('Empty declaration inventory')
        modules=sorted(set(t['module'] for t in inventory));artifacts=[]
        for mod in modules:
            p=work/'.lake/build/lib/lean'/pathlib.Path(*mod.split('.')).with_suffix('.olean')
            if not p.exists() or p.stat().st_size==0 or p.stat().st_mtime<started-2:
                raise RuntimeError('Missing/empty/stale target artifact: '+mod)
            artifacts.append({'module':mod,'path':str(p.relative_to(work)),'bytes':p.stat().st_size,'sha256':sha(p)})
        audits=work/'Audits';audits.mkdir()
        for i,t in enumerate(inventory):
            name=t['declaration'];audit=audits/f'Target{i:04}.lean'
            audit.write_text('import '+t['module']+'\n#check @'+name+'\n#print axioms '+name+'\n')
            text=run.cmd(f'audit-{i:04}',['lake','env','lean',str(audit)])
            axioms=parse_axioms(text,name)
            result['compiled_targets'].append({'declaration':name,'module':t['module'],'axioms':axioms,
                'audit_source_sha256':sha(audit),'declaration_type_readback':f'execution-evidence/audit-{i:04}/stdout.bin'})
        after=sources(work)
        for p,h in before.items():
            if after.get(p)!=h:raise RuntimeError('Build altered frozen source/lock '+p)
        if len(result['compiled_targets'])!=len(inventory):raise RuntimeError('Partial inventory')
        result.update(status='CANDIDATE_TARGETS_COMPILED_AND_AUDITED',dependencies=depids,
                      artifacts=artifacts,source_hashes=before)
    except Exception as ex:
        result.update(status='FAIL_CLOSED',failure=str(ex))
        raise
    finally:
        (work/'FORMAL_EXECUTION_RESULT.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':result['status'],'targets':len(result['compiled_targets']),
                      'adoption':False,'obligation_pass_credit':False},indent=2))
if __name__=='__main__':main()
