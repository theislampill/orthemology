# Independent review: actual Rule arithmetic code maps

## Verdict

PASS for the frozen candidate `hase-coded-rule-templates-20261010`, within the stated canonical-input scope. No candidate defect or required change was found. This review does not establish source-domain validation, the full recursive certificate checker, source derivability r.e., semantic completeness, or T20 closure.

Reviewer: `private-locator:af5d71717f145b0f2809`.
Author: `private-locator:b666aef3749a95964e8c`.
Review timestamp: 2026-10-10T19:57:18.281878+00:00.

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

- Lean Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release); every selected compile and negative control used `--trust=0`.
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
- Fresh output directory: `hase-coded-rule-maps-independent-review-20261010/fresh-replay-puvxgby5`

All claims above are limited to this exact frozen packet and its retained dependencies.
