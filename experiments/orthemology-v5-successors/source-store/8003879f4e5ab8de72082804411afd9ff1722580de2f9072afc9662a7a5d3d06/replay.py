"""Portable source-only replay. No network or package-source mutation."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys

PACKAGE=Path(__file__).resolve().parent
MODULES=['GroundedSupport','GroundedQuotient','AliasCuts','OccurrenceControls','CutControls','MutationControls']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    out=args.output.resolve()
    if out==PACKAGE or PACKAGE in out.parents:raise SystemExit('Output must be outside the sealed source package.')
    if out.exists():raise SystemExit('Output directory must not already exist.')
    manifest=json.loads((PACKAGE/'SOURCE_MANIFEST.json').read_text())
    for row in manifest['files']:
        p=PACKAGE/row['path']
        if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:
            raise SystemExit('Source hash mismatch: '+row['path'])
    out.mkdir(parents=True);objects=out/'objects';objects.mkdir();logs=out/'logs';logs.mkdir()
    lean=os.environ.get('LEAN_BIN') or shutil.which('lean')
    if not lean:raise SystemExit('Pinned Lean is not available; prepare the dependency environment first.')
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    env['LEAN_PATH']=str(objects)+os.pathsep+env.get('LEAN_PATH','')
    env['PYTHONPATH']=str(PACKAGE)+os.pathsep+env.get('PYTHONPATH','')
    statuses=[]
    def run(name,command):
        result=subprocess.run(command,cwd=out,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (logs/(name+'.txt')).write_text(result.stdout)
        statuses.append({'check':name,'exit_code':result.returncode})
        if result.returncode:
            (out/'FAILED_CHECKS.json').write_text(json.dumps(statuses,indent=2)+'\n')
            raise SystemExit('Failed '+name+'; inspect output logs.')
        return result.stdout
    version=run('lean-version',[lean,'--version']).strip()
    if 'version 4.19.0,' not in version or 'commit 6caaee842e94' not in version:
        raise SystemExit('Unexpected Lean version: '+version)
    lean_command=[lean,'--root='+str(PACKAGE)]
    imports=[]
    for module in MODULES:
        source=PACKAGE/'lean'/(module+'.lean')
        run('build-'+module,lean_command+['-o',str(objects/(module+'.olean')),str(source)])
        deptext=run('deps-'+module,lean_command+['--deps',str(source)])
        for line in deptext.splitlines():
            p=Path(line.strip())
            if p.name.endswith('.olean'):
                imports.append({'module':module,'object_name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
    readback=run('type-and-axiom-readback',lean_command+[str(PACKAGE/'lean/Readback.lean')])
    if readback!=(PACKAGE/'validation/TYPE_AXIOM_READBACK.txt').read_text():
        raise SystemExit('Exact author theorem/axiom readback differs.')
    run('independent-lean-controls',lean_command+['-o',str(objects/'IndependentControls.olean'),str(PACKAGE/'review/IndependentControls.lean')])
    run('python-tests',[sys.executable,'-m','unittest','discover','-s',str(PACKAGE),'-p','test_grounded_support.py','-v'])
    run('alias-search',[sys.executable,str(PACKAGE/'search_cut_order.py')])
    if json.loads((out/'CUT_ORDER_SEARCH.json').read_text())!=json.loads((PACKAGE/'validation/CUT_ORDER_SEARCH.json').read_text()):raise SystemExit('Alias search result differs.')
    oracle_path=out/'INDEPENDENT_FINITE_CHECKS.json'
    run('independent-finite-checks',[sys.executable,str(PACKAGE/'review/independent_finite_checks.py'),str(oracle_path)])
    if json.loads(oracle_path.read_text())!=json.loads((PACKAGE/'review/INDEPENDENT_FINITE_CHECKS.json').read_text()):raise SystemExit('Independent finite oracle result differs.')
    receipt={'status':'PASS_PORTABLE_SOURCE_REPLAY','source_manifest_sha256':sha(PACKAGE/'SOURCE_MANIFEST.json'),'lean_version':version,'lean_binary_sha256':sha(Path(lean).resolve()),'candidate_modules_fresh':MODULES,'independent_control_module_fresh':True,'author_readback_identical':True,'checks':statuses,'direct_import_bindings':imports,'scope':'Fresh supplied source; prepared dependency objects reused. No cold dependency rebuild, general Python refinement or actual-world authority claim.'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS source identity, six modules, exact readback, independent Lean controls, Python tests and independent finite oracle.')
if __name__=='__main__':main()
