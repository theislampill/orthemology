# Independent tagged-row actual-law audit

## Disposition

PASS within the sealed semantic scope. No mathematical defect found in the actual prefix/tail law, unary selector, tagged mass identity, or Pi3-shaped endpoint equivalence. This report does not credit later finite-prefix selector/observer additions, numeric-code reduction or hierarchy completeness.

Exact archive: `private-locator:2ffbe7601c64d797b9e5`

SHA256: `7f1dc1ecce6717ff02cd9349dfe96635e3e0741e87291ca80f3de13f66b88ca9`

Exact author receipt: `private-locator:e8582bd6b9284396092a`

SHA256: `294054cc309ac7cf86e4193b8f1d8e098694fe20c2b21304cf13a183967dbafc`

The archived sealed-v1 bytes, manifest hashes and all 23 source hashes were checked. They still match their origins. The audit's independent complete receipt is `TAGGED_STAGE_AUDIT_RESULT.json`, SHA256 `0d3e33fad485a2aff625017ae3044eafbb842a66866f11b9f672845020dba27d`.

## Independent reproduction

The preserved completed receipt records all 23 custom source modules plus Audit compiling into `tagged-build` with exit 0. The local import path used that fresh build and only pinned official Mathlib/package caches; no author project olean directory was used. Commands used Lean 4.19.0 commit `6caaee842e94`, `-j1`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

The 35 named new theorem readbacks have axiom footprints contained in `{propext, Classical.choice, Quot.sound}`. The additional independently authored `TaggedBoundaryWitnesses.lean` has six checked endpoint readbacks with the same ceiling. Its SHA256 is `1bceade046b558d9b76b2d52018b3df7076a13fbda9c4b14f73844c2bad50474`; its successful readback log SHA256 is `7f01fb52e268b02e79b472b74c452cc0258ba3801d46dca31f7ae0a8ba339367`.

A coordination/context gap later caused an unnecessary restart that regenerated seven dependency outputs from identical sources before stopping. It is not credited as a second complete build. The original complete JSON receipt and aggregate Audit/boundary logs remain preserved. `TAGGED_RECONCILIATION.json` records the current hash reconciliation, and `tagged-redundant-partial.log` preserves the partial restart. No original source or canonical repository was changed.

## Prefix/tail disintegration

`PrefixTail.finite_tail_prefix_event` identifies the actual event of a prescribed N-bit prefix plus a finite tail pattern with a literal product cylinder on coordinates `range N ∪ {N+k : k∈I}`. `combined_card` proves the two coordinate sets are disjoint and the shift injective, so their total size is `N + |I|`. Thus finite product probabilities factor without assuming independence between overlapping or conditionally chosen coordinates.

The tail is `dropBits N x k = x(N+k)`. `restricted_tail_law` proves the entire unnormalized pushforward

`(fairCantor restricted to the fixed prefix).map(dropBits N) = 2^(-N) • fairCantor`.

It first proves every finite projection equality on singleton patterns. Each finite Boolean projection space is finite, so equality on singleton masses gives equality of projection measures. The full equality then follows from the projective-limit uniqueness theorem. This is not an unjustified leap from one finite horizon, nor an assumed conditional-independence axiom. N=0 and empty finite tail sets are included.

## Selector, all-true branch and mixture law

`tagEvent i` is exactly i true bits followed by false. Its tag length is i+1, and the untouched tail begins at i+1. `tagged` selects the first false bit using Nat.find when one exists and returns allTrue on the actual all-true input. Thus the observer remains defined on every input.

The tag events are pairwise disjoint. They do not cover every input: their complement is precisely `{allTrue}`. The source fair-Cantor singleton theorem makes this complement null, establishing almost-everywhere coverage. `fairCantor_sum_restrict` uses that measured fact to express the source as the sum of its restrictions. The all-true branch is omitted only after its null contribution is proved.

Measurability is proved by decomposing preimages into the countable measurable tagged pieces plus the singleton branch. On each selected branch, the actual output equals `tag i (rows i (tail i x))`. Prefix/tail disintegration gives that branch's pushed-forward law, and `map_sum` gives the full actual tagged-mixture law. The output tag is echoed in the correct positions; no off-by-one selector coordinate is fed into the row as its first supposedly fair tail bit.

This sealed top-level definition is noncomputable because it asks whether an arbitrary infinite input ever contains false. The theorem is a measurable observer semantics result. It does not itself prove a finite-prefix executable implementation; that is a separate later addition.

## Positive-singleton mass and weights

The append-tag map has the measurable left inverse `tail i`: `tail i (tag i y) = y`. `tag_mass` applies mass monotonicity first along tag and then along this left inverse, obtaining exact mass preservation. It does not rely on arbitrary injective maps having measurable inverses, nor conflate positive-singleton mass with a different atomicity notion on general measurable spaces.

The imported countable mixture theorem uses the countable union of the component positive-singleton supports, proving exact linearity of mass even where component supports overlap. The tagged construction then yields

`mass(actual tagged law) = sum_i 2^(-i-1) * mass(row law i)`.

`weights_sum` proves exact normalization, and `weight_ne_zero` proves every row's weight is strictly positive. `weighted_full_mass_iff` combines positivity, normalization and each row mass ≤1. If one row has strictly deficient mass, its positive weighted term gives a strict deficit in the total sum. No zero-weight row can be hidden in the universal conclusion.

The row laws are probabilities by measurable pushforward, which supplies the required row-mass bounds and avoids invalid ENNReal-toReal reasoning at infinity. `defect_zero_iff_mass_one` is handled by the precise toReal-equals-one theorem. All underlying probabilities are finite.

## Pi3-shaped equivalence

The rows are the already-audited least-surviving-candidate observers. The actual full law has zero defect exactly when each row has zero defect, and each row has zero defect exactly when it has a witness. The result therefore preserves the order

`forall i, exists s, forall t, R(a,i,s,t)`.

The complementary positive-defect statement is exactly

`exists i, forall s, exists t, not R(a,i,s,t)`.

Nonnegativity is proved from probability mass ≤1 before replacing nonzero defect with strictly positive defect. The witnesses may depend on i; no uniform s is asserted. The top-level matrix family only requires decidability at each row, so this equivalence is a semantic quantifier normal form rather than a proof of an effective Pi3 index-set classification.

## Six independent boundary endpoints

`tagged-sources/TaggedBoundaryWitnesses.lean` and its successful log establish:

1. `no_pointwise_selector_cover`: allTrue refutes pointwise coverage by the unary selector events
2. `unshifted_prefix_coordinate_not_fair`: on selector-zero, the selector bit is fixed false, so treating coordinate zero as a fresh fair tail bit is false
3. `zero_weight_hides_bad_row`: without strict positivity, weighted mass can equal one while a zero-weight row has deficient mass
4. `row_witnesses_need_not_be_uniform`: the matrix `R(i,s,t) := (s=i)` gives zero defect with separate row witnesses but no single witness for all rows
5. `tagged_mixed_mass_half`: making row zero constant and every other row the identity gives actual atomic mass 1/2
6. `tagged_mixed_defect_half`: the same actual tagged observer has defect 1/2

The last example also prevents confusing the full tagged law with an endpoint-only row dichotomy: the aggregate defect need not be zero or one.

## Exclusions

No claim here extends to the subsequently authored PrefixBits, FiniteSelector or PrefixObserver files before their own immutable receipt is audited. No numeric-index translator, PR completeness, byte-code correspondence, computability/hierarchy hardness, general effective arity-index classification, novelty, canonical adoption, or physical/ethical interpretation is established. The exact sealed actual-law and quantifier statements above do pass.
