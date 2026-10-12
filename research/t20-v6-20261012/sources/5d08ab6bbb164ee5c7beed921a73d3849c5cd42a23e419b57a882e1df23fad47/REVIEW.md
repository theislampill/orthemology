# Independent review: actual auxiliary checker code realizers

Disposition: PASS for the frozen packet's stated scope. No correctness finding remains. This review provides evidence to the parent; it does not authorize source integration or closure of the larger audit.

Candidate: `hase-auxiliary-checker-computability-20261010`.
Author: `private-locator:effefec49e9dbafdc7c3`.
Reviewer: `private-locator:b4fbebf561863267ef8e`.

## Verified evidence

- Fresh Lean 4.19.0 `--trust=0` compilation of the actual retained `AuxiliaryCertificates.lean`, three grammar modules, and all 13 candidate modules: 17 selected modules total, without errors, warnings, or `sorryAx`.
- The separately PASS-reviewed mixed-transformation outputs were reused with exact object pins and receipt binding. No large baseline rebuild was performed.
- All six author false controls were independently rejected with the intended Lean diagnostic.
- Added 38 source controls importing only the actual retained checker source: equations for all 24 constructors and 14 concrete/nested semantic controls. They cannot invoke candidate checker exactness.
- Added 55 direct code controls: shape and child equations for all 24 constructors; five complete evaluator reductions; a Lookup successor recurrence; and two successor layers enforcing three weakenings. These proofs unfold code definitions and codec arithmetic, never rewrite through the candidate checker exactness theorems.
- Added ten independent false source mutation claims and five false code-child-layout mutations. Every one rejected because `decide` proved its proposition false; parser, missing-name, or import failures are excluded as rejection evidence.
- Ten explicit interface guards verify genuine root-qualified Mathlib `Primrec`, right-nested Nat tuple order, and canonical exactness against each actual `AuxiliaryCertificates.check…` definition.
- All 83 explicitly named candidate helper theorems were axiom-audited. Every dependency is within `propext`, `Classical.choice`, and `Quot.sound`.
- Exact first-resolved direct import objects are recorded in `EXACT_IMPORT_GUARDS.json`; every retained object must match an input pin. All 2,907 candidate pins and 27 initial review-boundary pins were checked before and after. The completed author receipt is separately frozen and checked at sealing.
- Candidate sources, protected inputs, source encodings, and the large retained baseline were not modified.

## Semantic inspection

The candidate retains the real source certificates and canonical encodings. Constructor-code identities are proved by `rfl`, including leaf-wrapped fields from external sorts and direct recursive fields from the same certificate sort.

Step covers I, K, S and both contextual directions. Contextual certificates require the child to prove the declared endpoints; matching outer application endpoints alone does not pass.

Red checks the actual Step certificate from the declared start to the intermediate term, then the actual recursive Red certificate from that same intermediate term to the target. Neither the outer endpoints nor independent accepted fragments can bypass that junction.

Poly covers all eight constructors. Symmetry swaps outer endpoints but checks its child in the original orientation. Transitivity requests the same middle polynomial from both children. Application congruence separates function and argument proofs. The bridge is directional and distinguishes an atom containing a Term application from a Poly application of two atoms.

Finite covers I, K, S, application, allI, allE, and reduction. Application requests an arrow-typed function and an argument of the same declared domain. allE uses the actual retained `TypeCode.instantiateType`; its code API has the expected image/body order. A nested quantified identity witness confirms capture-avoiding shift of the open substitution image. Reduction checks both the original typing derivation and the actual Red certificate with the same source and target terms.

Lookup checks the entire encoded telescope, index, claimed type, and actual `wk`. The successor child is checked against its declared smaller telescope, original index, and pre-weakening type. A source witness with open identity endpoints and two successor layers accepts exactly three weakenings, rejects a missing weakening, and rejects a permuted context. The direct code recurrence independently confirms that repeated weakening is enforced rather than inferred from candidate exactness.

The primitive-recursive witnesses are ordinary Mathlib primitive recursion/composition on natural-code data, using the frozen bounded dependency evaluator. The exactness inductions establish strict code decrease of each recursive certificate field through `field_lt_pack`. The predecessor TypeCode instantiation and Ty weakening realizers were independently reviewed and are pinned. No generic Encodable-to-Computable implication, replacement codec, source Primcodable instance, executable-to-PR inference, or whole-checker hypothesis appears.

## Limits

Exactness is only claimed on genuine encoded inputs. Malformed natural-number inputs may have arbitrary totalized behavior. The candidate's deliberate malformed-polynomial countercontrol demonstrates that these functions are not standalone code-domain validators; a serialized checker needs separate canonical-image gates.

This review does not establish whole Joint/E checker computability, source derivability being r.e., the final reduction, source integration, publication, active rule-template correctness, or T20 closure. Negative controls are discriminating examples, not exhaustive mutation testing.

Exact hashes, commands, source/object/log records, import guards, and the accepted boundaries are in `REVIEW_RECEIPT.json` and `SELECTIVE_REPLAY.json`.
