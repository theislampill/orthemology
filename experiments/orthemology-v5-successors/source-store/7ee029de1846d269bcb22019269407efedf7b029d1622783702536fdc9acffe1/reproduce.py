#!/usr/bin/env python3
"""Fresh isolated Init-only replay; refuses to overwrite prior evidence."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, sys

def guarded_output(requested, protected):
    # Check both the user's lexical path and its actual filesystem destination.
    requested = Path(requested)
    if requested.exists() or requested.is_symlink():
        raise RuntimeError('Refusing an existing output path or symlink')
    lexical = Path(os.path.abspath(requested))
    output = requested.resolve()
    for raw in protected:
        raw = Path(raw)
        lexical_root = Path(os.path.abspath(raw))
        actual_root = raw.resolve()
        if lexical.is_relative_to(lexical_root) or output.is_relative_to(actual_root):
            raise RuntimeError('Output must be outside every protected input tree')
        # Internal cache aliases are allowed. Escaping aliases are unsupported,
        # including a dependency directory symlink into a separate object store.
        if actual_root.is_dir():
            for parent, directories, files in os.walk(actual_root, followlinks=False):
                for name in directories + files:
                    item = Path(parent) / name
                    if item.is_symlink() and not item.resolve().is_relative_to(actual_root):
                        raise RuntimeError('Escaping symlinked input layout is unsupported')
    if not output.parent.is_dir():
        raise RuntimeError('Output parent must already exist')
    return output

def verify_public_package(root):
    manifest = json.loads((root / 'SOURCE_PACKAGE.json').read_text())
    for row in manifest['files']:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Unsafe package member')
        path = root / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256'] or path.stat().st_size != row['bytes']:
            raise RuntimeError('Selected source package identity mismatch: ' + row['path'])
    return {'status': 'PASS', 'selected_files': len(manifest['files']), 'historical_raw_source_binding_replay': 'NOT_RUN; locator-only public source selection'}


P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args=parser.parse_args()
LEAN=args.lean.resolve()
if args.output.is_symlink(): raise SystemExit("Refusing an existing output symlink")
out=args.output.resolve()
if out.exists(): raise SystemExit('Refusing existing output path.')
if any(out.is_relative_to(p) for p in [P, LEAN.parent.parent]): raise SystemExit('Output must be outside source and compiler trees.')
if not out.parent.is_dir(): raise SystemExit('Output parent must exist.')
out=guarded_output(args.output,[P,args.lean.parent.parent,LEAN.parent.parent])
verify_public_package(P)
EXPECTED='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if not LEAN.is_file(): raise SystemExit(f'Existing official Lean executable missing: {LEAN}')
if sha(LEAN)!=EXPECTED: raise SystemExit('Compiler identity mismatch; no installation or replacement attempted.')
out.mkdir()
env=os.environ.copy();env['LEAN_PATH']=str(out)
steps=[]
def run(label,args,expected=0):
    result=subprocess.run([str(LEAN),*map(str,args)],cwd=P,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/(label+'.log')).write_text(result.stdout)
    steps.append({'label':label,'command':[str(LEAN),*map(str,args)],'exit_code':result.returncode,'expected':'reject' if expected else 'success','log':label+'.log'})
    if expected:
        if result.returncode==0 or ("tactic 'decide' proved that the proposition" not in result.stdout or "is false" not in result.stdout):
            raise RuntimeError(f'{label}: expected a kernel decide rejection, got {result.returncode}; see log')
    elif result.returncode!=0 or 'error:' in result.stdout or 'warning:' in result.stdout:
        raise RuntimeError(f'{label}: compile unsuccessful or warning; see log')
    return result.stdout
try:
    run('toolchain',['--version'])
    for module in ['AnchoredSourceBridge','Controls','ModalAbilityControl']:
        run(module,['-o',out/(module+'.olean'),P/'src'/(module+'.lean')])
    run('Acceptance',[P/'tests/Acceptance.lean'])
    declarations=[]
    readback=['import ModalAbilityControl','set_option pp.universes true','set_option pp.proofs false','set_option format.width 140']
    for module,namespace in [('AnchoredSourceBridge','AnchoredSourceBridge'),('Controls','AnchoredSourceBridge.Controls'),('ModalAbilityControl','AnchoredSourceBridge.Controls.ModalAbility')]:
        content=(P/'src'/(module+'.lean')).read_text()
        for name in re.findall(r'^theorem\s+(\w+)',content,re.M):
            fqn=namespace+'.'+name;declarations.append({'name':fqn,'module':module})
            readback.extend(['#print '+fqn,'#print axioms '+fqn])
    (out/'Readback.lean').write_text('\n'.join(readback)+'\n')
    readback_log=run('Readback',[out/'Readback.lean'])
    if 'sorryAx' in readback_log or 'Lean.ofReduceBool' in readback_log:
        raise RuntimeError('Unacceptable axiom in readback')
    for f in sorted((P/'tests/rejected').glob('*.lean')): run('rejected-'+f.stem,[f],expected=1)
    verify_public_package(P)
    statuses='PASS'
except Exception as exc:
    statuses='FAIL'; failure=str(exc)
files=[]
for root in ['src','tests']:
    for f in sorted((P/root).rglob('*')):
        if f.is_file(): files.append({'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)})
files.append({'path':'reproduce.py','bytes':Path(__file__).stat().st_size,'sha256':sha(Path(__file__))})
manifest={'schema':'t20-anchored-original-provision-build-v1','status':statuses,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'compiler':{'path':str(LEAN),'sha256':sha(LEAN)},'import_scope':'Init and the three new modules only','semantic_scope':'Conditional typed contribution-incidence mathematics and explicit finite interpretations; no metaphysical warrant verification','source_files':files,'steps':steps,'declarations':locals().get('declarations',[]),'outputs':[{'path':str(f.relative_to(out)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(out.rglob('*')) if f.is_file()]}
if statuses=='FAIL': manifest['failure']=failure
(out/'BUILD_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':statuses,'output':str(out),'steps':len(steps),'theorems':len(manifest['declarations']),'failure':manifest.get('failure')},indent=2))
raise SystemExit(0 if statuses=='PASS' else 1)
