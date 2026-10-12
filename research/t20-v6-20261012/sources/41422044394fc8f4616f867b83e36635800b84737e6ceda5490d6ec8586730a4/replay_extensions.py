#!/usr/bin/env python3
"""Fresh trust-zero checks of the two frozen increments; zero inherited rebuilds.
Embedded predecessor source archives travel with the packet. Exact prerequisite
objects, Lean distribution, and pinned external package builds remain external.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())


def inside(root, name):
    rel = PurePosixPath(name)
    assert not rel.is_absolute() and '..' not in rel.parts, name
    p = root / rel
    assert not p.is_symlink() and p.resolve().is_relative_to(root.resolve()), name
    return p


def verify_index(root, expected=None):
    index = root / 'ARCHIVE_CONTENTS.json'
    if expected: assert sha(index) == expected, str(index)
    rows = read(index)['files']
    assert len({r['path'] for r in rows}) == len(rows)
    for row in rows:
        p = inside(root, row['path'])
        assert sha(p) == row['sha256'] and p.stat().st_size == row['bytes'], str(p)
    return len(rows)


def archive_matches(path, root):
    with zipfile.ZipFile(path) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        assert len({i.filename for i in infos}) == len(infos)
        for i in infos:
            rel = PurePosixPath(i.filename)
            assert rel.parts[0] == root.name
            assert z.read(i) == inside(root, str(PurePosixPath(*rel.parts[1:]))).read_bytes(), i.filename
    return len(infos)


def extract_predecessors(contract, output):
    roots = {}
    for row in contract['predecessors']:
        path = ROOT / 'predecessors' / row['archive']
        assert sha(path) == row['sha256'] and path.stat().st_size == row['bytes']
        with zipfile.ZipFile(path) as z:
            names = [i.filename for i in z.infolist() if not i.is_dir()]
            assert len(names) == len(set(names)) == row['entry_count']
            for i in z.infolist():
                if i.is_dir(): continue
                assert PurePosixPath(i.filename).parts[0] == row['root']
                assert (i.external_attr >> 16) & 0o170000 != 0o120000, 'ZIP symlink'
                p = inside(output, i.filename)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(z.read(i))
        root = output / row['root']
        verify_index(root, row['index_sha256'])
        archive_matches(path, root)
        roots[row['archive']] = root
    return roots


def source_path(binding, roots):
    mapping = binding['mapping']
    if mapping['kind'] == 'addition': return inside(ROOT, mapping['path'])
    if mapping['kind'] == 'predecessor':
        rel = PurePosixPath(mapping['entry'])
        root = roots[mapping['archive']]
        assert rel.parts[0] == root.name
        return inside(root, str(PurePosixPath(*rel.parts[1:])))
    raise AssertionError(mapping)


def load_verifier(root):
    spec = importlib.util.spec_from_file_location('authenticated_predecessor', root / 'replay_extractor.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(args, c, roots, predecessor):
    count = verify_index(ROOT)
    for row in c['predecessors']:
        assert sha(ROOT / 'predecessors' / row['archive']) == row['sha256']
        verify_index(roots[row['archive']], row['index_sha256'])
    for row in c['frozen_manifests'] + c['result_pins']:
        assert sha(inside(ROOT, row['path'])) == row['sha256'], row['path']
    omissions = {r['path']: r for r in c['omitted_new_object_snapshots']}
    for frozen in c['frozen_manifests']:
        base = Path(frozen['path']).parent
        for row in read(ROOT / frozen['path'])['files']:
            name = (base / row['path']).as_posix()
            if name in omissions:
                assert name.endswith('.olean') and omissions[name]['sha256'] == row['sha256']
                if 'bytes' in row: assert omissions[name]['bytes'] == row['bytes']
                assert not (ROOT / name).exists()
            else: assert sha(inside(ROOT, name)) == row['sha256'], name
    assert sha(args.lean) == c['lean_binary_sha256']
    # Authenticated existing verifier checks all 83 sources/Git blobs, the inherited
    # 89-source and 3-model object bindings, exact Lean version and package Git pins.
    # It verifies/reuses 94 inherited objects. No compiler campaign is invoked.
    inherited = predecessor.verify(args)
    objects = []
    for row in c['runtime_objects']:
        p = getattr(args, row['group']) / Path(*row['module'].split('.')).with_suffix('.olean')
        assert sha(p) == row['sha256'] and p.stat().st_size == row['bytes'], str(p)
        objects.append({**row, 'resolved': str(p)})
    external = args.packages / c['external_object']['package_path']
    assert sha(external) == c['external_object']['sha256']
    object_by_original = {r['original_path']: r for r in objects}
    bindings = []
    historical = []
    for row in c['source_and_evidence_bindings']:
        kind = row['mapping']['kind']
        if kind == 'lean_binary': p = args.lean
        elif kind == 'object_binding':
            if row['mapping'].get('runtime_original_path',row['path']) in object_by_original:
                r = object_by_original[row['mapping'].get('runtime_original_path',row['path'])]
                assert r['sha256'] == row['sha256']
                p = Path(r['resolved'])
            elif row['path'] == c['external_object']['path']: p = external
            else:
                assert row['path'] in omissions and omissions[row['path']]['sha256'] == row['sha256'], row['path']
                historical.append({'path':row['path'],'sha256':row['sha256'],'status':'historical_new_output_omitted_not_rehashed'})
                continue
        else: p = source_path(row, roots)
        assert sha(p) == row['sha256'] and p.stat().st_size == row['bytes'], row['path']
        bindings.append({'original_path':row['path'],'sha256':row['sha256'],'resolved':str(p)})
    mapping = {r['original_path']:r for r in bindings}
    for row in objects:
        if 'source_path' in row: assert mapping[row['source_path']]['sha256'] == row['source_sha256']
    # Review copied-source bindings are literal, not just semantically equivalent.
    for module in ['RawContextUniformity','RawContextControls']:
        assert (ROOT/'hase-raw-context-uniformity-20261010'/(module+'.lean')).read_bytes() == (ROOT/'hase-raw-context-review-20261010/frozen'/(module+'.lean')).read_bytes()
    return {'archive_index_files':count,'inherited':inherited,'runtime_objects':objects,
            'external_object':{'path':str(external),'sha256':sha(external)},'bindings':bindings,
            'omitted_historical_bindings':historical}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ['lean','packages','baseline-objects','scalar-objects','structural-objects','identity-objects','extractor-objects','out']:
        parser.add_argument('--'+flag, required=True, type=Path)
    parser.add_argument('--archive', type=Path, help='Check exact extracted agreement. Independently check the published ZIP SHA-256.')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    for name,value in vars(args).items():
        if isinstance(value,Path):setattr(args,name,value.resolve())
    assert not args.out.exists(), 'Use a new, absent output directory'
    for protected in [ROOT,args.lean.parent.parent,args.packages,args.baseline_objects,args.scalar_objects,args.structural_objects,args.identity_objects,args.extractor_objects]:
        assert not args.out.is_relative_to(protected), 'Output must be outside all frozen input trees'
    verify_index(ROOT)
    archive_entries = archive_matches(args.archive, ROOT) if args.archive else None
    c = read(ROOT/'REUSE_CONTRACT.json')
    args.out.mkdir(parents=True)
    depout = args.out/'predecessors';depout.mkdir()
    roots = extract_predecessors(c, depout)
    args.v3 = roots['hase-type-completion-evidence-20261010-v3.zip']
    args.continuation = roots['hase-source-continuation-20261010.zip']
    extractor = roots['hase-complete-development-extractor-20261010.zip']
    args.v3_archive = ROOT/'predecessors/hase-type-completion-evidence-20261010-v3.zip'
    args.continuation_archive = ROOT/'predecessors/hase-source-continuation-20261010.zip'
    args.prerequisite_objects = args.baseline_objects
    args.closed_objects = args.scalar_objects
    previous = load_verifier(extractor)
    before = verify(args,c,roots,previous)
    print('PASS: source/evidence closure, exact Lean, package revisions, 103 retained project objects and one external Mathlib object',flush=True)
    if args.verify_only:
        receipt={'status':'PASS_HASH_VERIFICATION_ONLY','kernel_compilations':0,'verification':before}
        (args.out/'VERIFY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        return
    baseline=args.out/'baseline-lib';baseline.mkdir()
    rawprereq=args.out/'raw-prerequisite-lib';rawprereq.mkdir()
    copies=[]
    for row in before['runtime_objects']:
        # Isolated paths keep inherited Controls/DependencyAudit out of the type
        # lane and prevent broad historical directories shadowing new modules.
        base=baseline if row['group']=='baseline_objects' else rawprereq
        dst=base/Path(*row['module'].split('.')).with_suffix('.olean')
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(row['resolved'],dst)
        assert sha(dst)==row['sha256']
        copies.append({'path':str(dst),'sha256':row['sha256']})
    packages=[args.packages/p['name']/'.lake/build/lib/lean' for p in before['inherited']['pinned_packages']]
    packages=[p for p in packages if p.is_dir()]
    # Lean resolves a namespace at its first root. Fill around the two exact
    # inherited Mathlib overrides with read-only links to pinned package builds.
    def fill(source,target):
        for entry in source.iterdir():
            dst=target/entry.name
            if not dst.exists():dst.symlink_to(entry,target_is_directory=entry.is_dir())
            elif entry.is_dir() and dst.is_dir():fill(entry,dst)
    fill(args.packages/'mathlib/.lake/build/lib/lean/Mathlib',baseline/'Mathlib')
    records=[]; negatives=[]
    for lane in ['type','raw']:
        stage=args.out/(lane+'-sources');stage.mkdir()
        lib=args.out/(lane+'-lib');lib.mkdir()
        libs=[lib]+([rawprereq] if lane=='raw' else [])+[baseline]+packages
        env={**os.environ,'LEAN_PATH':':'.join(map(str,libs)),'PYTHONDONTWRITEBYTECODE':'1'}
        for row in c['fresh_compilation_scope']:
            if row['lane']!=lane:continue
            source=inside(ROOT,row['path']);assert sha(source)==row['sha256']
            copied=stage/source.name;shutil.copy2(source,copied);assert sha(copied)==row['sha256']
            clean=previous.clean_code(copied.read_text())
            assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',clean),row['module']
            obj=lib/(row['module']+'.olean')
            command=[str(args.lean),'--trust=0','-o',str(obj),str(copied)]
            started=time.monotonic()
            proc=subprocess.run(command,cwd=stage,env=env,capture_output=True,text=True,timeout=600)
            log=proc.stdout+proc.stderr
            logfile=args.out/(lane+'-'+row['module']+'.log');logfile.write_text(log)
            rec={**row,'command':command,'exit_code':proc.returncode,'trust_zero':True,'elapsed_seconds':time.monotonic()-started,'log_path':str(logfile.relative_to(args.out)),'log_sha256':sha(logfile)}
            if row['expected']=='rejection':
                assert proc.returncode!=0 and 'error:' in log and not obj.exists(),(row['module'],log)
                assert 'sorryAx' not in log
                negatives.append(rec)
                print(row['module'],'EXPECTED REJECTION',flush=True)
            else:
                assert proc.returncode==0 and obj.exists(),(row['module'],log)
                assert not any(x in log for x in ['error:','warning:','sorryAx']),(row['module'],log)
                axioms=set()
                for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
                    axioms.update(filter(None,re.sub(r'\s+','',match).split(',')))
                assert axioms <= {'propext','Quot.sound','Classical.choice'},(row['module'],axioms)
                rec.update(object_sha256=sha(obj),reported_axioms=sorted(axioms))
                records.append(rec)
                print(row['module'],'PASS',flush=True)
    after=verify(args,c,roots,previous)
    assert before==after
    for row in copies:assert sha(Path(row['path']))==row['sha256']
    receipt={'status':'PASS_FRESH_EXTRACTED_NEW_MODULE_REPLAY','archive_entries':archive_entries,
             'lean_version':before['inherited']['lean_version'],'lean_binary_sha256':sha(args.lean),
             'source_pin':c['source_pin'],'mathlib_revision':c['mathlib_revision'],
             'inherited_project_objects_rehashed':len(before['runtime_objects']),'external_mathlib_objects_rehashed':1,
             'inherited_83_sources_rehashed':83,'inherited_modules_recompiled':0,
             'fresh_positive_modules':records,'fresh_negative_controls':negatives,
             'before_after_verification_equal':True,'source_and_evidence_bindings_verified':len(before['bindings']),
             'omitted_historical_new_objects_not_claimed_rehashed':before['omitted_historical_bindings'],
             'verification':before,'source_only_fresh_machine_build_certified':False,
             'repository_changes':False,'integration':False,'owner_acceptance':False,'T20_closure':False,
             'limits':c['limits']}
    (args.out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: fresh new-module replay; inherited modules recompiled: 0',flush=True)


if __name__=='__main__':main()
