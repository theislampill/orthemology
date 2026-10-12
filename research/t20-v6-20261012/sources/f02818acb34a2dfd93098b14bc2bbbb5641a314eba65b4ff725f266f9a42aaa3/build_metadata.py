"""Bind exact research text and evidence without granting canonical/kernel credit."""
from pathlib import Path
import hashlib,json,re,datetime
R=Path(__file__).resolve().parents[1];P=R.parent/'p02_predecessor'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):
 p=R/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def ident(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b)}
obs=json.loads((R/'provenance/ORIGINAL_OBLIGATIONS.json').read_text())
inv=json.loads((R/'provenance/FORMAL_INVENTORY.json').read_text())
old=json.loads((P/'OBLIGATION_RESULTS.json').read_text())['results']
# Original exact statement families and their evidence dimensions.
primary={
 'P02-M01':'proved by ordinary mathematics','P02-M02':'proved by ordinary mathematics','P02-M03':'proved by ordinary mathematics','P02-M04':'proved by ordinary mathematics','P02-M05':'counterexample/refutation','P02-M06':'proved by ordinary mathematics',
 'P02-F01':'proposed theorem/model','P02-F02':'proposed theorem/model','P02-F03':'proved by ordinary mathematics','P02-F04':'counterexample/refutation',
 'P02-R01':'proved by ordinary mathematics','P02-R02':'proved by ordinary mathematics','P02-R03':'proved by ordinary mathematics','P02-R04':'proved by ordinary mathematics','P02-R05':'proved by ordinary mathematics','P02-R06':'counterexample/refutation','P02-R07':'proved by ordinary mathematics',
 'P02-C-SYNTAX-01':'implementation not yet built','P02-C01':'proved by ordinary mathematics','P02-C02':'proposed theorem/model','P02-C03':'proposed theorem/model','P02-C04':'proved by ordinary mathematics',
 'P02-QC01':'proved by ordinary mathematics','P02-QC02':'proved by ordinary mathematics'}
rows=[]
for o in old:
 for id in o['output_statement_ids']:
  rows.append({'id':id,'obligation':o['id'],'primary_classification':primary[id],
    'ordinary_proof_scope':'See unchanged predecessor statement_and_proof_file, including effective-numbering hypotheses where present.',
    'source_file_inside_predecessor':o['statement_and_proof_file'],
    'source_file_sha256':sha((P/o['statement_and_proof_file']['path']).read_bytes()),
    'kernel_verified_in_attempt1':False,'repeated_census_or_proof_for_ceremony':False,
    'attempt2_action':'Retained as premise; strengthened/newly implemented only under separately identified result IDs.'})
extras=[
 {'id':'A1-F03-ALGORITHM','primary_classification':'implementation not yet built','component':'Exact rational vertex enumeration; built in attempt2 code/flow_solver.py'},
 {'id':'A1-C03-CODEC-COMPILER','primary_classification':'implementation not yet built','component':'Uniform symbolic reductions lacked concrete bytes; P02-L1 is a new explicit representation, not recovered indices'},
 {'id':'A1-FINITE-CENSUSES','primary_classification':'finitely executed only','component':'46,656 Mealy machines; 139,968 state checks; 498 proper marginal equalities; 9,324 cells; 83 pairs; retained without replay'},
 {'id':'A1-LEAN-11','primary_classification':'unverified Lean source','component':'Four MeasureCore and seven T300ThreeBit source candidates retained byte-for-byte; zero new execution'},
 {'id':'A1-HISTORICAL-DECLARATION-CUSTODY','primary_classification':'genuinely external dependency','component':'Absent historical declarations/weights/immutable locators are not recovered by new mathematics'},
 {'id':'A1-OWNER-ADOPTION','primary_classification':'genuinely external dependency','component':'Canonical adoption is a later authorised act, not a mathematical premise'},
 {'id':'A1-TOOLCHAIN','primary_classification':'genuinely external dependency','component':'Old host absence was historical; attempt2 separately probes actual local/network/library routes. New source completeness is a different question.'}]
save('provenance/PREDECESSOR_CLASSIFICATION.json',{'families':rows,'component_results':extras,'named_family_count':len(rows),
 'original_strict_wrapper':'GENUINE_FAIL_PRESERVED','mapped_native_formal':'ACCEPTED_INPUT_SCOPE_NOT_NEW_P02_KERNEL_EVIDENCE'})
