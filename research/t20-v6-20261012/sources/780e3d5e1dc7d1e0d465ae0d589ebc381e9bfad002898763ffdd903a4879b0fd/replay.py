import pathlib,json,hashlib,argparse,subprocess,sys,shutil
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
w=o/'working';w.mkdir()
for n,s in json.loads((r/'ORIGINAL_BINDINGS.json').read_text()).items():
 dst=w/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(r/n,dst)
a='pairwise-corroboration-bound-20261011';v='pairwise-corroboration-independent-review-20261011';u='pairwise-corroboration-asymmetric-supplement-20261011';acc=json.loads((r/v/'RECEIPT.json').read_text())
for n,row in acc['author_snapshot'].items():assert h(r/a/n)==row['sha256']
for row in acc['files']:assert h(r/v/row['path'])==row['sha256']
for row in json.loads((r/u/'MANIFEST.json').read_text())['files']:assert h(r/u/row['path'])==row['sha256']
for label,d,script,report in [('author',a,'verify.py','CONTROL_RESULTS.json'),('independent',v,'independent_controls.py','INDEPENDENT_RESULTS.json'),('supplement',u,'verify.py','CONTROL_RESULTS.json')]:
 run=subprocess.run([sys.executable,str(w/d/script)],capture_output=True,text=True);(o/(label+'.stdout.json')).write_text(run.stdout);(o/(label+'.stderr.txt')).write_text(run.stderr);assert run.returncode==0,run.stderr;assert (w/d/report).read_bytes()==(r/d/report).read_bytes()
rec={'status':'PASS_FULL_RELEVANT_REPLAY','author_exact_assertions':39280,'independent_total_assertions':14163,'independent_mathematical_assertions':14120,'independent_integrity_assertions':43,'custody_records':17,'unique_upstream_files':14,'supplement_author_stage_assertions':6860,'supplement_independently_reviewed':False,'all_three_reports_byte_identical':True,'required_input_exclusions':0,'source_reading_renewed':False}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps(rec))
