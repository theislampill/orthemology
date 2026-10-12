import pathlib,json,hashlib,argparse,zipfile,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
results={}
for n,s in json.loads((r/'COMPONENT_BINDINGS.json').read_text()).items():
 z=r/'components'/n;assert h(z)==s;x=o/n.removesuffix('.zip');x.mkdir()
 with zipfile.ZipFile(z) as f:f.extractall(x)
 out=o/(n.removesuffix('.zip')+'-output');subprocess.run([sys.executable,str(x/'replay.py'),'--output-dir',str(out)],check=True)
 assert h(out/'REPLAY_RECEIPT.json')==h(r/'receipts'/(n.removesuffix('.zip')+'-REPLAY_RECEIPT.json'))
 results[n]=json.loads((out/'REPLAY_RECEIPT.json').read_text())
x=o/'responsive-demonstration-preservation-20261011';b=json.loads((x/'responsive-demonstration-root-independent-review-20261011/FINAL_FREEZE_BINDING.json').read_text())
for f in b['verified_author_files']:assert h(x/f['path'])==f['sha256']
x=o/'particular-recognition-source-preservation-20261011';d=x/'particular-recognition-source-reconciliation-independent-review-20261011';m=json.loads((d/'REVIEW_MANIFEST.json').read_text())
for n,s in m['files'].items():assert h(d/n)==s
assert hashlib.sha256(''.join(n+'\0'+s+'\n' for n,s in sorted(m['files'].items())).encode()).hexdigest()==m['snapshot_digest']=='c5dc7a6a1bef258a4ac1bad368a4d3a65d323ae248826e8d460283e24cee23af'
d=x/'particular-recognition-source-reconciliation-20261011'
for f in json.loads((d/'MANIFEST.json').read_text())['files']:assert h(d/f['path'])==f['sha256']
(o/'COLLECTION_REPLAY_RECEIPT.json').write_text(json.dumps({'status':'PASS_WITH_DECLARED_EVIDENCE_BOUNDARIES','accepted_source_bindings_verified':True,'component_reports_byte_identical':True,'components':results},indent=2,sort_keys=True)+'\n')