# Complete exact source text per research section.
family={ 'M2':'U05','F2':'U08','R2':'CV-R','C2':'CV-C','Q2':'Q1c' }
common={
 'U05':'Probability (or explicitly finite measure at stronger lemma scope), measurable singletons; measurable maps/events; active positive-weight fibres; countable mixtures. Topological/effective hypotheses are separately stated in each section.',
 'U08':'Actual specified domain and row correspondence; nonempty rows. Compactness/convexity/topology are proved for each permitted envelope, not assumed for the all-safe-law set. Rational effectivity requires exact finite rational row constraints.',
 'CV-R':'Probability space; countable measurable observations with measurable singletons and declared coarsening/coherence; common-null interpretation only as separately stated. Full-event necessity additionally requires richness. J retained.',
 'CV-C':'P02-L1 total PR synchronous prefix observers, effective numeric coding, fair Cantor input. Invalid syntax is zero; resource exhaustion is not a semantic answer. Matrices compiled with declared arity; thresholds exact rationals.',
 'Q1c':'Finite normalised nonnegative laws; n≥1 for parity; genuinely proper coordinate subsets; n≥3 for pairwise T300; declared target and intervention; 0<α≤1 for moving nonempty marginals.'}
cat=[]
for p in sorted((R/'proofs').glob('*.md')):
 text=p.read_text();matches=list(re.finditer(r'^## ([MFRQC]2-\d+)\. (.*)$',text,re.M))
 for i,m in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else len(text)
  section=text[m.start():end];id=m.group(1);ob=family[id.split('-')[0]]
  cat.append({'id':id,'obligation':ob,'title':m.group(2),'proof_file':str(p.relative_to(R)),
   'proof_file_sha256':sha(p.read_bytes()),'source_start_line':text.count('\n',0,m.start())+1,
   'source_end_line':text.count('\n',0,end)+1,'exact_section':section,'section_sha256':sha(section.encode()),
   'common_hypotheses':common[ob],'mathematical_status':'ORDINARY_PROOF_OR_EXACT_DEFINITION_SUPPLIED_AS_STATED',
   'kernel_verified':False,'canonical_adoption':False,'novelty':'UNCLAIMED'})
save('NEW_RESULT_CATALOGUE.json',{'result_sections':cat,'count':len(cat),'not_a_count_of_kernel_theorems':True})
# Exact pin and source coverage, with missing bridges stated rather than concealed.
coverage={
 'U05':{'modules':['P02A2.MeasureCore','P02A2.Mixture','P02A2.Fibres','P02A2.FiniteMeasureBridge'],
   'covered':'Actual positive-singleton support/countability/measurability; rich lower bound; normalized fibre and weighted defect identities; countable mixture core; finite-law interpretation.',
   'ordinary_only_or_missing_source':['Weak-limit measure instances and their convergence/counterexample Lean proofs','Complete Q8 bounded-machine-code to fair-Cantor-measure/undecidability Lean bridge','Standard-Borel measurable-atom identification and total-variation continuity strengthening']},
 'U08':{'modules':['P02A2.Stationary','P02A2.SimplexStationary','P02A2.Flow'],
   'covered':'Constructed Cesàro approximate fixed points for a compact convex invariant linear map; actual finite row correspondence existence; rational flow witness equivalence.',
   'ordinary_only_or_missing_source':['Countable ℓ1 cap-envelope compactness/application','General arbitrary Kakutani correspondence theorem (cited, not reimplemented)','Full Python vertex-enumerator refinement proof in Lean']},
 'CV-R':{'modules':['P02A2.Refinement','P02A2.Observation','P02A2.Fibres'],
   'covered':'Actual measurable observation bridge; normalized one-step fibre debt; finite telescope; summable disjoint losses; full-history defect identity with J; real budget algebra.',
   'ordinary_only_or_missing_source':['Cell-mass limit/uniform-small-cell equivalence Lean strengthening','Almost-everywhere coherence wrapper (candidate core uses explicit pointwise coherence)','Optional conditional-expectation/martingale result']},
 'CV-C':{'modules':['P02A2.ObserverCore'],
   'covered':'Typed LOOP syntax and structural semantics; prefix causality; diagonal non-surjectivity; rational shift comparison algebra.',
   'ordinary_only_or_missing_source':['Full byte codec/Python interpreter/primitive-recursion closure simulation in Lean','Fair-Cantor cylinder counting and soft-mass convergence in Lean','Code-level hierarchy membership/hardness reductions and exact table in Lean','Finite Mealy universal algorithm-to-law refinement in Lean']},
 'Q1c':{'modules':['P02.T300ThreeBit','P02A2.FiniteLaw','P02A2.AllNParity','P02A2.ParityBridge','P02A2.FiniteMeasureBridge'],
   'covered':'General finite rational law/Measure interface; deterministic and stochastic transport; all-n mask counts linked to enumerated bit-word events; proper profiles and mixture formulas; unchanged seven three-bit candidates.',
   'ordinary_only_or_missing_source':['Fin n → Bool coordinate-wrapper identification to list masks','Complete all-n deterministic flip/overwrite Measure-map composition wrapper','Walsh observable formulation in Lean']}}
