#!/usr/bin/env python3
"""Check exact source locks, preserved predecessors, complete roots and pins."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(records):
    for r in records:
        p=ROOT/r['path']
        assert p.is_file(),f"Missing locked input: {r['path']}"
        assert digest(p)==r['sha256'],f"Source digest mismatch: {r['path']}"

def without_comments(s):
    out=[];i=0;depth=0
    while i<len(s):
        if depth:
            if s.startswith('/-',i):depth+=1;i+=2
            elif s.startswith('-/',i):depth-=1;i+=2
            else:i+=1
        elif s.startswith('/-',i):depth=1;i+=2
        elif s.startswith('--',i):
            end=s.find('\n',i);i=len(s) if end<0 else end
        else:out.append(s[i]);i+=1
    assert depth==0,'Unclosed comment'
    return ''.join(out)
lock=json.loads((ROOT/'verification/source-lock.json').read_text())
verify(lock['files'])
for name in lock['new_modules']:
    body=without_comments((ROOT/(name+'.lean')).read_text())
    body=re.sub(r'"(?:\\.|[^"\\])*"', '""', body)
    bad=re.search(r'\b(sorry|admit|axiom|unsafe|partial)\b',body)
    assert not bad,f'Forbidden new-source token in {name}: {bad.group() if bad else ""}'
expected=set(json.loads((ROOT/'MODULES.json').read_text()))
actual={p.stem for p in ROOT.glob('*.lean') if p.name!='lakefile.lean'}
assert actual==expected, f'Unexpected or missing module: {actual^expected}'
roots=set(re.findall(r'`([A-Za-z][A-Za-z0-9_.]*)',(ROOT/'lakefile.lean').read_text()))
assert roots==expected|{'verification.KernelAudit'},f'Lake default-root coverage changed: {roots^expected}'
lakefile=(ROOT/'lakefile.lean').read_text()
default_blocks=re.findall(r'@\[default_target\]\s*lean_lib\s+\w+\s+where\s+roots\s*:=\s*#\[(.*?)\]',lakefile,re.S)
default_roots={n for block in default_blocks for n in re.findall(r'`([A-Za-z][A-Za-z0-9_.]*)',block)}
assert default_roots==expected,f'Lake default-root coverage changed: {default_roots^expected}'
manifest=json.loads((ROOT/'lake-manifest.json').read_text())
assert {p['name']:p['rev'] for p in manifest['packages']}==lock['dependency_revisions']
assert 'c44e0c8ee63ca166450922a373c7409c5d26b00b' in (ROOT/'lakefile.lean').read_text()
assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.19.0'
preserved=json.loads((ROOT/'verification/preserved-module-lock.json').read_text())
assert len(preserved)==88 and sum(r['source']=='unified-v3' for r in preserved)==76
verify(preserved)
for p,h in {'raw-v2-receipt.json':'24db3eb238d712fa242cb5c71a5c074d70a4a52434d34b41ada2f3d731327082','unified-v3-receipt.json':'53cd30a370c0f94db9fc211d2005637af204cc5197e88f30c7edcbfed6a52a27', 'unified-v4-receipt.json':'3ab3b08b87aef587b2b6dd3964f6a884fb90c3b547511157b73275ebe4f7d637'}.items():
    assert digest(ROOT/'verification/historical'/p)==h, f'Historical receipt changed: {p}'
for name in ['AllProjectProofAudit.lean','ExportDeclarationInventory.lean']:
    text=(ROOT/'verification'/name).read_text()
    selected=text.split('def modules : Array Name := #[',1)[1].split(']',1)[0]
    audited=set(re.findall(r'`([A-Za-z][A-Za-z0-9_.]*)',selected))
    assert audited==expected,f'Complete module audit coverage changed: {name}'
print('SOURCE_IDENTITY_PASS: 88 roots; 86 preserved v4 modules; 2 exact polynomial-test support modules; nine exact dependency pins')
