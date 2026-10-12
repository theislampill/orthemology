# Orthemology formal qualification audit

## Assessment

The repaired P01, P02 and P03 research shadows support their bounded mathematical claims. This review found no critical or high-severity soundness defect in the inspected repairs or the final qualified declarations. Independent compiler readbacks and fresh builds confirmed the reported acceptance and axiom ceilings. Several boundaries are mathematically essential; crossing them would produce unsupported claims.

The clearest new negative result is operational: an accepted source proof with 7,916 input nodes requires 1,022 units of constructor-export work and is refused by the actual 512-unit exporter. Source acceptance therefore does not establish total export. P03 now includes an explicitly partial export theorem and a kernel-checked version of that counterexample.

This assessment concerns identified shadow sources and research extensions as inspected on 30 September 2026. It does not adopt them into the canonical repository, claim external human refereeing, establish historical source identity, or conclude the wider research campaign.

## Scope and verification

The canonical checkout remained at main commit 03e2604dfcef278b01c60d19b05370fcec4194b6 with no tracked changes when checked. The review used the supplied Lean 4.19.0 installation, commit 6caaee842e94, with the pinned Mathlib revision c44e0c8ee63ca166450922a373c7409c5d26b00b. It did not independently audit the Lean implementation or reproduce the external release supply chain.

- P01: all 507 immutable input files were independently rehashed; all 31 compiled artifacts were matched to strict-0004; every copied candidate source matched the current shadow. The complete 382-target audit was rerun with exit zero and byte-identical output. These are declaration targets, not 382 newly proved theorems
- P02: all 15 candidate source files, original hashes and current artifacts were matched to the sealed 130-theorem result. A separate 130-target type and axiom readback exited zero and was byte-identical to the sealed readback
- P03 graph: all graph, guarded-transport, audit and qualification-control modules were rebuilt in an independent empty output directory. The original 14-target surface passed
- P03 constructor checker: the final fresh-build-2 generation was independently rebuilt from copied source with the import path restricted to the fresh directory. All 13 modules passed. All 468 Python/model cases were rerun against these independent objects: 151 accepted and 317 refused, with every one of the 20 generated Lean modules passing
- Earlier frontier: eight mathematical modules and the verification module were freshly rebuilt. All 38 requested transitive axiom readbacks stayed within propext, Classical.choice and Quot.sound
- Measure extensions: TotalVariation, ResidualStability and AtomicPattern were freshly rebuilt; the arbitrary-index and explicit classification additions are treated separately below

The audit reviewed every repair hunk and the load-bearing definitions and statements. Compiler acceptance, source correspondence, mathematical scope and operational completeness were assessed separately. Failed experiments and expected-failure controls remain in the evidence directory and receive no success credit.

## P01 repair preservation

The nine proof and elaboration repairs preserve the written mathematical conclusions. The subsequent narrow-import repair in P01TypeAlgebra changes the imported library surface without changing its definitions. The display-option correction from pp.width to format.width fixes the audit driver; the failed earlier audit is not counted as a pass.

The PLift change is a genuine interface correction. Option requires a Type-valued payload, whereas Conv is a proposition. Returning Option (PLift (Conv t u)) preserves an actual conversion proof inside the successful payload. It is not an unchanged signature. The dependent fst, snd and sigma_eta_context binder annotations resolve the intended contextual types that the rejected original source did not elaborate. No comparison can establish identity with a nonexistent earlier elaborated type; the supported claim is preservation of the written intended domain and conclusion.

The direct reducibility proof covers all seven unchanged FiniteDerives constructors. Candidate membership includes strong normalisation and forward reduction closure; the proof does not smuggle global System F normalisation into a premise. The separate translation proof uses a nonempty beta path for every source step, including context steps. Its target-to-source normalisation reflection remains conditional on target normalisation.

The following restrictions must remain visible:

