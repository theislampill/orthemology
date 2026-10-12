#!/usr/bin/env python3
"""Non-mutating independent replay and provenance checks for research shadows."""
import pathlib,subprocess,json,os,hashlib,datetime,re,shutil
R=pathlib.Path(__file__).resolve().parent; E=R/'evidence'; E.mkdir(exist_ok=True)
T=pathlib.Path('private-locator:4211d241978f643cb623')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'toolchain_sha256':sha(T),'scope':'Independent source snapshot, fresh P03 builds and P02 receipt integrity; no canonical mutation','checks':[]}
def check(name,condition,details=None):
 row={'check':name,'pass':bool(condition),'details':details};record['checks'].append(row)
 if not condition:raise AssertionError(row)
def run(label,cmd,cwd,env=None):
 p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=180)
 (E/(label+'.stdout')).write_bytes(p.stdout);(E/(label+'.stderr')).write_bytes(p.stderr)
 record['checks'].append({'check':label,'pass':p.returncode==0,'command':cmd,'cwd':str(cwd),'exit_code':p.returncode,'stdout_sha256':sha(E/(label+'.stdout')),'stderr_sha256':sha(E/(label+'.stderr'))})
 if p.returncode:raise RuntimeError(label+': '+p.stdout.decode()+p.stderr.decode())
 return p.stdout.decode()
try:
 base=pathlib.Path('private-locator:6e1cdd2685640ba2eef0');orig=pathlib.Path('private-locator:7ea32b53e570f697d181')
 receipt=base/'receipts/qualification-20260930T134433Z/QUALIFIED_RESULT.json';q=json.loads(receipt.read_text())
 check('P02_sealed_result_hash',sha(receipt)=='1e963ab5c8558a2e633b1f0f83e08628cd23d09058ebfdd577a9f0e944e4b52c',sha(receipt))
 check('P02_source_and_original_hashes',all(sha(base/r['source'])==r['repaired_sha256'] and sha(orig/r['source'])==r['original_sha256'] for r in q['sources']))
 check('P02_target_counts',len(q['axioms'])==130 and sum(r['theorems'] for r in q['sources'])==130)
 check('P02_axiom_ceiling',all(set(a)<= {'propext','Classical.choice','Quot.sound'} for a in q['axioms'].values()))
 check('P02_nonempty_current_artifacts',all((base/'.lake/build/lib/lean'/pathlib.Path(*r['module'].split('.'))).with_suffix('.olean').stat().st_size==r['bytes'] and sha((base/'.lake/build/lib/lean'/pathlib.Path(*r['module'].split('.'))).with_suffix('.olean'))==r['sha256'] for r in q['artifacts']))
 pp=base/'receipts/qualification-20260930T134433Z'
 check('P02_readback_hash',sha(pp/'all-types-and-axioms-corrected.stdout')==q['audit_output_sha256'])
 src=pathlib.Path('private-locator:a5027252c749f1a6a04e');pr=json.loads((src/'RECEIPT.json').read_text())
 check('P03_source_receipt_hashes',all(sha(src/n)==r['sha256'] and sha(pathlib.Path(r['origin']))==r['sha256'] for n,r in pr['source_files'].items()))
 build=R/'p03-fresh-independent-2';build.mkdir(exist_ok=False)
 modules=['InternalPolymorphism','FiniteBridge','SourceTypeOps','SourceHeadStep','SourceChecker','SourceCheckerProofs','SourceResources','SourceRepresentation','SourceResourceBounds','SourceControls','SourceBranchControls','SourceExportBoundary','SourceCheckerAudit']
 for m in modules:shutil.copy2(src/(m+'.lean'),build/(m+'.lean'))
 graph=pathlib.Path('private-locator:9266f637ed90401341b7')
 for m in ['P03GuardedGraph','P03GuardedVCT','P03Audit','P03QualificationControls']:shutil.copy2(graph/(m+'.lean'),build/(m+'.lean'))
 modules+=['P03GuardedGraph','P03GuardedVCT','P03Audit','P03QualificationControls']
 env={**os.environ,'LEAN_PATH':str(build)};env.pop('LEAN_SYSROOT',None)
 run('lean-version',[str(T),'--version'],build,env)
 for m in modules:
  check('fresh_output_absent_'+m,not (build/(m+'.olean')).exists())
  run('P03_final_'+m,[str(T),'-j1','-o',m+'.olean',m+'.lean'],build,env)
  check('nonempty_output_'+m,(build/(m+'.olean')).stat().st_size>0)
 record['p03_source_snapshot']={m+'.lean':sha(build/(m+'.lean')) for m in modules}
 record['p03_artifact_snapshot']={m+'.olean':sha(build/(m+'.olean')) for m in modules}
 record['status']='PASS_BOUNDED_CHECKS'
except Exception as e:record['status']='FAIL_CLOSED';record['failure']=repr(e);raise
finally:
 record['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(E/'INDEPENDENT_REPLAY_FINAL.json').write_text(json.dumps(record,indent=2)+'\n')
 print(record['status'],len(record['checks']),flush=True)
