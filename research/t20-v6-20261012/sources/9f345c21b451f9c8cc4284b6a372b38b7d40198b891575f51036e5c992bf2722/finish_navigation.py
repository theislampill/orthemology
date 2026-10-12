from pathlib import Path
import sys,json,re,collections
sys.path.insert(0,'private-locator:d6057749b06d9c8f270e')
from reconstruct_publication import sha,dump,require,tree
root=Path('private-locator:464813627ad1f0d8df15')
pkg=Path('private-locator:90a296a8ad91d8f0e383')
j=json.loads((pkg/'PUBLIC_OVERLAY/research/t20-live-20261009/INDEX.json').read_text())
orig_members=json.loads((pkg/'inventory/ALL_MEMBERS.json').read_text())
removed_counts=collections.Counter();removed_redactions=collections.Counter()
for m in orig_members:
 if m.get('repo_path','').endswith('.jsonl'):
  removed_counts[m['checkpoint_id']]+=1;removed_redactions[m['checkpoint_id']]+=m.get('redacted_private_machine_paths',0)
for r in j['records']:
 cp=r['id'];r['public_files']-=removed_counts[cp];r['private_only_files']+=removed_counts[cp];r['private_locator_substitutions']-=removed_redactions[cp]
 if cp=='CP08':r['private_locator_substitutions']+=6
 if cp=='CP21':r['private_locator_substitutions']-=2
 if cp=='CP22':r['private_locator_substitutions']-=2;r['public_files']-=1;r['private_only_files']+=1
cp23={'id':'CP23','original_name':'T20_Resumed_Research_Intermediate_Checkpoint23_20261009.zip','private_locator_substitutions':6,'private_only_files':52,'public_files':105,'navigation_files':2,'public_path':'checkpoints/CP23','source_members':157,'source_sha256':'1be566be13c1317cafd63e35e6d58c79af826b5c9df13ac994f6b672f3156633'}
j['records'].insert(next(i for i,r in enumerate(j['records']) if r['id']=='S01'),cp23)
j['source_archive_shas']['CP23']=cp23['source_sha256']
j.update(numbered_checkpoints=23,published_files=2063,total_public_files=2067,generated_navigation_files=4)
j['nonclaims'][2]='No claim original ZIP members equal mechanically redacted or amended public copies; original source and replay hashes retain their original scope'
upstream='https://github.com/Nakammura/spinoza-ethica-lean/blob/6d4c0461265e50a3bbedb640fe60d9ad292b50a7/'
a='checkpoints/CP21/spinoza-formal-transfer-screen-20261009/'
refs=[{'new_field':'upstream_url','old_field':'repository_path','path':'checkpoints/CP21/REFERENCE_ONLY_CODE.json','upstream_url':upstream+'docs/auxiliary_axioms.md'}, {'new_field':'upstream_url','old_field':'path','path':a+'READING_LEDGER.json','upstream_url':upstream+'docs/auxiliary_axioms.md'}, {'link_label':'upstream coverage register','path':a+'sources/README.md','upstream_url':upstream+'docs/coverage.md'}, {'link_label':'upstream gap register','path':a+'sources/README.md','upstream_url':upstream+'docs/gaps.md'}, {'new_field':'upstream_url','old_field':'path','path':a+'VERIFICATION.json','upstream_url':upstream+'docs/auxiliary_axioms.md'}, {'path':a+'source-bindings.json','removed_redundant_field':'path','retained_url_field':'url','upstream_url':upstream+'docs/auxiliary_axioms.md'}]
j['publication_repairs']={'historical_commit_boundary':'Withholding or aliasing in this revision does not erase previously published commits. Original source/replay hashes still bind original private bytes, not the amended public projections.', 'private_linkage_inventory':{'alias_policy':'Distinct typed aliases preserve equality across records and JSON keys. Original-to-public map remains private; aliases are not live Library/file/message locators.','aliased_by_type':{'conversation_file_id':4,'library_file_id':187,'message_id':16},'delivery_records_withheld':2,'files_aliased':37,'files_before':39,'occurrences_aliased':207,'occurrences_before':217,'occurrences_withheld':10,'remaining_original_identifiers':0},'restored_license':{'bytes':1188,'path':a+'sources/LICENSE','sha256':'47b99d4833f7c801c29bdf0e0c8488a6e9f5f5fd26d0a54a816982b783b7e837','upstream_url':upstream+'LICENSE'},'reviewed_head':'aba0bce3d651ab7f09cb9aa6a31c395e31e900fc','scope':'Mechanical publication repair only; T20 ACTIVE; scientific and original verification scopes unchanged.','upstream_reference_qualifications':refs,'withheld_delivery_records':['checkpoints/CP21/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint20_20261009.LIBRARY_DELIVERY.json','checkpoints/CP22/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint21_20261009.LIBRARY_DELIVERY.json']}
dump(root/'INDEX.json',j)
# Derive the root navigation from the old, independently bound candidate.
t=(pkg/'PUBLIC_OVERLAY/research/t20-live-20261009/README.md').read_text()
t=t.replace('The 22 sequential checkpoint ZIPs','The 23 sequential checkpoint ZIPs')
for r in j['records']:
 cp=r['id']
 if cp in removed_counts or cp=='CP22':
  pattern=r'(- \*\*'+cp+r'\*\*[^\n]*?original members, )\d+( public projected files\.)'
  t,n=re.subn(pattern,lambda m:m.group(1)+str(r['public_files'])+m.group(2),t);require(n==1,'README row '+cp)