- The canonical Code interpretation and the normalising candidate interpretation are different constructions
- The endpoint PER and intrinsic dependent core can contain non-normalising terms. In particular, Omega inhabits an arrow with an empty PER domain, and even has a tracked intrinsic term. The finite-source normalisation theorem cannot be promoted to blanket dependent-core normalisation
- Sigma eta is valid on the represented Sigma domain. Representedness explicitly includes conversion to the pair of projections; it is not eta for every raw SKI term
- ParamFamily carries the body identity-extension law, and All introduction requires real uniformity evidence. The qualified predecessor supplies these generic interfaces; it does not itself supply the full recursive heterogeneous dependent interpretation or its probability/coupling theorem
- Proof-carrying envelope soundness extracts evidence already carried by an actual kernel object. It does not certify arbitrary JSON labels, the Python interpreter, or total frontend export

The join checker and envelope theorems are sound by construction. Their proof-carrying design explains why some equality hypotheses are unused; this is not circular evidence that an independently implemented unchecked frontend is correct.

## P02 repair preservation

All 130 original theorem headers are unchanged up to whitespace. The actual diffs are proof-body, notation-scope and pinned-library elaboration repairs. No mathematical definition, theorem domain or conclusion was weakened in the reviewed patch. The predecessor's finite rational checks use kernel reduction rather than native_decide.

The strongest qualified results genuinely use measures: countable positive singleton support, positive-fibre normalisation, weighted fibre identities, finite and infinite observation decompositions, compact-convex Cesaro fixed points, exact finite rational measure transport and all-length parity counting. Finiteness and measurability premises are present where the proofs need them. In particular, toReal is used only after controlling infinite mass in the relevant identities.

The infinite observation identity retains its residual term. The finite-row correspondence theorem selects actual stochastic rows and applies the proved fixed-point route; it does not import a field assuming the desired fixed point. ObserverCore remains a collection of LOOP semantics, causal output and algebraic ingredients. Compiling it alone does not establish a byte-code simulation, computable-index reduction or full hierarchy classification.

The 130-target seal and subsequent Q8 work have distinct source and evidence identities. The stronger Q8 results must be credited to the new extension, not retroactively attributed to the original 130 declarations.

## P03 graph and policy boundaries

The recursive endpoint repairs make the Path functions genuinely polymorphic in their recursive endpoints. Changing authorityTrace from an unguarded Via result to AuthorityPath uses the already-present intermediate redelegation evidence. It strengthens the helper to the guarded conclusion required by the unchanged main theorem; it does not erase the guard.

The transport theorem is a sound composition of local graph, evidence, semantic, authority and custody witnesses. Nontrivial positive controls show that it is not supported only by empty graphs or false source worlds. The following application obligations remain:

- Policy.epoch has no constraint connecting its number to policy predicates or observations of current time. An independent, axiom-free control reconstructs the same path at every numeric epoch while retaining the same predicates
- Frame.claim can change across a path. The theorem supplies no claim-identity invariant
- Graph nodes, EvidenceState obligations and SemanticState meanings have no representation relation linking them. A real application must establish that its graph and semantic witnesses encode the actual claims and reasons
- Onto is surjectivity on nodes. Hom.edge preserves source edges in one direction. An independent two-node control proves that a surjective map may introduce a target edge absent from the source. “Exact image” is justified for the node carrier, not for the entire edge relation
- An authority path need not be direct endpoint authority, and a root-custody path need not imply endpoint equality

These are limitations of what the model states, not counterexamples to its stated composition theorem. Temporal eligibility, evidence-to-graph correspondence or frozen-claim preservation need separately named extensions with explicit premises.

## P03 source and export boundaries

The new source evaluator is not an alias for target acceptance. It independently evaluates the seven constructors, performs capture-avoiding substitution, checks exact application domains and validates the full explicit reduction trace. The encoder separately erases trace content to repeated Cert.step constructors. The positive square identifies both the returned term and the returned type.

