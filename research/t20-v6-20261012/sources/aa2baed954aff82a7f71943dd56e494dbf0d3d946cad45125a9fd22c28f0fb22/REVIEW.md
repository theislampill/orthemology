# Independent review: the internal scalar graph construction

10 October 2026. Disposition: **PASS, bounded source-construction review**. The exact literal `HasE [] c3 (W q)` and its negation remain **OPEN**. No owner acceptance, integration, or programme closure is asserted.

## Result

The two new files contain a genuine derivation in the original source grammar, rather than a semantic surrogate or an assumed graph-fusion principle. The graph carrier is exactly

`G = Sigma s:S. Sigma x:alpha. Id_alpha(x, snd(s) f a)`.

The state coordinate and scalar coordinate are independent term coordinates, linked by typed identity. The lifted step updates them to `Delta s` and `f x`. It does not replace the scalar with `h(Delta s)` by recomputation. Formation, seed, strong step, Church instantiation, and invariant extraction are all kernel checked. The final extracted judgement concerns two coordinates of the same graph run:

`HasE Gamma (snd(snd r)) (Id_alpha(fst(snd r), h(fst r)))`, where `r = n g b`.

It does not yet compare either coordinate with the corresponding external iteration.

## Source and parameter audit

- `Graph` uses the actual `S = Sigma N N`, with the scalar parameter at `.param 0`. Its two bound term coordinates are represented by variables 1 and 0; outer f and a are shifted by two. `graph_inst`, `graph_leaf_inst`, and `graph_wk` compute these substitutions explicitly.
- `graph_pair_has` accepts a separately supplied x and a proof `Id_alpha(x,h(s))`. This is the relevant strength beyond `pack`, which only constructs the reflexive recomputing graph point.
- The congruence motive is `Id_alpha(f x, f y)` over the actual two-coordinate theta telescope; f and x are weakened twice. Transitivity uses the motive `Id_alpha(x,z)` over the corresponding varying endpoint. Both motives, their base and target instances, and all endpoint typings are supplied to actual `Has.j`.
- `strong_step_body_has` combines the incoming graph proof via congruence with the raw identity `f(h(s)) = h(Delta s)` in the correct orientation, using transitivity. The state step is the imported original `diagonalStep`; its typing and raw beta law are derived without replacement.
- `graph_run_has` uses actual source `allElim` to instantiate N at the formed dependent graph type, then applies the typed lifted step and seed. It does not take induction, parametricity, naturality, or a projection equation as a premise.
- The general result assumes original `Ctx` and `Has` derivations for n, f, and a. Its output is included into `HasE`. It is not a theorem over arbitrary HasE-only input derivations. In the displayed literal scalar context `[alpha, alpha -> alpha, N]`, all needed original premises are available by the variable rules.
- `original_scalar_computation` uses the imported `redundant_closed_exact`, binding q to the actual unchanged compiled `redundantExpr.closed`. ScalarFusionCore and LiteralScalarFusion were read and hash-compared to their prior immutable bindings. The latter was not rebuilt in this review, and its conditional four-way equivalence was not mistaken for an inhabitant.

No unproved graph-naturalness premise or semantic-completeness import is hidden in the positive source construction. The transitive Lean constant audit additionally excludes dependencies on F, G, predicates, old semantic soundness/fundamental results, graph_application, and semantic_church_standardness for eight positive targets.

## Exact open boundary

The following types are formed in the literal scalar context:

1. `Id_S(fst(n g b), n Delta z0)`
2. `Id_alpha(fst(snd(n g b)), n f a)`

No source inhabitant of either type is supplied. Together they are a sufficient projection-transport route for this graph construction; they are not claimed necessary for every possible proof of scalar fusion. Even the conditional assembly from arbitrary HasE inhabitants of these two types to W(q) has not been formalized in this package. Ordinary identity congruence, symmetry, and composition explain that intended assembly, rather than serving as an already checked theorem.

