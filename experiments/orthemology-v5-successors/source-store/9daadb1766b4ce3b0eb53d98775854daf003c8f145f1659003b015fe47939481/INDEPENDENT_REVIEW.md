# Independent review: grounded attestation and continuation

Disposition: PASS within the stated formal and finite-test scope. No blocking finding. This is an independent machine-assisted proof/source review, not external human or empirical validation.

Frozen candidate: `SOURCE_MANIFEST.json`, SHA256 `75528460e5853d4f4265fd1e4bf06cf08cf6d041157845e37a2e7ad6482439d1`.

## Verification actually performed

- Read the README, complete written proof, theorem map, plan, all six mathematical Lean modules, generated readback, author validation receipt, test/search implementations and enumeration output.
- Verified every one of the 15 manifest-bound files before and after review. Also bound and rechecked the author readback, receipt, declaration list, dependency/import receipts, search result and initial-red log. No source or author output was modified.
- Freshly compiled GroundedSupport, GroundedQuotient, AliasCuts, OccurrenceControls, CutControls and MutationControls using the existing Lean 4.19.0 release into this review's own initially empty object directory. Custom imports resolve only to these fresh objects. The exact 39-declaration type/axiom readback is byte-identical to the author's readback.
- Rehashed the existing 1,365 bound dependency objects, 806,871,632 bytes, against binding manifest `36a363d2306ad5892338e820212aa766ea8a9721c20c21be5bdd155c2778fcdf`: no mismatches. This is dependency-byte reuse, not a compiler bootstrap, cold dependency rebuild or predecessor-science replay.
- All six mathematical sources are free of `sorry`, `admit`, `native_decide` and custom `axiom` declarations. Exact declared dependencies are recorded per theorem in `EXACT_AXIOMS_AND_IMPORTS.json`; their union is precisely `propext`, `Quot.sound`, `Classical.choice`.
- Replayed the author's seven Python tests and alias search on copied Python inputs, keeping generated output outside the frozen packet. Independently reproduced the finite results with a separately written integer-bitmask oracle that does not call the author's cut, minimization, partition or search helpers.

## Exact finite coverage

The 2,325 rule systems are all selections of zero through three distinct rules from 24 possible rules over three claims, with two roots and fixed base relation {(0,0),(1,1)}. The count is C(24,0)+C(24,1)+C(24,2)+C(24,3). Four availability subsets per system give 9,300 profiles. Both support minimality and availability/closure agreement were checked. This is not enumeration of all rule systems, base assignments or finite sizes.

The alias search covers nonempty antichains of nonempty supports on 1–4 labelled elements, including unused labels, paired with every set partition of the full label universe. Counts by size are 1×1=1, 4×2=8, 18×5=90 and 166×15=2,490, totaling 2,589 cases. Full inclusion-minimal-cut transport passed in every case. Strict minimum-cardinality-first cost errors are 0, 0, 0 and 40. The independent oracle confirmed each number.

Ten additional independent checks cover empty families, empty supports and redundant/dominated supports omitted from the author's alias search. Other discriminating checks cover alternative derivations versus their flattened union, the requirement for saturated availability after aliasing, and the stated four-label example.

## Mathematical and interpretive findings

1. **Grounding and exact survival.** `Derivable` is an inductive, finitely branching derivation relation; a cyclic rule graph alone supplies no derivation. Nullary rules remain allowed and have an explicit soundness burden. `exists_minimal_subset` needs only a finite satisfying set, not finite ambient types or a finite rule relation. Retraction uses finite U and removal sets, with meanings/base/rules unchanged. Global inclusion minimality on a subset of U is equivalent to minimality within U. The two directions of `derivable_after_retraction_iff` establish the claimed exact availability condition.

2. **Truth is conditional.** `derivable_sound` requires both sound available primitives and truth-preserving selected rules. There is no converse completeness statement. Loss of all modeled derivations does not imply falsehood, invalidate an immutable historical assertion, or exclude other epistemic routes. The review added and compiled an explicit underivable-but-true-interpretation control.

