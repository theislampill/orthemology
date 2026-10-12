#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def H(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((R/p).read_text())
def write(p,j):(R/p).write_text(json.dumps(j,indent=2)+'\n')
inv=read('formal/SOURCE_INVENTORY.json');source_hash=H((R/'formal/SOURCE_INVENTORY.json').read_bytes())
allnames={t['name']:t for t in inv['targets']}
base={'kernel_credit':False,'canonical_adoption':False,'historical_status_rewritten':False,
      'lean_4_19_compilation':'HOST_EXECUTION_BLOCKED','declaration_type_readback':{},'axiom_audit':{},
      'compiled_artifacts':[],'source_inventory_sha256':source_hash,'novelty_claim':False}
statuses={
'U09':{**base,'terminal_status':'PARTIAL — EXACT IRREDUCIBLE BLOCKER: exact Lean 4.19.0 compilation, declaration/type readback and axiom audit of the fully authored U09 candidate modules cannot execute on this host.',
 'inherited_status':'PARTIAL','ordinary_mathematics':'PROVED_AT_EXACT_SOURCE_SCOPE',
 'formal_source_status':'COMPLETE_AUTHORED_CANDIDATE_BODIES_BUT_UNVERIFIED',
 'completed_local_gates':['canonical seven-rule finite typing and source relations fixed','target Curry syntax/typing and both substitutions','lambda generation across forall rules and target subject reduction','typing preservation and positive compatible simulation','finite/chain and conditional target-SN reflection','independent direct source SN','source confluence/NF completeness','Omega no finite representative modulo Conv'],
 'refuted_subclaim':'Target beta-convertibility implies raw source Conv.',
 'replacement':'Source conversion is preserved; finitely typed source inputs have unique source normal forms, and conversion is equality of those normal forms.',
 'ordinary_work_not_deferred':True,
 'not_claimed':['target-conversion reflection','new global target-System-F-SN mechanisation','semantic Code SN','kernel proof before actual compile']},
'U10':{**base,'terminal_status':'REFUTED_AS_STATED / REPLACEMENT_PROVED','inherited_status':'REFUTED_AS_STATED / REPLACEMENT_PROVED',
 'ordinary_mathematics':'PRESERVED_EXACT_ATTEMPT2_REPLACEMENT_MODEL_AND_THEOREMS',
 'formal_source_status':'GENERIC_PER_AND_EXPLICIT_ALL_INTERFACES_AUTHORED_UNCOMPILED; FULL_RECURSIVE_ORDINARY_MODEL_MECHANISATION_NOT_CLAIMED',
 'refutation_scope':['unrestricted raw-conversion identity extension','arbitrary fixed-environment unary membership entails relational membership','unconditional coupling-existence/intersection interchange'],
 'replacement':'Endpoint-indexed respectful PER/link model and source abstraction theorem with explicit dependent coherence; finite common-coupling criterion and shared-seed effect theorem.',
 'original_contract_disposition':'Resolved by precise refutations plus the preserved ordinary replacement at its stated hypotheses; accepted finite R1 unchanged.',
 'new_research_repetition':False,'kernel_qualification_required_for_formal_claims':True,
 'not_claimed':['arbitrary canonical Code is parametric','new full recursive/dependent U10 kernel model','novelty or independent expert review']},
'U11':{**base,'terminal_status':'PARTIAL — EXACT IRREDUCIBLE BLOCKER: exact Lean 4.19.0 qualification of the authored intrinsic tracked dependent core, generated finite envelopes and partial proof-replay soundness targets cannot execute on this host.',
 'inherited_status':'PARTIAL','ordinary_mathematics':'PROVED_FOR_PROPOSED_INTRINSIC_CORE_AND_EXPLICIT_PARTIAL_REPLAY_INTERFACE',
 'formal_source_status':'COMPLETE_AUTHORED_CANDIDATE_BODIES_FOR_NAMED_CORE_AND_REPLAY_SCOPE_BUT_UNVERIFIED',
 'completed_local_gates':['finite polynomial abstraction beta and structural laws','valid contexts/coherent types/tracked terms/substitutions','Pi/Sigma/identity/contextual J with both coherence coordinates','explicit parametric All formation/uniform introduction/elimination/self','exact Girard-sensitive closure exclusion','strict finite-evidence frontend and source-path proof replay','partial canonical exporter with bound target objects','nonempty dependent/All examples and finite generated replay targets'],
 'refuted_subclaim':'Every accepted dependent frontend result has a total literal export to unchanged canonical TypeCode/Cert with no refusal.',
 'replacement':'Partial exact finite rendering plus kernel admission only through real bound FiniteEnvelope/DependentEnvelope; accepted replay is sound, refusal produces no proof.',
 'ordinary_work_not_deferred_at_replacement_scope':True,
 'not_claimed':['universal machine verification of Python/JSON interpreter','a total arbitrary-JSON-to-intrinsic dependent interpreter','decision of all PER equalities','SN of all semantic/dependent realisers','same-level Girard-sensitive closure','canonical adoption of the new admission interface']}}
