"""Independent wrapper controls against an explicitly supplied extracted package."""
from pathlib import Path
import argparse, importlib.util, json, os, shutil, subprocess, sys, tempfile

sys.dont_write_bytecode = True
p = argparse.ArgumentParser()
p.add_argument('--checkpoint', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
checkpoint = a.checkpoint.resolve()
spec = importlib.util.spec_from_file_location('reviewed_wrapper', checkpoint / 'replay.py')
wrapper = importlib.util.module_from_spec(spec); spec.loader.exec_module(wrapper)
results = []

def rejected(call, text):
    try: call()
    except RuntimeError as exc:
        assert text in str(exc), str(exc)
    else: raise AssertionError('Expected rejection')

with tempfile.TemporaryDirectory() as temporary:
    temp = Path(temporary)
    protected = temp / 'protected'; protected.mkdir()
    alias = temp / 'alias'; alias.symlink_to(protected, target_is_directory=True)
    rejected(lambda: wrapper.require_fresh_output(alias / 'new', [protected]), 'protected')
    assert not (protected / 'new').exists()
    results.append('Resolved output-parent symlink cannot enter a protected tree')
    broken = temp / 'broken'; broken.symlink_to(temp / 'absent')
    rejected(lambda: wrapper.require_fresh_output(broken, []), 'must be absent')
    results.append('Broken output symlink is rejected')
    names = wrapper.EXPECTED_CACHE_PACKAGES + wrapper.UNUSED_PINNED_PACKAGES
    dependency = temp / 'dependency'; dependency.mkdir()
    (dependency / 'lake-manifest.json').write_text(json.dumps({'packages': [{'name': n} for n in names]}))
    caches = []
    for name in wrapper.EXPECTED_CACHE_PACKAGES:
        cache = dependency / '.lake/packages' / name / '.lake/build/lib/lean'
        cache.mkdir(parents=True); caches.append(cache)
    for cache in caches:
        cache.rmdir()
        rejected(lambda: wrapper.pinned_dependency_caches(dependency), 'Required pinned package cache is missing')
        cache.mkdir()
    results.append('Each of the seven required package caches independently fails closed when missing')
    (dependency / '.lake/packages/Cli/.lake/build/lib/lean').mkdir(parents=True)
    unused_extra = dependency / '.lake/packages/notListed/.lake/build/lib/lean'; unused_extra.mkdir(parents=True)
    _, actual, unused = wrapper.pinned_dependency_caches(dependency)
    assert actual == caches and unused['Cli']['cache_present']
    assert unused_extra not in actual and not any('/Cli/' in str(q) for q in actual)
    results.append('Present unused Cli and unlisted package caches are excluded from the import path')
    (dependency / 'lake-manifest.json').write_text(json.dumps({'packages': [{'name': n} for n in names + ('aesop',)]}))
    rejected(lambda: wrapper.pinned_dependency_caches(dependency), 'package set differs')
    results.append('Duplicate dependency package identity is rejected')
    duplicate_records = [{'path': 'x'}, {'path': 'x'}]
    rejected(lambda: wrapper.exact_inventory(temp, duplicate_records, 'manifest'), 'Duplicate public manifest')
    results.append('Duplicate public inventory path is rejected')
    copied = temp / 'checkpoint'; shutil.copytree(checkpoint, copied)
    original = wrapper.ROOT
    wrapper.ROOT = copied
    try:
        (copied / 'unexpected-empty-directory').mkdir()
        rejected(wrapper.verify_checkpoint, 'Unlisted checkpoint directory')
        (copied / 'unexpected-empty-directory').rmdir()
        target = copied / 'review/REFERENCE_CLOCK_V6_RECEIPT.json'
        old = target.read_text(); changed = json.loads(old); changed['candidate_manifest_sha256'] = '0' * 64
        target.write_text(json.dumps(changed))
        rejected(wrapper.verify_checkpoint, 'Independent review receipt changed')
        target.write_text(old)
    finally: wrapper.ROOT = original
    results.append('Actual package verifier rejects empty extra directories and altered review identity')
    existing = temp / 'existing'; existing.mkdir(); sentinel = existing / 'sentinel'; sentinel.write_text('retain')
    command = [sys.executable, '-B', str(checkpoint / 'replay.py'), '--lean', '/absent-lean',
               '--mathlib', '/absent-mathlib', '--output', str(existing)]
    run = subprocess.run(command, cwd=temp, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=15)
    assert run.returncode != 0 and 'Output path must be absent' in run.stdout
    assert sentinel.read_text() == 'retain' and list(existing.iterdir()) == [sentinel]
    results.append('Actual CLI rejects existing output before compiler/dependency access and preserves sentinel')
    output = temp / 'not-created'
    for timeout in ['0', '-1', '601', 'nan', 'inf']:
        command[-1] = str(output)
        run = subprocess.run(command + ['--stage-timeout', timeout], cwd=temp, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=15)
        assert run.returncode != 0 and 'Stage timeout must be greater than zero and at most 600' in run.stdout
        assert not output.exists()
    results.append('Actual CLI rejects nonpositive, excessive, nonfinite timeouts before output creation')

identity = wrapper.verify_checkpoint()
data = {'status': 'PASS', 'public_manifest_sha256': identity, 'checks': results,
        'mutations': 'Disposable reviewer-owned fixtures only; extracted package and dependencies unchanged.'}
assert not a.output.exists()
a.output.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps(data, indent=2))