t=t.replace('- **S01** —','- **CP23** — [Resumed research checkpoint 23](checkpoints/CP23/PUBLICATION.md); 157 original members, 105 public research files plus two navigation records. Recorded Lean frontier theorem; separately scoped written and finite-tested certificate compilation. Internal AI reviews only; subsequent research remains active.\n- **S01** —')
old='Some public projections only replace private machine locators with `[OMITTED_PRIVATE_MACHINE_PATH]`.'
new='Public projections replace private machine locators with `[OMITTED_PRIVATE_MACHINE_PATH]` where needed. Owner-approved publication markup corrects one CP02 relative link, displays unavailable CP04 historical links as literal locators, and marks one unchanged CP05 formula as inline code to prevent false link parsing. These changes are recorded in the private source-to-public bindings; scientific text and verdicts are not revised. Sixty event/session JSONL files remain private under the repository publication boundary.'
require(t.count(old)==1,'README sentence');t=t.replace(old,new)
repair='''## Publication repair boundary

The review repair preserves **23 numbered checkpoints plus S01**: 2,063 source projections and four navigation records, 2,067 public files total. The 24 private original ZIPs still contain 2,978 members; 915 members remain private. Two delivery-only records are withheld. Across the required reports, 207 private Library/file/message linkage occurrences use consistent distinct typed aliases; the other ten occurrences belonged to the withheld records. Aliases preserve identity and equality, including JSON keys, but are not working locators. The original-to-public map remains private. Public source identities and original archive/member hashes are preserved.

Six CP21 references now identify their external owner at [the pinned upstream commit](https://github.com/Nakammura/spinoza-ethica-lean/tree/6d4c0461265e50a3bbedb640fe60d9ad292b50a7). Three JSON path fields become URL fields for the affected records only; one redundant path field is removed while its existing pinned URL remains; two Markdown labels identify upstream registers. This supersedes the earlier CP21 gap-link escaping. The copied component's [original licence](checkpoints/CP21/spinoza-formal-transfer-screen-20261009/sources/LICENSE) is restored byte-for-byte. The [checkpoint index](INDEX.json) records exact public destinations, field transformations, omissions and counts.

Original source/replay hashes in historical records continue to identify original private bytes. Amended projection hashes identify the public copies; these mechanical changes are not new kernel verification, scientific evidence or external peer review. A corrective commit does not remove earlier public history. T20 remains ACTIVE and all stopped or deferred research boundaries remain in force.

'''
require(t.count('## Source entry points')==1,'README insertion');t=t.replace('## Source entry points',repair+'## Source entry points')
(root/'README.md').write_text(t)
for name,expected in [('INDEX.json','578b2f63c3038627a68c1d4cd816ca9f9a3cd973ee35864a5c22e3860f2f7483'),('README.md','543cc8ea246fdc3f1fb03e0b41bb539dde2f23a7eeaa2ddf9178826840b5f139')]:
 actual=sha((root/name).read_bytes());print(name,len((root/name).read_bytes()),actual,actual==expected)
print('FULL TREE',tree(root))