write('STATUS_RECORDS.json',statuses)
for u,r in statuses.items():write('boundary/'+u+'_TERMINAL_DISPOSITION.json',r)
write('formal/FORMAL_STATUS.json',{'required_pin':'leanprover/lean4:v4.19.0',
 'required_lean_commit_prefix':'6caaee842e94','required_mathlib':'c44e0c8ee63ca166450922a373c7409c5d26b00b',
 'candidate_module_count':len(inv['build_order'])-12,'public_declaration_targets':len(inv['targets']),
 'explicit_private_dependencies':len(inv['private_dependencies']),
 'ordinary_proof_scope':'research documents and exact predecessor documents; not a kernel readback',
 'source_authoring':'all named definition/proof bodies supplied; elaboration/tactic correctness unverified',
 'source_inventory_sha256':source_hash,'compile_status':'HOST_EXECUTION_BLOCKED',
 'kernel_credit':False,'compiled_artifacts':[],'declaration_type_readback':{},'axiom_readback':{},
 'axiom_policy_only':['propext','Classical.choice','Quot.sound'],
 'source_status_by_obligation':{u:r['formal_source_status'] for u,r in statuses.items()},
 'scope_exclusions':statuses['U11']['not_claimed']+statuses['U10']['not_claimed']})
# Logical dependencies are distinct from exact file imports, retained below.
ns=[]
def node(i,deps,scope,files,targets=(),premises=()):
 for n in targets:
  if n not in allnames:raise ValueError('unknown target '+n)
 ns.append({'id':i,'depends_on':deps,'scope':scope,'files':files,'formal_targets':list(targets),'explicit_premises':list(premises)})
