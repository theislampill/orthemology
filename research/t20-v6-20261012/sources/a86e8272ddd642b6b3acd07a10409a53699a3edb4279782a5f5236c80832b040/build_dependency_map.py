#!/usr/bin/env python3
"""Execution provenance for this run. Working paths are not handoff instructions.
The sealed map is authoritative; portable verification reads the embedded ZIPs.
"""
from pathlib import Path
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
P02=Path('private-locator:4ca860528aafed352fda');P03=Path('private-locator:21591a7f277cb1b3725e')
sha=lambda b:hashlib.sha256(b).hexdigest()
receipt=json.loads((P02/'RECEIPT.json').read_text())
results=json.loads((P02/'OBLIGATION_RESULTS.json').read_text())
notes={
'U05':'analysis/U05_MEASURE_SEMANTICS.md','U08':'analysis/U08_CORRESPONDENCE.md',
'CV-R':'analysis/CV_R_REFINEMENT.md','CV-C':'analysis/CV_C_COMPUTABILITY.md','Q1c':'analysis/Q1c_FINITE_PROBABILITY.md'}
export=[]
for r in results['results']:
    path=notes[r['id']];data=(P02/path).read_bytes();text=data.decode();target=ROOT/'inputs/p02-analysis'/Path(path).name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    export.append({'obligation':r['id'],'actual_obligation_status':r['obligation_status'],
       'statement_ids':r['output_statement_ids'],'source_member':path,'bytes':len(data),'sha256':sha(data),
       'exact_statement_and_proof_text':text,'exact_hypotheses_from_result':r.get('hypotheses'),
       'remaining_from_result':r['remaining'],'ordinary_status':r.get('ordinary_research_status'),
       'formal_status':r.get('formal_status'),'kernel_credit':r['kernel_credit'],
       'adoption_credit':False})
formal=[]
for p in sorted((P02/'proposals').rglob('*.lean')):
    data=p.read_bytes();formal.append({'member':str(p.relative_to(P02)),'bytes':len(data),'sha256':sha(data),'status':'UNEXECUTED_P02_CANDIDATE','kernel_credit':False,'exact_source':data.decode()})
(ROOT/'inputs/P02_EXACT_RESULT_INTERFACES.json').write_text(json.dumps({'archive_sha256':'365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9','statuses':receipt['obligation_statuses'],'scope':'Exact supplied P02 ordinary results and unexecuted candidates, not a new P02 completion or source adoption.','interfaces':export,'formal_candidates':formal},indent=2)+'\n')
for name in ['OBLIGATION_RESULTS.json','NEGATIVE_FINDINGS.json','UNRESOLVED_DEPENDENCIES.json']:
    shutil.copy2(P02/name,ROOT/'inputs'/('P02_'+name))
entries=[]
def edge(target,owner,ids,disposition,statement,premises,consequence,formal_status='NOT_DISCHARGED_NO_KERNEL_IMPORT',required=True):
    src=notes[owner]
    entries.append({'P03_target':target,'P02_owner':owner,'exact_P02_prerequisite':ids,
        'P02_actual_obligation_status':receipt['obligation_statuses'][owner],
        'dependency_disposition':disposition,'required_for_named_P03_target':required,
        'reusable_statement':statement,'premises_carried':premises,'P03_consequence':consequence,
        'evidence':{'archive_sha256':'365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9','member':src,'sha256':sha((P02/src).read_bytes()),'result_record':'OBLIGATION_RESULTS.json#'+owner},
        'ordinary_credit':'Ordinary source proof reviewed and instantiated in P03; no canonical adoption',
        'formal_dependency_disposition':formal_status})
