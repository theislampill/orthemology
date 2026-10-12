# Independent review of Gaussian entropy regularization

11 October 2026 UTC. Ordinary independent mathematical review for active T20. This is an internal review separate from the author, not external peer review, audit-assess output, formal-kernel certification, protected integration, or programme closure. No author or frozen baseline bytes were edited.

## Verdict

PASS within the declared finite-dimensional Gaussian contract. No blocking mathematical defect was found in the frozen comparison report. The metric correspondence is exact. The different covariance drifts genuinely arise from different energies. The entropy-regularized Gaussian ODE, positive-definite covariance bounds, global forward existence, fixed-temperature convergence, and finite-horizon parameter comparison are supported by the displayed arguments without assuming that Q and Sigma commute.

The result does not establish a new Gaussian SHK geometry, a general full-law uniqueness theorem, a uniform-time small-error theorem, convergence in KL to a singular target, equality of intrinsic Gaussian and unrestricted endpoint distances, or applicability to indefinite quadratic potentials. The report correctly withholds these extensions.

## Frozen inputs and review boundary

The reviewed comparison RESULT.md has SHA-256 b21c31a755ac253d31af5cb7088773e2c923689a942be7a15e89b1edc398c75f. The local author MANIFEST.json has SHA-256 0e8e1e18da3269ff7adcb3462244060c98d6eb9c3baf9639d0deca9d47b1284c. Its complete declared file set was checked against those pins before and after replay.

The frozen baseline gaussian-correction-geometry-20261011/RESULT.md has SHA-256 67577bc185c3190cbf131993fdfdd36aa67c605435fd225eb6f29b2cc6c21efa. Its original and the author's copied input agree. This review read its full-density minimization contract and multivariate extension, especially equations (18)-(23).

The primary source was WIAS Preprint 3198, *Evolution of Gaussians in the Hellinger-Kantorovich-Boltzmann gradient flow*, by Liero, Mielke, Tse and Zhu, submitted 13 May 2025. The PDF at https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf has SHA-256 f7d34fed7f0c9be50564b0a931e1c9a3ed4b34d59c0323cdd2ce940e4a5d2e29. This reviewer independently inspected sections 3.2-3.4, the section 1 normalization, and the rendered PDF pages 15-16, printed pages 13-14. Public web retrieval independently identified the same title, authors and preprint. This review does not claim to have checked the final journal revision or independently checked the arXiv HTML.

The portable derivative has the identical RESULT.md and its own manifest, SHA-256 571e541865a884034192c32947f659c6e45aeed2ee61266fefd2151c4b79795f. Its replay script has SHA-256 fad4e3508cb26be867b7d9eaf8de53e7cf3c98fcbef03563f4f9feb14dfd9ba7. That derivative's absent-source behavior was checked separately. Raw third-party manuscripts, extracted manuscript text, and page images are not included in this review folder.

## Metric correspondence

The primary comparison is direct: WIAS Lemma 3.6 and Theorem 3.11 give the covariance and mean Onsager blocks used in the comparison. Section 3.3 differentiates the Gaussian relative entropy; section 3.4 specializes to probability mass one. Source order (Sigma,m) is harmlessly permuted to (m,Sigma). The source's named Hellinger convention uses reaction coefficient four; the baseline uses coefficient one. Nonunit mass changes the shape cometric by the reciprocal mass. These distinctions are correctly recorded.

Independently, for centered x and a symmetric cotangent S, take f=a^T x+x^T S x-tr(S Sigma). The positive density operator with coefficients alpha,beta maps this to the full Gaussian tangent

    h=(alpha I+beta Sigma)a,
    B=2alpha(S Sigma+Sigma S)+2beta Sigma S Sigma.

The matching quadratic action is

    alpha(|a|^2+4tr(S^2 Sigma))
      + beta(a^T Sigma a+2tr(S Sigma S Sigma))
      =a^T h+tr(S B).

This both fixes the normalization and proves that the proposed finite cotangent representative realizes the complete density tangent. For a diagonal covariance, the multiplier on S_ij is 2[alpha(lambda_i+lambda_j)+beta lambda_i lambda_j]. A symmetric off-diagonal entry occurs twice in tr(B L^{-1}B), giving precisely the off-diagonal denominator in (C2). The factor is not optional. At unit coefficients the baseline equations (18)-(21) are recovered exactly.

The baseline supplies the all-admissible-fields orthogonality and cutoff argument needed for the tangent infimum. The present comparison does not replace that proof by a first-two-moments calculation. The source match also removes any basis for claiming novelty of the Gaussian metric; the baseline already disclaimed historical priority.