node('S0',[],'UNCHANGED_CANONICAL_SOURCE',['formal/vendor/FiniteBridge.lean','formal/vendor/BoundaryResults.lean'])
node('F1',['S0'],'NEW_SUBSTITUTION_PROOF',['formal/P01TypeAlgebra.lean','formal/P01LambdaSyntax.lean'])
node('F2',['F1'],'TARGET_TYPING_SUBSTITUTION_GENERATION_SUBJECT_REDUCTION',['formal/P01SystemF.lean'],['P01F.type_substitution','P01F.term_substitution','P01F.lambda_generation','P01F.subject_reduction'])
node('F3',['S0','F1'],'POSITIVE_COMPATIBLE_SIMULATION',['formal/P01Translation.lean'],['P01F.step_simulation','P01F.reduction_simulation','P01F.conversion_preservation'])
node('F4',['F2','F3'],'ALL_SEVEN_FINITE_TYPING_RULES',['formal/P01Translation.lean'],['P01F.typing_preservation'])
node('F5',['F3'],'CONDITIONAL_TARGET_SN_ROUTE',['formal/P01Translation.lean','formal/P01SNReflection.lean'],['P01F.target_SN_implies_source_SN','P01F.chain_simulation'],['actual target accessibility proof; not asserted globally'])
node('N1',['S0'],'DIRECT_SOURCE_REDUCIBILITY_ROUTE_INDEPENDENT_OF_SYSTEM_F',['formal/P01Candidates.lean','formal/P01SNReflection.lean'],['P01Candidates.finite_reducibility','P01Candidates.finite_SN'])
node('N2',['S0'],'RAW_SOURCE_CONFLUENCE_INDEPENDENT_OF_TARGET_CONVERSION',['formal/P01Confluence.lean'],['P01Source.confluence'])
node('N3',['N1','N2'],'NORMAL_FORMS_AND_TYPED_CONVERSION',['formal/P01Confluence.lean'],['P01Source.conversion_by_normal_forms'])
node('N4',['N2','N3'],'OMEGA_INVARIANT_AND_NONREPRESENTABILITY',['formal/P01Omega.lean'],['P01Source.omega_no_finite_representative'])
node('N5',['N2','F3'],'REFUTED_TARGET_REFLECTION',['formal/P01ReflectionCountermodel.lean'],['P01F.target_conversion_reflection_false'])
node('R0',['S0'],'PROPOSED_ENDPOINT_PER_EQUALITY_NOT_RAW_CONV',['formal/P01PER.lean','predecessors/attempt2_surviving_exact/research/U10_REPLACEMENT_MODEL.md'])
node('D1',['S0'],'FINITE_TRACKER_SUBSTITUTION_AND_APPLICATION_BETA',['formal/P01Polynomials.lean'],['P01D.abstraction_beta','P01D.abstraction_naturality','P01D.abstraction_substitution'])
node('D2',['R0','D1'],'INTRINSIC_VALID_CONTEXTS_TYPES_TERMS_AND_SUBSTITUTIONS',['formal/P01DependentCore.lean'],['P01D.typing_under_substitution','P01D.term_substitution_related'])
node('D3',['R0','D1','D2'],'COHERENT_PI_AND_TYPED_ABSTRACTION',['formal/P01PER.lean','formal/P01DependentCore.lean'],[],['coherent domain/fibre PERs; tracked body derivation'])
node('D4',['R0','D2'],'REPRESENTED_SIGMA_AND_ETA',['formal/P01PER.lean','formal/P01DependentCore.lean'],['P01D.sigma_eta'],['representation on Sigma inhabitants'])
node('D5',['R0','D1','D2'],'IDENTITY_AND_CONTEXTUAL_BASED_J',['formal/P01ContextualJ.lean'],['P01D.j','P01D.j_computation'],['motive coherent in endpoint AND proof coordinate'])
node('R1',['R0','D2','D3','D4','D5'],'PRESERVED_ORDINARY_RELATIONAL_MODEL_AND_ABSTRACTION_THEOREM',['predecessors/attempt2_surviving_exact/research/U10_REPLACEMENT_MODEL.md'],[],['explicit endpoint/link environments and transported dependent fibres'])
node('R2',[],'PRESERVED_FINITE_HALL_COMMON_COUPLING_CRITERION',['predecessors/attempt2_surviving_exact/research/U10_COUPLING_THEOREMS.md'],[],['finite rational laws; intersection support relation'])
node('R3',['R1','R2'],'PRESERVED_SHARED_SEED_FINITE_EFFECT_THEOREM',['predecessors/attempt2_surviving_exact/research/U10_COUPLING_THEOREMS.md'],[],['fixed finite sampling syntax and weights; related environments; ONE common seed/coupling'])
node('D6',['R0','D2','R1'],'EXPLICIT_PARAMETRIC_ALL_AND_LEGAL_SELF_INSTANTIATION',['formal/P01PER.lean','formal/P01DependentCore.lean','formal/P01Examples.lean'],['P01D.allIntro','P01D.allElim','P01D.allSelf'],['ParamFamily body relation/IE; contextual coherence; uniformity proof at introduction'])
node('D7',['D6'],'EXACT_GIRARD_SENSITIVE_BOUNDARY',['formal/P01UniverseBoundary.lean','formal/vendor/HurkensBoundary.lean'],['P01D.no_same_level_Girard_retraction'],['hypothetical full ambient GirardFamily pack/unpack and beta; NOT supplied by All self-instantiation'])
node('E1',['S0','D1','D2','D3','D4','D5','D6'],'NEW_FINITE_EVIDENCE_FRONTEND_PROPOSAL',['executable/checker.py','research/U11_REFINEMENT_AND_SOUNDNESS.md'],[],['only explicit computational equality or literal equality; guards refuse'])
node('E2',['S0','N1'],'RAW_SOURCE_PROOF_REPLAY',['formal/P01Certificates.lean'],['P01Certificate.replay_sound','P01Certificate.join_sound','P01Certificate.finite_envelope_sound','P01Certificate.finite_envelope_SN'])
node('E3',['E1','E2','D1'],'PARTIAL_EXACT_CANONICAL_EXPORT',['executable/checker.py','formal/P01GeneratedExports.lean'],[],['supported TypeCode/Cert image; closed runtime context; exact type/code commitments; actual replay required for kernel admission'])
node('E4',['D2','D3','D4','D5','D6'],'INTRINSIC_DEPENDENT_PROOF_REPLAY',['formal/P01Certificates.lean'],['P01Certificate.dependent_envelope_sound','P01Certificate.accepted_replay_sound','P01Certificate.refusal_preserved'],['real intrinsic Tm plus exact polynomial binding; no premise that arbitrary JSON supplies it'])
node('E5',['S0','E1'],'TOTAL_LITERAL_EXPORT_REFUTED',['formal/P01Certificates.lean','executable/test_checker.py'],['P01Certificate.identity_not_in_exact_target_image','P01Certificate.sigma_not_in_exact_target_image'])
node('K0',['F4','F5','N4','N5','D7','E2','E3','E4'],'EXTERNAL_EXACT_PIN_KERNEL_QUALIFICATION',['handoff/qualify_lean419.py','formal/P01Audit.lean'],[],['actual4.19.0 compiler/dependencies; fresh nonempty artifacts; exact declaration/type/axiom readbacks'])
dag={'schema':'p01-internal-dependency-map-v3','nodes':ns,
     'P02_dependencies':[],'P03_dependencies':[], 'formal_file_imports':inv['imports'],
     'logical_dependencies_not_equated_with_module_imports':True,
     'forbidden_inferences':['target beta equality -> raw source Conv','PER equality -> raw source Conv','source NF decision -> arbitrary PER equality decision','finite source SN -> all semantic/dependent tracker SN','forall relation exists coupling -> one common coupling without common-support hypotheses','legal All self-instantiation -> full ambient section reification/SCUU','frontend ACCEPTED -> kernel admitted without exact proof replay','historical mapped-native or4.32.2 output -> new4.19.0 target credit']}
