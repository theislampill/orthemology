import pathlib,json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((r/'MANIFEST.json').read_text())
for n,s in m.items():assert h(r/n)==s,n
b=json.loads((r/'ORIGINAL_BINDINGS.json').read_text())
for n,s in b.items():assert h(r/n)==s,n
receipt={'status':'PASS_INCLUDED_FILE_INTEGRITY_ONLY','included_files':len(m),'original_evidence_files':len(b),'excluded_raw_source_files':len(json.loads((r/'EXCLUDED_SOURCE_BINDINGS.json').read_text())),'fresh_source_review':False,'mathematical_or_kernel_replay':False,'all_included_hashes_match':True}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps(receipt))
