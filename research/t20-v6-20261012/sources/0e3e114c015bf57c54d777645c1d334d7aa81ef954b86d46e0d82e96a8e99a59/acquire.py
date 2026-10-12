"""Read-only acquisition and inventory. Acquisition is not semantic review."""
from __future__ import annotations
import csv, hashlib, io, json, os, shutil, subprocess, tarfile, time, urllib.request, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path('private-locator:1a21b068f7983766df37')
PKG=ROOT/'package'; SRC=PKG/'sources'; EXT=PKG/'extracted'; LOG=PKG/'ledgers'
for p in (SRC,EXT,LOG,PKG/'research',PKG/'audits',PKG/'verification'):p.mkdir(parents=True,exist_ok=True)
FILES=['The_Last_Moat_Edition_3(3).pdf','orthing_modal_metaphysical_frontier_v2(1).zip','orthing_continuation_frontier_v1.zip','orthing_formalisation_v1(1).pdf','information-composition-and-self-revision-v5(1).pdf','the-cost-of-a-decisive-revision(1).pdf','private-identity:fa1bd280b552b4f4afc7.png']
FONTS={'.ttf','.otf','.woff','.woff2','.eot','.pfb','.pfa','.ttc'}
EVENTS=[]; originals=[]
def event(kind,**kw):EVENTS.append({'kind':kind,**kw})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_parts(name):
 p=PurePosixPath(name.replace('\\','/'))
 if p.is_absolute() or '..' in p.parts:raise ValueError('unsafe member path')
 return p.parts
for name in FILES:
 p=Path('/mnt/data')/name
 if not p.is_file():event('attachment_missing',name=name);continue
 originals.append({'name':name,'sha256':sha(p),'bytes':p.stat().st_size})
 if p.suffix.lower()=='.zip':
  dest=SRC/'attachment_members'/p.stem;dest.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(p) as z:
   has_font=any(Path(i.filename).suffix.lower() in FONTS for i in z.infolist())
   if not has_font:
    (SRC/'original_attachments').mkdir(exist_ok=True);shutil.copy2(p,SRC/'original_attachments'/p.name)
   else:event('original_zip_not_redistributed_fonts',name=name)
   for i in z.infolist():
    if i.is_dir():continue
    try:
     parts=safe_parts(i.filename)
     if Path(i.filename).suffix.lower() in FONTS:event('font_excluded',source=name,member=i.filename);continue
     if (i.external_attr>>16)&0o170000==0o120000:event('symlink_not_extracted',source=name,member=i.filename);continue
     t=dest.joinpath(*parts);t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(z.read(i))
    except Exception as e:event('zip_member_error',source=name,member=i.filename,error=repr(e))
 else:
  (SRC/'original_attachments').mkdir(exist_ok=True);shutil.copy2(p,SRC/'original_attachments'/p.name)
