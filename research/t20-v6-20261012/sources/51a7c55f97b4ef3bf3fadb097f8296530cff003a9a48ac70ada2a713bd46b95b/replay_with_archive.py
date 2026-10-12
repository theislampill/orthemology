#!/usr/bin/env python3
"""Portable, fresh-output replay for the bounded Sixth follow-up packet.

No downloads, source rewrites, heartbeat escalation, or custom-object reuse.
--verify-only performs packaging/source-integrity checks, not Lean proof replay.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, time, sys
if sys.flags.optimize:
    raise RuntimeError("Optimized Python is refused: all source and outcome guards must execute")
sys.dont_write_bytecode = True
from verify_dependency_identity import verify_dependencies

ROOT = None
CREATED_OUTPUT = None
EXPECTED_PACKET_MANIFEST_SHA256 = "f2eae35e8dfc35f630f1ef8228700517520b777aa451ad47fa2ec7e8c4198064"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(path, obj): Path(path).write_text(json.dumps(obj, indent=2)+'\n')
def verify_packet():
    if sha(ROOT/'MANIFEST.json') != EXPECTED_PACKET_MANIFEST_SHA256:
        raise ValueError('Unexpected original packet manifest identity')
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    assert sha(ROOT/'MANIFEST.json') == (ROOT/'MANIFEST.sha256').read_text().split()[0]
    expected = {x['path'] for x in manifest['files']} | {'MANIFEST.json','MANIFEST.sha256'}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == expected, 'Packet inventory differs from manifest'
    for row in manifest['files']:
        assert sha(ROOT/row['path']) == row['sha256'], row['path']
    inputs = json.loads((ROOT/'INPUT_MAP.json').read_text())
    for row in inputs['runtime_closure']:
        assert sha(ROOT/row['path']) == row['sha256']
    for row in inputs['mutations']:
        a=(ROOT/row['baseline']).read_bytes();b=(ROOT/row['path']).read_bytes()
        assert sha(ROOT/row['path']) == row['sha256']
        assert a.count(row['replace_before'].encode()) == 1
        assert a.replace(row['replace_before'].encode(),row['replace_after'].encode()) == b
    # Graph is reconstructed, rather than trusting the stated closure census.
    by={row['module']:row for row in inputs['runtime_closure']}
    seen=set()
    order=[]
    def visit(name):
        if name in seen or name not in by: return
        seen.add(name)
        text=(ROOT/by[name]['path']).read_text()
        for line in text.splitlines():
            if line.startswith('import '):
                for dep in line[7:].split():
                    if dep in by: visit(dep)
                    else: assert dep.startswith(('Mathlib','Lean','Std','Init')), dep
        order.append(name)
    visit('FullControllerCanonicalLaw')
    assert set(order)==set(by) and len(order)==162
    return inputs, [by[name] for name in order]

def main():
    global ROOT, CREATED_OUTPUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--packet',type=Path,required=True,help='Freshly extracted unchanged original controls packet')
    parser.add_argument('--mathlib-archive',type=Path,help='Exact official pinned tar.gz when Mathlib is an archive extraction')
    parser.add_argument('--verify-dependencies-only',action='store_true',help='Validate original packet and all dependency identities without proof replay')
    parser.add_argument('--lean-bin',type=Path,help='Directory containing pinned Lean and lake executables')
    parser.add_argument('--mathlib',type=Path,help='Exact pinned Git checkout or source-archive extraction, with official dependency caches')
    parser.add_argument('--out',type=Path,help='Absent output directory outside this immutable packet')
    parser.add_argument('--mode',choices=['cost','runtime','all'],default='all')
    args=parser.parse_args()
    ROOT=args.packet.resolve()
    inputs,order=verify_packet()
    if args.verify_only:
        print('PASS_PACKET_INTEGRITY: 162 exact runtime modules; two exact mutation derivations. No proofs rerun.')
        return
    if args.lean_bin is None or args.mathlib is None or args.out is None:
        parser.error('--lean-bin, --mathlib and --out are required for replay')
    lean_bin=args.lean_bin.resolve();mathlib=args.mathlib.resolve();out=args.out.resolve()
    assert not out.exists() and not out.is_relative_to(ROOT), 'Output must be absent and outside packet'
    for protected in [ROOT, Path(__file__).resolve().parent, mathlib, lean_bin.parent]:
        if out.is_relative_to(protected):
            raise ValueError('Output cannot be inside an immutable packet, wrapper, or dependency root')
    pins=json.loads((ROOT/'DEPENDENCY_PINS.json').read_text())
    lean=lean_bin/'lean';assert sha(lean)==pins['lean_binary_sha256']
    assert subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version']
    identity=verify_dependencies(mathlib,args.mathlib_archive,pins)
    if args.verify_dependencies_only:
        print(json.dumps({'status':'PASS_PACKET_AND_DEPENDENCY_IDENTITIES','dependency_identity':identity},indent=2))
        return
    libs=[mathlib/'.lake/build/lib/lean']+sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    assert (libs[0]/'Mathlib.olean').is_file(), 'Official Mathlib cache is required'
    out.mkdir()
    CREATED_OUTPUT = out
    logs=out/'logs';logs.mkdir();build=out/'runtime/build';build.mkdir(parents=True)
    env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build]+libs))
    result={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'mode':args.mode,'status':'RUNNING','packet_manifest_sha256':sha(ROOT/'MANIFEST.json'),
      'scope':'Sixth baseline revalidation; no Seventh novelty or automatic baseline-status changes',
      'trusted_official_dependency_cache':True,'custom_objects_reused':False,'heartbeat_flags_added':False,
      'dependency_identity':identity,
      'baseline_control_statuses':{'cost':'INCONCLUSIVE','runtime':'INCONCLUSIVE'},'runs':[]}
    save=lambda:write(out/'RESULT.json',result)
    save()
    def run(label,source,output=None,root=None,timeout=180):
        command=[str(lean),'-j1']
        if root: command+=['--root='+str(root)]
        if output: output.parent.mkdir(parents=True,exist_ok=True);command+=['-o',str(output)]
        command+=[str(source)];start=time.monotonic()
        try:
            p=subprocess.run(command,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
            text=p.stdout;code=p.returncode
        except subprocess.TimeoutExpired as e:
            text=e.stdout.decode() if isinstance(e.stdout,bytes) else (e.stdout or '')
            text+='\nWALL_CLOCK_LIMIT_'+str(timeout)+'_SECONDS\n';code=None
        log=logs/(label+'.log');log.write_text(text)
        row={'id':label,'source_sha256':sha(source),'exit_code':code,'command':command,
             'log_sha256':sha(log),'elapsed_seconds':round(time.monotonic()-start,3),
             'resource_inconclusive':code is None or 'timeout' in text.lower()}
        if output and output.exists():row['object_sha256']=sha(output)
        result['runs'].append(row);save()
        print(label,code,flush=True)
        return row,text
    if args.mode in ('cost','all'):
        row,text=run('cost-positive',ROOT/'focused/CostTolerancePremise.lean',timeout=60)
        assert row['exit_code']==0 and 'sorryAx' not in text and 'error:' not in text,text
        row,text=run('cost-negative-scalar',ROOT/'focused/CostTolerancePremiseNegative.lean',timeout=60)
        assert row['exit_code']==1 and not row['resource_inconclusive'] and 'error: type mismatch' in text and 'η ≤ ε / 2' in text,text
        result['cost']='SCALAR_OBSTRUCTION_CONFIRMED_NOT_FULL_MUTANT_REJECTION';save()
    if args.mode in ('runtime','all'):
        for module in order:
            row,text=run(module['module'],ROOT/module['path'],build/(module['module'].replace('.','/')+'.olean'),ROOT/'runtime/src')
            if row['exit_code']!=0 or re.search(r'\b(sorry|admit)\b|declaration uses',text):
                result['status']='POSITIVE_CLOSURE_BLOCKED';save();return
        row,text=run('runtime-target-readback',ROOT/'focused/RuntimeTargetReadback.lean',timeout=60)
        assert row['exit_code']==0 and 'sorryAx' not in text and 'Lean.ofReduceBool' not in text,text
        d=out/'runtime/mutant';d.mkdir();src=d/'FullControllerCanonicalLaw.lean'
        src.write_bytes((ROOT/'mutations/runtime/FullControllerCanonicalLaw.lean').read_bytes())
        row,text=run('runtime-original-mutant',src,root=d)
        result['runtime_mutant']='INCONCLUSIVE' if row['resource_inconclusive'] else ('ACCEPTED_REQUIRES_REVIEW' if row['exit_code']==0 else 'NON_RESOURCE_FAILURE_REQUIRES_REVIEW')
    result['status']='COMPLETED_BOUNDED_REPLAY'
    result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
    print(result['status'])

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        # A failed guard must not leave a terminal attempt labeled RUNNING.
        if CREATED_OUTPUT is not None:
            receipt=CREATED_OUTPUT/'RESULT.json'
            if receipt.is_file():
                state=json.loads(receipt.read_text())
                state.update(status='FAIL_CLOSED',error=str(exc),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
                write(receipt,state)
        raise
