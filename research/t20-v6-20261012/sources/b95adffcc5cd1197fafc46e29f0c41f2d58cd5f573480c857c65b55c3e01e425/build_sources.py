#!/usr/bin/env python3
import hashlib, json, os, pathlib, re, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
LEAN = WORKSPACE / '.toolchains/lean-4.19.0-linux/bin/lean'
PACKAGE_BASE = WORKSPACE / 'separating-projection-lean-20261009/.lake/packages'
OUT = pathlib.Path(os.environ.get('BUILD_OUT', str(ROOT / 'build/lib'))).resolve()
OUT.mkdir(parents=True, exist_ok=True)
LIBS = [p / '.lake/build/lib/lean' for p in PACKAGE_BASE.iterdir() if p.is_dir()]
# Lean resolves a module namespace in its first matching root. Overlay existing
# Mathlib objects by read-only symlinks, then build only the two absent modules.
mathlib_base = PACKAGE_BASE / 'mathlib/.lake/build/lib/lean/Mathlib'
for source in mathlib_base.rglob('*'):
    if source.is_file():
        target = OUT / 'Mathlib' / source.relative_to(mathlib_base)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists(): target.symlink_to(source)

ENV = {**os.environ, 'LEAN_PATH': ':'.join(map(str, [OUT] + LIBS))}
ACQ = json.loads((ROOT / 'ACQUISITION.json').read_text())
BY_MODULE = {x['module']: x for x in ACQ['sources']}
assert not ACQ['missing']
for m, x in BY_MODULE.items():
    b = (ROOT / 'sources' / (m + '.lean')).read_bytes()
    assert hashlib.sha256(b).hexdigest() == x['sha256'], m
    assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == x['git_blob'], m
records = []
log = (ROOT / 'validation/SOURCE_BUILD.log').open('w')
log.write(subprocess.check_output([str(LEAN), '--version'], text=True))

def build(module, source, cwd):
    dest = OUT / pathlib.Path(*module.split('.')).with_suffix('.olean')
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(LEAN), '-o', str(dest), str(source)]
    start = time.time()
    p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)
    log.write('$ ' + ' '.join(cmd) + '\n' + p.stdout + p.stderr); log.flush()
    records.append({'module': module, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                    'exit_code': p.returncode, 'seconds': round(time.time()-start, 3)})
    print(module, p.returncode, flush=True)
    if p.returncode:
        (ROOT / 'validation/SOURCE_BUILD.json').write_text(json.dumps({'status':'FAIL','modules':records},indent=2)+'\n')
        print(p.stdout + p.stderr)
        sys.exit(p.returncode)

for x in json.loads((ROOT / 'EXTERNAL_BUILD_PLAN.json').read_text()):
    source = WORKSPACE / x['source']
    build(x['module'], source, PACKAGE_BASE / 'mathlib')

seen = set()
def visit(module):
    if module in seen or module not in BY_MODULE: return
    seen.add(module)
    for dep in BY_MODULE[module]['imports']: visit(dep)
    build(module, ROOT / 'sources' / (module + '.lean'), ROOT / 'sources')
visit(ACQ['root'])
assert len(seen) == len(BY_MODULE)
(ROOT / 'validation/SOURCE_BUILD.json').write_text(json.dumps({'status':'PASS','modules':records},indent=2)+'\n')
print('PASS exact original closure:', len(seen), 'modules plus', len(records)-len(seen), 'external modules', flush=True)