ids={n['id']:n for n in ns};active=set();done=set()
def visit(i):
 if i in active:raise ValueError('cycle '+i)
 if i in done:return
 active.add(i)
 for p in ids[i]['depends_on']:visit(p)
 active.remove(i);done.add(i)
for i in ids:visit(i)
dag['acyclic']=True;write('P01_INTERNAL_DEPENDENCY_MAP.json',dag)
# Literal obligation/predecessor language stays in its own immutable data record.
obs=read('boundary/ORIGINAL_OBLIGATIONS.json')
conf=[]
for o in obs:
 conf.append({'id':o['id'],'title':o['title'],'exact_original_record':o['exact_source_record'],
  'completion_criteria':o['completion_criteria'],'falsification_criteria':o['falsification_criteria'],
  'predecessor_theorem_ids':o['predecessor_theorem_ids'],'source_bindings':o['source_bindings'],
  'original_canonical_status':o['source_status'],'attempt3_proposed_status':statuses[o['id']]['terminal_status'],
  'canonical_status_changed':False})
write('boundary/OBLIGATION_CONFIRMATIONS.json',conf)
write('boundary/REMAINING_BLOCKERS.json',[
 {'id':'EXTERNAL-KERNEL-419','scope':['U09 formal qualification','U11 formal qualification','new optional U10 formal targets'],
  'kind':'HOST_EXECUTION_BLOCKED','condition':'Obtain exact Lean4.19.0 and locked dependencies, actually elaborate all inventoried sources and obtain fresh nonempty artifacts plus exact type/axiom audits.',
  'evidence':'evidence/LEAN_QUALIFICATION.json','source_authoring_not_hidden_as_blocker':True},
 {'id':'EXTERNAL-A2-EXACT-CUSTODY','scope':['original attempt2 ZIP/workspace identity only'],
  'kind':'EXACT_BYTES_ABSENT','condition':'Actual missing archive/workspace bytes, if they exist on another surface. No reconstruction from prose.',
  'mathematical_research_dependency':False,'evidence':'boundary/ATTEMPT2_RECOVERY.json'},
 {'id':'OWNER-CANONICAL-ADOPTION','scope':['later repository/source-status effects'],
  'kind':'NOT_AUTHORISED','condition':'Explicit later owner/Codex review and effect authority; not required for the stated ordinary research results.',
  'mathematical_research_dependency':False}])