The asymmetry is necessary. A wrong-start singleton trace is refused by the source, but erases to a target certificate that accepts. Both the author's control and an independently compiled control establish this. Hence target acceptance cannot be used as a replacement for source acceptance.

The resource-aware model retains root shape, depth and integer limits, intermediate output limits and aggregate output-validation work. Its tree representation counts field-name keys and repeated occurrences. The inspected work-accounting experiment compares the actual Python work-list decrements with sourceRun for all 151 accepted cases; it is finite corroboration of the source map, not a universal Python-interpreter theorem.

The independently reproduced balanced-identity witness is particularly useful. Starting with polymorphic identity p0, define p(n+1) as application of p(n), instantiated at the identity type, to another p(n). At depth eight, reference.check succeeds and dump_json succeeds. The actual exporter rejects the proof at its constructor budget. The revised partialConstructorExport models that separate 512-unit work guard, including the source reduce wrapper's own work charge in addition to emitted step nodes.

The revised source_checker_export_square requires partial constructor-export success. Identifier, text-byte, module-row, JSON parser, mutable/hostile object and host allocation or stack behaviour remain outside that theorem. No general CPython refinement or total export claim is supported. NativeDecoder work started later and is not included in the fresh-build-2 assessment.

## Rank and finite machine frontier

The maximum and minimum rank theorems are both sound, but their hypotheses and conclusions are different.

The maximum envelope uses full successor-fibre coverage. Every target successor alternative must have an appropriate source predecessor. Combined with per-step source countdown and conservative zero-rank target transfer, it gives a fixed horizon and target persistence. The bundled contract also requires nonempty fibres and nonblocking; an independent theorem supplies an infinite policy run, excluding dead-end-only success.

The minimum envelope instead uses matching from every current source alternative and pairwise bad-state reflection. One minimal source witness transfers a budget for the number of bad visits. It yields eventual absence of bad states, but no cutoff bounded by the initial rank. The delayed single-bad-visit fixture correctly shows arbitrary delay with rank one. It cannot rescue the older stale-fibre example, because that example fails the stronger pairwise reflection premise.

The PER completion proof uses two tagged copies, so losing even a diagonal pair separates opposite tags. The quotient-cardinality potential and its exact formula retain inactive states correctly. Finite nonempty state hypotheses support the 2m minus 1 bound. The actual universal-input Mealy operator is compared over independent input words, not merely equal inputs, and its all-cardinality sharpness family establishes the lower bound beyond small examples.

The finite-block result counts actual input-word paths and normalises their cardinality. It does not, by itself, construct an infinite product probability space or prove an almost-sure or atomic-mass theorem. Any such upgrade requires its own measure bridge.

## Law-dependent measure stability

The measure stability proofs do not misuse same-map data processing. Each law-dependent atomic event is replaced by the union of the two laws' positive singleton supports. The additional countable support has zero mass under the other law where it was not already positive. This produces the needed common representative.

For countably many coordinates, the replacements hold simultaneously almost everywhere. ArbitraryPattern removes that countability restriction for product-sigma laws by proving equality on finite cylinders and invoking finite-measure uniqueness. It does not claim simultaneous almost-everywhere equality of uncountably indexed functions. Finite measure assumptions are explicit; probabilities are needed for the usual zero-to-one interpretation of defect, although the displayed difference bound is valid for the more general finite measures used in its theorem.

LossDecoder and HistoryClass give a measurable classifier for retained full-history atoms, first finite loss and residual infinity. The full-history exclusion is retained in the finite-class characterisation. Stage zero means initial loss; under coherent refinement, first loss at stage n plus one corresponds to the CV-R event L_n. Shared observation functions and full-law event-supremum total variation are essential. These statements do not establish stability from weak convergence or finite-marginal proximity alone.

