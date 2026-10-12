from pathlib import Path
import datetime, hashlib, json, re, sys
r = Path(__file__).resolve().parent
p = r.parent / 'productive-origination-target-20261011'
expected_report, expected_manifest = sys.argv[1:3]
h = lambda b: hashlib.sha256(b).hexdigest()
checks=[]
def record(name, passed, **data): checks.append({'check':name, 'pass':bool(passed), **data})
report=(p/'REPORT.md').read_bytes(); manifest=(p/'MANIFEST.json').read_bytes()
record('author_report_pin',h(report)==expected_report,sha256=h(report))
record('author_manifest_pin',h(manifest)==expected_manifest,sha256=h(manifest))
for row in json.loads(manifest):
 b=(p/row['path']).read_bytes()
 record('manifest_member', h(b)==row['sha256'] and len(b)==row['bytes'],path=row['path'],sha256=h(b))
for row in json.loads((p/'INPUT_BINDINGS.json').read_text()):
 original=(p.parent/row['source_path']).read_bytes(); copy=(p/row['copy_path']).read_bytes()
 record('inherited_live_copy_binding', original==copy and h(copy)==row['sha256'] and len(copy)==row['bytes'],id=row['id'],sha256=h(copy))
for ident in (1270,1271,920,921,922):
 lines=(p/'sources'/f'dar-{ident}.txt').read_text().splitlines()
 selected=(p/'sources'/f'SELECTED_dar-{ident}.txt').read_text().splitlines()
 nums=[]; matched=True
 for s in selected:
  m=re.fullmatch(r'L(\d+): (.*)',s); nums.append(int(m.group(1)))
  matched &= lines[nums[-1]-1] == m.group(2)
 record('selected_source_text_and_continuity',matched and nums==list(range(nums[0],nums[-1]+1)),id=ident,range=[nums[0],nums[-1]],paragraphs=len(nums))
for row in json.loads((p/'sources/ACQUISITION.json').read_text()):
 b=(p/'sources'/f"dar-{row['id']}.html").read_bytes()
 record('source_download_binding',h(b)==row['sha256'] and len(b)==row['bytes'],id=row['id'],sha256=h(b))
# The report and all manifest-bound files must still be stable at the end.
record('author_pins_stable',h((p/'REPORT.md').read_bytes())==expected_report and h((p/'MANIFEST.json').read_bytes())==expected_manifest)
out={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_pass':all(c['pass'] for c in checks),'check_count':len(checks),'author_report_sha256':expected_report,'author_manifest_sha256':expected_manifest,'checks':checks,'scope':'Independent byte identity, source-selection continuity and inherited-copy binding only. Does not authenticate a historical witness, prove philosophical premises, or run Lean.'}
(r/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
(r/'REVIEWED_AUTHOR_MANIFEST.json').write_bytes(manifest)
print(json.dumps({k:out[k] for k in ('verified_utc','all_pass','check_count','author_report_sha256','author_manifest_sha256')},indent=2))
if not out['all_pass']: sys.exit(1)
