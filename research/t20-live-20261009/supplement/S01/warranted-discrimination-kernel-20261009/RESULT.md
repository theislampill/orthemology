# Kernel certification of the canonical residual-certificate theorem

9 October 2026. Bounded mathematical continuation; no protected repository changes, integration, adoption decision, or programme closure.

## Result

The substantive canonical frontier theorem in §3 / Theorem 1 of `warranted-discrimination-research-20261009/RESULT.md` is now kernel checked in Lean 4.19.0. The development proves all four clauses at the finite support/cost-pair level:

1. Removing dominated pairs preserves the least terminal checking cost after every evidence addition.
2. The complete cost function uniquely recovers the normalized frontier. Equality of frontiers is both necessary and sufficient for equality of all continuation-cost observations.
3. Subtracting new evidence and then normalizing updates the frontier exactly. Equal frontier states remain equal after every common acquisition.
4. Any summary with a correct decoder for every per-verdict future cost must distinguish different frontier tuples.

This is not merely a support-union lemma or a finite enumeration. The exact inverse formula and its converse are general proved theorems. Three false strengthenings have independently proved finite counterexamples and deliberately rejected Lean mutations.

The original report remains unchanged. Its statement that it did not then claim Lean certification records its own earlier status; this separately bound supplement supplies the narrower certification described here.

## Exact mathematical scope

Let `E` be a type with decidable equality and `C` a linearly ordered type. A pair is a finite support together with a price in `C`. A catalogue is a finite set of such pairs. The product order compares support inclusion and price simultaneously. Its `frontier` retains precisely the minimal elements.

`cost A U` is the infimum over the finite catalogue, using a pair's price when its support is contained in `U`, and otherwise a newly adjoined top element. Thus the output type is `WithTop C`; the empty minimum is top. The theorem requires no arithmetic or price nonnegativity. Consequently it applies in particular to the manuscript's finite nonnegative real prices. The checked code is generic in `C`; it does not import or separately instantiate Lean's real-number library.

This order-theoretic generality does not silently permit an infinite verification price to be identified with infeasibility. Each catalogue price is embedded into `WithTop C`, strictly below its new top. If `C` itself has a top, that embedded value remains distinct from the output top. A separate control demonstrates the failure when those two levels are intentionally collapsed.

`E` need not be finite globally, but every support, inventory, and acquisition set is finite. This includes the manuscript's finite token universe, where every subset is represented. Catalogue finiteness and the declared persistent set-difference acquisition law remain explicit.

Each fixed scoped verdict has its own catalogue. The per-verdict theorem does not erase verdict identity or silently optimize across different conclusions. No probability model, truth oracle, philosophical premise, source-trust hypothesis, or proof-admission axiom is introduced into the Lean development.

## Certified statements

| Lean theorem | Substantive content |
|---|---|
| `exists_frontier_le` | Every original pair has an actual retained dominating pair; normalization coverage is derived from finiteness. |
| `cost_le_iff` | At every finite price threshold, the cost bound holds exactly when some original pair is eligible at that price. |
| `cost_frontier` | Pareto normalization preserves the full cost function. |
| `frontier_inverse` | An arbitrary pair `(D,c)` is in the frontier iff `cost A D = c` and deleting any member of `D` strictly raises that cost. The reverse direction does not assume the pair belongs to the catalogue. |
| `frontier_eq_iff_cost` | Canonical necessity and sufficiency across arbitrary finite catalogues. |
| `frontier_antichain`, `frontier_idempotent` | Antichain status and normalization idempotence are proved, not assumed. |
| `cost_residual`, `residual_residual` | Residual cost is old cost at the union of acquisitions; successive residualization composes by union. |
| `frontier_residual_normalize`, `residual_congruence` | Normalizing before acquisition loses no relevant future pair; equality is a congruence. |
| `inventory_cost_recovery` | Theorem 1.1 in the paper's inventory form. |
| `inventory_canonical`, `per_verdict_canonical` | Theorem 1.2 for inventories of fixed verdict catalogues. |
| `inventory_update`, `inventory_congruence` | Theorem 1.3 directly for inventory additions. |
| `inventory_summary_necessity` | Theorem 1.4: a correct fixed-catalogue, per-verdict decoder cannot identify inventories with different frontier tuples. |

