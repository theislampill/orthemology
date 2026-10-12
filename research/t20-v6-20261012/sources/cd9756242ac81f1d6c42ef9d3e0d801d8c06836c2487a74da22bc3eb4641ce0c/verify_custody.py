#!/usr/bin/env python3
"""Read-only exact custody checks; this is not source retranscription or research."""
import argparse,hashlib,json,re,sys
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
A='hase-structured-context-uniformity-20261010';V='hase-structured-context-review-20261010'
S='local-correction-capacity-20261010';T='local-correction-capacity-review-20261010';U='local-correction-root-20261010'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def safe(root,name):
 rel=PurePosixPath(name);need(not rel.is_absolute() and '..' not in rel.parts,'Unsafe path: '+name)
 p=root/rel;need(p.resolve().is_relative_to(root.resolve()),'Escaping path: '+name)
 need(not any(x.is_symlink() for x in [p,*p.parents]),'Symlink: '+name)
 return p
def check(p,row):
 need(p.is_file(),'Missing file: '+str(p));b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==row['sha256'],'Hash mismatch: '+str(p))
 if 'bytes' in row:need(len(b)==row['bytes'],'Length mismatch: '+str(p))
 if 'git_blob_sha1' in row:need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'],'Blob mismatch: '+str(p))
def verify(root,expected=None,external=None):
 index=root/'MANIFEST.json'
 if expected:need(sha(index)==expected,'External manifest pin mismatch')
 rows=load(index)['files'];names=[r['path'] for r in rows];need(len(names)==len(set(names)),'Duplicate inventory')
 actual=set()
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink in packet')
  if p.is_file():actual.add(p.relative_to(root).as_posix())
 need(actual==set(names)|{'MANIFEST.json'},'Exact inventory mismatch')
 for r in rows:check(safe(root,r['path']),r)
 c=load(root/'REUSE_CONTRACT.json');inherit=load(root/'EXACT_INHERITANCE.json');omitted={r['path']:r for r in inherit['omitted_original_files']}
 for r in c['frozen_pins']:check(safe(root,r['path']),r)
 for r in inherit['copied_files']:check(safe(root,r['packet_path']),r)
 counts={}
 def records(label,rs,prefix=''):
  included=excluded=0
  for r in rs:
   name=prefix+r['path']
   if name in omitted:
    q=omitted[name];need(q['sha256']==r['sha256'],'Omission hash mismatch: '+name)
    if 'bytes' in r:need(q['bytes']==r['bytes'],'Omission size mismatch: '+name)
    need(not safe(root,name).exists(),'Omitted path present: '+name);excluded+=1
   else:check(safe(root,name),r);included+=1
  counts[label]={'included_checked':included,'omitted_identified_not_rehashed':excluded}
 records('structured_author_manifest',load(root/A/'MANIFEST.json')['files'],A+'/')
 records('structured_review_manifest',load(root/V/'MANIFEST.json')['files'],V+'/')
 records('source_author_manifest',load(root/S/'MANIFEST.json')['files'])
 records('source_author_inputs',load(root/S/'INPUT_BINDINGS.json')['inputs'])
 records('source_review_manifest',load(root/T/'REVIEW_MANIFEST.json')['files'],T+'/')
 records('duplicate_support_companion_manifest',load(root/'objective-goodness-source-check-20261010/MANIFEST.json')['files'],'objective-goodness-source-check-20261010/')
 records('duplicate_support_companion_inputs',load(root/'objective-goodness-source-check-20261010/INPUT_HASHES.json')['records'])
 before=load(root/T/'BEFORE_HASH_RECEIPT.json');after=load(root/T/'AFTER_HASH_RECEIPT.json')
 records('source_review_before_manifest',before['manifest_checks']);records('source_review_before_inputs',before['input_binding_checks'])
 for r in after['checks']:need(r['before_sha256']==r['after_sha256'] and r['unchanged'],'Historical after receipt reports change')
 records('source_review_after',[{'path':r['path'],'sha256':r['after_sha256']} for r in after['checks']])
 rr=load(root/V/'REVIEW_RECEIPT.json')
 need(rr['status']=='PASS_WITHIN_STATED_SCOPE','Review status')
 need(rr['review_manifest_sha256']==sha(root/V/'MANIFEST.json'),'Review seal mismatch')
 need(rr['author_manifest_sha256']==sha(root/A/'MANIFEST.json'),'Author seal mismatch')
 for k in ['replay_receipt','replay_log']:check(root/V/rr[k]['path'],rr[k])
 need(load(root/T/'READ_RECEIPT.json')['reviewed_report_sha256']==sha(root/S/'REPORT.md'),'Source reviewed target mismatch')
 for name in ['REPORT.md','INPUT_BINDINGS.json','MANIFEST.json','PRIOR_SOURCE_SEARCH.json','SOURCE_READS.json','VERIFICATION.json']:
  need((root/S/name).read_bytes()==(root/T/'inputs'/name).read_bytes(),'Frozen source copy mismatch')
 for r in load(root/V/'REVIEW_INPUTS.json')['frozen_files']:
  name=r['path']; snap=V+'/'+r['snapshot']
  if name in omitted:need(snap in omitted and omitted[name]['sha256']==omitted[snap]['sha256'],'Frozen omission mismatch')
  else:need((root/name).read_bytes()==(root/snap).read_bytes(),'Frozen Lean copy mismatch')
 rootcheck=load(root/U/'SOURCE_CHECK.json');need(sha(root/U/'printed274.png')==rootcheck['image_sha256'],'Root image mismatch')
 need(rootcheck['pdf_sha256']==omitted[S+'/sources/intisar.pdf']['sha256'],'Root source mismatch')
 # End markers delimit pages, rather than introducing them. Check continuity and duplicate overlap only.
 pat=re.compile(r'\(الكتاب/(\d+)\)');seen={};occurrences=0;extracts=[]
 for derivative in load(root/'PACKAGING_DERIVATIVES.json')['files']:
  check(root/derivative['path'],derivative)
  need(omitted[derivative['original_path']]['sha256']==derivative['original_sha256'],'Derivative source binding mismatch')
  start,end=derivative['first_page'],derivative['last_page'];text=(root/derivative['path']).read_text();matches=list(pat.finditer(text));need([int(m[1]) for m in matches]==list(range(start,end+1)),'Noncontinuous page markers')
  pos=0
  for m in matches:
   page=int(m[1]);body=text[pos:m.start()].strip();pos=m.end()
   if page in seen:need(seen[page]==body,'Overlap mismatch')
   seen[page]=body;occurrences+=1
  need(not text[pos:].strip(),'Unexpected trailing unmarked excerpt')
  extracts.append(derivative)
 external_result={'performed':False,'fresh_retranscription':False,'fresh_image_render':False}
 if external:
  raw=[r for r in omitted.values() if not r['path'].endswith(('.olean','.pyc'))]
  for r in raw:check(safe(external,r['path']),r)
  body=(external/S/'sources/intisar.txt').read_text()
  for r in extracts:
   start=f"(الكتاب/{r['first_page']-1})";end=f"(الكتاب/{r['last_page']})";a=body.index(start)+len(start);b=body.index(end,a)+len(end)
   received=body[a:b].strip()+'\n';need(received.encode()==(external/r['original_path']).read_bytes(),'External received-transcription excerpt mismatch')
   parts=[];pos=0
   for m in pat.finditer(received):
    pagebody=received[pos:m.start()].split('_________',1)[0].strip();pos=m.end();parts.append(pagebody+'\n'+m[0]+'\n')
   need(('\n'.join(parts)).encode()==(root/r['path']).read_bytes(),'Packaging derivative mismatch')
  external_result.update(performed=True,excluded_original_files_rehashed=len(raw),exact_received_transcription_excerpts_compared=len(extracts))
 return {'status':'PASS_CUSTODY_ONLY','manifest_sha256':sha(index),'inventory_files':len(rows),'binding_counts':counts,'continuous_page_occurrences':occurrences,'distinct_received_pages':len(seen),'overlap_consistent':True,'external_source_check':external_result,'new_source_reading_credit':False,'independent_retranscription':False,'fresh_research':False,'root_check_independent_witness':False,'scope':load(root/'PRESERVATION_SCOPE.json')}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',required=True,type=Path);p.add_argument('--expected-manifest-sha256');p.add_argument('--external-source-root',type=Path);a=p.parse_args();a.root=a.root.resolve();a.output=a.output.resolve()
 need(not a.output.exists(),'Refusing existing output');need(not a.output.is_relative_to(a.root),'Output must be outside packet')
 if a.external_source_root:a.external_source_root=a.external_source_root.resolve();need(not a.output.is_relative_to(a.external_source_root),'Output must be outside external source tree')
 result=verify(a.root,a.expected_manifest_sha256,a.external_source_root);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['status'],result['inventory_files'],'files;',result['distinct_received_pages'],'distinct received pages')
if __name__=='__main__':main()