write('boundary/PROPOSED_DEFINITIONS_AND_SOURCE_MAP.json',{
 'mode':'NEW_PROPOSAL_ADDITIONS_ONLY','canonical_source_mutated':False,
 'new_definitions':['Curry Has target independent of source typing','normalisation Candidate distinct from semantic Code','type-relative respectful PER/Link and explicit ParamFamily/AllFormation interfaces','intrinsic tracked Context/Ty/Tm/Sub calculus','represented Sigma and coherent represented identity','finite-evidence frontend computational equality','binding-preserving partial FiniteEnvelope/DependentEnvelope admission'],
 'changed_accepted_definitions':[],
 'explicit_premises':['coherent fibres','tracked finite polynomial substitutions','body identity extension and relation data for ParamFamily','uniformity for All introduction','endpoint and proof-coordinate coherence for J','bound real proof object for replay admission'],
 'exact_preimages':'inputs/original/source-main and formal/vendor; all original hashes retained',
 'new_statement_inventory':'formal/SOURCE_INVENTORY.json',
 'literature_comparison':'inputs/attempt1/research/LITERATURE_COMPARISON.md; preserved without new novelty credit',
 'formal_metadata_change':{'path':'formal/lake-manifest.json','change':'root package name p01Attempt3 only; all dependency revisions match original lock','old_preimage':'inputs/original/source-main/experiments/orthemology-v5/formal_project/lake-manifest.json'}})
# Exact surviving input and newly authored statement identities; exclude dynamic seal metadata.
ident=[]
for folder in ['predecessors','boundary','research']:
 for p in sorted((R/folder).rglob('*')):
  if p.is_file():ident.append({'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':H(p.read_bytes())})
write('INPUT_AND_STATEMENT_IDENTITIES.json',{'files':ident,'formal_source_inventory_sha256':source_hash,
 'attempt1_expected':{'bytes':984262,'sha256':'2564e3b5e994e3676f3b63619bc452f1d297300050f9743454f05f4ff38fcbd6'},
 'recovery_kind':'EXACT_SIX_DOCUMENT_SURVIVORS_NOT_COMPLETE_ATTEMPT2', 'kernel_credit':False})
print(json.dumps({'status_records':len(statuses),'dependency_nodes':len(ns),'acyclic':True,
 'candidate_modules':len(inv['build_order'])-12,'public_targets':len(inv['targets']),
 'new_kernel_credit':False},indent=2))
