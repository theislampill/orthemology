from pathlib import Path
import json,hashlib,datetime
r=Path(__file__).resolve().parent
rows=json.loads((r/'INPUT_BINDINGS.json').read_text())
checks=[]
for x in rows:
 original=r.parent/x['source_path'];copy=r/x['copy_path']
 for kind,p in [('inherited_original',original),('retained_copy',copy)]:
  actual=hashlib.sha256(p.read_bytes()).hexdigest()
  checks.append(dict(check=kind,path=str(p.relative_to(r.parent)),expected=x['sha256'],actual=actual,pass_=actual==x['sha256']))
for n,(a,b) in {'1271':(1118,1132),'920':(1118,1133),'921':(1118,1126),'922':(1118,1121),'1270':(1127,1128)}.items():
 lines=(r/'sources'/f'dar-{n}.txt').read_text().splitlines()
 expected='\n'.join(f'L{k:04d}: {lines[k-1]}' for k in range(a,b+1))+'\n'
 checks.append(dict(check='exact_selected_range',source=f'dar-{n}.txt',range=[a,b],pass_=expected==(r/'sources'/f'SELECTED_dar-{n}.txt').read_text()))
for x in json.loads((r/'sources'/'ACQUISITION.json').read_text()):
 actual=hashlib.sha256((r/'sources'/f"dar-{x['id']}.html").read_bytes()).hexdigest()
 checks.append(dict(check='download_binding',id=x['id'],pass_=actual==x['sha256']))
out={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_pass':all(x['pass_'] for x in checks),'checks':checks,'meaning':'Byte bindings, inherited nonmutation and extract fidelity only; not philosophical correctness or historical witness authentication'}
(r/'AUTHOR_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
manifest=[]
for p in sorted(r.rglob('*')):
 if p.is_file() and p.name not in ('MANIFEST.json',):
  data=p.read_bytes();manifest.append({'path':str(p.relative_to(r)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(r/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'all_pass':out['all_pass'],'checks':len(checks),'report_sha256':hashlib.sha256((r/'REPORT.md').read_bytes()).hexdigest(),'manifest_sha256':hashlib.sha256((r/'MANIFEST.json').read_bytes()).hexdigest()},indent=2))
assert out['all_pass']
