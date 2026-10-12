import pathlib,json,hashlib,argparse,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
author='ordered-control-projective-transport-20261011';review='ordered-control-projective-independent-review-20261011';w=o/'working';w.mkdir()
for n in json.loads((r/'ORIGINAL_BINDINGS.json').read_text()):
 dst=w/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(r/n,dst)
b=w/author/'INPUT_BINDINGS.json';data=json.loads(b.read_text());removed=data['external_sources'];assert len(removed)==2;data['external_sources']=[];b.write_text(json.dumps(data,indent=2)+'\n')
for label,script in [('author',w/author/'check.py'),('independent',w/review/'independent_checks.py')]:
 run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True);(o/(label+'.stdout.log')).write_text(run.stdout);(o/(label+'.stderr.log')).write_text(run.stderr);assert run.returncode==0,run.stderr
original=json.loads((r/author/'CHECKS.json').read_text());projected=dict(original);projected['checks']=[x for x in original['checks'] if not x.startswith('retained source binding: ')];projected['count']=len(projected['checks']);assert projected['count']==39
expected=json.dumps(projected,indent=2)+'\n';(o/'EXPECTED_PROJECTED_CHECKS.json').write_text(expected);assert (w/author/'CHECKS.json').read_text()==expected
assert h(w/review/'CHECK_RESULTS.json')==h(r/review/'CHECK_RESULTS.json')
receipt={'status':'PASS_SCOPED_EXACT_REPLAY','author_controls_replayed':39,'author_original_controls':41,'excluded_source_byte_checks':2,'independent_exact_groups':9,'projected_author_report_byte_identical':True,'independent_report_byte_identical':True,'working_only_input_change':'external_sources=[]','author_checker_unchanged':h(w/author/'check.py')==h(r/author/'check.py')}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps(receipt))
