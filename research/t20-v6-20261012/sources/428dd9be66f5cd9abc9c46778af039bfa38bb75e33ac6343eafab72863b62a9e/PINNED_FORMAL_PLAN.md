# Exact-pin formal plan and source-to-statement map

This is an implementation plan, not a successful Lean run. Target toolchain:

- Lean 4.19.0, compiler commit 6caaee842e94.
- Lake 5.0.0-6caaee8.
- mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b.

The separate accepted 4.32.2 scope cannot fill these targets. The 12-module mapped-native A8F results remain accepted at their exact previous scope; the original strict wrapper remains FAIL. The current environment has no Lean/Lake/Elan executable. The supplied candidates have neither an observed declaration type nor an axiom readback.

## New concrete candidate inventory: 11 theorem targets, zero checked

`P02.MeasureCore`: positiveSingletons_countable; positiveSingletons_measurable; positiveSingleton_mem_of_null_compl; positiveSingletons_subset_conull_intersection.

`P02.T300`: normalised; weights_nonnegative; all_proper_marginals_equal; parity_target_changes; declared_flip; mixture_target_retained; every_pair_profile_changes.

All exact headers and definitions are in the hashed candidate source, with `Readbacks.lean` requesting each declaration and its axioms. The finite module has n=3 only. These 11 targets do not constitute U05 or Q1c closure and do not cover CV-R/CV-C/U08.

## U05 target sequence

| Target | Exact hypotheses/result | Formal ingredients | State |
|---|---|---|---|
| M01a | Finite measure, measurable singletons ⇒ positive singleton set countable/measurable | inspected disjoint-set countability API | unexecuted candidate |
| M01b | Probability measure ⇒ a=measure positive singletons=their sum; 0≤a,d≤1 | countable measure/sum; finite ENNReal conversion | statement/proof only |
| M02 | Conull events; measurable intersection ⇒ mass≥a; rich singleton-complement repertoire attains a | null complements; countable support; explicit measurable/full interface | inclusion candidate only; full equivalence pending |
| M03 | Measurable h and positive coarse fibres ⇒ exact weighted fibre identity | Measure.map, restrict, normalisation, countable regrouping | statement/proof only |
| M04 | Countable normalised mixture ⇒ a,d affine | measure sum; countable null sets; zero-weight guards | statement/proof only |
| M05 | Two explicit weak-convergence sequences on [0,1] | real Lebesgue instances, finite grids, test-function convergence | statement/proof only |
| M06 | Bounded-halting observer ⇒ d=0/nonhalting, d=1/halting | exact Cantor product law, bounded simulation | statement/proof only |

Do not conflate measure atoms with singletons, real and ENNReal subtraction, outer-measure notation with a measurable conjunction, or an uncountable mixture with M04. No regular conditional probability theorem is needed for M03's positive fibres.

## CV-R target sequence

U05-M01/M03 must be checked before importing them as formal predecessors. Construct the countable product output, measurable positive-cell events, their decreasing relation, and the positive full-history event. Prove one-step debt, finite telescope, continuity from above, and J as a separate measurable difference. Then prove the cell-mass characterisation and the specified order of limits. Semantic certificate equivalence uses the exact U05 event repertoire; artifact validity is not part of the measure equation. The optional martingale formulation additionally requires a pinned conditional-expectation convergence theorem; R03's elementary proof does not depend on it.

## CV-C target sequence

Freeze a reviewed byte-level total PR syntax/numbering and parameter compiler, rather than treating the semantic class as an already implemented codec. Construct its exact dyadic cylinder probabilities. Prove soft-mass monotonicity, integral representation and both limits. Define index-set reducibility and the relevant arithmetical classes; formalise the FIN/INF and rowwise-finiteness compilers, then the non-dyadic rational selector. Check every strict/non-strict and endpoint statement separately. For finite Mealy, prove cross-input determinism, countability of hitting outputs, exponential avoidance bound, atomic-mass/hitting equality and rational linear solve. The Python census cannot serve as any of these universal proofs.

## U08 target sequence

Review the proposed finite-support envelope and fixed row-set correspondence separately from canonical safe-domain definitions. Identify a compatible pinned fixed-point library declaration, or explicitly author/review a proof of the restricted family. Discharge nonempty/compact/convex domain, range and values, continuity/closed graph, and the fixed-point statement. Formalise the rational-flow equivalence and exact finite feasibility separately. The noncomputable constant-map obstruction concerns unrestricted real data, not the rational subclass. Failure to identify the pinned library remains open; no imaginary import is provided.

## Q1c target sequence

First check the 3-bit candidate, including all actual declaration types and permitted axiom dependencies. Then implement the all-n parity-flip bijection and the completion-count bijection on a proper coordinate subset; derive normalised finite probability, deterministic transport and the finite-mixture kernel. Preserve n≥3 for the pairwise statement. Wrapper consumers receive this only after explicit acceptance; no Q1a pure theorem depends on adopting this application.

## Permitted future verification evidence

For each successful target, retain command, cwd, start/end or duration, exit, exact executable identity/version, pin and candidate source hashes, raw stdout/stderr, declaration/type and transitive-axiom readbacks, and fresh nonempty .olean files with hashes. Repeat in a separate clean proposal workspace. A successful command alone is insufficient. Reject wrong pins, missing targets, added assumptions, `sorryAx`, errors, missing artifacts, stale artifacts and output-only spoofing. The current candidate text has no admitted theorem placeholder, but a static scan is not an axiom audit.

The helper shell script performs builds and captures evidence **only when executed later in a fresh external workspace**. It never prints a theorem PASS and never changes canonical source. Its terminal marker requires actual type/axiom and source-mapping review before any credit. New compiler diagnostics must be preserved; syntax repairs may not weaken hypotheses or collapse the scope to an assumption-loaded theorem.