edge('P03-A2-PROB-DECLARED (model defect and certificate)','U05',['P02-M01','P02-M02','P02-M04'],'FULLY_DISCHARGED_AT_ORDINARY_DECLARED_MODEL_SCOPE',
'Positive-singleton defect; rich measurable-conull intersection criterion; affine defect of a countable mixture.',
['Probability measures with measurable singletons','Engine finite-program or finitely tagged uniform-interval interpretation is fixed explicitly','Full measurable repertoire, and measurable conjunction intersections','Literal model identity is not empirical identification'],
'Finite-program observations have defect 0; tagged revealing-coordinate mass is exactly the sum of its component weights; certify accepts iff that declared defect is within tolerance, subject to arithmetic/transport resources.')
edge('P03-A2-PROB-REV (finite model refinement)','U05',['P02-M03'],'FULLY_DISCHARGED_AT_ORDINARY_DECLARED_MODEL_SCOPE',
'd(mu)=d(h_*mu)+sum_y nu{y} d(normalised positive fibre).',
['Both observation maps and coarsening factor measurable','Only positive fibres are normalised','Exact unchanged base law/carrier/weights for the engine report'],
'Engine report fibre weights, defects and increment instantiate M03. Syntactic all-component guards are sound but stricter than merely a.s. factorisation on zero-weight components.')
edge('P03-A2-PROB-REV (finite revision budget)','CV-R',['P02-R01','P02-R02','P02-R07'],'FULLY_DISCHARGED_AT_ORDINARY_FINITE_CHAIN_SCOPE',
'One-step increments telescope; final full-event epsilon certificate iff the cumulative increment fits the original slack.',
['Admissible nested observations over one declared probability law','Nonnegative exact increments','P02-M02 richness for necessity','Current-version licence separately revalidated'],
'Finite accepted refinement reports compose. Coarsening may improve defect but does not revive a stale ticket.')
edge('P03-A2-PROB-INFINITE (optional stream/history conclusion)','CV-R',['P02-R03','P02-R04','P02-R06','P02-R07'],'CONDITIONALLY_INHERITED_WITH_EXACT_RESIDUAL',
'd_infinity=d_0+sum_n Delta_n+J, J=mu(all positive finite cells but zero limiting cell).',
['Countable measurable compatible observation family','Measurable positive-cell sets','The residual J is included in any infinite certificate budget'],
'No inference from finitely safe dispatch prefixes to an epsilon-safe full history unless the full increment plus J fits. No general J=0 claim is made.',required=False)
edge('P03-A2-PROB-PUSH (finite input/outcome tables)','Q1c',['analysis/Q1c_FINITE_PROBABILITY.md section 2 (not a theorem ID)'],'FULLY_DISCHARGED_AT_ORDINARY_FINITE_TABLE_SCOPE',
'Nonnegative normalised finite mass table; deterministic pushforward by fibre sums; stochastic transport by row-normalised matrix multiplication.',
['Explicit finite input/environment distribution','Each branch outcome includes refusal/pending rather than silently conditioning it away','Any conditional independent bit law is stated'],
'Pointwise operational refinement lifts by finite sums. Kernel composition and conditional-event denominators are proved in the P03 note; no T300 witness is required.')
edge('P03-A2-PROB-PUSH (general measurable histories)','U05',['P02-M01','P02-M03'],'CONDITIONALLY_INHERITED_WITH_MEASURABILITY',
'P02-M01 defines positive-singleton defect; P02-M03 proves the positive-fibre coarsening defect identity. Equality of commuting pushforward history laws is derived separately in P03, not attributed to these P02 theorem statements.',
['One explicitly supplied joint law for inputs, entropy, scheduling and faults','Measurable concrete/abstract trace maps and abstraction','Pointwise operational simulation or almost-sure simulation on a common full set'],
'Exact probability-carrying refinement is conditional on that environmental law, not on fair random bits being physically present.')
edge('CV-O convergence / stationary-policy extrapolation','U08',['P02-F01','P02-F02','P02-F03','P02-F04'],'NOT_A_PREREQUISITE_FOR_DEPLOYED_CV_O',
'New finite-simplex correspondence has fixed points under its explicit row-set hypotheses; existence neither forces iteration convergence nor a general computable sampler.',
['Restricted row-set proposal, not all safe measures','No such solver/iteration exists in the bound Engine'],
'No CV-O convergence or fixed-point claim is made. P02 Kakutani/flow formal gaps do not block the existing operational transition theorem.',required=False)
edge('CV-O observer certificate / possible stronger finite observer','CV-C',['P02-C04'],'OPTIONAL_INTERFACE_ORDINARY_ONLY_NOT_USED_AS_ENGINE_IMPLEMENTATION',
'For the specified finite Mealy model, atomic mass equals probability of reaching deterministic-output states; exact rational hitting algorithm.',
['Finite nonempty Mealy control state and IID fair bits','Not the same as arbitrary binary-tape programs'],
'The deployed engine uses a stronger sufficient closed-control-state nonhalting certificate, proved directly; C04 is not silently identified with that implementation.',required=False)
edge('CV-O arbitrary PR observer decision','CV-C',['P02-C-SYNTAX-01','P02-C01','P02-C02','P02-C03'],'NOT_A_PREREQUISITE_UNSUPPORTED_EXTENSION',
'Exact soft-mass limits and index-class analysis at a specified total PR-synchronous numbering; byte codec and compiler remain unimplemented.',
['No arbitrary PR classifier is present in the finite operational grammar'],
'No broad WAITING_ON_P02. Such an added decision feature would need a different interface and cannot be claimed from finite engine checks.',required=False)
edge('Q1f guarded reason/version composition','Q1c',['P02-QC01','P02-QC02'],'NOT_A_PREREQUISITE',
'T300 parity and pair-profile mixture witnesses are separate targets.',
['Q1f pure reason/version contracts do not depend on T300'],
'Q1c broader partial status neither advances nor blocks Q1f. Optional TRC prerequisites remain P12/DAEE scoped and separate.',required=False)
edge('CV-O optional conditional expectation / martingale proof','CV-R',['P02-R05'],'NOT_A_PREREQUISITE_FOR_FINITE_ENGINE',
'Positive-cell indicators form a supermartingale; a different conditional-expectation martingale separates the extinction residual.',
['Any such infinite stochastic-process formal proof requires exact measure and filtration hypotheses'],
'No martingale or stochastic convergence claim is used to justify a registry commit.',required=False)
for row in entries:
    if not row['required_for_named_P03_target']:
        row['formal_dependency_disposition']='NOT_APPLICABLE_TO_REQUIRED_P03_TARGET'
obj={'schema':'orthemology-p02-p03-statement-reuse-v2','P03_predecessor_sha256':'d984a85387bf15d2da4abfdb388fbeb83a1f27339aa593d7f4123c1569b6e280','P02_predecessor_sha256':'365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9','P02_actual_statuses':receipt['obligation_statuses'],'canonical_dependency_DAG_changed':False,'edges':entries,'remaining_required_P02_ordinary_dependencies':[],'required_new_P02_kernel_imports_claimed':[],'formal_ceiling':'P02 has no new kernel-checked measure/probability declarations. The P03 ordinary theorem does not pretend to import them. A later joint Lean development must prove its actually used measure/table lemmas.'}
(ROOT/'P02_P03_DEPENDENCY_MAP.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'exported_obligations':len(export),'P02_formal_candidates':len(formal),'reuse_rows':len(entries),'P02_statuses':receipt['obligation_statuses']},indent=2))
