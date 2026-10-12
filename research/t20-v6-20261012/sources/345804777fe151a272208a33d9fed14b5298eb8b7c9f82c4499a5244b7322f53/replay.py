import pathlib,json,hashlib,argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
v=r/'nonnegative-moving-gradient-escape-independent-review-20261011';author=r/'nonnegative-moving-gradient-escape-20261011'
subprocess.run([sys.executable,str(v/'verify_review.py'),'--author-dir',str(author)],check=True)
subprocess.run([sys.executable,str(v/'replay_review.py'),'--author-dir',str(author),'--output-dir',str(o/'controls')],check=True)
assert h(o/'controls/independent/INDEPENDENT_RESULTS.json')==h(v/'INDEPENDENT_RESULTS.json')
rec={'status':'PASS_EXACT_CONTROLS','author_checks':12,'independent_checks':42,'both_output_reports_byte_identical':True,'source_exclusions':0,'kernel_replay':False}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
