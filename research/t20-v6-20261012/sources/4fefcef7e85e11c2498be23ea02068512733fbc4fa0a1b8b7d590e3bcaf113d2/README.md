# Checked generic unary-prefix realisation

Run from `private-locator:8f24556a330b05a11a95`:

```sh
bash rational-shift-realisation-20261011/compiler/check_unary_prefix.sh
```

The script uses the unchanged baseline/cache search path from `rational-threshold-formal-extension-20261011/lean_path.txt` and local Lean 4.19.0. It creates the object and log only in this compiler directory.

## Main theorem

`OrthemologyTagged.UnaryPrefix.exists_primrec_numeric_family` proves that for each fixed joint primitive-recursive family `F : Nat → Nat → Nat → Nat` and fixed primitive-recursive `D : Nat → Bool`, there exists one fixed ternary LOOP program `p` such that:

- its concrete numeric specialization map `P02.Codec.parameterIndex p` is primitive recursive;
- for every parameter `a`, its output is exactly `tagged (rows F D a)`;
- `rows F D a i` is identity if `D i` is true, and `output (F a)` otherwise.

The equality is pointwise on all infinite Boolean sources, including `allTrue`. This is a fixed-family theorem, not a claim that arbitrary primitive-recursive syntax has a joint primitive-recursive universal evaluator. It is an alternative unary-selector construction and does not verify the separate Python `compile_shift` implementation.

## Checked proof chain

- `drop_prefix`: dropping `i+1` bits from the finite original prefix gives exactly the finite prefix of `tail i x`.
- `suffixWord_prefix`: the dropped finite suffix is re-encoded with the original sentinel convention.
- `prefixValue_output`: full pointwise semantic equality, before a tag, at its zero terminator, and after it, plus `allTrue`.
- `prefixValue_allTrue` and `prefixValue_at_stop`: explicit all-true and tag-stop corollaries.
- `suffixWord_primrec` and `prefixValue_primrec`: joint finite-input PR proofs, total also on malformed numeric inputs.
- `family_primrec` and `exists_fixed_program`: one fixed ternary LOOP realization.
- `numeric_observer_eq` and `exists_primrec_numeric_family`: concrete codec specialization and primitive-recursive index map.

`#print axioms` on the main semantic, PR, and numeric realization theorems reports only `propext`, `Classical.choice`, and `Quot.sound`. There are no `sorry` or added axioms. The baseline and frozen upper sources were not edited.
