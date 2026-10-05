#!/usr/bin/env python3
"""Fail-closed source identities, registration, syntax, pins, and proof-token audit."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def strip_comments_and_strings(text):
    out, i, nesting = [], 0, 0
    while i < len(text):
        if nesting:
            if text.startswith('/-', i): nesting += 1; i += 2
            elif text.startswith('-/', i): nesting -= 1; i += 2
            else: i += 1
        elif text.startswith('/-', i): nesting = 1; i += 2
        elif text.startswith('--', i):
            n = text.find('\n', i); i = len(text) if n < 0 else n
        elif text[i] == '"':
            i += 1
            while i < len(text):
                if text[i] == '\\': i += 2
                elif text[i] == '"': i += 1; break
                else: i += 1
            out.append(' ')
        else: out.append(text[i]); i += 1
    assert nesting == 0, 'Unclosed block comment'
    return ''.join(out)

lock = json.loads((ROOT/'verification/source-lock.json').read_text())
assert [len(lock[k]) for k in ('baseline', 'intensional', 'extensional')] == [53, 6, 6]
records = lock['baseline'] + lock['intensional'] + lock['extensional']
expected = {r['file']: r['sha256'] for r in records}
assert len(expected) == 65
assert {p.name for p in ROOT.glob('*.lean') if p.name != 'lakefile.lean'} == set(expected)
for name, digest in expected.items():
    assert sha256(ROOT/name) == digest, f'Frozen source changed: {name}'
    code = strip_comments_and_strings((ROOT/name).read_text())
    bad = re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', code)
    assert not bad, f'Forbidden proof token in {name}: {bad}'
base = (ROOT/'AllSyntax.lean').read_text().split('mutual\n', 1)[1].split('\nend', 1)[0]
plus = (ROOT/'IntensionalIdentityBridge.lean').read_text().split('mutual\n', 1)[1].split('\nend', 1)[0]
for old, new in [('P01DF.PolyConv','PolyConvPlus'), ('Ctx','CtxPlus'), ('Form','FormPlus'), ('Has','HasPlus')]:
    base = re.sub(r'(?<![\w])'+re.escape(old)+r'(?![\w])', new, base)
assert base == plus, 'Unexpected original-to-Plus grammar change'
repair = (ROOT/'ExtensionalRepairSyntax.lean').read_text()
retained = repair.split('mutual\n',1)[1].split('    /-- Exactly §3.1',1)[0].rstrip()
core = plus.replace('CtxPlus','CtxE').replace('FormPlus','FormE').replace('HasPlus','HasE').rstrip()
assert retained == core, 'Unexpected retained Plus-to-E grammar change'
assert 'inductive PolyConv' not in strip_comments_and_strings(repair)
assert re.findall(r'^    \| (\w+) :', repair.split('    /-- Exactly §3.1',1)[1].split('\nend',1)[0], re.M) == ['piExt','allExt']
lake = (ROOT/'lakefile.lean').read_text()
roots = re.findall(r'`(\w+)', lake)
assert len(roots) == len(set(roots)) == 65
assert set(roots) == {Path(p).stem for p in expected}
assert lake.count('@[default_target]') == 3
assert '../' not in lake and ' from git ' in lake
assert (ROOT/'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.19.0'
manifest = json.loads((ROOT/'lake-manifest.json').read_text())
assert {d['name']:(d['rev'],d['url'],d['type']) for d in manifest['packages']} == {
    d['name']:(d['revision'],d['official_origin'],'git') for d in lock['dependencies']}
assert all(d['type'] == 'git' and d['url'].startswith('https://github.com/') for d in manifest['packages'])
assert len(manifest['packages']) == 9
print('SOURCE_AUDIT_PASS: 53 unchanged baseline + 6 frozen intensional + 6 frozen extensional modules; all 65 registered; exact retained grammars; 9 official Git pins; no forbidden proof tokens.')
