# Independent review: posterior-only continuation candidate

10 October 2026 UTC. Ordinary mathematical/code review only. This document does not authorize integration, protected changes, T20 closure, release, or a field-novelty claim.

## Result

The amended posterior-only tensor criterion is correct under its declared finite-alphabet, nonnegative, fixed-readout assumptions. The fixed binary-audit quotient is also correct, including boundary joint laws with zero cells when both audit marginals remain positive. I found no counterexample to either stated result. Initial presentation gaps about the alphabet, word order, empty word, admissibility, and exact input representation were communicated to the author and corrected during review.

The primary reviewed derivation is `../audit-aware-correction-root-20261010/POSTERIOR_ONLY_TENSOR_DERIVATION.md`, SHA-256 `688615b3038603c4b37621a38e3079b369063672b0ea3c679359dcbf195472fc`. The reviewed binary checker is `../audit-aware-correction-root-20261010/check_binary_audit_quotient.py`, SHA-256 `31bb07ffe18920cfab084353f4f8925da19c54ff0a4d87d14e1113693d074604`.

## Mathematical findings

1. **Universal iff.** Write the column-state product for chronological word `w=a1...ak` as `M_w=M_ak...M_a1`. For every readout row `c`, the cross-multiplied posterior difference is exactly `(c⊗1−1⊗c)(M_w⊗M_w)(r⊗s)`. Equality of conditional outputs on a jointly feasible word is equivalent to its vanishing. The least right-invariant row span of the initial covectors contains exactly the linear combinations of these word covectors. Its annihilation therefore checks all cross-products, not merely a selected finite horizon.

2. **Product order.** Under this chronological convention, multiplying a word covector on the right by `T_a` prepends `a` to the chronological word. This is valid because the theorem ranges over the full free monoid; every finite word still occurs. A witness-producing implementation must preserve that reversal/prepending convention. The reviewed candidate has no witness-label implementation to get wrong. An explicit noncommuting independent control confirms the orientation.

3. **Impossible branches.** Nonnegativity of both the matrices and beliefs implies `1ᵀM_w r=0` exactly when `M_w r=0`. All cross-products vanish if either state has zero branch probability. Thus the tensor condition alone deliberately loses the distinction between a feasible and impossible branch. A separate feasible-language test is logically necessary. With that test, jointly impossible words agree in status and jointly feasible words may safely be normalized.

4. **Support test.** The set-valued update is deterministic, with at most `2^n` supports. Breadth-first search of a pair of supports is finite, with at most `4^n` pairs. A reached pair with exactly one empty support witnesses inequality. Equal initial supports imply equal supports after every word and hence equal feasible languages. Equal initial supports are sufficient, not necessary, for language equality.

5. **Finite decidability.** The candidate now explicitly supplies a finite alphabet and rational matrices, fixed readout, and compared beliefs. Consequently row-span membership, support positivity, and residual zero tests are exact operations. Finite dimension alone does not yield an effective test for arbitrary real-valued input descriptions. An arbitrary history-dependent admission language is not silently handled: use the full free monoid as stated or explicitly include a finite controller in the model. A finite controller does not represent every possible history-dependent permission policy.

6. **Readout scope.** A fixed `C` can read the current latent state after a transition. An arbitrary external `C_t` does not satisfy the stated fixed-generator theorem without an appropriate enlarged fixed model. Static-target preservation is a semantic specialization, not an automatic consequence of nonnegative matrices.

7. **Dimension and minimality.** The antisymmetric covectors are invariant under `M⊗M`, so `dim W≤n(n−1)/2` over the rationals/reals. This is a bound for the paired-state linear test. It is not the dimension of a minimal single-state filter, a storage lower bound, or a minimal sufficient nonlinear posterior representation. The amended candidate explicitly avoids those claims.

