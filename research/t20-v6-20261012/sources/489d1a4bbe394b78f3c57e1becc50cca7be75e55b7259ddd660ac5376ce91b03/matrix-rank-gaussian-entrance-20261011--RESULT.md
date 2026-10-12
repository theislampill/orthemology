# Matrix-rank Gaussian entrance with a fixed entire observed marginal

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. The parent proposed the matrix multiplier, covariance equation, nullspace test and codimension asymptotics. This report checks those proposals by full-density projection and proves the resulting entrance theorem. No protected edits, independent-review claim, formal-kernel certification, empirical warrant, field-priority claim or programme closure.

## 1. Statement and exact scope

Let k,m be positive finite integers, Y~N(0,I_k), G~N(0,I_m) independent. For B in R^(m×k) and symmetric S≥0, write μ(B,S) for the law of

    (Y, BY+S^(1/2)G),
    Σ(B,S)=[[I_k,Bᵀ],[B,BBᵀ+S]].

Fix a supplied target π=μ(B*,T), T>0, and set Γ=Σ(B*,T), Q=Γ⁻¹. Keep the inherited unit Euclidean transport/centred-reaction action and the constraint that the entire observed law stays N(0,I_k). All means here are zero. Set H=[I_k;B] and

    M=Q_yy+Q_yz B−I_k,
    N=HᵀQH−I_k,
    P=(M+Mᵀ+N)/3,
    Pbar=diag(P,0_m).

Define the symmetric polynomial matrix field

    F(B,S)=2I_(k+m)+Σ−QΣ−ΣQ−ΣQΣ
                         +PbarΣ+ΣPbar+ΣPbarΣ,       (1)

and the polynomial parameter system

    B′=F_zy,
    S′=F_zz−B′Bᵀ−B(B′)ᵀ.                         (2)

For every initial B₀ and S₀≥0, (2) has a unique global forward solution. It has S(t)>0 for every t>0, and its positive-time Gaussian laws solve the actual full-law constrained KL gradient equation. They converge in W₂ to μ(B₀,S₀) as t↓0 and to π as t→∞, with KL→0 at infinity. Uniqueness asserted here is within this centred Gaussian class with the specified trace, not all-law weak PDE uniqueness.

Suppose r=dim ker S₀>0. Let R=range S₀, K=ker S₀, and let U and V have orthonormal columns spanning R and K. Use determinant 1 for the empty R block. Put

    A_R=UᵀS₀U,
    A_K=2Vᵀ(I_m+B₀B₀ᵀ)V,
    d₀=det A_R det A_K>0.

Then, as t↓0,

    det S(t)=d₀ t^r(1+O(t)),
    E(t)=KL(μt||π)=−(r/2)log t+C₀+O(t),
    D(t)=r/(2t)+O(1),                              (3)
    C₀=½[tr(T⁻¹S₀)+tr((B₀−B*)ᵀT⁻¹(B₀−B*))
                        −m+log det T−log d₀].

Here D is the minimum instantaneous full-field action representing this density tangent. Thus its original-time action diverges, but the length of this specified curve is

    L(0,ε)=∫₀^ε√D(t)dt=√(2rε)+O(ε^(3/2)).          (4)

The time change t=u² has action density 2r+O(u²), including a finite-action singular endpoint. The unit-time endpoint competitor t=εu², u∈[0,1], has total action 2rε+O(ε²). These are curve-specific statements, not geodesic minimality or equality with an endpoint distance. For r=0 there is no entrance singularity; the positive-state theorem applies directly.

The coefficient r is the codimension of the initial joint Gaussian support: rank Σ₀=k+rank S₀, hence nullity Σ₀=r. This covers partial rank loss and interacting, noncommuting matrix data. It is not a collection of independent scalar examples.

## 2. Full-density projection, including the observed flux

Use the inherited operators

    Dμ(v,α)=−div(μv)+μα,
    jμf=(∇f,f−μf),       Kμf=Dμjμf,
    Bμ(f,g)=∫∇f·∇g dμ+Covμ(f,g).