The four step/seed commuting computations are genuinely proved. They do not establish that an arbitrary source Church variable preserves those commuting maps. `allElim` keeps the polynomial but changes its instantiated type; it is not a naturality rule. The extensionality rules still require the relevant displayed identity evidence. Neither raw normal forms of proof terms nor their erasure licenses introduction inversion, as the previously read ScalarFusionCore.forward_fixed counterexample already shows.

The two new negative theorems are precisely raw PolyConvPlus nonconversion:

- For the first projection, the raw valuation n = K(K I) makes the compared terms reduce to K and I.
- For the scalar projection, n = K(K K) makes them reduce to K I and K.

Both use actual conversion soundness under arbitrary raw valuations and normal-form distinction. Neither valuation is asserted to satisfy the typed Church context. Thus they refute the direct raw-conversion premises for those displayed endpoints, not the possible HasE identities, not original target derivability, and not the existence of a faithful typed model. They also do not rule out a J/extensionality proof of either bridge.

## Independent execution and controls

The author froze Lean sources at these SHA-256 hashes before replay:

- InternalGraph.lean: `74ef636570ba73c227daf40d913bdba5a9c40bb83b87579f1b902f1f6a2db25e`
- ProjectionBoundary.lean: `99209853e5882ee3ce54d86c32cd0f33efcc43e66ef7dca934788ca5ecfd8469`

Both were copied into the review source directory, compiled afresh with Lean 4.19.0 `--trust=0`, and compared again to the author's frozen sources. Exit codes are zero. Only ordinary propext, Classical.choice, and Quot.sound appear.

Prerequisite reuse was explicit rather than an unverified cache assumption. This review rehashed all 89 previously fresh trust-zero prerequisite objects and the 83 pinned source modules against `hase-full-per-review-20261010/PREREQUISITE_REBUILD.json`. It also rechecked the three predecessor manifests, the four scalar-frontier bindings, the ScalarFusionCore source/copy/object records, and the Lean binary hash. No second rebuild of the 83-module closure was performed. Third-party library objects and the compiler bootstrap remain the same external trust base as in the prior review.

New independent controls compile under `--trust=0` and verify:

- Proof erasure reduces the constructed step evidence to I, while the data step still retains `f x`.
- Open f and a remain correctly scoped after extending the scalar context with the genuinely dependent graph binder; the actual step typechecks there.
- Numeral zero has a source-typed graph run and both desired projection conversions, providing a positive non-vacuity/control case without extrapolating to arbitrary source n.
- Printed theorem types expose exactly the original Has premises.
- Eight positive targets have no transitive dependency on the forbidden semantic results; both conversion-boundary theorems have only standard axioms.

Evidence files: `SOURCE_REPLAY.json`, the two `*_REPLAY.log` files, `IndependentControls.lean`, `CONTROLS_FINAL.log`, `PREREQUISITE_REUSE.json`, and `REVIEW_RECEIPT.json`.

## Inherited-result and novelty check

The frozen 83-module source closure already contains EffectiveStandardness.graph_application and semantic_church_standardness. They are semantic F/G graph/standardness results. A bounded search across that closure and direct inspection of those declarations found no copy of this dependent source graph construction. More importantly, the checked new positive targets do not depend on those semantic results. The new work's contribution is this explicit source-typed strong graph construction and the precise new projection boundaries. It is not a claim that graph iteration, congruence, Church encodings, or the mathematical idea is novel, nor an exhaustive search of all earlier project artifacts or literature.

## Findings and terminal status

- Source derivation, parameter scopes, compiler binding, theorem strength: PASS.
- Frozen replay, controls, standard-axiom audit, forbidden semantic-dependency audit: PASS.
- Projection transports and original literal target: OPEN, explicitly out of the proved result.
- No protected predecessor source or prior evidence was modified by this reviewer.
- One minor author-report replay-command path ambiguity was reported for correction; final report bytes and correction status are bound in REVIEW_RECEIPT.json.

This review supplies bounded evidence to the parent audit. It does not grant acceptance or closure authority.
