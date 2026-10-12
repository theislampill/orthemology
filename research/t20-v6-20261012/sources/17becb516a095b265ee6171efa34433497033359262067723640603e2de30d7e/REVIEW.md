# Independent review: posterior-only continuation versus inquiry value

10 October 2026 UTC. Separate additive review; previous author/review seals are unchanged. No integration, release, T20 closure, psychological validation, or field-novelty authority is granted.

## Result

The final root note `../posterior-inquiry-value-20261010/RESULT.md`, SHA-256 `5f6f84b1af7e5049139a381142a791eb7aeebdb57ebf9095e14fa49cfc652fcf`, is correct within its stated scope. The ternary counterexamples genuinely reverse a one-step audit-versus-skip decision despite all-word posterior/status equivalence. The positive-fibre iff, finite-risk binary-audit preservation theorem, and resulting minimal audit cardinality are valid. No blocking issue remains.

The final note also resolves an important modelling ambiguity raised in review: the fixed objects are the posterior matrix `Q=P(Θ|D)` and projective reading of an existing audit variable. The forward conditional law `P(D|Θ)` generally varies with the audit weights. The examples compare joint beliefs under the same fixed-audit instrument; they do not keep that target-conditioned forward likelihood fixed.

## Exact example and sign

For `q_d=(0,1/2,1)` and `t=(a,1−2a,a)`, `0<a<1/2`, the current target law is always uniform. Every constant nonempty word identifies its audit value and returns the specified posterior; any word containing different audit values is impossible. The empty word returns the common current law. This proves universal behavioral equivalence; finite word tests only corroborate it.

Under half the two-coordinate squared loss, binary Bayes risk is `H(p)=p(1−p)`. The expected posterior risk is `(1−2a)/4`, so expected loss reduction is `H(1/2)−E H=a/2`. At `a=1/4` and `1/8`, gains are `1/8` and `1/16`. Subtracting a common cost `3/32` produces `+1/32` and `−1/32`. The sign is loss reduction minus cost; maximizing a reward-based score would require the corresponding sign convention.

The all-positive-cell variant `q_d=(1/4,1/2,3/4)` has gain `a/8`, giving `1/32` and `1/64`, and net values `±1/128` at cost `3/128`. Thus the obstruction does not depend on zero target–audit cells.

For distinct laws `p0,p1`, their midpoint `p*`, and finite strictly concave Bayes risk `H`, the symmetric family's gain is `a[2H(p*)−H(p0)−H(p1)]`. Strict concavity makes the bracket positive; varying `a` changes value. A cost between the two values then reverses the same decision. This concerns the stated finite loss objective and an available skip action, not arbitrary epistemic value or a general adaptive optimum.

## Positive-fibre iff and its necessary domain restriction

Let `Q` be finite and column-stochastic, let `q` be a probability law, and let `F={t>0:Qt=q}` contain `t0`. The normalization `Σt=1` follows from column stochasticity. For any finite real vector `h`, `hᵀt` is constant on `F` iff `h∈rowspan(Q)`.

Sufficiency: if `hᵀ=bᵀQ`, then `hᵀt=bᵀq`. Necessity: for every `v∈ker Q`, a sufficiently small positive `ε` makes both `t0±εv` strictly positive and preserves `Qt=q`. Constancy forces `hᵀv=0`, hence row-space membership. This proof uses the whole fibre, not merely a sampled or reachable subset.

For posterior Bayes risk, put `h_d=H(Q_d)`, requiring these values and `H(q)` to be finite. The expected improvement differs from `−hᵀt` only by the constant `H(q)`. A constant cost adds no missing coordinate; outcome-dependent costs can, and the note correctly requires their own expectation contract.

Without a full-support feasible point the global row-space condition can be too strong. For the same three posterior columns and `q=(0,1)`, the nonnegative fibre is the singleton `(0,0,1)`, so expected half-Brier risk is constant zero although `(0,1/4,0)` is outside `rowspan(Q)`. On a boundary face use the feasible difference space, or equivalently restrict to the active support when that relative fibre has a positive point. On an arbitrary restricted family the exact condition is annihilation of its admissible differences. The final note states the needed restriction.

## Binary-audit theorem and minimal cardinality

For one fixed audit with at most two feasible outcomes and any finite target alphabet, posterior-only equivalent joint laws preserve `E H(posterior)` for every finite function `H` of the posterior law. Thus they preserve the corresponding expected improvement and every common constant audit cost.

When both outcomes are feasible, write the posterior columns as `Q0,Q1`. If they differ, `q=(1−t)Q0+tQ1` determines `t` uniquely: subtracting two such representations gives `(t−s)(Q1−Q0)=0`. If they coincide, both equal `q`, so expected posterior risk is `H(q)` and gain is zero for every audit frequency. If only one outcome is feasible, the feasibility status identifies it and its posterior equals the current law, again giving zero gain.

Therefore three outcomes are minimal for this one-fixed-audit, finite-posterior-risk, constant-cost value-loss obstruction. The conclusion does not cover outcome-dependent costs: on an independence fibre a cost assigned differently to the two labels can have different expectations. Nor does it establish preservation for arbitrary repeated fresh experiments or adaptive multi-instrument systems.

## Controls actually run

The root's standard-library `verify.py` replay passed and exactly reproduced `CONTROL_RESULTS.json`: 1,093 word comparisons for each of the boundary and interior examples, with both decision reversals and nonzero risk/kernel pairings.

The separate `check_inquiry_value.py` imports no root checker and uses SymPy 1.14.0 plus exact fractions. Its `RESULTS.json` records:

- 3,280 ternary posterior/status comparisons through word length seven;
- both exact boundary/interior gain and cost reversals;
- 64 exact rational posterior matrices, including 47 explicit nonconstant positive-fibre witnesses and 74 constant row-space/direction controls;
- the proper-risk boundary counterexample to an unqualified iff;
- 225 binary joint laws, including zero audit marginals, grouped into 207 posterior classes, with 126 distinct equivalent ordered pairs; each class preserves expectations for three finite functions of the posterior, including nonconcave and discontinuous controls;
- the symbolic symmetric-family gain identity.

The first local symbolic check used structural equality between differently expanded but equal SymPy expressions; that assertion was corrected to compare the expanded difference with zero. The final executed script passes. No mathematical claim depended on that transient checker-format mismatch. The universal claims are established by the displayed proofs, not by bounded enumeration.

## Ownership and preserved scope

H-ICS's feasible-support factorization already owns the linear fibre/difference-space mechanism. H-Continuation Theorem 2(c) already preserves adaptive policy branch-weighted values, and its reward-predictive discussion and contract map already distinguish answer, risk, and incentive observables. The final note now explicitly credits those sources. The bounded increment here is the exact posterior-only equivalence-to-inquiry-value obstruction, its strict-risk/interior witness, and the fixed-audit cardinality/classification specialization. No general mechanism or field-wide priority is established as new.

`BINDINGS.json` records the final root files, separately reported revision history, inherited source hashes, previous seals, and these new review artifacts. The intermediate hashes are recorded as parent-reported revisions, not as archived independently rehashed snapshots. The reviewed final hash above is directly verified. All earlier bound review/author files remain unchanged.
