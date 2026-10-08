# Independent technical review: generic covering and opaque repair search

## Disposition and exact subject

**Accept the specified conditional covering/search kernel closure in central-v2, subject to the retained source-model premises below.** This is a technical proof and semantic-correspondence review, not governor/audit closure authority, and adds no mathematical novelty claim.

Reviewed immutable checkpoint:

- `tranche7-restart/formal/covering-kernel-closure/checkpoints/central-v2`
- `MANIFEST.json` SHA-256: `4b93bf89047342432837405ffacbff321da5c45f9bbc48e41ab58b2a173d0815`
- 73 manifest entries, with the exact file inventory checked.

The cold review began at central-v1, manifest `6aed0af13453d9e99bf0bb3e426d4e09639401e54cbccad6780af0b57c71d208` (68 entries). V1 is preserved. V2 adds an explicit defective-start state bridge and strengthens a deletion control. All ten original main Lean sources and both copied attribution dependencies are byte-identical between the checkpoints. `V1_V2_DELTA.json` records the complete inventory difference.

No blocking mathematical or source-interface error remains in v2. Two pre-acceptance matters were resolved:

1. **Objective correspondence, reviewer requested.** A successful path/intervention is not the same as target-state achievement from an already-correct initial state. V2 states the defective-start lower-bound restriction, proves the identity-or-repair coordinate bridge, and proves the zero-attempt initially-correct case.
2. **Deletion-control quality, author identified during the cold review.** V1's opacity-to-`True` mutation failed too early at binder inference. V2 uses a well-typed reflexive equality that removes observation information; the compiler reaches and rejects the intended observation-equality obligation. The main kernel proof did not change.

## Evidence custody and independent replay

The reviewer verified the immutable manifest before replay and rechecked it afterward. Source hashes are checked against the actual accepted originals, not merely against copies that agree with each other:

- All 70 entries of the accepted unknown-root extension manifest were rehashed. Its manifest digest is `ad4d729f661b5ef8007a42d6b529dfa5fd78423a820cf47f7db43a4edfbf20f5`.
- All 31 entries of the accepted attribution central-v1 dependency checkpoint were rehashed. Its manifest digest is `2830c05f25dcda6f05617e6da58bac50eb3ea86cc9671f5b8301417bf2a1d295`.
- Every source copy listed in `SOURCE_BINDING.json` was compared to the original bytes. Both `RootImage.lean` and `Availability.lean` were compiled from those exact copied source files into the reviewer's fresh output directory.
- Official Lean 4.19.0 reports release commit `6caaee842e94`; executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- Mathlib is `c44e0c8ee63ca166450922a373c7409c5d26b00b`. All 6,816 source/archive files match the pinned archive, SHA-256 `9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425`.
- Existing third-party compiled Mathlib/dependency libraries were reused. No accepted source or dependency was edited; no dependency installation/update occurred. No author-generated local proof `.olean` was imported.

`replay_review.sh` requires a fresh output directory, verifies binding before and after execution, runs the frozen author replay, compiles the reviewer's independent theorems and full axiom audit, exercises six additional primary-interface mutants, and runs independent Python controls normally and under `python -O`. The two semantic outputs and the before/after bindings must be byte-identical. It also rejects warnings, errors, or `sorryAx` in successful proof logs. Deliberately rejected mutant diagnostics are kept separate.

The author's `verify.sh` itself validates bound inputs and compiles source but is not a substitute for checking the enclosing central manifest. The reviewer wrapper performs that enclosing immutable-checkpoint check explicitly.

## Mathematical and semantic correspondence

### 1. Complementary portfolios and a true minimum

`CoveringPortfolio.lean` defines availability by avoidance of every maximal bad-label set and a cover by containment of each such set. `complement_portfolio_iff` proves the elementary equivalence; complementation is involutive and injective, so it preserves family cardinality. `portfolio_cover_sizes_iff` relates all attainable cardinalities, not just one witness. `least_portfolio_eq_coveringNumber` therefore compares the same minimization problem.

The covering number is the natural-number infimum of actual uniform finite covering-family sizes. It is not an axiom naming the desired attempt bound. `all_blocks_cover` constructs a feasible family using subset extension, and `coveringNumber_attained` proves that the infimum is attained when `k ≤ b ≤ m`. Those existence/attainment premises are visible. The empty-infimum convention outside feasible parameters is disclosed and is not used as a feasible optimum.

`LabelTransport.lean` proves equivalence transport for arbitrary finite label universes and connects this definition to numeric `C(m,b,k)`. This is genuine label-set transport, not a proposed renaming of policy nonces or a finite numeric case check.

For `b=k`, containment between equal-size finite sets forces equality. `self_blocks_forced` consequently identifies a cover with the full family of k-subsets, and `coveringNumber_self` gives the binomial count. The minimal-label specialization `m=3k+1, q=2k+1` follows arithmetically. No search enumeration substitutes for this general proof. The separate small values such as `C(9,4,2)=8` remain outside this newly mechanized scope.

