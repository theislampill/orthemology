"""Mandatory build/custody gates. Policy tests are NOT proof-kernel evidence.

The gate trusts the selected Lean executable, operating system and filesystem.
It rejects incomplete evidence; it cannot make a malicious compiler trustworthy.
All subprocesses here are local trusted build/test tools, not candidate programs.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import tempfile
import time
from typing import Any

APPROVED_AXIOMS = frozenset({'propext', 'Classical.choice', 'Quot.sound'})
PIN = 'leanprover/lean4:v4.19.0'
VERSION = '4.19.0'

class GateError(ValueError):
    """A required verification condition was not established."""

def strict_json(path: Path) -> Any:
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise GateError('duplicate JSON key: '+k)
            d[k]=v
        return d
    try:
        if path.stat().st_size > 8*1024*1024: raise GateError('metadata size limit')
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(GateError('nonfinite metadata')))
    except (OSError, ValueError, RecursionError) as e:
        raise GateError(f'metadata {path.name}: {e}') from e

def digest(path: Path) -> dict:
    if path.is_symlink() or not path.is_file(): raise GateError('not a regular file: '+str(path))
    h=hashlib.sha256(); n=0
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):
            n+=len(block);h.update(block)
    return {'bytes':n,'sha256':h.hexdigest()}

def verify_manifest(root: Path) -> dict:
    """Exact coverage: only this root manifest is excluded, NEVER nested ones."""
    root=root.resolve(); path=root/'MANIFEST.json'
    if not path.is_file() or path.is_symlink(): raise GateError('mandatory root manifest missing')
    j=strict_json(path)
    if type(j) is not dict or type(j.get('files')) is not list: raise GateError('manifest schema')
    expected=set()
    for row in j['files']:
        if type(row) is not dict or set(row)!={'path','bytes','sha256'}:raise GateError('manifest entry schema')
        rel=row['path']
        if type(rel) is not str or not rel or '\\' in rel:raise GateError('manifest path')
        p=PurePosixPath(rel)
        if p.is_absolute() or '..' in p.parts or p.as_posix()!=rel or rel=='MANIFEST.json':raise GateError('manifest path traversal/noncanonical')
        if rel in expected:raise GateError('duplicate manifest entry: '+rel)
        expected.add(rel)
        if type(row['bytes']) is not int or row['bytes']<0 or type(row['sha256']) is not str or not re.fullmatch('[0-9a-f]{64}',row['sha256']):raise GateError('manifest digest schema')
        item=root/p
        # Check every path component, including directory symlinks.
        if any(q.is_symlink() for q in [item,*item.parents] if q!=root.parent):raise GateError('manifest symlink')
        if digest(item)!={'bytes':row['bytes'],'sha256':row['sha256']}:raise GateError('manifest mismatch: '+rel)
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():raise GateError('unmanifested symlink')
        if p.is_file() and p!=path:actual.add(p.relative_to(root).as_posix())
    if actual!=expected:raise GateError('manifest coverage: missing='+repr(sorted(expected-actual))+' extra='+repr(sorted(actual-expected)))
    return {'status':'PASS','members':len(expected),'manifest_sha256':digest(path)['sha256']}

def enforce_version(expected: str, output: str) -> None:
    m=re.fullmatch(r'Lean \(version ([0-9]+\.[0-9]+\.[0-9]+)(?:,[^\r\n]*)?\)\s*',output)
    if m is None or m.group(1)!=expected:raise GateError('wrong or missing Lean identity: '+output[:200])

def check_artifact(path: Path) -> dict:
    d=digest(path)
    if d['bytes']==0:raise GateError('empty compiled artifact: '+str(path))
    return d

def parse_audit(output: str, targets: list[str]) -> dict:
    """Exact per-declaration types AND transitive axiom readback are mandatory.

    Input must come from the real compiler in production. Unit strings exercise
    this parser only and never result in a kernel_verified receipt.
    """
    if not targets or len(targets)!=len(set(targets)):raise GateError('empty/duplicate required targets')
    blocks=re.findall(r'^AUDIT_BEGIN ([A-Za-z0-9_.]+)\n(.*?)^AUDIT_END \1\s*$',output,re.M|re.S)
    names=[n for n,_ in blocks]
    if len(names)!=len(set(names)) or set(names)!=set(targets):raise GateError('declaration audit coverage')
    if output.count('AUDIT_BEGIN ')!=len(names) or output.count('AUDIT_END ')!=len(names):raise GateError('partial/malformed audit block')
    result={}
    for name,text in blocks:
        # #check prints a universe suffix when pp.universes is enabled.
        if re.search(r'^'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:',text,re.M) is None:raise GateError('missing declaration type: '+name)
        dep=re.findall(r"['`]?"+re.escape(name)+r"['`]? depends on axioms:\s*\[([^\]]*)\]",text,re.S)
        empty=re.findall(r"['`]?"+re.escape(name)+r"['`]? does not depend on any axioms",text)
        if len(dep)+len(empty)!=1:raise GateError('missing/ambiguous axiom target: '+name)
        used={a.strip() for a in dep[0].split(',') if a.strip()} if dep else set()
        if used-APPROVED_AXIOMS:raise GateError('unapproved dependencies: '+repr(sorted(used-APPROVED_AXIOMS)))
        result[name]={'axioms':sorted(used),'type_and_axiom_text':text.strip()}
    if 'sorryAx' in output:raise GateError('sorryAx in readback')
    return result

def run_bounded(command: list[str], cwd: Path, *, timeout: float=180,
                output_limit: int=8*1024*1024, env: dict|None=None) -> dict:
    """Capture both streams, status and errors; kill the process group on limits.

    Output is spooled to files (not unbounded memory). Polling may permit a brief
    overshoot on disk; only the configured prefix is read into the receipt.
    This is orchestration resource control, not a security sandbox.
    """
    if timeout<=0 or output_limit<1:raise GateError('invalid process limits')
    started=time.monotonic(); result={'command':list(map(str,command)),'cwd':str(cwd),'ok':False}
    with tempfile.TemporaryDirectory(prefix='orth-process-') as td:
        out=Path(td)/'stdout';err=Path(td)/'stderr';p=None;status='EXIT'
        try:
            with out.open('wb') as fo,err.open('wb') as fe:
                p=subprocess.Popen(command,cwd=cwd,env=env,stdout=fo,stderr=fe,start_new_session=True)
                while p.poll() is None:
                    if time.monotonic()-started>timeout:status='TIMEOUT';break
                    if out.stat().st_size+err.stat().st_size>output_limit:status='OUTPUT_LIMIT';break
                    time.sleep(.01)
                if status!='EXIT':
                    try:os.killpg(p.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                p.wait(timeout=5)
            size=out.stat().st_size+err.stat().st_size
            if size>output_limit and status=='EXIT':status='OUTPUT_LIMIT'
            result.update(status=status,exit_code=p.returncode,output_bytes=size,ok=status=='EXIT' and p.returncode==0)
        except (OSError,subprocess.SubprocessError) as e:
            if p is not None and p.poll() is None:
                try:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
                except (OSError,subprocess.SubprocessError):pass
            result.update(status='OS_ERROR',exit_code=None,error=repr(e))
        def read(p):
            if not p.exists():return ''
            with p.open('rb') as f:return f.read(output_limit).decode('utf-8','replace')
        result.update(stdout=read(out),stderr=read(err),elapsed_seconds=round(time.monotonic()-started,6))
    return result

def write_run(dest: Path, label: str, record: dict) -> dict:
    dest.mkdir(parents=True,exist_ok=True)
    for stream in ('stdout','stderr'):(dest/(label+'.'+stream+'.txt')).write_text(record.get(stream,''))
    row={k:v for k,v in record.items() if k not in ('stdout','stderr')}
    (dest/(label+'.json')).write_text(json.dumps(row,indent=2)+'\n')
    return row

# These are acceptance-contract roles, not an inventory inferred only from
# whichever #print commands happen to remain in edited source.
MANDATORY_TARGETS=frozenset({
    'OrthemologyV2.selfInstantiate_same_program',
    'OrthemologyV3.checked_sound',
    'OrthemologyV4.checker_sound',
    'OrthemologyV4.execution_implies_checked',
    'OrthemologyV4.revision_stability',
    'OrthemologyV4.parametric_reach',
    'OrthemologyV4.not_SCUUAt',
    'OrthemologyV4.positive_OWOU',
    'OrthemologyV4.mainWitnessAt',
})

def strip_comments(text: str) -> str:
    out=[];i=0;depth=0;string=False
    while i<len(text):
        if depth:
            if text[i:i+2]=='/-':depth+=1;i+=2
            elif text[i:i+2]=='-/':depth-=1;i+=2
            else:i+=1
        elif string:
            if text[i]=='\\':i+=2
            elif text[i]=='"':string=False;i+=1
            else:i+=1
        elif text[i:i+2]=='/-':depth=1;i+=2
        elif text[i:i+2]=='--':
            j=text.find('\n',i);i=len(text) if j<0 else j
        elif text[i]=='"':string=True;i+=1
        else:out.append(text[i]);i+=1
    if depth or string:raise GateError('unclosed source comment/string')
    return ''.join(out)

def declared_theorems(text: str) -> list[str]:
    """Hygiene inventory for the explicitly used simple namespace syntax.
    Does not pretend to be a Lean parser. Actual #check is the build authority.
    """
    scope=[];names=[]
    for line in strip_comments(text).splitlines():
        n=re.match(r'^\s*(namespace|section)\s*([A-Za-z0-9_.]*)\s*$',line)
        if n:scope.append(n.groups());continue
        if re.match(r'^\s*end(?:\s+[A-Za-z0-9_.]+)?\s*$',line):
            if scope:scope.pop()
            continue
        n=re.match(r'^\s*(?:protected\s+)?theorem\s+([A-Za-z0-9_.]+)',line)
        if n:names.append('.'.join([s for kind,s in scope if kind=='namespace']+[n.group(1)]))
    return names

def validate_inventory(contract: dict, actual: dict[str,list[str]]) -> list[dict]:
    if type(contract) is not dict or type(contract.get('modules')) is not list or not contract['modules']:raise GateError('missing formal inventory')
    rows=contract['modules'];names=[];all_targets=[]
    for row in rows:
        if type(row) is not dict or set(row)!={'name','targets'} or type(row['name']) is not str or type(row['targets']) is not list:raise GateError('formal inventory schema')
        if not re.fullmatch('[A-Za-z][A-Za-z0-9_]*',row['name']):raise GateError('unsafe module name')
        ts=row['targets']
        if not ts or any(type(x) is not str or not re.fullmatch('[A-Za-z][A-Za-z0-9_.]*',x) for x in ts) or len(ts)!=len(set(ts)):raise GateError('target inventory schema')
        if row['name'] not in actual or not set(actual[row['name']])<=set(ts):raise GateError('unaudited theorem declaration')
        names.append(row['name']);all_targets.extend(ts)
    if len(names)!=len(set(names)) or set(names)!=set(actual):raise GateError('incomplete module inventory')
    if len(all_targets)!=len(set(all_targets)):raise GateError('duplicate declared targets')
    if not MANDATORY_TARGETS<=set(all_targets):raise GateError('missing acceptance-contract targets: '+repr(sorted(MANDATORY_TARGETS-set(all_targets))))
    return rows

def render_required_audit(rows: list[dict]) -> str:
    """Actual compiler input; every target runs the transitive in-Lean guard.

    Source emission/tests do not mean this command has elaborated successfully.
    Production success additionally requires the real compiler and full readback.
    """
    if not any(r['name']=='AuditSupport' for r in rows):raise GateError('mandatory elaborated audit module absent')
    text='\n'.join('import '+r['name'] for r in rows)+'\nset_option pp.universes true\n'
    for row in rows:
        for name in row['targets']:
            text+=f'#eval IO.println "AUDIT_BEGIN {name}"\n#check {name}\n#ortho_audit {name}\n#print axioms {name}\n#eval IO.println "AUDIT_END {name}"\n'
    return text
