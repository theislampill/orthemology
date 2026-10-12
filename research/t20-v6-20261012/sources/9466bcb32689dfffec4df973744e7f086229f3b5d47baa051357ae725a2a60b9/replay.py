#!/usr/bin/env python3
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
import sympy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
 root=Path(__file__).resolve().parent;out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
 assert actual()==manifest['files']
 ev=root/'evidence';config=json.loads((root/'REPLAY_CONFIG.json').read_text());excluded=json.loads((root/'EXCLUDED_SOURCE_BINDINGS.json').read_text())['files'];verified=[];omitted=[]
 for spec in config['bindings']:
  data=json.loads((ev/spec['source']).read_text());data=data[spec['key']] if 'key' in spec else data
  for name,h in data.items():
   target=str(Path(spec['prefix'])/name);p=ev/target
   record={'source':spec['source'],'target':target,'sha256':h}
   if p.is_file():assert sha(p)==h,record;verified.append(record)
   else:assert target in excluded and excluded[target]==h,record;omitted.append(record)
 out.mkdir(parents=True);work=out/'work';shutil.copytree(ev,work);records=[]
 for spec in config['suites']:
  original=json.loads((ev/spec['directory']/spec['input_manifest']).read_text());reduced={k:h for k,h in original.items() if k not in excluded}
  assert len(original)-len(reduced)==2
  script=work/spec['directory']/spec['script'];(script.parent/spec['input_manifest']).write_text(json.dumps(reduced,indent=2)+'\n')
  p=subprocess.run([sys.executable,str(script)],cwd=script.parent,text=True,capture_output=True)
  (out/(spec['name']+'.stdout.txt')).write_text(p.stdout);(out/(spec['name']+'.stderr.txt')).write_text(p.stderr);assert p.returncode==0,(spec['name'],p.stderr)
  report=json.loads((ev/spec['directory']/spec['report']).read_text());assert report[spec['count_key']]==spec['expected_original_count']
  names={spec['label_prefix']+k for k in excluded};labels=report[spec['labels_key']]
  name=lambda row:row['name'] if isinstance(row,dict) else row
  removed=[row for row in labels if name(row) in names];assert len(removed)==2
  report[spec['labels_key']]=[row for row in labels if name(row) not in names];report[spec['count_key']]=len(report[spec['labels_key']]);assert report[spec['count_key']]==spec['expected_filtered_count']
  expected=(json.dumps(report,indent=2)+'\n').encode();projection=out/(spec['name']+'.EXPECTED_INCLUDED_SCOPE.json');projection.write_bytes(expected)
  generated=script.parent/spec['report'];assert generated.read_bytes()==expected
  assert sha(script)==sha(ev/spec['directory']/spec['script'])
  records.append({'suite':spec['name'],'original_count':spec['expected_original_count'],'fresh_included_count':spec['expected_filtered_count'],'excluded_source_byte_controls':removed,'mathematical_controls_omitted':0,'included_input_manifest_sha256':sha(script.parent/spec['input_manifest']),'unchanged_script_sha256':sha(script),'report_sha256':sha(generated),'exact_projected_report_match':True})
 assert actual()==manifest['files'],'Extracted packet changed'
 result={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'included_files_verified':len(manifest['files']),'suites':records,'included_bindings_verified':verified,'excluded_bindings_not_revalidated':omitted,'extracted_packet_unchanged':True,'scope':'Two source-byte controls per suite deliberately omitted; every mathematical control executed. Ordinary mathematical proofs and inherited classical existence theorem are not kernel-verified. No modern source content revalidation, integration or closure.'}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','author':268,'independent':136,'receipt':str(out/'REPLAY_RECEIPT.json')}))
if __name__=='__main__':main()
