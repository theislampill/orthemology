# Independent review of fixed marginal KL correction

11 October 2026 UTC. Ordinary mathematical review for active T20. No audit-governor role, protected edit, integration, external peer-review claim, or closure authority.

## Finding and reviewed object

No blocking mathematical finding in the frozen author result, within its explicitly stated weak-solution, chain-rule, and positivity hypotheses. The author establishes the full tangent projection, a coercive weak multiplier problem, and a globally defined Gaussian solution. The stronger Gaussian entropy inequality supplied during this review is a participating extension, not independently certified by its originator.

Reviewed author RESULT.md SHA256:

    34f54d2c1ac994fc9212eb900e92d8bcb3898c7b4a00a6002c361b8752eee8e1

Reviewed author MANIFEST.json SHA256:

    493640bbeee1b5b929cf81b8d0a8772e7f451c2d090f0b1c37444b26b364ac87

REVIEW_BINDINGS.json records complete before-and-after author hashes, snapshot equality, author-manifest verification, and replay commands. The author packet is copied without modification. The separate independent checker imports no author/root checker code. Its 50 exact controls supplement the following ordinary proofs; neither their count nor their success proves general PDE well-posedness.

## Full tangent projection

Write Nμ=(ker Dμ)⊥ inside Hμ. Every represented density tangent has exactly one minimum field in Nμ, so the tangent Hilbert space is identified with Nμ. Let Qν be the orthogonal projection of coarse fields onto Nν. For a coisometric observation, C is conditional field pushforward and L=C* is the isometric horizontal lift, satisfying CL=I.

The correct marginal map on minimum fields is P=QνC restricted to Nμ. Raw C need not produce a minimum coarse representation. If k∈Nν and h∈ker Dμ, then Ch∈ker Dν and

    ⟨Lk,h⟩=⟨k,Ch⟩=0.

Thus L maps Nν into Nμ. For h∈Nμ and k∈Nν, ⟨QνCh,k⟩=⟨h,Lk⟩; consequently P*=L and PP*=I. The normal projection on Nμ is LQνC. Therefore the negative constrained gradient is

    −(I−LQνC)jμℓ.

When the coarse minimum field has potential φ, QνCjμℓ=jνφ, this becomes −jμ(ℓ−φ∘T), with Kνφ=T_*Kμℓ. The author proves the equivalent statement intrinsically in tangent space. This is genuine ambient minimality, rather than minimum cost among a stipulated ansatz or merely removal of a conditional mean.

The quadratic-plus-linear minimization in author §3 is correctly normalized. Its distinct prescribed-decrease minimum is d²/||Gc||², provided Gc≠0. A pure minimum-norm vertical problem would have the zero solution. None of these instantaneous statements establishes a shortest endpoint path.

## Weak multiplier and fixed marginal

For target ν⊗πZ, ℓ=log(r/πZ), differentiation under the conditional integral gives E[∇yℓ|Y]=0. Hence the coarse positive gradient is ν(h−νh), where h=E[ℓ|Y]. The multiplier equation is the weighted elliptic resolvent

    −ν⁻¹div(ν∇φ)+φ=h−νh,   νφ=0.

The author's Wν completion and positive smooth weight make the weighted gradient closable. Constants belong to Wν by cutoffs. The bilinear form ∫(∇φ·∇ψ+φψ)dν is the defining Hilbert norm and the right side is bounded because h−νh∈L²(ν). Riesz representation gives the unique weak solution; testing with 1 fixes its mean to zero. Testing with φ gives Bν(φ,φ)≤Varν(h). A spectral gap is unnecessary for this weak solve because the zeroth-order term already controls L².

This establishes an instantaneous weak vector field. It does not establish classical potential regularity, existence of the general nonlinear constrained PDE, or uniqueness among all full-law solutions. The author correctly preserves those distinctions. Along an admissible time-dependent solution, the distributional identity T_*μdot=0 fixes the entire marginal law. The arbitrary fixed-marginal case against πY⊗πZ retains the constant residual KL(ν||πY); it cannot be called convergence to the original target unless ν=πY.

## Gaussian derivation and global behavior

Let e=z−by, with Y~N(0,1), E~N(0,s) independent. The centered score and multiplier are

    ℓ−μℓ=b²(y²−1)/2+bye+(s−1)(e²−s)/(2s),
    φ=b²(y²−1)/6.

Spatial y differentiation holds z fixed, so ∂y=∂/∂y−b∂/∂e. The negative constrained fields are

    vy=−be/s+b²y/3,
    vz=−by−(1−1/s)e,
    α=−b²(y²−1)/3−bye−(s−1)(e²−s)/(2s).

Their pushed fields are b²y/3 and −b²(y²−1)/3. They are individually nonzero when b≠0, but their coarse transport and reaction cancel. Direct substitution into −div(ρv)/ρ+α gives

    ρdot/ρ=(b′/s)ye+(s′/(2s²))(e²−s),
    b′=−b(s+2+b²/3),
    s′=(1−s)(s+2)+2b².

This verifies the full Gaussian density derivative, rather than only its first two moments. The checker independently verifies that polynomial identity.

For b0∈R and s0>0, put m=min(s0,1), k=m+2, and M=max(s0,(-1+sqrt(9+8b0²))/2). On the first-exit interval, s≥m, b²≤b0² exp(−2kt), and the vector field points inward at s=M. Therefore the solution remains in a bounded region with s≥m>0. Local uniqueness for the polynomial ODE extends it to every finite forward time. This proves global existence for the constructed Gaussian solution, not general PDE uniqueness.

For w=s−1, the equation w′=−(s+2)w+2b² and variation of constants give

    |w(t)|≤(|w0|+2b0²/k) exp(−kt).

