#!/usr/bin/env python3
"""Independent read-only candidate inspection; outputs belong to private review."""
from pathlib import Path
import hashlib, json, re, sqlite3, collections, datetime
B=Path(__file__).resolve().parents[2]
P=B/'projection/package'
R=B/'review/portability'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
read=lambda p:json.loads(p.read_text())
files=[{'path':p.relative_to(P).as_posix(),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(P.rglob('*')) if p.is_file()]
canonical=json.dumps(files,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
snapshot={'schema':'independent-package-byte-snapshot-v1','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'digest_definition':'SHA256 of UTF-8 canonical JSON file array, sort_keys=True,separators=(comma,colon), ensure_ascii=False','file_array_sha256':sha(canonical),'file_count':len(files),'bytes':sum(x['bytes'] for x in files),'files':files}
(R/'REVIEWED_PACKAGE_SNAPSHOT.json').write_text(json.dumps(snapshot,indent=2)+'\n')
D=read(P/'PUBLIC_PROJECTION.json'); db=sqlite3.connect(B/'catalogue/catalogue.sqlite3'); failures=[];bindings=[]
published={r['repository_path']:r for r in map(json.loads,(B/'catalogue/published_file_identity_map.jsonl').open())}
baseline_refs={r['path']:r for r in read(P/'BASELINE_REFERENCE_CHECK.json')['files']}
for row in D['files']:
 h=row['original_sha256']; op=B/'catalogue/objects'/h[:2]/h
 if not op.is_file() or sha(op.read_bytes())!=h or op.stat().st_size!=row['original_bytes']:failures.append(['original_identity',h])
 for origin in row.get('original_member_bindings',[]):
  hit=db.execute('select 1 from members where archive_sha256=? and member=? and sha256=?',(origin['archive_sha256'],origin['member'],h)).fetchone()
  if not hit:failures.append(['member_binding',h,origin])
 if row['disposition']=='included':
  p=P/row['public_path']
  if not p.is_file() or sha(p.read_bytes())!=row['public_sha256'] or p.stat().st_size!=row['public_bytes']:failures.append(['public_identity',h])
 else:
  pub=published.get(row['repository_path'])
  matched=bool(pub and any(x['sha256']==row['public_sha256'] and x['bytes']==row['public_bytes'] for x in pub['held_exact_public_byte_matches']))
  if not matched and row['repository_path'] in baseline_refs:
   raw=op.read_bytes();git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
   matched=(git_blob==baseline_refs[row['repository_path']]['git_blob_sha1'] and h==row['public_sha256'] and len(raw)==row['public_bytes'])
  if not matched:failures.append(['pinned_public_identity',h])
  if row['public_url']!='https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/'+row['repository_path']:failures.append(['public_pin',h])
 if row['projection']=='EXACT' and (row['original_sha256']!=row['public_sha256'] or row['original_bytes']!=row['public_bytes']):failures.append(['false_exact',h])
 if row['projection']!='EXACT' and not row.get('transformations'):failures.append(['unexplained_transformation',h])
 for cp in row.get('required_replay_copies',[]):
  p=P/cp['path']
  if not p.is_file() or sha(p.read_bytes())!=cp['sha256'] or p.stat().st_size!=cp['bytes']:failures.append(['duplicate_replay_binding',h,cp['path']])
 bindings.append(h)
covered=set(bindings);excluded={x['original_sha256'] for x in D.get('exclusions',[])};owner_coverage={}
for filename in ['foundations/SOURCES_AND_READING.json','geometry/SOURCE_REGISTER.json','proofs/SOURCE_REGISTRY.json','evidence/SOURCE_MAP.json']:
 doc=read(B/filename);sources=doc.get('sources',doc);sources=sources.values() if isinstance(sources,dict) else sources
 sources=list(sources); missing=[x['sha256'] for x in sources if x['sha256'] not in covered|excluded]
 owner_coverage[filename]={'source_rows':len(sources),'unmapped':missing}
 if missing:failures.append(['unmapped_owner_sources',filename,missing])
patterns={
 'machine_locator':r'/(?:workspace|home|Users|root|mnt/data)/|[A-Z]:[\\/](?:Users|workspace)',
 'private_linkage':r'(?:file-[A-Za-z0-9]{15,}|msg_[A-Za-z0-9]{15,}|library_file_id|sediment://|codex://threads/)',
 'signed_url':r'[?&](?:sig|X-Amz-Signature|token)=',
 'credential_pattern':r'gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
 'email':r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'}
hits=[];banned=[];symlinks=[];missing_links=[]
math=re.compile(r'\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\\)\$(?!\$)(?:\\.|[^$\n])*?(?<!\\)\$')
for p in sorted(P.rglob('*')):
 rel=p.relative_to(P).as_posix()
 if p.is_symlink():symlinks.append(rel)
 if not p.is_file():continue
 if p.suffix.lower() in {'.zip','.7z','.rar','.jsonl','.pyc','.olean','.ilean','.so','.sqlite3'} or p.name.startswith('.env') or '__pycache__' in p.parts:banned.append(rel)
 try:text=p.read_text()
 except UnicodeError:failures.append(['nontext_payload',rel]);continue
 for label,pat in patterns.items():
  ms=list(re.finditer(pat,text))
  if ms:hits.append({'path':rel,'label':label,'count':len(ms),'line_numbers':[text[:m.start()].count('\n')+1 for m in ms]})
 if p.suffix=='.md':
  stripped=math.sub(lambda m:''.join('\n' if c=='\n' else ' ' for c in m[0]),text)
  for m in re.finditer(r'\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)',stripped):
   target=m[1]
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
   if not (p.parent/target).exists():missing_links.append({'path':rel,'target':target,'line':stripped[:m.start()].count('\n')+1})
if banned:failures.append(['forbidden_payloads',banned])
if symlinks:failures.append(['symlinks',symlinks])
result={'captured_utc':snapshot['captured_utc'],'package_file_array_sha256':snapshot['file_array_sha256'],'source_bindings':len(bindings),'projection_counts':dict(collections.Counter(r['projection'] for r in D['files'])),'disposition_counts':dict(collections.Counter(r['disposition'] for r in D['files'])),'owner_coverage':owner_coverage,'failures':failures,'privacy_pattern_hits_requiring_manual_classification':hits,'banned_payloads':banned,'symlinks':symlinks,'regex_markdown_link_candidates':missing_links,'link_scan_limit':'Math spans stripped using pinned baseline expression. Regex screen is not a full CommonMark parser or a full repository validation.'}
(R/'CANDIDATE_INSPECTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()},indent=2))
