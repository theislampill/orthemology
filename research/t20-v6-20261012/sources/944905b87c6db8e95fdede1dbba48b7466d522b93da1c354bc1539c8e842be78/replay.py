import pathlib,json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parent;o=pathlib.Path(a.output_dir);o.mkdir(parents=True,exist_ok=False)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,s in json.loads((r/'MANIFEST.json').read_text()).items():assert h(r/n)==s,n
for n,s in json.loads((r/'ACCEPTED_PINS.json').read_text()).items():assert h(r/n)==s,n
ex=json.loads((r/'EXCLUDED_SOURCE_BINDINGS.json').read_text());counts={}
for d in ['productive-origination-target-20261011','productive-origination-target-independent-review-20261011']:
 included=omitted=0
 for x in json.loads((r/d/'MANIFEST.json').read_text()):
  n=d+'/'+x['path']
  if n in ex:assert ex[n]['sha256']==x['sha256'];omitted+=1
  else:assert h(r/n)==x['sha256'];included+=1
 counts[d]={'included_manifest_members':included,'excluded_source_members':omitted}
a=r/'productive-origination-target-20261011'
for x in json.loads((a/'INPUT_BINDINGS.json').read_text()):assert h(a/x['copy_path'])==x['sha256']
assert (a/'REPORT.md').read_bytes()==(r/'productive-origination-target-independent-review-20261011/REVIEWED_REPORT.md').read_bytes()
rec={'status':'PASS_SCOPED_OFFLINE_INTEGRITY','manifest_coverage':counts,'retained_input_copies':10,'historical_57_check_suite_freshly_replayed':False,'fresh_source_reading':False,'initial_report_bytes_available':False}
(o/'REPLAY_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps(rec))
