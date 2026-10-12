"""Read-only source reconstruction; never invokes source-archive code or writes a Git repository."""
from pathlib import Path
import hashlib,json,re,shutil,collections
BASE=Path('/mnt/data')
PKG=BASE/'recovered/T20_Live_Integration_Handoff_20261009/T20_Live_Integration_Handoff_20261009'
CP23=BASE/'recovered/T20_Resumed_Research_Intermediate_Checkpoint23_20261009/T20_Resumed_Research_Intermediate_Checkpoint23_20261009'
OUT=BASE/'audit/reconstructed_publication'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(x,msg):
 if not x: raise RuntimeError(msg)
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
def oid(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree(p):
 entries=[]
 for f in p.iterdir():
  if f.is_dir(): entries.append((f.name.encode()+b'/',b'40000 '+f.name.encode()+b'\0'+bytes.fromhex(tree(f))))
  elif f.is_file() and not f.is_symlink():entries.append((f.name.encode(),b'100644 '+f.name.encode()+b'\0'+bytes.fromhex(oid('blob',f.read_bytes()))))
  else:raise RuntimeError(f'Unsupported file: {f}')
 return oid('tree',b''.join(b for _,b in sorted(entries)))
if __name__=='__main__':
 require(not OUT.exists(),'Output already exists; preserve prior attempt')
 shutil.copytree(PKG/'PUBLIC_OVERLAY/research/t20-live-20261009',OUT)
 # Declared original mechanical repairs. Sources themselves remain untouched.
 changed=[]
 p=OUT/'checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport-review/VERIFICATION.json'
 b,n=re.subn(rb'private-locator:c895d03ab0cf3731d677[A-Za-z0-9_-]+/',b'[OMITTED_PRIVATE_MACHINE_PATH]/',p.read_bytes());require(n==6,'CP08 prefix count');p.write_bytes(b)
 p=OUT/'checkpoints/CP02/t20-next-frontier-20261008/noise-aware-review/frozen/RESULT.md'
 b=p.read_bytes();old=b'](../noise-aware-review/RESTRICTED_MASK_LOWER_BOUND.md)';require(b.count(old)==1,'CP02 link count');p.write_bytes(b.replace(old,b'](../RESTRICTED_MASK_LOWER_BOUND.md)'))
 p=OUT/'checkpoints/CP04/t20-next-frontier-20261008/action-genus-scope-audit/EXACT_EVIDENCE.md'
 b=p.read_bytes();b,n=re.subn(rb'\]\((\.\./(?:ontology-type-control|targeted-final-loci)/[^)]+)\)',rb']\\(\1)',b);require(n==10,'CP04 link count');p.write_bytes(b)
 p=OUT/'checkpoints/CP05/t20-next-frontier-20261008/grouped-calibration-invariants-review/REVIEW.md'
 b=p.read_bytes();old=b'theta(d,e)=[(e-d)/(2e)](d/e)^[d/(e-d)]';require(b.count(old)==1,'CP05 formula');p.write_bytes(b.replace(old,b'`'+old+b'`'))
 p=OUT/'checkpoints/CP21/spinoza-formal-transfer-screen-20261009/sources/README.md'
 b=p.read_bytes();old=b'[`docs/gaps.md`](docs/gaps.md)';require(b.count(old)==1,'CP21 link');p.write_bytes(b.replace(old,b'[`docs/gaps.md`]\\(docs/gaps.md)'))
 removed=[]
 for p in OUT.rglob('*.jsonl'):removed.append(p.relative_to(OUT).as_posix());p.unlink()
 require(len(removed)==60,'JSONL omission count')
 # CP23 public selection is reconstructed from the declared path/suffix boundary.
 exclude_roots={'COMPONENT_MANIFEST_CHECKS.json','MANIFEST.json','MANIFEST.sha256','OMISSIONS_AND_DEPENDENCIES.json','PRESERVATION_RECEIPT.json','PRESERVED_INPUTS.json','PRIOR_CHECKPOINT.json','SUPPLIED_COMPANION.json'}
 exclude_dirs={'prior-checkpoint-identities','independent-research-companion-20261009','replay'}
 records=[]
 for p in sorted(CP23.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(CP23)
  if p.name in {'AGENTS.md','AGENTS.override.md'} or str(rel) in exclude_roots or rel.parts[0] in exclude_dirs or p.suffix.lower() not in {'.md','.json','.py','.sh','.lean','.csv','.jsonl'}:continue
  raw=p.read_bytes();b,n=re.subn(rb'private-locator:c895d03ab0cf3731d677[A-Za-z0-9_-]+/',b'[OMITTED_PRIVATE_MACHINE_PATH]/',raw)
  dest=OUT/'checkpoints/CP23'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
  records.append({'path':str(rel),'original_sha256':sha(raw),'public_sha256':sha(b),'public_bytes':len(b),'projection':'machine_locator_redacted' if n else 'exact','machine_prefix_replacements':n})
 require(len(records)==105,'CP23 selection count')
 dump(BASE/'audit/cp23_initial_records.json',records)
 # Retain old-head source map before the later privacy repair.
 oldfiles={str(p.relative_to(OUT)): {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'git_blob':oid('blob',p.read_bytes())} for p in OUT.rglob('*') if p.is_file()}
 dump(BASE/'audit/pre_repair_source_projection.json',oldfiles)
 patterns={'library':r'libfile_[A-Za-z0-9]+','message':r'Sentinel_[A-Za-z0-9]+','file':r'file_[0-9a-fA-F]{32}'}
 matches={k:set() for k in patterns};counts=collections.Counter()
 for p in OUT.rglob('*'):
  if not p.is_file():continue
  t=p.read_text(errors='strict')
  for k,rx in patterns.items():
   # Require token boundary so file_ does not match inside libfile_.
   found=re.findall(r'(?<![A-Za-z0-9_])'+rx,t);matches[k].update(found);counts[k]+=len(found)
 print('Original identifier matches',dict(counts),'unique', {k:len(v) for k,v in matches.items()})
 aliases={old:f'private-{kind}-alias-{i:03d}' for kind,vals in matches.items() for i,old in enumerate(sorted(vals),1)}
 dump(BASE/'audit/PRIVATE_ALIAS_MAP.json',aliases)
 # Delete only the two specified delivery records, keeping all original archive bytes.
 withheld=['checkpoints/CP21/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint20_20261009.LIBRARY_DELIVERY.json','checkpoints/CP22/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint21_20261009.LIBRARY_DELIVERY.json']
 for rel in withheld:require((OUT/rel).is_file(),rel);(OUT/rel).unlink()
 for p in OUT.rglob('*'):
  if not p.is_file():continue
  b=p.read_bytes();old=b
  for src,dst in aliases.items():b=b.replace(src.encode(),dst.encode())
  if b!=old:p.write_bytes(b);changed.append(str(p.relative_to(OUT)))
 print('Aliased files',len(changed))
 # Source-rights repair uses exact original upstream bytes kept by prior independent reviewer.
 notice=BASE/'recovered/Orthemology_PR33_Independent_Review_20261009/Orthemology_PR33_Independent_Review_20261009/UPSTREAM_LICENSE_TO_RESTORE.txt'
 require(sha(notice.read_bytes())=='47b99d4833f7c801c29bdf0e0c8488a6e9f5f5fd26d0a54a816982b783b7e837','Licence bytes')
 (OUT/'checkpoints/CP21/spinoza-formal-transfer-screen-20261009/sources/LICENSE').write_bytes(notice.read_bytes())
 # Reference owner correction: preserve file-specific formatting and all unrelated content.
 root=OUT/'checkpoints/CP21/spinoza-formal-transfer-screen-20261009'
 upstream='https://github.com/Nakammura/spinoza-ethica-lean/blob/6d4c0461265e50a3bbedb640fe60d9ad292b50a7/'
 for p,field in [(OUT/'checkpoints/CP21/REFERENCE_ONLY_CODE.json','repository_path'),(root/'READING_LEDGER.json','path'),(root/'VERIFICATION.json','path')]:
  b=p.read_text();old='"'+field+'": "docs/auxiliary_axioms.md"';require(b.count(old)==1,f'{p}: reference count');p.write_text(b.replace(old,'"upstream_url": "'+upstream+'docs/auxiliary_axioms.md"'))
 p=root/'source-bindings.json';t=p.read_text();t,n=re.subn(r'^\s*"path": "docs/auxiliary_axioms.md",\n','',t,flags=re.M);require(n==1,'source-bindings redundant field');p.write_text(t)
 p=root/'sources/README.md';t=p.read_text();t=t.replace('[`docs/coverage.md`](docs/coverage.md)','[upstream coverage register]('+upstream+'docs/coverage.md)');t=t.replace('[`docs/gaps.md`]\\(docs/gaps.md)','[upstream gap register]('+upstream+'docs/gaps.md)');p.write_text(t)
 expected=['b3604d24ded308a72c38d3a3278fc56287cc61dc','ade7c2306d54ddf6f574f4418dbd41702ecabed5','2ca1ae0196c62c466c5b8ad9937a0d5f2436242d','ceaa5befbf94b3f00b9f23e0d1515325716f5526','8e81093070db9aa17b780d4c4cd7a0e75126f2c1','70b22bcbdee9e2bbed6951bb58d1158308dbb6df','b6265ea6d075dbd7ebda5233699dcf7cfef9a074','19336f7d29476b24c0dc8f4c1f59dea8e1780d3a','e8cbd8b30de5a8f9ec26fe6dae171430e1453b93','9e55b6762fe54616ab61a278bf80a7908630a95d','a755bf030336a2a06602cb0d18efa3656e91266c','09122c722f979f4713b5f99f13d4c020d7494358','876fff49e7fea3890657e012e11c07845e915ad7','7f81e2cb4336f7cdd6b852c916e04db909004a37','dda7318ac93aa90fad28e42f5781bcdeede3a23e','36c6ed7e752ac0845d5c7321bb7aef72c0c09573','0b6185ad88ad2972653ce8d369d00ca0c34900b6','b4e5e938f3da6a5c7dd5b010cd2efd3cb2f97c13','ab87368f518c5efc02124b3da631fea2e6e7c15f','5832f7d385dc7fc7e8be3c746cb6d2df6240b2ed','66fb585ec89753d0ecd2d59627aa2b624940a81a','8885318d3dcef2218f2e67ffebc6ef8f763cb01d','3c89eda2128612998dec073c298757f91c882876']
 results=[]
 for i,target in enumerate(expected,1):
  cp=f'CP{i:02d}';actual=tree(OUT/'checkpoints'/cp);count=sum(p.is_file() for p in (OUT/'checkpoints'/cp).rglob('*'));print(cp,count,actual,actual==target);results.append({'checkpoint':cp,'files':count,'expected_git_tree':target,'actual_git_tree':actual,'match':actual==target})
 print('supplement',tree(OUT/'supplement'),'dd697e4173bdaa89cb0fe1962200ee39b4a2c3f3')
 dump(BASE/'audit/reconstruction_stage1.json',results)