## Energy and full-density flow

At a Gaussian, entropy contributes minus one half log det Sigma up to constants. Therefore J_epsilon has mean cotangent Qe and covariance cotangent (Q-epsilon Sigma^{-1})/2. Applying the same metric yields

    m' = -(I+Sigma)Qe,
    Sigma' = 2epsilon I+epsilon Sigma-QSigma-Sigma Q-Sigma QSigma.

The complete variational potential, after discarding a constant, is

    (Qe)^T x + one half x^T(Q-epsilon Sigma^{-1})x
      - one half tr[(Q-epsilon Sigma^{-1})Sigma].

It is quadratic. Substitution into the full density operator reproduces the Gaussian score with those two parameter derivatives. Thus an exact Gaussian solution is obtained, rather than just a matching moment projection. Gaussian uniqueness and continuation here concern this smooth ODE; the report does not supply uniqueness in an unspecified class of general weak measure-valued solutions.

With Gamma=epsilon Q^{-1}, multiplying the entire source KL vector field by epsilon reproduces the displayed system. The time substitution s=epsilon t is essential for positive epsilon. The zero value is taken directly in the polynomial ODE, not through an undefined target precision or a degenerate time change.

For epsilon=1 the covariance drift differs from the expected-energy drift by 2I+Sigma. This cannot be removed by an additive energy constant. The stationary covariance is Q^{-1} for KL and epsilon Q^{-1} for positive-temperature regularization. For expected energy there is no nondegenerate covariance equilibrium when Q is positive definite.

Noncommutation matters throughout. The rational witness used by the independent checks is Sigma=[[2,1],[1,3]] and Q=[[3,1],[1,1]], both positive definite. Replacing QSigma+Sigma Q by 2Sigma Q changes the vector field and makes this covariance velocity nonsymmetric. The report makes no such replacement.

## Positive definiteness and global continuation

Write q=lambda_min(Q)>0 and r=lambda_max(Q). For any unit eigenvector u of Sigma with eigenvalue lambda,

    u^T Sigma' u = (2+lambda)(epsilon-lambda u^T Q u).

This identity is valid without simultaneous diagonalization. At a multiple eigenvalue the extremal one-sided derivatives are bounded using the Rayleigh extrema in its eigenspace. Consequently lambda_max has the scalar upper differential bound (2+lambda_max)(epsilon-q lambda_max). With epsilon in [0,epsilon_bar], the barrier M=max(lambda_max(Sigma_*),epsilon_bar/q) is valid for all forward time for which the solution exists.

The least eigenvalue then has almost-everywhere lower differential bound

    lambda_min' >= -r(2+M)lambda_min.

On [0,T] this gives the stated ell_T. The claimed containing set is horizon dependent; the proof never treats its fixed lower face as an all-time invariant face. At each finite T this positive lower bound excludes arrival at the covariance boundary.

For the mean, y=Q^{1/2}e obeys y'=-[Q+Q^{1/2}Sigma Q^{1/2}]y. This symmetric equation gives |y(t)|<=exp(-qt)|y(0)| and hence |e|<=R. It is important that the proof uses this Q-weighted norm: it does not assume that the nonsymmetric matrix (I+Sigma)Q is symmetric.

The covariance upper bound and mean bound prevent blowup, while ell_T prevents a finite-time exit through singular covariance. Standard finite-dimensional local uniqueness and continuation prove the stated global Gaussian solution. The assumptions cover epsilon_bar=0, vanishing initial mean error, arbitrary finite dimension, and every positive-definite initial covariance.

For fixed epsilon>0 the stronger bound lambda_min>=min(lambda_min(Sigma_*),epsilon/r) follows from the same scalar barrier. Thus the trajectory is precompact in the nondegenerate Gaussian parameter manifold for that fixed epsilon.

## Explicit perturbation estimate

Let Delta=Sigma_epsilon-Sigma_0 and z=m_epsilon-m_0, with common initial data. The noncommuting product expansion is

    Sigma_epsilon QSigma_epsilon-Sigma_0 QSigma_0
      =Delta QSigma_epsilon+Sigma_0 QDelta.

This gives exactly the report's two difference equations. The Frobenius submultiplicative inequalities and the shared upper covariance bound yield

    D+||Delta||_F <= 2r(1+M)||Delta||_F
                         + epsilon sqrt(d)(2+M),
    D+|z| <= r(1+M)|z|+rR||Delta||_F.