for ob,v in coverage.items():
 v.update({'kernel_compilation':'HOST_EXECUTION_BLOCKED','mathematical_proofs':'SUPPLIED_ORDINARY',
  'source_status':'AUTHORED_UNEXECUTED_CANDIDATES_WITH_EXPLICIT_COVERAGE_LIMITS',
  'declaration_type_readback':None,'axiom_audit':None,'olean_artifact_identity':None,
  'candidate_declarations':[x['declaration'] for x in inv['theorems'] if x['module'] in v['modules']]})
save('FORMAL_COVERAGE.json',{'Lean':'4.19.0 / 6caaee842e94','Mathlib':'c44e0c8ee63ca166450922a373c7409c5d26b00b',
 'coverage':coverage,'formal_source_complete_for_all_obligations':False,
 'unproved_prop_definitions_not_counted_as_proofs':['P02A2.FiniteLaw.properMarginalTarget','P02A2.Refinement.UniformSmallCells','P02A2.ObserverCore.Sigma2Normal','P02A2.ObserverCore.Pi3Normal'],
 'kernel_checked_targets':0,'no_sorryAx_acceptance':True,'no_wrong_version_credit':True})
# Internal edges are scoped, not topic adjacency.
edges=[
 ('M2-01','R2-01','MEASURE_PREREQUISITE','Countable measurable positive-singleton support'),
 ('M2-03','R2-02','MEASURE_PREREQUISITE','Normalized positive fibre one-step debt'),
 ('R2-01','R2-03','CORE_DEPENDENCY','Decreasing measurable events and full-history subset'),
 ('R2-03','R2-06','SEMANTIC_BUDGET','Exact residual formula'),
 ('M2-02','R2-06','RICHNESS_CONDITIONAL_ONLY','Necessity for arbitrary conull conjunction certificates'),
 ('M2-01','C2-08','MEASURE_PREREQUISITE','Countable support and singleton measurability'),
 ('M2-04','C2-11','MEASURE_PREREQUISITE','Countable selector mixture identity'),
 ('M2-04','C2-12','MEASURE_PREREQUISITE','Rational selector law, including non-dyadic q'),
 ('C2-01','C2-06','CODEC_DEPENDENCY','Concrete syntax and indexing'),
 ('C2-02','C2-06','COMPILER_DEPENDENCY','PR byte constructors and numeric coding'),
 ('C2-03','C2-10','EXPRESSIVE_CLASS','Every fixed PR matrix admits the implemented LOOP representation'),
 ('C2-06','C2-10','REDUCTION_COMPILER','Sigma2 compiler semantics'),
 ('C2-06','C2-11','REDUCTION_COMPILER','Pi3 row compiler semantics'),
 ('C2-06','C2-12','REDUCTION_COMPILER','Rational shift compiler semantics'),
 ('C2-08','C2-09','HIERARCHY_MEMBERSHIP','Soft atomic mass formula'),
 ('F2-03','F2-06','FEASIBILITY_EXISTENCE','Actual finite-row stationary point implies rational-flow polytope is nonempty'),
 ('M2-01','F2-03','OPTIONAL_MEASURE_INTERPRETATION','Finite-support laws have zero singleton defect'),
 ('M2-01','Q2-01','OPTIONAL_MEASURE_INTERPRETATION','Zero-defect interpretation only; pure finite law does not need infinite measure theory'),
 ('Q2-01','Q2-04','FINITE_PROBABILITY','Mixture and kernel algebra')]
