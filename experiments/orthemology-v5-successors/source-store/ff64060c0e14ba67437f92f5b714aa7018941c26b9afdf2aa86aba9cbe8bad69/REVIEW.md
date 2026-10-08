# Independent review: source-bound attribution kernel closure

## Disposition and scope

**Accepted for the exact all-parameter A–C targets in SPEC.md**, with the separately bound actual-root corollaries below. No mathematical defect, weakened conclusion, circular hypothesis, custom axiom, or unclosed target remains in this scope. This is an independent correctness review, not an audit-governor release decision.

The review is bound to:

- Central checkpoint `formal/attribution-kernel-closure/checkpoints/central-v1/MANIFEST.json`: SHA-256 `2830c05f25dcda6f05617e6da58bac50eb3ea86cc9671f5b8301417bf2a1d295`.
- Supplement `formal/attribution-kernel-closure/checkpoints/controls-v1/MANIFEST.json`: SHA-256 `f29de5f526216178d1925281eef35a8f8558dc15810b6f7e40428324963f93e4`.
- Unchanged accepted source `delivery/unknown-root-attribution-accepted-v1/PACKET_MANIFEST.json`: SHA-256 `ad4d729f661b5ef8007a42d6b529dfa5fd78423a820cf47f7db43a4edfbf20f5`.
- Accepted general statement: SHA-256 `a59fc17c52c53d341d19fbae37622056b682df5b3b771ddbb8b7ef76bbd28662`.

The exact theorem scope is the sharp robust root-image iff, full actual-root availability equivalence and maximal-taint realization, arbitrary fixed-family feasibility iff, and their representation transport. The supplement derives root-witness equivalence and the sharp actual-root cost. The general q/r formula displayed in the ordinary text is not separately restated as a new named kernel equivalence in these checkpoints; the acceptance here is the explicitly specified A/B/C target statements, not a blanket statement that every sentence of the source has a new formal theorem.

No credit is given here for covering/search optimality, randomized caps, physical cancellation behavior, or temporal/service/authorization applicability. Those claims and retained premises require their separate evidence. No source-attribution oracle, observation extension, adaptive family redesign, root churn, or fixed-R5 enlargement is introduced.

## Cold semantic assessment

### Actual images and exact safety

`rootMap` maps all and only class labels to `none`, and each outside label i to `some i`. `rootImage` is its actual Finset image, and `sharedRoots` is the intersection of two actual images. This is not a disguised label-intersection count.

`sharedRoots_decomposition` proves that the shared image consists of the injectively named shared labels outside A plus a disjoint possible singleton `{none}`. Its condition is that A meets both P and R, including when their label intersection is empty. `cross_image_identity` then derives the accepted equation (1). No cardinality formula is postulated.

`sharp_nonempty_minimum` proves both the universal lower bound and an attaining class, for every finite label type and nonempty intersection. The natural-number expression `s-c+1` is `(s-c)+1`, with truncated subtraction, and is exactly the accepted `max(1,s-c+1)` integer expression. The case split constructs A within the intersection when possible and otherwise extends the intersection to the prescribed class size. The assumptions guarantee existence of the needed subsets.

`forced_bridge_iff` proves the exact complement-size condition; together with `disjoint_zero_fault_iff` it explicitly covers the zero-fault exception. `robust_iff` handles both nonempty and empty overlap. In the latter/small-intersection branch it constructs a c-class containing the whole overlap, leaving at most one shared root, and uses B≥1. The sufficient direction uses the independently proved collapse inequality. It is not a threshold-family-only theorem: P and R are arbitrary Finsets.

### Actual faults and availability

`Available` universally quantifies every c-class A and every finite S contained in `actualRoots A` with `S.card ≤ B`; the allowed F is supplied outside both quantifiers. `taintedLabels` is the literal pullback of S through `rootMap`. `disjoint_image_iff` identifies root-level avoidance with disjointness from that pullback.

`tainted_label_budget` follows from the image collapse bound and image containment. It happens to hold for larger ambient S as well, but the public world contract correctly restricts S to actual roots. `maximal_taint_realizable` constructs a c-subset A of the arbitrary maximal label set T, chooses S to be the image of T, proves that S lies in the actual image, proves exactly B distinct faulty roots, and proves exact pullback equality with T. This is a construction, not an independent-label-fault hypothesis.

`available_iff` uses that realization for necessity and extends each actual pullback to a k-set for sufficiency. Its weaker `k≤m` auxiliary domain is explicit. The central theorem retains the original B<n assumption, which implies the stronger `k<m`. We independently kernel-checked this strict non-saturation and class nonvacuity.

### Arbitrary fixed families and threshold

`FixedFamilyContract` has both availability predicates and safety for every P∈F and R∈G. F and G are arbitrary Sets of finite label subsets, so they permit nonuniform families without encoding a threshold assumption. On a finite label universe these Sets introduce no missing finite-family restriction. The outer existence in `fixed_family_feasible_iff` fixes F/G before all map/fault quantifiers.

The lower proof first obtains P avoiding a k-set, hence `|P|≤m-k`. It chooses U⊆P of size `min(k,|P|)` and uses the other family's availability to obtain R avoiding U. Therefore `|P∩R|≤|P|-min(k,|P|)`. Universal cross safety then forces `m≥3k+1`. This is a valid alternative to the ordinary two-maximal-taint-set obstruction and uses no uniformity, monotonicity, or simultaneous-world assumption.

