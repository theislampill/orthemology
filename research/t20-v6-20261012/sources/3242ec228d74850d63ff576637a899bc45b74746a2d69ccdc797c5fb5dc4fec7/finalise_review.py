from pathlib import Path
import json
OUT=Path('private-locator:a12b7fb1f25ab7f5d347')
p=json.loads((OUT/'REVIEW_CONTENT_DRAFT.json').read_text())
repls={
 'FINAL_EFFECT_SUMMARY':'Nineteen scoped effect-contract checks pass in independent AI replay. Source-neutral effect identity, declared productive routes and logical occurrence certificates are now separate. Adding a redundant certificate leaves production unchanged; adding a productive route can change it despite the same endpoint table.',
 'FINAL_EFFECT_COUNT':'nineteen',
 'FINAL_EFFECT_REVIEW_LOCATOR':'successor-issued-profile/REVIEW.md, REVIEW_BINDINGS.json, LOCAL_19_REPLAY.log and ISOLATED_19_REPLAY.log. The earlier EFFECT_REVIEW.md and EFFECT_FINAL_BINDINGS.json remain eighteen-check historical records',
 'A second concrete route is an independently identified indirect causal history with enough occurrence information for faithful transport. The present direct adapter does not claim that extension.':'The new indirect-history test already supplies three-occurrence and four-occurrence histories projecting to the same full inherited Run. Their different outcomes under fixed-lineage deletion expose the missing occurrence information. The next advance would need an independently identified actual history or a justified canonical convention; the direct adapter still rejects indirect Run-only input.',
}
for pg in p:
 for b in pg['blocks']:
  if 'text' in b:
   for a,z in repls.items():b['text']=b['text'].replace(a,z)
# Keep the substantive occurrence advance visible rather than leaving it only in the outlook.
p[1]['blocks'].insert(-1,{'kind':'sub','title':'A concrete occurrence boundary','text':'The final effect investigation also tests an indirect programme. Two explicitly supplied occurrence histories, with three and four occurrences, project to the same complete inherited Run. Fixed-lineage deletion loses the downstream effect in one and retains it in the other. The inherited deterministic history function still correctly returns three per-proof tuples. The refinements are extra declared semantics, not two executions of that function; deletion without rescheduling differs from disabling a rule and recomputing closure. This is a scoped application of the inherited H continuation criterion. [S7]'})
# Source catalogue names the final review.
for b in p[-1]['blocks']:
 if b.get('title','').startswith('S6 '):
  b['text']=b['text'].replace('SOURCE_REVIEW.md and VALUED_REVIEW.md','SOURCE_REVIEW.md, VALUED_REVIEW.md and EFFECT_REVIEW.md')
# Preserve review-discovered defects and fixes without treating replay as new science.
p[7]['blocks'].insert(2,{'kind':'p','text':'Independent AI review reproduced two further defects: certificate enumeration for nondefault event states, and applicability not bound to the ledger’s own issued-act profile. Both repairs have regression checks, alongside the earlier certificate-binding, state and lineage corrections. The eighteen-check receipt is retained as a historical intermediate; the final effect receipt covers nineteen checks. The final exact-hash review reports no unresolved load-bearing code/report discrepancy within its scope. The philosophical efficacy dispute remains open. [S6, S7]'})
for b in p[-1]['blocks']:
 if b.get('title','').startswith('S6 '):
  b['text'] += ' The latest nineteen-check disposition is in successor-issued-profile/REVIEW.md; the earlier REVIEW_SUMMARY.md and EFFECT_REVIEW.md retain the eighteen-check boundary. CONTRACT_FINDING.json preserves the reproduced helper defect.'
# UK English editorial normalisation leaves original status values unchanged.
for pg in p:
 for b in pg['blocks']:
  for field in ['title','text']:
   if field in b:
    for a,z in {'authorizes':'authorises','authorize':'authorise','normalization':'normalisation','axiomatization':'axiomatisation','neighboring':'neighbouring','[S1–S6]':'[S1–S7]'}.items():
     b[field]=b[field].replace(a,z)
for pg in p:
 for b in pg['blocks']:
  if b.get('title')=='Boundary ledger COMPLETED':
   b['text']=b['text'].replace('Current continuation needs a successor overlay; old plan labels must not erase later executions.', 'This successor overlay records the additions; final integration remains pending. Old plan labels must not erase later executions.')
# Primary links retain the exact reported targets.
for b in p[-1]['blocks']:
 if b['kind']=='links':
  b['items'][1][1]='https://islamweb.net/ar/library/content/60/1674/الإمام-الشافعي'
  b['items'][2][1]='https://www.islamweb.net/ar/library/content/60/4654/الهكاري'
  b['items'].append(['Minhaj 2 efficacy passage','https://islamweb.net/ar/library/content/108/157/'])
for b in p[7]['blocks']:
 if b.get('text','').startswith('The inherited addendum’s 27'):
  b['text']=b['text'].replace('They must not be totalled as independent discoveries', 'Together these are 35 targeted implementation checks. They must not be counted as 35 independent discoveries')
p[-1]['blocks'][0]['text']='These locators identify the evidence used in the review. The delivery manifest determines which files are included. Primary source bodies and reviewed snapshots are not all distributed in the public packet; links and identities do not reproduce excluded witnesses. Relative paths distinguish the recovered checkpoint, addendum and successor evidence.'
assert 'FINAL_EFFECT' not in json.dumps(p)
(OUT/'REVIEW_CONTENT.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
o=json.loads((OUT/'REVIEW_OBLIGATIONS_DRAFT.json').read_text())
o['pending_lane']=None
for r in o['formal_objective_submatrix']:
 if r['id']=='BOUNDARY_LEDGER':
  r['limit']='This successor overlay records the additions; final integration remains pending. Old plan labels must not erase later executions.'
o['scientific_lane_status']['effect_production']='completed_19_checks_independently_replayed'
o['scientific_lane_status']['all_assigned_scientific_reports_received']=True
(OUT/'REVIEW_OBLIGATIONS.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
lines=[]
for pg in p:
 lines.append('# '+pg['title'])
 for b in pg['blocks']:
  if b['kind']=='sub':lines.extend(['','## '+b['title'],'',b['text']])
  elif b['kind']=='p':lines.extend(['',b['text']])
  elif b['kind']=='links':lines.extend(['']+[f'[{t}]({u})' for t,u in b['items']])
 lines.extend(['',''])
(OUT/'Orthemology_T20_Updated_Owner_Review_Source_20261008.md').write_text('\n'.join(lines))
for n,pg in enumerate(p,1):
 words=sum(len(b.get('text','').split()) for b in pg['blocks'])
 print(n,words,pg['title'])
