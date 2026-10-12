# Audit transport through the exact OU–reaction correction

11 October 2026 UTC. A focused, additive T20 interface application. Ordinary proofs and exact controls; no protected edits, integration, external peer review, formal-kernel certification, or programme closure. The parent supplied the central distinction, proposed identities, and scope guards. This report checks and develops that author-stage proposal.

## 1. Result and prior coverage

At every finite positive step, the inherited exact correction preserves the entire incoming probability law injectively, yet it admits no prior-independent output likelihood for a nonconstant input likelihood on the full finite-second-moment law domain. These claims concern different contracts. Injectivity permits a nonlinear, state-dependent audit decoder on the actual image. It does not make that decoder multiplication by one fixed likelihood.

There is an exact positive repair. On one fibre, let D be the known Ornstein–Uhlenbeck kernel and R_a the normalized density power, with Φ=R_aD. Under the incoming joint law r(dx)D(dz|x), put

    ℓ_r(z) = E_r[L(X) | Z=z].

Then

    Φ(B_L r) = B_(ℓ_r^a) Φ(r).                         (1)

The conditional factor depends on r. A fixed-covariance Gaussian class and exponential tilts give a useful exception: its output factor is independent of the prior mean. Exact Gaussian output parameters also recover the incoming Gaussian parameters on the valid image, so extra stored incoming parameters are not universally necessary.

