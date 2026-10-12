#!/usr/bin/env python3
"""Independent semantic controls and complete actual import-closure binding."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, time

R = Path(__file__).resolve().parent
W = R.parent
L = R / 'replay'
C = R / 'controls'
A = W / 'full-functional-lean-20261010'
leanroot = W / '.toolchains/lean-4.19.0-linux'
lean = leanroot / 'bin/lean'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
paths = (R/'lean_path.txt').read_text().strip().split(':')
env = dict(os.environ, LEAN_PATH=':'.join(paths))

# Author packet is checked as evidence, not executed by this driver.
manifest_digest = '9019e221673e39162216e2d5538ce836ec3d89c07e8350f13e11368b5b5ae8c6'
assert sha(A/'FROZEN_MANIFEST.json') == manifest_digest
packet_files = json.loads((A/'FROZEN_MANIFEST.json').read_text())['files']
for name,digest in packet_files.items():
    assert sha(A/name) == digest, name
source_freeze = json.loads((A/'SOURCE_FREEZE.json').read_text())['sources']
for name,digest in source_freeze.items():
    assert sha(A/name) == sha(R/'frozen-target'/name) == sha(L/name) == digest

schur = (R/'frozen-target/Schur.lean').read_text()
old = 'extendA A v (1 + v ⬝ᵥ w)'
assert schur.count(old) == 2
(C/'FalseSchurNoSlack.lean').write_text(schur.replace(old,'extendA A v (v ⬝ᵥ w)'))

names = ['PositiveChecks','FalseWitnessPositive','FalseZeroStrict','FalseArbitraryMomentPositive',
         'FalsePremiseErasure','FalseScalarPolynomialIdentity','FalseFiniteCutoffStrict','FalseSchurNoSlack']
records = []
for name in names:
    source = C/(name+'.lean')
    local = L/source.name
    shutil.copyfile(source,local)
    cmd = [str(lean),'--trust=0']
    if name == 'PositiveChecks':
        obj = L/(name+'.olean')
        if obj.exists(): obj.unlink()
        cmd += ['-o',str(obj)]
    cmd += [str(local)]
    start = time.monotonic()
    p = subprocess.run(cmd,cwd=L,env=env,text=True,capture_output=True,timeout=600)
    out = p.stdout+p.stderr
    log = L/(name+'.log')
    log.write_text(out)
    if name == 'PositiveChecks':
        assert p.returncode == 0 and 'error:' not in out, out
        ax = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)
        assert len(ax) == 4
        for theorem,used in ax:
            assert set(map(str.strip,used.split(','))) <= {'propext','Classical.choice','Quot.sound',''}
    else:
        assert p.returncode != 0 and 'error:' in out, (name,out)
        assert any(x in out for x in ['unsolved goals','type mismatch','tactic','failed to find a contradiction']), (name,out)
        assert not any(x in out for x in ['unknown module','does not exist','unknown identifier','unexpected token']), (name,out)
    records.append({'name':name,'status':'PASS' if name=='PositiveChecks' else 'EXPECTED_REJECTION',
                    'exit_status':p.returncode,'command':cmd,'source_sha256':sha(source),'log_sha256':sha(log),
                    'elapsed_seconds':round(time.monotonic()-start,3)})
    print(name+': '+records[-1]['status'],flush=True)

# Modules are taken from the actual successfully imported environment, not a
# guessed textual-import traversal. Bind existing sources and imported objects;
# only the seven local author modules were freshly built from those sources.
imports = re.findall(r'^REVIEW_IMPORT (.+)$',(L/'PositiveChecks.log').read_text(),re.M)
assert len(imports) == len(set(imports))
closure = []
search = [Path(p) for p in paths] + [leanroot/'lib/lean']
for module in imports:
    relative = Path(*module.split('.')).with_suffix('.olean')
    matches = [p/relative for p in search if (p/relative).is_file()]
    assert len(matches) == 1, (module,matches)
    obj = matches[0]
    if obj.is_relative_to(L):
        source = obj.with_suffix('.lean')
        origin = 'independently rebuilt local source'
    elif '/.lake/build/lib/lean/' in str(obj):
        root,rel = str(obj).split('/.lake/build/lib/lean/',1)
        source = Path(root)/Path(rel).with_suffix('.lean')
        origin = 'retained dependency source and object; no baseline rebuild'
    else:
        source = leanroot/'src/lean'/obj.relative_to(leanroot/'lib/lean').with_suffix('.lean')
        origin = 'retained Lean standard-library source and object'
    assert source.is_file(), str(source)
    closure.append({'module':module,'source':str(source),'source_sha256':sha(source),
                    'object':str(obj),'object_sha256':sha(obj),'object_bytes':obj.stat().st_size,'origin':origin})
(R/'IMPORT_CLOSURE.json').write_text(json.dumps(closure,indent=2)+'\n')

binary_bindings = []
for binary in [lean,*(leanroot/'lib/lean').glob('*shared*.so')]:
    binary_bindings.append({'path':str(binary),'sha256':sha(binary),'bytes':binary.stat().st_size})
for name,digest in source_freeze.items():
    assert sha(A/name) == digest
for name,digest in packet_files.items():
    assert sha(A/name) == digest, name
receipt = {'status':'PASS_INDEPENDENT_SEMANTIC_CONTROLS','author_manifest_sha256':manifest_digest,
           'records':records,'import_modules':len(closure),'import_closure_sha256':sha(R/'IMPORT_CLOSURE.json'),
           'axioms_positive_checks':ax,'binary_bindings':binary_bindings,'driver_sha256':sha(Path(__file__)),
           'no_baseline_rebuild':True,'author_sources_unchanged':True,
           'author_packet_files_verified_unchanged':len(packet_files),
           'ordinary_proof_sha256':'08fdec67591a4a0639fa4ca721293bd8c480ec405dcd1a7c5a08d3244aa84c80'}
(R/'CONTROL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: '+str(len(imports))+' actual imported modules bound',flush=True)
