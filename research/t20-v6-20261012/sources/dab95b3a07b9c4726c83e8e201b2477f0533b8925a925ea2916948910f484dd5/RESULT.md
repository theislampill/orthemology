# Exact Raw-endpoint motive boundary for the original pair

10 October 2026. **The attempted motive `Id_Raw(endpoint,q)` is not formed in the actual J context for the original pair.** This is a new-to-project target-specific application of the inherited all-rule soundness result. It is not a new general soundness theorem, and `HasE [] c3 (W q)` remains OPEN.

## The actual test

Keep the original endpoints unchanged:

    p = variableExpr.closed
    q = redundantExpr.closed
    T = N → N
    B = Id_T(p,q).

The actual source J context is `theta [] T p`. Its de Bruijn coordinate 0 is the identity proof; coordinate 1 is the varying endpoint of type T.

The new file checks all of the following against the imported original grammar:

1. `no_endpoint_raw`: `HasE [T] (var 0) Raw` is impossible.
2. `no_theta_endpoint_raw`: `HasE (theta [] T p) (var 1) Raw` is impossible, including any indirect derivation through J, conversion or the other HasE rules.
3. `endpoint_motive_not_formed`: `FormE (theta [] T p) (Id_Raw(var 1,q))` is impossible. Formation of this identity would require exactly the excluded Raw typing of its endpoint variable.
4. `no_raw_reflection_under_assumption`: for every proof polynomial r, `HasE [B] r Id_Raw(p,q)` is impossible. Even declaring the original typed identity as a hypothesis does not provide raw identity of these original endpoints.

This does not infer a forbidden coercion merely by inspecting the last rule of a typing derivation. The typing exclusions use the inherited soundness theorem for **all** HasE rules. The final formation step can then legitimately invert `FormE.identity`, since the fixed type constructor has that formation rule.

## Positive controls and non-vacuity

The two test contexts are actually formed in the source calculus. The ordinary assumption-variable rule is checked for the typed-identity context. Most importantly,

    theta_proof_coordinate_raw:
    HasE (theta [] T p) (var 0) Raw

is derived with the actual `proofErase` constructor. The endpoint coordinate is excluded; the proof coordinate erases legitimately. The source's operation has not been replaced by a blanket prohibition on Raw typing or J motives.

The semantic environments are explicitly constructed:

- At `[T]`, one valuation sends its endpoint to p, the other to q.
- At `theta [] T p`, both proof coordinates are I; the endpoint coordinates are p and q.
- At `[B]`, the assumption coordinate is I in both valuations.

These valuations are related in the **inherited F/G interpretation**. Thus the negative claims do not depend on an empty or malformed context.

Independent reviewer-only kernel checks also establish D-membership of both theta valuations and the assumed-identity valuation, Raw typing of the fixed q in theta, and formation of the Raw-identity target in `[B]`. The first failure isolates the varying endpoint; the second is a genuinely uninhabited, well-formed identity target in a semantically inhabited context. These extra controls are in `validation/IndependentBoundaryChecks.lean`.

## What supplies the contradiction

The retained checker theorem establishes F-model relatedness of p and q at T. The retained endpoint theorem establishes that their raw evaluations are not convertible. These are different relations.

If the endpoint variable were typable Raw, inherited all-rule HasE soundness would require its evaluations at the two related valuations to be raw-convertible. They are exactly p and q, contradicting the retained raw nonconversion theorem.

The same reasoning excludes raw identity in the context declaring B: its related semantic valuation exists, so soundness would force raw conversion of the unchanged closed endpoints. Evaluation-independence of those closed polynomials is used explicitly.

No closed HasE derivation of B is assumed or produced. The theorem `typed_related` has conclusion **F T rho zeroEnv p0 q0**, not `HasE [] r B`. `[B]` is a well-formed hypothetical context. Its F/G semantic witness is not silently promoted to a source proof of B.

## What is inherited and what is new

The recovered source already contains `closed_raw_identity_conversion`, a different typed/raw separation witness, and `separation_proof_erases`. Those generic facts are credited to the inherited source, not presented here as newly established research.

The new operation is the exact original pair's contextual and J-motive stress test, with both coordinates, formed-context controls, and the stronger statement about every raw-reflection proof polynomial under an assumed original typed identity. A targeted repository search and inspection of the recovered closure found no duplicate of these exact statements; no claim of global mathematical novelty is made.

The source closure and conversion/compiler transport package are immutable predecessors. This file imports actual `UArrowAndCompilerControls` and `ExtensionalRepairSoundness`. It does not import the open-term standardness proof or assume soundness of that newer interpretation.

## Effect on the remaining frontier

The proposed raw-code-sensitive J motive is not a counterexample to extending the new open-term PER reduct: it fails an actual source formation obligation. `rawAtom` types closed raw atoms, and `proofErase` types identity evidence; neither gives the tested bound endpoint a Raw type.

This does **not** validate every other possible motive or establish a whole-HasE model on the open-term carrier. It also does not block the already retained scalar motive W(k), which uses the endpoint at its proper function type and was separately formed in the fixed-witness construction. No inference from the fixed proof's raw normal form to introduction inversion is made.

The remaining full-model problem is still to establish the complete formation/coherence/fundamental theorem for the new interpretation, or find another **legally formed** discriminating obligation. The original literal typed target and its negation are both unproved here.

## Verification

`RawMotiveBoundary.lean` is checked with Lean 4.19.0 and `--trust=0`. Its negative theorems depend only on the ordinary Lean axioms `propext`, `Classical.choice` and `Quot.sound`; the positive context/proof-erasure controls omit `Classical.choice`. There are no new postulates, admitted proofs or oracle checks.

`replay.sh` checks the immutable predecessor manifests and compiles the new file against the already independently rebuilt exact source closure. Its receipt deliberately records this as a new-file replay rather than claiming another rebuild of all 83 original modules. The separate review is recorded in `validation/INDEPENDENT_REVIEW.md`.