**No new general Bayes theorem is claimed.** The received authorial Cross_Front_Theorems, Theorem B and its positive repair, already contain the universal kernel obstruction and conditional-expectation factor. The inherited heat review §7 already proves Gaussian-convolution injectivity. The normalized power and exact split are prior art: Crucinio–Pathiraja, [arXiv:2511.18060v3](https://arxiv.org/html/2511.18060v3), §2 equation (2.5), display (W-FR), and §3. The present contribution is a bounded, operator-faithful application to the newly supplied Φ, including its normalized-only obstruction, the power a, class restrictions, actual Gaussian implementation controls, and the observed-marginal guard. The basic mechanisms receive no new proof or discovery credit. No exhaustive priority search was performed.

## 2. One-fibre domain and definitions

Fix g∈R^d and T symmetric positive definite, and let π=N(g,T). For 0<h<∞, set

    A=exp(−h T⁻¹),  Q=T−ATA>0,  a=exp(−h)∈(0,1).
    D r = Law(g+A(X−g)+ξ),  X∼r, ξ∼N(0,Q) independent.
    R_a(fπ) = f^a π / ∫f^a dπ,  Φ=R_aD.

This is the same map as the inherited split; it is not a new integrator. D r has a strictly positive finite Lebesgue density for every probability r. Thus its ratio f to π is well-defined and positive. Since π is a probability, 0<∫f^a dπ≤1, so Φ is defined as a probability-law map even before imposing a second-moment assumption. The audited domain below is P₂(R^d), matching the finite-relative-second-moment input class on one fixed fibre. No additional all-law iteration or numerical-computability assertion is needed here.

For the universal assertion, L:R^d→(0,∞) is a **specified pointwise** bounded Borel function. Write Z_r=∫L dr>0 and B_Lr=Lr/Z_r. Then B_L preserves P₂. Specifying L only π-almost everywhere is insufficient because allowed singular inputs can charge π-null sets. The Gaussian exponential-tilt example later uses a separate, explicitly integrable domain; its L is generally unbounded.

An output multiplier M must be a nonnegative measurable function, independent of r, with a finite positive normalizer for every output being tested. Multipliers differing by a positive scalar give the same normalized audit. Normalizer accounting is considered separately below.

## 3. Full-law injectivity and its exact boundary

**Proposition 1.** Φ is injective on its entire input probability-law domain for every fixed finite h>0.

**Proof.** Center X and Z at g and write their characteristic functions. The OU identity is

    χ_(D r)(u)=χ_r(Aᵀu) exp(−uᵀQu/2).

The Gaussian factor never vanishes and A is invertible. Equality of the output laws therefore gives equality of the characteristic functions of the inputs at every argument, hence equality of those laws. This is the inherited heat cancellation argument with an invertible affine drift.

If R_a(fπ)=R_a(kπ), then f^a/Z_f=k^a/Z_k π-almost everywhere. Thus f=c k for a positive constant c, and integrating gives c=1. Both D and R_a are injective on their respective domains, so their composition is injective. □

On the actual reaction image, if s=dq/dπ, the inverse is

    f = s^(1/a) / ∫s^(1/a)dπ.                         (2)

The denominator is finite for points in that image; arbitrary probability densities need not satisfy this condition. Undoing Gaussian convolution is likewise a map only on the actual image. The formal characteristic-function inverse need not be a characteristic function for an arbitrary proposed output. This report asserts no stable deconvolution, error bound, efficient finite encoding, or valid inverse on arbitrary perturbed outputs.

Finite compositions of fixed known injective steps remain injective. Convergence as the number of steps tends to infinity to a common target is compatible with injectivity at every finite step. Infinite-time collapse and finite-time exact-law encoding are different statements.

## 4. A fixed likelihood fails even for the normalized-only contract

**Proposition 2.** There is an M independent of r such that

    Φ(B_Lr)=B_MΦ(r)  for every r∈P₂                  (3)

if and only if L is constant pointwise.

**Proof.** For any x, B_Lδ_x=δ_x. Equation (3) therefore implies B_MΦ(δ_x)=Φ(δ_x). A normalized multiplier fixes a probability q exactly when it is constant q-almost everywhere, equal to its normalizer. Φ(δ_x) has a strictly positive Lebesgue density, so M must be one positive constant Lebesgue-almost everywhere. Every Φ(r) is also equivalent to Lebesgue measure, hence B_M fixes every Φ(r).

If L(x)≠L(x′), take r=(δ_x+δ_x′)/2. Its reweighted atom masses differ from 1/2, so B_Lr≠r. Proposition 1 gives Φ(B_Lr)≠Φ(r), contradicting (3). Conversely a constant L gives the identity audit and a constant M works. □

This is stronger in one respect than simply applying the received Theorem B: it concerns a nonlinear postprocessing and asks only for normalized outputs. The proof nevertheless uses classical injectivity and the same point-mass/full-support mechanism. It is an application, not a replacement for the earlier theorem.

For a concrete actual-OU witness, take d=T=1, g=0, h=log 2, so A=1/2, Q=3/4, a=1/2. Let r=(δ_−1+δ_1)/2, and L(x)=1 for x≤0 and 2 for x>0. If k_±(z) are the two OU Gaussian densities, then k_+/k_−=exp(4z/3), and

    ℓ_r(z)=(k_−+2k_+)/(k_−+k_+).

Its values at z=0 and z=(3/4)log 2 are 3/2 and 5/3. Therefore the density ratio Φ(B_Lr)/Φ(r) changes by the factor sqrt(10/9) between those two points. Both density ratios are continuous, so this is a genuine law difference, not merely a choice of null-set versions.

No conclusion says noise annihilates the input law. In contrast to the noninjective transition collision in historical-source-revision §7, no two distinct incoming laws collide here.

## 5. Exact state-dependent repair and evidence normalizers

The OU kernel gives the explicit version

    ℓ_r(z) = [∫L(x)ϕ_Q(z−g−A(x−g))r(dx)]
             / [∫ϕ_Q(z−g−A(x−g))r(dx)].               (4)

For bounded positive L, the denominator is positive and the ratio is Borel, positive, and bounded above. The elementary change-of-measure identity is

    D(B_Lr)=B_(ℓ_r)(D r),   ∫ℓ_r d(D r)=Z_r.         (5)

It follows either by integrating the kernel or by the defining conditional-expectation identity. If f=d(D r)/dπ, then D(B_Lr) has ratio ℓ_r f/Z_r. Raising it to a and normalizing cancels Z_r^a, proving (1).

Thus a decoder using the exact output law alone and the known operator and likelihood can be written on the valid image as

    q ↦ Φ(B_L(Φ⁻¹q)).                                (6)

The prior-dependence in (4) can be supplied by recovering r. A retained incoming law or suitable joint conditional model is a sufficient implementation route, not a universal extra-memory lower bound. A finite-moment summary, finite sample, approximate density, or arbitrary encoded state has not been shown to implement (6).

The canonical final multiplier ℓ_r^a has output normalizer

    H_r=∫ℓ_r^a dΦ(r),

which generally differs from Z_r. Equation (1) is a posterior-law identity; it does not identify H_r with the probability or mass ratio of the original audit. For a full evidence contract retain or recover Z_r from (5) or from r. One could scale the final multiplier by Z_r/H_r to match that scalar as well, but this scale is itself state-dependent and requires both quantities. A likelihood ratio used to replace a historical factor has its own mass-ratio meaning, not automatically the probability of a new report.

For successive audits, the conditional factor must also be revised. With r′=B_(L₁)r,

    E_r[L₁|Z] E_(r′)[L₂|Z] = E_r[L₁L₂|Z].            (7)

This follows by changing the conditional input law by L₁. Raising to a gives the correct product of successive transported multipliers. Multiplying the two conditional expectations both computed under the old r is generally wrong. This is exactly the source-interaction warning already present in the received Theorem B and inherited historical revision contract.

## 6. Gaussian positive class, recovery, and actual implementation test

Let r=N(m,S), S≥0, and L_θ(x)=exp(θᵀx) for a finite real θ. All required exponential and second moments are finite within this Gaussian class, including singular S. Completing the square on its support, or its moment generating function, gives B_(L_θ)r=N(m+Sθ,S).

Put

    S_D=ASA+Q,  C=[a S_D⁻¹+(1−a)T⁻¹]⁻¹,
    m_+=g+C a S_D⁻¹A(m−g).

The corrected audited mean is m_++C b with the same covariance C, where

    b=a S_D⁻¹ A S θ.                                 (8)

Hence the exact transported output factor is exp(bᵀz), up to a scalar. This is also (4) raised to a: the Gaussian conditional mean of X given Z is m+SA S_D⁻¹[z−g−A(m−g)], and its conditional covariance is independent of z. In particular b does not depend on m. For known fixed S, all Gaussian prior means therefore admit one fixed output multiplier for this fixed θ. This restricted-class positive result does not contradict Proposition 2, whose domain includes arbitrary two-point laws and Dirac laws at every location.

Allowing S to vary generally changes b. In the scalar fixture T=1, h=log 2, θ=1, it equals S/(S+3), taking 1/4 at S=1 and 4/7 at S=4. Both corresponding outputs have full support, so no single multiplier can give both required tilts. Singular S=0 gives b=0: the input point mass is unchanged by its audit.

For Gaussian q=N(m_+,C) in the exact image, incoming parameters can be reconstructed:

    P₀=C⁻¹−(1−a)T⁻¹,
    S_D=a P₀⁻¹,
    S=A⁻¹(S_D−Q)A⁻¹,
    m=g+A⁻¹(S_D/a)C⁻¹(m_+−g).                        (9)

The necessary and sufficient covariance range conditions are P₀>0 and S_D−Q≥0; an arbitrary C>0 is insufficient. Given these and any finite m_+, (9) yields S≥0 and reproduces the supplied q. Boundary equality permits singular input covariance. In the scalar T=1, h=log 2 fixture the range is 6/7≤C<2. C=1/2 fails the recovered-input PSD condition; C=3 fails the reaction precision condition. No numerical inversion stability follows.

The executable controls use the inherited noncommuting fixture T=diag(1,2), S=[[2,1],[1,3]], h=log 4, together with θ=(2,−1). They symbolically check (8)–(9), the Gaussian conditional-expectation coefficient, a wrong matrix ordering countercontrol, singular and partial-rank inputs, and whole Gaussian density ratios. A separate labelled floating-point test calls the **copied, hash-bound actual inherited gaussian_step.py**, comparing audit-then-correction against output tilt. These checks do not replace the proofs or certify floating-point error globally.

## 7. Conditional audits and the global observed-marginal guard

For μ(dy,dx)=ν(dy)r_y(dx), a separately normalized conditional audit B_(L_y)r_y preserves ν. Subject to measurability and the input moment hypotheses, (1) applies on ν-almost every fibre. Global boundedness of L alone does not guarantee that dividing by very small Z_y preserves the integrated relative second moment. A sufficient condition is 0<c≤L(y,x)≤C<∞, or one can directly verify the audited integrated moment. No unjustified interchange of normalization and disintegration is used.

A global joint Bayesian audit is a different operation. It changes the observed marginal to

    ν_L(dy)=Z_y ν(dy)/∫Z_y dν,   Z_y=∫L_y dr_y.

Unless Z_y is ν-almost everywhere constant, this is outside the fixed-ν operator's declared input fibre. It is not a counterexample to its conditional contract.

If one explicitly extends the family of fibrewise operators to accept each input's own observed marginal, then the exact joint output multiplier relative to ν(dy)Φ(r_y)(dz) is, up to one global scalar,

    M(y,z)=Z_y ℓ_(r_y)(z)^a/H_y,
    H_y=∫ℓ_(r_y)^a dΦ(r_y).                          (10)

Indeed its y-conditional normalizer is exactly Z_y, while its conditional update is (1). Merely using ℓ_(r_y)^a globally would generally give the wrong y-marginal.

The parent's exact two-fibre discriminator makes this visible. Take ν=(1/2,1/2), the same conditional δ₀ on both fibres, L₀=1/4, L₁=1, and a=1/2. The true global audit yields (1/5,4/5). Using ℓ_y^a as a global weight yields (1/3,2/3). Equation (10) restores (1/5,4/5); the common conditional law does not change under either conditional audit. This does not turn a globally updated marginal into the original ν.

## 8. Cross-front interpretation and stopping boundary

- Theorem B already owns conditional Bayes transport; this packet adds its exact composition with R_a and the actual Φ interface. Its full-evidence theorem and the normalized-only Proposition 2 are explicitly distinguished.
- Theorem J concerns labelled positive-simplex flows under fixed-context, arbitrary weight audits. The entropy correction changes whole laws and is not that finite labelled state space. Its failure of the fixed-M property neither refutes J nor demonstrates a new defect in the inherited exact split.
- Source-audit-revision owns selection-sensitive report conditioning and the distinction between an observed audit and replacing an adopted model factor. The present identities start only after a justified numerical L or ratio has been specified. They do not decide whether it is evidentially correct.
- Historical-source-revision owns occurrence/version records and sufficient historical/current joint state. Its noninjective finite transition example proves missing information for that transition. Φ's injectivity rules out importing that information-loss proof without checking the operator. A recoverable exact numerical law does not itself retain occurrence IDs or factor versions.
- The heat review owns Gaussian-convolution injectivity and the persistence of distinct moment-equivalent laws. The tensor results own operation-relative sufficient information and finite known-support closure. Nothing here recovers arbitrary probability laws from finitely many moments, or even from all moments without a determinacy premise.
- If two source histories already map to the same incoming law, Φ maps them to the same output. Injectivity on laws cannot restore source identity, operative basing, permissions, or warrant provenance previously omitted by the history-to-law map. Retain the appropriate inherited record when queries depend on those distinctions. This is inherited composition logic, not a new philosophical or warrant theorem.

The bounded outcome is an attributed interface result with positive and negative controls. It does not establish a new splitting method, a new general audit theorem, arbitrary-law finite computation, inversion stability, target authentication, new warrant, or T20 closure. No new rate or cost campaign is opened.
