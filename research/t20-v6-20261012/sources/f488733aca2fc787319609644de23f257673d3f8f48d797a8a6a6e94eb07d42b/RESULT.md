# Actual Joint recursor uniqueness from shared algebra laws

## Result

The explicit comparison-step obligation in the independently accepted `hase-joint-induction-computation-20261010` packet is now discharged in actual `HasJ`.

For arbitrary `CtxJ Γ`, arbitrary newly formed `FormJ (N :: Γ) P`, a typed seed `p : P(0)`, and a typed curried step `s : Πn:N, P(n) → P(succ n)`, let `u,v : Πn:N, P(n)` be actual source sections. Supply only their ordinary algebra laws:

- zero witnesses `zu : Id_(P(0))(u zero,p)` and `zv : Id_(P(0))(v zero,p)`;
- successor-law sections `lu : Πn:N, Id_(P(succ n))(u(succ n), s n (u n))` and `lv : Πn:N, Id_(P(succ n))(v(succ n), s n (v n))`.

`recursor_unique` constructs `HasJ Γ ident (Id_(Πn:N,P(n))(u,v))`.

Each successor-law family names only its own section and the common supplied `s`. Neither law contains the other section, an induction hypothesis, or a comparison-step premise. `recursor_unique_generic_laws` offers the equivalent ordinary-rule interface, accepting these two source law derivations directly in context `N :: Γ` and using Pi introduction to package them. No uniform source function is inferred from a meta-level assertion only about closed numerals.

## How the formerly missing step is built

The comparison family is the retained literal `C(n) = Id_(P(n))(u n,v n)`. At a generic `n` and a genuinely bound source assumption `e : C(n)`, the common operation `s n : P(n) → P(succ n)` gives, by source J congruence:

`Id_(P(succ n))(s n (u n), s n (v n))`.

Compose the `u` successor law, this congruence identity, and the symmetric `v` successor law. The result is `C(succ n)`. Actual weakening and Pi introduction produce the entire curried comparison step. `comparison_step` has no comparison-step hypothesis: it derives it. The bound assumption `e` is passed to `arrow_congr`, whose proof transports reflexivity along `e` using actual source J.

The zero comparison seed uses the two supplied zero laws, symmetry and transitivity. The retained `induction_extensionality` then invokes actual `natInduction` on C and actual `piExt` to produce typed function identity.

The comparison step's polynomial can be `abstract (abstract ident)` because source J erasure and symmetry permit I evidence for the composed identity. This does not assert equality of arbitrary identity-proof polynomials or proof-path uniqueness. Derivability still depends on the supplied law proofs and the bound comparison hypothesis.

## Exact canonical-recursion corollary

`canonical_successor_laws` packages the preceding packet's actual successor theorem into a source law section for its exact unchanged `sectionPoly p s`. It obtains the proof in the generic-variable context and applies Pi introduction; it does not turn unrelated pointwise existential witnesses into a source function.

`unique_to_canonical` proves that every actual section obeying the supplied zero and successor laws is typed-function-identical to that exact `sectionPoly p s`. Its formation, seed and step premises remain arbitrary actual Joint judgments. No old-E formation/typing premise or external rigidity witness is added.

## Scope controls

The new-family instance reuses the accepted literally index-dependent family `P(n) = Id_E(n I I,n I I)` with the genuinely Joint-new carrier E. The packet independently supplies zero and successor laws for the direct section `abstract ident`, using the same retained seed I and step `abstract (abstract ident)`. The new uniqueness theorem identifies this direct section with the exact canonical `sectionPoly ident step` at typed function identity.

Retained exclusion theorems are rechecked at this instance: the family is not old-E formed; no old-E term inhabits its seed type or its step type; its zero and successor-zero source instances differ literally. This is an input-scope discriminator, not a minimality argument: the family is reflexive and already admits its displayed direct section.

## Verification and preservation

Run `python3 hase-joint-recursor-uniqueness-20261010/verify.py`. It pins the five new source modules, scripts and this report; verifies all 388 retained source/object/report/toolchain pins before and after; and compiles just these five additive modules in a fresh output directory with Lean 4.19.0 and `--trust=0`. The candidate's existing object directory is removed from the replay import path. No retained dependency is rebuilt.

`JointRecursorAudit` checks the entire dependency closures of every new helper, public theorem and scope control for nonstandard axioms and `sorryAx`. Positive constructions must not depend on retained semantic fundamental/soundness or completion-rule soundness shortcuts. Further positive controls require actual source J in congruence, the common-operation congruence theorem in the comparison step, and actual `natInduction` plus `piExt` in uniqueness. The general uniqueness theorem uses only `propext` and `Quot.sound`; the canonical corollary also inherits standard `Classical.choice` through the retained source construction. No foundationally axiom-free or choice-free claim is made.

The source/replay freeze is `validation/CANDIDATE_FREEZE.json`; retained inputs are `validation/RETAINED_INPUTS.json`; fresh replay evidence is `validation/AUTHOR_REPLAY.json`. Independent review is separate.

## Boundary

This is uniqueness up to actual typed function identity from shared ordinary recursion laws. It is not Raw conversion, proof-path uniqueness, full categorical initiality, global completeness or decidability. The older packet's strict typed-versus-Raw successor separation is preserved unchanged. The old-E negative result, faithful-Raw FullPER positive model, and positive unadopted Joint completion remain distinct. No source rule, adoption decision, protected source, retained evidence, branch or release is changed, and no T20 closure is claimed.