The upper proof uses every `(m-k)`-subset. Complementation proves availability, and the union/intersection cardinal identity proves sufficient overlap. `fixed_contract_iff` transports both directions back to actual-root safety and actual-world availability; `fixed_family_feasible_iff` retains B≥1, c≥1, c≤m and B<m-c+1.

### Root names, bijection, and accepted representation

`ExactOneClassMap` states exactly the equality-fiber condition: equal images iff labels are equal or both in A. It does not assume the desired image-cardinality or safety result. `canonical_exact` proves that the Option model satisfies it. For an arbitrary decidable root-name type β, `rename_commutes` and `renamed_image` show surjectivity onto every actual image; `rename_injOn` proves injectivity on the actual canonical roots. The map need not be injective on unused ambient names, which is neither required nor correct.

`arbitrary_map_shared_card` transports each shared-image count. Both fault transport directions preserve actual-image containment, exact fault cardinality and label-by-label membership. `arbitrary_map_available_iff` follows from those transfers. We independently constructed a subtype-level bijection between the actual images in `IndependentChecks.lean`, and composed the supplied lemmas into a fixed-family/all-map contract equivalence. This confirms that the abstraction loses no compatible map merely by choosing Option root names.

`Correspondence.lean` imports the byte-identical accepted `UnknownRootAttribution.lean`. It proves that representative encoding commutes with the original `rootOf`, is injective on actual images when the representative belongs to A, and preserves the shared-root count. `booleanLabels_card` derives equality with the exact original recursive `ChargedInterlock.card`, not a replacement cardinal axiom. Every finite label subset is recovered by `setPredicate`, closing the reverse quantification in `old_robust_iff_new`. The final `old_robust_iff` states the sharp result using the original Bool/Nat interface. Independent checks additionally establish original `pulledFault` membership and recursive fault cardinality correspondence.

### Actual-root witness and cost supplement

`root_witness_safe_iff` proves that every ≤B actual fault set leaves a shared untainted root iff the shared-root count exceeds B. Necessity may choose the whole shared image as its fault set, whose actual-image containment is proved. It does not assume a physical veto.

`arbitrary_family_actual_root_lower` derives `n≥3B+2c-1` from the arbitrary-family theorem and actual root count. `sharp_minimum_construction` generically attains that count at `m=3(B+c-1)+1` and establishes the arithmetic difference `2(c-1)` from `3B+1`. This last comparison treats the accepted known-attribution count as the comparison quantity; it does not newly prove its operational applicability.

## Replay and adversarial evidence

Fresh reviewer-owned directories were used. No candidate, accepted-source, dependency, or canonical repository file was edited. No author `.olean` was copied or imported. The new and unchanged legacy modules were compiled from the exact copied `.lean` bytes into an initially empty build directory.

The compiler is official Lean 4.19.0, release commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The Mathlib revision is `c44e0c8ee63ca166450922a373c7409c5d26b00b`, archive SHA-256 `9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425`. All 6,816 archive source files match the installed tree byte-for-byte. The tree was supplied as an archive, not a Git checkout. Existing pinned Mathlib/dependency compiled libraries are trusted dependencies; this review did not rebuild all Mathlib from source.

All 70 accepted packet manifest entries and all central/supplement entries were size/hash verified. Legacy files match their accepted originals. Copies and original freezes were checked again after replay.

`replay-review.sh` successfully compiles:

1. Three unchanged legacy modules, six central modules and all three generic Target tests.
2. The frozen Regression file, including examples beyond the old exhaustive m≤7 range and B=0/c=0/c>m countermodels.
3. Four supplementary generic root-witness/cost theorems and both supplied family-deletion controls.
4. Eight reviewer-written generic transport/nonvacuity/correspondence proofs and seven reviewer-written hypothesis-deletion countermodels.
5. An explicit transitive axiom audit of all 50 central theorems; all dependencies are limited to `propext`, `Classical.choice`, and `Quot.sound`. The supplement and independent proofs likewise have only these standard axioms.

The seven independent deletion controls cover B≥1, c≥1, c≤m, k≤m, the second family's availability, cross safety, and the actual-image restriction for cardinality-preserving fault transport. The supplied stronger family controls also show nonempty-family failure when G availability is removed and failure of diagonal-only safety. Three isolated source mutants are correctly rejected: deleting B positivity, deleting c positivity, and counting labels as separate roots. Their expected-failure logs may mention `sorryAx`; no mutant is part of or imported by any successful proof build.

The successful sources contain no `sorry`, `admit`, custom `axiom`, `unsafe`, `native_decide`, `implemented_by`, or `extern` proof escape. Generic finset constructions prove the central results. Finite `decide` examples are controls only.

## Verification entry-point note

The frozen central `verify.sh` intentionally runs `Target*.lean` and does not run its included `Regression.lean`. The controls supplement supplies that second stage, but its frozen directory expects the original working layout rather than being standalone. This is a reproducibility layout qualification, not a theorem defect. The reviewer-owned `replay-review.sh` explicitly combines the two frozen inputs, exports a fresh isolated build path, runs Regression and all supplementary/independent checks, and keeps expected-failing mutants separate from successful logs. The present acceptance relies on that full replay, not on interpreting central `verify.sh` alone as a full control-suite pass.

## Remaining ceiling

The A–C ordinary-proof gaps identified in the accepted review now have all-parameter kernel proofs under the declared finite static one-class map/fixed-family interface. External physical, temporal, institutional, authorization and observation-boundary premises remain assumptions of applicability. Covering/search closure is outside this review and receives no inferred credit. Any change to either frozen manifest requires a new exact-byte assessment of the changed material.
