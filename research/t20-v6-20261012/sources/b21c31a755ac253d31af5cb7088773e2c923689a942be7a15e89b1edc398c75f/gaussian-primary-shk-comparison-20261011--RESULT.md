# Gaussian SHK source comparison and an entropy regularization bridge

11 October 2026 UTC. Author-side additive mathematics for active T20, written in scratch only. The accepted Gaussian packet remains unchanged. This report establishes a source correspondence and a conditional transfer, not historical novelty of the metric, an independent review, a formal-kernel proof, protected-source integration, or programme closure.

## 1 Main conclusion

The Gaussian metric already calculated in `gaussian-correction-geometry-20261011/RESULT.md` is exactly the unit/unit normalized Gaussian SHK metric in Liero, Mielke, Tse and Zhu. The correspondence includes the noncommuting covariance operator and its Frobenius factors. The useful consequence is energy-sensitive: their Gaussian KL dynamics become our expected-quadratic dynamics only after removing the entropy term. A positive entropy coefficient instead supplies an exact Gaussian regularization with a positive-definite target. Section 5 proves a quantitative finite-horizon comparison as the coefficient tends to zero.

The metric is established prior art; this report supplies explicit attribution and transfer. The earlier packet did not claim field priority. It remains a direct full-density, all-admissible-fields proof in its declared contract. This comparison strengthens its attribution without retroactively altering that frozen artifact.

## 2 Primary source and reading boundary

