import pathlib,hashlib,json,subprocess,os,datetime
R=pathlib.Path('private-locator:4bb2f72cdc070f304a86');P=pathlib.Path('private-locator:9e37730c688c952e3d37');O=pathlib.Path('private-locator:0834fb4d4a670543c64b');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result={'scope':'P01 final receipt, source/artifact binding, immutable input, independent 382-target readback'}
q=json.loads((P/'strict-0004/QUALIFICATION.json').read_text()); old=json.loads((P/'INPUT_IMMUTABILITY.json').read_text())
assert len(old)==507
assert {str(p.relative_to(O)):sha(p) for p in O.rglob('*') if p.is_file()}==old
assert q['status']=='KERNEL_VERIFIED_EXACT_PIN_SCOPED_TARGETS' and q['target_count']==382 and len(q['declarations'])==382
assert all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in q['declarations'].values())
assert all(sha(P/'strict-0004'/r['path'])==r['sha256'] for r in q['compiled_artifacts'])
# Every candidate formal source copied into the successful project still matches the shadow.
for f in (P/'shadow-packet/formal').glob('*.lean'):
 cp=P/'strict-0004/project'/f.name
 assert cp.exists() and sha(cp)==sha(f),f
result.update(original_files_unchanged=507,target_count=382,artifacts_hash_checked=len(q['compiled_artifacts']),receipt_sha256=sha(P/'strict-0004/QUALIFICATION.json'),patch_sha256=sha(P/'SOURCE_REPAIRS.patch'),statement_scope='All original target names retained; PLift signature correction and explicit dependent binders audited separately')
bin=pathlib.Path('private-locator:d97af50b47918e94879b'); env={**os.environ,'PATH':str(bin)+':'+os.environ['PATH']};env.pop('LEAN_SYSROOT',None);env.pop('LEAN_PATH',None)
cmd=[str(bin/'lake'),'env','lean','-j1','P01Audit.lean']
p=subprocess.run(cmd,cwd=P/'strict-0004/project',env=env,capture_output=True,timeout=240)
(R/'evidence/P01-independent-readback.stdout').write_bytes(p.stdout);(R/'evidence/P01-independent-readback.stderr').write_bytes(p.stderr)
result.update(command=cmd,exit_code=p.returncode,stdout_sha256=sha(R/'evidence/P01-independent-readback.stdout'),stderr_sha256=sha(R/'evidence/P01-independent-readback.stderr'))
assert p.returncode==0
s=p.stdout.decode();assert 'sorryAx' not in s
assert sum(s.count('AUDIT_BEGIN '+n+'\n') for n in q['declarations'])==382
assert all("'"+n+"'" in s for n in q['declarations'])
result.update(status='PASS_BOUNDED_P01_FINAL_AUDIT',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(R/'evidence/P01_FINAL_INDEPENDENT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