The forcing estimate uses ||2I+Sigma||_F<=sqrt(d)(2+M). Norm upper-right derivatives are legitimate even at zero, so the common initial condition creates no differentiability gap.

With D=|z|+||Delta||_F, L=r[2(1+M)+R], and A=sqrt(d)(2+M), the coefficient of ||Delta||_F is exactly L and the coefficient of |z| is no larger. Also L>0, including R=0, because Q and Sigma_* are positive definite. The scalar comparison solution is epsilon A(exp(Lt)-1)/L, with initial value zero. Therefore (C9) follows with no missing dimension factor or commutator term.

Although the inequality is valid at every finite t with the same M,R,L,A, its right-hand side grows in t. The supported consequence is the stated O(epsilon) comparison on each fixed finite horizon. This is not a uniform-in-time O(epsilon) result. Neither a claim that stronger estimates are impossible nor a claim that they have been proved follows.

## Terminal behavior and limits

For a fixed positive epsilon the compact parameter region just established keeps the smooth vector field, energy, and dissipation under control. Along the flow the negative energy derivative is the sum of the two strictly positive cometric quadratic forms, vanishing precisely when Qe=0 and Q-epsilon Sigma^{-1}=0. Thus the only critical point is (n,epsilon Q^{-1}).

To justify the omega-limit argument explicitly: if an accumulation point had positive dissipation, continuity would give a neighborhood with dissipation bounded away from zero. Bounded speed on the compact containing region supplies a uniform positive duration for recurrent passages through a smaller neighborhood. A disjoint subsequence of these passages would force unbounded total energy loss. The energy is bounded below on the compact region, giving a contradiction. Every accumulation point is therefore the unique critical point, and the trajectory converges. No rate theorem from the source is needed or imported.

At epsilon=0 the baseline precision formula remains valid without Q-Sigma commutation. Its first term alone gives P(t)>=lambda_min(P_*) exp(2qt)I, so Sigma(t)<=lambda_max(Sigma_*)exp(-2qt)I. The Q-norm mean estimate tends to zero as well. Thus the Gaussian law converges weakly to delta_n. This endpoint lies outside the positive-definite Gaussian manifold.

The positive-temperature targets also approach that Dirac law weakly. These two individually established facts do not constitute a general interchange-of-limits theorem. Inverse covariance and KL comparisons become singular as epsilon tends to zero. In particular, for any fixed nondegenerate Gaussian the quadratic part of KL to N(n,epsilon Q^{-1}) is proportional to 1/epsilon with positive coefficient, dominating the logarithmic normalization term. The divergence warning is correct.

## Narrow check of the printed sign

On the inspected image of WIAS printed page 13, equation (3.7) visibly uses a plus sign before rho grad log pi. The preceding Onsager operator, applied with minus sign to log(rho/pi), instead gives div(grad rho-rho grad log pi) for the transport part. This is a version-specific apparent sign typo, not a broad criticism of the paper.

An independent exact discriminator sets rho=pi to the standard one-dimensional Gaussian. The operator-derived expression is zero. The printed plus expression divided by rho is 2(x^2-1), which is not zero. The normalized Gaussian ODE in (3.8) has the target as equilibrium, agreeing with the operator-derived sign. The report is right to rely on those consistent formulas. No statement about a later journal correction is made here.

## Evidence and reproduction

The independent check_independent.py imports no author code and passes 32 symbolic or rational controls. These include general symbolic symmetric 2D matrices, full-density tangency, weighted action, reciprocal-mass scaling, off-diagonal Frobenius factors, the entropy differential, source time scaling, zero-entropy precision dynamics, the perturbation identities, an eigendirection check, and the sign discriminator. These tests corroborate the proofs above; finite tests alone do not prove all-dimension positivity or convergence.

The frozen author's script was replayed with all output redirected to this review folder: all 35 local applicable controls passed. Its numerical trajectories are numerical controls only. A clean isolated copy of the portable derivative passed all 33 applicable controls without raw sources or the sibling baseline original, and explicitly reported unavailable source custody. The two omitted local checks concern those unavailable files; no mathematical control was suppressed. Requesting mandatory source custody failed as expected with exit code 1. No missing raw source was reclassified as a successful custody check.

Run python3 replay_review.py --output-dir private-locator:41b1fcef6c5de25a3651 for the independent portable controls and snapshot integrity checks. Optional --author-dir, --portable-dir, and --source-dir arguments enable additional checks against those available local folders. The local inspection receipt records the actually inspected primary source pins; portable replay does not pretend to recreate that visual inspection without the primary material.
