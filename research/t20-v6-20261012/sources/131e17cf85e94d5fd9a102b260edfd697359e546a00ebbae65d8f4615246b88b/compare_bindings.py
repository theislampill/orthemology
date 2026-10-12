#!/usr/bin/env python3
"""Bind the new matrix award to its own seal and both unchanged prior subjects."""
import pathlib,json,hashlib,sys
root=pathlib.Path(__file__).resolve().parent;receipt=pathlib.Path(sys.argv[1]).resolve();author=pathlib.Path(sys.argv[2]).resolve();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads(receipt.read_text());assert r['status']=='PASS'
sealpath=author/'COMPUTABLE_MATRIX_SEAL.json';s=json.loads(sealpath.read_text())
files=[{'path':k,'expected':v,'actual':sha(author/k),'matches':sha(author/k)==v} for k,v in s['files'].items()]
arpath=next(author/k for k in s['files'] if k.endswith('COMPUTABLE_MATRIX_RESULT.json'));a=json.loads(arpath.read_text());c=json.loads((author/'COMPUTABLE_MATRIX_SOURCE_CLOSURE.json').read_text())
rows=[{'module':x['module'],'author_sha256':x['sha256'],'independent_sha256':r['sources'][x['module']]['sha256'],'matches':r['sources'][x['module']]['sha256']==x['sha256']} for x in c['sources']]
priorpaths=[pathlib.Path(x).resolve() for x in sys.argv[3:]] or [pathlib.Path('private-locator:d256a08b24273a4590c0'),pathlib.Path('private-locator:dd9cc78ae9314ca3e9c0')]
priors=[]
for path in priorpaths:
 p=json.loads(path.read_text()); bindings=[{'module':m,'matches':r['sources'][m]['sha256']==v['sha256']} for m,v in p['sources'].items() if m in r['sources']]
 priors.append({'receipt':str(path),'receipt_sha256':sha(path),'shared_modules':len(bindings),'unshared_prior_modules':sorted(set(p['sources'])-set(r['sources'])),'all_shared_sources_unchanged':all(x['matches'] for x in bindings),'bindings':bindings})
keys={t['declaration'] for t in a['targets']}
checks={'all_author_seal_files_match':all(x['matches'] for x in files),'all_77_author_sources_match':len(rows)==77 and all(x['matches'] for x in rows),'all_35_author_theorem_targets_audited':len(keys)==35 and keys<=set(r['axioms']),'author_target_axioms_match':all(r['axioms'][n]==a['axioms'][n] for n in keys),'author_audit_source_matches':r['sources']['ComputableMatrixAudit']['sha256']==a['audit_sha256'],'both_prior_subjects_unchanged':len(priors)==2 and sorted(x['shared_modules'] for x in priors)==[35,51] and all(x['all_shared_sources_unchanged'] for x in priors),'root_arithmetic_digest_matches':r['sources']['MatrixArithmetic']['sha256']=='31fc8116bff2b69959c4c198619cd80dc05e1ed3f5529a2fe5ea5e9c33b1d994','all_six_arithmetic_targets_audited':all('AtomicMembership.'+x in r['axioms'] for x in ['divNat_eq_div','rational_imp_cross','rational_imp_dyadic_cross','zero_denominator_control','upper_rational_vacuity','inclusive_rational_tie']),'author_seal_matches_snapshot':sha(sealpath)==r['author_seal']['sha256'],'independent_origins_unchanged':r['origins_unchanged']}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'sealed_files':files,'source_bindings':rows,'prior_subjects':priors,'author_receipt_sha256':sha(arpath),'independent_receipt_sha256':sha(receipt)}
(root/'SOURCE_BINDING_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':checks},indent=2));raise SystemExit(0 if result['status']=='PASS' else 1)