save('P02_INTERNAL_DEPENDENCY_MAP.json',{'schema':'p02-research-dependencies-v2','not_integration_DAG':True,
 'nodes':[{'id':x['id'],'obligation':x['obligation']} for x in cat],
 'edges':[dict(source=a,target=b,kind=c,reason=d) for a,b,c,d in edges],
 'independence':['CV-R does not require U08 fixed-point existence or a CV-C decision procedure.',
 'CV-C hardness uses elementary fair finite bit probabilities, not the T300 parity theorem.',
 'Q1c pure parity/counting does not require U05 formal PASS.',
 'No U08 convergence/effective selection is consumed implicitly.',
 'Finite Mealy decidability is a separate representation, not an algorithm for the PR hierarchy.'],
 'other_packet_new_passes_assumed':[]})
# Scope-specific research acceptance and explicit incomplete formal work.
status={
 'U05':'PARTIAL — EXACT IRREDUCIBLE BLOCKER: exact Lean 4.19.0 execution is unavailable on this host.',
 'U08':'PASS',
 'CV-R':'PARTIAL — EXACT IRREDUCIBLE BLOCKER: exact Lean 4.19.0 execution is unavailable on this host.',
 'CV-C':'PARTIAL — EXACT IRREDUCIBLE BLOCKER: exact Lean 4.19.0 execution is unavailable on this host.',
 'Q1c':'PASS'}
just={
 'U05':'The general ordinary measure family and an exact pinned candidate/API plan are supplied. The expanded full-formal-source goal is NOT complete: weak-limit and Q8 Lean bridges are still missing. Host blockage is real but is not the sole remaining work.',
 'U08':'Research acceptance is discharged: an actual correspondence is matched to every stated existing theorem hypothesis; finite and countable safe envelopes are proved, the unsupported unrestricted domain is refuted, and rational effectivity/convergence obstructions are separated. PASS is research-only, not general Kakutani kernel credit or adoption.',
 'CV-R':'The exact core finite/infinite weighted-fibre/residual/budget formal candidates are authored. They have not elaborated under 4.19.0. Additional cell-mass, a.e.-coherence and optional martingale Lean strengthening remains ordinary-only; no full formal-family closure is claimed.',
 'CV-C':'Concrete codec and compilers, universal ordinary simulation arguments, membership/hardness proofs and finite-state separation are supplied. The full Lean code-to-fair-law/soft-mass/hierarchy refinement is not authored. This internal source gap is not renamed external or irreducible.',
 'Q1c':'The original scoped-proposal acceptance criterion is discharged with exact public target recovery, all-n ordinary probability proofs, a general finite law/measure candidate layer, all-n enumerated-mask candidates and the two concrete interventions. PASS is not a compiled coordinate-wrapper or historical recovery claim.'}
results=[]
for o in obs:
 id=o['id'];results.append({'id':id,'terminal_status':status[id],
 'original_obligation':o,'research_acceptance_rationale':just[id],
 'mathematical_proof_status':'ORDINARY_PROOFS_SUPPLIED_AT_EXACT_HYPOTHESES',
 'Lean_source_status':coverage[id]['source_status'],'Lean_4_19_0_compilation':'NOT_EXECUTED_HOST_BLOCKED',
 'declaration_type_readback':None,'axiom_audit':None,'olean_artifact_identity':None,
 'source_work_remaining':coverage[id]['ordinary_only_or_missing_source'],
 'irreducibility_claim_scope':'Actual host acquisition/execution only; internal source gaps are NOT claimed irreducible.',
 'full_expanded_exhaustion_criterion_met':False,
 'canonical_status_changed':False,'owner_adoption_credit':False,'external_review_credit':False,'historical_recovery_credit':False})
save('OBLIGATION_RESULTS.json',{'schema':'p02-attempt2-research-results-v1','results':results,
 'research_acceptance_PASS':['U08','Q1c'],'kernel_PASS':[],
 'full_exhaustion_certified':False,'missing_source_work_not_concealed_as_host_blockage':True})
