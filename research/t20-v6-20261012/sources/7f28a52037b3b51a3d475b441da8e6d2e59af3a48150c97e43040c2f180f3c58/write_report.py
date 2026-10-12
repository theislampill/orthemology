from pathlib import Path
import datetime,hashlib,json,re
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-coded-rule-templates-20261010'
def rec(p):return {'path':str(p.relative_to(W)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
p=R/'REPLAY_RECEIPT.json';r=json.loads(p.read_text());assert r['status']=='PASS';assert len(r['positive'])==15 and len(r['negative'])==24
for p in json.loads((R/'FINAL_REVIEW_PINS.json').read_text()):assert rec(W/p['path'])==p,p['path']
a=json.loads((C/'validation/AUTHOR_REPLAY.json').read_text());assert a['status']=='PASS' and len(a['positive'])==51 and len(a['negative'])==6
out=W/r['fresh_output'];names=json.loads((R/'ALL_HELPER_TARGETS.json').read_text());assert len(names)==833
text=f'''# Independent review: actual Rule arithmetic code maps

## Verdict

PASS for the frozen candidate `hase-coded-rule-templates-20261010`, within the stated canonical-input scope. No candidate defect or required change was found. This review does not establish source-domain validation, the full recursive certificate checker, source derivability r.e., semantic completeness, or T20 closure.

Reviewer: `[OMITTED_PRIVATE_MACHINE_PATH]`.
Author: `[OMITTED_PRIVATE_MACHINE_PATH]`.
Review timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}.

## Frozen subject and source binding

- The eight core files match `CORE_SOURCE_FREEZE.json` exactly.
- The final author input set contains 3,032 pins. The final independent replay verified 3,113 combined source, retained-object, toolchain, prior-review, and control pins before and after execution.
- `CertificateRules.lean` and `generated_rule_metadata.json` still match the original joint-certificate `CANDIDATE_FREEZE.json`; this was independently checked, not inferred from the new candidate's declarations.
- All 63 constructor names, parameter types, parameter ordering, and all 189 conclusion/premises/checkSide metadata expressions exactly match that retained source.
- The untouched generator scripts were run under an isolated, equivalent directory tree. Their three generated modules are byte-identical to the candidate.
- Tags 0–62 are dispatched in the correct order. Each of the 189 branches has its own closed primitive-recursion proof and exactness theorem; the three universal theorems exhaust the real Rule type by cases.

## What the proofs establish

In namespace `CodedRuleTemplates`:

- `conclusionCode : Nat → Nat` is Primrec and equals `encode r.conclusion` on `encode r`.
- `premisesCode : Nat → List Nat` is Primrec and equals `r.premises.map encode` on `encode r`.
- `checkSideCode : Nat → Bool` is Primrec and equals `r.checkSide` on `encode r`.

These declarations have no assumed checker-computability parameters, no replacement source codec, and no source-type Primcodable assumption. The ListNat bridge is the genuine standard list codec transport for every Encodable head type. The side branches call the actual lookup, finite, polynomial, term-scope, and type-scope functions. The finite checker uses the already independently reviewed red/step checker chain; the five actual auxiliary maps and mixed/source-primitive predecessors retain their earlier PASS receipts and frozen inputs.

## Semantic checks

The independent controls cover:

- Sigma branch `[b,a]` orientation, full instantiation of the remaining tail, and pair-substitution offset 2.
- Motive `[e,y]` orientation, no term-variable lift under type-level `all`, and term-variable lift under `pi`.
- Exact theta context order and weakening; section seed/step shifts and the uncurried-step shift; source pairing, projections, J and dependent-step helpers remain universally exact.
- Sigma elimination's actual argument slots, J argument slots, and conclusion J/E tags.
- Source context roots and exact ordered premises for sigma elimination and dependent induction, plus all three J-from-E base rules.
- Both finite J and finite E rules retain every τ image, including unused and duplicate entries, in original order. Dropping unused entries, deleting a duplicate, and reordering distinguishable entries each fail for both rule families.
- Real lookup/poly evidence, finite support checks, and conversion scope cannot be ignored.

There are 28 independently authored source/raw-code theorems. Raw-code equations unfold the actual implementation rather than the candidate's universal exactness theorems. The 24 false code-map assertions reject specifically because the resulting proposition is false, not because of syntax/import errors. Those falsification tests use established exactness where needed to avoid enormous concrete numeral encodings.

A direct fully expanded section-equality negative control did not reduce through the well-founded source abstraction definition. That diagnostic is retained; it is not counted as a rejection or proof. The accepted section control instead isolates the required seed shift, paired with the direct universal raw section equation and the candidate's kernel-checked universal section exactness. No deep concrete-encoding performance claim is made.

## Malformed-code boundary

The independent runtime witness `pack 1 [leaf 99]` gives `(decode Rule ...).isNone = true` while `checkSideCode ... = true`. Thus this side-condition map is demonstrably not a source-domain validator. Unknown tag 63 returns the totalization defaults `(0, [], false)` for conclusion, premises, and side respectively. Exactness is only asserted for canonical Rule encodings.

## Verification evidence

- Lean {r['lean_version']}; every selected compile and negative control used `--trust=0`.
- Independent final fresh replay: 15 modules, including both ListNat transport modules, ConstructorDescriptors/CertificateDescriptions, all six core modules, both author controls/audit modules, independent controls, malformed runtime checks, and the complete helper axiom audit.
- Independently replayed author controls: all 17 runtime values are true; the 22-target audit is standard-only.
- Complete candidate/generic-transport axiom audit: all 833 theorem targets, only `propext`, `Classical.choice`, and `Quot.sound`.
- Independent semantic rejections: all 24 expected false propositions reject.
- Author's separately checked receipt: 51 selected source modules, 6 semantic rejections, and unchanged 3,032 input pins.
- Exact first-resolved imports are recorded. Candidate target outputs are freshly generated and never substituted with prior candidate objects. Upstream retained objects are pinned, with prior independent auxiliary/mixed receipts bound into the review.
- No entire baseline rebuild, protected-source edit, commit, or publication occurred.

## Replay and receipts

Run from the workspace root:

`python hase-coded-rule-maps-independent-review-20261010/verify_review.py`

The script creates a new additive output directory, checks pins before/after, recompiles the 15 selected modules, runs all 24 false assertions, checks all runtime/axiom results, verifies direct import identities, and reruns the original generators for byte parity.

- Final replay: `REPLAY_RECEIPT.json`
- Final review: `REVIEW_RECEIPT.json`
- Frozen review inputs: `FINAL_REVIEW_PINS.json`
- All-source metadata comparison: `GENERATOR_REPRODUCTION.json`
- Original Rule freeze binding: `RETAINED_RULE_BINDING.json`
- Static theorem/dispatch checks: `STATIC_AUDIT.json`
- Fresh output directory: `{r['fresh_output']}`

All claims above are limited to this exact frozen packet and its retained dependencies.
'''
(R/'REVIEW.md').write_text(text)
receipt={'status':'PASS','scope':'All63 actual Rule conclusion/premises/checkSide arithmetic realizers, exact on canonical inputs','reviewer':'[OMITTED_PRIVATE_MACHINE_PATH]','author':'[OMITTED_PRIVATE_MACHINE_PATH]','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report':rec(R/'REVIEW.md'),'independent_replay':rec(R/'REPLAY_RECEIPT.json'),'review_inputs':rec(R/'FINAL_REVIEW_PINS.json'),'candidate_inputs':rec(C/'validation/INPUT_PINS.json'),'core_freeze':rec(C/'validation/CORE_SOURCE_FREEZE.json'),'author_replay':rec(C/'validation/AUTHOR_REPLAY.json'),'source_binding':rec(R/'RETAINED_RULE_BINDING.json'),'generator_parity_and_metadata':rec(R/'GENERATOR_REPRODUCTION.json'),'static_audit':rec(R/'STATIC_AUDIT.json'),'trust':0,'lean_version':r['lean_version'],'independent_fresh_modules':15,'independent_positive_theorems':28,'independent_false_assertion_rejections':24,'all_candidate_and_generic_transport_axiom_targets':833,'author_runtime_values_independently_checked':17,'author_final_audit_targets_independently_checked':22,'pins_verified_before_after':3113,'all63_rules_and_189_map_branches':True,'all_J_and_E_tau_images_preserved_in_order':True,'actual_auxiliary_maps_instantiated':True,'malformed_boundary_explicit':True,'entire_baseline_rebuilt':False,'protected_or_candidate_inputs_changed':False,'findings':[],'whole_checker_computability_proved':False,'source_derivability_RE_proved':False,'T20_closure':False}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
files=[]
for f in sorted(R.rglob('*')):
 if f.is_file() and f.name!='REVIEW_MANIFEST.json':files.append(rec(f))
(R/'REVIEW_MANIFEST.json').write_text(json.dumps({'status':'SEALED','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files},indent=2)+'\n')
print(json.dumps({'status':'PASS','report':rec(R/'REVIEW.md'),'receipt':rec(R/'REVIEW_RECEIPT.json'),'replay':rec(R/'REPLAY_RECEIPT.json'),'manifest':rec(R/'REVIEW_MANIFEST.json')},indent=2))