The new spike example sharply marks the arbitrary-index boundary. Every coordinate of spike(x)(i) = [x=i] is almost everywhere false under the fair Cantor law. Its product-sigma pushforward is the all-false Dirac law, although no source point produces the all-false function. The all-false singleton is therefore not measurable in that uncountable product sigma-algebra. The proof is sound and prevents promotion of product-law equality to arbitrary full-pattern tests.

## Q8 structural compiler extension

The separately inspected Q8 construction uses an actual fair Cantor product law and a concrete finite two-counter machine. The switch copies fresh input coordinates on an eventually true persistent halt flag; the singleton bound is proved against arbitrarily long finite cylinders. The nonhalting law is Dirac and the halting law has zero singleton masses.

The structural compiler uses the stated register layout, a frozen old program counter during the instruction scan and stage plus one bounded execution. These details agree with the inspected Python compile_q8 construction after flattening list sequences into binary sequences. Immediate-halt and increment-forever witnesses inhabit both defect branches. Incorrect loop-bound and moving-program-counter variants are rejected by genuine false-proposition controls.

The measure equivalences do not by themselves establish a formal undecidability reduction. Python byte encoding, numeric indexing, resource-limited interpreter refinement and the computable map into a chosen program indexing remain separate obligations. The scope document retains those boundaries.

## Separate recursive finite model

A later P01 extension supplies an actual recursive interpretation of the frozen TypeCode constructors var, bottom, arrow and all. It is separate from the repaired predecessor. The 58-target qualification was independently rebuilt and read back, along with additional independently written controls.

No hidden restriction to diagonal environments was found. Any two endpoint PER environments and any family of respectful endpoint links can be packed into REnv; an independent control checks this directly. Heterogeneous arrow relations retain endpoint membership. The All object is explicitly the uniformity-constrained AllPER, and its identity extension is derived from the recursively constructed body identity law.

The allI case of finite_fundamental derives both endpoint uniformity proofs from the induction hypothesis under every extended diagonal environment, then derives the heterogeneous relation under every extended relational environment. The allE case uses the interpreted argument's actual heterogeneous link and the substitution theorem. There is no additional uniformity premise on the final theorem. Substitution's diagonal step correctly uses already-established model identity extension.

Independent witnesses establish polymorphic identity membership for every outer object environment, its heterogeneous relation for every relational environment, a nonempty heterogeneous link, and impossibility of a finite inhabitant of bottom. These prevent interpreting the result as an empty-model or absent-input victory. This is a parametric model of the closed finite calculus. Equivalence with an unrestricted nonparametric intersection interpretation of All, the full dependent/effect model and arbitrary ambient-section reification remain unproved by this extension. A further independent build covers the two Curry-parametricity and model-witness modules, with 22 additional theorem readbacks. The open-valuation fundamental theorem uses the shifted type-variable context at All introduction and typed application equality at lambda abstraction. Its concrete negative control shows that holding the type-variable context fixed makes unrestricted All introduction inadmissible. At the nonempty polymorphic identity type, I and SKK are related even though raw source conversion separates them. These are separate new-model results, not changes to the predecessor.

## Evidence and use

The main evidence index is EVIDENCE_INDEX.json. The directory retains copied source, exact commands, readbacks, successful and failed controls, and independent replay records. Primary records are P01_FINAL_INDEPENDENT.json, P02_FINAL_INDEPENDENT.json, INDEPENDENT_REPLAY_FINAL.json, EXTENSION_REPLAY.json, Q8_INDEPENDENT_REPLAY.json and the separately named measure and recursive-model addenda records. P03 cross-language evidence is in p03-cross-independent/RESULT.json. The independent negative witnesses are in IndependentBoundaryChecks.lean and probes/export_budget_boundary.py.

Use the repaired and new theorems at their stated premises and exact source versions. Preserve operational refusals and representation boundaries in any later integration. Any strengthening to full dependent semantics, total source execution, time-valid authority, arbitrary full-pattern observation or a complete computability classification should receive new declarations and its own evidence rather than a status-only upgrade.
