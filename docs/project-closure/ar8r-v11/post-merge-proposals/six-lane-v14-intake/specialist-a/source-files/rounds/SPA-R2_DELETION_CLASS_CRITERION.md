# SPA-R2 — hypothesis-class deletion criterion

**Status:** specialist-local mathematical result; elementary standard
restriction/fibre criterion; no novelty or new theorem identity.

## Typed statement

Let `X` be a finite set of experiment cells, `Y` an output alphabet,
`H ⊆ Y^X` a declared hypothesis class, and `D ⊆ X` the observed cells. Define
`res_D : H → Y^D` by restriction.

Then the observed cells identify members of `H` exactly when `res_D` is
injective. Equivalently, there are no distinct `h,h' ∈ H` that agree on every
cell in `D`.

## Proof

This is the definition of injectivity unpacked. A noninjective restriction map
supplies two distinct hypotheses with the same observed restriction, and any
such pair witnesses noninjectivity.

For the unrestricted response-table class `H = Y^X`, if `|Y| ≥ 2` and `D` is a
proper subset, choose an omitted cell and alter only that cell. The resulting
profiles collide on `D`.

The unrestricted corollary does **not** transfer to a constrained `H`.

## Deletion models

- Unrestricted binary tables on three cells remain nonidentifiable after one
  cell is deleted.
- The even-parity class `y2 = y0 XOR y1` is identified by cells 0 and 1, even
  though cell 2 is absent.
- The constant-profile class is identified by one cell even when two cells are
  deleted.

Thus “one missing factorial cell always destroys identification” is false
without an unrestricted-table or equivalent richness assumption.

## Executable evidence

The checker exhausts every nonempty binary hypothesis class for `|X|=1,2,3`
and every deletion set: 2,106 class/deletion cases, zero criterion mismatches.
It separately checks all 11 proper deletions of unrestricted binary tables.

Five mutants are killed, including the universal-deletion claim, an
`n-1`-cells sufficiency claim, repeated-twin acceptance, prefilled counters, and
a cell-count-only criterion.

## Lean status

`lean/DeletionCriterion.lean` drafts the exact criterion. Source is present;
parse, elaboration, kernel checking, project build, and axiom reporting were not
run because no Lean binary was available in the runtime.

## Conclusion ceiling

Identification is relative to the declared hypothesis class. No actual
architecture class, causal semantics, source truth, or metaphysical target is
identified by this result alone.