# The P03 interface is explicitly evidence-level typed.
allowed=['M2-01','M2-02','M2-03','M2-04','M2-05','M2-06','R2-01','R2-02','R2-03','R2-04','R2-05','R2-06',
 'Q2-01','Q2-02','Q2-03','Q2-04','C2-01','C2-02','C2-03','C2-05','C2-06','C2-07','C2-08','C2-09','C2-10','C2-11','C2-12','C2-13','C2-14','F2-03','F2-04','F2-05','F2-06','F2-07']
bindings=[]
for x in cat:
 if x['id'] not in allowed:continue
 bindings.append({k:x[k] for k in ['id','obligation','title','proof_file','proof_file_sha256','source_start_line','source_end_line','section_sha256','common_hypotheses']}|
  {'may_consume_as':'ORDINARY_MATHEMATICAL_RESEARCH_PREMISE_WITH_EXPLICIT_HYPOTHESES',
  'kernel_verified':False,'automatic_P03_kernel_axiom_permission':False,
  'formal_coverage_pointer':'FORMAL_COVERAGE.json#/coverage/'+x['obligation'],
  'conditionality':'All exact hypotheses in the cited section; no result from another packet assumed.'})
save('P03_CONSUMER_BINDINGS.json',{'schema':'p02-to-p03-research-interface-v2',
 'supersedes_interface_of_predecessor_sha256':'365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9',
 'supersedes_only':'P02 research interface/proposal coverage, not unchanged historical evidence or canonical status.',
 'bindings':bindings,'code_bindings':[ident(R/'code/prcodec.py'),ident(R/'code/flow_solver.py')],
 'mandatory_guards':['Keep J in infinite refinement and include it in budget transport.',
 'Rich-event necessity requires the actual declared repertoire; countable syntax alone is not rich.',
 'No inference from weak limits that d≤epsilon is closed; use an explicitly proved safe domain.',
 'P02-L1 indices are new; do not reinterpret old proposal indices as these byte codes.',
 'Hierarchy is for total PR synchronous observers with fair input, not arbitrary/P03 parser programs.',
 'ResourceLimit is refusal/non-answer, never a zero-defect witness.',
 'Formal consumers may not import ordinary proof text as trusted axioms or count unexecuted source as kernel evidence.',
 'Research PASS does not imply a P03 checker/implementation refinement proof.'],
 'other_packet_results_assumed':[],'canonical_effect_authorised':False})
# Inputs remain exact; no remote status is freshly claimed.
save('provenance/INPUT_IDENTITIES.json',{'predecessor':ident(R/'predecessor/Orthemology_P02_Measure_Research_Checkpoint_20260922.zip'),
 'expected_members':693,'nested_original_packet_sha256':'70630d5b703fb3262e123b8424c19580e95bf604db3e9eb5d364653c333fdf13',
 'main':'03e2604dfcef278b01c60d19b05370fcec4194b6','tree':'3d06e80277ce39286c94307e0f14b215bc94ed83','PR_merged':28,
 'integration_remaining':0,'identity_scope':'Accepted inherited packet, not fresh remote requalification',
 'assigned_source_bindings':{o['id']:o['source_bindings'] for o in obs},
 'T300_additional_binding':next(o for o in old if o['id']=='Q1c')['additional_input_bindings']})