For the orthogonal observation p(y,z)=y, the constrained negative gradient is −Kμ(q−φ∘p), where q=log(dμ/dπ) modulo constants and Kνφ=p_*Kμq, ν=N(0,I_k). This is the full Hilbert-quotient orthogonal projection inherited from fixed-marginal-correction, not a covariance-only optimization.

For S>0 put A=Q−Σ⁻¹, so q=xᵀAx/2 plus a constant. Conditional Gaussian expectation gives

    E[∇y q|Y=y]=My,
    E[q|Y=y]−E[q]=½(yᵀNy−tr N).                   (5)

Indeed Σ⁻¹H=[I_k;0], and HᵀΣ⁻¹H=I_k. The remaining conditional covariance term in E[q|y] is constant in y. Notice M need not be symmetric. Averaging both transport and reaction yields

    p_*Kμq=−div_y(νMy)+½ν(yᵀNy−tr N)
           =½ν[yᵀ(M+Mᵀ+N)y−tr(M+Mᵀ+N)].         (6)

The antisymmetric part of M contributes zero. Under the standard Gaussian observed law, the weighted operator −ν⁻¹div(ν∇)+I acts with eigenvalue 3 on every centred quadratic. Therefore the unique centred weak multiplier is

    φ(y)=½(yᵀPy−tr P),       P=(M+Mᵀ+N)/3.        (7)

This also follows from coercivity of the inherited weighted Sobolev solve. Omitting the observed flux term M+Mᵀ would generally fail the entire marginal constraint.

Set C=Q−Σ⁻¹−Pbar. The minimizing negative-gradient fields are

    v(x)=−Cx,
    α(x)=−½(xᵀCx−tr(CΣ)).                         (8)

Gaussian tails justify the polynomial cutoffs, integration by parts, and L² pairings. Their action is

    D=tr(CΣC)+½tr(CΣCΣ)≥0.                        (9)

They minimize among every admissible field representation of the entire density tangent, by the inherited potential-field quotient theorem, not just Gaussian or linear/quadratic competitors.

The full Gaussian density derivative is

    ρ′/ρ=−½tr(Σ⁻¹Σ′)+½xᵀΣ⁻¹Σ′Σ⁻¹x.

For Σ′=−CΣ−ΣC−ΣCΣ, it equals

    tr C−xᵀΣ⁻¹Cx−½xᵀCx+½tr(CΣ),

which is exactly (−div(ρv)+ρα)/ρ. Thus the entire density PDE, not only covariance moments, is satisfied. Expanding Σ⁻¹ contributions gives (1). Moreover

    F_yy=−(M+Mᵀ+N)+3P=0.                         (10)

Consequently the covariance tangent has precisely the form (2), and the mean remains zero. The full observed Gaussian distribution is retained.

## 3. Local entrance through every missing covariance direction

The right side of (2) is polynomial on all B and all symmetric S. Standard finite-dimensional ODE existence and uniqueness applies even when S₀ is singular. For v∈ker S₀, define n=(-B₀ᵀv,v). Then Σ₀n=0. In (1), every term except 2I has Σ on at least one side, so

    nᵀF(B₀,S₀)n=2|n|²=2vᵀ(I_m+B₀B₀ᵀ)v.

Using F_yy=0 and the definition of S′ proves

    vᵀS′(0)v=2vᵀ(I_m+B₀B₀ᵀ)v.                  (11)

Polarization yields VᵀS′(0)V=A_K>0.

For clarity, positivity is not inferred from an eigenvector moving with t. Use the fixed orthogonal basis [U,V]. Smoothness gives the block expansion

    [U,V]ᵀS(t)[U,V]
       =[[A_R+O(t), O(t)],
         [O(t), tA_K+O(t²)]].                     (12)

The upper block is positive definite for small t; its Schur complement is tA_K+O(t²), also positive definite for small positive t. If R is empty only the lower block is present. Thus S(t)>0 for all sufficiently small positive t. The block determinant formula gives (3)'s determinant coefficient. The division det S(t)/t^r extends smoothly and positively through t=0: determinant and blocks are smooth, and their vanishing orders were established explicitly. In fact the polynomial ODE solution is locally analytic.

