# Independent acceptance: bounded unknown-root-attribution extension

Reviewer: `review_dynamic_repair_proofs`. Completed: 2026-10-02 UTC.

## Disposition and exact boundaries

**ACCEPTED AS A CONDITIONAL FIXED-FAMILY MATHEMATICAL EXTENSION.** No required correction or unresolved review finding remains.

This acceptance binds two immutable source boundaries:

1. Ordinary theorem, finite controls and dependency binding: `../attribution-author-freeze-v1/FREEZE_MANIFEST.json`, SHA-256 `f99ef03c66d51eb5689f8eff1fcd7af6c2430e7fa8fab78434fa1fdb5a77eae1`.
2. Additive formal component: `../attribution-formal-addendum-v1/FORMAL_MANIFEST.json`, SHA-256 `4c0af26b40c1e7f16a37af2bf63d5705f12c09fea1c88375bb7fe1d13b274623`.

New Lean source: `UnknownRootAttribution.lean`, SHA-256 `cbf291fec343e9b9e9eb62cacf9dbef810541f8b0d729a7c077b1ef62cd03b7b`.

The complete ordinary proof assessment is in `ORDINARY_REVIEW_V1.md`. Its conclusions stand without correction after review of the additive formal component.

## Accepted result and its ceiling

For m labels with exactly one unknown static c-label root class, all other roots singleton, and `c≥1`, `B≥1`, `B<m−c+1`, put `k=B+c−1`.

- Universal actual-root overlap greater than B is exactly label intersection at least `k+1`, including the forced-bridging corner.
- Every maximal k-label taint set is realized by one fixed compatible map and exactly B actual fault roots.
- Arbitrary fixed observable repair/revocation families, with every allowed pair required safe in every compatible world and both families universally available, exist exactly when `m≥3k+1`.
- At the minimum, uniform `q=r=2k+1` works, cancellation requires `k+1` labels, and the exact opaque macro-attempt optimum is `choose(3k+1,k)`.
- The general uniform-path optimum is `C(m,m−q,k)`.
- The minimum actual-root count is `3B+2c−1`, an additional `2(c−1)` actual roots relative to known attribution at the same B in this interface.

The lower bound uses a complete admissible common failed transcript, including preparation/cancellation content and timing. It does not prove that aliasing is unlearnable through richer experiments. Partial-control probes, extra identity evidence, internal gate-state readout, out-of-path old-command queries, physical side channels and adaptive family redesign are expressly outside acceptance.

All v2 external applicability premises persist: correct actor scheduling, root-coherent live gates/tombstones, full-command authentication/binding, independent control access, bounded service, actual reservation/cleanup rights, stable descriptor delivery, a sufficiently long authorized quiescent suffix and lifetime-union fault accounting. Neither the arithmetic nor this review proves those world facts. No fixed-R5 enlargement or defeat is established.

## Exact Lean coverage

Cold reading confirms that the new formal source proves the claims actually advertised in its additive manifest:

- `tainted_label_budget`: a root map collapses the class to one representative; at most B faulty root indices pull back to at most `B+c−1` tainted labels.
- `sound_unknown_map_overlap`: the sufficient sum threshold `m+(B+c−1)<|L|+|S|` supplies a shared label whose actual root is untainted. This is the uniform-threshold sufficient implication, not a formalization of the complete sharp arbitrary-set root-image iff.
- `sound_unknown_map_cancellation`: more than `B+c−1` acknowledger labels supply at least one untainted actual root. The enduring physical-veto conclusion is obtained only with the retained gate/tombstone contract.
- `realization_labelwise` and `realization_root_cardinality`: when a positive class A is contained in a maximal taint set T, choose its representative and taint it plus singleton labels in T\A. The pullback equals T pointwise and the chosen fault set has cardinality B. Existence of the c-subset/representative for every maximal T remains the elementary ordinary construction.
- `exact_minimum_actual_root_count` and `threshold_actual_root_lower_bound`: the numerical translation from label-threshold minimum to actual-root count. The full arbitrary-family lower-bound quantifier argument is not encoded by these arithmetic lemmas.

Actual roots are represented by label indices outside A together with one representative in A. Unused alias indices need not be counted as fault roots in an application; the upper-bound lemma is conservative even if its general predicate contains such unused indices. The explicit realizing predicate uses only actual representative/singleton indices.

No custom axiom, `sorry`, `native_decide`, or unsafe definition is present. Printed dependencies are ordinary Lean logical axioms (`propext`, `Classical.choice`, `Quot.sound` as applicable). The sharp forced-bridge iff, full nonuniform-family impossibility and general covering/randomized search argument remain ordinary proofs, as the author states.

## Replay evidence

All nine ordinary manifest entries and seven formal-addendum entries were size/hash checked. Parent v2 manifest and independent-review hashes match the dependency binding. Both author source boundaries were checked again after replay and remained unchanged.

Reviewer-owned copies were used exclusively. The finite checker exited zero, and both generated JSON outputs match the frozen author outputs byte-for-byte. The reviewer's separate explicit-partition checker, which imports no author functions, passed 2,353,056 root-image pair cases, 417,488 positive-B equivalences, 5,556 map/fault instantiations, 741 canonical maximal-world realizations and 56 obstruction parameter cases for m=2…7; it also verified a zero-fault forced-bridge exception.

Official Lean 4.19.0 (release commit `6caaee842e94`) successfully compiled, in order:

1. Exact accepted-v2 `DynamicInterlock.lean` into the review build directory.
2. Exact accepted-v2 `CoveringCore.lean` using that dependency.
3. Frozen `UnknownRootAttribution.lean` using those two compiled dependencies.

All three compiler logs match author bytes. Official executable SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

Evidence is retained in `finite-replay.log`, `formal-replay-logs/`, `INDEPENDENT_ROOT_IMAGE_RESULTS.json` and `INDEPENDENT_REVIEW_RECEIPT.json`.

Enumeration counts are bounded test cases, not general proofs; duplicate representations for c=1 are not distinct physical worlds. Kernel compilation verifies the listed formal propositions, not the entire operational/physical interpretation. Any subsequent source change requires a new digest-bound review of the changed material.
