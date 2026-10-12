# Rational binary weights: kernel-checked deliverable

The source `BinaryWeights.lean` has been compiled with the existing Lean 4.19.0 toolchain and pinned cached mathlib environment using `--trust=0`. No baseline or existing rational-threshold source was modified. This is a Lean theorem result, not a claim of verification of any Python shift compiler.

## Direct interface

All declarations are in namespace `RationalBinaryWeights`.

- `weight (i : ℕ) : ℝ := (1/2 : ℝ)^(i+1)`.
- `digit (a b i : ℕ) : Bool := decide ((a * 2^(i+1) / b) % 2 = 1)` (via `quotient`).
- `closedDigit a b i := if a = b then true else digit a b i`.
- `rationalDigit (q : ℚ≥0) : ℕ → Bool := closedDigit q.num q.den`.
- `rationalDigit_primrec (q : ℚ≥0) : Primrec (rationalDigit q)`.
- `rational_binary_tsum (q : ℚ≥0) (hq : q ≤ 1) : (∑' i, if rationalDigit q i then weight i else 0) = (q : ℝ)`.

The last pair gives the concrete primitive-recursive Boolean selector and exact selected dyadic weight for every nonnegative rational at most one, including zero and one.

## Additional proved facts

- `quotient_step`: the next quotient divided by two equals the current quotient.
- `digit_step`: the next quotient is twice the current quotient plus the Boolean digit.
- `prefix_sum`: for `a < b`, the selected first `n` weights sum to `(a * 2^n / b : ℕ) * (1/2)^n` in the reals.
- `prefix_bounds`: when `0 < b`, the quotient approximation is at most `a/b`, which is at most that approximation plus `(1/2)^n`.
- `binary_hasSum`, `binary_tsum`: exact series for `a < b`.
- `digit_zero`: every digit for numerator zero is false.
- `weight_hasSum`: all weights have sum one.
- `closed_binary_hasSum`, `closed_binary_tsum`: exact series for `0 < b` and `a ≤ b`.
- `digit_primrec`, `closedDigit_primrec`: primitive recursion for fixed numerator and denominator.
- `digit_uniform_primrec`, `closedDigit_uniform_primrec`: primitive recursion uniformly on `((a,b),i)`.
- `closed_binary_tsum_ennreal`: corresponding ENNReal sum equals `(a : ℝ≥0∞) / b`.

## Reproduction

From any directory:

```sh
bash private-locator:fe60cd1a8026982b79c3
```

The script sets `LEAN_PATH` from the unchanged existing `lean_path.txt`, adds this directory, and invokes the existing compiler with `--trust=0`. It emits `BinaryWeights.olean`, `BinaryWeights.log`, and `SHA256SUMS`. The exported axiom checks report only `propext`, `Classical.choice`, and `Quot.sound`; they do not contain `sorryAx`.

To use this file, include this `weights` directory in `LEAN_PATH` and write `import BinaryWeights`. The real series theorem uses precisely `(1/2)^(i+1)` weights; an enclosing shift theorem can unfold `weight` if its local notation uses that expression directly.