# Computational evidence dimensions separated for each classification group.
save('COMPUTABILITY_EVIDENCE_DIMENSIONS.json',{'coding':'P02-L1','rows':[
 {'claim':'Finite Mealy decidability and rational hitting probability','finite_execution':'Preserved predecessor census; no replay',
  'ordinary_proof':'C2-14','reduction_proof':'Not needed for finite decidability','hierarchy_membership':'Decidable finite presentation',
  'hierarchy_hardness':'No general PR hardness inferred from finite state','implementation_correspondence':'Universal ordinary invariant/linear-solver argument; not Lean-verified'},
 {'claim':'PR observer threshold and endpoint completeness table','finite_execution':'New compiler prefix tests and fixtures; never a proof of an infinite defect value',
  'ordinary_proof':'C2-08..C2-13','reduction_proof':'C2-10/11/12 bound to concrete compile_sigma2/compile_pi3/compile_shift',
  'hierarchy_membership':'C2-09, including explicit PR bounded-rejection normal-form conversion',
  'hierarchy_hardness':'C2-10/11/12 for each stated rational threshold and endpoint',
  'implementation_correspondence':'C2-01..C2-07 ordinary proof; byte implementation tested; full Lean simulation missing'},
 {'claim':'Q8 restricted bounded-halting family','finite_execution':'Concrete finite two-counter programs and mutation test',
  'ordinary_proof':'M2-06 and C2-06','reduction_proof':'compile_q8; machine halting iff diffuse fresh-bit tail',
  'hierarchy_membership':'Restricted binary family; not the complete broader Pi03 theorem',
  'hierarchy_hardness':'Nonhalting reduction only at this restricted family',
  'implementation_correspondence':'Explicit bounded-simulation invariant; no kernel evidence'}],
 'new_kernel_classification_proofs':0})
# Negative controls, refutations and honest remaining source coverage.
save('NEGATIVE_FINDINGS.json',{'original_statuses_preserved':True,'refutations':[
 {'id':'M2-01-ATOM','claim':'Every measurable atom is a singleton atom without space hypotheses','countermodel':'Countable/co-countable probability space','replacement':'Countable separating measurable family implies positive atoms are point-carried'},
 {'id':'M2-05-WEAK','claim':'Singleton defect is weakly continuous or safe laws are unconditionally weakly closed','countermodel':'Finite grids -> diffuse law; shrinking diffuse laws -> Dirac','replacement':'Fixed finite/at-most-m atom classes weakly closed; total-variation 1-Lipschitz defect'},
 {'id':'F2-02-ROTATION','claim':'Every continuous invariant map on all d≤epsilon safe laws has a safe fixed point','countermodel':'Irrational rotation on circle, epsilon<1','replacement':'Actual compact finite or summable-cap envelopes'},
 {'id':'R2-J','claim':'Finite budget bounds alone imply full-history budget without residual/slack control','countermodel':'Preserved fair-prefix and mixed 1/3+5/12 witnesses','replacement':'Exact J≤epsilon-L; J=0 sufficient not necessary'},
 {'id':'C2-07-SURJECTIVITY','claim':'PR observer codes cover every computable synchronous observer injectively','countermodel':'Computable diagonal constant observer; distinct unused-register programs with same denotation','replacement':'Surjective onto declared PR prefix class; syntax injective codec; denotation not injective'},
 {'id':'Q2-DIMENSION','claim':'Pairwise blindness applies also when n=2 and pair is full coordinate set','countermodel':'Full parity is distinguished','replacement':'Proper marginals; pairwise theorem n≥3'}],
 'invalid_evidence_preserved':['INVALID_MUTATION_DISCOVERY','SURVIVING_SHIFT_MUTANT','VERIFIER_HARDENING_RED'],
 'corrected_controls':'MUTATION_RESULTS.json: six assertion failures, zero discovery errors, matching green baselines',
 'host':'Exact Lean absent; actual runner failed closed at exit127 before any compilation',
 'source_coverage':'Full Lean bridges missing as listed in FORMAL_COVERAGE.json; not all are external blockers.'})
save('UNRESOLVED_DEPENDENCIES.json',{'host_external':[{'id':'HOST-LEAN419','condition':'Usable exact Lean4.19.0/Lake and pinned dependency sources/cache','executed_attempt_evidence':'evidence/environment; evidence/TOOL_MEDIATED_ACQUISITION.json; evidence/FORMAL_HOST_GATE'}],
 'internal_formal_source_gaps':{o:coverage[o]['ordinary_only_or_missing_source'] for o in coverage},
 'owner_or_custody_not_research_premises':['Canonical adoption/implementation effects','Exact unavailable historical source identities/weights','Independent specialist review','Licensing/publication/empirical-world authority'],
 'full_requested_exhaustion_met':False,
 'reason':'The portable result is substantial but the complete Lean source/verification coverage requested is not attained. Missing internal proof bridges are stated rather than falsely declared irreducible external work.'})
print(json.dumps({'predecessor_families':len(rows),'new_result_sections':len(cat),'P03_bindings':len(bindings),'candidate_theorems':inv['theorem_count']}))