The inverse includes the empty-support case: the deletion condition is vacuous, but finite cost equality remains required. Empty catalogues are supported. The code proves no theorem by assuming that a catalogue is already normalized.

The coarseness result concerns equivalence classes under all declared future evidence sets. It does not assert that the frontier is the unique encoding, a minimum physical-RAM representation, or the coarsest quotient for a restricted action menu that cannot realize all those evidence sets.

## Rejected false strengthenings

`Controls.lean` proves the following counterexamples through ordinary kernel reduction (`decide`), without `native_decide`:

- **Cost-blind pruning fails.** Supports `{a}` at price 10 and `{a,b}` at price 1 both survive. With `{a,b}` supplied, the correct minimum is 1; deleting the larger support changes it to 10.
- **Present cost/availability is insufficient.** For one proof requiring `{a,b}`, inventories `{a}` and `{b}` both have present cost top. A common acquisition of `{b}` completes the first for price 7 while leaving the second infeasible. Their frontiers differ.
- **Infinite-price collapse breaks necessity.** Under deliberately altered semantics that identify a certificate's own infinite price with the infeasibility value, a catalogue containing an empty-support infinite-price pair and an empty catalogue have identical cost functions but different frontiers.

Corresponding files in `mutations/` assert the false conclusions. All three compiler runs fail specifically with “tactic 'decide' proved that the proposition … is false.” These are semantic counterexamples, not missing imports, unfilled proof holes, or syntactic-error controls. `replay.sh` fails if a mutant compiles or if its rejection lacks this expected diagnostic.

## Kernel and replay evidence

The original theorem is bound to SHA-256:

`71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28`

Frozen Lean sources:

- `CertificateFrontier.lean`: `5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0`
- `Controls.lean`: `7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132`
- `replay.sh`: `925769666b67cdccae6da51365e58bc4beaf81c7512f3d5673c7f157d3038593`

Run from this workspace:

```sh
bash warranted-discrimination-kernel-20261009/replay.sh
```

The script reuses the existing toolchain and dependency outputs without invoking a build, install, or dependency update. Compilation uses:

```sh
lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/CertificateFrontier.olean" "$HERE/CertificateFrontier.lean"
lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/Controls.olean" "$HERE/Controls.lean"
```

Lean version: 4.19.0, commit `6caaee842e94`. Reused mathlib checkout: `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The actual dependency path is in `inherited-environment.txt`; source and proof bindings are in `BINDING.json`; the fresh replay result is in `CHECK_RESULTS.json` and `kernel.log`.

All 13 printed principal theorem/wrapper dependency sets and all four control dependency sets contain only `propext`, `Classical.choice`, and `Quot.sound`. These are Lean's standard logical dependencies. There are no added axioms, `sorry`, `admit`, `sorryAx`, or native-evaluation proof axioms in the accepted sources. The development is kernel checked but does not claim a choice-free constructive metatheory.

An independent reviewer replayed the frozen core, wrappers, controls, and mutations and found no blocking mathematical or scope-mapping defect. Its revision-bound report is in `independent-review/REVIEW.md`. The coordinating root also performed a separate successful replay in `root-resumed-research-20261009/frontier-kernel-replay`.

## What remains outside the certificate

The Lean catalogue contains support/price pairs, not derivation trees, authentication records, rule checkers, source-trust proofs, or certificate identifiers. `frontier_subset` witnesses an original pair, not an original proof object. Producing an actual checked certificate still needs the reconstruction channel and validity assumptions stated in the manuscript.

This certificate covers Theorem 1's frontier, inverse, update, and quotient mathematics. It does not kernel certify Theorem 2's Bellman recurrence or full-transcript completion criterion, the `2^n` state-count consequence, semantic-cover compilation, or any epistemic/philosophical application. Those retain their separately stated written-proof/review status. In particular, numerical availability is not execution of a terminal check, source authentication is not truth, and a cost optimizer does not establish human knowledge or operative basing.

No conclusion about the Necessary Being, intrinsic necessity, uniqueness, or attribute-ascent arguments is derived here. No new literature search or field-wide originality claim was attempted. All work was confined to this new directory and read-only use of the declared inherited materials and toolchain.