8. **Fixed binary audit.** The empty word provides `q`; nonempty constant audit words provide `q0` or `q1`; contradictory rereads are impossible for every law in the declared domain. Thus `(q,q0,q1)` is complete. If `q0≠q1`, `t=(q−q0)/(q1−q0)` reconstructs all four joint cells. If `q0=q1`, total probability gives `q=q0=q1` and the table is independent; the audit marginal `t∈(0,1)` is unobservable in this posterior-only signature. This holds also at `q=0` or `q=1`. It does not establish any classification when an audit marginal is zero, and it must not be applied to fresh audit samples.

## Exact controls actually run

Run `python independent_checks.py` from this directory, or use its full path. This independent script imports neither author's checker and uses SymPy 1.14.0 exact rational row spaces. The support-language oracle enumerates the Boolean relation semigroup rather than using the author's belief-support-pair routine. This provides an independently structured finite feasibility check.

- The author's binary checker passed: 79 positive joint laws and 6,241 pair comparisons.
- Independent generic controls passed for 24 two-symbol rational instruments at dimensions 2, 3, and 4; 776 belief pairs; 41,496 pair/word comparisons; and 6,936 chronological product identities.
- The generated instrument families are jointly column-stochastic. Beliefs include boundary supports, equal states, full-support states, and matching-current-target/differing-nuisance pairs. Every chronological word through the antisymmetric dimension bound was compared against the stabilized tensor closure. This finite bound suffices for the cross-product linear representation; these tests supplement the ordinary proof rather than replacing it.
- An explicit noncommuting two-symbol instrument checks that chronological `(0,1)` means `M1 M0`, not `M0 M1`.
- A missing-feasibility false positive uses `C=[[1,1,0],[0,0,1]]`, `r=e1`, `s=e2`, `M0=diag(1,0,1)`, and `M1=diag(0,1,0)`. Every tensor equation passes. Word `0` has target posterior `(1,0)` under `r` and is impossible under `s`. The separate guard rejects it.
- The independent binary-audit grid contains 207 rational joint laws, including zero cells but excluding zero audit marginals: 180 dependent laws and 27 independent laws. All 42,849 pair comparisons agree with the claimed quotient classification.

Machine-readable output is in `INDEPENDENT_RESULTS.json`. The reviewed input hashes are also in `INPUT_BINDINGS.json`. The test script's own hash is recorded in its output. These are bounded exact controls, not exhaustive enumeration of all rational models.

## Ownership and publication ancestry

The inspected retained source `../tensor-moment-continuation-20261009/H_CONTINUATION_SOURCE.md`, lines 217–292, already gives action–observation instruments, invariant observable closure for branch probabilities and terminal numerators, closed predictive updates, and a full-simplex continuous-coordinate minimality result. Those results are inherited and must not be credited as new here. The posterior-only criterion compares a weaker behavioral contract: equality of normalized readouts plus feasible-word status.

The author's ancestry account should cite and delimit the established weighted-automata machinery. Kiefer, Murawski, Ouaknine, Wachter, and Worrell, *On the Complexity of Equivalence and Minimisation for Q-Weighted Automata* (2013), §2.2 Proposition 2.1 and §3 Proposition 3.1, supply the Kronecker mixed-product identity and finite-span zeroness/witness framework. [Primary PDF](https://people.mpi-sws.org/~joel/publications/Q_weighted_automata13.pdf). The inspected passages do not themselves state this posterior-only theorem; the reduction is a specialization of established machinery. The paper's entrywise matrix Hadamard products should not be presented as an inspected formal-series Hadamard-closure theorem.

The fixed-audit reconstruction is an elementary application of total probability. Neither it nor the paired lift has been established as new to the field by this review. Broader project/source ownership remains the author's responsibility; this review does not substitute for that account.

## Residual presentation note

The phrase “alphabet ... including the empty word in the observations” is slightly awkward: the empty word belongs to `Σ*`, not ordinarily to the alphabet. The subsequent explicit `M_empty=I` removes substantive ambiguity. A future editorial pass can simply say “all words in `Σ*`, including the empty word.” No mathematical change is required.
