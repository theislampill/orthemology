from pathlib import Path
import hashlib,json,shutil,re,subprocess,sys
W=Path(__file__).resolve().parents[2]; D=W/'t20-depth-reassessment-20261011'; B=W/'t20-consolidation-20261011'; P=B/'projection/package-v3'; V=B/'projection/package-v2'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(rel,obj):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def write(rel,text):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
projection=json.loads((V/'PUBLIC_PROJECTION.json').read_text()); rows=projection['files']; byhash={r['original_sha256']:r for r in rows}; transforms=[]
def add(src,rel,owner,kind='EXACT',public=None):
 src=Path(src); raw=src.read_bytes(); h=sha(raw); out=raw if public is None else public.encode() if isinstance(public,str) else public
 writepath=P/rel;writepath.parent.mkdir(parents=True,exist_ok=True);writepath.write_bytes(out)
 own={'track':'consolidation-depth-reassessment','source_id':owner}
 if h in byhash:
  r=byhash[h]
  if own not in r['owners']:r['owners'].append(own)
  if rel!=r.get('public_path'):
   r.setdefault('required_replay_copies',[])
   if not any(x['path']==rel for x in r['required_replay_copies']):r['required_replay_copies'].append({'path':rel,'sha256':sha(out),'bytes':len(out),'reason':'Separately dated reassessment portable replay or exact source evidence.'})
 else:
  r={'original_sha256':h,'original_bytes':len(raw),'owners':[own],'original_member_bindings':[{'member':src.name,'context':'Separately received or authored consolidation-depth reassessment, 2026-10-11'}],'original_identity_scope':'Scientific owner bytes or explicitly derived public locator projection; no inherited execution scope enlargement.','disposition':'included','projection':kind,'public_path':rel,'public_sha256':sha(out),'public_bytes':len(out)}
  if out!=raw:r['transformations']=['Private custody locators mapped to selected package sources; original and public hashes distinguished.']
  rows.append(r);byhash[h]=r
 if out!=raw:transforms.append({'path':rel,'original_sha256':h,'public_sha256':sha(out),'transformation':r.get('transformations',['Derived public companion'])[0]})
 return r

def locate(h,path=''):
 if h in byhash:
  r=byhash[h]
  candidates=[]
  if r.get('public_path'):candidates.append(r['public_path'])
  candidates += [x['path'] for x in r.get('required_replay_copies',[])]
  for rel in candidates:
   if sha((P/rel).read_bytes())==h:return rel
  if candidates:return candidates[0]
  return r['public_url']
 prefix='t20-consolidation-20261011/'
 if path.startswith(prefix) and (V/path[len(prefix):]).is_file():
  rel=path[len(prefix):]
  return 'reassessment/inherited-reader-v2/'+rel if rel in HISTORICAL_READERS else rel
 if path.endswith('grouped-source-audit-gradient-20261011/INPUT_BINDINGS.json'):return 'replay/grouped-source-audit-gradient-20261011/INPUT_BINDINGS.json'
 return None

def binding(item):
 h=item.get('sha256');path=item.get('path','');rel=locate(h,path) if h else None
 out={k:v for k,v in item.items() if k not in ('path','original_locations','sha256','bytes')}
 out.update(original_sha256=h,original_bytes=item.get('bytes'))
 if rel:
  out['public_source']=rel
  if not rel.startswith('https://'):
   raw=(P/rel).read_bytes();out.update(public_sha256=sha(raw),public_bytes=len(raw),projection='EXACT' if sha(raw)==h else 'DERIVED_PUBLIC_LOCATOR_OR_READER')
 else:out['disposition']='Historical inspection record only; no public source-body promise for this non-scientific custody/reading register.'
 return out

HISTORICAL_READERS=['geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','foundations/FOUNDATIONAL_SYNTHESIS.md','evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md']
for rel in HISTORICAL_READERS:add(V/rel,'reassessment/inherited-reader-v2/'+rel,'historical-v2-reader-snapshot')

# New exact mathematical/report bodies and authored reader; no raw owner instructions.
for name in ['OWNER_ASSESSMENT.md','COMBINED_RESEARCH_SYNTHESIS.md']:
 add(D/name,'reassessment/'+name,'depth-'+name)
for lane,names in {
 'audit_symmetries':['RESULT.md','CLAIMS.json','EXACT_CHECKS.json','EXACT_CHECKS_OPTIMIZED.json'],
 'restricted_controls':['RESULT.md','AUTHOR_VERIFICATION.json','verification_normal.json','verification_optimised.json'],
 'foundational_interface':['RESULT.md','TIBYAN_CORRECTION.diff','SCOPE_REPLAY_NORMAL.json','SCOPE_REPLAY_OPTIMIZED.json'],
 'independent_review':['REVIEW.md','RESTRICTED_PRECISION_CORRECTION.diff','restricted_precorrection_f593393.md','CONTROL_NORMAL.json','CONTROL_OPTIMIZED.json'],
 }.items():
 for name in names:
  src=D/lane/name
  if src.exists():add(src,'reassessment/'+lane+'/'+name,lane+'-'+name)
