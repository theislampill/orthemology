import pathlib,json,hashlib,argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
a=r/'gaussian-correction-geometry-20261011';v=r/'gaussian-induced-geometry-independent-review-20261011-0045';acc=json.loads((v/'review_receipt.json').read_text())
for d,key in [(a,'author_files'),(v,'review_files')]:
 for row in acc[key]:assert h(d/row['path'])==row['sha256']
subprocess.run([sys.executable,str(a/'verify.py'),'--output-dir',str(o/'author')],check=True)
pj=json.loads((a/'author-run/CONTROL_RESULTS.json').read_text());pj['groups']=[x for x in pj['groups'] if not x.startswith('original ')];pj['assertions']=len(pj['groups']);assert pj['assertions']==157
expected=json.dumps(pj,indent=2)+'\n';(o/'EXPECTED_PORTABLE_CONTROL_RESULTS.json').write_text(expected);assert (o/'author/CONTROL_RESULTS.json').read_text()==expected
run=subprocess.run([sys.executable,str(v/'independent_checks.py')],capture_output=True,text=True);assert run.returncode==0,run.stderr;(o/'independent_checks.json').write_text(run.stdout);assert run.stdout==(v/'independent_checks.json').read_text()
rec={'status':'PASS_PORTABLE_EXACT_CONTROLS','author_portable_controls':157,'author_original_aware_controls':166,'live_original_checks_not_part_of_portable_run':9,'independent_controls':25,'projected_author_report_byte_identical':True,'independent_report_byte_identical':True,'source_exclusions':0,'working_evidence_modifications':0}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps(rec))