There is no probability continuation to all small negative times when r>0: the lower Schur block has negative quadratic directions there. No inverse covariance, logarithmic score, or finite ordinary initial KL gradient is assigned at zero.

## 4. Positive-time global continuation and convergence

The exact conditional KL is

    E(B,S)=½[tr(T⁻¹S)+tr((B−B*)ᵀT⁻¹(B−B*))
                              −m+log det T−log det S].       (13)

Let λ_i be the positive eigenvalues of T^(-1/2)ST^(-1/2). Then

    E=½‖T^(-1/2)(B−B*)‖_F²
                         +½Σ_i(λ_i−1−log λ_i).             (14)

Every finite sublevel therefore bounds B, bounds S above and keeps S uniformly positive definite. These sublevels are compact within the positive-state parameter domain. The full projection yields E′=−D. One can also obtain this by differentiating (13) along (2).

For S>0, the first summand of (9) is ‖Σ^(1/2)C‖_F². Thus D=0 forces C=0. Its zz and zy blocks imply, using the block precision formula,

    T⁻¹−S⁻¹=0,
    −T⁻¹B*+S⁻¹B=0,

so S=T and B=B*. Conversely the target makes C,P and F zero. Thus D vanishes exactly at the target, with no need to calculate a full coordinate mobility matrix.

Starting at any positive time in the locally constructed entrance, descent confines the state to its finite compact KL sublevel. Smooth ODE continuation is global and prevents future rank loss. D is smooth on that compact set, its time derivative is bounded, and ∫Ddt is finite from that positive time. Hence D(t)→0 by uniform continuity and integrability. Every subsequential limit lies at its unique zero, so B→B*, S→T, E→0. Standard Gaussian coupling gives W₂ convergence. This establishes the claimed global entrance, using no finite value E(0).

## 5. Codimension asymptotics, length and endpoint action

Inserting the smooth determinant factorization and B(t)=B₀+O(t), S(t)=S₀+O(t) into (13) gives (3)'s E and C₀. The remainder after subtracting −(r/2)log t is smooth at zero, so differentiating it is legitimate. Since E′=−D at positive times,

    D(t)=r/(2t)+O(1).

This argument uses smooth factorization, not differentiation of an arbitrary O(t) remainder. Therefore E(0)=∞ and ∫₀^εDdt=∞, whereas integrating √D gives (4). The exact leading coefficient loses target and orientation dependence because each missing covariance direction contributes one logarithmic determinant factor. The determinant prefactor d₀ retains geometric information, including B₀ and the positive initial conditional covariance.

At every positive time, (8) minimizes action among all fields realizing this same full density tangent. Thus alternative representations cannot make the original-time action finite. The meaningful energy identity is E(h)−E(T)=∫_h^T Ddt for h>0, not a finite-energy identity at h=0.

For t=u², multiply v and α by 2u. The action density is

    4u²D(u²)=2r+O(u²).                             (15)

For a unit-time endpoint curve t=εu², it is 2rε+O(ε²u²); integration gives 2rε+O(ε²). Time change preserves the curve and its whole marginal but changes its speed. It is not the original KL gradient flow in the new clock. These explicit finite-action competitors neither prove geodesic minimality nor imply a noncompact endpoint minimizer exists.

## 6. Trace, weak endpoint equation and the Gaussian uniqueness boundary

Use the common independent pair (Y,G). The squared coupling displacement from the initial law is

    ‖B(t)−B₀‖_F²+‖S(t)^(1/2)−S₀^(1/2)‖_F²→0,

by continuity of the positive-semidefinite square root. Thus μt→μ₀ in W₂ and narrowly. When r>0, μ₀ lies on a proper linear subspace and μt has a positive Lebesgue density for t>0, so total-variation convergence is impossible.

On every finite [0,T], ∫√Ddt is finite. Probability Cauchy–Schwarz gives

    ∫₀^T∫(|v|+|α|)dμt dt≤√2∫₀^T√Ddt<∞.

