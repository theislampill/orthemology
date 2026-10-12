#!/usr/bin/env python3
"""Bounded byte and formula checks; this is not a Lean-import equivalence proof."""
import hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
bindings = json.loads((ROOT / 'SOURCE_BINDINGS.json').read_text())
checked = []
for b in bindings['sources']:
    data = (ROOT / b['local_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == b['sha256'], b['name']
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert blob == b['git_blob'], b['name']
    checked.append({'name': b['name'], 'sha256': b['sha256'], 'git_blob': blob})

def strip_comments(text):
    return re.sub(r'/\-.*?\-/', '', text, flags=re.S)

def body(file, name):
    text = strip_comments(file.read_text())
    start = re.search(r'^def ' + re.escape(name) + r'\b', text, flags=re.M)
    assert start, (file, name)
    tail = text[start.start():]
    next_decl = re.search(r'\n(?:@\[.*?\]\s*)?(?:def|theorem|inductive|structure|namespace|end)\b', tail)
    decl = tail[:next_decl.start()] if next_decl else tail
    # Functions by equations have no :=; their first equation begins with |.
    rhs = decl.split(':=', 1)[1] if ':=' in decl else decl[decl.index('\n  |'):]
    return re.sub(r'\s+', '', rhs.replace('Poly', 'P'))

formula_map = {
    'P01Polynomials.lean': ['freeZero', 'drop', 'abstract', 'pairPoly', 'fstPoly', 'sndPoly'],
    'EffectiveObserver.lean': ['iterationPoly', 'inputNumeral'],
    'EffectivePrimitiveRecursion.lean': ['succBody', 'succPoly'],
    'UArrowAndCompilerControls.lean': ['diagonalStepBody', 'diagonalStep', 'diagonalZero', 'literalPairStateBody'],
}
formulas = []
mirror = ROOT / 'FrozenCompilerMirror.lean'
for filename, names in formula_map.items():
    for name in names:
        source_body, mirror_body = body(ROOT / 'sources' / filename, name), body(mirror, name)
        assert source_body == mirror_body, (filename, name, source_body, mirror_body)
        formulas.append({'source': filename, 'declaration': name, 'normalized_rhs_equal': True})

result = {'source_bytes_and_git_blobs': checked, 'formula_checks': formulas,
          'scope': 'Fourteen formula RHS checks after whitespace and Poly-to-P normalization. No inherited typed source was imported or replayed.'}
(ROOT / 'validation' / 'SOURCE_CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: five pinned source byte/git-blob checks; fourteen compiler formula RHS checks.')