Thus b→0 and s→1, and the covariance converges to I. For b0≠0, integrability of w and b² gives a nonzero limit of exp(3t)b. Also exp(3t)w has a finite limit because its derivative is exp(3t)(−w²+2b²), an integrable function. The author's asymptotic KL exponent 6 follows. The separate closed-form fibrewise solution has correlation of order exp(−2t), hence KL exponent 4 for nonzero initial correlation. These exact-family rate claims are correctly distinguished from general path ordering.

## Dissipation and field restriction

Independent Gaussian integration gives, with E=(b²+s−1−log s)/2,

    Dc=(s−1)²(1/s+1/2)+b²(s+1+1/s)+b⁴/3,
    Df=(s−1)²(1/s+1/2)+b²(1+s),
    Du−Dc=b⁴/6,
    Dc−Df=b²/s+b⁴/3,
    E′=−Dc.

The first difference is the actual minimum coarse tangent norm, rather than the cost of a possibly nonminimal averaged representation. The second compares the ambient constrained gradient to the stricter field control vy=0 and E[α|Y]=0. Because that field-control space is a closed subspace of the marginal-preserving field space, the author's nested projection argument is valid. Restricted field action need not equal ambient tangent action.

The author's rational witness checks exactly. At b=1/2 and s=3/4, the fibrewise tangent covariance derivative is [[0,−7/8],[−7/8,−3/16]]. The stated symmetric Bf yields this entire tangent through −(BfΣ+ΣBf)−ΣBfΣ, with ambient minimum action 2489/7392. Its fibrewise field action is 53/96; their difference is 199/924. Potential-field duality establishes ambient minimality, beyond just the trace calculation.

At b=0,s=1 an additional simple review control gives the same lesson. The density tangent ρ B yz is represented by the full minimum fields

    (vy,vz,α)=(Bz/3,By/3,Byz/3),   action=B²/3,

and by the fibrewise minimum fields

    (vy,vz,α)=(0,By/2,Byz/2),       action=B²/2.

Each field is a gradient in its corresponding control space, so kernel orthogonality proves the indicated minimum property. The very same attainable density tangent has two different costs.

More generally every (b′,s′) in the Gaussian fixed-marginal family is attainable in either geometry. For the full constrained geometry its mobility in these coordinates is

    Mc=[[1+2s+b²/3, −2bs],
        [−2bs, 2s(s+2+2b²)]],

whereas the fibrewise mobility is Mf=diag(1+s,2s(s+2)). Mc is positive definite: its determinant is

    2s[2s²+5s+2+(7s+8)b²/3+2b⁴/3]>0.

The difference Mc−Mf is positive semidefinite, with first diagonal s+b²/3 and determinant 4sb⁴/3. Thus the full minimum tangent metric is no greater than the fibrewise metric on this shared two-dimensional tangent family. This does not assert equality of all distributional tangent ranges under arbitrary regularity assumptions.

## Conditional recentering is feasible but not optimal

Keeping v=−∇ℓ and replacing α by −(ℓ−E[ℓ|Y]) also preserves the fixed target marginal under the same score-integrability hypotheses: its averaged y velocity and averaged reaction are both zero. It is therefore incorrect to dismiss this operation as intrinsically infeasible. Its distinction from the projected gradient is optimality in the declared full tangent metric.

For the Gaussian family this reaction-only recentering gives

    b′n=−b(s+2),
    s′n=(1−s)(s+2)+2b²,
    Dn=Df+b²/s=Dc−b⁴/3.

The exact density tangent and KL chain rule are checked separately. The author's frozen report makes no contrary assertion; this clarification is an additional reviewer calculation.

One initial reviewer checker label incorrectly suggested infeasibility, although its actual equality only checked the difference of density tangents and passed. Before freezing this review, the label was corrected and explicit feasible-density and dissipation checks were added. The original script and its 39 passing controls remain under snapshots/. There was no failed algebraic assertion, no author edit, and no concealed reversal of a reviewed author claim.

## Participating entropy bound

The reviewer supplied, and the author then checked, the stronger inequality Dc≥6E. With

    R(s)=(s−1)²(1/s+1/2)−3(s−1−log s),

one has R(1)=0 and R′(s)=(s−1)³/s². Thus R has global minimum zero at 1. The exact decomposition is

    Dc−6E=R(s)+b²(s−1)²/s+b⁴/3≥0.

Consequently E(t)≤E(0)exp(−6t) for the global Gaussian solution. The constant 6 is sharp as a uniform Gaussian entropy-dissipation constant, since Dc/E→6 along s=1,b→0. This is a constructive extension from this reviewer and receives no claim of independent certification by the same reviewer. Its author-side algebraic replay and the transparent proof support it.

## Ancestry and boundaries

Focused primary-source checks confirm the author's attribution. Alvarez, Bolte and Brahic §2.2 equations (7)–(10) explicitly gives metric-projected gradients under affine constraints. [Primary paper](https://arxiv.org/pdf/1811.10331).

Kondratyev and Vorotnikov Remark 1.1 and Definitions 3.14–3.15 give the centered gradient and unit transport/reaction action. Their displayed dynamic definition uses a torus; their additional PDE hypotheses have not been imported here. [Primary paper](https://arxiv.org/html/1809.03430v2).

Liero, Mielke, Tse and Zhu §3.4, Theorem 3.11, equations (3.8a,b), give the established normalized Gaussian SHK KL flow. [Primary paper](https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf).

This is a bounded review of the displayed result and its dependencies, not an exhaustive priority search. No novelty is assigned to constrained gradients, conditional KL, Gaussian invariance, or SHK. No empirical warrant or philosophical identification follows from the stipulated mathematical targets. No general PDE existence or uniqueness, universal all-laws manifold, globally least-action endpoint path, or T20 closure has been established.
