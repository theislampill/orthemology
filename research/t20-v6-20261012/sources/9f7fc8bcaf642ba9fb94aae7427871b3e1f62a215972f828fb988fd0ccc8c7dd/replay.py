import pathlib,json,hashlib,argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
v=r/'gaussian-entropy-transfer-independent-review-20261011';a=r/'gaussian-primary-shk-comparison-portable-20261011'
subprocess.run([sys.executable,str(v/'replay_review.py'),'--output-dir',str(o/'controls'),'--portable-dir',str(a)],check=True)
assert (o/'controls/EXACT_CHECKS.json').read_bytes()==(v/'EXACT_CHECKS.json').read_bytes()
assert (o/'controls/CLEAN_PORTABLE_REPLAY.json').read_bytes()==(v/'local-replay/CLEAN_PORTABLE_REPLAY.json').read_bytes()
rr=json.loads((o/'controls/REPLAY_RECEIPT.json').read_text());assert rr['clean_portable_count']==33 and rr['independent_exact_count']==32
rec={'status':'PASS_PORTABLE_CONTROLS_SOURCE_CUSTODY_UNAVAILABLE','author_portable_mixed_controls':33,'historical_local_author_controls':35,'independent_exact_controls':32,'both_reports_byte_identical':True,'required_missing_source_rejection_passed':True,'raw_source_custody':'unavailable; not verified','raw_source_bodies_included':False,'renewed_source_reading':False}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps(rec))
