from pathlib import Path
import hashlib,json,shutil,datetime,re,yaml
root=Path('private-locator:1dc82187dd31bb556614');inp=Path('private-locator:4c8bc74717a70d6fa8d2')
sha=lambda b:hashlib.sha256(b).hexdigest()
def row(p,base):
 b=p.read_bytes();return {'path':str(p.relative_to(base)),'bytes':len(b),'sha256':sha(b)}
def dump(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
obs=json.loads((inp/'OBLIGATIONS.json').read_text());inv=json.loads((inp/'SOURCE_INVENTORY.json').read_text());byrepo={r['repository_path']:r for r in inv}
notes={'U05':'U05_MEASURE_SEMANTICS.md','U08':'U08_CORRESPONDENCE.md','CV-R':'CV_R_REFINEMENT.md','CV-C':'CV_C_COMPUTABILITY.md','Q1c':'Q1c_FINITE_PROBABILITY.md'}
hyp={
'U05':['Probability measure; measurable singletons; measurable maps for pushforwards; only positive-mass fibres normalised.','Arbitrary conjunction probabilities require measurable intersections, or a separately named measurable-conull-subset interpretation.','Necessity/attainment uses the rich singleton-complement repertoire; countable or restricted repertoires are distinct.','Mixture index is countable and weights nonnegative with sum one; weak limits use the explicitly specified Borel [0,1] examples.','Q8 is a separate total synchronous bounded-simulation observer reduction.'],
'U08':['Proposed restricted family: finite nonempty simplex; fixed nonempty compact convex row sets; finite outcome labels in a measurable-singleton space.','Compactness and continuity are proved for this proposed envelope, not assumed for all safe measures.','Effectivity additionally requires exact rational polytope row descriptions and their nonemptiness.','Unrestricted noncomputable real parameters are outside the finite-description oracle-free sampler contract.','Typing of outcome labels, if claimed, is an explicit accepted-premise wrapper and is not inferred.'],
'CV-R':['Probability space; countable coherent measurable observations with measurable singleton carriers and measurable coarsening.','Almost-everywhere coherence is interpreted on a common conull set; product observation is measurable.','Positive-cell extinction J is retained; no reversal of epsilon and stage limits.','Certificate necessity uses the separately stated rich-event premise; no artifact/epoch validity follows from a probability bound.'],
'CV-C':['Fixed effective, syntactically total PR synchronous observer presentation with invalid codes assigned zero.','Exact dyadic cylinder probabilities; positive rational gap in strict threshold formula; specified limit order.','Uniform PR construction/parameter substitution for hardness; new byte-level codec is unimplemented and unadopted.','Threshold table has fixed rational 0<q<1 and separately stated endpoints.','Finite Mealy states, binary fair independent inputs, total binary transitions; no inference to arbitrary PR observers.'],
'Q1c':['n>=3 for all pairwise marginals to be proper; proper coordinate subset in the general counting formula.','Normalised nonnegative finite weights; declared even-parity probability-one target.','Deterministic coordinate flip for restoration; separately specified fair mixture kernel for profile movement.','Q0 remains accepted only at supplied scope; downstream wrapper use is not a pure prerequisite.','Three-bit Lean candidate is not the all-n theorem and not historical declaration recovery.']}
remaining={
'U05':['No new exact-pin compilation, declaration/type or transitive-axiom readback.','Full support-sum, rich-event equivalence, restriction/map, countable mixture, weak-limit and Q8 Lean proofs remain.'],
'U08':['Compatible pinned Kakutani fixed-point declaration/development not identified.','Proposed domain requires separate review; general formal obligation not closed by restricted row-set family.','Flow/sampler formalisation and implementation not executed.'],
'CV-R':['U05 measure dependencies not kernel-checked in this run.','Full CV-R Lean development, including J and exact certificate transport, absent.','Optional martingale convergence requires a further exact-pin theorem mapping.'],
'CV-C':['Exact byte-level PR codec and uniform compiler unimplemented; semantic proposal not adopted.','Cylinder/soft-mass and arithmetical hierarchy/reduction formal proofs absent.','Finite Mealy theorem and Python-to-formal refinement remain ordinary/unverified.'],
'Q1c':['Eleven combined candidate theorem targets across two files are all unexecuted; seven concern n=3 T300.','General all-n PMF/counting/kernel bridge not implemented in Lean.','No historical missing declarations or original mixture payload recovered.']}
ids={'U05':['P02-M01','P02-M02','P02-M03','P02-M04','P02-M05','P02-M06'],'U08':['P02-F01','P02-F02','P02-F03','P02-F04'],'CV-R':['P02-R01','P02-R02','P02-R03','P02-R04','P02-R05','P02-R06','P02-R07'],'CV-C':['P02-C-SYNTAX-01','P02-C01','P02-C02','P02-C03','P02-C04'],'Q1c':['P02-QC01','P02-QC02']}
sel=[];results=[]
for o in obs:
 f=inp/'source-main'/o['source_locator'];d=yaml.safe_load(f.read_text()) if f.suffix in ['.yaml','.yml'] else json.loads(f.read_text())
 key=o['source_selector'].split('[')[0];r=next(x for x in d[key] if x['id']==o['id'])
 assert r==o['exact_source_record']
 s={'id':o['id'],'selector':o['source_selector'],'source':row(f,inp),'exact_record_equal':True};sel.append(s)
 extra=[]
 if o['id']=='Q1c':
  rp='docs/project-closure/ar8r-v11/theorems/ar8r-t300-lower-order-alignment-blind-restoration.md';extra=[byrepo[rp]]
 results.append({'id':o['id'],'obligation_status':'PARTIAL','canonical_status_unchanged':o['current_status'],'original_obligation':o,'selector_verification':s,'additional_input_bindings':extra,'hypotheses':hyp[o['id']],'output_statement_ids':ids[o['id']],'statement_and_proof_file':row(root/'analysis'/notes[o['id']],root),'ordinary_research_status':'SUPPLIED_FOR_REVIEW_NOT_KERNEL','formal_status':'UNVERIFIED_NO_RUNTIME','completion_criteria_assessment':'Scoped research/proposal work supplied; broader formal obligation remains open. No acceptance criterion weakened.','remaining':remaining[o['id']],'kernel_credit':False,'source_status_change':False,'external_review_credit':False,'historical_recovery_credit':False})
dump(root/'OBLIGATION_RESULTS.json',{'schema':'orthemology-p02-obligation-results-v1','results':results,'other_packets_assumed_passed':[]})
dump(root/'evidence/SELECTOR_VERIFICATION.json',{'status':'PASS','records':sel,'checked':5})
# Preserve exact packet bytes and all extracted source/evidence, not reconstructed histories.
shutil.copytree(inp,root/'inputs/packet',dirs_exist_ok=True)
shutil.copy2('private-locator:a516cf88ef66ba04ead5',root/'inputs/Orthemology_Pro_P02_Measure_CV_R_C.zip')
checks=[]
for f in inp.rglob('*'):
 if f.is_file():checks.append({'path':str(f.relative_to(inp)),'unchanged':f.read_bytes()==(root/'inputs/packet'/f.relative_to(inp)).read_bytes(),'sha256':sha(f.read_bytes())})
dump(root/'evidence/INPUT_COPY_READBACK.json',{'status':'PASS' if all(x['unchanged'] for x in checks) else 'FAIL','copied_files':len(checks),'checks':checks,'native_checkout_claimed':False,'full_main_tree_recomputed':False})
control=[row(p,inp) for p in sorted(inp.iterdir()) if p.is_file()]
dump(root/'provenance/INPUT_IDENTITIES.json',{'original_archive':row(root/'inputs/Orthemology_Pro_P02_Measure_CV_R_C.zip',root),'control_files':control,'source_files':539,'accepted_projection_bindings':54,'canonical_identity_source':'Inherited accepted packet, not fresh live GitHub or native full-tree verification','main_commit':'03e2604dfcef278b01c60d19b05370fcec4194b6','main_tree':'3d06e80277ce39286c94307e0f14b215bc94ed83','PR':28,'integration_cells_remaining':0})
negative=[
('N01','PRESERVED_ORIGINAL_STRICT_FAIL','inputs/packet/accepted-evidence/A8R/cells/A8R/ORIGINAL_PACKET_REPLAY.json','Original strict wrapper exit 1 and BoundaryResults compilation FAIL remain genuine failure, separate from accepted mapped-native qualification.'),
('N02','PRESERVED_LOGICAL_VS_MEASURE','analysis/U05_MEASURE_SEMANTICS.md','Abstract Full compilation is not an actual measure-theory instantiation.'),
('N03','PRESERVED_RICHNESS_MEASURABILITY','analysis/U05_MEASURE_SEMANTICS.md','Atomless null-singleton complements defeat rich arbitrary conjunction closure; countable repertoire behaves differently.'),
('N04','PRESERVED_INFINITE_RESIDUAL','analysis/CV_R_REFINEMENT.md','Finite telescoping does not charge J; mixed witness has finite debt 1/3 and residual 5/12.'),
('N05','PRESERVED_MODEL_AND_THRESHOLD','analysis/CV_C_COMPUTABILITY.md','Partial/arbitrary observers, swapped limits, or changing strict thresholds defeat the stated classifier.'),
('N06','PRESERVED_SAFE_DOMAIN_OBSTRUCTION','analysis/U08_CORRESPONDENCE.md','Unrestricted defect-safe sets are not weakly closed; existence does not give general iteration or an exact sampler.'),
('N07','PRESERVED_HISTORICAL_CUSTODY','analysis/Q1c_FINITE_PROBABILITY.md','Exact T300 target present; old payload identities are not recovered from a new witness. Absent historical declarations remain absent.'),
('N08','CURRENT_RUNTIME_BLOCK','evidence/ENVIRONMENT.json','No Lean/Lake/Elan available; failed runtime DNS acquisition is distinct from historical strict-wrapper FAIL.'),
('N09','PRESERVED_VERSION_AND_SCOPE','inputs/packet/FORMAL_TOOLCHAIN_STATE.json','Existing 4.32.2 and mapped 4.19.0 results do not substitute for these new targets.'),
('N10','NEW_PROPOSALS_NOT_ADOPTED','provenance/PATCH_MAPPING.json','Finite safe envelope, PR codec, measure interface, mixed example and explicit T300 mixture remain proposals.'),
('N11','NO_NOVELTY_OR_EXTERNAL_CREDIT','analysis/LITERATURE_COMPARISON.md','Limited primary-source comparison does not establish priority, expert review, empirical authority, owner adoption or licensing.'),
]
dump(root/'NEGATIVE_FINDINGS.json',{'findings':[{'id':a,'status':b,'evidence':c,'finding':d} for a,b,c,d in negative],'new_refutation_of_exact_accepted_theorem_claimed':False,'source_diagnoses_relabelled':False})
deps=[
{'id':'DEP-LEAN419','status':'BLOCKED_CURRENT_RUNTIME','affects':['U05','U08','CV-R','CV-C','Q1c'],'requirement':'Actual Lean4.19.0/Lake/mathlib-pin execution with nonempty artifacts and complete type/axiom readbacks.','evidence':['evidence/ENVIRONMENT.json','evidence/ACQUISITION_PROBE.json']},
{'id':'DEP-KAKUTANI-PIN','status':'NOT_IDENTIFIED_NOT_PROVEN_ABSENT','affects':['U08'],'requirement':'An exact-pin compatible fixed-point development or a separately reviewed formal proof of the restricted family.'},
{'id':'DEP-PR-CODEC','status':'UNIMPLEMENTED_UNADOPTED_DEFINITION','affects':['CV-C'],'requirement':'Freeze byte-level codec, total parser, PR semantics and uniform reduction compiler; no historical numbering identity inferred.'},
{'id':'DEP-U05-MEASURE','status':'ORDINARY_PREMISES_ONLY','affects':['CV-R','CV-C'],'requirement':'New formal consumers must use checked U05 dependencies; present proofs are ordinary, not kernel imports.'},
{'id':'DEP-Q0-SCOPE','status':'INCLUDED_SCOPED_ACCEPTANCE_ONLY','affects':['Q1c'],'requirement':'Preserve Q0 and specialist guards/observation/indices; no blanket queue advance or missing historical recovery.'},
{'id':'DEP-OWNER','status':'NOT_REQUESTED_NOT_GRANTED','affects':['U05','U08','CV-R','CV-C','Q1c'],'requirement':'Separate authority for adoption, canonical source/index/manifest changes, licensing, external review, publication or empirical claims.'},
{'id':'DEP-HISTORICAL-WHOLE-PACKETS','status':'NOT_INCLUDED_NO_RECOVERY_CLAIM','affects':['Q1c'],'requirement':'Original whole checkpoint payloads and absent historical declarations remain outside supplied custody; not necessary to state the public T300 target.'},
]
dag=json.loads((inp/'DEPENDENCY_DAG.json').read_text())
dump(root/'UNRESOLVED_DEPENDENCIES.json',{'dependencies':deps,'relevant_dag_edges':[e for e in dag['edges'] if e['source'] in notes or e['target'] in notes],'other_packet_new_results_consumed':[],'new_cross_packet_edges_adopted':[]})
patch=[]
for o in obs:
 patch.append({'obligation':o['id'],'action':'ADD_SEPARATE_PROPOSAL_ONLY','canonical_preimages':o['source_bindings'],'source_locator_preimage':sel[[x['id'] for x in sel].index(o['id'])]['source'],'proposed_statement_ids':ids[o['id']],'proposal_note':'analysis/'+notes[o['id']],'canonical_patch_applied':False,'source_status_change_proposed_for_automatic_adoption':False,'later_review':'Reject, revise or accept at exact scope; do not replace historical evidence or general targets with concrete candidates.'})
dump(root/'provenance/PATCH_MAPPING.json',{'mapping':patch,'new_definitions_separately_reviewable':['P02 actual-measure interface, not logical Full replacement','P02-F01 finite-support row-set envelope, not all safe measures','P02-C-SYNTAX-01 PR codec/numbering proposal, not historical indices','P02-R06 mixed refinement witness','P02-QC02 explicit 1/2 parity/Dirac mixture witness'],'new_theorem_premises':['Fixed finite carrier and compact convex row sets for F01','Exact rational polytope descriptions for F03','Effective PR syntax and parameter substitution, with byte codec pending','Optional typing of outcome labels only from included accepted premises'],'canonical_deletions':[],'canonical_edits':[]})
# Candidate declaration inventory is static source evidence, not Lean elaboration.
leanfiles=list((root/'proposals/lean/P02').glob('*.lean'))
names=[]
for f in leanfiles:
 for m in re.finditer(r'^theorem\s+(\w+)',f.read_text(),re.M):names.append({'file':str(f.relative_to(root)),'short_name':m.group(1)})
assert len(names)==11
static={'status':'STATIC_SOURCE_INVENTORY_ONLY','targets':names,'target_count':11,'checked_target_count':0,'lean_executed':False,'declaration_types_observed':False,'axiom_readbacks_observed':False,'nonempty_olean_artifacts':0,'forbidden_placeholder_tokens_in_candidate_modules':{str(f.relative_to(root)):bool(re.search(r'\b(sorry|admit|axiom|sorryAx)\b',f.read_text())) for f in leanfiles},'not_an_axiom_audit':True}
dump(root/'evidence/LEAN_CANDIDATE_STATIC_INVENTORY.json',static)
# Self-reference is avoided: the later verifier checks these source files before copying.
dump(root/'provenance/PROPOSAL_IDENTITIES.json',{'files':[row(p,root) for p in sorted((root/'proposals').rglob('*')) if p.is_file()],'status':'UNADOPTED_PROPOSAL_BYTES'})
print('metadata written; source selectors and all 620 copied input files verified; 11 unexecuted Lean theorem targets')
