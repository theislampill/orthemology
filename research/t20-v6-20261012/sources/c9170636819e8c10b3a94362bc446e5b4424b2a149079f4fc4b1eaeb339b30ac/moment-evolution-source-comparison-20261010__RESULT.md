# Moment-evolution sources: comparison, obstruction, and affine extension

10 October 2026 UTC. Additive ordinary mathematical research. No canonical repository or earlier packet was edited. This is a bounded reading of identified primary sources, not a novelty search or an independent review of Theorems G/V. Sources, hashes, and precise reading boundaries are in SOURCE_MANIFEST.json, INPUT_BINDINGS.json, and READING_BOUNDARIES.md. No numerical sampling campaign was performed.

## 1. Outcome

The inspected arguments do not subsume or contradict Theorem G or Theorem V. In particular, their measure-evolution formulas do not supply our missing initial measure from an abstract, full, square-positive hierarchy. The literature gives useful comparisons, not a replacement existence proof.

Two substantive consequences emerge:

1. **Obstruction:** full dynamic square positivity does not force representability for the heat hierarchy, even on a small positive-time interval. The proof below constructs the obstruction without assuming an underlying vector measure. Consequently our conditional negative-square witness result cannot be transferred to arbitrary diffusion moment equations.
2. **Positive extension:** Theorem V immediately extends to affine transport plus its SOS-dominated polynomial killing, by a polynomial-preserving characteristic change of coordinates. The full proof is below; it is a corollary of V, not a claim that the identified sources establish reverse existence.

A source caution matters: the current 2026 v3 of the PDE/atoms preprint contains a uniform-time assertion (Corollary 3.22) incompatible with spatial dilation. Its pointwise assertion (Theorem 3.21) is a different statement and is not refuted by this argument. Do not import the uniform parameter into a representation certificate.

## 2. Exact source comparison

### Heat and linear transport, 2021 arXiv v1

Curto–di Dio, https://arxiv.org/pdf/2108.03505v1 . Lemma 2.1 derives a degree-lowering heat moment recursion from Schwartz data; Definition 2.3 then defines its finite polynomial solution for arbitrary sequences. Theorem 2.10 assumes a moment sequence and describes its allowable heat times. Theorem 2.23 preserves initial indeterminacy forward; Corollary 2.25 preserves determinacy only backward through allowable times. Section 3 transports measures by an invertible diagonal linear map and scalar factor; Corollary 3.7 preserves all four stated determinacy classes. Thus heat does not perform coercive-killing regularization of a moment fibre.

The 2023 journal publication is verified as bibliographic metadata at https://academic.oup.com/imrn/article-abstract/2023/17/14955/6696867 . Its full published text was not retrieved. These theorem numbers and proof readings refer to the 20-page arXiv v1, not an assumed identical journal version.

### General PDE and atoms, original 2022 v1 and current 2026 v3

Curto–di Dio–Korda–Magron, https://arxiv.org/pdf/2211.04416v3 . Theorem 2.2 assumes Schwartz initial data and spatially smooth bounded coefficients (including all spatial derivatives); its dual generally leaves the polynomial algebra. Lemma 4.1 assumes an initial atom and smooth bounded transport/reaction coefficients. V3 corrects the atomic weight to include divergence. Theorem 4.2 starts with a finite-rank moment sequence, not arbitrary square positivity. Corollary 3.25 is an exception to a blanket “all results assume representation” description: it proposes a strict-square-positive backward-heat criterion for ternary degree-four truncated functionals, relying on Corollary 3.22's uniform time. Neither is our full hierarchy theorem. Theorem 3.9 preserves SOS under positive convolution; Lemma 3.16 obstructs heat-to-SOS conversion when the leading form is non-SOS.

The older atomic weight in https://arxiv.org/pdf/2211.04416v1 omits divergence. V3 is therefore the relevant version for that convention. No assertion that the whole paper is invalid is warranted by a localized issue below.

### Classical killing is not the reverse-existence step

