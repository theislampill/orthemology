# Classifying reference-transported Bregman contraction

11 October 2026 UTC. Bounded continuation of `information-geometry-transport-20261009/RESULT.md` §6. Ordinary mathematical proof with symbolic/rational controls. No protected-source changes, integration, adoption, novelty claim, or programme closure.

## 1. Result and contribution

The quadratic reference repair extends exactly to generators whose reciprocal curvature is concave. It includes a continuum of nonquadratic, nonentropy generators. Probability normalization does not weaken this classification: a three-input/two-output deterministic merge already detects every failure of scalar joint convexity when the positive reference may vary.

This is an application of the classical Bauschke–Borwein joint-convexity criterion, not a new characterization in convex analysis. The useful continuation is the exact equivalence with the inherited reference-transport contract, its normalized-probability necessity argument, and its distinct equality/recovery requirements. A targeted depth-two search of local RESULT.md reports for `jointly convex`, `Bauschke`, and reciprocal curvature found no prior report of this classification. This is bounded local deduplication, not an exhaustive novelty search.

## 2. Exact theorem

Let φ belong to C³((0,∞)) and satisfy φ″>0. Define

    bφ(x,y)=φ(x)−φ(y)−φ′(y)(x−y),
    Fμ(p)=Σ_i μ_i φ(p_i/μ_i),
    Dμ(p,q)=Σ_i μ_i bφ(p_i/μ_i,q_i/μ_i).

Here μ is an arbitrary positive finite vector, not necessarily a probability law; p and q are strictly positive probability vectors. For every nonnegative column-stochastic m-by-n matrix K with no zero row, put ν=Kμ. Then these statements are equivalent:

1. Dν(Kp,Kq)≤Dμ(p,q) for every finite n,m and all admissible μ,p,q,K.
2. The same inequality holds just for n=3,m=2 and K merging inputs 1 and 2 and preserving input 3, for all μ,p,q.
3. bφ is jointly convex on (0,∞)².
4. r=1/φ″ is concave on (0,∞).

Positive scaling of φ changes divergence by that factor; adding an affine function changes no divergence. The reference is transported rather than reset or re-estimated.

### Joint convexity implies contraction

Set x_i=p_i/μ_i, y_i=q_i/μ_i, and w_ji=K_ji μ_i/ν_j. For each row, w_j is a probability vector and

    (Kp)_j/ν_j=Σ_i w_ji x_i,
    (Kq)_j/ν_j=Σ_i w_ji y_i.

Jensen applied to bφ gives the row inequality. Multiplication by ν_j and summation gives contraction because Σ_j K_ji=1. In fact the exact nonnegative gap is

    Dμ−Dν=Σ_j ν_j [Σ_i w_ji bφ(x_i,y_i)
                          −bφ(Σ_i w_ji x_i,Σ_i w_ji y_i)].

### Probability-normalized necessity

Fix arbitrary positive x₁,x₂,y₁,y₂ and λ∈(0,1). Let X=λx₁+(1−λ)x₂ and Y=λy₁+(1−λ)y₂. Choose 0<ε<min(1/X,1/Y), and set

    μ=(ελ, ε(1−λ), 1),
    p=(ελx₁, ε(1−λ)x₂, 1−εX),
    q=(ελy₁, ε(1−λ)y₂, 1−εY).

These laws are positive and normalized. Under the stated merge, the third coordinate and its reference stay unchanged, so their divergence terms cancel. The assumed inequality reduces to

    ε bφ(X,Y)≤ε[λbφ(x₁,y₁)+(1−λ)bφ(x₂,y₂)].

Divide by ε. Since the pairs and λ were arbitrary, bφ is jointly convex. Endpoint λ=0,1 is trivial. Thus no unconstrained-positive-mass premise has been smuggled into the probability theorem. Even requiring μ itself to be a probability law would suffice: take additionally ε<1 and use μ₃=1−ε instead; buffer cancellation is unchanged.

### Joint convexity iff concave reciprocal curvature

Write h=φ″>0. Direct differentiation gives

    Hess bφ(x,y) = [[h(x), −h(y)],
                     [−h(y), h(y)−(x−y)h′(y)]].

The first leading entry is positive. Thus positive semidefiniteness is equivalent to nonnegative determinant, equivalently

    h(y)−(x−y)h′(y) ≥ h(y)²/h(x).

Dividing by h(y)² gives

    r(x)≤r(y)+(x−y)r′(y).

This is exactly the tangent-majorant condition for the C¹ function r to be concave. Since bφ is C² on the open convex quadrant, its Hessian is positive semidefinite everywhere iff it is convex. No fourth derivative is needed.

