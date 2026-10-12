# Computable closed-input count extraction by complete developments

10 October 2026. The requested **normal-order completeness theorem is not supplied**. A distinct, deterministic **complete-development strategy** is implemented and proved to reach the generic-open iteration for every supplied original closed derivation `HasE [] n N`. This is an executable consequence of the already checked standardness result, not a second Church-canonicity result, a field-novel normalization theorem, or a proof of the universal scalar-fusion judgement.

## Result

`OpenDevelopments.extractIteration` is an ordinary computable Lean definition. It takes the actual original `n : Poly` and a proof `HasE [] n N`, and returns:

```
{ k : Nat // PolyConvPlus (scalarLeft n) (iterationPoly k) }
```

The returned count is shown in `extractIteration_uniform` to work for every raw open `f,a`. `closed_HasE_development_terminates` additionally proves that both actual scalar endpoints, including the original imported `originalQ`, reach the same exact `var(1)^k var(0)` under repeated complete developments.

The definition uses executable, decidable `Nat.find` over structural readback of finite development rounds. It does **not** compute a count by extracting data from `Classical.choice`. Its termination proof uses the existing full-PER model and its ordinary logical axioms in `Prop`; runtime computation uses only the finite source syntax, complete developments, and exact iteration recognition. The declaration compiles without `noncomputable`. Lean `#eval` runs return counts `0,1,2,2,2` for literal numerals 0/1/2, `K numeral(2) Ω`, and the compound-atom-packed numeral 2.

A separately implemented bounded Python diagnostic produces explicit compatible-SKI contraction-address traces for both endpoints. A separate address replay checker validates each step and the exact count. Generated Lean certificates replay those traces using `ScalarCertificates` and conclude actual `PolyConvPlus` conversions. For closed input syntax, the certificates also reconstruct:

```
HasE [] (app c3 n)
  (inst (all (pi End (pi A (Leaf originalQ)))) n)
```

This positive certificate reconstruction is source-syntactic and does not call model soundness, Church standardness, or the prior closed-instance theorem. A declaration dependency audit checks that separation. It uses the independently typed iteration, actual conversion/identity/introduction rules, scope, and the inherited source atom-packing bridge. It does not infer `HasE [] n N` from JSON. Closed scope plus successful scalar-iteration certificates suffices for this particular positive reconstruction; the HasE premise supplies the general search-termination domain.

## Why this is not duplicate inherited work

- `EffectiveStandardness.semantic_church_standardness` already gives the uniform count existentially on the inherited closed raw carrier. That logical conclusion is not claimed as new.
- `ClosedProofCanonicalisation` canonicalizes a proof polynomial only after an identity derivation is supplied. It does not supply count extraction or strategy termination.
- Inherited `P01Certificates` already performs finite address replay and join checking. The new checker adapts that mechanism to the actual open carrier and reflects into original source `PolyConvPlus`; finite replay itself is not claimed as new.
- P01's Python `first_step`/`normalise` already implements bounded root-first, left-to-right reduction on its frontend syntax. P03's source correspondence explicitly covers finite head-step traces, not full normal-order completeness. Another bounded leftmost evaluator would have been duplicative.
- `P01Confluence` supplies the parallel-development triangle and Church–Rosser machinery. No inspected file supplies a normal-order completeness theorem for arbitrary weakly normalizing `HasE` terms. Church–Rosser alone is not asserted to do that.

The additional checked work is the complete-development cofinality/termination route, its computable count reader on the actual generic-open source input, and explicit scalar certificate emission/replay preserving the actual source endpoints.

## Termination argument and exact carrier

The carrier is unchanged `OpenTermStandardness.T`, with variables, I/K/S, inert literal zero/one, and application. No alternate object language or marker substitution is introduced. The open parallel relation and `dev` are a minimal port of inherited `P01Confluence`, adding the required inert-variable case.

The strategy develops a finite tree as follows:

- `I x` develops to `dev x`
- `K x y` develops to `dev x`, discarding y
- `S f g x` develops to `(dev f)(dev x)((dev g)(dev x))`
- A nonredex application develops its children

The inherited triangle argument gives `Par t u → Par u (dev t)`. Applying it again gives monotonicity `Par (dev t) (dev u)`. Iterating monotonicity shows that reaching a parallel-normal form by complete developments is preserved in both directions along each parallel step, hence along compatible SKI conversion. Thus anything convertible to a normal form reaches it under this strategy. `redexFree_normal` explicitly relates ordinary absence of compatible SKI redexes to the parallel-normality premise; no equality `dev t = t` is used as a stopping criterion.

