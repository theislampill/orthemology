import pathlib,json,hashlib,argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
v=r/'finite-polynomial-state-independent-review-20261011';subprocess.run([sys.executable,str(v/'replay.py'),'--output-dir',str(o/'controls')],check=True)
assert (o/'controls/INDEPENDENT_RESULTS.json').read_bytes()==(v/'INDEPENDENT_RESULTS.json').read_bytes()
rec=json.loads((o/'controls/REPLAY_RECEIPT.json').read_text());rec['independent_output_byte_identical']=True
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