## 3. Families, endpoints, and a negative control

For 1<α≤2, φ(t)=t^α has

    r(t)=t^(2−α)/(α(α−1)),

which is concave, strictly so for 1<α<2. These give genuinely nonquadratic/nonentropy examples in the interior of the range. The normalized family

    φα(t)=[t^α−αt+α−1]/[α(α−1)]

has φα″(t)=t^(α−2), extends at α=1 to t log t−t+1, and at α=2 is (t−1)²/2. Hence its endpoint divergences are KL and reference-weighted half-quadratic distance. The unnormalized t^α family itself tends to an affine, zero-divergence generator at α=1; calling that unnormalized limit entropy would be incorrect.

For φ=t log t, μ_i bφ(p_i/μ_i,q_i/μ_i)=p_i log(p_i/q_i)−p_i+q_i, so the summed divergence is KL and is independent of μ. For φ=t²/2, it is Σ(p_i−q_i)²/(2μ_i).

For φ=t⁴, r(t)=1/(12t²) is strictly convex, so universal contraction fails. The inherited exact witness is retained: μ=(1,1,1), p=(19/100,1/100,4/5), q=(31/100,29/100,2/5), with the same merge. Its coarse-minus-fine gap is 921/1562500>0.

A nonentropy positive check uses φ=t^(3/2), μ=(1/16,1/16,1), p=(1/4,1/16,11/16), q=(1/16,1/16,7/8). For the merge,

    Dμ(p,q)−Dν(Kp,Kq)=(18−5√10)/32>0,

since 18²>25·10. The unchanged buffer contributes equally on both sides.

## 4. Equality discriminates the transport contract

All row weights below are restricted to K_ji>0; zero entries do not matter. The exact gap above vanishes iff every rowwise Jensen gap vanishes.

### Strictly concave reciprocal curvature

If r is strictly concave, its tangent inequality is strict whenever x≠y. Consequently Hess bφ is positive definite off the diagonal x=y. Consider a nonconstant segment of pairs. Unless the entire segment lies on the diagonal, an open segment portion lies off it and the directional second derivative is positive there. The restriction of bφ to this segment cannot be affine. Thus Jensen equality between distinct pairs is possible exactly when all pairs lie on the diagonal.

For a finite collection the same conclusion follows either by restricting to any two unequal points with positive weights or by the supporting-plane criterion: equality at the barycenter forces bφ to equal its supporting plane at each point and throughout their convex hull. Therefore equality in a row occurs exactly when either:

- all supported pairs (p_i/μ_i,q_i/μ_i) are identical, or
- p_i=q_i on every supported input in that row.

The second case allows varying common density. It is essential; claiming all density pairs must coincide would be false. It applies in particular to 1<α<2.

### Entropy and quadratic endpoints

For entropy, the row gap can be written as A times the KL divergence between normalized row masses a_i/A and b_i/B, where a_i=K_ji p_i, b_i=K_ji q_i, A=Σa_i and B=Σb_i. Equality is exactly p_i/q_i constant over the row support. The reference cancels.

For φ=t²/2, the row gap is (ν_j/2) times Var_wj(x−y). Equality is exactly (p_i−q_i)/μ_i constant on the row support.

For strictly concave r, either rowwise equality case implies that p_i/q_i is constant over the row. Thus the q-Bayes reverse R_ij=K_ji q_i/(Kq)_j is column-stochastic and recovers both q and p: RKq=q, and rowwise likelihood-ratio constancy gives RKp=p. The same conclusion holds at the entropy endpoint. This is pairwise statistical recovery; it need not recover μ.

The interior power generators therefore impose different equality requirements from either endpoint. Divergence monotonicity alone does not mean they retain the same distinctions at equality.

### Common recovery is sufficient, not necessary

For every generator in the contractive class, if a nonnegative column-stochastic R satisfies RKp=p, RKq=q, and RKμ=μ, contraction through K and then R gives equality. Positivity of μ and RKμ ensures that R has no zero row.

The converse fails even when p≠q and divergence is positive. Set

    p=(1/8,1/8,1/4,1/2),
    q=(1/8,1/8,1/2,1/4),
    μ=(1/8,3/8,1/4,1/4),

and merge the first two coordinates, leaving the other two separate. The merged block has p=q, giving zero divergence before and after; all other terms are unchanged. Thus equality holds for every strictly convex φ. Nevertheless let A=[p q μ] and B=KA. Exact computation gives det B=−1/16 and the unique linear map satisfying RB=A is

    R=[[1/8, 1/8, 1/8],
       [7/8,−1/8,−1/8],
       [0,1,0],
       [0,0,1]].

