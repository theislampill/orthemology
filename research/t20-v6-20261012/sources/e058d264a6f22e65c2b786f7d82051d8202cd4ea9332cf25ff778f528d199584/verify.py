import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
root=p.parent.parent
bindings=json.loads((p/'SOURCE_BINDINGS.json').read_text())['sources']
for r in bindings:
 f=root/r['path']; expected=r.get('public_sha256',r.get('sha256'))
 assert hashlib.sha256(f.read_bytes()).hexdigest()==expected, str(f)
coverage=json.loads((p/'INDIVIDUAL_COVERAGE.json').read_text())
expected={'T6-KNOWLEDGE','T6-UPSTREAM'}|{f'S6F-{i:02}' for i in range(1,10)}
assert {r['id'] for r in coverage['families']}==expected
assert len(coverage['families'])==11
application=json.loads((p/'BOUNDED_APPLICATION.json').read_text())
assert all(application['checks'].values())
assert application['classification']=='WARRANTED_RETAINED_STANDARD_REPAIR_NOT_CANDIDATE_E_RADICAL_CORRECTION'
print(json.dumps({'status':'PASS','verified_source_bindings':len(bindings),'family_rows':11,'application_checks':len(application['checks'])}))