### 2. Arbitrary full commands, histories and adaptive failure spines

The primary lower-bound interface is `OpaqueActions.lean`, not the simpler path-only adapter. `Action` and `Obs` are arbitrary types. A support extractor selects the label set, while a policy consumes the entire list of preceding **full actions and full observations**. The world observation function can depend on the full prior history and submitted action. Thus bodies, recipients, selected paths, arbitrary nonce choices, preparation and cancellation messages, and logical timing coordinates can be represented without discarding them.

The `admitted`/uniformity premise fixes the allowed support family. It does not fix the order of queries. The reviewer's `any_uniform_action_policy_lower` additionally derives the lower bound for any policy whose supports all have cardinality q by embedding them into the full q-subset family. The source's fresh-command policies are included; the generic lower theorem does not pretend that an arbitrary nonce policy can be renamed to ordinal nonces without loss.

`Actions.Opaque` restricts replies only when the candidate T is compatible with the complete failed prefix through the current trial. It requires no observation equality after a hit or on a prefix already incompatible with T. Equality of actual and failed histories, and the first-hit/portfolio equivalence, are then proved. They are not placed into the definition as desired conclusions.

The all-failure-spine portfolio has at most N distinct supports after N attempts, including policies that repeat paths or choose later commands adaptively. Success in every maximal world therefore makes that portfolio an available family, yielding `C ≤ N`. `SuccessWithin` uses `i < N`, so N counts exactly N macro-attempt opportunities, with no off-by-one slack.

The reviewer supplied kernel examples in which opacity holds while replies differ on unreachable histories and on a reachable post-success failed trial. These check the intended restricted opacity boundary rather than silently accepting a stronger global observation-homogeneity condition.

### 3. Upper attainment and fresh commands

A minimum available portfolio is obtained from the attained minimum cover. Its enumeration is one attaining strategy; the lower bound does not restrict competing strategies to that enumeration.

`FullCommandInterface.lean` binds a selected `Path F`, nonce and repair body in a single command value. `fullCommand_root_world_cap_attained` proves one fixed body is preserved, the actual nonce at attempt n is n, and some untainted support is tried within the covering number. This proves actual freshness of the constructed commands, rather than a nonce-renaming claim. The policy ignores observations, so it does not depend on a trusted success receipt or terminate early on an untrusted success label.

The all-intact support is a sufficient success condition for the upper bound under the retained service contract. Tainted paths that happen to succeed improve that bound. The theorem counts completed macro-attempts at the source interface; it does not newly prove physical cancellation, phase service, or the conversion to three logical phases per trial.

### 4. Genuine fixed-map actual-root worlds

The source comparison uses the accepted `GENERAL_UNKNOWN_CLASS_THEOREM.md` Theorems B and E and the base `COVERING_TRADEOFF.md` Section 1. A label T of size `B+c−1` is realized by the accepted kernel's actual root map: one c-label class maps to the alias root, while outside labels map to singleton roots. `maximal_taint_realizable` supplies one class A of size c and one actual-root fault set S of size B with `taintedLabels A S = T`.

This is the required quantifier bridge. The argument never promotes label-authentication to independent-root authentication, nor assembles faults from incompatible maps into one world. `available_source_iff` and the upper theorem handle every actually tainted root set of size **at most** B by extending its label preimage to a maximal T. The lower witness has exactly B actual roots and a single static map.

The source's admissible homogeneous failed transcripts still need the retained protocol justification: fresh complete-command cancellation, coherent roots, a quiescent suffix, fixed map/fault horizon and no additional probes. An arbitrary symbolic common payload does not itself prove cryptographic authenticity, coherent hardware behavior or physical admissibility. V2 discloses this distinction accurately.

### 5. Randomization: one fixed world, almost-sure caps and probability corners

The measure μ is fixed across all worlds; only the policy depends on the complete coin outcome. The finite family of maximal T permits an intersection of finitely many conull success events. On a probability space this common conull set is nonempty. A seed in it would yield the prohibited deterministic smaller cap.

In `Actions.randomized_below_cover_fixed_root_world`, the existential class A and fault set S precede the almost-everywhere coin quantifier. The conclusion is one fixed realized root world for which the cap fails on a non-null set of seeds. The adversary does not receive the realized private coins. The reviewer's `fixed_root_world_positive_outer_measure` independently converts this exact statement to explicit strictly positive failure outer measure.

The source also gives the finite-averaging bound. The packet's probability utility proves `1 / |W|`; the reviewer's `fixed_root_world_quantitative_failure` instantiates it for all k-subsets, proves their count is `choose(m,k)`, and then realizes the chosen T by A,S. It produces the bound `1 / choose(m,B+c−1)` for **one fixed actual-root world** outside the coin quantifier. The explicit `k ≤ m` premise ensures a nonempty candidate family and a nonzero binomial denominator.