Its negative entries exclude a stochastic common recovery. This is stronger than failure of the canonical μ-reverse: no simultaneous stochastic reverse exists.

### Quadratic equality can fail even pairwise recovery

Take μ=(1,1,1), p=(4/10,3/10,3/10), q=(3/10,2/10,5/10), with the three-to-two merge. Both transported quadratic divergences equal 3/100, since density differences agree on the merged row. But [Kp Kq] has determinant 1/5, and the unique simultaneous linear reverse is

    R=[[11/20,1/20],[9/20,−1/20],[0,1]].

Its negative entry excludes any stochastic reverse recovering even the two laws. Thus the distinction from the strictly concave class is substantive: equality of a quadratic score can retain its value while losing pairwise statistical information.

## 5. Interpretation and boundaries

The reference μ is an explicitly supplied numerical measure. This classification does not warrant it as a true prior, source authority, repository metaortheme, or canonical geometry. It classifies only the stated separable, common scalar-generator, transported-reference family. It is not a uniqueness theorem for all probability geometries, all potentials, or arbitrary choices of K-dependent score. Because μ is additional transported structure, these examples do not refute metric-uniqueness claims on unadorned probability simplices.

The coherent potential has Hessian diag(φ″(p_i/μ_i)/μ_i), positive definite on the ambient positive orthant and hence on simplex tangents. It can therefore be inserted into the inherited Bayes-compatible perspective construction with the separately specified radial term. Nothing here changes that radial term or warrants an actual epistemic interpretation.

Divergence contraction is not gradient-field projectability, commutation of arbitrary likelihood multiplication with K, preservation of every vertex score or absolute risk, recovery of individual sample outcomes, or recovery of reference/source provenance. Fixed-truth evidence garbling remains the broader Jensen theorem for every convex coherent potential in the inherited report; the present iff concerns changed truth coordinates with a transported reference.

All states and reference entries are strictly positive and dimensions finite. Boundary extensions, infinite spaces, nonseparable generators, approximate recovery, and a full classification of equality for concave but not strictly concave r remain outside this bounded result.

## 6. Primary ancestry and reading scope

- H. H. Bauschke and J. M. Borwein, *Joint and Separate Convexity of the Bregman Distance*, 2001, pp. 23–36. [Author-hosted manuscript](https://cmps-people.ok.ubc.ca/bauschke/Research/c04.ps), [author bibliography](https://cmps-people.ok.ubc.ca/bauschke/research.html), DOI 10.1016/S1570-579X(01)80004-5. Directly checked manuscript Lemma 3.2, Theorem 3.3 and its Hessian proof, and Remark 3.6 (manuscript pp. 4–5). These give precisely the reciprocal-curvature characterization and affine-reciprocal endpoint discussion. Attribution is explicit; our proof is included for the particular transport application.
- D. Chafaï, *Binomial-Poisson entropic inequalities and the M/M/∞ queue*, ESAIM Probability and Statistics 10 (2006), 317–339. [Author's arXiv manuscript, v2](https://arxiv.org/pdf/math/0510488), DOI 10.1051/ps:2006013. Directly checked §4, especially Theorem 4.4 statements 1 and 4 and their proof (manuscript pp. 19–22). Its AΦ(u,v)=Φ(u+v)−Φ(u)−Φ′(u)v becomes our bφ(x,y) under (u,v)=(y,x−y), an invertible linear change. Thus it supplies the Φ-entropy ancestry of the same convexity criterion. No theorem about the present three-object recovery converse is attributed to it.

The primary manuscripts were downloaded into sources and hashed. The Bauschke–Borwein manuscript is PostScript converted locally to PDF/text; text extraction drops some glyphs, so the key mathematical statement was also visually inspected. Only the specified portions, not entire works or all their cited ancestry, were used. Local inherited-report bytes and all retrieved source bytes are bound in SOURCE_LEDGER.json.

## 7. Verification and stopping boundary

verify.py checks the symbolic Hessian and determinant identity, normalized-probability embedding, t⁴ failure, interior-power radical gap, the equality/no-common-recovery witness, and exact endpoint equality separations. The controls supplement rather than replace the all-input proofs. verification.txt records executed checks. No formal proof-assistant certification or empirical validation is claimed.

The root supplied the initial candidate iff, normalized-buffer strategy, interior-power fixture, and displayed recovery witness. This worker independently derived the Hessian equivalence and strict-r equality argument, located and checked primary ancestry, and replayed fixtures. This is workflow attribution, not field priority. The inherited open frontier now has a precise family-level classification under its declared transport contract; the programme remains open.
