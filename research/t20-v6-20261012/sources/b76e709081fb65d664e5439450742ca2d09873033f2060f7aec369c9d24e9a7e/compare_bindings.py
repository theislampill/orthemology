#!/usr/bin/env python3
"""Bind the independent snapshot to the complete author seal and prior semantics."""
import pathlib,json,hashlib,sys
root=pathlib.Path(__file__).resolve().parent; receipt=pathlib.Path(sys.argv[1]).resolve();author=pathlib.Path(sys.argv[2]).resolve()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads(receipt.read_text());s=json.loads((author/'UNIFORM_COMPUTABILITY_SEAL.json').read_text())
assert r['status']=='PASS'
files=[{'path':k,'expected':v,'actual':sha(author/k),'matches':sha(author/k)==v} for k,v in s['files'].items()]
author_result_path=next(author/k for k in s['files'] if k.endswith('UNIFORM_COMPUTABILITY_RESULT.json'))
a=json.loads(author_result_path.read_text());c=json.loads((author/'UNIFORM_COMPUTABILITY_SOURCE_CLOSURE.json').read_text())
rows=[{'module':x['module'],'author_sha256':x['sha256'],'independent_sha256':r['sources'][x['module']]['sha256'],'matches':r['sources'][x['module']]['sha256']==x['sha256']} for x in c['sources']]
prior_path=pathlib.Path(sys.argv[3]).resolve() if len(sys.argv)>3 else pathlib.Path('private-locator:b145c2acccece9ba1047');prior=json.loads(prior_path.read_text())
legacy=[{'module':m,'matches_prior_independent_sha256':r['sources'][m]['sha256']==v['sha256']} for m,v in prior['sources'].items() if m in r['sources']]
keys={t['declaration'] for t in a['targets']}
checks={'all_author_seal_files_match':all(x['matches'] for x in files),
 'all_35_author_sources_match':len(rows)==35 and all(x['matches'] for x in rows),
 'all_119_author_theorem_targets_audited':len(keys)==119 and keys<=set(r['axioms']),
 'all_author_target_axioms_match':all(r['axioms'][n]==a['axioms'][n] for n in keys),
 'audit_source_matches_author_receipt':r['sources']['UniformComputabilityAudit']['sha256']==a['audit_sha256'],
 'prior_operational_sources_unchanged':all(x['matches_prior_independent_sha256'] for x in legacy),
 'author_seal_matches_initial_snapshot':sha(author/'UNIFORM_COMPUTABILITY_SEAL.json')==r['author_seal']['sha256'],
 'independent_origins_unchanged':r['origins_unchanged']}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'sealed_files':files,'source_bindings':rows,'legacy_bindings':legacy,'author_receipt_sha256':sha(author_result_path),'independent_receipt_sha256':sha(receipt)}
(root/'SOURCE_BINDING_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':checks},indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
