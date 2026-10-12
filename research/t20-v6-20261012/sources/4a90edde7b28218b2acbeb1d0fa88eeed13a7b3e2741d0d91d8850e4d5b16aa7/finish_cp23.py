from pathlib import Path
import sys,json,re
sys.path.insert(0,'private-locator:d6057749b06d9c8f270e')
from reconstruct_publication import sha,dump,require,tree
root=Path('private-locator:864f97b6fbd7fa2f623e')
records=json.loads(Path('private-locator:3fd48e56fa4537ba2b58').read_text())
for r in records:
 p=root/r['path'];b=p.read_bytes()
 if sha(b)!=r['public_sha256']:
  require(r['path']=='warranted-discrimination-research-20261009/SOURCES.json','Unexpected CP23 repair')
  r.update(projection='private_linkage_aliased',public_bytes=len(b),public_sha256=sha(b),private_linkage_alias_counts={'library_file_id':2})
pub={'schema':'t20-checkpoint-public-projection-v1','checkpoint':'CP23','status':'T20 ACTIVE','source_files':105,'private_only_files':52,'machine_prefix_replacements':6,'records':records,'original_hash_scope':'Original hashes bind private source bytes. Public hashes bind the selected, possibly redacted copies. Historical manifests and evidence bindings retain their original scope.','research_execution_by_integration':False,'review_scope':'Internal AI review records; not external peer review.','private_linkage_aliases':{'affected_files':1,'identity_map':'Owner-private; distinct aliases preserve equality with S01.','occurrences':2}}
dump(root/'PUBLIC_PROJECTION.json',pub)
# Decode only the known historical text literal, never execute the transcript.
s=Path('private-locator:fb3b375ee082af806c00 text(20261009-125604).txt').read_text()
s='\n'.join(l[2:] if l.startswith('> ') else '' if l=='>' else l for l in s.splitlines())
start=s.index("(dest/'PUBLICATION.md').write_text('''")+len("(dest/'PUBLICATION.md').write_text('''")
end=s.index("''',encoding='utf-8')",start)
t=s[start:end]
old='Six private scratch-directory prefixes in five files are replaced by `[OMITTED_PRIVATE_MACHINE_PATH]`; all other selected research bytes are unchanged.'
new='Six private scratch-directory prefixes in five files are replaced by `[OMITTED_PRIVATE_MACHINE_PATH]`. Two private Library linkage values in the warranted-discrimination source record use distinct aliases consistent with S01; their identity map remains private. All other selected research bytes are unchanged.'
require(t.count(old)==1,'Publication sentence');t=t.replace(old,new)
(root/'PUBLICATION.md').write_text(t)
for name,expected in [('PUBLICATION.md','15310de15d233f992d03ffa7101f557acfecce34fba946dcf7c586a517bffcb0'),('PUBLIC_PROJECTION.json','3bb0e641c13a1e842c24fe2c32b61c859862d88a140730587da9cb03c648982f')]:
 actual=sha((root/name).read_bytes());print(name,actual,actual==expected);require(actual==expected,name)
print('CP23 tree',tree(root));require(tree(root)=='3c89eda2128612998dec073c298757f91c882876','CP23 tree')
