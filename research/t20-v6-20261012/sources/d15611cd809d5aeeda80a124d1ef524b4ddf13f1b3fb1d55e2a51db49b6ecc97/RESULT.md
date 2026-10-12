# Full-polynomial Schur countermodel: complete algebraic Lean proof

10 October 2026 UTC. This is a new additive artifact. It does not modify the
ordinary construction packet, protected sources, integration state, or T20
closure. No field-novelty claim is made.

## Checked result

`FullPolynomialCountermodel.full_polynomial_countermodel` constructs a real
linear map on the actual type `MvPolynomial (Fin 2) ℝ` with:

- `L 1 = 1`;
- for every nonzero real polynomial `p`, without any degree cutoff,
  `0 < L (p ^ 2)`;
- one actual polynomial `witness` whose value is at least `3/4` under every
  assignment of the two variables;
- `L witness = -1`.

The final theorem has no positivity, matrix-existence, moment-existence,
finite-degree, or representation assumptions. This is not a theorem that
merely assumes its desired functional exists or is positive. The functional
is defined and its positivity derived from its explicit infinite recursion.

The witness is

    1 + X₀⁴ X₁² + X₀² X₁⁴ − X₀² X₁².

`not_pointwise_positive` derives failure of positivity on all pointwise
nonnegative polynomials. `finite_sum_squares_nonnegative` derives
nonnegativity on every finite sum of squares.

## Proof chain

1. `Indexing.lean` defines the exceptional first ten monomials and subsequent
   degree shells. It proves the forward-index formula, bijection onto positive
   naturals, all-degree midpoint precedence, and first-four parity separation.
   `exponentAt` is the zero-based inverse, with both inverse laws proved.
2. `Schur.lean` proves the completed-square identity and positivity of the
   appended matrix directly from finite real sums. It also proves that the
   explicit updated inverse really multiplies the matrix to the identity.
   No unavailable positive-definite/Schur-complement library is imported.
3. `Recurrence.lean` supplies recursively growing finite index types,
   their positions, the actual diagonal seed matrices, and universal
   preservation of symmetry, inverse, and strict quadratic-form positivity.
4. `Moment.lean` instantiates the column with precisely the even midpoint
   moments of the preceding state. Midpoint precedence proves the column
   only uses prior assigned moments. It proves old moments never change,
   constructs one infinite sequence, and proves every finite moment Gram
   matrix equals the corresponding recursively constructed matrix and is
   positive definite. The four separating moments are proved from the seed.
5. `PolynomialBridge.lean` defines an actual linear map by finite monomial
   coefficients. It proves that every polynomial has coordinates in some
   recursive finite index set and that applying the map to its square is
   exactly the Gram quadratic form. Its generic Gram-positivity premise is
   discharged by the proved recurrence in the final theorem.
6. `Countermodel.lean` instantiates that bridge and proves normalization,
   unbounded strict square positivity, the negative witness value, and the
   positive pointwise lower bound. `ScalarSupport.lean` is copied byte-for-byte
   from the preceding packet and supplies only the scalar inequality.

## Exact recurrence interpretation

At state `n`, the matrix has `n+4` indices, whose positions are `0,…,n+3`.
The newly appended monomial has one-based index `n+5`. Its column is the old
moment sequence at each parity-compatible midpoint, and zero otherwise.
The new diagonal is `1 + vᵀ B v`, and the inverse update is exactly
`[[B+wwᵀ,-w],[-wᵀ,1]]`, with `w=Bv`.

A finite state's `J` is a total function, initially equal to 1 outside its
four assigned entries. Those arbitrary tail values are never used for a new
column: `column_precedes` proves that fact universally. Subsequent states
update just the newly assigned index. `state_J_stable` and
`state_J_compatible` prove prefix agreement. Defining the global value at
index `k` from state `k` is therefore safe, and `J_eq_state` proves it agrees
with every sufficiently long state. The matrix-to-functional connection is
an equality theorem, not a postulate.

## Scope boundaries

The algebraic full-polynomial countermodel is formalized. The following
additional statements from the ordinary proof are not claimed as Lean theorems:

- dyadic-rational/executable computability of every moment;
- the explicit integer-square-root inverse-enumeration algorithm;
- the determinant invariant `det Aₙ = 4`;
- the positive-Borel-measure/integral representation corollary.

The inverse enumeration used here is noncomputable classical choice from a
proved bijection. Real arithmetic and the real linear map are also represented
noncomputably, as usual in this part of Mathlib. The source algorithm remains
the separate exact rational implementation. The ordinary measure contradiction
follows from the checked positive polynomial and negative functional value,
using positivity of integration, but that measure-theoretic step is not part
of this Lean package.

## Replay and trust

Run `python check_full.py` from any directory in this retained workspace.
The script compiles all seven sources with the retained Lean 4.19.0 executable
at `--trust=0`, checks the printed theorem axiom dependencies, runs three
mathematical negative controls, and records exact selected import objects and
source hashes through the full explicit import closure. It never rebuilds
missing baseline modules. `LEAN_RECEIPT.json` records the result and scope.

Only the standard Lean axioms `propext`, `Classical.choice`, and `Quot.sound`
occur in the checked target dependencies. The sources introduce no axiom,
`sorry`, `admit`, `native_decide`, or replacement implementation escape hatch.
The retained toolchain and Mathlib objects are prerequisites; the packet does
not bundle or reinstall the baseline toolchain.
