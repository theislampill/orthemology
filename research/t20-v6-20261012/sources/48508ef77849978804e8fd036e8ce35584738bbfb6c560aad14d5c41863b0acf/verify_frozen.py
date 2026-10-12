#!/usr/bin/env python3
"""Read-only author-packet binding; replay only reviewer-owned copies."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parents[1]
AUTHOR = HERE.parent / 'cooperation'
WORKSPACE = HERE.parents[2]
EXPECTED_MANIFEST = 'ebd5775a8177a33884aceb0f07da982232aed1526dec662ea0330893da3d727b'
LEAN = WORKSPACE / 'tranche20/hase-positive-research/toolchain-preparation/toolchains/lean-4.19.0-linux/bin/lean'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def author_check(manifest):
    assert sha(AUTHOR/'AUTHOR_MANIFEST.json') == EXPECTED_MANIFEST
    for row in manifest['files']:
        p = AUTHOR / row['path']
        assert p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], row['path']
    return len(manifest['files'])

manifest = json.loads((AUTHOR/'AUTHOR_MANIFEST.json').read_text())
before = author_check(manifest)
snapshot = HERE/'frozen-author'
snapshot.mkdir(exist_ok=True)
for row in manifest['files'] + [{'path':'AUTHOR_MANIFEST.json'}]:
    src = AUTHOR/row['path']; dst = snapshot/row['path']
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dst)
replay = HERE/'replay'
(replay/'src').mkdir(parents=True,exist_ok=True)
(replay/'build').mkdir(exist_ok=True)
for p in (snapshot/'src').iterdir():
    if p.suffix in ('.lean','.py'): shutil.copyfile(p,replay/'src'/p.name)
shutil.copyfile(HERE/'src/IndependentScope.lean',replay/'src/IndependentScope.lean')
commands=[]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', LEAN_PATH=str(replay/'build'))
def run(name, args):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
    r=subprocess.run([str(x) for x in args],cwd=replay,env=env,capture_output=True,text=True)
    log=HERE/'receipts'/name
    log.write_text(r.stdout+r.stderr)
    commands.append({'command':[str(x) for x in args],'cwd':str(replay),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':r.returncode,'log':str(log.relative_to(HERE)),'log_sha256':sha(log)})
    assert r.returncode == 0, f'{name}: {r.stdout}{r.stderr}'
    return r

run('lean-version.log',[LEAN,'--version'])
run('author-search-copy.log',[sys.executable,replay/'src/search.py'])
run('author-tests-copy.log',[sys.executable,replay/'src/test_search.py'])
run('author-lean-copy.log',[LEAN,'-o',replay/'build/FixedTarget.olean',replay/'src/FixedTarget.lean'])
run('author-readback-copy.log',[LEAN,replay/'src/Readback.lean'])
run('independent-scope.log',[LEAN,'-o',replay/'build/IndependentScope.olean',replay/'src/IndependentScope.lean'])
run('independent-finite.log',[sys.executable,HERE/'src/independent_checks.py'])
expected=json.loads((snapshot/'results/SEARCH_RESULT.json').read_text())
actual=json.loads((replay/'results/SEARCH_RESULT.json').read_text())
expected.pop('run_utc'); actual.pop('run_utc')
assert expected==actual, 'Semantic replay differs'
for log in ['author-lean-copy.log','author-readback-copy.log','independent-scope.log']:
    assert 'sorryAx' not in (HERE/'receipts'/log).read_text()
after=author_check(manifest)
result={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'author_manifest_sha256':EXPECTED_MANIFEST,'author_files_verified_before':before,'author_files_verified_after':after,
        'author_unchanged':True,'copied_search_semantically_identical_ignoring_run_timestamp':True,
        'toolchain_sha256':sha(LEAN),'commands':commands,
        'scope':'New campaign only; no prior-science replay; source warrant assessed separately in REVIEW.md'}
(HERE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
