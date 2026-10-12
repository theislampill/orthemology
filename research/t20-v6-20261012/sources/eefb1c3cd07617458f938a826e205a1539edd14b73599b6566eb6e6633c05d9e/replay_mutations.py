#!/usr/bin/env python3
"""Reject six semantic shortcut mutants using hash-verified exact fresh baseline objects."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, re, subprocess

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--baseline',type=Path,required=True)
    ap.add_argument('--lean-bin',type=Path,required=True)
    ap.add_argument('--mathlib',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); packet=a.packet.resolve(); baseline=a.baseline.resolve(); out=a.out.resolve()
    root=Path(__file__).resolve().parents[1]
    if out.exists() or out.is_relative_to(root) or out.is_relative_to(packet):
        ap.error('Output must be absent and outside both immutable packets')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    declared={'MANIFEST.json'}
    for row in manifest['files']:
        rel=row['path']; p=root/rel
        if p.resolve().is_relative_to(root) is False or p.is_symlink() or not p.is_file():
            raise ValueError('Unsafe or missing input')
        if rel in declared or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:
            raise ValueError('Mutation input identity mismatch')
        declared.add(rel)
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    if declared!=actual: raise ValueError('Mutation input census mismatch')
    spec=importlib.util.spec_from_file_location('core',packet/'tooling/portable_core.py')
    core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
    identity=core.verify(packet)
    receipt=json.loads((baseline/'REPLAY_RESULT.json').read_text())
    if receipt['status']!='PASS' or receipt['input_manifest_sha256']!=identity['manifest_sha256']:
        raise ValueError('Baseline is not a passing replay of exact source packet')
    suite=next(s for s in receipt['suites'] if s['id']=='scc_parity_pruning')
    if suite['status']!='PASS': raise ValueError('Baseline suite not passing')
    build=baseline/'scc_parity_pruning/build'
    for row in suite['modules']:
        obj=build/(row['module'].replace('.','/')+'.olean')
        if row['status']!='FRESH_COMPILE' or sha(obj)!=row['olean_sha256']:
            raise ValueError('Baseline object not freshly compiled or changed')
    pins=json.loads((packet/'replay/DEPENDENCY_PINS.json').read_text())
    lean,libs,version,checks=core.verify_pins(a.lean_bin,a.mathlib,pins,{r['module'] for r in suite['modules']})
    out.mkdir(parents=True);(out/'source').mkdir();(out/'logs').mkdir()
    result={'status':'RUNNING','scope':'Expected kernel rejection of false semantic-shortcut controls; exact fresh baseline object reuse only',
      'mutation_manifest_sha256':sha(root/'MANIFEST.json'),'baseline_receipt_sha256':sha(baseline/'REPLAY_RESULT.json'),
      'source_manifest_sha256':identity['manifest_sha256'],'lean_version':version,'dependency_checks':checks,'mutations':[]}
    save(out/'MUTATION_RESULT.json',result)
    env=dict(os.environ);env.pop('LEAN_SRC_PATH',None)
    env['LEAN_PATH']=':'.join(map(str,[build]+libs));env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','')
    for src in sorted((root/'mutations').glob('*.lean')):
        core.check_source(src.read_text());target=out/'source'/src.name;target.write_bytes(src.read_bytes())
        run=subprocess.run([str(lean),'-j1','--root='+str(out/'source'),str(target)],cwd=out/'source',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=out/'logs'/(src.stem+'.log');log.write_text(run.stdout)
        errs=re.findall(r'^.*: error: (.*)$',run.stdout,re.M)
        expected=(run.returncode!=0 and len(errs)==1 and errs[0]=="tactic 'decide' proved that the proposition" and 'is false' in run.stdout and 'warning:' not in run.stdout)
        item={'name':src.stem,'source_sha256':sha(src),'exit':run.returncode,'log_sha256':sha(log),'expected_false_proposition_rejected':expected}
        result['mutations'].append(item);save(out/'MUTATION_RESULT.json',result)
        print(src.stem,'EXPECTED_REJECTION' if expected else 'FAIL',flush=True)
        if not expected: raise ValueError('Unexpected mutation outcome '+src.stem)
    if len(result['mutations'])!=6:raise ValueError('Wrong mutation count')
    result['status']='PASS_SIX_EXPECTED_REJECTIONS';save(out/'MUTATION_RESULT.json',result)
if __name__=='__main__':main()
