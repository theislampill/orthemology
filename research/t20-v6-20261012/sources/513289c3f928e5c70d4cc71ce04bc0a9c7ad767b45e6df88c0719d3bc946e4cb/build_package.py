from pathlib import Path
import shutil, json, hashlib
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'t20-continuation-20261008'
STAGE=BASE/'delivery/stage-final'
STAGE.mkdir(exist_ok=True)
selected=[]
for section in ['source-dependencies','efficacy-warrant','valued-cooperation','effect-production','independent-review']:
 for p in sorted((BASE/section).rglob('*')):
  if not p.is_file(): continue
  rel=p.relative_to(BASE/section)
  if any(x in rel.parts for x in ['__pycache__','sources','primary-readbacks','reviewed-snapshots']): continue
  if p.suffix not in ['.md','.json','.jsonl','.py','.log','.txt']:continue
  target=STAGE/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);selected.append(str(p.relative_to(ROOT)))
for name in ['RECOVERY.json','ROOT_SOURCE_REVIEW.md']:
 p=BASE/name; target=STAGE/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ['Orthemology_T20_Targeted_Source_Addendum_20261008.zip','Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008.zip']:
 p=ROOT/'recovery-t20'/name;target=STAGE/'checkpoints'/name;target.parent.mkdir(exist_ok=True);shutil.copy2(p,target)
(STAGE/'SELECTION.json').write_text(json.dumps({'kind':'additive_research_review_not_repository_integration','selected_successor_paths':selected,'excluded':'Primary source bodies, PDFs, images, transient bytecode and duplicate review snapshots. Original receipts may bind excluded source bytes; those remain source acquisition records, not self-contained source-collation claims.','predecessors':'Two exact latest checkpoint ZIPs are embedded unchanged for reproducible dependencies. Earlier original consolidated and first supplement remain preserved in Library; this archive is not their replacement.'},indent=2))
print(STAGE, len(selected))