META={'repository':'theislampill/orthemology','historically_observed_pin':'f50dc1aee52356cc6adbef342387576b02afc124','current_pin_verified':False,'complete_tree_acquired':False,'history_and_discussions_acquired':False}
def get(url,timeout=15):
 req=urllib.request.Request(url,headers={'User-Agent':'Orthemology-read-only-research-archive','Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()
try:
 raw=get('https://api.github.com/repos/theislampill/orthemology/branches/main')
 (LOG/'github_main_response.json').write_bytes(raw);branch=json.loads(raw);pin=branch['commit']['sha']
 META.update(current_pin=pin,current_pin_verified=True)
except Exception as e:
 event('current_branch_acquisition_failed',error=repr(e));pin=META['historically_observed_pin'];META.update(acquisition_pin=pin,pin_status='historical_fallback_not_verified_current')
try:
 raw=get('https://codeload.github.com/theislampill/orthemology/tar.gz/'+pin,timeout=25)
 META['download_sha256']=hashlib.sha256(raw).hexdigest();META['download_bytes']=len(raw)
 dest=SRC/'github_tree';dest.mkdir(exist_ok=True);expected=[]
 with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tf:
  members=tf.getmembers()
  for m in members:
   if m.isdir():continue
   parts=safe_parts(m.name)[1:]
   if not parts:continue
   entry={'path':'/'.join(parts),'type':'file' if m.isfile() else 'link_or_special','bytes':m.size};expected.append(entry)
   if Path(m.name).suffix.lower() in FONTS:event('font_excluded',source='github',member=entry['path']);continue
   if not m.isfile():event('github_special_member_not_materialised',member=entry['path'],link=m.linkname);continue
   f=tf.extractfile(m)
   if f is None:raise ValueError('no bytes for '+m.name)
   t=dest.joinpath(*parts);t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(f.read())
 META.update(acquisition_pin=pin,complete_tree_acquired=True,tracked_archive_members=len(expected))
 (LOG/'github_archive_members.json').write_text(json.dumps(expected,indent=2))
except Exception as e:event('github_tree_acquisition_failed',error=repr(e))
# External discussions are a separate scope; retain only discovery metadata here.
try:
 raw=get('https://api.github.com/repos/theislampill/orthemology/issues?state=all&per_page=100',timeout=10)
 (LOG/'github_issue_discovery_first_page.json').write_bytes(raw)
 event('github_discussion_scope_pending',note='First-page metadata is not all issue bodies/comments, PR reviews, or history.')
except Exception as e:event('github_issue_discovery_failed',error=repr(e))
rows=[];duplicates={}
for idx,p in enumerate(sorted(SRC.rglob('*'))):
 if not p.is_file():continue
 rel=str(p.relative_to(PKG));data=p.read_bytes();digest=hashlib.sha256(data).hexdigest()
 row={'source_id':f'S{idx:06d}','source_path':rel,'bytes':len(data),'sha256':digest,'kind':'binary','text_lines':0,'extracted_path':'','semantic_review':'PENDING','evidence_status':'ACQUIRED_NOT_VALIDATED'}
 duplicates.setdefault(digest,[]).append(rel)
 if p.suffix.lower()=='.pdf':
  try:
   import fitz
   doc=fitz.open(p);text='\n'.join(f'\n[[PDF_PAGE_{i+1}]]\n'+page.get_text('text') for i,page in enumerate(doc));row['kind']='pdf';row['pages']=len(doc)
   out=EXT/(row['source_id']+'.txt');out.write_text(text,encoding='utf-8');row.update(text_lines=len(text.splitlines()),extracted_path=str(out.relative_to(PKG)),extraction='PyMuPDF text; mathematics/page-image review PENDING')
  except Exception as e:event('pdf_extraction_failed',source=rel,error=repr(e))
 elif p.suffix.lower() not in {'.zip','.gz','.png','.jpg','.jpeg','.gif','.webp','.mp4','.pyc','.ico','.sqlite','.db'}:
  try:
   text=data.decode('utf-8')
   if '\x00' not in text:
    row.update(kind='utf8_text',text_lines=len(text.splitlines()),extracted_path=rel,extraction='original UTF-8 bytes')
  except UnicodeDecodeError:pass
 rows.append(row)
(ROOT/'package'/'ledgers'/'source_inventory.json').write_text(json.dumps(rows,indent=2))
with (LOG/'source_inventory.csv').open('w',newline='') as f:
 keys=['source_id','source_path','bytes','sha256','kind','text_lines','extracted_path','semantic_review','evidence_status'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
coverage={'inventory_files':len(rows),'inventory_bytes':sum(x['bytes'] for x in rows),'text_or_pdf_extraction_lines':sum(x['text_lines'] for x in rows),'fresh_line_by_line_semantic_review_certified_files':0,'fresh_line_by_line_semantic_review_certified_lines':0,'scope_note':'Machine acquisition/extraction is not a line-by-line semantic read. Prior conversational summaries are not promoted to fresh review receipts.','overall_status':'INCOMPLETE_NOT_APPROVED'}
(LOG/'coverage.json').write_text(json.dumps(coverage,indent=2));(LOG/'github_scope.json').write_text(json.dumps(META,indent=2));(LOG/'original_attachment_hashes.json').write_text(json.dumps(originals,indent=2));(LOG/'acquisition_events.json').write_text(json.dumps(EVENTS,indent=2));(LOG/'exact_duplicate_groups.json').write_text(json.dumps([v for v in duplicates.values() if len(v)>1],indent=2))
# A true work queue: nothing is falsely assigned reviewed merely because it was indexed.
with (LOG/'semantic_review_queue.jsonl').open('w') as f:
 for x in rows:
  if x['text_lines']:
   for start in range(1,x['text_lines']+1,160):
    f.write(json.dumps({'source_id':x['source_id'],'path':x['source_path'],'extracted_path':x['extracted_path'],'start_line':start,'end_line':min(start+159,x['text_lines']),'state':'PENDING','required_receipt':['semantic_summary','claims_and_assumptions','cross_source_relations','adversarial_findings','dispositions','reviewer_and_time']})+'\n')
print(json.dumps({'coverage':coverage,'github':META,'events':EVENTS},indent=2))