Liero, Mielke, Tse and Zhu, *Evolution of Gaussians in the Hellinger–Kantorovich–Boltzmann gradient flow* (2025), [WIAS Preprint 3198](https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf), [arXiv 2504.20400v1](https://arxiv.org/html/2504.20400v1). The actual WIAS PDF was downloaded and §§2–3 read; printed pp. 13–14 were visually inspected. The journal [record](https://www.aimsciences.org/article/doi/10.3934/cpaa.2025105?viewType=HTML) was inspected, but its full text required access. All numbered mathematical references below are to WIAS, not an uninspected journal revision.

Source reading summary: §2 derives Gaussian parameter dynamics for relative Boltzmann energy. §3.1 uses constrained Onsager reduction. §3.2 obtains additive transport/reaction cometrics through quadratic potentials. §3.4, Theorem 3.11 and (3.8), gives the normalized Gaussian system. §3.5 changes the target inside a Gaussian variational restriction. These results distinguish reduced geometry from invariance of a particular full-law flow. No numerical algorithm, general-law convergence theorem, or historical priority conclusion is imported.

The exact accepted input and downloaded source are hash-bound in `SOURCE_READING.json`. Page images `primary-15.png` and `primary-16.png` show PDF pages 15–16, printed pp. 13–14.

## 3 Exact coefficient and coordinate comparison

Write a probability tangent as σ=−div(ρu)+ρr with Eρr=0. To avoid notation collisions, r is the reaction field: it is not the paper's nonnegative scalar coefficient α. For α,β>0 use action E[|u|²/α+r²/β]. Its Onsager operator is

    Kαβ(ρ)f = −α div(ρ∇f)+βρ(f−Eρf).

Thus our action E[|u|²+r²] means α=β=1. The paper uses β=4 for its named pure Hellinger distance normalization. Confusing that with unit reaction would change every reaction coefficient by four. At an endpoint α=0 or β=0, forbid the corresponding channel instead of dividing by zero; exclude α=β=0.

Use covariance Σ, mean m, Frobenius pairing tr(SB), and centered ξ=x−m. For a cotangent (a,S), its centered polynomial representative is

    f=aᵀξ+ξᵀSξ−tr(SΣ).

Our direct full-density computation, with weighted fields u=α∇f and r=βf, gives

    h=(αI+βΣ)a,
    B=Lαβ,Σ(S),
    Lαβ,Σ(S)=2α(SΣ+ΣS)+2βΣSΣ.                       (C1)

These are the two blocks of WIAS Theorem 3.11. Its parameter order is (Σ,m); our accepted (20) writes (m,Σ). Set α=β=1 in (C1) to recover accepted (18)–(21), exactly. At nonunit mass κ, the paper's shape blocks have an extra factor 1/κ; a normalized probability has κ=1 and no mass coordinate.

For Σ diagonal with eigenvalues λi>0, the covariance operator multiplier on Sij is

    2[α(λi+λj)+βλiλj].

Consequently the tangent metric is

    gαβ((h,B),(h,B))
      =hᵀ(αI+βΣ)⁻¹h
       +Σi Bii²/[4αλi+2βλi²]
       +Σi<j Bij²/[α(λi+λj)+βλiλj].                (C2)

The off-diagonal denominator differs by a factor two from the full i,j expression because the Frobenius pairing counts both symmetric entries. For d=1, (C2) is

    gαβ=dm²/(α+βv)+dv²/(4αv+2βv²).

Its unit/unit specialization is exactly the accepted metric. The coefficient channels add at the cometric level. This is justified here by the common quadratic potential representing the entire Gaussian tangent, not by a general rule that arbitrary submanifold restrictions commute with adding cometrics.

## 4 The energy difference is consequential

Fix Q positive definite and F(x)=½(x−n)ᵀQ(x−n)+C. Write e=m−n. Our expected energy, minus C, and Gaussian negative entropy are

    J0(m,Σ)=½[eᵀQe+tr(QΣ)],
    Ent(N(m,Σ))=−½ log det Σ−(d/2)log(2πe).

The Gaussian KL energy with target N(n,Q⁻¹) differs from J0 by Ent and a constant. In particular DΣJ0=Q/2, whereas adding Ent gives DΣ=(Q−Σ⁻¹)/2. Apply the same (C1):

    Expected F: m′=−(I+Σ)Qe,
                Σ′=−QΣ−ΣQ−ΣQΣ.

    KL:         m′=−(I+Σ)Qe,
                Σ′=2I+Σ−QΣ−ΣQ−ΣQΣ.                (C3)

The second system is WIAS (3.8) with Γ=Q⁻¹. The extra +2I+Σ is exactly the entropy contribution. It is not removable by dropping an energy constant. At Σ=Q⁻¹ the KL covariance is stationary; the expected-energy covariance is still decreasing. In d=1 with Q=1, the two variance equations are respectively −v(v+2) and (1−v)(v+2).

For a general polynomial F, the same geometry still defines the Gaussian-restricted gradient. Gaussian integration by parts gives a=E∇F, S=½E∇²F. This produces a reduced model, not full-law Gaussian invariance. The accepted quartic residual already proves that agreement of the first two moment derivatives cannot supply invariance. A non-Gaussian target in a Gaussian variational approximation does not erase that obstruction.

## 5 A controlled entropy regularization transfer

### Statement and exact scope

Assume d is finite, Q is symmetric positive definite, n is fixed, the spatial metric is Euclidean, and all trajectories start from the same N(m*,Σ*) with Σ* positive definite. Keep α=β=1. For ε≥0 define, on Gaussian probabilities,

    Jε=EF+ε Ent(ρ).

For ε>0 this equals ε KL(ρ || πε) plus a constant, where

    πε=N(n, εQ⁻¹).

Its full-law SHK variational derivative is F+ε logρ modulo constants. That is quadratic at every Gaussian. Direct density differentiation therefore proves invariance and the exact system

    mε′=−(I+Σε)Q(mε−n),
    Σε′=2εI+εΣε−QΣε−ΣεQ−ΣεQΣε.                    (C4)

This is also obtained from WIAS (3.8) by Γ=εQ⁻¹ and multiplication of its entire vector field by ε, equivalently by setting source time s=εt. The time factor is essential. No parameter rescaling is made at ε=0: (C4) then directly becomes the accepted expected-quadratic flow.

For all ε≥0, (C4) has a unique global forward Gaussian solution. For ε>0 its unique equilibrium is (n,εQ⁻¹), and the solution converges to it. For ε=0, the covariance tends to zero and the law tends weakly to δn. These are different terminal states for different energies.

### Shared finite-horizon bounds

Fix εbar≥0 and T<∞. Define

    q=λmin(Q)>0,             r=λmax(Q),
    M=max(λmax(Σ*), εbar/q),
    R=sqrt((m*−n)ᵀQ(m*−n)/q),
    ellT=λmin(Σ*) exp[−r(2+M)T].                    (C5)

Every solution for 0≤ε≤εbar obeys, for 0≤t≤T,

    ellT I ≤ Σε(t) ≤ M I,       |mε(t)−n| ≤ R.      (C6)

To prove this without a commutation assumption, let u be a unit eigenvector of Σ with eigenvalue λ. Directly from (C4),

    uᵀΣ′u=(2+λ)(ε−λ uᵀQu).                        (C7)

The standard extremal-eigenvalue one-sided derivative inequalities follow by maximizing or minimizing this Rayleigh expression within a multiple eigenspace. At λmax=M the upper derivative is nonpositive. For the least eigenvalue, (C7) gives λmin′≥−r(2+M)λmin almost everywhere. Scalar comparison gives (C6).

For y=Q^(1/2)(m−n),

    y′=−[Q+Q^(1/2)ΣQ^(1/2)]y,
    (|y|²)′≤−2q|y|².

This gives the mean bound. The bounds prevent finite-time escape or contact with the singular covariance boundary. Smooth local ODE existence and continuation then yield global forward existence and uniqueness. The compact set in (C6) is a common containing region on [0,T]; it need not be invariant beyond that horizon.

### Quantitative comparison with zero entropy

To distinguish time-dependent solutions from initial data, let (m^(0)(t),Σ^(0)(t)) denote the ε=0 solution, with the same initial state. Define

    Dε(t)=|mε(t)−m^(0)(t)|+||Σε(t)−Σ^(0)(t)||F,
    L=r[2(1+M)+R],       A=sqrt(d)(2+M).            (C8)

Then for every 0≤ε≤εbar and t≥0,

    Dε(t) ≤ ε A [exp(Lt)−1]/L.                     (C9)

In particular sup[0,T] Dε=O(ε), with every constant explicit and independent of ε in the chosen interval. The estimate grows with T and makes no uniform-in-time small-error assertion.

Proof. Set Δ=Σε−Σ^(0), z=mε−m^(0). The exact differences are

    Δ′=−QΔ−ΔQ−ΔQΣε−Σ^(0)QΔ+ε(2I+Σε),
    z′=−(I+Σε)Qz−ΔQ(m^(0)−n).

Use operator bounds ||Σε||op,||Σ^(0)||op≤M, ||Q||op=r and the mean bound R. The upper right derivatives of the norms satisfy

    D+||Δ||F ≤ 2r(1+M)||Δ||F+ε sqrt(d)(2+M),
    D+|z|    ≤ r(1+M)|z|+rR||Δ||F.

These statements also hold at zero norms via the norm upper-derivative inequality. Add them and use (C8) to obtain D+Dε≤L Dε+εA, with Dε(0)=0. Integrating proves (C9).

### Positive temperature and the singular limit

For fixed ε>0, (C7) gives the stronger all-time lower bound Σε≥min(λminΣ*,ε/r)I. Together with (C6)'s upper and mean bounds, this places the trajectory in a compact subset of the Gaussian manifold. Along the gradient flow,

    Jε′=−aᵀ(I+Σ)a−tr(S L1,1,Σ(S)),
    a=Q(m−n),       S=(Q−εΣ⁻¹)/2.

Both quadratic terms are positive unless a=S=0. The only stationary state is (n,εQ⁻¹). Compactness, continuity and the strict Lyapunov identity imply every omega-limit point is stationary: otherwise the dissipation stays bounded below on a neighborhood visited for a uniformly positive time infinitely often, contradicting finite total energy drop. Thus the solution converges to that state. This argument imports no optimization rate.

For ε=0 the accepted precision formula applies,

    P(t)=exp(tQ)P*exp(tQ)+(exp(2tQ)−I)/2.

It implies Σ^(0)(t)→0, and the preceding mean estimate implies m^(0)(t)→n. The limiting Dirac law lies outside the nondegenerate Gaussian manifold. Although πε also tends weakly to δn as ε↓0, neither (C9) nor the source correspondence supplies uniform-in-time comparison in KL, inverse covariance, or Riemannian distance, nor a general interchange-of-limits theorem. In fact KL(N(m,Σ)||πε) diverges as ε↓0 for any fixed nondegenerate N(m,Σ), showing why metric/energy and parameter-limit statements must be separated.

The assumption Q>0 is essential to this stated transfer. An indefinite or merely semidefinite Q on the whole Euclidean space need not define a normalizable Gibbs target. Nothing here transfers the positive-temperature conclusions to the accepted concave finite-time blowup example.

## 6 Narrow source formula caution

On WIAS printed p. 13, equation (3.7) visibly prints a plus sign in div(∇ρ+ρ∇logπ). The preceding displayed SHK operator, the energy derivative log(ρ/π), equation (1.3), and the target-stationary ODE (3.8) instead give div(∇ρ−ρ∇logπ). Substituting ρ=π already detects the inconsistency. This is a version-specific apparent sign typo, also present in the inspected arXiv v1 HTML. We use the displayed operator and (3.8), not that expanded PDE sign. The journal's public table labels its SHK operator (1.7), but its full equation was not accessible; no claim is made about the journal revision.

## 7 What this work does and does not establish

The transfer provides an explicit, energy-controlled route from a classical Gaussian KL flow to the accepted correction dynamics, including a shared-domain proof and quantitative finite-horizon perturbation estimate. It identifies precisely which additional term changes the terminal covariance. The metric, its Gaussian Onsager reduction, and the KL flow require the external attribution above; this packet makes no originality claim for them or for entropy regularization as a method.

It does not identify unrestricted SHK endpoint distance with intrinsic Gaussian distance, import geodesic convexity, infer exponential rates for EF, prove Gaussian closure for higher polynomials, or identify a probabilistic state with a noetic bearer or epistemic warrant. Source ancestry, ordinary mathematical validity, application adequacy and protected programme integration remain separate questions.

Run `python3 verify.py`. Symbolic/rational checks corroborate coefficient matching, the entropy contribution, noncommuting matrix identities, density tangency, stationary targets, source-time scaling, and the difference equations. Numerical noncommuting trajectories are explicitly only controls. The all-dimension bounds and ODE arguments are the proofs above, not a consequence of finite tests.
