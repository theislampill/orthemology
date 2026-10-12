# Rational unary-shift realisation: substantive formal bridge

## Result

Lean 4.19.0 checks a complete **alternative unary-tag rational shift** in the unchanged original P02-L1 evaluator. For every fixed jointly primitive-recursive family `F(e,n,word)` and fixed natural `a,b` with `0 < b` and `a ≤ b`, there exists one fixed `Program 3` whose concrete literal-specialized numeric indices are primitive recursive in `e`, whose output is pointwise equal to the new unary construction, and whose actual fair-source defect is

`a/b + (1-a/b) * defect(fairCantor.map(output(F e)))`.

This closes the proposed alternative-construction compiler/output-law gap. It does **not** verify the original Python `compile_shift` syntax or supply a PR universal interpreter. The ordinary rational threshold classification is predecessor work, not newly credited here. T20 remains active; no closure or repository adoption is claimed.

## Exact new proof chain

1. `weights/BinaryWeights.lean`, namespace `RationalBinaryWeights`:
   - Quotients `floor(a*2^n/b)` obey the binary recurrence.
   - Boolean digits are primitive recursive, also jointly in their numeric inputs.
   - The finite weighted sum telescopes; its error is bounded by `2^-n`.
   - `binary_hasSum` and `binary_tsum` prove the exact real series for `a<b`.
   - `closedDigit` handles `a=b` by all true digits; `closed_binary_tsum` covers the entire closed unit interval, including zero. Further `ℚ≥0` and ENNReal interfaces are proved.
2. `compiler/UnaryPrefixRealisation.lean`, namespace `OrthemologyTagged.UnaryPrefix`:
   - `prefixValue` scans only the given `n+1` input bits, preserves the unary tag and zero terminator, then uses either the source bit or a freshly re-encoded suffix sentinel for `F`.
   - `prefixValue_output` proves exact pointwise output equality with tagged rows, including the all-true input, not merely almost-everywhere equality.
   - Suffix construction and the whole evaluator are jointly PR for fixed jointly PR `F` and PR digits.
   - `exists_primrec_numeric_family` invokes existing checked PR coverage, fixed-program compilation, concrete numeric specialization and PR index coding.
3. `UnaryShiftLaw.lean`, namespace `OrthemologyRationalShift`:
   - `unaryShift_mass` proves actual output atomic mass is the complementary digit weight times base atomic mass.
   - `unaryShift_defect` and `unaryShift_defect_of_weight` prove the actual affine law, using the unchanged tagged-mixture theorem.
   - Complement weights and endpoint laws are proved, not assumed.
4. `RationalShiftRealisation.lean`:
   - `exists_primrec_rational_shift` combines the exact pointwise numeric output theorem and rational actual-law identity.
   - `exists_primrec_pi3_threshold_reduction` composes with the unchanged fixed jointly PR Pi3 prefix family: for every `a<b`, a single PR map reduces that Pi3 condition to both defect `= a/b` and defect `≤ a/b`, and its complement to defect `> a/b`.

5. `Sigma2ThresholdRealisation.lean`:
   - `exists_primrec_sigma2_threshold_reduction` gives one PR numeric index map, independent of the threshold, with the exact baseline Sigma2 row defect.
   - For every real `0<r≤1`, simultaneously `D<r` is equivalent to `∃s∀t R` and `r≤D` to `∀s∃t ¬R`. This composes the checked zero-shift with the already proved 0/1 dichotomy. It supplies the remaining Sigma2/Pi2 lower compiler assurance.

## Endpoint, null-set and totality checks

- `q=0`: all digit choices are base rows; defect is unchanged, although the tagged output is a different stream map.
- `q=1`: all rows are identity, and actual defect is one. No Pi3 hardness claim is made at this constant endpoint. The raw quotient digit convention is **not** used there.
- The unary selector's all-true input is defined and produces allTrue at every finite stage. The compiler equality explicitly includes it.
- Only measure transport discards that singleton, through unchanged `selector_cover_ae` / `tagged_mixture_law`; nullity does not replace productivity.
- Tail invocation uses the original sentinel of precisely the suffix after the tag zero; it does not pass the old word or old stage to the base evaluator.
- Every observer index in the theorem is an actual index of the original numeric L1 evaluator, obtained from one fixed program.

## Boundaries and ownership

The new programme is a unary-tag/list-suffix construction. It is not byte-for-byte, syntax-for-syntax or stage-for-stage the Python rational-cell stopping-prefix compiler at `P02/code/prcodec.py:293–310`. Literal `compile_shift` verification remains owned by that source/compiler bridge: formal bounded cell scan, stopping partition masses and output-reset theorem are still required if that exact compiler is the target.

PR coverage is existential for an already fixed jointly PR family. The theorem does not extract code from erased proof arguments, prove a PR map from arbitrary program syntax, or turn the uniformly computable variable-index interpreter into a jointly PR evaluator. Its effective map is the checked `parameterIndex p` for the resulting fixed `p`.

The upper-cut extension and 77 baseline source modules are untouched. This work uses their cached objects and exact original Mathlib cache, with no reacquisition. Historical baseline comments saying UNEXECUTED have not been rewritten; current replay receipts determine the actual verification status.

## Reproduction and controls

Run `python rational-shift-realisation-20261011/verify.py` from the workspace. It rebuilds all five new modules in a fresh directory under `--trust=0`, rejects warnings and sorryAx, checks preserved baseline/upper hashes, and performs six compile-failing mutation controls:

- q=1 wrongly assigned all false digits
- failure to drop the tag's zero terminator
- base evaluator given the unreset word
- law branches reversed
- Sigma2 threshold guard incorrectly includes zero
- Sigma2 threshold guard incorrectly permits values above one

`AUTHOR_REPLAY.json` records exact source/object hashes and logs. Independent review, when provided, is separate from this author report.

Accepted source membership is exactly the five entries in `FROZEN_SOURCE_MANIFEST.json`. Files under `replay-*` named for mutation controls deliberately fail; `exploratory-not-accepted/Check.lean` contains API exploration and is not a proof artifact. No test or exploratory source belongs to the accepted theorem set.

`ORIGINAL_SOURCE_BINDINGS.json` rechecks every source pin inherited from the predecessor gap inspection, including the untouched literal Python compiler, and binds the existing baseline/cache manifests.
