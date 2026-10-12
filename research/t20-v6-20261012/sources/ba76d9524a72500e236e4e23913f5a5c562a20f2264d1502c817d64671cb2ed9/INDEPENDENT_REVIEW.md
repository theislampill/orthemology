# Independent mathematical review

Reviewed 9 October 2026 UTC. This is a separate review receipt for the scratch mathematical report. It does not authorize protected integration, release, audit closure, or a claim of formal certification.

## Reviewed snapshot

- RESULT.md SHA-256: 06351f384910bb9984c75712bea3b483201fad575a0ac8da258406b5f56d7f69
- verify.py SHA-256: f74bdf6cc3bbd5635701ac26a7f881ece4baca1e64305f53c72e5cc81dbdd6ac
- Scope: independent derivation, full document-level mathematical read, inspection and execution of the complete verification script, and separate numerical spot checks.
- Outcome: no blocking mathematical finding in this snapshot. An earlier domain clarification in section 6 was requested and is now fixed: the proper-score identities use r,s in the simplex interior.

## Proof review

1. The closed-simplex existence and uniqueness statement is valid. The generators extend continuously to the closed interval; positive interior second derivatives give strict convexity on the closed interval. The projection objective is therefore continuous and strictly convex on the compact simplex. No endpoint derivative is required.
2. Lemma 1 is valid, including endpoints. For a subprobability input, a proposed minimizer coordinate at or below its input permits a transfer from a coordinate strictly above its input. The resulting strict objective decrease follows from interior derivative bounds or endpoint secant bounds. Thus every projected coordinate is strictly above its input and the projection is interior.
3. Theorem 2 is valid. A local common dual-shift curve exists by the inverse function theorem using only positive continuous second derivatives. It remains in the same projection fiber. Under a single-coordinate attenuation, subtracting KKT equations before differentiation gives the stated curvature ratio, while an unchanged coordinate makes the ratio equal to one. This forces f_i''(t)=alpha_i/t separately for each coordinate. The weighted-entropy projection formula proves sufficiency.
4. Theorem 3 is valid. Downward scalar neutrality forces normalization by scaling either the raw vector or its normalized representative. Interiority is then a consequence. Independent cube coordinates force one common entropy coefficient. The converse and full positive-likelihood equivariance follow from normalization. No n=2 exception occurs; n=1 is correctly excluded.
5. The weak composition law is genuinely weaker. Unequally weighted entropy obeys it while failing scalar neutrality. The radical example in the report is exact.
6. Corollary 4 is valid. Coherent-prior scalar neutrality alone yields pairwise equality of t f_i''(t) on the subprobability region. A sufficiently small comparison value connects arbitrary values within each coordinate, including for n=2. The resulting two-outcome null channel has strictly positive expected regret for every generator outside the common-entropy class, with both reports interior.
7. The exact quadratic example, proper-score decomposition, information-minus-regret identities, three-point repair identity, and duplicate-root calculation are correct. The report keeps the declared-prior and channel premises explicit and preserves the first-argument divergence orientation.

## Fresh verification

The full command `python warranted-learning-20261009/verify.py` exited 0 during this review. Its eight check groups passed:

- Exact quadratic null-channel countermodel: prior risk 3/16, updated risk 13/64, excess 1/64, statewise repair gain 1/16.
- Exact quadratic failure of the restricted weak contract.
- 810 exact normalization contract cases.
- 27 exact finite-channel accounting cases.
- Exact duplicate-root countermodel and regret.
- Exact unequal-weight entropy radical relations.
- 252 weighted-composition numerical diagnostics, maximum absolute residual 6.661338147750939e-16.
- The retained bytes for all 12 source bindings match the recorded Git-framed SHA-1 blob hashes.

Separately, an independently written in-memory bisection check ran 1,000 random weighted-entropy composition cases across dimensions 2, 3, 5, and 10, with maximum absolute residual 1.3322676295501878e-15. It also independently confirmed the exact radical and quadratic examples numerically.

## Review boundaries

The universal results are supported by the written proof review, not by finite tests. This is not a proof-assistant or kernel certification. The numerical checks are diagnostics only. Source-byte hash checks establish agreement with the recorded manifest; this review did not independently re-audit the substantive content of all 12 source documents or establish field-wide originality. The report now explicitly attributes the existing Bayes, conditional-factorization, and duplicate-invariance machinery to Deep AX V2 and bounds its contribution to the repair–likelihood interface. Nothing reviewed establishes an actual prior, actual likelihood, semantic mapping, proper function, or noetic warrant.
