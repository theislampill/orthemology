#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys
root=pathlib.Path(__file__).resolve().parent
binding=json.loads((root/'SOURCE_BINDING.json').read_text())
results=[]
for entry in binding['inputs']:
    p=root/entry['copy']
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if digest!=entry['sha256'] or p.stat().st_size!=entry['bytes']:
        raise SystemExit('Input copy mismatch: '+str(p))
    original=pathlib.Path(entry['source'])
    state='original not present; bound copy verified'
    if original.exists():
        if hashlib.sha256(original.read_bytes()).hexdigest()!=digest:
            raise SystemExit('Original changed: '+str(original))
        state='original and copy verified identical'
    results.append({'copy':entry['copy'],'sha256':digest,'status':state})
for p in list(root.glob('*.lean'))+list((root/'dependencies').glob('*.lean'))+list((root/'tests').glob('*.lean')):
    s=p.read_text()
    for pattern in [r'\bsorry\b',r'\badmit\b',r'\bnative_decide\b',r'^\s*axiom\s',r'^\s*unsafe\s']:
        if re.search(pattern,s,re.M): raise SystemExit('Forbidden proof device in '+str(p))
lean=pathlib.Path('private-locator:cb50f30cfa35bdf3a0cf')
if lean.exists() and hashlib.sha256(lean.read_bytes()).hexdigest()!=binding['lean_sha256']:
    raise SystemExit('Official compiler hash mismatch')
result={'status':'PASS','inputs':results,'forbidden_proof_devices':'none'}
pathlib.Path(sys.argv[1]).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
