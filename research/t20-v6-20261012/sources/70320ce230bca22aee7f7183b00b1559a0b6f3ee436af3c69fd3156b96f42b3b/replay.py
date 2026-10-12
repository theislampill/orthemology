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
(o/'REPLAY_RECEIPT.json').write_text(json.dumps({'status':'PASS_WITH_DECLARED_CUSTODY_AND_REPLAY_BOUNDARIES','four_component_archives_unchanged':True,'all_replay_receipts_byte_identical':True,'components':results},indent=2,sort_keys=True)+'\n')
