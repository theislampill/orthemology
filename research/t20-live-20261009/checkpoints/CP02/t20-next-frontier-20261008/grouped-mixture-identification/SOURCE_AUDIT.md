# Source return, ancestry, and dependency record

Checked on 8 October 2026 UTC. The proofs in this sibling are self-contained elementary specializations. They do not claim a new general finite-mixture, Prony, moment, tensor, or continuation theorem.

## Primary grouped-mixture source

Robert A. Vandermeulen and Clayton D. Scott, **An Operator Theoretic Approach to Nonparametric Mixture Models**, *Annals of Statistics* 47(5), 2704–2733 (2019), DOI [10.1214/18-AOS1762](https://doi.org/10.1214/18-AOS1762). Primary author preprint available at [arXiv:1607.00071 PDF](https://arxiv.org/pdf/1607.00071). Targeted inspection covered the grouped-law definition and identifiability/determinedness discussion, the statements of Theorems 4.1–4.4, and the Section 7 passages identified below; it was not a continuous reading of the whole paper or all proofs.

- Definition 3.2 and the accompanying distinction between identifiable and determined mixtures separate bounded-order competitors from all orders.
- Theorems 4.1–4.2, PDF printed p.5, give the sharp `2m−1` grouped-sample identification threshold; Theorems 4.3–4.4, printed p.6, give the `2m` determinedness threshold.
- Section 7, especially Lemma 7.1 and Corollaries 7.1–7.2, connects grouped finite-outcome observations with multinomial mixtures and preserves these distinctions.

Our binary endpoint setting falls within this established framework. The present stage proves its univariate moment version directly and checks that lower-bound nodes can be genuine base4 route-histogram codes, rather than merely arbitrary probability measures. The authors' earlier primary preprint [On The Identifiability of Mixture Models from Grouped Samples, arXiv:1502.06644](https://arxiv.org/pdf/1502.06644), Theorems 4–5, was also checked. No precedence claim for this stage follows.

## Primary Prony reconstruction source

Dmitry Batenkov, Gil Goldman and Yosef Yomdin, **Super-resolution of near-colliding point sources**, *Information and Inference: A Journal of the IMA* 10(2), 515–572 (2021). Inspected author preprint: [arXiv:1904.09186 PDF](https://arxiv.org/pdf/1904.09186), Appendix A, printed pp.31–32.

Propositions A.1–A.3 record finite-node uniqueness, the annihilating-polynomial recurrence, and reconstruction from moments of orders `0,...,2d−1` by a Hankel nullspace, polynomial roots, and Vandermonde weights. This is cited as a primary research exposition of the standard Prony method, not as its historical invention. Our positive nonzero weights meet the nonvanishing-amplitude conditions needed for full rank. Our report makes no claim to transfer this paper's Fourier-noise stability results to the route experiment.

## Primary truncated-moment source

Raúl E. Curto and Lawrence A. Fialkow, **Recursiveness, Positivity, and Truncated Moment Problems**, *Houston Journal of Mathematics* 17(4), 603–635 (1991), [journal PDF](https://hjm.math.uzh.ch/v017n4/0603CURTO.pdf).

The inspected material includes Proposition 2.2 (first singular Hankel section), Section 3's generating-polynomial reconstruction, and Theorem 3.10 on uniqueness in the singular even truncated-moment case, printed pp.620–621. This is the relevant classical ancestry for the support certificate from moments through `2s`. Our proof uses the simpler promised-measure argument `integral p^2=0`, avoiding any assertion that an arbitrary positive-semidefinite finite Hankel matrix by itself always has a representing measure. The paper explicitly warns against that inference in the singular case.

As a primary cross-check, Curto, Fialkow and H. Michael Möller, **The extremal truncated moment problem**, [author PDF](https://www.cs.newpaltz.edu/~fialkowl/files/emp.pdf), Section 1, states that a polynomial in the moment-matrix kernel vanishes on the support of an existing representing measure. We use this support implication, not the paper's general multivariate sufficiency machinery.

## Stationary identity

The persistence control is proved by expanding a square and using equal second marginals. It is the usual variance/Dirichlet-form identity. No Markov or reversibility theorem is needed, and none is claimed. In particular, a source that states it under reversibility must not be misread as imposing that unnecessary assumption on the elementary identity. The report supplies an exact nonreversible cycle and exact premise-removal adversaries.

## Inherited continuation source

The parent directly reacquired `theory/lineages/h-continuation/continuation_complete_orthing.md` at commit `fd0903d99d657c35e32fddcc8864d2a77930cf40` in `theislampill/orthemology`; Git blob `99d0434aad8b8a841f59eb078e2b70c0b961d226`. Received lines 108–292 were read from `../root-audit-addenda/H_CONTINUATION_108_292.md`.

The relevant inherited material is the finite-state action–observation instrument hierarchy and its full-simplex continuous-coordinate bound. Our specific map is diagonal no-effect multiplication, `K_0^j1=q^j`, yielding a Vandermonde hierarchy. The hierarchy itself and its general predictive-memory conclusion are not newly discovered here. A restriction to sparse mixtures changes the domain and cannot inherit a full-simplex lower bound without a separate argument.

## Still-editing scalar source dependencies

Read, without alteration, from `../countable-signature-identification/`:

- `RESULT.md`
- `ORACLE_AND_EXTENSION_BOUNDARIES.md`
- `THEOREMS.md`

The imported content is finite-histogram base4 scalar injectivity, exact rational histogram decoding, the all-rate mixture counterexample, and boundaries for guards, approximations, and infinite-route completion. These were still-editing inputs at initial receipt. A fingerprint below records that observed version rather than asserting that this worker froze it.

Observed SHA-256 fingerprints at `2026-10-08T09:29:29Z`:

- `RESULT.md`: `1b4c66a3fa955ea4a60d2d04d3210f773620dcdacbcb1ff8a6381b6a23f95923`
- `ORACLE_AND_EXTENSION_BOUNDARIES.md`: `c694d06f556cc62d55504dfd3b73da0a034bbb5971aae571d624a905b42a719c`
- `THEOREMS.md`: `f232016d83bff0f15dbe9b9623f70f6ed6e512e7de05095b5d4f280bea65cce0`
- H-Continuation source-return file: `bb226ec3e294b31153808cca11e5facd2182af0372974b267c6f68f18b491396`

Subsequently the parent reported the scalar author's frozen `MANIFEST.json`, SHA-256 `43681d0c2d070e30200afb7b3dc557396150bff9c8012e75bd0a72328a27a974`. This worker independently checked that manifest file and its three imported text-file hashes before freezing this sibling. The historical observed hashes above are retained; the freeze is the scalar author's later checkpoint, not this worker's ownership or acceptance of that stage.

## Retrieval limits and research credit

The direct university-hosted grouped-mixture PDF initially returned a fetch error, so its arXiv primary preprint was used. The journal-hosted super-resolution page redirected to an inaccessible endpoint; its arXiv primary preprint provided the inspected Appendix A instead. One PDF screenshot request returned a cache miss; source-check claims here rely on retrieved document text, not an asserted visual audit of that failed page. No external primary quotation beyond brief titles is reproduced.

This is prospective research performed for the assigned sibling. It does not retroactively credit earlier waiting, packaging, other workers' analysis, or overlapping elapsed time as additional active research. No protected repository edit or final integration was performed.