3. **Faithful quotient transport.** `QuotientBase` retains the label-to-claim relation, bounded by U. Available actual roots expose all and only their labelled primitives in U. This saturation is indispensable: retaining an arbitrary single alias can lose premises. A fixed map need not be injective or surjective. The theorem neither discovers/authenticates it nor claims independent carrier failures vanish when their source is shared.

4. **Archive order and minimality.** Image/pullback proofs are correct for an arbitrary finite bounded support family, without an antichain or nonemptiness assumption. Root-minimal cuts lift from inclusion-minimal label cuts. The root-minimality equivalence then correctly discards nonminimal images. The label archive predicate is independent of the map. The review additionally compiled `archive_before_origin`, explicitly constructing a finite archive under ∃ archive, ∀ later origin-map quantifier order. No cheapest-label-cut sufficiency is smuggled into that statement.

5. **Counterexamples.** For supports {a1}, {a2,b}, {a3,b}, the unique cheapest label cut is {a1,b}; its image costs two roots. The other inclusion-minimal label cut {a1,a2,a3} maps to the unique optimum {a}, cost one. Both the Lean kernel controls and independent bitmask check verify this, so it is not a tie-breaking artifact. K3,2 is a second compiled control. The written at-most-three-label argument is valid with one implicit trivial branch made explicit: if the two-root quotient optimum already costs two, every mapped label cut costs at most two and at least that optimum, so no strict error is possible. Only the optimum-one case needs the paired/singleton argument. This is explanatory completion, not a counterexample or a new general kernel theorem.

6. **Occurrence, force and time.** In the fixed fixture, prospective revocation deletes only the current grant; it preserves historical standing and source evidence. Evidence invalidation is a distinct operator that explicitly preserves the live grant. Current applicability is required for present action, while the historical duty can remain derivable without it. Authorship alone does not suffice, and three deliberately weakened rule systems constructively derive the respective baseline-excluded conclusions. These are stipulated symbolic distinctions; they do not authenticate an actual messenger, establish actual jurisdiction, or carry out a physical action.

## Independent controls and limits

Five new review-only Lean theorems compiled on their first attempt: archive selection before any origin map; no cut for a family containing empty support; the unique empty cut for an empty family; explicit nullary rules having empty support; and an underivable claim having a true interpretation. Their axiom readback uses only the same standard three-axiom set.

No general refinement theorem connects `grounded_support.py` to Lean. No algorithmic complexity result, arbitrary nonmonotone calculus, unresolved-map robustness, changing-map dynamics, physical continuation or actual metaphysical premise is established. The seven tests and finite enumeration are bounded implementation evidence, not replacements for such theorems.

The prior-ownership ceiling is respected: T6 owns the prior root-cut/transversal and copied-root work; T7–8 own alias image/cost and shared-store distinctions; T9 owns the prior join, reacquisition and all-query bounds. The accepted increment is the scoped grounded-inference/source-force-time/retraction integration and the concrete unsafe summarization order. Horn/provenance/hypergraph methods are established mathematics, not discoveries credited here. Primary-source page accuracy and external specialist judgment were not revalidated in this formal review.

## Preserved failures and custody

The author's initial anchor-propagation failure is preserved as `logs/author-initial-red-preserved.txt`; preservation does not independently establish its development chronology. All fresh candidate builds and Python replays passed on the first review attempt.

The review's own final-evidence checker initially used textual path-prefix comparison, which falsely classified the sibling `grounded-attestation-independent-review` directory as being inside `grounded-attestation`. The failing script/output and a two-case diagnosis are preserved. The corrected check uses resolved path containment; its next run passed. This was a reviewer harness failure, not a candidate proof/import failure, and no candidate source was changed to repair it.

Final source identities, dependency rehash, exact axioms/imports, replay statuses, independent finite checks and control logs are bound by the machine-readable receipt and output manifest in this directory.