The author-hosted Fitzsimmons–Pitman Feynman–Kac discussion, https://mathweb.ucsd.edu/~pfitz/downloads/kac/node11.html , begins with a supplied Markov process and its killed semigroup. Its HTML prose was read, but the image-only equations were not audited, and no theorem from it is imported here. The familiar survival/likelihood formula is classical. Our additional question is whether an abstract polynomial hierarchy has any representing law in the first place.

## 3. Full square-positive heat paths can be non-moment paths

This is a reader-derived mathematical consequence. It uses the classical existence of a square-positive non-moment functional on R[x,y], already identified in the accepted G packet as Schmüdgen 2017, Proposition 13.5. It is not a newly constructed explicit functional or a new priority claim.

Let Λ be such a functional. It is nonzero. If Λ(1)=0, Cauchy–Schwarz gives |Λ(p)|²≤Λ(p²)Λ(1)=0 for every p, a contradiction. Hence scale it to Λ(1)=1.

For a polynomial p define the finite algebraic heat operator

    P_t p = exp(tΔ)p = Σ_{k=0}^{floor(deg(p)/2)} t^k Δ^k p/k!.

For polynomials f,g there is the finite identity

    P_t(fg)=Σ_α (2t)^|α|/α! · (P_t∂^αf)(P_t∂^αg).      (S)

Indeed, on the diagonal x=y the Laplacian of a product corresponds to Δ_x+Δ_y+2Σ_i∂_{x_i}∂_{y_i}. These operators commute and lower total degree, so their exponential series are finite on polynomial inputs and can be multiplied without convergence assumptions. Apply the resulting operator to f(x)g(y), then restrict to x=y. This proves (S).

With f=g=q and t≥0, (S) expresses P_t(q²) as an actual finite sum of polynomial squares. Moreover, if q is nonzero and β indexes any nonzero highest-total-degree monomial, ∂^βq is a nonzero constant. Its term in (S) has strictly positive constant coefficient whenever t>0. This observation will yield strict square positivity, not just nonnegativity. No measure for Λ was introduced.

Define

    L_t(p)=Λ(P_t p),    t≥0.

Then every coordinate is polynomial in t, L_t(1)=1, L_t(q²)≥0 for every q and every t≥0, and in fact L_t(q²)>0 for q≠0 and t>0 by (S) and Λ(1)=1. Also

    L_t'(p)=Λ(ΔP_t p)=L_t(Δp).

Because Λ is not a moment functional, Haviland's theorem implies that some globally nonnegative polynomial F has Λ(F)<0. The finite polynomial t↦Λ(P_tF) is continuous and strictly negative at zero. Therefore there is ε>0 with

    L_t(F)<0,    0≤t<ε.

No L_t in this interval has a positive representing measure. This is a genuine positive-time obstruction, not merely invalid data at the initial boundary. All square tests pass on the entire forward half-line, but nonrepresentability has only been proved on [0,ε). Nothing here decides what occurs afterward.

In particular, an algorithm restricted to searching for negative polynomial squares cannot detect these invalid heat records, since no such witness exists anywhere along this path. The finite nonnegative witness F is not a square or SOS. Our coercive-killing witness corollary has different generator and coercivity promises; the example does not challenge it.

The failure can occupy any prescribed finite horizon [0,H], using a different initial functional. Put Λ_a(f)=Λ(f(a·)) and F_a(x)=F(x/a), for a>0. These preserve normalization and square positivity. Heat covariance gives

    Λ_a(P_tF_a)=Λ(P_{t/a²}F).

Choose a²>H/ε. The right side is then negative throughout [0,H]. Thus one can arrange an arbitrarily long finite interval of nonrepresentation, with strict square positivity at all positive times. This is a family depending on H, not one path proved nonrepresentable for all times. No explicit computational model for the classical Λ is claimed.

