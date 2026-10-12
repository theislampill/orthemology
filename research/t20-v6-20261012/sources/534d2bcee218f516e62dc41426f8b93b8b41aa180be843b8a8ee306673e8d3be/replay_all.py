#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,sys,zipfile
from pathlib import Path
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--lean-prerequisite-root');args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required';root=Path(__file__).resolve().parent
 manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'};assert actual()==manifest['files'];config=json.loads((root/'REPLAY_MANIFEST.json').read_text());out.mkdir(parents=True);results=[]
 for spec in config['components']:
  archive=root/spec['archive'];assert sha(archive)==spec['sha256'] and archive.stat().st_size==spec['bytes'];assert sha(root/spec['seal_receipt'])==spec['seal_receipt_sha256']
  extracted=out/spec['id']/'extracted';extracted.mkdir(parents=True)
  with zipfile.ZipFile(archive) as z:
   for name in z.namelist():assert (extracted/name).resolve().is_relative_to(extracted.resolve())
   z.extractall(extracted)
  target=out/spec['id']/'replay';script=extracted/spec['entrypoint'];cmd=[sys.executable,str(script),'--output',str(target)]
  if spec['tier']=='prerequisite_bound_lean' and args.lean_prerequisite_root:cmd+=['--prerequisite-root',str(Path(args.lean_prerequisite_root).resolve()),'--compile']
  p=subprocess.run(cmd,cwd=script.parent,text=True,capture_output=True);(out/spec['id']/'stdout.txt').write_text(p.stdout);(out/spec['id']/'stderr.txt').write_text(p.stderr);assert p.returncode==0,(spec['id'],p.stderr)
  receipt=target/'REPLAY_RECEIPT.json';data=json.loads(receipt.read_text())
  if spec['tier']=='prerequisite_bound_lean':
   expected='PASS_PROJECT_SOURCE_REBUILD_WITH_REUSED_STANDARD_OBJECTS' if args.lean_prerequisite_root else 'INTEGRITY_PASS_PREREQUISITES_REQUIRED';assert data['status']==expected
  else:assert data['status']=='PASS'
  assert sha(archive)==spec['sha256'];results.append({'id':spec['id'],'tier':spec['tier'],'archive_sha256':spec['sha256'],'receipt_sha256':sha(receipt),'receipt':data,'scope':spec['scope']})
 assert actual()==manifest['files']
 record={'status':'PASS_WITH_DECLARED_EVIDENCE_BOUNDARIES','component_count':len(results),'components':results,'formal_kernel_reperformed_this_run':bool(args.lean_prerequisite_root),'source_component_fresh_source_reading':False,'all_component_archives_unchanged':True,'outer_manifest_sha256':sha(root/'MANIFEST.json'),'scope':'Separate ordinary-math/exact-execution/source-integrity/prerequisite-bound-formal evidence tiers. No blanket kernel or source-authentication PASS; no upload/integration/owner acceptance/T20 closure.'}
 (out/'COLLECTION_REPLAY_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'components':len(results),'formal_kernel_reperformed':record['formal_kernel_reperformed_this_run'],'receipt':str(out/'COLLECTION_REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
