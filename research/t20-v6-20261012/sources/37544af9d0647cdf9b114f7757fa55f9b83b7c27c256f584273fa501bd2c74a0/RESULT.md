# Full-polynomial moment countermodel: result and verification scope

The proposed rational Schur-completion construction works. It gives one
normalized real linear functional on the entire bivariate polynomial algebra,
strictly positive on every nonzero polynomial square, while assigning −1 to an
everywhere-positive polynomial. Hence no positive representing measure exists.

## Mathematical evidence

`PROOF.md` proves the monomial bijection, the global midpoint-precedence lemma,
and an explicit total dyadic recursion. Only the nine exceptional small
parity-compatible pairs need enumeration; arbitrary larger degrees are handled
symbolically. A simultaneous induction proves exact inverses and real positive
definiteness of every finite Gram matrix. Finite support then gives the universal
polynomial assertion. This is a full-algebra result, not a truncated positivity
claim or an inference from a numerical prefix.

`RANK_SUBSTITUTION.md` shows that this explicit full functional supplies exactly
the four B properties used by the existing partial-damping Gaussian-mixture
counterpath, preserving its witness value −1 and all-time negative bound. It
does not edit or rerun the rank-classification packet.

The seed witness is F=1+x⁴y²+x²y⁴−x²y². The proof establishes F≥3/4 globally and
ΛF=−1. The source convention and seed values are classical. The explicit later
diagonal choice is jₙ=1+vₙᵀAₙ₋₁⁻¹vₙ, implemented with an elementary inverse update.

## Executable evidence

Run from the containing workspace:

    python3 full-polynomial-moment-countermodel-20261010/check_exact.py
    python3 full-polynomial-moment-countermodel-20261010/countermodel.py --prefix 25
    python3 full-polynomial-moment-countermodel-20261010/lean-support/check_support.py

The exact checker records 37,588 passed assertions. Through index 25, independent
Gaussian solves agree with the inverse-update implementation, and independent
LDL factorization reconstructs every Gram matrix with pivots 1,1,1,4,1,1,… .
The determinant is 4 from index 4 onward. Exact prefix output, finite-check
receipt and log are preserved. Incorrect Schur sign, zero-tail continuation,
wrong witness value and assumed diagonal monotonicity are negative controls.

The Lean scalar support passed Lean 4.19.0 at trust level 0, with only the
standard axioms propext, Classical.choice and Quot.sound. It proves the global
scalar lower bound and seed arithmetic. Two false-claim controls are rejected.

## Exact limits

- The universal recurrence, its Gram induction, the actual linear functional
  and the no-measure result are written mathematical proofs, not yet Lean proofs.
- The retained lower-level matrix algebra and MvPolynomial modules load. Direct
  PosDef and SchurComplement imports are absent and would require hundreds of
  missing dependency objects. No baseline rebuild was launched. The support
  report describes a prospective elementary route avoiding those large imports.
- This is different from the earlier ternary truncated Lean functional. It does
  not extend that functional's moments or repair its higher-degree zero tail.
- No growth condition, coercive dynamical law, heat equation solution, computable
  representing measure, integration into protected text, or T20 closure is claimed.
- The source PDF's searchable text was inspected, but page screenshots returned
  cache misses. No visual verification is claimed.
- This artifact contains no independent human/adversarial review verdict; that
  remains a separate assessment. The second arithmetic implementation is an
  independent algorithm inside the author's verification script.

Prior-art credit: J. Friedrich's explicit nonmoment example, as presented in
Konrad Schmüdgen, *The Moment Problem*, Propositions 13.4–13.5, pp. 318–319;
attribution in §13.12, p. 355. The alternative recurrence and its use here carry
no field-novelty claim.