**Preserved positive boundary.** If the initial functional is already represented by μ, its heat path is represented by μ convolved with the Gaussian heat kernel. The degree-lowering equations determine each coordinate uniquely by induction on degree, so the counterexample cannot be interpreted as a fake alternative heat path departing from valid initial full moments. Two distinct laws with the same initial moments instead have the same entire heat moment path. Their Gaussian convolutions remain distinct because the Gaussian Fourier multiplier never vanishes. Heat therefore neither resolves that moment fibre nor identifies which initial law was used; coercive killing in G/V has a different conclusion.

For comparison, pure invertible affine transport preserves the distinction even more directly. If Φ_t is an affine bijection, Λ_t(p)=Λ(p∘Φ_t) is square-positive. Any representing measure for Λ_t would pull back to one for Λ; hence Λ_t is nonrepresentable at every time. The nonnegative witness F_t=F∘Φ_t^{-1} satisfies Λ_t(F_t)=Λ(F)<0. For Φ_t(x)=e^t x this is a nonstationary hierarchy Λ_t'(p)=Λ_t(x·∇p).

## 4. A precise affine-transport extension of Theorem V

Assume the hypotheses on h_t from Theorem V, including the local common degree bound, continuous coefficients, and uniform SOS radial domination. Let

    v_t(x)=B_t x+b_t

with B_t,b_t continuous in time. Let L_t be normalized, square-positive, coordinatewise C¹, and satisfy

    L_t'(p)=L_t(v_t·∇p)−L_t(h_t p)+L_t(h_t)L_t(p).       (A)

Let Φ_t(y)=F_t y+d_t be the affine characteristic flow with Φ_0=id,

    F_t'=B_tF_t,   F_0=I,
    d_t'=B_td_t+b_t,   d_0=0.

On each finite time window F_t is invertible, its smallest singular value has a positive common lower bound σ, and d_t is bounded. Standard finite-dimensional linear ODE existence supplies this flow globally on every supplied finite coefficient window; no arbitrary continuous nonlinear-flow uniqueness is invoked.

Define the polynomial pullback functional

    M_t(q)=L_t(q∘Φ_t^{-1}),    h̃_t(y)=h_t(Φ_t(y)).

For each fixed q, q∘Φ_t^{-1} has a fixed finite degree and C¹ coefficients. The coefficientwise product rule is valid before any measure exists. The characteristic identity gives

    ∂_t(q∘Φ_t^{-1})+v_t·∇(q∘Φ_t^{-1})=0.

Substitution into (A) cancels transport and yields

    M_t'(q)=−M_t(h̃_tq)+M_t(h̃_t)M_t(q).

Also M_t(1)=1 and M_t(q²)≥0, since affine substitution preserves polynomial squares.

We must check the crucial domination rather than presume it. On a fixed compact window suppose h_t+C−c|x|² is SOS, and set D=max_t|d_t|. Since |F_ty|²−σ²|y|² is a positive-semidefinite quadratic form,

    h̃_t(y)+(C+cD²)−(cσ²/2)|y|²
      = [h_t(F_ty+d_t)+C−c|F_ty+d_t|²]
        +(c/2)|F_ty+2d_t|²
        +(c/2)(|F_ty|²−σ²|y|²)
        +c(D²−|d_t|²)

is a sum of squares. The other hypotheses of V are preserved by affine composition. Theorem V therefore supplies a unique probability μ, with all polynomial moments, such that

    K_t(y)=∫_0^t h_u(Φ_u(y))du,
    L_t(p)= ∫p(Φ_t(y)) exp(−K_t(y))dμ(y)
             / ∫exp(−K_t(y))dμ(y).                    (B)

This proves representation from the abstract transported hierarchy, not merely propagation of a supplied measure. Conversely (B), for any initial μ with every polynomial moment, satisfies (A): finite-window affine bounds and the preceding domination give polynomially dominated integrands for differentiation. Thus the initial representing-law fibre again parametrizes paths. Every positive-time record is determinate, since an affine bijection carries any alternative representative back to an alternative representative of M_t. The same reasoning yields unique continuation along a supplied future pair (v_t,h_t).

