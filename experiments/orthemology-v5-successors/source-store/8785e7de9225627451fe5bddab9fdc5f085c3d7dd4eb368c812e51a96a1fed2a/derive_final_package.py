"""Bind only the frozen package's HasE inventory to verified source-built objects.

This does not add an arbitrary dependency override to the original replay runner.
The original package is never edited. The derived directory must be absent.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, shutil, subprocess, sys

MANIFEST='9f2a0f116f90fc4189faacc79d5b7c02116e1d36735cc2cdffe4f9117406de95'
RUNNER='4b1522dbe651ac97bece149b2fd21c8fc0688a87ac7bbd10e1f761bcf80d9adc'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')

def main():
    if sys.flags.optimize:raise ValueError('Assertions must be enabled')
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--original-package',type=Path,required=True)
    p.add_argument('--derived-package',type=Path,required=True)
    args=p.parse_args();A=args.work.resolve();E=A/'evidence';O=args.original_package.resolve();N=args.derived_package.resolve()
    assert sha(O/'MANIFEST.json')==MANIFEST and sha(O/'replay.py')==RUNNER
    if N.exists():raise ValueError('Derived package directory must be absent')
    if N.is_relative_to(O) or O.is_relative_to(N):raise ValueError('Packages must not overlap')
    if not N.name.startswith('SOURCE_BUILD_'):raise ValueError('Derived directory must have a SOURCE_BUILD_ label')
    subprocess.run([sys.executable,'-E','-S','-B',str(O/'replay.py'),'verify'],check=True)
    r=read(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json');inventory=read(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json')
    assert r['status']=='PASS' and r['provenance']=='SOURCE_BUILD'
    assert r['fresh_third_party_modules']==1369 and r['compiler_commands_bound_to_every_output']==1369
    assert r['preexisting_dependency_proof_objects_used']==0 and r['unexpected_dependency_proof_objects']==0
    assert sha(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json')==r['inventory_sha256']
    assert sha(E/'DEPENDENCY_COLD_BUILD.log')==r['build_log_sha256']
    assert sha(E/'DEPENDENCY_COLD_BUILD.json')==r['build_receipt_sha256']
    assert read(E/'DEPENDENCY_COLD_BUILD.json')['log_sha256']==r['build_log_sha256']
    assert sha(E/'COMPILER_PARSED_SOURCE_CLOSURE.json')==r['source_closure_sha256']
    old=read(O/'dependencies/hase.json'); expected={(x['package'],x['path']) for x in old['files']}
    fresh={(x['package'],x['object_relative_path']):x for x in inventory}
    assert set(fresh)==expected and len(fresh)==len(inventory)==1369
    objects=[]
    for row in old['files']:
        x=fresh[(row['package'],row['path'])];obj=A/'dependencies'/row['package']/'.lake/build/lib/lean'/row['path']
        assert obj.is_file() and not obj.is_symlink() and sha(obj)==x['object_sha256'] and obj.stat().st_size==x['object_bytes']
        src=A/'dependencies'/row['package']/x['source_path'];assert sha(src)==x['source_sha256']
        objects.append(dict(row,sha256=x['object_sha256'],bytes=x['object_bytes']))
    actual={(d.name,f.relative_to(d/'.lake/build/lib/lean').as_posix()) for d in (A/'dependencies').iterdir() for f in d.glob('.lake/build/lib/lean/**/*.olean')}
    assert actual==expected
    for package in old['packages']:
        d=A/'dependencies'/package['name']
        assert subprocess.check_output(['git','-C',str(d),'rev-parse','HEAD'],text=True).strip()==package['revision']
        assert not subprocess.check_output(['git','-C',str(d),'status','--porcelain','--untracked-files=no'],text=True).strip()
    shutil.copytree(O,N)
    new=dict(old,files=objects,trust='SOURCE_BUILD: exact objects freshly compiled from the unchanged official source pins; custody is in the separate SOURCE_BUILD_DERIVATION_RECEIPT.json. No dependency-byte reproducibility or compiler bootstrap claim.',inventory_origin_sha256=r['inventory_sha256'])
    write(N/'dependencies/hase.json',new)
    manifest=read(N/'MANIFEST.json')
    for row in manifest['files']:
        if row['path']=='dependencies/hase.json':row.update(sha256=sha(N/row['path']),bytes=(N/row['path']).stat().st_size)
    write(N/'MANIFEST.json',manifest)
    before={f.relative_to(O).as_posix():sha(f) for f in O.rglob('*') if f.is_file()}
    after={f.relative_to(N).as_posix():sha(f) for f in N.rglob('*') if f.is_file()}
    changed=sorted(k for k in before if before[k]!=after[k])
    assert set(before)==set(after) and changed==['MANIFEST.json','dependencies/hase.json']
    assert sha(O/'MANIFEST.json')==MANIFEST and sha(N/'replay.py')==RUNNER
    subprocess.run([sys.executable,'-E','-S','-B',str(N/'replay.py'),'verify'],check=True)
    sources=[{'path':k,'sha256':v} for k,v in sorted(before.items()) if k.endswith(('.lean','.py'))]
    write(E/'SOURCE_BUILD_DERIVATION_RECEIPT.json',{'status':'PASS_DERIVED_HASE_BINDING','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'provenance':'SOURCE_BUILD','original_package':str(O),'derived_package':str(N),'original_manifest_sha256':MANIFEST,
        'derived_manifest_sha256':sha(N/'MANIFEST.json'),'unchanged_runner_sha256':RUNNER,'changed_files':changed,
        'original_inventory_sha256':sha(O/'dependencies/hase.json'),'derived_inventory_sha256':sha(N/'dependencies/hase.json'),
        'source_build_receipt_sha256':sha(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json'),'source_object_inventory_sha256':r['inventory_sha256'],
        'scientific_and_runner_source_files_unchanged':sources,'all_other_package_bytes_unchanged':True,
        'changed_object_hashes_from_original':sum(x['sha256']!=y['sha256'] for x,y in zip(old['files'],objects)),
        'runner_static_cold_dependency_build_field_remains_false':True,'runner_static_cache_scope_text_unchanged':True,
        'scope_note':'Only this separately labelled HasE invocation is source-build qualified. Historical/cache-oriented package text and the runner cold_dependency_build=false field remain unchanged; this detached receipt supplies actual dependency custody. No other package lane or completed tranche is claimed.',
        'hase_replay_still_required':True})
    T=Path(read(A/'config.json')['toolchain'])
    write(A/'hase-environment.json',{'lean':str(T/'bin/lean'),'dependency_roots':{'hase':str(A/'dependencies')},'module_timeout_seconds':600})
    print('DERIVED_HASE_BINDING_PASS',changed)

if __name__=='__main__':main()
