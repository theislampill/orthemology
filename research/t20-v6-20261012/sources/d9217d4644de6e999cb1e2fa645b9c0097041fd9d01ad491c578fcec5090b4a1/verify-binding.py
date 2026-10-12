import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
review = root / 'review_semantic'
hash_file = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
snapshot = json.loads((review / 'reviewed-source-hashes.json').read_text())
for relative, expected in snapshot.items():
    assert hash_file(root / relative) == expected, ('source changed', relative)
    if relative.endswith('.lean'):
        assert hash_file(review / 'fresh' / relative) == expected, ('review copy changed', relative)
binding = json.loads((root / 'BINDING.json').read_text())
for entry in binding['copies']:
    assert hash_file(root / entry['frozen_copy']) == entry['sha256']
    assert hash_file(root.parent / entry['source']) == entry['sha256']
for entry in binding['environment_inputs']:
    path = root.parent / entry['path']
    assert hash_file(path) == entry['sha256']
    assert path.stat().st_size == entry['bytes']
mathlib = root.parent / 't20-next-frontier-20261008/formal-identification/mathlib'
assert subprocess.check_output(['git', '-C', str(mathlib), 'rev-parse', 'HEAD'], text=True).strip() == binding['mathlib_commit']
log = (review / 'logs/final-replay.log').read_text()
assert log.count('Checked frozen source:') == 11
assert log.count('Checked new source:') == 4
assert log.count('PASS ') == 63
assert 'sorryAx' not in log and 'error:' not in log
assert log.endswith('Replay passed: eleven frozen and four new modules, actual-tree runtime checks twice.\n')
assert (review / 'logs/submitter-mutations.log').read_text().count('PASS ') == 3
assert (review / 'logs/independent-mutations.log').read_text().count('PASS ') == 2
assert (review / 'logs/adverse.log').read_text().count('PASS ') == 12
assert 'Initial local olean count: 0' in (review / 'logs/environment.log').read_text()
print('PASS exact current-source, independent-copy, predecessor, environment, and final-result bindings')