The continuity equation on [h,T], tested against compactly supported C¹ functions, therefore passes to h↓0 using the narrow trace and finite spacetime total variation. This is an endpoint L¹ distributional equation with no impulsive source. It does not satisfy the original-time finite-L²-action endpoint contract. The u²-reparametrized fields do satisfy that contract, and their endpoint equation follows the same way. Values assigned to fields on the single initial time slice have no effect.

If a centred Gaussian classical positive-time projected-flow entrance has the same narrow Gaussian trace, its covariance parameters converge to B₀,S₀ by the finite-dimensional Gaussian weak-convergence criterion. This is not a general inference of moment convergence from narrow convergence. Its parameters solve (2). Continuity of the polynomial field near the trace permits integration down to zero, giving the initial-value integral equation and ODE uniqueness. This proof is restricted to centred Gaussian entrances; it does not silently claim uniqueness for noncentred Gaussians or arbitrary weak PDE solutions.

Positive-definite initial approximations B_n→B₀, S_n→S₀ converge uniformly in parameters on every finite time interval by smooth ODE continuous dependence in a compact tube around the entrance. Their laws converge uniformly in W₂ by the coupling and uniform continuity of the matrix square root on bounded positive-semidefinite sets. On [h,T], h>0, E and D converge uniformly. Their initial energies and original-time actions are not uniformly bounded as n→∞ when r>0.

## 7. Inheritance, primary ancestry and bounded new scope

The copied hash-bound inputs in INPUT_BINDINGS.json were inspected. The scalar singular-entrance packet already owns the one-dimensional entrance mechanism, finite-length/infinite-action distinction, trace and reparametrization argument. The correlated-target packet owns the required observed-score flux correction. The fixed-marginal packet owns the full Hilbert-quotient projection, cutoff justification and full tangent minimum. The Gaussian primary-comparison packet owns the exact relationship to normalized Gaussian SHK dynamics.

This report generalizes those arguments to arbitrary finite observed/latent dimensions and partial conditional rank loss. Its explicit matrix multiplier, strict nullspace inflow and determinant codimension law are not statements located in those inspected predecessor reports. No exhaustive corpus or literature nonduplication claim is made. The scalar k=m=r=1 specialization is checked exactly, and is inherited rather than new.

Classical Gaussian SHK covariance dynamics and entropy smoothing are credited to Liero, Mielke, Tse and Zhu, Evolution of Gaussians in the Hellinger–Kantorovich–Boltzmann gradient flow, §§2 and 3.4 (normalized Gaussian dynamics): https://arxiv.org/html/2504.20400v1 . The inspected source treats the positive-definite Gaussian parameter domain and supplies the unconstrained mechanism. The present constrained matrix/rank statement is derived here rather than attributed to a theorem not located there.

Weighted-Sobolev projection under path constraints is classical ancestry: Bauer, Charon, Needham and Nishino, Path constrained unbalanced optimal transport, §3.2 and Remark 4.24: https://arxiv.org/html/2402.15860v3 . Classical block Gaussian precision, Schur complements, smooth ODE continuation and determinant asymptotics do the remaining work. No discovery claim for those tools or for Gaussian regularization generally is made.

The observed covariance I_k is part of the declared scope. Arbitrary whitening of a nonidentity observed marginal changes the Euclidean transport metric unless its pullback is tracked. Therefore this result does not assert an unchanged formula for arbitrary observed covariance. Targets, geometry and normalization are supplied, not learned or epistemically authenticated.

## 8. Exact controls and exclusions

Run `python3 verify.py`, or use `--output private-locator:89feb0c096e035676ad0`. CHECKS.json records 31 passing exact symbolic/rational controls. They cover matrix observed-block cancellation, three distinct singular ranks, nullspace strict inflow and determinant leading coefficients, a genuinely noncommuting positive matrix case, entire density polynomial coefficients, KL dissipation, target stationarity, scalar predecessor specialization and input hashes. The chosen finite matrices supplement the general-dimensional proof; they are not a sampling campaign or a substitute for it.

The result makes no general non-Gaussian singular-entrance theorem, all-law uniqueness claim, arbitrary observed-marginal transfer, geodesic or completeness assertion, convergence-rate campaign, empirical-noetic warrant, protected integration or T20 closure claim.