The closed-input theorem gives conversion to an exact generic-open iteration, which is proved normal. This yields finite strategy termination. No strong normalization, bare `n → literal numeral`, fresh-marker erasure, universal-source completeness, or normal-order standardization is used.

## Meaningful adversarial boundary

`DomainControls.padded_has` proves actual `HasE [] (K numeral(k) Ω) N` using the real conversion rule. No typing of Ω is needed. `padded_not_SN` proves that this same closed input is not strongly normalizing: compatible reduction can follow the inherited three-step Ω cycle in the discarded argument. The chosen complete-development strategy still discards that branch and extracts k.

This prevents accidentally applying inherited `finite_SN`, whose premise is the narrower `FiniteDerives` judgement, to arbitrary `HasE`. Packed-atom controls also prevent silently treating `.atom (app r t)` as source `.app (.atom r) (.atom t)` without the actual bridge.

## Guarantee boundaries

- The Lean mathematical extractor is total on the supplied `HasE [] n N` domain. Its proof uses ordinary `propext`, `Classical.choice`, and `Quot.sound`; no new axiom, admitted proof, unsafe proof, or native evaluator oracle is added.
- The Python producer is resource-bounded. Fuel, node, step, memory, or host-recursion exhaustion is inconclusive, never evidence of inequivalence or source nonderivability. Its fixed budgets do not implement a total physical machine for all finite inputs.
- The proof concerns the exact mathematical `dev` sequence. The Python program is independently checked on successful outputs, not claimed to have been extracted from Lean or formally verified as a whole Python/JSON runtime.
- A source symbol is exported to JSON by Lean from the actual `originalQ` and literal numeral constructors, then rebound on replay. JSON contents, claimed counts, and claimed types are never trusted as kernel evidence.
- No efficiency, asymptotic bound, or improvement over inherited leftmost reduction is claimed. Complete developments can duplicate large trees; retained resource-limit controls make this visible.
- Successful finite certificates prove the concrete scalar instance, not the unconditional bound-variable judgement `HasE [] c3 (W originalQ)`. That universal target and its negation remain OPEN.

## Separate partial rejection of the input domain

`NonstandardRejection.checked_non_iteration_refutes` is a small, distinct consequence. If finite address replay proves that the generic-open `scalarLeft n` reaches z, the executable `normalB` checker certifies that z has no compatible redex, and exact iteration readback returns none, then `HasE [] n N` is impossible. Standardness plus normal-form uniqueness supplies the contradiction. The literal source input `.atom .zero` is checked with an empty trace: `((zero var(1)) var(0))` is a non-iteration normal form.

This is a sound **partial rejection certificate for closed Church-input typing**. It is not a typability decision procedure, a rejection of the scalar-instance target, or a claim that every untyped input produces such a certificate. The Python `normal_non_iteration` response remains an untrusted candidate until the corresponding kernel premises are checked; no resource refusal is promoted to rejection.

## Executed controls

Fifteen adversarial Python tests pass. Ten finite certificates have kernel replay for literal numerals 0–6, compound-atom-packed numeral 3, I-wrapped numeral 4, and discarded-Ω numeral 2; each preserves its literal input and actual original q and produces the exact source instance. Four additional kernel controls reject invalid addresses, a forged endpoint, and a forged count. An open erased-coordinate input yields conversion only, with no closed-source-instance export. A forged count of 10^18 is rejected without allocating a corresponding iteration tree.

The numeral-6 diagnostic explicitly exhausts its 200,000-node allowance, then succeeds with a 5,000,000-node allowance. Both outcomes are retained. Zero development rounds and an eight-round Ω run also produce `RESOURCE_INCONCLUSIVE`. These are resource tests, not the general termination proof.

## Replay and preservation

Run `python3 replay.py` from this directory. Replay verifies the pinned Lean binary, predecessor receipts/source hashes, and reused checked objects; builds only the addition into a fresh local output directory with `--trust=0`; re-exports the original source AST; runs adversarial Python tests; regenerates and independently kernel-checks finite certificates; and checks semantic-dependency separation. It does not rebuild the inherited module closure or modify any predecessor.

Final replay records, source bindings, and independent-review disposition are retained separately. See the replay result for exact executed case counts and resource outcomes rather than interpreting test examples as the proof of general termination.
