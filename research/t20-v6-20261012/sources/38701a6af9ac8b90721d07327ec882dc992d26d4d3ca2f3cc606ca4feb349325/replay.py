import pathlib,json,hashlib,argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
a=r/'gaussian-quartic-variance-root-20261011';v=r/'gaussian-quartic-variance-independent-review-20261011';acc=json.loads((v/'review_receipt.json').read_text())
for d,key in [(a,'author_files'),(v,'review_files')]:
 for row in acc[key]:assert h(d/row['path'])==row['sha256']
for name,script,target,expected in [('corrected',a/'check.py',a/'CHECKS.json',0),('independent',v/'independent_check.py',v/'INDEPENDENT_CHECKS.json',0),('initial_failure',a/'snapshots/initial_check.py',v/'INITIAL_FAILURE_REPLAY.json',1)]:
 run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True);(o/(name+'.json')).write_text(run.stdout);(o/(name+'.stderr.txt')).write_text(run.stderr);assert run.returncode==expected;assert run.stdout==target.read_text()
c=json.loads((o/'corrected.json').read_text());f=json.loads((o/'initial_failure.json').read_text());assert c['values']==f['values'];assert not f['checks']['positive_gap_factor'];assert 'AssertionError' in (o/'initial_failure.stderr.txt').read_text()
rec={'status':'PASS_WITH_EXPECTED_HISTORICAL_FAILURE_REPRODUCED','corrected_root_controls':5,'independent_controls':12,'all_three_json_outputs_byte_identical':True,'initial_failure_same_mathematical_values':True,'right_hand_derivative_scope':'Analytic proof retained; finite controls are not universal verification','source_exclusions':0}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps(rec))