Arbitrary predicates need not be measurable, so numeric measures here are outer measures. With measurable failure events the same bounds are ordinary probabilities. The almost-everywhere statements themselves are correctly formulated without adding an unmentioned measurability assumption. Removing `IsProbabilityMeasure` is not innocuous: the zero measure makes every cap almost-everywhere true. This is both a kernel control and a rejected primary-interface deletion.

This is a worst-case almost-sure cap theorem, **not** an expected-attempt lower bound. Uniform permutations of the four minimal paths have fixed-world expected attempts 5/2, but a.s. cap 4; each fixed world still fails a cap of 3 with probability 1/4. Both author and reviewer finite controls verify that distinction.

### 6. Nonempty candidates and the defective-start objective

`available_nonempty` uses `k ≤ m` to produce an actual maximal candidate and hence a member of any available family. This justifies enumeration rather than silently choosing from an empty portfolio. Independent generic tests prove a feasible cover has positive size, including k=0. Even the empty universe has one empty maximal world and one empty-block cover; if `k > m`, there are no such worlds and the feasible-source claim does not apply. Physical applications separately retain the source's q≥1 and threshold conditions.

`SuccessWithin` denotes a successful intervention/hit. V2's `RepairState.after_true_iff` proves that a canonical identity-or-repair target coordinate is true after N attempts iff it was initially true or a hit occurred before N. `defective_start_iff_successWithin` therefore supplies the precise defective-start interpretation. `correct_start_already_done` proves target achievement at zero attempts from an already-correct state. The reviewer also compiles `defective_target_cap_lower`, combining the bridge with the unrestricted full-action lower theorem.

The source's initially defective canonical lower-bound world is thus retained. No positive target-achievement lower bound is asserted for an initially correct plant. The upper construction remains valid from any safe initial state under the accepted adequate-repair-or-identity contract. The Boolean bridge is deliberately a target-coordinate model, not a replacement proof of the full physical state machine or safety against absorbing damage.

## Verification and controls

The successful replay compiles 11 new main modules, two exact copied attribution dependencies, and four author statement/control modules. An independent audit prints axioms for all 100 declared definitions/abbreviations/theorems in the 11 main modules. Its results contain only `propext`, `Classical.choice`, and `Quot.sound`, or no axioms. No custom desired-bound axiom, `sorry`, `admit`, `native_decide`, or unsafe implementation is present in the accepted proof sources.

The reviewer adds generic proofs and concrete kernel boundary controls in `IndependentChecks.lean`, including:

- positive feasible covering number and nonmaximal-taint extension;
- zero-attempt, empty-universe and impossible-world corners;
- zero-measure vacuity;
- explicit positive and quantitative fixed-realized-world failure measure;
- arbitrary uniform-support full-action policies;
- defective-target lower-bound transport;
- reachable post-success and unreachable-history opacity boundaries.

The author six-mutant suite passes with its repaired opacity control. The reviewer additionally rejects six disposable mutants focused on the primary interfaces: erase full-action opacity information, remove the probability premise, strengthen the lower inequality to a false strict bound, reuse nonce zero in the upper policy, omit maximal covering worlds, and replace exact block uniformity with an overlarge bound. The corresponding compiler diagnostics reach proof/type obligations rather than import or syntax failures. Rejected mutant files are not trusted proof dependencies; their expected `sorryAx` diagnostics do not enter successful builds.

Independent Python checks cover seven small exact covering values, all 341 failure sequences of length at most four at the four-path minimum, 6,706 complete-command adaptive traces, and 13,412 identity/repair state cases. The trace policy uses full prior actions/replies and genuinely fresh, nonordinal, history-dependent nonces; the repair body remains fixed. It includes actual correlated-root realizations for `(m,B,c)=(7,1,2)`, and computes a fixed-world failure probability after integrating over seeds. A richer failed-root disclosure protocol achieves two rather than four attempts, demonstrating why such map/fault information lies outside the opaque theorem. These finite controls corroborate the general proofs; they do not replace them.

## Scope ceiling retained after acceptance

This review accepts the generic mathematical covering/search closure at its declared observation and execution interfaces. It does not establish physical interlocks, non-bypassability, actual root attribution/coherence, authentication, authorization or cleanup rights, independently bounded control ports, cancellation efficacy, stable delivery, phase duration, residual-old-work accounting, enough remaining horizon, or absence of unmodeled observation channels. Those are the accepted source's separate applicability premises.

There is no discovery-of-map theorem, no dynamically learned/rebuilt-family generalization, no partial-cancellation or out-of-path probing result, no unrestricted mobile-fault claim, no new independent-label fault model, no expanded R5 resource claim, no N2/T0/metaphysical source conclusion, and no whole-program closure claim. Within that ceiling, the source-to-kernel correspondence is adequate and the requested covering/opaque-search gap is closed.
