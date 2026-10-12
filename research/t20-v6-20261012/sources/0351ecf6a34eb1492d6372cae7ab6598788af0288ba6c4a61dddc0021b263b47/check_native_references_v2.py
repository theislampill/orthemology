#!/usr/bin/python3
"""Run exact pinned reference/parser functions on real candidate+selected baseline bytes."""
from pathlib import Path
import json,shutil,importlib.util,sys,hashlib
B=Path(__file__).resolve().parents[2];R=B/'review/portability';stage=R/'reference-stage-v2';S=stage/'scripts';S.mkdir(parents=True,exist_ok=True)
receipts=json.loads((B/'catalogue/repository-evidence/FETCHED_FILE_BYTE_RECEIPT.json').read_text())
for name in ['validate_repo.py','validate_internal_references.py','generate_current_state.py','validate_v5_successors.py']:
 source=B/'catalogue/repository-evidence'/('scripts__'+name);raw=source.read_bytes();expected=next(x for x in receipts if Path(x['file']).name==source.name)
 assert hashlib.sha256(raw).hexdigest()==expected['sha256']
 (S/name).write_bytes(raw)
P=stage/'research/t20-consolidated-20261011'
if P.exists():shutil.rmtree(P)
shutil.copytree(B/'projection/package-v2',P)
sys.path.insert(0,str(S));import validate_repo as v;import validate_internal_references as i
i.ROOT=str(stage);v.ROOT=str(stage)
missing=[];occurrences=0;files=0
for p in sorted(P.rglob('*')):
 if p.suffix not in i.SCAN_EXT:continue
 src=p.relative_to(stage).as_posix();text=p.read_text();files+=1
 for cited,line in i._citation_occurrences(src,text,root=stage,successor_sources=[]):
  occurrences+=1
  if not i._resolves(src,cited):missing.append({'source':src,'cited':cited,'line':line})
result={'scope':'Exact pinned validate_internal_references._citation_occurrences and _resolves over a disposable copy of the proposed payload plus four exact selected baseline scripts. No full baseline checkout, exemption registry, historical source registry or Git-native full-check invocation is claimed.','baseline_commit':'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c','files_scanned':files,'citation_occurrences':occurrences,'unresolved':missing,'validator_sha256':hashlib.sha256((S/'validate_internal_references.py').read_bytes()).hexdigest(),'parser_owner_sha256':hashlib.sha256((S/'validate_repo.py').read_bytes()).hexdigest()}
(R/'NATIVE_REFERENCE_SCOPE_CHECK_V2.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'files_scanned':files,'citation_occurrences':occurrences,'unresolved_count':len(missing),'first_unresolved':missing[:15]},indent=2))
