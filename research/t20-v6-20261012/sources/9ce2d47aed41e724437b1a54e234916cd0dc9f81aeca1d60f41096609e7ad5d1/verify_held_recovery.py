"""Verify corpus-wide source-byte recovery without changing or running source files."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
CAT=OUT.parent/'catalogue'
summary=CAT/'reconciled_advertised_source_recovery_summary.json'
rows=CAT/'reconciled_advertised_source_recovery.jsonl'
sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads(summary.read_text());a=[json.loads(x) for x in rows.read_text().splitlines() if x.strip()]
matched=0;missing=[];mismatched=[];total=0
for x in a:
 path=x.get('held_actual_object_path')
 if not path:missing.append(x['id']);continue
 b=(BASE/path).read_bytes();total+=len(b)
 if sha(b)!=x['sha256'] or len(b)!=x['bytes']:mismatched.append(x['id'])
 else:matched+=1
if len(a)!=10104 or matched!=10104 or missing or mismatched:raise SystemExit('Full held-corpus source-byte verification incomplete.')
result={'schema':1,'date_utc':'2026-10-11','status':'all_advertised_document_bytes_recovered_in_full_held_corpus','advertised_documents':len(a),'fresh_exact_hash_matches':matched,'missing':missing,'mismatched':mismatched,'bytes_hashed':total,'advertised_copied_paths':s['advertised_copied_paths'],'present_at_advertised_root_path_in_trimmed_zip':s['present_at_advertised_root_path'],'final_recovered_transcript':{'filename':'Pasted markdown(20261010-235350).md','bytes':78807,'sha256':'9d1022f04db0d6d3ddd8b8369ecd8800277b9d5d19e5d0cf2899bff3d805cdb9','publication':'Excluded; only custody metadata recorded here.'},'catalogue_receipts':[{'path':str(p.relative_to(BASE)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in [summary,rows]],'scope':'Mechanical fresh SHA-256 and size verification only. No new semantic reading or execution of recovered programs. The trimmed ZIP still lacks all advertised root source paths and its root manifest. Missing R3 proof/code/log successor remains missing.'}
(OUT/'RECOVERY_ADDENDUM.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