For an initially finite atomic μ, (B) moves the atoms by Φ_t and reweights them by exp(−K_t), followed by normalization. This recovers the expected characteristic mechanism while retaining the reverse-existence conclusion for unrestricted initial moment fibres.

**Density convention.** The unnormalized conservative equation corresponding to (A) is ∂_tν=−div(v_tν)−h_tν. A non-divergence-form equation ∂_tν=−v_t·∇ν+r_tν instead has test generator v_t·∇+(r_t+div v_t). Thus its killing potential is −r_t−div v_t. This explains the divergence in the current primary source; it must not be silently dropped. Spatially constant divergence cancels after normalization, but variable divergence generally does not.

**Limit.** This proof does not extend to general nonlinear transport merely by naming a flow. Its inverse may not preserve polynomials, its pulled-back energy may not satisfy V, and trajectories may escape in finite time. No diffusion-plus-killing theorem or arbitrary-coercive nonautonomous extension is asserted.

## 5. Version-specific obstruction to a uniform heat-to-SOS time

Printed p.20 of https://arxiv.org/pdf/2211.04416v3 , Corollary 3.22, quantifies

    ∃τ<∞  ∀f∈Pos(3,4)  ∀t≥τ : exp(tΔ)f ∈ SOS(3,4).

The definition of Pos imposes only nonnegativity and degree≤4; it imposes no spatial normalization. This differs from the pointwise quantifiers ∀f∃τ_f in Theorem 3.21. The p.14 Choi–Lam threshold calculation gives a convenient exact control, but the following independent argument needs only that Pos(3,4) strictly contains its closed SOS cone.

Suppose the uniform assertion held at some T>0. Put D_a f(x)=f(ax), a>0. Then

    exp(TΔ)D_af = D_a exp(a²TΔ)f.

Dilation preserves both cones in both directions. As a²T ranges over all positive times, the asserted fixed-T conversion would force exp(tΔ)f to be SOS for every t>0 and every nonnegative ternary quartic f. Letting t↓0 and using closedness of the finite-dimensional SOS cone would force every such f itself to be SOS, contrary to the classical Choi–Lam example. T=0 is contradicted immediately by the same example.

Concretely, for

    f_CL=1−4xyz+x²y²+x²z²+y²z²,
    f_a(x,y,z)=f_CL(ax,ay,az),

its exact heat-to-SOS entry time is 1/(9a²). Hence f_a→1 coefficientwise as a↓0 while the entry times diverge, whereas the constant 1 has entry time zero. Entry-time continuity does not follow from joint continuity of the polynomial flow. Multiplying each f_a by a positive scalar to normalize it on a usual compact cone base does not change its SOS entry time, so that maneuver cannot repair the argument.

This prevents use of Corollary 3.22's universal parameter and dependent Corollary 3.25 as a warranted reverse-existence shortcut. It does not refute the correctly different pointwise assertion of Theorem 3.21. No blanket claim is made about all subsequent statements (for instance a literal quadrature claim permitting all weights zero has a degenerate reading).

## 6. What remains warranted

- The accepted autonomous theorem G still depends on its compact-fibre existence bridge. Heat/transport semigroup formulas do not remove it.
- The time-varying theorem V still needs its uniform SOS radial certificate. Heat smoothing cannot repair a non-SOS highest form: a degree-lowering operator leaves that highest form unchanged.
- Finite negative-square controls can be decisive for a specified hierarchy with the right converse theorem. They are not a universal characterization of multivariate measure realizability.
- The affine extension is fully derived above but has not been independently reviewed here. A separate reviewer is checking the heat obstruction and uniform-time counterargument; its final report, when available, is separate evidence. The parent also contributed the general dilation proof and checked the pullback/SOS calculation; that participation is not independent review.
- The inspected sources establish no field-priority conclusion about G, V, this corollary, or the obstruction.
