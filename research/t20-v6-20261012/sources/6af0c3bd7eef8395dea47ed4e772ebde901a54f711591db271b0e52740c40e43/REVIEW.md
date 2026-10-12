# Independent review: type-indexed family controls

10 October 2026. Ordinary independent mathematical/source review of `hase-type-indexed-henkin-obstruction-20261010`, frozen by its author at 10:58:53 UTC. This is not formal audit-service approval, integration, or programme closure.

## Verdict

PASS for the frozen packet's bounded claims. I found no blocking mathematical, source-fidelity, or kernel-replay defect. The packet establishes genuine source-grammar tests and conditional family obstructions. It constructs no whole `HasE` model, exhausts no Henkin class, and proves neither the literal universal `HasE [] c3 (W originalQ)` nor its negation.

The decisive limitation is substantive: `FamilyObstructions.lean` supplies explicit set-level results under a compositional family/projection/assembly contract. It does not derive that contract from arbitrary membership soundness. The source controls and semantic calculations are correctly kept separate, with the mathematical connection stated conditionally. The structured observer gives an additional constraint on a proposed model, not either missing scalar/graph transport bridge.

## Frozen material and independent replay

The reviewed author manifest has SHA-256 `b18b9bb4dc32125bc163c8185e71841fae3a6882669ec612245b6b66121b3412`; the reviewed RESULT has SHA-256 `f5895528ea5483a9b72986c84cb8c2469c63c99f2a43106f35a05c88c763a568`.

`replay_independent.py` is a separate reviewer driver. It checks the author's frozen files, INPUTS, predecessor receipt, Lean executable, all supplied source/object bindings, and the consistency of bindings with the predecessor receipt. It additionally hashes the entire inherited 83-module source closure against that receipt. It freshly compiles only the author's three new modules and two reviewer modules into a reviewer-owned fresh output directory with Lean 4.19.0 and `--trust=0`.

All five compilations passed without warnings. Ninety existing object bindings were checked and reused; the 83-module predecessor baseline was not rebuilt. No author file, inherited source, receipt, grammar, compiler endpoint, repository branch, or protected file was modified. Before/after rehashing confirms the frozen inputs remained unchanged throughout the replay.

