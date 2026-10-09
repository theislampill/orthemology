#!/usr/bin/env python3
"""Read-only audit of the frozen finite bridge. Writes only reviewer outputs."""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / 'reason-causation-bridge'
FROZEN = '504ef228406a1e9d9e38979df9dfa58f0f3fab4a7551ed944177a2a3e5d29794'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def binding():
    assert sha(STAGE/'MANIFEST.json') == FROZEN
    manifest = json.loads((STAGE/'MANIFEST.json').read_text())
    for rec in manifest['files']:
        p = STAGE/rec['path']
        assert p.stat().st_size == rec['bytes'], rec['path']
        assert sha(p) == rec['sha256'], rec['path']
    return len(manifest['files'])

before = binding()
spec = importlib.util.spec_from_file_location('frozen_bridge', STAGE/'model/check_bridge.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
# Literal truth values are a separately written truth table, not the author's evaluator.
worlds = ((False, False), (False, True), (True, False), (True, True))
truth = ((False, False, True, True), (True, True, False, False),
         (False, True, False, True), (True, False, True, False))
names = ('p', 'not_p', 'q', 'not_q')
counts = dict(bit_packets=0, conditional_cases=0, true_input_cases=0,
              accepted_cases=0, accepted_true_input_cases=0,
              accepted_false_input_cases=0, conditional_failures=0,
              drop_match_true_input_false_output_cases=0,
              drop_first_true_input_false_output_cases=0)
single_bit_output_changes = [0]*9
single_bit_accepted_derivation_changes = [0]*9
accepted_derivation = lambda o: (bool(o[0]), (o[1],o[2]) if o[0] else None)
for bits in itertools.product((0,1), repeat=9):
    A,B,C = (bits[i] + 2*bits[i+1] for i in (0,2,4))
    enabled1, enabled2 = bool(bits[6]), bool(bits[7])
    expected = (int(enabled1 and enabled2 and A == B), bits[4], bits[5])
    got = m.microstep(bits)
    assert got == expected
    assert m.abstraction(bits) == (names[A], names[B], names[C], enabled1, enabled2)
    assert m.decode_output(got) == (bool(expected[0]), names[C])
    assert m.macrostep(m.abstraction(bits)) == (bool(expected[0]), names[C])
    counts['bit_packets'] += 1
    for k in range(9):
        changed = list(bits); changed[k] = 1-changed[k]
        changed_out = m.microstep(changed)
        single_bit_output_changes[k] += changed_out != got
        single_bit_accepted_derivation_changes[k] += accepted_derivation(changed_out) != accepted_derivation(got)
    for w in range(4):
        inp = (not enabled1 or truth[A][w]) and (not enabled2 or not truth[B][w] or truth[C][w])
        out = not bool(got[0]) or truth[C][w]
        counts['conditional_cases'] += 1
        counts['true_input_cases'] += inp
        counts['accepted_cases'] += bool(got[0])
        counts['accepted_true_input_cases'] += bool(got[0]) and inp
        counts['accepted_false_input_cases'] += bool(got[0]) and not inp
        counts['conditional_failures'] += inp and not out
        assert m.input_correct(m.abstraction(bits), worlds[w]) == inp
        assert m.output_correct(m.decode_output(got), worlds[w]) == out
        for key, kw in [('drop_match', {'drop_match':True}), ('drop_first', {'drop_first':True})]:
            bad = m.microstep(bits, **kw)
            counts[key+'_true_input_false_output_cases'] += inp and bool(bad[0]) and not truth[C][w]
assert counts['conditional_cases'] == 2048
assert counts['conditional_failures'] == 0
assert counts['accepted_true_input_cases'] == 32
assert counts['drop_match_true_input_false_output_cases'] > 0
assert counts['drop_first_true_input_false_output_cases'] > 0
assert all(n > 0 for n in single_bit_output_changes[:8])
assert single_bit_output_changes[8] == 0

# Execute the author's test function without the __main__ file rewrite.
actual = json.loads(json.dumps(m.run()))
assert actual == json.loads((STAGE/'model/RESULTS.json').read_text())
assert (STAGE/'results/model_check.log').read_bytes() == (STAGE/'model/RESULTS.json').read_bytes()
# Independently inspect its coupled source-error control.
base = (0,0,0,0,0,1,1,1,0)
a,b = (True, True, False), (True, False, True)
for p,q,error in (a,b):
    assert p and ((not p or q) or error)
    assert m.microstep(base) == (1,0,1)
assert a[1] != b[1]
after = binding()
assert before == after
inputs = json.loads((STAGE/'INPUT_BINDINGS.json').read_text())['files']
for rec in inputs:
    assert sha(HERE.parent.parent/rec['path']) == rec['sha256'], rec['path']
result = {'reviewed_manifest_sha256': FROZEN, 'payload_hashes_before_and_after': before,
          'counts': counts, 'single_bit_output_changes_over_512_packets': single_bit_output_changes,
          'single_bit_accepted_derivation_changes': single_bit_accepted_derivation_changes,
          'predecessor_hash_bindings_verified': len(inputs),
          'saved_results_equal': True, 'author_tree_unchanged': True,
          'limits': ['Finite declared equations only; no device physics or human-cognition experiment.',
                     'Conditional soundness is not completeness, warrant, content origin or a reliability probability.',
                     'Single-bit intervention counts are directed finite comparisons, not frequencies of natural processes.']}
print(json.dumps(result, indent=2, sort_keys=True))
