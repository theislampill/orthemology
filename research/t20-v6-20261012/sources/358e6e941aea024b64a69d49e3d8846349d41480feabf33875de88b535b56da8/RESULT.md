# Fixed typed-carrier observer: a Raw-independent coherence test

10 October 2026. Core frozen after a fresh Lean 4.19.0 `--trust=0` replay.

## Result

The Raw-only source observer genuinely generalizes to arbitrary fixed, original-source typed carriers. For any source telescope Γ, type B, and original P01AC.Has derivations

- Γ ⊢ n : N
- Γ ⊢ f : B → B
- Γ ⊢ a : B,

`TypedObserver.lean` constructs the same observer polynomial

`fst(n (λs. pair (f (fst s)) I) (pair a I))`

at B. The step's displayed lambda is the actual existing bracket abstraction, not a new source constructor. The structured carrier is `Sigma B (A → A)` for fresh A. The proof uses typed Pi application of f, never rawApp. B can contain existing type parameters and dependent identity endpoints: the inner term-binder bookkeeping uses real wk/has_wk, not an assumption that B is term-independent.

Most importantly, under a fresh type parameter the construction is at `twk B` in `twkTel Γ`, then allIntro gives `All (twk B)` in Γ. allElim at every formed T gives B by the actual theorem `tinst_twk`. The outer B is held fixed; `All B` is not declared constant by definition. In the concrete parameter test, B=param 0 becomes param 1 beneath fresh A, and elimination recovers param 0.

The source hypotheses are original Has/Form/Ctx, not arbitrary HasE derivations. The resulting derivations are included into HasE, and the explicit identity results are HasE identities. No general HasE weakening or all-rule semantic theorem is claimed. In particular, this construction can be used with n as an ordinary N-valued source variable, so it is not restricted to source-definable closed semantic n-values.

## Exact source observations

`TypedObservations.lean` proves open source PolyConv, for arbitrary polynomials f,a:

- observe(inputNumeral 0,f,a) ≃ a
- observe(inputNumeral 1,f,a) ≃ f a.

Together with all endpoint typings these become actual HasE identities at B. A source-typed constant endomap is `K b : B → B`; the second observation then converts to b and has the corresponding HasE identity. No full function-space assumption is needed just to obtain this constant map. The previous Raw I/K separation is replaced by the candidate's own distinct semantic values a≠b in B. Those values can be supplied by a context; they need not be closed source-definable values.

The open beta and pair-first lemmas are reused from the existing InternalGraph object. They are not counted as new results.

## Exact candidate contract

At a fixed outer semantic environment and valuation, let D be the interpretation of B, U the type-instance indices, and Q the candidate carrier for All(twk B). The contract assumes:

1. Actual type weakening identifies the interpretation of twk B under each extended type environment with the same D and preserves the weakened term valuation. This is a required interpretation law, not proved for arbitrary candidate semantics here.
2. `decode : Q → U → D` gives All elimination. Reintroduction after eliminating at r is represented by `reintroAt r x`. Ordinary body assembly gives `decode (reintroAt r x) i = decode x r`.
3. Derivation coherence for the literal `fixed_reabstract` source cycle gives `reintroAt r x = x`. The source cycle includes the actual has_twk step.
4. The interpretation of the actual source `observe_all_has` derivation assembles its displayed structured-body values: `decode result i = structuredObservation X n f a i`. This equation depends on the candidate's interpretations of Pi, Sigma, SKI, and All; it is explicit, not inferred from bare unary membership soundness.

Under these laws, `observer_uniform` proves that the observed B-result is independent of fresh A. `no_zero_one_assembly` then rejects a family that is zero-like at one structured carrier `D × End(X i)` and one-like at another, using typed K b and a≠b in D. A local Bool-valued control checks the rejection alongside a subsingleton Unit designated as Raw. It is not a whole-source model with finite Raw.

## Duplication and scope

The predecessor's set-level `structuredObservation` and uniformity theorem were already polymorphic in a result set R. Replacing its letter R by D would contribute nothing. The nonduplicative source addition is typed B instead of Raw, real dependent term/type weakening, the All(twk B) erased cycle, and exact source 0/1 identities at B using a typed endomap. The new contract spells out the same conditional coherence principle; it is not claimed to be a new general set-theoretic theorem.

This excludes the displayed incompatible structured-coordinate choices only for a candidate with the stated compositional and coherence laws and a nontrivial fixed B. It does not force every type-indexed carrier to collapse when Raw collapses, refute all Henkin models, construct a whole model, supply either original graph projection, prove arbitrary naturality or scalar fusion, prove the literal universal W, or prove source noninhabitation. A family choosing counts uniformly over the entire Sigma outer shape could still pass this one observer. A separate sibling investigation tests a Sigma/Pi cross-typing case; it is not part of this frozen core.

## Replay

Run `python hase-typed-observer-coherence-20261010/replay.py` from the shared workspace. It verifies bound source/object hashes and compiles only the three new modules into a fresh output directory, reusing existing retained prerequisite objects. No baseline rebuild, protected edit, integration, or T20 closure occurred.

Author replay result: validation/REPLAY.json, status PASS. Source and object hashes are recorded there; INPUTS.json binds the retained inputs. The printed dependency sets are confined to propext, Classical.choice, and Quot.sound. No new axioms, admitted proofs, unsafe implementations, or native evaluator shortcuts occur. Independent review, if available, is a separate result and is not claimed by this author report.