Source pin: `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. Mathlib pin: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

The inherited receipt and existing compiler/library objects remain the supplied trust base. Hash verification is provenance checking, not a fresh compilation or bootstrap verification of those prerequisites.

## 1. Exact erased re-abstraction control

I read `AllSyntax.lean`, `ExtensionalRepairSyntax.lean`, and `IntensionalIdentityBridge.lean`, including the actual `allIntro`, `allElim`, variable lookup, type weakening/substitution, conversion, identity, J, and extensionality premises.

For `P = All Raw`, the source's type weakening preserves `[P]` definitionally. The variable lookup requires the declaration's term weakening; `wk P = P` also holds definitionally. Consequently the author's direct variable proof really derives `HasE [P] (var 0) P`. Eliminating at formed Raw yields the same polynomial at Raw. Reintroducing All under the same type-weakened telescope yields literally the original judgement. `same_endpoint_identity` uses the original identity-introduction constructor with the direct and reintroduced typings and reflexive `PolyConvPlus`; it does not insert annotated type application or abstraction.

Under the stated semantic contract, direct interpretation is `f`; elimination at Raw is `f r`; and body assembly gives the constant family `fun _ => f r`. Derivation-independent interpretation therefore requires `f = reabstract r f`. The equivalence with coordinate constancy is pointwise function equality, proved in both directions. The unrestricted Bool-indexed, Bool-valued identity family violates it.

This reasoning requires the displayed interpretation laws and the usual identification of valuations across the unchanged telescope. Bare closure of a membership predicate under the two typing rules does not imply those operations or equations. The author explicitly states that restriction. A quotient-valued or otherwise different candidate would need to supply its own interpretation contract and verify the actual source rules; it is not refuted merely by being type indexed.

## 2. Surviving constant-family fragment

`ConstantFamilies U R r` consists exactly of functions constant at their r-coordinate. Evaluation at r and constant-function formation are mutual inverses. The author's equivalence proof has the correct orientation, and pointwise extensionality reduces to function and subtype extensionality. Distinct Bool values give distinct constant families, so the repair is nontrivial.

This verifies a local fragment only. It establishes neither Pi/Sigma/J soundness nor closure of a full impredicative type universe. My singleton-index control additionally shows that unrestricted families can be coherent when the index type is a singleton even though R has two values; this prevents interpreting the two-coordinate test as an unconditional theorem against every possible family index.

## 3. Structured observer and retained Raw separation

The actual context is `[a:Raw, f:Raw, n:N]`. It is formed from the unchanged Church type. For fresh A, `Carrier = Sigma Raw (A → A)` is formed, and the source seed is `(a,I)`.

In the body context `[s:Carrier,a:Raw,f:Raw,n:N]`, index 2 denotes f, not n. `sigmaFst` gives the Raw first coordinate of s; `rawApp` applies the genuinely Raw f to that coordinate; the second coordinate I has `A → A`. The result has Carrier. `piIntro` checks the bracket-abstraction scope. Outside that binder, index 2 again denotes n. Its actual `allElim` instance at Carrier supplies the Church iterator type, two `piElim` applications type the run, and `sigmaFst` gives the Raw observation. The initial proof is in original `Has` and enters `HasE` through the unchanged inclusion theorem. No premise is removed.

The telescope is definitionally invariant under type weakening. The same observe polynomial consequently has both `All Raw` and its Raw specialization, plus the displayed source reflexive identity. These are real source derivations in an open n context; they do not rely on n being a closed numeral.

The semantic uniformity theorem assumes both (i) a constant-family result and (ii) equations identifying each coordinate with the structured body observation. Its equality chain is valid. The result constrains observations at the structured carriers `R × (X i → X i)` for source-realizable Raw updates under that contract. It is not a general naturality theorem for all functions and all carrier maps.

The frozen author packet no longer relies on a two-element model of Raw. Its actual term-algebra probe assigns a=I and f=K K. At numeral zero the run returns the seed and first projection reduces to I. At numeral one the bracket-abstracted step runs once, the first projection exposes `(K K) (fst seed)`, and K-reduction yields K. Normal-form uniqueness for the retained raw conversion separates I from K. The two environments are controls using distinct closed source numerals, not a construction of one nonparametric n.

I independently checked the Raw typings of I and K K and the actual source typings of every supplied input numeral. I also proved that the atom/application bridge in `PolyConvPlus` cannot identify the two evaluated observations: its inherited raw-conversion soundness would contradict the author's raw separation. This is a conversion control, not a new all-rule source-identity noninhabitation theorem.

A candidate whose Raw equality collapses I and K does not face this particular separating observation. A candidate preserving that distinction and claiming the assembly contract cannot assign zero-like and one-like behaviour at the two tested structured instances. The packet correctly retains those qualifications.

## 4. Exact self-instantiation and diagonal

`D = All (α → Raw)` is formed by the actual All/Pi rules. In `[D]`, `allElim` at the formed type D gives the same variable at `D → Raw`; `piElim` then derives `x x : Raw`. My independent definitional check confirms `tinst DiscriminatorBody Discriminator = arr Discriminator Raw`. Thus the self-instance is genuinely available in this grammar, rather than introduced by an invented weaker or stronger type system.

For the set-level result, define `ev x = e x d`. A fixed-point-free flip of R produces `δ(x)=flip(ev x x)`, which cannot equal any row `ev x`: evaluation at x gives a fixed point. Two distinct R values provide a fixed-point-free map classically. If e identifies `El d` with the full product of all `El i → R`, any prescribed g at coordinate d can be extended to a whole family by using a constant a elsewhere. Applying `e.symm` makes ev surjective, contradicting the diagonal.

The dependent cast in that completion has the correct direction, from `El i` to `El d` when `i=d`. The proof needs neither an interpretation of every HasE constructor nor full-PER soundness. The strengthened Henkin result directly exhibits a function omitted by every such self-coordinate decoding.

The obstruction concerns the displayed full product of full function spaces with a self code and nontrivial R. It does not forbid full Pi spaces alone, nor all restricted All-family interpretations. My explicit equivalence `Unit ≃ (Unit → Unit → Unit)` verifies that removing the two-distinct-results premise permits a full self product. No inconsistency of the source follows from the diagonal argument.

## 5. Independent positive and negative controls

`IndependentControls.lean` adds the following checks beyond replaying the author:

- Definitional equality of both relevant type-weakened telescopes and of D's self-instantiation.
- Actual source typings of the Raw I seed, Raw K K update, and every input numeral.
- Nonconversion of the evaluated Raw probes even under the retained polynomial atom/application bridge.
- Full-family coherence with a singleton index and nontrivial result type.
- A full self product with singleton result type, showing why nontriviality matters.
- Uniformity of the zero family and the one family separately on genuinely differing structured carriers.
- A varying local zero/one family whose two Bool observations differ.
- Existence of a coherent constant result alongside those differing observations when assembly equations are absent.
- Impossibility of coherent assembly for that exact varying family when the advertised equations are imposed.

The finite Bool calculations are deliberately local hypothesis controls. They do not interpret the full source Raw combinatory algebra. The negative controls are proved mathematical negations, not merely failed tactic attempts.

## 6. Dependency and inherited-result review

`Dependencies.lean` traverses the transitive declaration dependencies of all 41 author theorem/equivalence declarations. Only `propext`, `Quot.sound`, and `Classical.choice` appear. It excludes the identified whole-model fundamental theorems, scalar-target validity, and Church-standardness/source-identity shortcuts. Required-dependency checks confirm use of the actual source variable, All, Pi, Sigma, Raw application, identity, and inclusion constructors, and of the retained numeral application, abstraction-beta, and raw normal-form uniqueness results. No admitted proof, added axiom, native-decide oracle, unsafe replacement, or kernel-check bypass was found.

The initial open raw source context and the final family proof hypotheses are not disguised source targets. The theorem signatures never assume or derive the original universal scalar target.

I compared the inherited strict-successor/strict-zero model failures, contextual free-proof failure, Raw-endpoint motive boundary, full-PER whole model, conditional graph-bridge assembly, and closed Church source-identity completeness. Their restrictions remain intact. In particular: no blanket Raw coercion is used; no free identity-proof generator is introduced; no closed-to-open inference occurs; and neither missing graph projection is supplied.

I also read `BoundaryResults.no_erased_full_sections` and its singleton-interface control. The generic erased/full-family incompatibility is inherited algebraic ancestry. The frozen RESULT properly credits that fact. The project additions reviewed here are the exact HasE controls, the new structured observer with retained Raw separation, and the application of the familiar self-index diagonal to an actually formed source type. This is not a claim of field-level novelty.

## Remaining work

A successful separator still needs an independently specified impredicative restricted-family construction; closure under the real introduction/elimination and substitution rules; dependent Pi/Sigma/identity/J and extensionality soundness; a genuinely admissible semantic Church element; and evaluation of the unchanged original scalar/compiler target that separates it. None is supplied by these local controls. Conversely, the packet does not show that every candidate satisfying these controls obeys full scalar fusion.

That is a real narrowing of candidate obligations, with the original universal problem still open.
