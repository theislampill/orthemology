import pathlib,json,hashlib,argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
v=r/'full-law-coarse-graining-independent-review-20261011'
subprocess.run([sys.executable,str(v/'author-snapshot/verify.py'),'--output-dir',str(o/'author')],check=True)
subprocess.run([sys.executable,str(v/'check_independent.py'),'--output-dir',str(o/'independent')],check=True)
assert (o/'author/CHECKS.json').read_bytes()==(v/'portable-author-replay/CHECKS.json').read_bytes()
assert (o/'independent/INDEPENDENT_CHECKS.json').read_bytes()==(v/'INDEPENDENT_CHECKS.json').read_bytes()
rec={'status':'PASS_PORTABLE_EXACT_CONTROLS','author_portable_checks':55,'author_original_inclusive_checks':70,'live_original_checks_not_replayed':15,'independent_checks':29,'both_reports_byte_identical':True,'source_bodies_included':False,'source_reading_renewed':False,'root_failure_snapshots_preserved':True}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps(rec))
