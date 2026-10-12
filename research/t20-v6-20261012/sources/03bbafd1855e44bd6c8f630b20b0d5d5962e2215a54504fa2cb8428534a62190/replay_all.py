#!/usr/bin/env python3
"""Fresh-extract and replay unchanged intermediate component archives."""
import argparse,hashlib,json,platform,subprocess,sys,zipfile
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'};assert actual()==manifest['files'],'Outer manifest mismatch'
 config=json.loads((root/'REPLAY_MANIFEST.json').read_text());out.mkdir(parents=True);records=[]
 for spec in config['components']:
  archive=root/spec['archive'];assert archive.stat().st_size==spec['bytes'] and sha(archive)==spec['sha256']
  assert sha(root/spec['seal_receipt'])==spec['seal_receipt_sha256']
  extracted=out/spec['id']/'extracted';extracted.mkdir(parents=True)
  with zipfile.ZipFile(archive) as z:
   for name in z.namelist():
    target=(extracted/name).resolve();assert target.is_relative_to(extracted.resolve()),'Unsafe ZIP member'
   z.extractall(extracted)
  replay=out/spec['id']/'replay';script=extracted/spec['entrypoint']
  p=subprocess.run([sys.executable,str(script),'--output',str(replay)],cwd=script.parent,text=True,capture_output=True)
  (out/spec['id']/'stdout.txt').write_text(p.stdout);(out/spec['id']/'stderr.txt').write_text(p.stderr)
  assert p.returncode==0,(spec['id'],p.stderr)
  receipt=replay/'REPLAY_RECEIPT.json';data=json.loads(receipt.read_text());assert data['status']=='PASS',spec['id']
  assert sha(archive)==spec['sha256'],'Component archive changed'
  records.append({'id':spec['id'],'archive_sha256':spec['sha256'],'replay_receipt_sha256':sha(receipt),'replay_receipt':str(receipt),'result':data,'scope':spec['scope']})
 assert actual()==manifest['files'],'Outer extracted packet changed'
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'outer_manifest_sha256':sha(root/'MANIFEST.json'),'component_count':len(records),'components':records,'all_original_component_archives_unchanged':True,'outer_extracted_packet_unchanged':True,'scope':'Intermediate integrity and finite control evidence only. Each component retains exact stated projection or portability boundaries. No universal kernel proof, external source reinspection, upload, integration, owner acceptance or T20 closure. Full-law action-length investigation excluded.'}
 (out/'COLLECTION_REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','components':len(records),'receipt':str(out/'COLLECTION_REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
