#!/usr/bin/env python3
"""Independent, isolated trust-zero rebuild of the full functional sources."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, time

R = Path(__file__).resolve().parent
W = R.parent
AUTHOR = W / 'full-functional-lean-20261010'
F = R / 'frozen-target'
L = R / 'replay'
L.mkdir(exist_ok=True)
lean = W / '.toolchains/lean-4.19.0-linux/bin/lean'
names = ['Indexing','Schur','Recurrence','Moment','PolynomialBridge','ScalarSupport','Countermodel']
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
paths = (AUTHOR / 'lean_path.txt').read_text().strip().split(':')
assert paths[0] == str(AUTHOR)
assert all('/.lake/packages/' in p for p in paths[1:])
env = dict(os.environ, LEAN_PATH=':'.join([str(L)] + paths[1:]))
(R / 'lean_path.txt').write_text(env['LEAN_PATH'] + '\n')
manifest = []
for name in names:
    source = F / (name+'.lean')
    assert sha(source) == sha(AUTHOR / source.name), name
    assert not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by|unsafe)\b', source.read_text())
    manifest.append({'name':name,'bytes':source.stat().st_size,'source_sha256':sha(source)})
    shutil.copyfile(source, L / source.name)
(R / 'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
records = []
for name in names:
    obj = L / (name+'.olean')
    if obj.exists(): obj.unlink()
    source = L / (name+'.lean')
    deps = subprocess.run([str(lean),'--deps',str(source)],cwd=L,env=env,text=True,capture_output=True)
    assert deps.returncode == 0, deps.stderr
    bindings = []
    for dependency in deps.stdout.splitlines():
        path = Path(dependency)
        assert path.exists(), str(path)
        assert not str(path).startswith(str(AUTHOR)), str(path)
        bindings.append({'path':str(path),'sha256':sha(path),'bytes':path.stat().st_size})
    cmd = [str(lean),'--trust=0','-o',str(obj),str(source)]
    start = time.monotonic()
    p = subprocess.run(cmd,cwd=L,env=env,text=True,capture_output=True,timeout=600)
    out = p.stdout+p.stderr
    (L / (name+'.log')).write_text(out)
    assert p.returncode == 0, (name,p.returncode,out)
    assert obj.exists()
    axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)
    for theorem, used in axioms:
        assert set(map(str.strip,used.split(','))) <= {'propext','Classical.choice','Quot.sound',''}, (theorem,used)
    records.append({'name':name,'command':cmd,'cwd':str(L),'trust':0,'exit_status':p.returncode,
                    'source_sha256':sha(source),'object_sha256':sha(obj),'log_sha256':sha(L/(name+'.log')),
                    'elapsed_seconds':round(time.monotonic()-start,3),'direct_imports':bindings,
                    'printed_axioms':axioms})
    (R / 'BUILD_PROGRESS.json').write_text(json.dumps(records,indent=2)+'\n')
    print(f'{name}: PASS trust=0 ({records[-1]["elapsed_seconds"]}s)',flush=True)
for name in names:
    assert sha(F / (name+'.lean')) == sha(AUTHOR / (name+'.lean')), name
receipt = {'status':'PASS_FRESH_SEVEN_SOURCE_TRUST_ZERO_REBUILD','records':records,
           'source_manifest_sha256':sha(R/'SOURCE_MANIFEST.json'), 'driver_sha256':sha(Path(__file__)),
           'author_sources_unchanged':True,'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),
           'lean_binary_sha256':sha(lean),'lean_path':env['LEAN_PATH']}
(R / 'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['status'],flush=True)