for lane in ['audit_symmetries','foundational_interface','independent_review']:
 src=D/lane/'SOURCE_BINDINGS.json';data=json.loads(src.read_text())
 out={k:v for k,v in data.items() if k!='sources'};out['sources']=[binding(x) for x in data['sources']]
 out['projection_note']='Original workspace/custody locations omitted. Original inspection identities and scope retained; public addresses distinguish exact original bytes from authored public-reader projections.'
 add(src,'reassessment/'+lane+'/SOURCE_BINDINGS.json',lane+'-source-bindings','AMENDED',json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Exact scientific review refers to its original custody. Explicit portable target mapping resolves it.
review_targets=[]
for lane,names in {'audit_symmetries':['RESULT.md','check_exact.py','SOURCE_BINDINGS.json'],'restricted_controls':['RESULT.md','verify.py']}.items():
 for name in names:
  raw=(D/lane/name).read_bytes();target='reassessment/'+lane+'/'+name
  if name.endswith('.py'):target='replay/'+('audit-refinement' if lane=='audit_symmetries' else 'restricted-controls')+'/'+name
  review_targets.append({'original_relative_target':lane+'/'+name,'original_sha256':sha(raw),'original_bytes':len(raw),'public_target':target})
dump('reassessment/independent_review/PORTABLE_REVIEW_BINDINGS.json',{'scope':'Exact original review body retains original reviewer-custody references. Those references are not additional public replay promises. Portable targets below bind current reports and checkers; original source-binding registry is a disclosed locator projection.','targets':review_targets,'currentness_original_sha256':sha((D/'independent_review/FINAL_CURRENTNESS.json').read_bytes()),'currentness_status':json.loads((D/'independent_review/FINAL_CURRENTNESS.json').read_text())['status']})

# Source-bound owner map, reused from existing mirrored sources; no corpus rereading burden.
all_bind=[]
for lane in ['audit_symmetries','foundational_interface','independent_review']:
 for item in json.loads((D/lane/'SOURCE_BINDINGS.json').read_text())['sources']:
  b=binding(item);b['inspection_owner']=lane;all_bind.append(b)
dump('reassessment/SOURCE_OWNERS.json',{'scope':'Selected actual owners reused from the inherited current package. Inspection scopes belong to the named report/reviewer and are not assembly-wide fresh reading claims.','sources':all_bind})

# Portable author suite: mathematical checker unchanged. Only fixture resolution is derived.
audit_dir='replay/audit-refinement'
add(D/'audit_symmetries/check_exact.py',audit_dir+'/check_exact.py','audit-refinement-author-code')
add(D/'audit_symmetries/RESULT.md',audit_dir+'/RESULT.md','audit-refinement-report')
portable=[]
for i,item in enumerate(json.loads((D/'audit_symmetries/SOURCE_BINDINGS.json').read_text())['sources']):
 rel=locate(item['sha256'],item['path'])
 if rel is None or rel.startswith('https://'):raise RuntimeError('missing portable audit dependency '+item['path'])
 raw=(P/rel).read_bytes();suffix=Path(rel).suffix or '.json';target=f'inputs/source-{i:02d}{suffix}'
 write(audit_dir+'/'+target,raw.decode())
 portable.append({'path':target,'sha256':sha(raw),'bytes':len(raw),'original_source_sha256':item['sha256'],'original_source_bytes':item['bytes'],'inherited_public_source':rel,'role':item['role'],'fixture_relation':'EXACT' if sha(raw)==item['sha256'] else 'Public locator/reader projection; original currentness evidence is separately retained'})
dump(audit_dir+'/SOURCE_BINDINGS.json',{'sources':portable,'scope':'Portable source-fixture binding; replaces private assembly locations with package-public counterparts. Mathematical check_exact.py bytes unchanged.'})
write(audit_dir+'/run_portable.py','''"""Derived relocation only; exact mathematical checker and report remain unchanged."""\nfrom pathlib import Path\nimport runpy\nscope=runpy.run_path(str(Path(__file__).with_name('check_exact.py')))\nmain=scope['main']\nmain.__globals__['ROOT']=Path(__file__).resolve().parent\nmain()\n''')
write(audit_dir+'/PORTABILITY.md','''# Portable audit control\n\nThe exact author checker is unchanged. run_portable.py rebinds its read-only ROOT to this disposable suite. SOURCE_BINDINGS.json maps the eleven inspected-source entries to selected public fixtures. Original scientific owner bytes are reused exactly; four authored assembly/index counterparts and the grouped ancestry locator registry use their already-public projections where original custody-only bytes are intentionally absent. Every original digest and public fixture digest is recorded. The finite/symbolic mathematics is unchanged. This is a new portable-fixture replay, not a replay of private assembly currentness. The original 3054-count receipt remains a separately attributed historical observation.\n''')
for lane,name,folder in [('restricted_controls','verify.py','restricted-controls'),('independent_review','check_independent.py','depth-independent')]:
 add(D/lane/name,'replay/'+folder+'/'+name,lane+'-checker')
 add(D/lane/('REVIEW.md' if lane=='independent_review' else 'RESULT.md'),'replay/'+folder+'/'+('REVIEW.md' if lane=='independent_review' else 'RESULT.md'),lane+'-proof')
for src in sorted((D/'foundational_interface/scope_replay').rglob('*')):
 if src.is_file() and src.name!='CHECK_RESULTS.json':add(src,'replay/foundational-scope/'+src.relative_to(D/'foundational_interface/scope_replay').as_posix(),'FND-033-scoped-replay')
for name in ['contracts.py','test_contracts.py','test_one_shot_recovery.py']:
 add(D/'pro-intake/reconstructed-80/research'/name,'replay/finite-contracts-reconstructed/'+name,'Pro-reconstructed-80-'+name)
add(V/'replay/finite-contracts/exhaustive_oracle.py','replay/finite-contracts-reconstructed/exhaustive_oracle.py','inherited-exhaustive-oracle')
add(D/'pro-intake/fresh-local-evidence/actual-code-diff.patch','reassessment/contract_repair/EXACT_DIFF.patch','Pro-reconstructed-four-input-boundary-repairs')
add(D/'pro-intake/execution/independent_exact_controls.py','replay/pro-exact-controls/independent_exact_controls.py','Pro-new-finite-exact-controls')

# Intake prose is scientific attribution, with custody-only file pointers qualified explicitly.
for name in ['DISCREPANCY_REPORT.md','INTEGRATION_SCOPE_NOTE.md']:
 text=(D/'pro-intake'/name).read_text()
 text += '\n\n## Portable edition note\n\nOriginal intake file/path names in the report identify its source custody. The public current assessment is in this directory and the source hashes remain exact. Private transfer identities, bulk archives and unfiltered logs are not republished. Public summary evidence is CUSTODY_UPDATE.json and CONTRACT_REPAIR_STATUS.json; actual successor code/tests are under replay/finite-contracts-reconstructed. Exact changed code is retained separately.\n'
 add(D/'pro-intake'/name,'reassessment/intake/'+name,'Pro-intake-'+name,'AMENDED',text)
dump('reassessment/intake/CUSTODY_UPDATE.json',{'status':'NEW_FULL_ARCHIVE_SEAL_VERIFIED; HISTORICAL_TRIMMED_FAILURE_RETAINED','date_utc':'2026-10-11','full_archive':{'sha256':'4d8f6c155f7af4333e70e0d7ae03f4822f751fd0179abc64b087dc3617a7b5e5','bytes':68339816,'regular_files':11393,'manifest_payload_entries_verified':11392,'advertised_copied_paths_verified':9814,'previously_held_member_hashes':11391,'new_member_bytes':['MANIFEST.json','corpus/members.json']},'unchanged_authorial_111min':{'sha256':'263d3b5bf32e698b8ce2417417072cbfe882159deaacbb84f86d0e3ba83de5fe','regular_files':38,'all_already_held_byte_identically':True},'historical_trimmed_archive':'Its earlier original-payload manifest/copy-path failure remains historical fact. This newly supplied full archive closes its own package-custody gap only.','R3_88':'reported/artifact-unavailable; neither reconstructed 30 tests nor 55 authorial tests substitute for it','scope':'Mechanical archive custody recovery, not fresh semantic reading or new scientific achievement. Bulk archives intentionally remain outside this selected public candidate.'})

# Add bounded replay targets; preserve all original specs and runner behavior.
new_suites={
 'finite-contracts-reconstructed':{'directory':'finite-contracts-reconstructed','commands':[['-B','-m','unittest','discover','-s','.','-p','test_*.py','-v'],['-O','-B','-m','unittest','discover','-s','.','-p','test_*.py','-v'],['-B','exhaustive_oracle.py'],['-O','-B','exhaustive_oracle.py']],'dependencies':[],'scope':'30 tests: 26 inherited plus four reconstructed input-boundary regressions, normal/optimized; unchanged finite exhaustive oracle both modes. Separate successor candidate, not R3, not the 52-to-55 line or general Iterable support.'},
 'audit-refinement':{'directory':'audit-refinement','commands':[['-B','run_portable.py'],['-O','-B','run_portable.py']],'dependencies':['sympy'],'scope':'Exact mathematical author checker, 14 groups/3054 counted controls and public fixture checks, normal/optimized. Derived public-fixture binding replaces private assembly-location verification; universal theorem rests on written proof.'},
 'restricted-controls':{'directory':'restricted-controls','commands':[['-B','verify.py'],['-O','-B','verify.py']],'dependencies':['sympy'],'scope':'31 exact restricted-control fixtures, normal/optimized. Ordinary universal proof and domain guards separate.'},
 'depth-independent':{'directory':'depth-independent','commands':[['-B','check_independent.py'],['-O','-B','check_independent.py']],'dependencies':['sympy'],'scope':'62 independent exact checks, normal/optimized; not a formal kernel proof. Reviewer contributed tagged-instrument corollary proof; review is not independent corroboration of that contribution.'},
 'foundational-scope':{'directory':'foundational-scope','commands':[['-B','synthesis-warrant-scope-20261011/support_scope_check.py'],['-O','-B','synthesis-warrant-scope-20261011/support_scope_check.py']],'dependencies':[],'scope':'33 inherited source/dependency checks with exact owner inputs, normal/optimized; not new theorem, human-warrant classification or Lean build.'},
 'pro-exact-controls':{'directory':'pro-exact-controls','commands':[['-B','independent_exact_controls.py']],'dependencies':[],'scope':'New supplied exact-rational finite validation, normal Python only because bare assertions would be removed by optimization; independent formulas do not replay actual later integrator.'}}
runner=(V/'replay_selected.py').read_text();runner=runner.replace('\n\ndef main():','\n\n# Separately dated consolidation-depth reassessment targets.\nSUITES.update('+repr(new_suites)+')\n\ndef main():')
write('replay_selected.py',runner)
scope=json.loads((V/'REPLAY_SCOPE.json').read_text());scope['suites'].update(new_suites);scope['reassessment_utc_date']='2026-10-11';scope['historical_replay_evidence']='SELECTED_REPLAY_VERIFICATION.json retains its exact v2 scope; REASSESSMENT_REPLAY_VERIFICATION.json records fresh selected delta controls.';dump('REPLAY_SCOPE.json',scope)

# Typed additive claim records, preserving source-owned inherited tracks.
claims=[]
def claim(id,title,statement,kind,proof,dependencies,limits,evidence='Ordinary proof with exact finite controls; scoped independent review PASS'):
 raw=(P/proof.split('#')[0]).read_bytes()
 claims.append({'id':id,'title':title,'exact_statement':statement,'contribution_class':kind,'date_utc':'2026-10-11','phase':'consolidation-depth reassessment after original cutoff','evidence':evidence,'source_owner':{'path':proof.split('#')[0],'section':proof.split('#')[1] if '#' in proof else None,'sha256':sha(raw)},'dependencies':[{'claim':x[0],'relationship':x[1],'scope':x[2]} for x in dependencies],'hypotheses_and_limits':limits,'owner_acceptance':'pending','repository_adoption':False})
claim('DR-01','Several-partition gradient refinement','Simultaneous all-positive audit covariance for several partitions is equivalent to common-refinement covariance and energy decomposition.','New bounded deduction','reassessment/audit_symmetries/RESULT.md#Theorem A',[('GEO-17','theorem_dependency','Exact inherited fixed-partition classification')],'C2 energy, retained Fisher–transport metric, complete positive simplex and connected full position product; local maximal flows, no completeness or arbitrary restricted group claim.')
claim('DR-02','Generated symmetry and gradient rigidity differ','Row/column-equivariant C1 fields may retain odds-ratio dependence; explicit nongradient and invariant-energy countercontrols show why the gradient hypothesis matters.','New bounded classification and countercontrols','reassessment/audit_symmetries/RESULT.md#Proposition B and B1–B3',[('DR-01','boundary_comparison','No action-generation inference'),('GEO-17','inherited_obstruction','Original row/column action group remains proper')],'Specified 2x2 positive labelled domain and metric. Scalar energy invariance is not gradient covariance.')
claim('DR-03','Several-instrument cone corollary','Common-refinement conditioning characterizes nonempty closed convex families stable under each of finitely many complete positive identity-summing instruments.','Inherited theorem corollary via tagged-instrument application','reassessment/audit_symmetries/RESULT.md#Corollary C',[('ET-23','direct_corollary','Apply inherited Theorem 5 to one tagged mixture instrument')],'Proper finite-dimensional cone, strictly positive normalizer, complete instruments and full-column equality; zero-mass guard. Stable convex hull is not finite-history reachability. Reviewer supplied tagged proof, so independence does not apply to that proof.')
claim('DR-04','Cone-to-gradient metric transport','The refinement gradient theorem applies to normalized cone interiors after canonical-summand coordinates and the specified transported Fisher–transport metric are supplied.','Conditional structure-preserving application','reassessment/audit_symmetries/RESULT.md#Section 6',[('DR-01','theorem_dependency','Refinement classification'),('ET-23','structure_dependency','Canonical indecomposable summands and permitted branch form')],'Cone order alone supplies no metric. All positive grouped multipliers require branches from an entire admissible binary-instrument family, not one finite instrument.')
claim('DR-05','Restricted-control exact barycentre quotient','Positive laws have identical full-output histories for all permitted Fisher controls exactly when their unnormalized full-output barycentres agree within fitness-signature groups.','New bounded deduction from inherited continuation machinery','reassessment/restricted_controls/RESULT.md#Sections 2–3',[('MOM-01','dynamics_and_proof_dependency','Inherited exponential solution and generic separating control'),('H-Continuation','observable_closure_dependency','Inherited action-observation closure, located by source hash')],'Fixed simplex-valued support; controls in declared linear U; finite piecewise-constant histories; all full output coordinates. Exact histories, not finite sample recovery or calibrated psychological model.')
claim('DR-06','Restricted-control continuous augmentation','The exact minimum additional continuous real coordinates beyond q is rank(B)-rank(A); the six-point example needs one rather than full-control three.','New specialization and exact example of inherited dimension principle','reassessment/restricted_controls/RESULT.md#Sections 4–5',[('DR-05','theorem_dependency','Continuation equivalence'),('H-Continuation','lower_bound_dependency','Proposition 9 continuity/invariance-of-domain method')],'Actual admissible image BΔ°; continuous sidecar, arbitrary exact decoder. Not finite bits, sample complexity or approximate storage.')
claim('DR-07','Isolated profiles fail composed correction','A nine-point law pair has identical complete x-only and y-only output profiles but distinct outputs after x then y; their stacked record has rank eight while composed signatures require nine.','New exact realization of inherited composition obstruction','reassessment/restricted_controls/RESULT.md#Section 6',[('DR-05','theorem_dependency','Sum-control signature refinement'),('ET-05','inherited_mechanism_comparison','Separate historical revision profiles already fail composition'),('H-Continuation','closure_dependency','Combined-operation observable closure')],'Arbitrary real amplitudes, finite concatenations and declared control subspaces. Restricted timing/order/menu constraints need reachable-set argument; common partition operation has different warrants across fronts.')
claim('DR-08','Foundational joint already present','FND-033 already joins original-ground arguments, selective revalidation, retained-report revision and non-inferential recognition; reassessment preserves that inherited accomplishment and its empirical mapping boundary.','Inherited overlap established by source-bound reassessment','reassessment/foundational_interface/RESULT.md',[('FND-033','source_ownership','Direct achieved foundational application'),('ET-18','source_ownership','Selective source/dependency scope'),('ET-03','role_revision_interface','Retained report may change evidence role')],'33 inherited checks freshly replayed; no new metaphysical proof, primary authentication, numerical human-warrant model or Lean build. No grounds supplied for forcing a new Boolean demonstration.','Direct source-report comparison and inherited static controls')
claim('DR-09','Reconstructed finite-contract input repair','Separately received repaired implementation snapshots four one-shot boundaries; constructor repair enforces accepted validated-storage invariant, while three other changes harden unspecified input shapes.','Separately attributed reconstructed code successor candidate','reassessment/intake/INTEGRATION_SCOPE_NOTE.md',[('ET-09','implementation_refinement','Finite reference implementation, not theorem repair')],'30=26+4 distinct from 52→55 and unavailable R3/88. Quotient/sidecar require reusable partitions; mapping-key iteration order changes. Old source-bound dependencies and receipts remain unchanged.','Red/green regressions, 30-test suite, unchanged finite oracle and separately disclosed downstream compatibility probe')
claim('DR-10','Full archive custody restored','Newly supplied full archive verifies 11392 payload manifest entries and 9814 advertised copied paths, with 11391 of 11393 member hashes already held.','Custody improvement, no scientific discovery','reassessment/intake/DISCREPANCY_REPORT.md',[],'Earlier trimmed failure remains historical; only root manifest and members index are new member bytes; reported R3 remains unavailable. No new semantic reading credit.','Exact SHA/size/CRC and manifest comparison')
claim('DR-11','Additional Pro exact finite controls','Supplied independent-formula controls establish displayed Euler discrepancy, sharp TV fixture and finite audit covariance grid.','New finite validation artifact, inherited theorem scope','reassessment/intake/DISCREPANCY_REPORT.md',[('GEO-18','bounded_validation','No actual later integrator import')],'6561 combinations over 2187 configurations; normal mode only due bare assert; no universal proof or actual-integrator replay.','Normal Python exact-rational finite controls')
dump('reassessment/CLAIMS.json',{'schema':'t20-depth-reassessment-claims-v1','status':'Proposed current additive reader; owner acceptance pending','original_research_cutoff_utc':'2026-10-11T11:32:55Z','reassessment_date_utc':'2026-10-11','scope':'Separately dated T20 consolidation-depth work; T20 remains active under standing mandate; no T21 initiation or exhaustive connection certification.','claims':claims})
compiler=(V/'tools/build_consolidated_register.py').read_text().replace("TRACKS = {","TRACKS = {\n    'consolidation_depth_reassessment': 'reassessment/CLAIMS.json',")
compiler=compiler.replace("'meaning': 'Navigation over reconciled inherited research, not a new universal theorem catalogue or an adopted repository registry.',","'meaning': 'Navigation over inherited research and separately dated consolidation-depth reassessment; contribution class remains in each source-owned record.',\n        'post_cutoff_addendum': {'date_utc': '2026-10-11', 'phase': 'consolidation-depth reassessment', 'T21_started': False},")
write('tools/build_consolidated_register.py',compiler)
subprocess.run([sys.executable,'-B',str(P/'tools/build_consolidated_register.py')],check=True)
index=json.loads((V/'DEPENDENCY_INDEX.json').read_text())
for c in claims:
 for d in c['dependencies']:index['edges'].append({'claim':c['id'],'references':d['claim'],'relationship':d['relationship'],'justification':d['scope'],'owner_file':'reassessment/CLAIMS.json','reference_status':'local_claim' if d['claim']!='H-Continuation' else 'source_owner_in_reassessment_SOURCE_OWNERS'})
index['edge_count']=len(index['edges']);dump('DEPENDENCY_INDEX.json',index)
interfaces=json.loads((V/'CROSS_FRONT_INTERFACES.json').read_text())
interfaces['interfaces'] += [
 {'id':'CF-15','source_claims':['GEO-17','ET-23'],'target_claims':['DR-01','DR-03','DR-04'],'relationship':'distinct_structure_preserving_applications','statement':'Common refinement has gradient-integrability and tagged-instrument mechanisms; their hypotheses cannot be interchanged.','required_scope':'Exact metric/product domain versus complete positive instruments/closed convex stable families.'},
 {'id':'CF-16','source_claims':['MOM-01','ET-05'],'target_claims':['DR-05','DR-06','DR-07'],'relationship':'restricted_control_specialization','statement':'Restricted output-preserving records can be smaller; separate complete profiles may fail their composed operation family.','required_scope':'Full output, declared control repertoire, observable closure and continuous coordinate sidecar.'},
 {'id':'CF-17','source_claims':['FND-033','ET-18','ET-03'],'target_claims':['DR-08'],'relationship':'inherited_source_application_confirmed','statement':'The foundational correction joint was already achieved at its declared semantic/static-control level.','required_scope':'No invented empirical basing or numerical warrant premises.'}]
dump('CROSS_FRONT_INTERFACES.json',interfaces)
# Preserve old correction records, add implementation-bound current successor entry.
corr=json.loads((P/'CORRECTION_INDEX.json').read_text());corr['corrections'].append({'current_claim':'DR-09','record_file':'reassessment/CLAIMS.json','correction':{'predecessor_sha256':'3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06','successor_sha256':'852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0','status':'Reconstructed successor candidate, adoption pending; old historical replay stays exact','patch':'reassessment/contract_repair/EXACT_DIFF.patch','separate_from':'52→55 authorial DAG-helper repair and unavailable R3/88'}});dump('CORRECTION_INDEX.json',corr)

# Current reader amendments do not alter any old public scientific original.
write('EDITION_V3.md','''# Version 3: consolidation-depth reassessment\n\nOriginal T20 research cutoff remains **2026-10-11T11:32:55Z**. This edition adds separately dated **11 October 2026 consolidation-depth reassessment** and newly received historical input qualification. It is a complete current candidate built over delivered v2; Codex must not manually merge multiple editions or reread the corpus. V2 and its delivered ZIP remain preserved.\n\n## Material changes\n\n- New several-partition gradient refinement theorem and odds-ratio countercontrols.\n- Direct inherited ET-23 cone corollary, with reviewer contribution credited; conditional cone-gradient metric transport.\n- Restricted-control grouped-barycentre theorem, exact continuous augmentation minimum, and nine-state composition failure.\n- Source-level confirmation that FND-033 already achieved the foundational joint; preserved affirmative appraisals and exact empirical mapping boundary.\n- Separately attributed 30-test reconstructed finite-contract successor and bounded compatibility evidence, with historical old26 source/receipts intact.\n- Newly supplied complete archive custody seal, retaining earlier trimmed failure and unrecovered R3 status.\n\nRead [owner assessment](reassessment/OWNER_ASSESSMENT.md), [combined synthesis](reassessment/COMBINED_RESEARCH_SYNTHESIS.md), and [typed claims](reassessment/CLAIMS.json). Exact proofs, reviews, source-owner mappings and selected replay targets are included. The reported independent review is an independent assistant review at stated scope, not external human peer review.\n\nThis demonstrates consequential work remained after v2. It does not certify that every worthwhile connection is exhausted. Owner acceptance, Codex integration, repository adoption and T21 initiation are separate. **T20 remains active under the standing mandate while the owner reviews this proposed baseline. T21 has not started.** Unresolved current frontiers are not automatically reassigned outside T20.\n''')
for name,title in [('README_FIRST.md','Current edition'),('FIELD_GUIDE.md','Consolidation-depth update'),('MATHEMATICAL_SYNTHESIS.md','Separately dated new cross-front deductions'),('OWNER_REVIEW_CASE.md','Current owner-review status'),('FOUNDATIONAL_CROSSWALK.md','Source-bound depth reassessment')]:
 text=(V/name).read_text();first,rest=text.split('\n',1)
 lead='\n\n## '+title+'\n\nThis is the complete v3 candidate. Read [EDITION_V3](EDITION_V3.md), [owner assessment](reassessment/OWNER_ASSESSMENT.md), and [combined research synthesis](reassessment/COMBINED_RESEARCH_SYNTHESIS.md) first. Original cutoff 2026-10-11T11:32:55Z is retained; new science is separately dated 11 October 2026 consolidation-depth reassessment. T20 remains active under the standing mandate while owner review is pending; T21 has not begun. Earlier open-boundary and custody statements below describe the inherited edition and are qualified by this current update.\n'
 write(name,first+lead+rest)
# Replace two misleading inherited reader assertions, preserving historical edition source in v2.
p=P/'README_FIRST.md';t=p.read_text().replace('Later received historical inputs restore earlier custody without advancing that scientific cutoff. Consolidation reading, qualification, repairs and packaging have their own evidence.','Later received historical inputs restore earlier custody without advancing that scientific cutoff. The v3 mathematical deductions are separately dated post-cutoff consolidation-depth reassessment; they are not silently assigned to the old cutoff.').replace('The earlier 26-test synthesis, original 52-test authorial contribution, corrected 55-test implementation and unavailable reported R3/88 successor are kept separate.','The historical 26-test synthesis, new reconstructed 30-test successor candidate, original 52-test authorial contribution, corrected 55-test implementation and unavailable reported R3/88 successor are kept separate.');p.write_text(t)
charter=(V/'T21_CHARTER.md').read_text().replace("Routine research continues under the owner's applicable research mandate once the accepted continuation begins.","T20 remains active under the owner's standing research mandate while the owner reviews this proposed baseline. T21 is proposed and has not started. Unresolved current frontiers are not automatically assigned out of T20; baseline acceptance and a named next tranche are separate decisions.")
write('T21_CHARTER.md',charter)
for rel,text in [('geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','The inherited statement that overlapping partition families remain unclassified is now resolved within the precise retained metric/product-domain contract by DR-01. Restricted groups/metrics outside it remain open. DR-05–07 compute a restricted-control quotient and its composed-control boundary.'),('evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md','DR-03 is a direct tagged-instrument application of ET-23, not a new general cone theorem. DR-09 carries the separate reconstructed finite-contract code successor; the historical old26 and authorial 52→55 lines remain distinct.'),('foundations/FOUNDATIONAL_SYNTHESIS.md','DR-08 establishes that the requested foundational correction interface was already substantially present in FND-033. Its 33 source-bound controls are freshly replayable; no new psychological warrant model or metaphysical proof is claimed.')]:
 t=(V/rel).read_text();first,rest=t.split('\n',1);write(rel,first+'\n\n## Current v3 qualification\n\n'+text+' See [separately dated reassessment](../EDITION_V3.md).\n'+rest)
# Installer and pins remain byte-identical; extend only bounded mechanical instructions.
codex=(V/'CODEX_START_HERE.md').read_text().replace('The bounded [version 2 scope](EDITION_V2.md) adds ET-23 and supersedes the undelivered first local candidate.','The current [version 3 scope](EDITION_V3.md) includes v2 in full plus separately dated consolidation-depth reassessment. Use this single candidate; do not integrate v2 and v3 separately. No new research task, corpus rereading, universal proof re-certification or T21 initiation is requested.')
codex=codex.replace('The four claim records control hypotheses, evidence and remaining obligations.','The four inherited track records and reassessment/CLAIMS.json control hypotheses, contribution classes, evidence and remaining obligations.')
codex=codex.replace('    python -B replay_selected.py --suite finite-contracts','    python -B replay_selected.py --suite finite-contracts\n    python -B replay_selected.py --suite finite-contracts-reconstructed\n    python -B replay_selected.py --suite audit-refinement\n    python -B replay_selected.py --suite restricted-controls\n    python -B replay_selected.py --suite depth-independent\n    python -B replay_selected.py --suite foundational-scope\n    python -B replay_selected.py --suite pro-exact-controls')
codex=codex.replace('REPLAY_SCOPE separates five package-local finite controls from source-preserved historical suites.','REPLAY_SCOPE separates five inherited package-local controls and six selected reassessment controls from source-preserved historical suites. For the unchanged v2 suites, reuse their exact source-bound receipts; only the old26 baseline and the six delta targets above need selected replay for this edition. Do not rerun every preserved proof family merely to integrate the reader. The reconstructed successor is not substituted into rational-hase-j; its compatibility probe is separate, explicitly qualified evidence. Review mapping iteration order and accepted input shapes in reassessment/contract_repair/REVIEW.md before choosing it in any new caller.')
write('CODEX_START_HERE.md',codex)
projection['files']=sorted(rows,key=lambda r:(r.get('public_path','~'+r.get('repository_path','')),r['original_sha256']))
projection['post_cutoff_addendum']={'date_utc':'2026-10-11','phase':'consolidation-depth reassessment','owner_acceptance':'pending','T21_started':False,'historical_cutoff_unchanged':True}
dump('PUBLIC_PROJECTION.json',projection)
oldtrans=json.loads((V/'PUBLIC_TRANSFORMATIONS.json').read_text());oldtrans['reassessment_records']=transforms;dump('PUBLIC_TRANSFORMATIONS.json',oldtrans)
# Preserve prior source entries and append exact new/additional owners.
write('SOURCE_INDEX.md',(V/'SOURCE_INDEX.md').read_text()+'\n## Separately dated consolidation-depth reassessment\n\nSelected inherited source bodies remain in place. See [portable source owners](reassessment/SOURCE_OWNERS.json) for new report-specific inspection scopes.\n\n'+'\n'.join('- '+', '.join(x['source_id'] for x in r['owners'] if x['track']=='consolidation-depth-reassessment')+': ['+r['original_sha256'][:12]+']('+r.get('public_path',r.get('public_url',''))+')' for r in rows if any(x['track']=='consolidation-depth-reassessment' for x in r['owners']))+'\n')
print('V3 initial assembly ready; review receipt and seal pending')

# Final independently reviewed reconstructed-code qualification.
add(D/'contract_repair_review/REVIEW.md','reassessment/contract_repair/REVIEW.md','independent-reconstructed-code-qualification')
results=json.loads((D/'contract_repair_review/RESULTS.json').read_text())
for run in results.get('runs',[]):
 if run.get('command') and run['command'][0].startswith('/'):run['command'][0]='python'
results['projection_note']='Executable paths normalized to python; exact original receipt digest retained by PUBLIC_PROJECTION. Original review used isolated local layouts, not the preserved old source-bound family.'
add(D/'contract_repair_review/RESULTS.json','reassessment/contract_repair/RESULTS.json','independent-reconstructed-code-results','AMENDED',json.dumps(results,indent=2)+'\n')
cb=[]
for path,h in json.loads((D/'contract_repair_review/INPUT_BINDINGS.json').read_text()).items():
 cb.append(binding({'path':path,'sha256':h,'bytes':(W/path).stat().st_size}))
dump('reassessment/contract_repair/SOURCE_BINDINGS.json',{'sources':cb,'scope':'Original reviewer input identities mapped to selected public owner bytes when included; historical receipt/preflight context is not a new whole-family replay promise.'})
status={'status':'SCOPED_INDEPENDENT_REVIEW_RECOMMENDS_ADDITIVE_SUCCESSOR; OWNER_ADOPTION_PENDING','predecessor':'replay/finite-contracts/contracts.py','predecessor_sha256':'3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06','successor':'replay/finite-contracts-reconstructed/contracts.py','successor_sha256':'852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0','tests':'26 inherited + 4 reconstructed = 30; distinct from authorial 52→55 and unavailable R3/88','four_accepted_boundaries':['finite transition-row triple iterables','finite partition/block iterables for valid_partition only','finite hashable reachability-target iterables','finite action family with finite matrix/row iterables in closure_basis'],'remaining_input_limits':['quotient and sidecar need reusable indexable partition containers AND blocks','closure_basis output rows still require sequences','Contract enabled-action menus need reusable sized containers','finite stable values only, no infinite/effectful/shared-exhausted iterator promise'],'python_observable_limits':['Kernel mapping key iteration order can change through enabled-pair set iteration and hash randomization','Per-key rows/values and within-row order, not complete insertion-order/exception/consumption-timing equivalence','Canonicalize serialization order or obtain a separately reviewed order-preserving successor if callers depend on it'],'downstream':results['downstream'],'historical_source_bound_dependency_unchanged':True,'no_Lean_rebuild':True,'review':'reassessment/contract_repair/REVIEW.md','reviewer_results':'reassessment/contract_repair/RESULTS.json'}
dump('reassessment/intake/CONTRACT_REPAIR_STATUS.json',status)
# Exact downstream import layout; separate from the immutable source-bound family.
for src in sorted((D/'contract_repair_review/downstream').rglob('*')):
 if src.is_file() and src.suffix in ('.py','.json'):
  add(src,'replay/contract-downstream/'+src.relative_to(D/'contract_repair_review/downstream').as_posix(),'rational-caller-disclosed-substitution')
write('replay/contract-downstream/run_probe.py','''"""New portable comparison; never rebinds or executes the historical whole verifier."""\nfrom pathlib import Path\nimport hashlib,json,os,subprocess,sys\nROOT=Path(__file__).resolve().parent\nOLD='3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06'\nNEW='852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0'\nDEP='received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py'\ndef require(ok,message):\n if not ok:raise RuntimeError(message)\noutputs=[];runs=[]\nfor flavor,expected in [('old',OLD),('repaired',NEW)]:\n actual=hashlib.sha256((ROOT/flavor/DEP).read_bytes()).hexdigest()\n require(actual==expected,'unexpected dependency bytes')\n historical_preflight=(actual==OLD)\n require(historical_preflight==(flavor=='old'),'historical pin boundary lost')\n for flags in [[],['-O']]:\n  p=subprocess.run([sys.executable,*flags,'-B','test_transport.py'],cwd=ROOT/flavor/'hase-rational-kernel-transport-20261011',capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'))\n  require(p.returncode==0,p.stderr)\n  result=json.loads(p.stdout);require(result['count']==162 and result['exhaustive_rows']==125 and result['status']=='PASS','caller scope changed')\n  digest=hashlib.sha256(p.stdout.encode()).hexdigest();outputs.append(digest)\n  runs.append({'dependency':flavor,'optimized':bool(flags),'checks':162,'finite_rows':125,'stdout_sha256':digest,'historical_dependency_pin_accepts':historical_preflight})\nrequire(len(set(outputs))==1,'caller outputs differ')\nprint(json.dumps({'status':'PASS','runs':runs,'scope':'Exact exercised rational Python caller, disclosed substitution only; original pin refuses repaired bytes; not full Python-observable equivalence or historical 3097-pin/Lean verifier.'},indent=2))\n''')
new_suites['contract-downstream']={'directory':'contract-downstream','commands':[['-B','run_probe.py']],'dependencies':[],'scope':'New explicit old/repaired Python dependency comparison; 162 checks/125 rows in both modes with byte-identical caller outputs, original single dependency pin rejects new bytes. No historical rebind, whole 3097-pin verifier, Lean build or all Python-observable equivalence.'}
runner=(V/'replay_selected.py').read_text().replace('\n\ndef main():','\n\n# Separately dated consolidation-depth reassessment targets.\nSUITES.update('+repr(new_suites)+')\n\ndef main():');write('replay_selected.py',runner)
scope['suites'].update(new_suites);dump('REPLAY_SCOPE.json',scope)
p=P/'CODEX_START_HERE.md';t=p.read_text().replace('six selected reassessment controls','seven selected reassessment controls').replace('six delta targets','seven delta targets').replace('    python -B replay_selected.py --suite pro-exact-controls','    python -B replay_selected.py --suite pro-exact-controls\n    python -B replay_selected.py --suite contract-downstream');p.write_text(t)
# Explicit intermediate checkpoint status under the latest owner mandate.
for rel in ['EDITION_V3.md','README_FIRST.md','CODEX_START_HERE.md','OWNER_REVIEW_CASE.md']:
 p=P/rel;t=p.read_text();first,rest=t.split('\n',1);p.write_text(first+'\n\n**INTERMEDIATE_REASSESSMENT_CHECKPOINT · T20 ACTIVE · owner acceptance pending.** Broader cross-front investigation continues under the owner’s standing mandate. This frozen candidate is a bounded working checkpoint, not final scientific closure or completion of that broader request. The prepared Codex handoff does not authorize application or a PR.\n'+rest)
projection['status']='INTERMEDIATE_REASSESSMENT_CHECKPOINT_T20_ACTIVE_OWNER_ACCEPTANCE_PENDING'
projection['files']=sorted(rows,key=lambda r:(r.get('public_path','~'+r.get('repository_path','')),r['original_sha256']))
dump('PUBLIC_PROJECTION.json',projection)
oldtrans['reassessment_records']=transforms;dump('PUBLIC_TRANSFORMATIONS.json',oldtrans)
write('SOURCE_INDEX.md',(P/'SOURCE_INDEX.md').read_text()+'\n## Reconstructed-code independent qualification\n\n- [Code review](reassessment/contract_repair/REVIEW.md) and [bounded input/ordering status](reassessment/intake/CONTRACT_REPAIR_STATUS.json)\n- [Source identities](reassessment/contract_repair/SOURCE_BINDINGS.json); exact downstream copies are separate from the retained historical family.\n')
# Derived-reader/source changes are explicitly inventoried; old v2 scientific files retain bytes.
reader=json.loads((V/'READER_PROJECTION.json').read_text())
reader['v3_scope']='Intermediate checkpoint; current reader amendments and new source-bound reassessment. Original v2 scientific source copies are unchanged.'
reader['v3_reader_files']=[]
for rel in ['README_FIRST.md','FIELD_GUIDE.md','MATHEMATICAL_SYNTHESIS.md','OWNER_REVIEW_CASE.md','FOUNDATIONAL_CROSSWALK.md','T21_CHARTER.md','CODEX_START_HERE.md','geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md','foundations/FOUNDATIONAL_SYNTHESIS.md','tools/build_consolidated_register.py']:
 a=(V/rel).read_bytes();b=(P/rel).read_bytes();reader['v3_reader_files'].append({'path':rel,'v2_sha256':sha(a),'v3_sha256':sha(b),'scope':'Current authored reader/navigation amendment, not alteration of an original scientific source.'})
dump('READER_PROJECTION.json',reader)
# Correct callable SOURCE_BINDINGS targets with public code now materialized.
p=P/'reassessment/independent_review/PORTABLE_REVIEW_BINDINGS.json';d=json.loads(p.read_text())
for r in d['targets']:
 raw=(P/r['public_target']).read_bytes();r['public_sha256']=sha(raw);r['public_bytes']=len(raw);r['projection']='EXACT' if sha(raw)==r['original_sha256'] else 'AMENDED'
dump('reassessment/independent_review/PORTABLE_REVIEW_BINDINGS.json',d)
# Add explicit source text for original finite input contract if not previously mirrored.
doc=W/'t20-consolidation-20261011/catalogue/archive-views/Orthemology_T20_Whole_Corpus_Synthesis_20261010_1_.zip--38ed92bbec08/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/REPRODUCE.md'
if doc.exists():add(doc,'reassessment/contract_repair/ORIGINAL_REPRODUCE.md','Pro-old26-original-contract-documentation')
projection['files']=sorted(rows,key=lambda r:(r.get('public_path','~'+r.get('repository_path','')),r['original_sha256']));dump('PUBLIC_PROJECTION.json',projection)
# Reusable source-safe package manifest (re-finalized after execution receipts).
files=[]
for path in sorted(P.rglob('*')):
 if path.is_symlink():raise RuntimeError('symlink')
 if path.is_file() and path.name!='PACKAGE_CONTENTS.json':
  raw=path.read_bytes();files.append({'path':path.relative_to(P).as_posix(),'sha256':sha(raw),'bytes':len(raw)})
dump('PACKAGE_CONTENTS.json',{'schema':'t20-consolidated-package-contents-v1','scope':'Intermediate checkpoint integrity; not scientific closure. Manifest excludes itself; checkpoint seal binds it.','files':files})
print('Intermediate candidate assembled:',len(files)+1,'files')
