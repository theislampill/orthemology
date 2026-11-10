# Common repair and the geometry of coherent forecasts

## Status and scope

This chapter is a mathematical exposition of public Orthemology research on repairing an incoherent forecast when several scoring standards remain admissible. It consolidates proofs, corrections and counterexamples; it does not amend an accepted paper, assert new priority for classical results, or confer scientific acceptance on an application. The mathematical object is a finite truth hull with specified losses. Claims about epistemic authority or human cognitive implementation require additional premises.

The central question is whether **one coherent forecast improves on the same disturbed forecast under every specified standard and every admissible truth**. For quadratic losses, agreement of weighted projections answers the question exactly. For smooth additive losses, this local geometry yields strong rigidity on dependency blocks of rank at least two. Rank-one blocks admit a larger class governed by comparison of generalized means. At the boundary, first-order agreement need not yield exact repair, a zero second-order margin does not decide feasibility, and even the complete Taylor data at one point can fail to determine the answer. A further counterexample holds the entire score functions fixed: changing only the admissible joint truth hull changes repair from possible to impossible.

All necessary arguments and concrete counterexamples are given below. Historical formal sources are identified at the end as inspectable verification dependencies; reading this chapter does not require executing them.

## 1. The common-repair problem

### 1.1 Truth, coherence and a shared decision

Let $`v_1,\ldots,v_m`$ be a nonempty finite list in $`\mathbb R^n`$, and put

```math
C=\mathrm{conv}\{v_1,\ldots,v_m\},\qquad
p\in\mathrm{ri}C,\qquad
T=\mathrm{span}(C-p).
```

Here relative interior is taken in the affine hull of $`C`$. The vectors $`v_j`$ need not be affinely independent, and repeated entries are allowed. A coherent forecast belongs to $`C`$. We examine

```math
b_\varepsilon=p+\varepsilon h,\qquad \varepsilon>0,
```

where the direction $`h\notin T`$ is transverse and the forecast remains in the domain of every loss for sufficiently small $`\varepsilon`$. Transversality makes $`b_\varepsilon`$ incoherent. A **common weak repair** is one $`c\in C`$ satisfying

```math
L_k(c,v_j)\leq L_k(b_\varepsilon,v_j)
\quad\text{for every }k,j.
```

A common strict repair makes every inequality strict. An $`\eta`$-repair replaces the right side by $`L_k(b_\varepsilon,v_j)+\eta`$, where $`\eta\geq0`$ is measured in the fixed units of the losses. The repair may depend on $`p,h,\varepsilon`$ and the family of standards, but it cannot depend on the unknown truth or on which standard will eventually be used.

There are two different local quantifiers. Existence along a sequence $`\varepsilon_\nu\downarrow0`$ is a weak requirement useful in necessity arguments. Existence for every sufficiently small positive $`\varepsilon`$ is a stronger conclusion. We state the distinction whenever it matters.

### 1.2 Positive barycentric weights

Every $`p\in\mathrm{ri}C`$ admits

```math
p=\sum_{j=1}^m\lambda_jv_j,\qquad
\lambda_j>0,\qquad \sum_j\lambda_j=1.
\quad\text{(1)}\quad
```

To prove this for the entire listed population, let $`\bar v=m^{-1}\sum_jv_j`$. Relative interior permits a point $`y=p+t(p-\bar v)\in C`$ for some $`t>0`$. Express $`y=\sum_j a_jv_j`$ with $`a_j\geq0`$ and $`\sum_j a_j=1`$. Then

```math
p=\frac{t}{1+t}\bar v+\frac1{1+t}y
  =\sum_j\left(\frac{t}{m(1+t)}+\frac{a_j}{1+t}\right)v_j.
```

Every displayed weight is positive. In particular, if numbers $`q_j\geq0`$ have $`\sum_j\lambda_jq_j=0`$, each $`q_j`$ is zero. Several rigidity proofs below depend on this implication; replacing relative interior by an arbitrary boundary point would lose it.

**Two interior conditions.** Relative interior in this argument is intrinsic to the affine hull. It supplies positive weights even when listed truths coincide; a duplicate contributes another positive weight without increasing the tangent rank. It does not imply interiority in each ambient coordinate. For example, the singleton hull $`\{0\}`$ has relative interior $`\{0\}`$, while its coordinate is on the boundary of $`[0,1]`$. The smooth results below separately exclude constant coordinates when they need derivatives on $`(0,1)`$. Counting encoded coordinates or repeated truth rows cannot replace that hypothesis. [finite-hull-review], [hull-interface-review]

### 1.3 Bregman losses and two identities

For a differentiable strictly convex potential $`F`$, use the truth-first Bregman convention

```math
D_F(v,b)=F(v)-F(b)-\nabla F(b)\cdot(v-b),
\qquad L_F(b,v)=D_F(v,b).
\quad\text{(2)}\quad
```

Thus the forecast is the second argument. Affine additions to $`F`$ do not change $`D_F`$; multiplying $`F`$ by a positive constant multiplies the loss.

The score difference between two forecasts is affine in $`v`$. Consequently inequalities verified at every listed truth extend to every $`v\in C`$, and averaging with (1) gives

```math
\sum_j\lambda_j\bigl(D_F(v_j,c)-D_F(v_j,b)\bigr)
 =D_F(p,c)-D_F(p,b).
\quad\text{(3)}\quad
```

A direct expansion also gives the three-point identity

```math
D_F(v,b)-D_F(v,c)
=D_F(c,b)+
 \bigl(\nabla F(c)-\nabla F(b)\bigr)\cdot(v-c).
\quad\text{(4)}\quad
```

These identities separate two optimization problems that should not be confused. To construct a coherent projection, minimize $`c\mapsto D_F(c,b)`$, with the candidate in the first argument. This is a strictly convex function of $`c`$. The truth-indexed forecast loss $`c\mapsto D_F(v,c)`$ need not be convex.

A positive-mass example makes the projection qualification concrete. For b=(x,y), m=x+y>0 and F(b)=(x²+y²)/(2m)+m²/2, write b=s(p,1−p) and c=t(q,1−q), with s,t>0 and 0<p,q<1. The displayed symbolic control gives D_F(b,c)=s(p−q)²+(s−t)²/2. In the truth-first convention, every simplex vertex has the same gain (s−1)²/2 when the forecast s(p,1−p) is replaced by its normalization. The Hessian identities H(b)b/m=(1,1), det H=2/m and H₁₁=1+2y²/m³ exhibit the radial mechanism and positive curvature in this two-coordinate example. They are not consequences of arbitrary strict convexity: replacing m²/2 by (m−1)⁴ leaves a singular radial Hessian at mass one while retaining tangent curvature. Euclidean projection of (3/5,7/10) instead subtracts 3/20 from both coordinates and differs from normalization. The positive-part perturbation [x+y/2−1]₊⁴ additionally vanishes on the simplex and its contracted positive rays but changes forward-projection stationarity at (9/10,4/5). Thus a restricted neutrality condition cannot silently become a global normalization theorem. These are identities and countercontrols specified by the exact unexecuted symbolic body; its referenced general analysis was not received. [A1634-F25-225](../research/t20-v6-20261012/sources/6085bc0f9452312e51c833559792158599ba899d792631030f37da4001126768/independent_controls.py#L19-L53) [A1634-F25-225](../research/t20-v6-20261012/sources/6085bc0f9452312e51c833559792158599ba899d792631030f37da4001126768/independent_controls.py#L55-L83)

Repeated all-truth repair need not preserve calibration to an earlier law. For F(x₁,x₂)=x₁ log x₁+2x₂ log x₂, with 0 log 0 interpreted as zero, set p=(1/2,1/2), tₖ=k log 2 and qₖ=(1−uₖ,uₖ), where uₖ=2/[1+√(1+8·2ᵏ)]. The displayed formula gives ∇F(qₖ)−∇F(p/2ᵏ)=λₖ(1,1). Subtracting consecutive identities shows that qₖ is the strictly convex forward projection of qₖ₋₁/2 onto the simplex. The three-point identity therefore gives the same positive gain D_F(qₖ,qₖ₋₁/2) at either categorical truth for k≥1. Yet qₖ moves away from p: D_F(p,qₖ)=−½ log[2(1−uₖ)]−log(2uₖ)−½+uₖ, which increases as uₖ decreases below 1/2. Its expected truth loss under p exceeds the baseline by exactly this divergence. There is no contradiction: each repair is compared with a newly contracted forecast, not with the preceding coherent forecast. These consequences follow from the displayed formulas and the three-point identity. The selected program only requests 100-digit numerical comparisons at 129 finite steps, including a finite asymptote approximation; it was not run and supplies no certified numerical error bound or empirical calibration result. [AFTER1884-T25-054](../research/t20-v6-20261012/sources/6a9ab36a3527b01a584c541a56c33a9f178708345159b7de2a23e932f39c5162/verify.py#L6-L38)

The entropy perspective supplies another exact positive-cone example. For x=s p and y=t q with s,t>0 and interior binary laws p,q, let F(x)=cΣᵢxᵢ log(xᵢ/s)+s²/2, c>0. Its forward divergence is D_F(x,y)=cs KL(p‖q)+(s−t)²/2, with the first argument’s mass s multiplying the normalized divergence. Its Hessian is c diag(1/xᵢ)+(1−c/s)11ᵀ; the generally nonzero mixed entry shows that this perspective need not be coordinate-additive. Replacing the quadratic radial term by a(s) instead adds D_a(s,t), which vanishes on every normalized pair. Hence normalized-only comparisons cannot determine radial shape across dimensions. For a₂(s)=s²/2 and a₃(s)=s³/3, the radial divergences at (s,t)=(2,1) differ by 5/6 even though both vanish at (1,1). Affine changes to a leave its divergence unchanged, and strict convexity of (s−1)⁴ does not make its second derivative positive at s=1. These symbolic identities concern the displayed generators and positive domains, not a proof of a universal channel-natural classification; the exact-control program was read rather than executed. [AFTER1884-X25-145](../research/t20-v6-20261012/sources/762951edadc75cde5c578191ef6ba0365e59f67405b6006ea82ad2d4b231ee91/independent_controls.py#L65-L96)

The unequal-weight entropy diagnostic admits a finite-dimensional curvature explanation beyond a binary example. For positive probabilities pᵢ and positive weights aᵢ, define qᵢ(t)=pᵢ exp(−t+λ(t)/aᵢ), with λ chosen so that Σqᵢ=1, and put μₚ=Σaᵢpᵢ, μq=Σaᵢqᵢ and Hq=(Σqᵢ/aᵢ)⁻¹. The normalizing equation is strictly increasing in λ with range (0,∞), so it determines a smooth λ and differentiation gives λ′=Hq. For F(x)=Σaᵢxᵢ log xᵢ, D_F(p,q(t))=tμₚ−λ−μₚ+μq. Since μq′=Hq−μq, the divergence has derivative μₚ−μq and second derivative μq−Hq=Hq Σᵢ<ⱼ qᵢqⱼ(aᵢ−aⱼ)²/(aᵢaⱼ). Thus it is strictly convex along finite t when the weights are not all equal, although its initial derivative is zero; equal weights give q(t)=p. The displayed diagnostic uses the positive pairwise formula to avoid cancellation, but computes λ by floating-point bisection and checks only three fixed laws over 301 times each plus eighty binary comparisons. The identities explain the diagnostic; its tolerances and asserted asymptotic comparisons are not certified error bounds, an observed run, or an empirical calibration theorem. [AFTER1884-E25-185](../research/t20-v6-20261012/sources/7a36ed15d110d66db4878d41fecc0805c53e05438e2f149c7d868b0b5af61cba/independent_diagnostics.py#L5-L26) [AFTER1884-E25-185](../research/t20-v6-20261012/sources/7a36ed15d110d66db4878d41fecc0805c53e05438e2f149c7d868b0b5af61cba/independent_diagnostics.py#L28-L55)

For coordinate-separable generators the likelihood-implementation question has a sharper classification. Let n≥2, F(b)=Σ_if_i(b_i), with f_i finite and continuous on[0,1], C² and f_i″>0 on(0,1), and, for strictly positive b∈(0,1)^n, let P_F minimize D_F(p,b) over the closed simplex. On these inputs with the strict subprobability condition Σ_i b_i<1, the minimizer is interior and exceeds the input in every coordinate: otherwise transferring a little mass from an above-input coordinate to a deficient one lowers the strictly convex objective. Even the restricted condition P_F(L⊙P_F(b))=P_F(L⊙b), for every b∈(0,1)^n with Σ_i b_i<1 and every positive likelihood vector L with L_k=a∈(0,1) at one coordinate and L_i=1 elsewhere, holds exactly when f_i″(t)=α_i/t with independently positive α_i. Indeed varying b along a common dual-gradient shift leaves its projection fixed; differentiating the projected KKT differences after attenuation gives a f_i″(ax)=f_i″(x). Conversely the weighted-entropy formula P_F(b)_i=b_i exp(λ/α_i) makes the shifts compose. Scalar neutrality P_F(cb)=P_F(b), 0<c≤1, is stronger: scaling to the simplex forces P_F(b)=b/Σb_i, and differentiating the KKT pair differences forces one common α across coordinates. Even neutrality only on contracted coherent priors suffices in this separable class, including n=2. This is a classification of multiplying likelihood weights and then using this projection, not a restriction on which proper score may evaluate an independently computed Bayesian posterior. The nonseparable perspective examples above lie outside its hypotheses. [AFTER3384-FIRST25-020](../research/t20-v6-20261012/sources/06351f384910bb9984c75712bea3b483201fad575a0ac8da258406b5f56d7f69/RESULT.md#L31-L152)

The evidential account also separates three quantities. For an independently justified finite prior p, channel outcome probabilities m_y, interior Bayesian posteriors Q_y and interior implemented reports q_y, write R_F(r,s)=Σ_jr_jD_F(e_j,s). The identities R_F(r,s)=R_F(r,r)+D_F(r,s) and Σ_ym_yQ_y=p give R_F(p,p)−Σ_ym_yR_F(Q_y,q_y)=Σ_ym_yD_F(Q_y,p)−Σ_ym_yD_F(Q_y,q_y). The first term is model-relative information gain; the second is implementation regret. If p=P_F(b) is additionally the justified prior and the projection is interior, comparison with raw b adds the separate coherence credit D_F(p,b). Thus uniform improvement over a raw weighted vector does not establish evidence gain over the prior. Ordinary normalization removes implementation regret for the stipulated Bayes channel but cannot validate that channel or make copied evidence independent; source provenance and actual warrant remain separate. [AFTER3384-FIRST25-020](../research/t20-v6-20261012/sources/06351f384910bb9984c75712bea3b483201fad575a0ac8da258406b5f56d7f69/RESULT.md#L176-L204) [AFTER3384-FIRST25-020](../research/t20-v6-20261012/sources/06351f384910bb9984c75712bea3b483201fad575a0ac8da258406b5f56d7f69/RESULT.md#L206-L224)

If $`F`$ is $`C^3`$ near $`p`$, write $`H_F=\nabla^2F(p)`$ and $`K_F=\nabla^3F(p)`$. Differentiation in the forecast gives

```math
\nabla_bD_F(v,b)=\nabla^2F(b)(b-v),
\qquad
D_b^2D_F(v,p)[u,u]
=H_F[u,u]+K_F[p-v,u,u].
\quad\text{(5)}\quad
```

The divergence and projection framework originates with Bregman [1]. The results below concern simultaneous repair under several standards, rather than priority for that framework.

The retained SmoothRigidity body uses a different argument convention locally: bregman F G v b is defined as F(b)−F(v)−G(v)(b−v), but bregman_gain uses the forecast-gradient difference G(c)−G(b), and totalDiv_eq_sum identifies it with the truth-first scalar divergence. Those displayed equations cannot simply be transferred through that definition. Equations (2)–(5) above retain the correct truth-first convention; the discrepancy is in this source body, not in those identities. [Exact retained source](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/15b7bbe674ea84ca5d397afe1991b34e35a1da870f6870ba2cc31b7398b48316/SmoothRigidity.lean)

## 2. Quadratic repair: exact compatibility and quantitative separation

### 2.1 A directionwise equivalence

Let $`\mathcal W`$ be any nonempty family of positive-definite symmetric matrices, including an infinite family, and define

```math
L_W(b,v)=\|b-v\|_W^2=(b-v)^\top W(b-v).
```

Let $`P_W`$ be the $`W`$-orthogonal projection onto $`T`$, and let $`Q_W=I-P_W`$.

**Theorem 1 — Exact quadratic common repair.** For fixed $`p\in\mathrm{ri}C`$ and $`h\notin T`$, the following are equivalent:

1. There are $`\varepsilon_\nu\downarrow0`$ and common weak repairs $`c_\nu\in C`$.
2. The vector $`P_Wh`$ is the same for every $`W\in\mathcal W`$.
3. For some $`z\in T`$, the single rule $`c_\varepsilon=p+\varepsilon z`$ is a common strict repair for every sufficiently small positive $`\varepsilon`$.

If these conditions hold, $`z=P_Wh`$ and

```math
L_W(b_\varepsilon,v)-L_W(c_\varepsilon,v)
=\varepsilon^2\|Q_Wh\|_W^2>0
\quad(v\in C).
\quad\text{(6)}\quad
```

**Proof.** Fix one matrix $`W_0`$. Averaging the weak-repair inequalities yields

```math
\|c_\nu-p\|_{W_0}^2
\leq \varepsilon_\nu^2\|h\|_{W_0}^2.
```

Hence $`z_\nu=(c_\nu-p)/\varepsilon_\nu`$ is bounded in $`T`$. Pass to a subsequence with $`z_\nu\to z\in T`$. For each fixed $`W`$ and each listed truth, expand the gain and divide by $`\varepsilon_\nu`$. The limit is

```math
2(p-v_j)^\top W(h-z)\geq0.
```

Its strictly positive barycentric average is zero, so every term is zero. The vectors $`p-v_j`$ span $`T`$, whence $`h-z`$ is $`W`$-orthogonal to $`T`$, and $`z=P_Wh`$. The same convergent subsequence works for every fixed $`W`$; no extraction over the possibly infinite family is required.

Conversely, if the projected vector is common, relative interior makes $`p+\varepsilon z\in C`$ for all sufficiently small $`\varepsilon`$. Its difference from $`b_\varepsilon`$ is $`W`$-normal to $`T`$. Pythagorean expansion proves (6). Since $`h\notin T`$, the normal vector is nonzero. The implication from strict to weak repair is immediate. $`\square`$

There is no asserted uniform positive gain over an infinite family of matrices. The common feasible scale is geometric, but the positive numbers $`\|Q_Wh\|_W^2`$ may have infimum zero.

The feasible scale is also directionwise. With $`p`$ and the common projected direction $`z`$ fixed, a relative ball around $`p`$ contains $`p+\varepsilon z`$ for sufficiently small $`\varepsilon`$. No positive radius works uniformly over an unbounded collection of directions: already on a nondegenerate interval, scaling a nonzero tangent direction eventually takes its endpoint outside the interval at any fixed positive $`\varepsilon`$. The theorem quantifies over each fixed direction before choosing its scale. [root-cold-review]

Universal directionwise repair is equivalent to equality of the projection operators. All projections already agree on $`T`$, so it is enough to compare their action on directions spanning $`\mathbb R^n/T`$. This is a sufficient finite test set, not a theorem that a particular query count is minimal.

### 2.2 The simplex reveals relative weights

For the categorical simplex $`C=\{x\geq0:\sum_i x_i=1\}`$, its tangent is $`T=\{u:\sum_i u_i=0\}`$. If $`W=\mathrm{diag}(w_1,\ldots,w_n)`$, then

```math
P_Wh=h-\left(\sum_i h_i\right)r_W,\qquad
(r_W)_i=\frac{w_i^{-1}}{\sum_jw_j^{-1}}.
\quad\text{(7)}\quad
```

Thus one transverse direction already identifies the relative diagonal weights: common repair for that direction requires the same normalized reciprocal vector, equivalently proportional weight vectors.

A symmetry conclusion needs an explicit premise about one fixed decision problem. Suppose a normalized candidate class of weights is closed under a permutation group, and one repair must work for every member of that class. Theorem 1 forces the class to be a singleton, so the surviving weights are constant on each group orbit; a transitive group forces equal weights. Merely relabelling the entire problem covariantly does not provide the premise that one fixed output must accommodate all the relabelled standards.

### 2.3 A finite-scale error bound

Choose $`r>0`$ with the Euclidean tangent ball $`B_T(p,r)\subset C`$. Let

```math
m_W=\lambda_{\min}(W),\qquad q_W=\|Q_Wh\|_W^2,
\qquad x_W=p+\varepsilon P_Wh.
```

If $`\varepsilon\|P_Wh\|_2\leq r/2`$, every all-state $`\eta`$-repair obeys

```math
\|c-x_W\|_2\leq
\frac{\varepsilon^2q_W+\eta}{r\,m_W}.
\quad\text{(8)}\quad
```

Indeed, put $`d=c-x_W`$. If $`d\ne0`$, the truth point

```math
v=x_W-\rho\,\frac d{\|d\|_W},
\qquad \rho=\frac r2\sqrt{m_W},
```

belongs to $`C`$. By (6), its repair gain is
$`\varepsilon^2q_W-2\rho\|d\|_W-\|d\|_W^2`$.
The $`\eta`$-condition bounds the two nonnegative subtracted terms by $`\varepsilon^2q_W+\eta`$, proving (8).

For two matrices $`W,Z`$, let $`d_0=\|P_Wh-P_Zh\|_2`$. Applying (8) twice gives

```math
\varepsilon d_0\leq\varepsilon^2A+\eta B,
\quad
A=\frac1r\left(\frac{q_W}{m_W}+\frac{q_Z}{m_Z}\right),
\quad
B=\frac1r\left(\frac1{m_W}+\frac1{m_Z}\right).
\quad\text{(9)}\quad
```

Therefore an error allowance $`\eta=o(\varepsilon)`$ still forces exact projection compatibility. Errors of order $`\varepsilon`$ can conceal disagreement.

Randomization independent of truth and standard does not circumvent the quadratic result if the requirement is expected loss. If a random repair $`X`$ lies in $`C`$, its mean lies in $`C`$, and
$`L_W(\mathbb EX,v)\leq\mathbb EL_W(X,v)`$.
The mean is consequently a deterministic repair whenever the randomized rule is one.

### 2.4 Exact binary repair cells and the information they encode

Take $`p=(1/2,1/2)`$, $`b_\varepsilon=(1/2+\varepsilon,1/2)`$, $`0<\varepsilon\leq1/4`$, and $`W_\alpha=\mathrm{diag}(\alpha,1-\alpha)`$ with $`0<\alpha<1`$. Write a coherent candidate as $`(t,1-t)`$. The exact $`\eta`$-repair cell is

```math
\left[
1-\sqrt{\frac14-\alpha\varepsilon+\alpha\varepsilon^2+\eta},
\quad
\sqrt{\frac14+\alpha\varepsilon+\alpha\varepsilon^2+\eta}
\right]\cap[0,1].
\quad\text{(10)}\quad
```

The quadratic projection is $`t_\alpha=1/2+\alpha\varepsilon`$, with gain $`D_\alpha=\alpha(1-\alpha)\varepsilon^2`$. Directly from the two endpoint inequalities,

```math
|t-t_\alpha|\leq2(D_\alpha+\eta)
\leq\frac{\varepsilon^2}{2}+2\eta.
\quad\text{(11)}\quad
```

For example, when $`t-t_\alpha\geq0`$, the loss increase at the zero endpoint is at least $`2t_\alpha(t-t_\alpha)`$; the opposite sign is controlled by the other endpoint. The weaker common bound uses $`t_\alpha,1-t_\alpha\geq1/4`$.

If $`\alpha`$ ranges over $`[a,b]\subset(0,1)`$, the common cell has the endpoints in (10) with $`\alpha=b`$ in the lower bound and $`\alpha=a`$ in the upper bound. Put

```math
A=\frac14-b\varepsilon+b\varepsilon^2+\eta,\qquad
B=\frac14+a\varepsilon+a\varepsilon^2+\eta.
```

It is nonempty exactly when $`\sqrt A+\sqrt B\geq1`$. For $`A,B\geq0`$, this is equivalent to
$`A+B\geq1`$ or $`4AB\geq(1-A-B)^2`$.
For $`\eta=0`$, write $`m=(a+b)/2`$ and $`d=b-a`$. In the branch $`A+B<1`$, the same condition is

```math
d^2\varepsilon^3-4d\varepsilon^2m+2d
 +4\varepsilon m^2-4\varepsilon m\leq0.
\quad\text{(12)}\quad
```

In a compact subinterval of $`0<m<1`$, the limiting admissible width is
$`d\leq2m(1-m)\varepsilon+O(\varepsilon^3)`$.

Every exact repair supplies the estimate
$`\widehat\alpha=(t-1/2)/\varepsilon`$ with
$`|\widehat\alpha-\alpha|\leq\varepsilon/2`$; with tolerance, the bound becomes
$`\varepsilon/2+2\eta/\varepsilon`$.
Consequently exact repair cells of parameters separated by more than $`\varepsilon`$ are disjoint. If a deterministic observation with $`N`$ possible outputs supports exact repair throughout $`[a,b]`$, each observation class has diameter at most $`\varepsilon`$, so
$`N\varepsilon\geq b-a`$.
A packing of $`M`$ pairwise separated parameters requires $`M`$ distinct observation classes, hence at least $`\lceil\log_2M\rceil`$ bits in a fixed-length binary encoding. A zero-error randomized output cannot assign positive probability to an output incompatible with the true parameter.

These are operational distinguishability statements. They do not establish that a repairer consciously represents the estimate, or that geometric identifiability makes a scoring standard normatively authoritative.

The exact binary helper extends the cell calculation to any b=(b₁,b₂) in [0,1]² and any weight interval [a,c]⊂(0,1). Let m₁ be the minimum of the two endpoint-weight losses of b at truth (1,0), and m₀ the corresponding minimum at (0,1). Loss is affine in the weight, so these endpoint minima are the minima over the whole interval. A coherent forecast (t,1−t) has losses (1−t)² and t² independently of the weight. Consequently a weak common repair exists exactly when √m₁+√m₀≥1, and a strictly improving common repair exactly when that sum is greater than one. Writing S=m₁+m₀, S>1 ensures the strict condition; at S=1 strictness requires m₁m₀>0 while weak repair always exists; at S<1 the conditions are respectively 4m₁m₀>(1−S)² and ≥. This derives the helper's separate equality branch without a floating-point square-root comparison. It is a finite two-truth weighted-quadratic criterion, not a general scoring-rule result or warrant for the authority of a selected weight; its assertions were not executed. [AFTER2134-S25-043](../research/t20-v6-20261012/sources/8854ac9ff8e110d19b90fed9c0c9d4ab1cb84db5fec8c8bebe35af2ca28d5d8b/accuracy_checks.py#L9-L29)

## 3. Dependency blocks and diagonal rigidity

An elementary vector of $`T`$ is a nonzero $`u\in T`$ whose support contains no strictly smaller support of a nonzero vector in $`T`$. Join two coordinates when they occur in the support of one elementary vector, and take the connected components $`B`$ of this graph, including isolated coordinates. Set

```math
T_B=T\cap\mathbb R^B.
```

The elementary vectors span $`T`$. To see this, if a vector is not elementary, choose a nonzero vector with smaller support and subtract a suitable multiple to cancel one nonzero coordinate. Both resulting vectors have strictly smaller support, and induction applies. The elementary supports therefore give

```math
T=\bigoplus_B T_B.
\quad\text{(13)}\quad
```

This is coordinate dependence in the affine truth structure. It is not probabilistic independence.

**Theorem 2 — Diagonal metrics agree exactly blockwise.** For positive diagonal matrices $`W=\mathrm{diag}(w_i)`$ and $`Z=\mathrm{diag}(z_i)`$, the following are equivalent:

1. $`P_W=P_Z`$.
2. $`D=\mathrm{diag}(z_i/w_i)`$ preserves $`T`$.
3. The ratio $`z_i/w_i`$ is constant on each dependency block.

**Proof.** The kernel of $`P_W`$ is $`W^{-1}T^\perp`$. Equality of the kernels is equivalent to $`D T^\perp=T^\perp`$. Since $`D`$ is symmetric and invertible, this is equivalent to $`DT=T`$.

Suppose $`D`$ preserves $`T`$, and let $`u`$ be elementary. The spectral projection onto each eigenspace of $`D`$ is a polynomial in $`D`$, by finite Lagrange interpolation on its distinct eigenvalues. It preserves $`T`$. If the support of $`u`$ met two eigenspaces, one nonzero projection would give a vector of strictly smaller support in $`T`$, a contradiction. Thus the diagonal entries of $`D`$ agree on every elementary support and hence on each connected block. Conversely, blockwise constancy makes every elementary vector an eigenvector. Their span is invariant. $`\square`$

The elementary-vector method has classical antecedents in Rockafellar [2]. The diagonal stabilizer statement is the positive-real form of the matroid-component description in Denham, Proposition 2.12 [3]. If a matrix has row space $`T`$, the minimal supports used here are cocircuits of its column matroid, equivalently circuits of the dual; a circuit/cocircuit reversal would misidentify the stated representation, although the component partition is unchanged by duality.

Singleton blocks require care. A singleton can be free, with $`e_i\in T`$, or constant, with $`u_i=0`$ for all $`u\in T`$. Both allow arbitrary diagonal scaling at the purely quadratic level. The smooth theorem below excludes constant coordinates and states separately what happens on free ones. If $`T=\mathbb R^n`$, there is no transverse incoherence to repair; if $`T=\{0\}`$, the coherent hull is a singleton and all projections vanish.

## 4. Smooth additive rigidity on higher-rank blocks

### 4.1 Hessian agreement is a necessary local condition

Assume first that

```math
F(x)=\sum_i f_i(x_i),\qquad G(x)=\sum_i g_i(x_i),
\quad\text{(14)}\quad
```

where the scalar functions are finite and continuous on $`[0,1]`$, are $`C^2`$ on $`(0,1)`$, and satisfy $`f_i'',g_i''>0`$ there. Truth vectors lie in $`[0,1]^n`$, and every coordinate varies on $`C`$, so every $`p\in\mathrm{ri}C`$ has coordinates in $`(0,1)`$.

The retained SmoothScalar body also weakens a premise that its later declarations consume: Score.positive states 0≤ddf(x), whereas the strict monotonicity arguments and local_curvature_sandwich use it as 0<ddf(x). Zero curvature satisfies the displayed field but cannot supply a positive local quadratic lower bound. The strict-curvature assumption above is therefore not replaceable by that source's nonnegative field. [Exact retained source](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/1600f5abe4ff749aebaf21f543ceaa5e997ed2da43c1ab122aaaf1e69b93e277/SmoothScalar.lean)

Suppose a common weak repair exists along $`\varepsilon_\nu\downarrow0`$. Equation (3) gives
$`D_F(p,c_\nu)\leq D_F(p,b_{\varepsilon_\nu})=O(\varepsilon_\nu^2)`$.
This forces $`c_\nu\to p`$, even when the derivatives of $`f_i`$ diverge at endpoints. For a scalar coordinate,

```math
D_f(p_i,x)=\int_x^{p_i}(p_i-u)f''(u)\,du.
\quad\text{(15)}\quad
```

The integral is positive away from $`x=p_i`$, and on any fixed interval around $`p_i`$ it is bounded below by a positive quadratic. Leaving that interval cannot make it tend to zero. After localization, (15) yields $`c_\nu-p=O(\varepsilon_\nu)`$. The first-order expansion and positive barycentric averaging used in Theorem 1 then show

```math
P_{H_F(p)}h=P_{H_G(p)}h.
\quad\text{(16)}\quad
```

Here and below a boundary candidate for which a forecast loss is undefined or infinite is not an admissible finite-loss repair.

The same conclusion holds for common $`\eta_\nu`$-repairs with $`\eta_\nu=o(\varepsilon_\nu)`$, but averaging alone is insufficient: it would give only a square-root bound in $`\eta_\nu`$. The all-state inequalities supply the missing control. Choose $`B_T(p,r)\subset C`$, put $`\xi=c-p`$, and $`u=\nabla F(c)-\nabla F(b_\varepsilon)`$. By affinity in truth, comparison at all $`p+t`$, $`\|t\|_2\leq r`$, gives

```math
r\|P_Tu\|_2
\leq D_F(p,b_\varepsilon)+\eta-D_F(p,c)
\leq O(\varepsilon^2)+\eta.
\quad\text{(17)}\quad
```

After $`c\to p`$, expand
$`u=H_F(p)\xi-\varepsilon H_F(p)h+o(\|\xi\|)+o(\varepsilon)`$.
The operator $`P_TH_F(p)`$ restricted to $`T`$ is positive definite. Absorbing the small remainder in (17) yields
$`\xi=O(\varepsilon+\eta)=O(\varepsilon)`$.
Divide the original inequalities by $`\varepsilon`$ and apply (1) to recover (16).

There is an equivalent finite-state proof of the needed linear bound that makes the assumptions especially visible. For $`H=H_F(p)`$ and $`\xi\in T`$, put


```math
\Phi(\xi)=\sum_j\max\{(p-v_j)^\top H\xi,0\}.
```


If $`\Phi(\xi)=0`$, every displayed derivative is nonpositive. Its positive barycentric average is zero, so all are zero. Since the vectors $`p-v_j`$ span $`T`$, this implies $`\xi^\top H\xi=0`$ and hence $`\xi=0`$. When $`T\ne\{0\}`$, compactness of its unit sphere gives a constant $`\kappa>0`$ with $`\Phi(\xi)\ge\kappa\|\xi\|`$. For $`T=\{0\}`$ the displacement is already zero.

After the preceding localization, the finitely many differentiable loss comparisons have remainders bounded by $`\delta\|\xi\|+o(\varepsilon)`$, with $`\delta`$ as small as required. The approximate inequalities therefore give


```math
\kappa\|\xi\|
 \le C\varepsilon+m\eta+m\delta\|\xi\|+o(\varepsilon).
```


Choose $`m\delta<\kappa/2`$ and absorb that term. This proves $`\|\xi\|=O(\varepsilon+\eta)`$ directly from the complete collection of truth-state inequalities. It explains why a bound on average regret, or on a single truth state, cannot replace the argument. [smooth-robustness-review]

The retained finite-hull extension keeps truth indices J distinct from coordinate indices ι and uses a strictly positive barycentric presentation of p, not a literal intrinsic-interior argument. Repairs must remain in the actual truth hull and open cube; ε>0 tends to zero, η≥0 and η/ε tends to zero. One supplied anchor score gives the displacement bound, after which a single subsequential tangent limit is tested against every fixed score in an arbitrary family. Its displayed bound proof, however, sets N=|ι| while obtaining positivity from |J| and summing the statewise estimates over J. No equality of those cardinalities is assumed, so neither that positivity step nor replacing the constant-sum factor |J| by N is justified. The zero-tolerance specialization and later common-Hessian conclusion depend on that unresolved step. This exact source therefore does not newly verify the ordinary finite-hull argument above; it also supplies no diagonal-stabilizer or matroid theorem. [SUB250-R17-062](../research/t20-v6-20261012/sources/59da81856bc4f5f80d986d7d20ac906eb4ddedcc32e2a971fab4c7aca2a85500/FiniteHullSmoothRigidity.lean#L1-L14) [SUB250-R17-062](../research/t20-v6-20261012/sources/59da81856bc4f5f80d986d7d20ac906eb4ddedcc32e2a971fab4c7aca2a85500/FiniteHullSmoothRigidity.lean#L53-L148) [SUB250-R17-062](../research/t20-v6-20261012/sources/59da81856bc4f5f80d986d7d20ac906eb4ddedcc32e2a971fab4c7aca2a85500/FiniteHullSmoothRigidity.lean#L151-L222)

The distinct finite-hull approximate-iff body has another, independent failure: common_normal_sublinear_gains defines eta identically zero while its following proofs use eta(n)=ΣkΣj|D(n,k,j)|, where D is the difference between the two divergence values. Its preceding derivative argument still gives D(n,k,j)/e(n)→0 under the shared Hessian-normality premise. Finiteness then supports the displayed sum-of-absolute-remainders construction, with eta/e→0 and D≤eta, but not the written zero tolerance. For a singleton quadratic score and vertex p=1/2, take h=0, z=1 and e(n)=1/(4(n+1)); the span of p−v is zero, so that lemma’s normality condition is automatic, while the remainder is positive of order e(n)². This refutes its chosen zero-tolerance witness, not existence of a sublinear tolerance or the final tangent-constrained equivalence. The positive-barycentric tangent-ray and common-interior sequence argument remains valid. The final necessity direction separately invokes the supplied approximate-Hessian theorem; its imported identity is not established by a similarly named source. [NEXT250-Z50-206](../research/t20-v6-20261012/sources/a649f11b12788adbfb59bfed138657d542f6c460d8067904d193ce83700e5f51/FiniteHullApproximateIff.lean#L15-L45) [NEXT250-Z50-206](../research/t20-v6-20261012/sources/a649f11b12788adbfb59bfed138657d542f6c460d8067904d193ce83700e5f51/FiniteHullApproximateIff.lean#L47-L99) [NEXT250-Z50-206](../research/t20-v6-20261012/sources/a649f11b12788adbfb59bfed138657d542f6c460d8067904d193ce83700e5f51/FiniteHullApproximateIff.lean#L103-L124)

For a precise control on the tempting square-root inference, let
$`\varepsilon_k=k^{-4}`$, $`\eta_k=k^{-6}`$ and $`d_k=k^{-3}`$. Then
$`\eta_k/\varepsilon_k\to0`$ and $`d_k^2=\eta_k`$, while
$`d_k/\varepsilon_k=k\to\infty`$. A quadratic regret bound by itself would permit this displacement. The coherence constraint is equally essential to the linear coercivity: at $`p=(1/3,1/3,1/3)`$, the point $`c=p-d\mathbf1`$ satisfies


```math
\|c-e_j\|^2-\|p-e_j\|^2=3d^2
\quad\text{for every }j,
```


although $`\|c-p\|`$ is of first order in $`d`$. This positive subprobability vector is outside the sum-one hull. Nor can zero barycentric weights support the step from a zero weighted average to vanishing of every derivative. These controls identify the exact proof premises; they are not counterexamples within those premises. Linear-scale tolerance also changes the question. For the unscaled quadratic matrices $`I`$ and $`\operatorname{diag}(1,2,2)`$, let $`b=p+\varepsilon e_1`$ at an interior simplex point. For either matrix and each truth vertex, the excess loss from leaving the report at $`p`$ is $`-2\varepsilon(p_1-v_{j1})-\varepsilon^2\le2\varepsilon`$. Thus tolerance $`2\varepsilon`$ admits the unchanged baseline despite the nonproportional standards. Its ratio to $`\varepsilon`$ is two, so it does not satisfy the sublinear assumption.

Two retained SmoothRobustness variants break different premises of this argument. The first replaces sum-one repair by sum(cₙ)≤1 in three local interfaces but still uses cₙ as normalized weights on the simplex vertices; positive subprobability coordinates do not establish that hull membership. The second restores sum equality but changes ηₙ/εₙ→0 to ηₙ/εₙ→1 in five local interfaces while retaining the zero-error first-order conclusion. That conclusion is already false for f(x)=x, derivative L=id, p=h=0, rₙ=z=1 and ηₙ=εₙ=1/(n+1): the gain premise is equality but the asserted conclusion is 0≤−1. The limit argument would retain an added 1. This second body also infers eventual ηₙ≤εₙ from convergence of the ratio to one, and its final global premise still supplies ratio zero to a local theorem requiring ratio one. These exact variants do not replace the coherent, sublinear theorem above. Their common imports and axiom-print commands are not evidence of one verified dependency closure or of a fresh compiler outcome. [SUB250-R17-076](../research/t20-v6-20261012/sources/5ce6e7c53a0b9c64abcf5fd9939aa2213f0231b212a953e923de7b22c5fec88a/SmoothRobustness.lean#L150-L158) [SUB250-R17-076](../research/t20-v6-20261012/sources/5ce6e7c53a0b9c64abcf5fd9939aa2213f0231b212a953e923de7b22c5fec88a/SmoothRobustness.lean#L215-L219) [SUB250-R17-076](../research/t20-v6-20261012/sources/5ce6e7c53a0b9c64abcf5fd9939aa2213f0231b212a953e923de7b22c5fec88a/SmoothRobustness.lean#L248-L275) [SUB250-R17-076](../research/t20-v6-20261012/sources/5ce6e7c53a0b9c64abcf5fd9939aa2213f0231b212a953e923de7b22c5fec88a/SmoothRobustness.lean#L306-L317) [SUB250-R17-094](../research/t20-v6-20261012/sources/5f466daa3fd36c116289a36e25239012fc9dc7c98ffe91e4d4bfd4df640fbe92/SmoothRobustness.lean#L81-L101) [SUB250-R17-094](../research/t20-v6-20261012/sources/5f466daa3fd36c116289a36e25239012fc9dc7c98ffe91e4d4bfd4df640fbe92/SmoothRobustness.lean#L138-L158) [SUB250-R17-094](../research/t20-v6-20261012/sources/5f466daa3fd36c116289a36e25239012fc9dc7c98ffe91e4d4bfd4df640fbe92/SmoothRobustness.lean#L207-L211) [SUB250-R17-094](../research/t20-v6-20261012/sources/5f466daa3fd36c116289a36e25239012fc9dc7c98ffe91e4d4bfd4df640fbe92/SmoothRobustness.lean#L347-L366) [SUB250-R17-094](../research/t20-v6-20261012/sources/5f466daa3fd36c116289a36e25239012fc9dc7c98ffe91e4d4bfd4df640fbe92/SmoothRobustness.lean#L248-L317)

Another SmoothRobustness body keeps sum-one repairs and sublinear tolerance but weakens its general positive-derivative coercivity premise to nonnegative barycentric weights. The claimed coercivity is then false. In the real line take B(x,y)=xy, vertices0 and1, weights1 and0, and p=0. The direction1 lies in the span of p minus the vertices, yet both positive parts B(p−v_i,1) vanish, so no positive constant can bound its norm by their sum. A zero weighted average cannot force the derivative at the zero-weight vertex to vanish. The later categorical applications use strictly interior coordinates, but the displayed proof chain still invokes this defective general helper. Restoring positive weights on every spanning vertex, or changing the span with an appropriate proof, is a separate repair obligation; no affine-classification or compiler success is newly credited to this exact body. [A750-S50-068](../research/t20-v6-20261012/sources/bab2c8cc55057594d09cdc95e0571912cdd0ccab8130a925cc6a62261e89dc19/SmoothRobustness.lean#L20-L78) [A750-S50-068](../research/t20-v6-20261012/sources/bab2c8cc55057594d09cdc95e0571912cdd0ccab8130a925cc6a62261e89dc19/SmoothRobustness.lean#L150-L180) [A750-S50-068](../research/t20-v6-20261012/sources/bab2c8cc55057594d09cdc95e0571912cdd0ccab8130a925cc6a62261e89dc19/SmoothRobustness.lean#L248-L298) [A750-S50-068](../research/t20-v6-20261012/sources/bab2c8cc55057594d09cdc95e0571912cdd0ccab8130a925cc6a62261e89dc19/SmoothRobustness.lean#L347-L407)

### 4.2 A categorical rigidity theorem

**Theorem 3 — Universal categorical repair.** Let $`C`$ be the categorical simplex with $`n\geq3`$, and let the fixed additive generators satisfy (14). The following are equivalent:

1. For every $`p\in\mathrm{ri}C`$, weak common repairs exist along a sequence approaching $`p`$ on the single transverse direction $`h=e_1`$.
2. For every interior $`p`$ and every transverse $`h`$, strict common repair exists for every sufficiently small positive $`\varepsilon`$.
3. There are one constant $`a>0`$ and constants $`b_i,d_i`$ such that

```math
f_i(x)=a\,g_i(x)+b_ix+d_i\qquad(0\leq x\leq1).
\quad\text{(18)}\quad
```

Replacing condition 1 by the existence of $`o(\varepsilon)`$-repairs gives the same equivalence.

**Proof.** Equation (7) applied to the Hessians makes (16) equivalent to

```math
r_i(p_i):=\frac{f_i''(p_i)}{g_i''(p_i)}=a(p)
\quad\text{for every }i.
\quad\text{(19)}\quad
```

Fix two values $`s,t\in(0,1)`$ for coordinate $`i`$. Choose another coordinate $`j`$ and a small $`u>0`$ with $`s+u<1`$ and $`t+u<1`$. Because there is a third coordinate, both pairs can be completed to strictly positive simplex points. Equation (19) gives $`r_i(s)=r_j(u)=r_i(t)`$. Thus each ratio is constant; feasible pairs show that the constants agree. Integrating twice and using endpoint continuity gives (18).

Conversely, minimize $`D_G(c,b_\varepsilon)`$ over the compact set $`C`$. Its unique minimizer tends to $`p`$: the objective converges uniformly on $`C`$ to $`D_G(c,p)`$, whose unique minimum is $`p`$. It therefore lies in $`\mathrm{ri}C`$ for small $`\varepsilon`$, and
$`\nabla G(c)-\nabla G(b_\varepsilon)\perp T`$.
Equation (4) gives gain $`D_G(c,b_\varepsilon)>0`$ at every truth. By (18) the $`F`$-gain is $`a`$ times this gain. $`\square`$

The conclusion depends on fixed generators across contexts, additive separability, at least three categorical coordinates, and relative interior. None is an innocuous convention.

The inspected BregmanProjection source supplies the compatible positive mechanism: compact minimizers of c↦D(c,b) converge to an interior coherent p as b→p, interior stationarity annihilates every simplex tangent, and the three-point identity gives weak repair. Positive affine rescaling transfers that repair to the second score. Its final equivalence, however, is stated for cardinality at least two, with necessity delegated to an imported rigidity theorem. That two-coordinate extension is not established by the inspected argument: the ordinary binary control below has common repairs without positive affine equivalence. Unless additional restrictions in the uninspected score interface exclude that control, the extension conflicts with it. The three-coordinate hypothesis of Theorem3 is therefore retained; no fresh verification of the imported necessity result is claimed. [SUB-M6-027](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/5335edddd506a7d10d636df0d47aa54f4391e565cb0c3069359ca8d4aeebf04e/BregmanProjection.lean#L88-L131) [SUB-M6-027](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/5335edddd506a7d10d636df0d47aa54f4391e565cb0c3069359ca8d4aeebf04e/BregmanProjection.lean#L149-L220) [SUB-M6-027](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/5335edddd506a7d10d636df0d47aa54f4391e565cb0c3069359ca8d4aeebf04e/BregmanProjection.lean#L245-L274)

A distinct BregmanProjection variant keeps the three-coordinate premise but replaces the perturbation in CommonLocalRepairs by p+e·0 for both scores. For any positive sequence e tending to zero, choosing c=p makes every displayed comparison reflexive, so this predicate imposes no relation between the generators and does not use its i0 parameter. Its claimed affine necessity therefore does not follow from the written repair condition; the sufficiency proof also calls the single-score construction in direction vertex i0 while its goal has direction zero. This is different from the preceding two-coordinate extension. The earlier compact-projection, stationarity, weak-repair and affine-scaling arguments remain separate authored interfaces, not evidence for the vacuous characterization or newly checked imports. [AF750-Q4-198](../research/t20-v6-20261012/sources/d2290a7a44877d98593ac79723c4563181388ccef3b63dc1d6b09f4ec2fcde8e/BregmanProjection.lean#L88-L220) [AF750-Q4-198](../research/t20-v6-20261012/sources/d2290a7a44877d98593ac79723c4563181388ccef3b63dc1d6b09f4ec2fcde8e/BregmanProjection.lean#L222-L279)

### 4.3 Binary and nonseparable counterexamples

For the binary coherent segment $`C=\{(t,1-t):0\leq t\leq1\}`$, take quadratic coordinate potentials and binary-entropy coordinate potentials

```math
f(x)=x^2,\qquad
g(x)=x\log x+(1-x)\log(1-x).
```

For an interior incoherent forecast $`(x,y)`$, the arithmetic correction
$`t=(x+1-y)/2`$ is a strict common repair. It is the Euclidean projection. For the logarithmic loss the two comparisons reduce to

```math
t^2-x(1-y)=\frac{(x+y-1)^2}{4},\qquad
(1-t)^2-(1-x)y=\frac{(x+y-1)^2}{4}.
\quad\text{(20)}\quad
```

Both are positive for an incoherent forecast. The curvatures $`2`$ and $`1/[x(1-x)]`$ are not proportional. Section 6 explains the broader rank-one reason.

Separability also matters. On the three-outcome simplex let $`a=(1,-1,0)`$ and

```math
F(x)=\frac12\|x\|_2^2,\qquad
G(x)=\frac12\bigl(\|x\|_2^2+(a\cdot x)^2\bigr).
\quad\text{(21)}\quad
```

Both Hessians have the same normal line spanned by $`(1,1,1)`$, so they have the same projection and common repair at every context. Yet the potentials are not positive affine rescalings. They can reverse rankings among coherent forecasts: at truth $`e_3`$, the points
$`c=(49/100,1/100,1/2)`$ and $`d=(1/3,1/3,1/3)`$
have unscaled squared losses $`2451/5000<2/3`$, whereas after adding $`(a\cdot x)^2`$ the first loss becomes $`3603/5000>2/3`$.

The converse separation is also possible: identical coherent scores need not determine the repair of an incoherent forecast. For positive vectors x,y, put s=Σxᵢ, t=Σyᵢ, p=x/s and q=y/t, and define F(x)=‖x‖²/(2s)+s²/2. Its truth-first divergence is D_F(x,y)=s‖p−q‖²/2+(s−t)²/2. The Hessian quadratic form is hᵀH_F(x)h=‖h−pΣhᵢ‖²/s+(Σhᵢ)², which is positive for every nonzero h. On the coherent simplex, including truth vertices by continuous extension, this divergence is exactly half the squared Euclidean loss. Yet minimizing D_F(c,b) over coherent c gives c=b/Σbᵢ, whereas the ordinary Euclidean ambient potential generally gives a different projection. For b=(3/8,1/8), the two projections are (3/4,1/4) and (5/8,3/8). The perspective repair improves the original F-loss by 1/8 at either truth vertex. If the normalized vector is the actual law, its coherent expected loss is 3/16, while using the Euclidean repair gives 13/64, an excess of 1/64 even without new information. This is a distinction between ambient extensions of the same coherent scoring rule, not a failure of either projection under its own specified objective. The exact formulas come from an unexecuted control body; its separate nonquadratic and boundary examples do not supply a newly verified general repair or flow theorem. [AFTER1384-S9-148](../research/t20-v6-20261012/sources/3609259ad8ca9a594ba2efb7f045db19e4d5e9bea52c96c8790c0639b987de93/verify.py#L6-L13) [AFTER1384-S9-148](../research/t20-v6-20261012/sources/3609259ad8ca9a594ba2efb7f045db19e4d5e9bea52c96c8790c0639b987de93/verify.py#L26-L79)

### 4.4 The general higher-rank theorem

Let $`l_i=\min_Cx_i`$, $`u_i=\max_Cx_i`$, and $`I_i=(l_i,u_i)`$. Assume $`l_i<u_i`$ for every coordinate. Use the dependency blocks of $`T`$ from Section 3. Suppose every nonsingleton block satisfies $`\dim T_B\geq2`$; singleton blocks are then free because constant coordinates have been excluded.

**Theorem 4 — Smooth rigidity by dependency block.** For fixed additive $`F,G`$ as in (14), universal local common repair is equivalent to the existence of constants $`a_B>0`$ such that

```math
f_i(x)=a_Bg_i(x)+b_ix+d_i
\quad\text{for }i\in B,\quad x\in[l_i,u_i],
\quad\text{(22)}\quad
```

on every nonsingleton block. No proportionality is required on a free singleton. “Universal local common repair” may mean weak repair along a sequence at every $`p,h`$, or existence of $`o(\varepsilon)`$-repairs there. Under (22), one gets strict repair for all sufficiently small positive $`\varepsilon`$.

**Proof of necessity.** The Hessian projections agree at each $`p`$. Theorem 2 makes $`r_i(p_i)=f_i''(p_i)/g_i''(p_i)`$ equal to one value $`a_B(p)`$ on a block. Since $`\dim T_B\geq2`$, two coordinate functionals on $`T_B`$ are linearly independent. Their joint map sends a relative neighborhood of $`p`$ to an open rectangle in $`\mathbb R^2`$. On that rectangle, $`r_i(s)=r_j(t)`$, so both are locally constant and $`a_B`$ is locally constant on $`\mathrm{ri}C`$. This relative interior is convex and connected, hence $`a_B`$ is constant. The image of $`\mathrm{ri}C`$ under coordinate $`i`$ is exactly $`I_i`$, so integration and continuity give (22).

**Proof of sufficiency.** Take the unique minimizer $`c`$ of $`D_G(c,b_\varepsilon)`$ on the actual hull $`C`$. As before, it tends to $`p`$ and lies in relative interior. First-order optimality holds separately on every $`T_B`$. Equation (22) multiplies each block's gradient difference by the constant $`a_B`$, so the $`F`$-gradient difference also annihilates each nonsingleton $`T_B`$. On a free singleton, stationarity reads $`g_i'(c_i)=g_i'(b_i)`$; positive curvature implies $`c_i=b_i`$, so the $`F`$-gradient difference vanishes there too. Equation (4) proves strict gain for both standards. No product decomposition of $`C`$ was assumed: the minimization took place on the full joint hull. $`\square`$

Only the attained coordinate intervals occur in (22); the theorem supplies no information about parts of a generator that the truth hull never visits. Nor does it classify rank-one constrained blocks.

For a supplied finite truth list, the tangent space, its coordinate dependencies and the ranks of its blocks are finite linear-algebra data. That observation makes the structural hypothesis checkable from exact truth coordinates; it does not give a decision procedure for the identities between arbitrary smooth functions in (22). It also gives no automatic numerical robustness: an arbitrarily small perturbation can remove an exact linear dependence. Approximate data require an error model and a separately proved stability result. The earlier block-classification source records a then-unresolved rank-one case; the explicit treatment in Section 6 supplies the later mathematics and is not withdrawn by that historical status. [block-classification-pre-review]

### 4.5 One anchor can serve an arbitrary family

Under the hypotheses of Theorem 4, let $`G`$ be fixed and let $`\{F_k\}_{k\in K}`$ be any family. If every pair $`(F_k,G)`$ has universal local common repair, (22) holds separately for each $`k`$. The one $`G`$-minimizer constructed above then strictly improves every $`F_k`$ and $`G`$. Its existence scale depends on the anchor and the local geometry, not on the cardinality of $`K`$.

This conclusion uses the blockwise proportionality theorem. It is not an inference from arbitrary pairwise intersections of repair sets. An infinite family with only pointwise Hessian compatibility would need uniform remainder control for analogous approximate statements.

## 5. What local compatibility does and does not establish

### 5.1 Approximate equivalence for a finite family

At one fixed interior $`p`$, consider finitely many $`C^2`$ potentials with positive-definite Hessians. Under the localization conditions of Section 4.1, common Hessian projection is equivalent to the existence of some common $`\eta_\varepsilon=o(\varepsilon)`$ repair.

Necessity is (17). For sufficiency, let the common projected vector be $`z`$ and set $`c_\varepsilon=p+\varepsilon z`$. Every loss difference
$`\Delta_{k,j}(\varepsilon)=D_{F_k}(v_j,c_\varepsilon)-D_{F_k}(v_j,b_\varepsilon)`$
has vanishing first-order term, so $`\Delta_{k,j}=o(\varepsilon)`$. The finite sum
$`\eta_\varepsilon=\sum_{k,j}|\Delta_{k,j}(\varepsilon)|`$
is nonnegative, is $`o(\varepsilon)`$, and bounds every excess.

This is an existential tolerance statement. It does not give exact repair, does not satisfy every prescribed $`o(\varepsilon)`$ allowance, and need not yield $`o(\varepsilon^2)`$ error. Necessity works for an arbitrary family by fixing one standard at a time; this sufficiency argument uses finiteness.

The regularity and family quantifiers in this proof are independent. Continuous second derivatives of the generator make each forecast-loss difference differentiable at the interior baseline, which is enough for the $`o(\varepsilon)`$ remainder used here. They do not by themselves give a quadratic remainder bound for that forecast-loss difference. A stronger estimate needs corresponding control of its derivative. Likewise, pointwise vanishing of a family of remainders does not bound their supremum: the elementary array $`r_n(k)=1`$ when $`n=k`$ and zero otherwise tends to zero for each fixed $`n`$ as $`k\to\infty`$, but $`\sup_n r_n(k)=1`$. This array is a control on the exchange of quantifiers, not a claimed realization by an infinite smooth score family. The exact anchored result in §4.5 avoids this issue through structural proportionality, not through a hidden uniform Taylor estimate. [approximate-iff-source], [hull-interface-review]

The [local approximate source][approximate-iff-source] also reports a sharper binary control: a quadratic and a complement-symmetric quartic generator have the same Hessian tangent projection along the coherent line, yet common exact repair fails on a perturbation interval. The reported control excludes every allowance $`\eta\le\varepsilon^2/100`$, hence every prescribed $`o(\varepsilon^2)`$ allowance eventually. Its quartic forecast losses are nonconvex, so this report does not contradict the convex-forecast-loss midpoint result discussed below. The selected source does not give the defining quartic polynomial; the threshold is preserved here as an attributed source report, not a newly rederived numerical theorem. Its exact formal control and original verification evidence retain that separate verification role.

### 5.2 Universal nudges versus an individual endpoint

A strict common descent direction at a forecast $`b`$ is a nonzero $`d`$ with

```math
\nabla_bD_{F_k}(v_j,b)\cdot d<0
\quad\text{for all }k,j.
\quad\text{(23)}\quad
```

Such a direction improves the losses for a sufficiently short movement. It need not carry the forecast to a coherent endpoint.

For fixed additive $`F,G`$ on a categorical simplex with $`n\geq3`$, universal local existence of a common descent direction is nevertheless rigid. Suppose at every interior $`p`$, along arbitrarily small forecasts $`p+\varepsilon e_1`$, a common descent direction exists. Normalize these directions to unit length and extract a limit $`d\ne0`$. At the coherent limit, (23) becomes
$`(p-v_j)^\top H_F(p)d\leq0`$ and its $`G`$-analogue. Their positive barycentric averages are zero. Hence

```math
H_F(p)d\in\mathrm{span}\{\mathbf1\},
\qquad
H_G(p)d\in\mathrm{span}\{\mathbf1\}.
```

The two Hessian-normal lines therefore coincide. Equations (7) and (19), followed by the three-coordinate argument, give (18). Conversely, when (18) holds, put $`s=\sum_i b_i`$ and

```math
d_i=\frac{1-s}{f_i''(b_i)}.
\quad\text{(24)}\quad
```

Every $`F`$-loss has directional derivative $`-(s-1)^2`$, and the $`G`$-derivative is a positive multiple of it. There is also a coherent-directed nudge: define

```math
r_i(b)=\frac{f_i''(b_i)^{-1}}{\sum_jf_j''(b_j)^{-1}},
\qquad
c=b-(s-1)r(b).
\quad\text{(25)}\quad
```

Near an interior coherent point, $`c`$ is in the simplex, and the derivative along $`c-b`$ is
$`-(s-1)^2/\sum_jf_j''(b_j)^{-1}<0`$.
Thus universal local nudges, universal coherent-directed nudges, and universal endpoint repair impose the same fixed-generator rigidity here. This extends neither to an arbitrary isolated forecast nor to all geometries.

Two retained nudge variants require separate qualifications. NudgeRigidity writes nonpositive directional inequalities, with no nonzero-direction premise, in both its proportionality theorem and CommonLocalNudges. The zero direction meets those weak inequalities, so the proof cannot infer a nonzero normalized limit merely from them; the strict descent premise in (23) is substantive. CoherentNudgeRigidity does require strict descent toward an interior coherent endpoint, but defines its candidate coordinate as b_i−ε/f_i″(b_i), omitting division by S=Σ_j1/f_j″(b_j) while later steps use that divisor. Its displayed candidate has coordinate sum 1+ε−εS, not generally one. Formula (25) retains the required normalization. These are exact-source definition/proof mismatches, not new universal rigidity theorems or observed kernel failures. [NEXT-FL8-026](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/203ddef990b34133cfd4b24f7c0e5e98190b79ef6e9c58f6768e486446c79ad8/NudgeRigidity.lean#L29-L101) [NEXT-FL8-042](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/2332704a8db20fa48f4eb7aba7c63c4414c68ae6e78baab917b7f1e99ab91e60/CoherentNudgeRigidity.lean#L12-L103)

For a concrete pointwise separation, use unscaled quadratic matrices
$`I`$ and $`\mathrm{diag}(1,2,2)`$, and set

```math
b=(1/2,7/20,7/20),\qquad d=(-13/10,-1,-1).
```

The three derivatives are $`(-1/10,-7/10,-7/10)`$ for $`I`$, and $`(-3/2,-1/10,-1/10)`$ for the second matrix. Moreover

```math
b+\frac2{33}d=(139/330,191/660,191/660)
```

is coherent, so the common nudge points toward a coherent target. Yet no common weak coherent endpoint exists. If $`c_0+c_1+c_2=1`$, the $`I`$-loss at truth $`e_0`$ forces
$`(1-c_0)^2\leq33/100`$.
Averaging the second loss over $`e_1,e_2`$, and minimizing over $`c_1,c_2`$ with their sum fixed, forces $`c_0^2\leq17/100`$. Their sum implies $`c_0^2+(1-c_0)^2\leq1/2`$, hence $`c_0=1/2`$, contradicting $`c_0^2\leq17/100`$.

The displayed coherent endpoint itself illustrates the failure of continuing a short nudge without checking the full loss: its unscaled $`I`$-loss at $`e_0`$ exceeds that of $`b`$ by $`68/9075`$. A negative initial derivative ensures an improving initial segment, not improvement at every point on that ray. In higher codimension, two distinct Hessian-normal subspaces may also share a nonzero vector; the categorical argument uses their being lines. [nudge-review]

The common-nudge field also has a boundary-sensitive clock distinction. Take additive curvature diag(x,1,1) on the positive interior and the curve b(x)=(x,1/2+x²/2,1/2+x²/2), starting at x=1/2. Its excess sum is r=x+x², so the field −r(1/x,1,1) is exactly db/dt when dx/dt=−1−x. The first coordinate reaches zero in physical time log(3/2), with the boundary limit (0,1/2,1/2). For the normalized clock τ(x)=log[(3/4)/(x+x²)], however, dτ/dt=1/x+2 and τ tends to infinity as x decreases to zero. Thus the finite-time boundary arrival in this particular field is compatible with an infinite reparameterized time; it does not license continuation through vanishing curvature or establish a general endpoint theorem. These identities are displayed in the unexecuted exact-control source. Its separately named distinct-arrival control checks only equality of two initial sums, so no second trajectory or differing-arrival conclusion is inferred from that label. [G24–25-207](../research/t20-v6-20261012/sources/1ea8dd5aac22fe14808f5c56f95cf0584711ad1458f6f632913ed5ef2d1adb04/independent_power_controls.py#L18-L31)

The geometry reconciliation reports a separate classification for the selected single-generator field ḃ_i=(1−z)q_i(b_i), z=Σ_ib_i and q_i=1/f_i″>0, on the full open product (0,1)^n. For n≥2 and continuous reciprocal curvatures, original-clock scalar projectability of z is equivalent to q_i(x)=ax+c_i with one common slope. The reported local Pexider argument needs no third derivative. This is one summary and one field, not the preceding common-repair comparison of two fixed generator families. Scalar closure and current admissibility still do not determine the first boundary exit: the report describes quadratic fields with equal z trajectories and different exits. Its dual-coordinate continuation result says every n=2 interior start is forward safe, whereas for n≥3 universal forward safety requires and is equivalent to f_i′(0+)=−∞ for every coordinate. Within that n≥3 class, adding scalar closure forces q_i(x)=ax with a>0, giving scaled negative-Shannon generators up to affine terms. This is a source-reported forward-time, field-specific result; its two controlling proof bodies were not reopened here. It supplies no universal uniqueness of safe geometry, geodesic completeness or permission to change clocks when comparing arrival times. [AFTER3384-FIFTH25-115](../research/t20-v6-20261012/research-v6/early_remaining/geometry_review_completion/REPORT.md#L59-L67)

The constant-curvature controls separate two other boundary behaviors. Starting at (1/4,3/4,3/4), the field ḃ_i=1−Σb_j has the trajectory b=(x,1/2+x,1/2+x), ẋ=−3x, so its coherent boundary limit is reached only as t→∞. Starting instead at (1/100,4/5,4/5), every coordinate decreases by the same amount until the first reaches zero; the resulting boundary point (0,79/100,79/100) retains excess sum 29/50. Since the excess solves ṙ=−3r and starts at 61/100, this first arrival occurs at log(61/58)/3, before coherence. Conversely the positive ray field ḃ_i=a(1−z)b_i, z=Σb_i and a>0, has ż=az(1−z), preserves b_i/z, and approaches the normalized initial vector; its exact solution is z=z₀/[z₀+(1−z₀)e^(−at)]. These ordinary identities concern the displayed fields and do not authorize continuation past a boundary or a general convergence claim. Their finite rational samples were not run. [AFTER2134-T25-073](../research/t20-v6-20261012/sources/8d4e49315ccbe23f2a04942e22082bcddf8de9cfe67fd0ce85ded7a45dcafc72/controls.py#L34-L83)

Konek's analysis of common improvements under epistemic and practical scoring standards is an important antecedent [6]. The distinction here is between an initial derivative and a complete endpoint, together with the stated universal quantifiers; it is not a claim that common-descent analysis began with this exposition.

### 5.3 A fixed numerical obstruction for entropy and quadratic loss

The categorical theorem predicts disagreement between the Euclidean and binary-entropy generators. It can also be witnessed without relying on a limiting argument. Let

```math
p=(1/2,1/3,1/6),\quad h=e_1,\quad
b=p+\varepsilon e_1,\quad
q=p+\varepsilon(2/3,-1/3,-1/3).
```

The entropy Hessian has normalized reciprocal vector
$`(9/22,4/11,5/22)`$, unlike the Euclidean normal vector $`(1/3,1/3,1/3)`$.
The tangent ball with radius $`1/6`$ lies in the simplex. Equation (8) shows that every exact Euclidean repair has
$`\|c-q\|_2\leq2\varepsilon^2`$, hence
$`\|c-q\|_1<4\varepsilon^2`$.

At categorical truth $`e_j`$, the entropy loss is
$`-\log P_j(x)`$, where $`P_j(x)=x_j\prod_{i\ne j}(1-x_i)`$.
Each $`P_j`$ is Lipschitz with constant one for the $`\ell^1`$ norm on the cube. Direct multiplication gives

```math
P_3(b)-P_3(q)=
\frac{5\varepsilon}{108}-\frac{\varepsilon^2}{18}
-\frac{2\varepsilon^3}{27}.
\quad\text{(26)}\quad
```

At $`\varepsilon=1/1000`$, subtracting $`4\varepsilon^2`$ leaves
$`63361/1500000000>0`$.
Consequently $`P_3(c)<P_3(b)`$ for every Euclidean repair $`c`$: the entropy loss at that truth is worse. Boundary candidates with zero $`P_3`$ cannot rescue the comparison. This is an exact finite obstruction, not a rounded numerical search.

### 5.4 Why the standards must remain fixed across contexts

The order of quantifiers in Theorem 3 cannot be changed. On the three-outcome simplex let $`F(x)=\tfrac12\sum_i x_i^2`$. For each coherent interior point $`p`$, define a different generator

```math
G_p(x)=\sum_i\left(\frac{(x_i-p_i)^2}{2}+(x_i-p_i)^4\right).
\quad\text{(27)}\quad
```

Its Hessian at its chosen $`p`$ is $`I`$. For $`b=p+\varepsilon e_1`$, the Euclidean correction $`q=p+\varepsilon(2/3,-1/3,-1/3)`$ has $`F`$-gain $`\varepsilon^2/6`$. Direct Bregman expansion gives

```math
D_{G_p}(v,b)-D_{G_p}(v,q)
=\frac{\varepsilon^2}{6}
 +\frac{7\varepsilon^4}{3}
 -\frac{8\varepsilon^3}{3}(v_1-p_1)>0
\quad\text{(28)}\quad
```

for $`0<\varepsilon<1/16`$, after also restricting to the local feasible scale. Nevertheless $`G_p`$ is not an affine rescaling of $`F`$, as its fourth coordinate derivative is $`24`$. The construction establishes a generator chosen separately for each context. It does not furnish one fixed nonquadratic generator satisfying the universal categorical theorem.

### 5.5 Faithful changes of representation

A change of coordinates must preserve the actual loss comparisons, not merely the appearance of a potential. For a differentiable map $`L`$,

```math
D_{F\circ L}(x,y)
=D_F(Lx,Ly)
 +dF_{Ly}\bigl(Lx-Ly-dL_y(x-y)\bigr).
\quad\text{(29)}\quad
```

Calling the left side a Bregman divergence additionally requires convexity of $`F\circ L`$. Affine $`L`$ makes the remainder vanish. Nonlinear injectivity does not. With $`L(x)=x^2`$ on the positive line and $`F(z)=z^2/2`$, the remainder is $`y^2(x-y)^2`$; at $`x=2,y=1`$, the pulled-back loss is $`9/2`$, while the divergence of the composite potential is $`11/2`$.

Any transport of a repair theorem must therefore specify the truth set, feasible forecasts, disturbances, and the whole transformed loss. Additive separability need not survive a general coordinate change. Curved representational divergences provide a broader setting for this distinction [8]; equation (29) is the exact elementary identity needed here.

A Riemannian re-description requires transporting the metric as well as the objective. On a fixed smooth manifold, positive-definiteness gives grad_g J=0 exactly when dJ=0; changing the metric while retaining J and the topology therefore preserves its critical set and minimizers, but not its directions or speeds. For a diffeomorphism F with g₁=F* g₂ and J₁=J₂∘F, pairing with arbitrary tangents and using the chain rule gives DF(grad_g₁ J₁)=grad_g₂ J₂∘F. Retaining Euclidean metrics on both sides of a nonisometric coordinate change need not satisfy this contract. Descent is also weaker than hard-constraint preservation. On R² take J(q)=|q|²/2, K={q₁≥0}, q=(0,1) and G=((2,−1),(−1,1)). The negative gradient is (−1,−2); a step of size 1/4 reaches (−1/4,1/2), lowering J from 1/2 to 5/32 while leaving K. Its G-metric projection onto the tangent half-space is (0,−1), whose same-sized step stays in K and lowers J to 9/32. These are ordinary identities and one explicit feasible-step contrast, not a global viability or convergence theorem. The source's rational checks were not rerun. Its smooth coordinates deliberately omit exact source and authority fields; neither a lower J nor an isometry authenticates those retained records or realizes an actual inquiry. [AFTER3384-EIGHTH25-175, lines 5–29](../research/t20-v6-20261012/sources/110d235c2054a2bf46d0ae1744c663a0a743372dbd5779d16a52f560b246c410/RESULT.md#L5-L29) [AFTER3384-EIGHTH25-175, lines 31–45](../research/t20-v6-20261012/sources/110d235c2054a2bf46d0ae1744c663a0a743372dbd5779d16a52f560b246c410/RESULT.md#L31-L45) [AFTER3384-EIGHTH25-175, lines 47–62](../research/t20-v6-20261012/sources/110d235c2054a2bf46d0ae1744c663a0a743372dbd5779d16a52f560b246c410/RESULT.md#L47-L62)

The scalar Hessian calculation gives a precise extension beyond the quadratic case. On an open positive interval, let f be C³ with h=f″>0 and write B(x,y)=f(x)−f(y)−f′(y)(x−y). Its Hessian is [[h(x),−h(y)],[−h(y),h(y)−(x−y)h′(y)]]. With g=1/h, its determinant divided by h(x)h(y)² is g(y)+g′(y)(x−y)−g(x). Because the first diagonal entry is positive, this Hessian is positive semidefinite everywhere exactly when every tangent to g lies above its graph, equivalently when g is concave. Thus B is jointly convex exactly under that reciprocal-curvature condition. For Dμ(p,q)=ΣᵢμᵢB(pᵢ/μᵢ,qᵢ/μᵢ), rowwise Jensen with weights Kⱼᵢμᵢ/(Kμ)ⱼ then proves contraction under any column-stochastic K, provided μ is positive, zero-reference output rows are omitted, and all density arguments lie in the interval. Quadratic, entropy x log x and x^(3/2) generators satisfy the condition; x⁴ does not on the positive line. This is an ordinary derivation from the displayed Hessian and weighted-merge formulas, not a newly executed symbolic test or an equality-to-recovery theorem. [AFTER2384-SEVENTH25-165](../research/t20-v6-20261012/sources/ba0ee95c1e7864a1ebbd381dab52d6b58fa14a24b7174995efc4406b5d02b0f5/verify.py#L3-L17) [AFTER2384-SEVENTH25-165](../research/t20-v6-20261012/sources/ba0ee95c1e7864a1ebbd381dab52d6b58fa14a24b7174995efc4406b5d02b0f5/verify.py#L20-L38)

Even a statistically sufficient truth-coordinate merge need not preserve a score that is reset after merging. Let q=(1/4,1/4,1/2), p₊=(3/8,3/8,1/4), p₋=(1/8,1/8,3/4), and K(x₀,x₁,x₂)=(x₀+x₁,x₂). A binary observation with likelihoods(3/4,3/4,1/4) and its complement has each outcome probability 1/2 and precisely these posteriors. The reverse R(u,v)=(u/2,u/2,v) recovers q and both p±, and KL(p±‖q)=KL(Kp±‖Kq). Nevertheless the quadratic regret Dμ(p,q)=½Σᵢ(pᵢ−qᵢ)²/μᵢ is 3/64 with fine reference μ=(1,1,1), whereas resetting the coarse reference to (1,1) gives 1/16. Transporting it instead to Kμ=(2,1) restores 3/64. This equality concerns regret and information gain, not absolute Bayes risk: the fine prior and expected posterior risks are 5/16 and 17/64, while their transported coarse counterparts are 3/16 and 9/64, differing by the common offset 1/8. Sufficiency therefore does not authorize replacing the transported scoring standard. These values follow by the displayed finite formulas, without executing the symbolic checker. [AFTER1634-S8-190](../research/t20-v6-20261012/sources/5be0ea120015682aafb73074d74c52608e55931589be4e82e50bc2c1309c2287/verify.py#L20-L62)

For C² strictly convex potentials f_n and f_m on the open probability simplexes and a column-stochastic K with no zero output row, cross-space contraction D_fm(Kp,Kq)≤D_fn(p,q) for every positive p,q is equivalent to the tangent inequality Hess f_m(Kq)[Kv,Kv]≤Hess f_n(q)[v,v] at every interior q and every v with Σv_i=0. Necessity follows from p=q+εv and the second-order expansion. Sufficiency integrates that inequality along q+t(p−q), using D_f(p,q)=∫₀¹(1−t)Hess f(q+t(p−q))[p−q,p−q]dt. Matching at one point is insufficient. Equality for all pairs likewise requires equality of these forms everywhere; a genuine noninjective lumping cannot be an isometry of a positive fine tangent metric. For the perspective potentials F_n(sp)=s f_n(p)+a(s), retaining the same radial a on both spaces makes full-cone contraction equivalent to the simplex condition, because the shared radial divergence cancels. Mass-preserving normalization commutes with K, but this alone proves neither divergence contraction nor descent of arbitrary likelihood multiplication. [AFTER3384-SECOND25-044](../research/t20-v6-20261012/sources/077fabaf882988d2de23bda85fd40cc03f6f630c0ca859f12864d53c604fbd94/RESULT.md#L16-L48)

**Repeated coordinates and the transported domain.** For an injective affine encoding $`\phi(x)=Mx+a`$, the exact identity just established is


```math
D_{F'\circ\phi}(v,b)=D_{F'}(\phi(v),\phi(b)).
```


The truth population, forecast, candidate repair set and allowed perturbations must all be transported by the same map. If coordinate $`x_i`$ is repeated in several encoded slots and the encoded potential is quadratic with slot weights $`w_\ell`$, its pullback gives $`x_i`$ the combined weight $`\sum_{\ell:\,\ell\text{ repeats }i}w_\ell`$. Equal weights per slot can therefore produce unequal weights per original coordinate. Replacing that pullback by an unweighted source score changes the standard.

An off-image perturbation that makes two copies disagree introduces a forecast absent from the source problem. The identity does not authorize an equivalence for that enlarged intervention domain. In particular, three slots encoding only two genuine truth states do not satisfy the three-outcome premise of Theorem 3. Faithful transport preserves the actual joint hull and its tangent dependencies; it does not replace them by a product hull or by a larger categorical simplex. These facts connect the representation boundary here to the norm-identity requirement in §5.4. [source-bridge-synthesis]

The weighted quadratic contract has a precise contraction rule. For a column-stochastic K and positive reference μ, let ν=Kμ, omit zero-reference output rows, and write zᵢ=(pᵢ−qᵢ)/μᵢ and aᵢ|ⱼ=Kⱼᵢμᵢ/νⱼ. Then 2[Dμ(p,q)−Dν(Kp,Kq)]=Σⱼνⱼ Var_{a·|ⱼ}(z)≥0, by expanding each weighted variance. Equality requires z constant on every output fibre with positive reference weight. Recovering p and q alone does not ensure this: in the preceding merge, replace μ by (1,2,1). The same R still recovers p₊ and q, but not μ; the fine and coarse regrets are 11/256 and 1/24, with gap 1/768. This is specific to the transported quadratic geometry, not every weighted Bregman generator. Nor is merging truth labels the same operation as garbling an observation while keeping truth coordinates fixed: independently flipping the preceding binary observation with probability 1/4 changes its posterior displacements to half their old size and reduces its quadratic information gain from 3/64 to 3/256. The source’s quartic and ambient-perspective checks remain separate authored controls, not a newly executed general contraction theorem. [AFTER1634-S8-190](../research/t20-v6-20261012/sources/5be0ea120015682aafb73074d74c52608e55931589be4e82e50bc2c1309c2287/verify.py#L63-L99)

Fixed-truth observation garbling has a general identity that does not require cross-space score transport. For a fixed finite Markov law X→Y→Z, interior posteriors p_Y,p_Z, prior q and one differentiable convex f on the unchanged truth simplex, conditional expectation gives p_Z=E[p_Y|Z]. Hence I_f(X;Y)=E D_f(p_Y,q)=E f(p_Y)−f(q), and I_f(X;Y)−I_f(X;Z)=E D_f(p_Y,p_Z)≥0. Strict convexity makes equality equivalent to p_Y=p_Z almost surely. This includes Brier, despite its failure when coordinate weights are reset after changing truth spaces. The joint law and score are fixed premises: retracting a discredited source or correcting a likelihood model is not automatically such a garbling. Separately, in the transported quadratic contract, one stochastic reverse recovering p,q and μ is sufficient for equality, by applying contraction through K and then through the reverse. Recovering only p and q is insufficient, as the existing counterexample shows; equality itself still need not supply a reverse channel. [AFTER3384-SECOND25-044](../research/t20-v6-20261012/sources/077fabaf882988d2de23bda85fd40cc03f6f630c0ca859f12864d53c604fbd94/RESULT.md#L99-L144)

The converse implication from quadratic-divergence equality to recovery of both laws also fails. Use μ=(1/3,1/3,1/3), p=(1/4,5/12,1/3), q=(1/6,1/3,1/2), and let K merge the first two coordinates. For Dμ(p,q)=½Σᵢ(pᵢ−qᵢ)²/μᵢ, direct substitution gives Dμ(p,q)=D_{Kμ}(Kp,Kq)=1/16. The normalized differences on the merged fibre agree, exactly as the variance criterion requires. Nevertheless ‖p−(4/3)q‖₁=7/18, while ‖Kp−(4/3)Kq‖₁=1/3. If one column-stochastic R recovered both p and q, it would recover that signed combination too, contradicting the ℓ¹ contraction of a stochastic matrix. Thus equality for this one transported quadratic divergence does not certify a reverse channel for the pair. This is a finite exact counterexample, not a refutation of the contraction formula or a claim about every Bregman generator. The source’s symbolic controls were not executed. [AFTER2384-SIXTH25-145](../research/t20-v6-20261012/sources/b8146a7c0b3f7a71b636f4ab91565a7c42b5723f97d2b10f1bc306683cd845e2/check_independent.py#L58-L65)

## 6. Rank-one blocks and comparison of means

### 6.1 Normalizing an isolated segment

Consider an isolated one-dimensional coherent segment. An affine coordinate change sends its endpoints to $`(0,\ldots,0)`$ and $`(1,\ldots,1)`$; if an original coordinate has negative orientation, reflect it. A transformed scalar potential has curvature $`u_i^2f_i''(a_i+u_it)>0`$. The Bregman comparisons are unchanged by this affine pullback.

Thus a forecast is $`t=(t_1,\ldots,t_d)\in(0,1)^d`$, $`d\geq2`$, and a coherent repair has all coordinates equal to $`q`$. For each standard $`k`$, let the coordinate potentials $`\psi_{ki}`$ be finite and continuous on $`[0,1]`$, $`C^3`$ on $`(0,1)`$, and have positive curvature there. Define

```math
A_{ki}(t)=D_{\psi_{ki}}(0,t),\qquad
B_{ki}(t)=D_{\psi_{ki}}(1,t).
```

Then
$`A_{ki}'(t)=t\psi_{ki}''(t)>0`$ and
$`B_{ki}'(t)=-(1-t)\psi_{ki}''(t)<0`$.
The all-truth repair interval for standard $`k`$ is

```math
L_k(t)\leq q\leq U_k(t),
\quad\text{(30)}\quad
```

where

```math
U_k(t)=\left(\sum_iA_{ki}\right)^{-1}
             \left(\sum_iA_{ki}(t_i)\right),
\qquad
L_k(t)=\left(\sum_i(-B_{ki})\right)^{-1}
             \left(\sum_i(-B_{ki}(t_i))\right).
\quad\text{(31)}\quad
```

Both are between $`\min_i t_i`$ and $`\max_i t_i`$. Intermediate truth points add no constraint, since score differences are affine in truth.

### 6.2 The comparison lemma

For strictly increasing $`C^2`$ functions $`a_i,b_i`$ with positive derivatives, define
$`M_a(t)=(\sum_i a_i)^{-1}(\sum_i a_i(t_i))`$, and similarly $`M_b`$.
Then

```math
M_a(t)\leq M_b(t)\quad\text{for every }t
\quad\text{(32)}\quad
```

holds exactly when all ratios $`b_i'(s)/a_i'(s)`$ equal one function $`\rho(s)`$, and $`\rho`$ is nondecreasing.

Here is a direct proof. At a diagonal tuple $`(s,\ldots,s)`$, the difference of the means is zero and has a minimum. Equality of first derivatives gives
$`b_i'/\sum_jb_j'=a_i'/\sum_ja_j'`$, hence the common ratio. For a nonzero direction $`w`$ with $`\sum_i a_i'(s)w_i=0`$, the second derivative of $`M_b-M_a`$ is

```math
\frac{\rho'(s)}{\rho(s)\sum_i a_i'(s)}
\sum_i a_i'(s)w_i^2.
```

It must be nonnegative; such a nonzero direction exists because $`d\geq2`$, so $`\rho'\geq0`$.

For sufficiency, for any $`u,t_i`$ monotonicity gives

```math
b_i(t_i)-b_i(u)
 -\rho(u)\bigl(a_i(t_i)-a_i(u)\bigr)
=\int_u^{t_i}(\rho(s)-\rho(u))a_i'(s)\,ds\geq0.
```

Choose $`u=M_a(t)`$ and sum. The $`a_i`$-terms cancel, so $`\sum_i b_i(t_i)\geq\sum_i b_i(u)`$, which proves (32).

The two-coordinate differential comparison is classical: Páles's signed Remark 5 gives the corresponding criterion [4]. Matkowski's later general-coordinate formulation places these comparisons in a convexity framework [5]. The present use is a scoring-rule application with its hypotheses and normalization made explicit.

### 6.3 Exact rank-one compatibility

Universal local repair first forces the curvature profiles to factor as

```math
\psi_{ki}''(s)=r_k(s)w_i(s),
\qquad r_k(s),w_i(s)>0,
\quad\text{(33)}\quad
```

where the coordinate functions $`w_i`$ are shared across standards. This is the rank-one Hessian-projection condition. Given (33), compare a lower mean $`L_\ell`$ with an upper mean $`U_k`$. The derivative ratio in the comparison lemma is

```math
\rho_{k\ell}(s)=
\frac{s\,r_k(s)}{(1-s)r_\ell(s)}.
\quad\text{(34)}\quad
```

**Theorem 5 — Isolated rank-one criterion.** Under (33), a common weak repair exists for every forecast tuple if and only if, for every pair $`k,\ell`$,

```math
\left|\frac{d}{ds}\log\frac{r_k(s)}{r_\ell(s)}\right|
\leq\frac1{s(1-s)}\qquad(0\lt{}s<1).
\quad\text{(35)}\quad
```

Universal local weak repair along every small transverse direction at every diagonal context is already sufficient to force (33) and (35).

**Proof.** A common interval exists exactly when $`L_\ell(t)\leq U_k(t)`$ for every ordered pair. The lemma makes this equivalent to nondecrease of (34). Applying it in both orders gives (35). Conversely these comparisons make
$`\sup_k L_k(t)\leq\inf_kU_k(t)`$;
both sides lie in the compact interval between the smallest and largest forecast coordinates. Thus even an arbitrary family has a common weak repair.

For the local necessity, a negative first derivative of $`U_k-L_\ell`$ at a diagonal point would rule out repair for every sufficiently small step in the corresponding direction. Applying the same argument to the opposite direction forces the first derivative to vanish and yields (33). A negative second derivative in a nonzero weighted-mean-zero direction would likewise rule out arbitrarily small repair; the second derivative in the comparison lemma then yields (35). These directions are transverse to the diagonal. $`\square`$

No uniform strict margin over an arbitrary family follows from this weak-interval theorem. Also, the theorem concerns an isolated segment; projecting one block out of a coupled truth hull need not preserve its repair problem.

### 6.4 Why pairwise comparison with an anchor can fail here

Take common coordinate weights $`w_i=1`$ and three curvature factors

```math
r_0(s)=1,\qquad
r_+(s)=\frac{s}{1-s},\qquad
r_-(s)=\frac{1-s}{s}.
\quad\text{(36)}\quad
```

Each of $`r_+`$ and $`r_-`$ satisfies (35) with the anchor $`r_0`$, at the boundary of the bound. Their mutual logarithmic derivative has magnitude $`2/[s(1-s)]`$, so they fail it with each other.

There is a direct witness. For $`r_+`$, the lower mean is the root mean square of the coordinates. For $`r_-`$, the upper mean is one minus the root mean square of their complements. At the tuple $`(1/4,3/4)`$, these are
$`\sqrt5/4`$ and $`1-\sqrt5/4`$, respectively. The first exceeds the second. Each standard may have a repair in common with the anchor, while the whole family has none.

The potentials obtained by integrating (36) twice are finite at the endpoints and smooth in the open interval. Their endpoint-singular curvatures must not be used as examples satisfying a theorem that requires a $`C^3`$ potential on an open neighborhood of the whole closed truth hull.

## 7. How much error is unavoidable?

### 7.1 First-order minimax loss for quadratic standards

For finitely many fixed quadratic matrices $`W_k`$, define the signed optimal excess

```math
R(\varepsilon)=
\min_{c\in C}\max_{k,j}
\bigl(L_{W_k}(c,v_j)-L_{W_k}(p+\varepsilon h,v_j)\bigr).
\quad\text{(37)}\quad
```

The smallest nonnegative permissible error is $`\max\{0,R(\varepsilon)\}`$. A negative value of $`R`$ records strict simultaneous improvement and must not be truncated when studying the asymptotics.

**Theorem 6 — First-order incompatibility cost.** The finite linear program

```math
\kappa(h)=
\min_{z\in T}\max_{k,j}
2(p-v_j)^\top W_k(z-h)
\quad\text{(38)}\quad
```

attains a nonnegative value, and

```math
R(\varepsilon)=\varepsilon\kappa(h)+O(\varepsilon^2).
\quad\text{(39)}\quad
```

Moreover, $`\kappa(h)=0`$ if and only if all $`P_{W_k}h`$ agree.

**Proof.** The barycentric average of each standard's linear terms in (38) is zero, so the maximum is nonnegative. A tangent ball in $`C`$ gives, for one anchor matrix,
$`\max_j2(p-v_j)^\top W_0 z\geq2r\,m_{W_0}\|z\|_2`$.
Subtracting the bounded $`h`$-terms proves coercivity and attainment of (38).

Writing $`u=c-p`$, the exact loss excess is

```math
2(p-v_j)^\top W_k(u-\varepsilon h)
 +\|u\|_{W_k}^2-\varepsilon^2\|h\|_{W_k}^2.
\quad\text{(40)}\quad
```

The feasible choice $`c=p`$ gives $`R(\varepsilon)=O(\varepsilon)`$ from above. The same anchor coercivity in (40), with the nonnegative quadratic term retained, forces actual minimizers to have $`u=O(\varepsilon)`$. On this bounded rescaling, (40) is its first-order expression plus a uniform $`O(\varepsilon^2)`$ remainder. Conversely, a minimizing $`z`$ in (38) gives the feasible candidate $`p+\varepsilon z`$ for small $`\varepsilon`$. These two comparisons prove (39).

If $`\kappa=0`$, every displayed linear term at a minimizer is nonpositive. Its positive barycentric average is zero, so every term vanishes, giving $`z=P_{W_k}h`$ for all $`k`$. The converse follows by the same orthogonality. $`\square`$

Thus incompatibility forces $`R(\varepsilon)\geq\kappa\varepsilon/2>0`$ eventually. Compatibility gives the stronger exact bound
$`R(\varepsilon)\leq-\varepsilon^2\min_k\|Q_{W_k}h\|_{W_k}^2<0`$.
Adding a tangent vector to $`h`$ does not change $`\kappa`$. Independent positive rescalings of the losses change its numerical value, although they do not change whether it is zero. General minimax sensitivity theory supplies a wider antecedent; Meitz and Shapiro's Proposition 2.3 is a relevant convex minimax result [7]. The proof here establishes the finite geometric case directly.

For the binary family $`W_\alpha`$, $`\alpha\in[l,u]\subset[0,1]`$, one can compute the whole minimax value. Set $`m=(l+u)/2`$ and now let $`d=(u-l)/2`$ be the **half-width**. For $`0<\varepsilon\leq1/4`$,

```math
t_*=\frac12+m\varepsilon-d\varepsilon^2,
\qquad
R(\varepsilon)=d\varepsilon-m(1-m)\varepsilon^2
 -2md\varepsilon^3+d^2\varepsilon^4.
\quad\text{(41)}\quad
```

Indeed, the worst excess is the maximum of the increasing function
$`t^2-1/4-l\varepsilon(1+\varepsilon)`$
and the decreasing function
$`(1-t)^2-1/4+u\varepsilon(1-\varepsilon)`$.
Their intersection lies in $`[0,1]`$ and gives (41). The formula extends algebraically to degenerate endpoint weights, although those endpoints fall outside the positive-definite hypotheses of Theorems 1 and 6.

### 7.2 Second-order control after first-order compatibility

Let $`F_1,\ldots,F_N`$ be $`C^3`$ on an open convex neighborhood of the entire compact hull $`C`$, with positive-definite Hessians there. Additive separability is not required. Fix a transverse $`h`$, and suppose there is one $`z\in T`$ with

```math
H_k(h-z)\perp T\quad\text{for every }k,
\qquad H_k=\nabla^2F_k(p),\quad K_k=\nabla^3F_k(p).
\quad\text{(42)}\quad
```

Define

```math
\begin{aligned}
E_k&=\frac12\bigl(H_k[h,h]-H_k[z,z]\bigr)
    =\frac12H_k[h-z,h-z]>0,\\
B_{kj}&=E_k+
\frac12\bigl(K_k[p-v_j,h,h]-K_k[p-v_j,z,z]\bigr),\\
A_{kj}(w)&=B_{kj}-H_k[p-v_j,w],\qquad w\in T,\\
\tau_*&=\max_{w\in T}\min_{k,j}A_{kj}(w).
\end{aligned}
\quad\text{(43)}\quad
```

**Theorem 7 — Optimized second-order repair.** The program (43) has a finite attained value. For the actual signed excess

```math
R(\varepsilon)=
\min_{c\in C}\max_{k,j}
\bigl(D_{F_k}(v_j,c)-D_{F_k}(v_j,p+\varepsilon h)\bigr),
```

one has

```math
R(\varepsilon)=-\tau_*\varepsilon^2+o(\varepsilon^2).
\quad\text{(44)}\quad
```

If $`\tau_*>0`$, strict common repair exists for every sufficiently small positive $`\varepsilon`$. If $`\tau_*<0`$, no common weak repair exists there, and no $`o(\varepsilon^2)`$ tolerance can suffice. The case $`\tau_*=0`$ is undecided by (44).

**Proof.** For one anchor standard, the tangent-ball argument gives
$`\max_j H_0[p-v_j,w]\geq c_0\|w\|_2`$, $`c_0>0`$.
Thus $`\min_{k,j}A_{kj}(w)\leq\max_j B_{0j}-c_0\|w\|_2`$, proving attainment and finiteness from above. A barycentric average of $`A_{kj}(w)`$ is $`E_k`$, which is another useful upper bound.

Compactness of $`C`$ gives actual minimizers. The feasible trial $`p+\varepsilon z`$ has excess $`O(\varepsilon^2)`$. Averaging under one standard gives the lower bound $`R(\varepsilon)\geq-D_{F_0}(p,b_\varepsilon)=-O(\varepsilon^2)`$, so $`R=O(\varepsilon^2)`$. Equation (3), together with positive curvature on the compact hull, forces every optimizing $`c_\varepsilon`$ to satisfy $`c_\varepsilon-p=O(\varepsilon)`$.

Set $`x_\varepsilon=c_\varepsilon-p-\varepsilon z\in T`$. Taylor expansion using (42) makes each anchor excess
$`H_0[p-v_j,x_\varepsilon]+O(\varepsilon^2)`$.
Its maximum is $`O(\varepsilon^2)`$, so the same coercivity yields $`x_\varepsilon=O(\varepsilon^2)`$. Actual minimizers therefore have the bounded form

```math
c_\varepsilon=p+\varepsilon z+\varepsilon^2w_\varepsilon,
\qquad w_\varepsilon=O(1).
\quad\text{(45)}\quad
```

Equation (5) now gives, uniformly for bounded $`w`$,

```math
D_{F_k}(v_j,b_\varepsilon)-
D_{F_k}(v_j,p+\varepsilon z+\varepsilon^2w)
=\varepsilon^2A_{kj}(w)+o(\varepsilon^2).
\quad\text{(46)}\quad
```

Using (45) bounds the optimum on one side. Using a maximizing $`w_*`$ from (43), whose corresponding candidate remains in $`C`$ by relative interior, bounds it on the other. This proves (44). The same localization argument applies to any exact-repair sequence, not just optimizers. $`\square`$

The open-neighborhood hypothesis matters. A potential whose Hessian blows up at truth endpoints does not meet this theorem merely because it is smooth at $`p`$.

### 7.3 Finite certificates

Finite-dimensional linear-programming duality gives

```math
\tau_*=
\min_{\lambda}
\sum_{k,j}\lambda_{kj}B_{kj},
\quad\text{(47)}\quad
```

subject to

```math
\lambda_{kj}\geq0,\quad
\sum_{k,j}\lambda_{kj}=1,\quad
\sum_{k,j}\lambda_{kj}H_k[p-v_j,w]=0
\quad\text{for all }w\in T.
\quad\text{(48)}\quad
```

The dual is feasible: put the positive barycentric weights on any one standard. For every feasible $`\lambda`$, averaging cancels the $`w`$-terms, so $`\min_{k,j}A_{kj}(w)\leq\sum\lambda_{kj}B_{kj}`$. The reverse equality follows from the separating-hyperplane theorem for the finite system $`A_{kj}(w)\geq\tau`$; coercivity established above prevents escape of a maximizing sequence.

A positive primal margin and a negative dual value are directly checkable certificates for opposite conclusions. With rational tensors and truth data, these are rational linear programs. This does not make arbitrary smooth generators effectively decidable from unspecified analytic descriptions. Independent positive rescaling preserves the sign classifications, but not a numerical common regret measured in fixed units.

The finite LP certificate body states a stronger inequality than its averaging proof supplies. For nonnegative weights of total mass one, with weighted linear part zero on every tangent vector, τ≤B_i−L_i(w) yields τ≤Σ_i weight_i B_i by weighted summation. Its dual_bound declaration instead concludes τ+1≤Σ_i weight_i B_i, while its calc chain starts at τ and ends at the unshifted weighted value. The singleton instance with weight1, B=0, L=0 and τ=0 satisfies every premise and separates the two conclusions. The later negative-dual corollary invokes this defective declaration; the zero-dual-excludes-strict argument independently uses a positive weight and positive weighted margins, so that ordinary argument does not require the extra unit. This source-local counterexample neither refutes ordinary weak duality nor establishes an observed kernel rejection. [R134-018](../research/t20-v6-20261012/sources/e21eb33ebc6f85a23e45e0bc18af927213e07de156c053b1d9bee83ed5c43344/FiniteLPCertificates.lean#L8-L33) [R134-018](../research/t20-v6-20261012/sources/e21eb33ebc6f85a23e45e0bc18af927213e07de156c053b1d9bee83ed5c43344/FiniteLPCertificates.lean#L35-L59)

## 8. A zero second-order margin does not decide exact repair

Use the diagonal binary segment, the quadratic potential $`G(x,y)=(x^2+y^2)/2`$, and $`F(x,y)=\psi(x)+\psi(y)`$, where

```math
\psi(t)=\frac{z^2}{2}+\frac23z^3+z^4,\qquad z=t-\frac12.
\quad\text{(49)}\quad
```

Its curvature
$`r(t)=1+4z+12z^2=12(z+1/6)^2+2/3`$
is positive on the whole real line. Thus this is a globally regular polynomial example, not an endpoint singularity.

At $`p=(1/2,1/2)`$, $`h=(1,0)`$, the common first-order correction is $`z_h=(1/2,1/2)`$. Write a tangent second-order correction as $`(w,w)`$. The four coefficients in (43), ordered by standard and endpoint truth, are

```math
A_{G,0}=\frac14-w,\quad A_{G,1}=\frac14+w,\quad
A_{F,0}=\frac34-w,\quad A_{F,1}=-\frac14+w.
\quad\text{(50)}\quad
```

Their minimum is maximized at $`w=1/4`$, with $`\tau_*=0`$.

Nevertheless no exact common weak repair exists for $`0<\varepsilon\leq1/100`$. Let

```math
A=\frac{(1/2+\varepsilon)^2+(1/2)^2}{2},
\qquad
u=\frac12+\frac{\varepsilon}{2}
 +\frac{\varepsilon^2}{4}-\frac{\varepsilon^3}{8}.
```

The quadratic comparison at truth zero forces $`q^2\leq A`$. But

```math
u^2-A=
\frac{\varepsilon^3}{64}
\bigl(\varepsilon^3-4\varepsilon^2-4\varepsilon+8\bigr)>0,
```

so $`q<u`$. Define $`L(q)=2D_\psi(1,q)`$. It is strictly decreasing on $`[0,1]`$, because $`L'(q)=-2(1-q)r(q)<0`$ in the interior. Exact expansion gives

```math
L(u)-D_\psi(1,1/2+\varepsilon)-D_\psi(1,1/2)
=\frac{\varepsilon^3}{6144}P(\varepsilon),
\quad\text{(51)}\quad
```

where

```math
\begin{aligned}
P(\varepsilon)={}&2304-17280\varepsilon+4992\varepsilon^2
 +1696\varepsilon^3-2304\varepsilon^4-816\varepsilon^5\\
&+592\varepsilon^6+72\varepsilon^7
 -72\varepsilon^8+9\varepsilon^9.
\end{aligned}
```

For $`0<\varepsilon\leq1/100`$, discard positive terms and bound the four negative terms by their endpoint magnitudes:

```math
P(\varepsilon)\geq
2304-\frac{17280}{100}-\frac{2304}{100^4}
-\frac{816}{100^5}-\frac{72}{100^8}>0.
```

Thus $`L(q)>L(u)`$ already exceeds the disturbed nonlinear loss, a contradiction. The first positive term of this witness is $`3\varepsilon^3/8`$.

For comparison, the globally regular potential

```math
\psi_+(t)=\frac1{16}e^{4(t-1/2)}
\quad\text{(52)}\quad
```

has the same curvature and curvature derivative at $`1/2`$, and hence the same four second-order coefficients (50). Its log-curvature derivative is $`4`$, which satisfies
$`4\leq1/[s(1-s)]`$ on $`(0,1)`$. Theorem 5 gives exact common repair with the quadratic score. For a nonconstant forecast tuple the relevant mean comparisons are strict: the derivative ratio in each ordered comparison is strictly increasing, with at most an isolated zero derivative. Hence a point in the interior of the common interval strictly repairs both standards.

The polynomial and exponential cases have the same first-order projections and the same zero second-order margin at this context, yet opposite exact conclusions. The missing information is not supplied by declaring a zero linear-program value a pass.

## 9. Joint truth structure can restore repair

### 9.1 A polynomial score that fails on an isolated block

For the rest of this section set

```math
\psi(t)=\frac{t^2}{2}+4t^4,\qquad
r(s)=\psi''(s)=1+48s^2.
\quad\text{(53)}\quad
```

Against the unit quadratic score, the isolated diagonal block violates (35) at $`s=1/4`$:

```math
\frac{r'(1/4)}{r(1/4)}=6
>\frac1{(1/4)(3/4)}=\frac{16}{3}.
\quad\text{(54)}\quad
```

There is also an explicit interval of impossibility. Disturb the isolated block to $`(1/4+\varepsilon,1/4)`$, and put

```math
A_\varepsilon=\frac{(1/4+\varepsilon)^2+(1/4)^2}{2},
\qquad
u_\varepsilon=\frac14+\frac{\varepsilon}{2}
 +\frac{13\varepsilon^2}{24}.
```

For $`0<\varepsilon\leq1/100`$, $`0<u_\varepsilon<1`$, and

```math
u_\varepsilon^2-A_\varepsilon
=\frac{\varepsilon^2}{576}
 (169\varepsilon^2+312\varepsilon+12)>0.
\quad\text{(55)}\quad
```

Let $`L(q)=2D_\psi(1,q)`$ and
$`N_\varepsilon=D_\psi(1,1/4+\varepsilon)+D_\psi(1,1/4)`$.
Then

```math
L(u_\varepsilon)-N_\varepsilon
=\frac{\varepsilon^2}{13824}Q(\varepsilon),
\quad\text{(56)}\quad
```

with

```math
Q(\varepsilon)=3456-63360\varepsilon-246864\varepsilon^2
 +41184\varepsilon^3+128440\varepsilon^4
 +105456\varepsilon^5+28561\varepsilon^6.
```

Its value is positive on this interval, since
$`3456-63360/100-246864/10000>0`$.
The quadratic zero-truth constraint $`q^2\leq A_\varepsilon`$ forces $`q<u_\varepsilon`$; strict decrease of $`L`$ then contradicts $`L(q)\leq N_\varepsilon`$. Only these two actual truth comparisons are needed.

The distinct isolated-obstruction body enlarges the premise to 0<ε≤1 but still derives ε²≤1/10000 in both the tail-positivity and envelope-membership proofs. That estimate does not follow: ε=1 is allowed, its stored envelope is 31/24, and its stored tail polynomial equals −3127. The algebraic excess identities and the slope violation remain different claims from this unsupported interval extension. The ordinary proof above retains 0<ε≤1/100; reading the altered body neither broadens that interval nor supplies a compiler rejection or a theorem classifying the remaining ε values. [NEXT250-S25-037](../research/t20-v6-20261012/sources/86087aa9604819cf9afbb780223a5e288a726dab10148dddc711e49b3b991dff/IsolatedObstruction.lean#L19-L39) [NEXT250-S25-037](../research/t20-v6-20261012/sources/86087aa9604819cf9afbb780223a5e288a726dab10148dddc711e49b3b991dff/IsolatedObstruction.lean#L58-L76) [NEXT250-S25-037](../research/t20-v6-20261012/sources/86087aa9604819cf9afbb780223a5e288a726dab10148dddc711e49b3b991dff/IsolatedObstruction.lean#L80-L99)

### 9.2 A coupled conjunction hull

Now keep the same first two coordinate potentials, but couple their truth values to two further propositions. Let $`C_{\wedge}`$ be the convex hull of

```math
(0,0,0,0),\quad(0,0,1,0),\quad
(0,0,0,1),\quad(1,1,1,1).
\quad\text{(57)}\quad
```

The first two coordinates both record the conjunction of the last two truth values. A relative-interior context has the form $`p=(s,s,z,w)`$, with the four positive barycentric weights

```math
1+s-z-w,\quad z-s,\quad w-s,\quad s.
\quad\text{(58)}\quad
```

We use duplicate first coordinates throughout this construction. In the equivalent complementary convention $`(x,y)`$, the affine transformation is $`(t_1,t_2)=(x,1-y)`$; the second transformed disturbance component is the negative of the original $`y`$-direction. Equation (29) has zero remainder for this affine transformation. The directions in the formulas below are the duplicate-coordinate directions.

Use

```math
G(x)=\frac12\sum_{i=1}^4x_i^2,\qquad
F(x)=\psi(x_1)+\psi(x_2)+50x_3^2+50x_4^2.
\quad\text{(59)}\quad
```

Write a disturbance direction as $`h=(h_1,h_2,h_z,h_w)`$ and define

```math
\mu=\frac{h_1+h_2}{2},\quad
e=\frac{(h_1-h_2)^2}{4},\quad
T_0=z+w,\quad A=T_0-2s.
```

Transversality is $`e>0`$. From (58),
$`0<s<1`$, $`0<A<1-s`$, and $`2s<T_0<1+s`$.
Set

```math
\begin{aligned}
\gamma&=\frac{96es^2}{T_0(100-r)},&
\beta&=\frac{48es-100\gamma}{r},\\
\theta&=\frac{9600s^2(T_0-2s)}
 {rT_0(100-r)},&
m_0&=1-\theta,\qquad r=1+48s^2.
\end{aligned}
\quad\text{(60)}\quad
```

The proposed repair is

```math
c_\varepsilon=
\bigl(q,q,z+\varepsilon h_z+\varepsilon^2\gamma,
             w+\varepsilon h_w+\varepsilon^2\gamma\bigr),
\quad
q=s+\varepsilon\mu+\varepsilon^2\beta.
\quad\text{(61)}\quad
```

We will prove $`m_0>0`$, membership in the actual hull, and strict gain under both scores. The whole truth relation (57), not merely its affine equality $`x_1=x_2`$, participates in the proof.

### 9.3 A finite positivity certificate

Define

```math
\begin{aligned}
\Pi(s)&=(1+s)r(s)(100-r(s))-9600s^2(1-s)\\
&=-2304s^5-2304s^4+14304s^3-4896s^2+99s+99.
\end{aligned}
\quad\text{(62)}\quad
```

The following exact Bernstein coefficients prove
$`\Pi(s)\geq132/5`$ on $`[0,1]`$.
On the interval $`j/8\leq s\leq(j+1)/8`$, put $`t=8s-j`$ and use the row in
$`\Pi(s)=\sum_{k=0}^5\binom5k b_k t^k(1-t)^{5-k}`$.

| $`j`$ | $`b_0`$ | $`b_1`$ | $`b_2`$ | $`b_3`$ | $`b_4`$ | $`b_5`$ |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 99 | 4059/40 | 963/10 | 13803/160 | 1185/16 | 7959/128 |
| 1 | 7959/128 | 3219/64 | 3099/80 | 30 | 132/5 | 30 |
| 2 | 30 | 168/5 | 222/5 | 5157/80 | 30591/320 | 17829/128 |
| 3 | 17829/128 | 29277/160 | 38277/160 | 12381/40 | 15801/40 | 993/2 |
| 4 | 993/2 | 23919/40 | 28617/40 | 135939/160 | 160149/160 | 149667/128 |
| 5 | 149667/128 | 428037/320 | 121839/80 | 17253/10 | 1944 | 2178 |
| 6 | 2178 | 2412 | 26613/10 | 46797/16 | 1024293/320 | 446385/128 |
| 7 | 446385/128 | 75477/20 | 651309/160 | 87513/20 | 187437/40 | 4998 |

Each row identity is verified by polynomial expansion. Every coefficient is at least $`132/5`$, and the Bernstein basis is nonnegative and sums to one. This supplies the advertised lower bound without a plot or numerical sampling.

Two further retained sources must be distinguished from these ordinary formulas. PolynomialAND sets ψ(t)=t²/2+3t⁴ but dψ(t)=t+16t³ and r(t)=1+48t²; its derivative proof instead differentiates a quartic with coefficient 4. At (v,t)=(1,0), its defined scalarDiv is 7/2 while its displayed expansion is 9/2. Its separate eight-cell Bernstein certificate therefore does not validate that scalar derivative/score connection. ANDCorrection has a different defect: γ=−96es²/[T(100−r)] although gamma_pos asserts positivity. Under the displayed curvature r(s)=1+48s², the parameter values s=1/4,T=1,e=1 give r=4, γ=−1/16, β=73/16 and θ=25/32, hence leadG(0,0)=−39/32 rather than the claimed 1−θ=7/32. This is a conditional arithmetic comparison, not identification of ANDCorrection's exact imported PolynomialAND body. These exact coefficient and sign variants do not supply the positive-gain construction below and are not silently replaced by its correct formulas. No compiler outcome is asserted. [SUB250-R25-227](../research/t20-v6-20261012/sources/7a64f28f09859dc4718fc4dbef0b032fd936b296e105bb027cf2bfe2a2a17716/PolynomialAND.lean#L141-L162) [SUB250-R25-143](../research/t20-v6-20261012/sources/68b49e71ce0e885b28ade6536ac598926eac030d4be71008eb8f35ee1d005644/ANDCorrection.lean#L9-L18) [SUB250-R25-143](../research/t20-v6-20261012/sources/68b49e71ce0e885b28ade6536ac598926eac030d4be71008eb8f35ee1d005644/ANDCorrection.lean#L66-L138)

The distinct PolynomialAND certificate changes the constant term of P from 99 to 98 without changing any of its eight Bernstein rows. Already at s=0 the first asserted row identity equates 98 with 99. Direct rational expansion of all eight displayed rows gives P+1, not P; each coefficient is still at least 132/5. Thus the valid Bernstein nonnegative-weight argument certifies P≥127/5 on [0,1] after subtracting one, while the submitted proof does not establish its stated 132/5 bound. This diagnoses the proof identity, not falsity of that stronger inequality. Independently, this body’s scalar definitions are mutually consistent: ψ(t)=t²/2+4t⁴, ψ′(t)=t+16t³, curvature 1+48t²>0, and the displayed divergence expansion agree algebraically. Those derivative and curvature arguments survive the certificate-constant defect and are distinct from the earlier coefficient-three scalar mutation. [NEXT250-Z50-231](../research/t20-v6-20261012/sources/a9cdf79a3325a3e8df69e1f13ca285578c1d3904ee8f3e07f493d91cd106782a/PolynomialAND.lean#L9-L33) [NEXT250-Z50-231](../research/t20-v6-20261012/sources/a9cdf79a3325a3e8df69e1f13ca285578c1d3904ee8f3e07f493d91cd106782a/PolynomialAND.lean#L35-L139) [NEXT250-Z50-231](../research/t20-v6-20261012/sources/a9cdf79a3325a3e8df69e1f13ca285578c1d3904ee8f3e07f493d91cd106782a/PolynomialAND.lean#L141-L162)

To deduce $`m_0>0`$, the denominator $`rT_0(100-r)`$ is positive: $`1\leq r<49<100`$. Let $`D=r(100-r)-9600s^2`$. The difference between that denominator and the numerator of $`\theta`$ is
$`T_0D+19200s^3`$.
If $`D\geq0`$, it is positive. If $`D<0`$, write it as
$`\Pi(s)+(T_0-1-s)D`$; both terms are positive. Thus $`\theta<1`$.

### 9.4 Actual gain, feasibility and a usable scale

For a truth in (57), let $`a`$ be its repeated first coordinate and $`j`$ the sum of its last two coordinates. The only possibilities are $`(a,j)=(0,0),(0,1),(1,2)`$. Exact polynomial expansion of the actual Bregman losses gives the following coefficients of $`\varepsilon^2`$ in the gain from (61):

| Truth class $`(a,j)`$ | Quadratic gain coefficient | Nonlinear gain coefficient |
|---|---|---|
| $`(0,0)`$ | $`em_0`$ | $`rem_0`$ |
| $`(0,1)`$ | $`em_0+\gamma`$ | $`rem_0+100\gamma`$ |
| $`(1,2)`$ | $`em_0+\dfrac{96es(T_0-2s)}{rT_0}`$ | $`rem_0`$ |

For clarity, before substituting (60), these coefficients are

```math
\begin{aligned}
\Gamma_G(a,j)
 &=e-2(s-a)\beta+(j-T_0)\gamma,\\
\Gamma_F(a,j)
 &=re+(s-a)(96se-2r\beta)+100(j-T_0)\gamma.
\end{aligned}
\quad\text{(63)}\quad
```

Substitution and elementary cancellation give the table. All coefficients are strictly positive.
These are coefficients of real score differences: the identity

```math
D_\psi(v,t)=\frac{(v-t)^2}{2}+4v^4+12t^4-16vt^3
\quad\text{(64)}\quad
```

shows that every gain is exactly $`\varepsilon^2\Gamma+\varepsilon^3R(\varepsilon)`$, with a polynomial remainder. No assumed remainder sign is needed.

Membership is equally concrete. Substitute (61) into the four affine expressions (58). Each resulting weight is its strictly positive original value plus a linear and a quadratic term in $`\varepsilon`$; their sum remains one, and their convex combination of the four actual truths is $`c_\varepsilon`$. They remain positive for sufficiently small $`\varepsilon`$.

An explicit local scale can be extracted from the same formulas. Let $`M`$ be the sum of the absolute coefficients of all finitely many remainder polynomials, so $`|R(\varepsilon)|\leq M`$ for $`0\leq\varepsilon\leq1`$. Let $`b_0`$ be the smallest original weight in (58), and $`L`$ the sum of the absolute linear and quadratic coefficients in their changes. Let $`p_0=\min_i\{p_i,1-p_i\}>0`$, and $`H=1+\sum_i|h_i|`$. It suffices to take

```math
0<\varepsilon<
\min\left\{1,\frac{em_0}{2(M+1)},
\frac{b_0}{2(L+1)},\frac{p_0}{2H}\right\}.
\quad\text{(65)}\quad
```

The gains are then at least $`em_0\varepsilon^2/2`$, the barycentric weights stay positive, and the disturbed forecast stays in the open cube. Thus the coupled hull admits strict common repair at every interior context and every transverse direction, although the isolated repeated block fails (54).

The retained ExplicitANDScale variant attempts a finite arithmetic radius for twenty constraints, covering both score gains, four barycentric weights and both sides of the input cube. Its second-order barycentric vector is written (β−γ,γ−β,γ−β,β), whose sum is γ. Expanding the first weight 1+c₀−c₂−c₃ instead requires β−2γ, which the later bary_identity proof itself writes inside a change step. For γ≠0 the stored coefficient and that expansion differ by γ, so the claimed identity differs by ε²γ. The remainder budgets and positive-radius argument depend on that identity and do not repair it. This local mismatch is separate from any imported gain or potential discrepancy; it supplies neither a checked explicit radius for these bytes nor an observed compiler result. [SUB250-R25-156](../research/t20-v6-20261012/sources/6bd44acd67a281113b32f11b9ede88c1de33269b5697c181cd008f137fb958b7/ExplicitANDScale.lean#L22-L62) [SUB250-R25-156](../research/t20-v6-20261012/sources/6bd44acd67a281113b32f11b9ede88c1de33269b5697c181cd008f137fb958b7/ExplicitANDScale.lean#L120-L172)

The separate rational scale-control body uses the corrected second-order barycentric vector (β−2γ,γ−β,γ−β,β), whose entries sum to zero. It also specifies one simultaneous radius for its twenty constraints. For positive heads Hᵢ, nonnegative remainder budgets Bᵢ and bounds |Rᵢ(ε)|≤Bᵢ on 0≤ε≤1, set δ=1/(1+Σᵢ 2(Bᵢ+1)/Hᵢ). Then 0<δ<1 and δ<Hᵢ/[2(Bᵢ+1)] for every i, so 0<ε<δ implies Hᵢ+εRᵢ(ε)>Hᵢ/2. Absolute coefficient sums supply such bounds for the displayed remainder polynomials on that interval. This is an elementary conditional radius argument, not an inference of the positive-head premises or oracle identities from sampled cases. The imported polynomial oracle was not read, the finite tests were not executed, and the output’s claim of separate kernel checking was not independently verified. The corrected vector in this Python body therefore neither repairs the retained Lean variant nor changes its recorded limitation. [AFTER2384-EIGHTH25-196](../research/t20-v6-20261012/sources/bdfe797c506bad4b4d4009ec561d0f845f3b0672293ea74f1c1d588610603770/scale_checks.py#L7-L20) [AFTER2384-EIGHTH25-196](../research/t20-v6-20261012/sources/bdfe797c506bad4b4d4009ec561d0f845f3b0672293ea74f1c1d588610603770/scale_checks.py#L31-L47)

### 9.5 Removing the free-coordinate explanation

The preceding four-coordinate example has free singleton directions in its tangent space. The phenomenon persists when every coordinate belongs to a constrained block.

Let $`C_{\mathrm c}\subset\mathbb R^6`$ be the convex hull of the six truth vectors

```math
\begin{aligned}
v_0&=(1,1,1,1,0,0),&
v_1&=(0,0,1,0,1,0),&
v_2&=(0,0,1,0,0,1),\\
v_3&=(0,0,0,1,1,0),&
v_4&=(0,0,0,1,0,1),&
v_5&=(0,0,0,0,1,1).
\end{aligned}
\quad\text{(66)}\quad
```

Its affine hull is $`x_1=x_2`$, $`\sum_{i=3}^6x_i=2`$, with tangent

```math
T=\{d:d_1=d_2,\ d_3+d_4+d_5+d_6=0\}.
\quad\text{(67)}\quad
```

For an explicit spanning verification, any $`d\in T`$ has coefficients

```math
\bigl(d_1,\ 0,\ d_3-d_1,\
d_5-d_1+d_3+d_4,\
-d_5-d_3,\
d_1-d_3-d_4\bigr)
\quad\text{(68)}\quad
```

whose sum is zero and whose combination of (66) is $`d`$. The two dependency blocks are $`\{1,2\}`$, of tangent rank one, and $`\{3,4,5,6\}`$, of tangent rank three. The duplicate-pair vector and the high-coordinate differences generate their elementary supports. No coordinate axis belongs to $`T`$.

Use

```math
G(x)=\frac12\sum_{i=1}^6x_i^2,\qquad
F(x)=\psi(x_1)+\psi(x_2)+50\sum_{i=3}^6x_i^2.
\quad\text{(69)}\quad
```

For $`p=(s,s,z,w,u,v)\in\mathrm{ri}C_{\mathrm c}`$, positive weights on (66) give
$`s>0`$, $`z>s`$, $`w>s`$, $`z+w<1+s`$, and all coordinates in $`(0,1)`$. Put

```math
\mu=\frac{h_1+h_2}{2},\quad
e=\frac{(h_1-h_2)^2}{4},\quad
k=\frac{h_3+h_4+h_5+h_6}{4},\quad E_H=2k^2.
```

The common Hessian projection is

```math
z_h=(\mu,\mu,h_3-k,h_4-k,h_5-k,h_6-k).
\quad\text{(70)}\quad
```

Indeed, its residual has opposite first-pair entries and equal high entries; both the Euclidean Hessian and $`\mathrm{diag}(r,r,100,100,100,100)`$ make it normal to (67).

Use $`\beta,\gamma`$ from (60), with $`T_0=z+w`$, and take

```math
c_\varepsilon=p+\varepsilon z_h+
\varepsilon^2(\beta,\beta,\gamma/2,\gamma/2,-\gamma/2,-\gamma/2).
\quad\text{(71)}\quad
```

Its actual gains have coefficients $`\Gamma_G(a,j)+E_H`$ and $`\Gamma_F(a,j)+100E_H`$, where $`\Gamma`$ is (63) and $`(a,j)`$ again runs through the three classes. If $`e>0`$, the previous positive table applies. If $`e=0`$, then $`\beta=\gamma=0`$; transversality means $`k\ne0`$, and the gains are exactly $`2k^2\varepsilon^2`$ and $`200k^2\varepsilon^2`$. Thus purely high-block disturbances are included, even with an arbitrary tangent component.

The retained MixedScore gain formulas do not both match this balanced construction. Its nonlinear gain includes 100·normalEnergy(h), while its quadratic gain omits normalEnergy(h). For the ordinary candidate (71), set h=(0,0,1,1,1,1) and β=γ=0: its projected direction is zero, the quadratic gain is exactly2ε² at every listed truth, but the displayed gainG right side is zero. This comparison is conditional on the balanced candidate used here; the file imports candidateWith from MixedHull, whose exact dependency body is not identified or rechecked by this reading. Nor is that import silently identified with the separate defective MixedHull variant. Thus the displayed formula cannot serve as a fresh verification of the ordinary high-block energy term. Its derivative interfaces likewise retain their imported polynomial-score dependencies. [SUB250-R25-178](../research/t20-v6-20261012/sources/6fed542205f6b2d5de42ecc0b3e9f3887668da7c3dd48f8bda413b7bb6347097/MixedScore.lean#L12-L44) [SUB250-R25-178](../research/t20-v6-20261012/sources/6fed542205f6b2d5de42ecc0b3e9f3887668da7c3dd48f8bda413b7bb6347097/MixedScore.lean#L100-L134)

To prove actual hull membership, choose the strictly positive barycentric weights $`\alpha_i`$ of $`p`$ supplied by (1). Apply (68) to $`d=c_\varepsilon-p`$, which lies in $`T`$. Adding those coefficients to $`\alpha_i`$ preserves their sum, reconstructs $`c_\varepsilon`$, and keeps every weight positive for small $`\varepsilon`$. Polynomial remainders and a finite positive leading margin then prove:

The retained MixedHull variant does not implement the balanced second-order correction in (71). In its zero-based coordinates 2,3,4,5 it adds (+γ/2,+γ/2,+γ/2,−γ/2)ε², so the high-coordinate sum of its displacement is γε² rather than zero. Every listed truth has high-coordinate sum two. For an interior p and fixed γ≠0, every nonzero ε therefore places that candidate outside the affine hull, contradicting its asserted arbitrary-parameter tangency and neighborhood membership. The coefficient reconstruction and positive-weight argument require the missing tangent equation and cannot repair the sign by themselves. The balanced formula above remains the mathematical construction; this exact source supplies neither its verification nor an observed compiler result. [SUB250-R17-077](../research/t20-v6-20261012/sources/5d61de60254b1791c18d40b05ef86ee13d2e91d245ac5cf92c599deee914dac5/MixedHull.lean#L12-L55) [SUB250-R17-077](../research/t20-v6-20261012/sources/5d61de60254b1791c18d40b05ef86ee13d2e91d245ac5cf92c599deee914dac5/MixedHull.lean#L87-L120)

**Theorem 8 — Mixed-rank coupled repair.** For every $`p\in\mathrm{ri}C_{\mathrm c}`$ and every $`h\notin T`$, (71) is a strict common repair under (69) for every sufficiently small positive $`\varepsilon`$, with the disturbed forecast still in the open cube.

The theorem does not contradict Theorem 4: there is a constrained rank-one block. It does show that repair on that block cannot in general be decided after discarding its joint truth relations with a higher-rank block.

### 9.6 The product hull has the opposite answer

Let $`C_{\mathrm p}`$ instead be the product of the duplicate segment and the hypersimplex
$`\Delta(2,4)=\{y\in[0,1]^4:\sum_i y_i=2\}`$.
Its twelve truths independently choose $`(a,a)`$, $`a\in\{0,1\}`$, and any high vector with exactly two ones. Keep the complete ambient score functions (69).

At

```math
p=(1/4,1/4,1/2,1/2,1/2,1/2),
\qquad h=(1,0,0,0,0,0),
\quad\text{(72)}\quad
```

no common weak repair exists for $`0<\varepsilon\leq1/100`$. To see this using actual product truths, take the two high truth vectors $`y^+=(1,1,0,0)`$ and $`y^-=(0,0,1,1)`$. Their average is the high block of $`p`$.

For any proposed repair $`(q,q,z,w,u,v)`$, define
$`S=(z-1/2)^2+(w-1/2)^2+(u-1/2)^2+(v-1/2)^2\geq0`$.
Average the two quadratic comparisons at truths $`(0,0,y^\pm)`$. They force

```math
q^2-A_\varepsilon+\frac S2\leq0.
```

Average the two nonlinear comparisons at $`(1,1,y^\pm)`$. They force

```math
L(q)-N_\varepsilon+50S\leq0.
```

Hence $`q^2\leq A_\varepsilon`$ and $`L(q)\leq N_\varepsilon`$, contradicting (55)–(56). This averaging is essential: the interior high-block point $`(1/2,1/2,1/2,1/2)`$ is not itself one of the listed Boolean truths. Four genuine product-state inequalities, not a fictitious extra truth, establish impossibility.

Both hulls have the same affine hull, tangent, dependency blocks and block projections. Their shared context (72) is in each relative interior. For $`C_{\mathrm c}`$, positive weights are
$`(1/4,1/8,1/8,1/8,1/8,1/4)`$.
For $`C_{\mathrm p}`$, give each of the six zero-flag truths weight $`1/8`$ and each of the six one-flag truths weight $`1/24`$.
The whole ambient score maps agree, so every derivative at $`p`$ agrees too. What differs is the admissible joint list of truth arguments.

### 9.7 Exact second-order values distinguish the hulls

The same example has compact rational primal and dual certificates. With (72), the common first direction is $`z_h=(1/2,1/2,0,0,0,0)`$. For a truth with repeated flag $`a`$, put

```math
A_G(v,w)=\frac14-(p-v)\cdot w,\qquad
A_F(v,w)=\frac52-6a-
\mathrm{diag}(4,4,100,100,100,100)[p-v,w].
\quad\text{(73)}\quad
```

Here the diagonal expression denotes its bilinear form. These are exactly the coefficients (43), obtained from the actual potentials (69), not separately chosen linear data.

For the coupled hull, the tangent correction

```math
w_{\mathrm c}=(12/41,12/41,3/328,3/328,-3/328,-3/328)
```

has every coefficient at least $`7/82`$. Substitution into the three truth classes verifies the lower bound. For every ambient $`w`$, the identity

```math
\frac{100}{123}A_G(v_5,w)
+\frac{11}{123}A_F(v_5,w)
+\frac{12}{123}A_F(v_0,w)=\frac7{82}
\quad\text{(74)}\quad
```

gives the matching dual bound. Thus $`\tau_{\mathrm c}=7/82`$.

The distinct coupling-certificate body changes the first two coordinates of coupledCorrection from 12/41 to 13/41 while retaining the claimed common margin 7/82. At the ordinary truth v5=(0,0,0,0,1,1), its displayed coefficientG is 1/4−13/82−3/164=3/41, strictly below 7/82. Thus that vector cannot supply the stated primal lower bound for the ordinary six-truth problem. The dual upper-bound identity, product-vector declarations and actual-gain binding formulas are separate interfaces; their presence does not repair the changed primal witness. This comparison leaves the ordinary 12/41 optimizer and its proof intact and asserts neither a fresh import check nor compiler rejection. [NEXT250-S25-031](../research/t20-v6-20261012/sources/8561f1f65ce4946a500c0d094ac813e24f0d9548c60f8b0407161a6c0bb0b414/CouplingLPValues.lean#L10-L18) [NEXT250-S25-031](../research/t20-v6-20261012/sources/8561f1f65ce4946a500c0d094ac813e24f0d9548c60f8b0407161a6c0bb0b414/CouplingLPValues.lean#L27-L56) [NEXT250-S25-031](../research/t20-v6-20261012/sources/8561f1f65ce4946a500c0d094ac813e24f0d9548c60f8b0407161a6c0bb0b414/CouplingLPValues.lean#L58-L89) [NEXT250-S25-031](../research/t20-v6-20261012/sources/8561f1f65ce4946a500c0d094ac813e24f0d9548c60f8b0407161a6c0bb0b414/CouplingLPValues.lean#L115-L144)

For the product hull, $`w_{\mathrm p}=(15/26,15/26,0,0,0,0)`$ gives every coefficient at least $`-1/26`$. Let $`v_{a,+}=(a,a,1,1,0,0)`$, $`v_{a,-}=(a,a,0,0,1,1)`$. The dual identity is

```math
\frac6{13}A_G(v_{0,+},w)+\frac6{13}A_G(v_{0,-},w)
+\frac1{26}A_F(v_{1,+},w)+\frac1{26}A_F(v_{1,-},w)
=-\frac1{26}.
\quad\text{(75)}\quad
```

The coefficients in each identity are nonnegative and sum to one; the $`w`$-terms cancel. Therefore $`\tau_{\mathrm p}=-1/26`$. Theorem 7 consequently gives signed optimal excesses
$`-7\varepsilon^2/82+o(\varepsilon^2)`$ and
$`\varepsilon^2/26+o(\varepsilon^2)`$, respectively. The explicit interval proof in Section 9.6 does not depend on these asymptotics.

**Corollary — A joint-hull representation obstruction.** No decision rule given only the common context and disturbance, affine and tangent geometry, separate block projections, and the complete ambient score functions can correctly decide local common repair for every instance in a class containing both $`C_{\mathrm c}`$ and $`C_{\mathrm p}`$.

The inputs just listed are identical in the two instances, but their correct feasibility answers differ. A representation adequate for both must retain the relevant joint truth constraints or information that distinguishes them. This does not identify a unique minimal representation, prove that every joint moment is necessary, or establish a cognitive realization of either truth family.

<a id="geometric-radius-and-verification-scope"></a>

### 9.8 An existential radius and a literal arithmetic certificate

The common-repair conclusion and its usable scale have different quantifiers. A result of the form “for every admitted context and direction there exists a positive radius” does not supply one radius uniform over all contexts and directions. Formula (65) displays that dependence through the actual leading gain, remainder, barycentric and coordinate bounds. A literal arithmetic certificate for the four-coordinate example is a separate strengthening at its specified inputs; it does not automatically strengthen the general mixed-rank theorem. The mixed-rank and explicit-scale audit guides expressly preserve this distinction. [GUIDE105-G023] [GUIDE105-G040]

A valid radius must control actual losses and actual membership inequalities together. A leading positive quadratic coefficient alone is insufficient if its remainder or an admissible-hull boundary is not controlled. The explicit-scale guide reports exact rational evaluation of all twenty actual constraints and a copied polynomial oracle as a test helper. It makes no general runtime-refinement claim for that helper. The specific fixture and its arithmetic proof are not supplied by the guide, so no additional numerical radius is inferred here. The directly readable coefficient argument in §§9.3–9.4 retains its own complete proof.

The direct polynomial sources give a rowwise alternative to (65). Use five groups of four constraints: the two normalized gain factors, the four candidate barycentric weights, and the lower and upper coordinate margins of the disturbed forecast. Each has the exact form $`a_j+\varepsilon R_j(\varepsilon)`$, with $`a_j>0`$. Use the following coefficient budgets $`M_j`$ on $`0\leq\varepsilon\leq1`$:

| Constraint group | Constant term $`a_j`$ | Remainder and budget |
|---|---|---|
| Quadratic gain factor | $`\Gamma_G`$ from (63) | $`R_G`$ from the exact gain identity; sum of its absolute coefficients |
| Nonlinear gain factor | $`\Gamma_F`$ from (63) | $`R_F`$ from the exact gain identity; sum of its absolute coefficients |
| Candidate barycentric weight | Original weight $`\lambda_i`$ in (58) | $`\lambda_i^{(1)}+\varepsilon\lambda_i^{(2)}`$; budget $`\lvert\lambda_i^{(1)}\rvert+\lvert\lambda_i^{(2)}\rvert`$ |
| Lower input-cube margin | $`p_i`$ | $`h_i`$; budget $`\lvert h_i\rvert`$ |
| Upper input-cube margin | $`1-p_i`$ | $`-h_i`$; budget $`\lvert h_i\rvert`$ |

Here $`\lambda_i^{(1)}`$ and $`\lambda_i^{(2)}`$ are the linear and quadratic coefficients obtained by substituting (61) into (58). In that order they are

```math
\begin{aligned}
\lambda^{(1)}&=(\mu-h_z-h_w,\ h_z-\mu,\ h_w-\mu,\ \mu),\\
\lambda^{(2)}&=(\beta-2\gamma,\ \gamma-\beta,\ \gamma-\beta,\ \beta).
\end{aligned}
```

The absolute coefficient sum bounds each polynomial remainder on this interval. Define

```math
\delta_{20}=\frac{1}{1+\sum_{j=1}^{20}2(M_j+1)/a_j}.
```

Then $`0<\delta_{20}\leq1`$ and $`\delta_{20}<a_j/[2(M_j+1)]`$ for every row. Consequently, if $`0<\varepsilon<\delta_{20}`$,

```math
a_j+\varepsilon R_j(\varepsilon)
\geq a_j-\varepsilon M_j>\frac{a_j}{2}>0.
```

The two actual gains are these positive factors multiplied by $`\varepsilon^2`$. The other rows give positive candidate weights and an input in the open cube; positive weights on the four truths also put the candidate in the open cube. This proves the stated repair for the same interior context and transverse direction. The construction is finite arithmetic for rational inputs. It is a sufficient, input-dependent radius, without an optimality, uniformity or mixed-rank extension claim. The direct coefficient, radius and twenty-row binding proofs are in [PolynomialBounds][formal-rowwise-budgets], [ConstraintBounds][formal-rowwise-radius] and [ExplicitANDScale][formal-twenty-row-repair].

One exact polynomial-bound source must be distinguished from this absolute-budget argument: its `budget` definition sums signed coefficients, although its nonnegativity and absolute-value proof scripts use absolute summands. A single coefficient −1 already separates those quantities. Its independently stated strict-gain implication still explicitly requires a nonnegative remainder budget and the displayed small-scale bound. This is a discrepancy in that exact source body, not in the absolute-coefficient argument above, and no compiler rejection is reported. [Baseline141-68](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/0dea756ab9e040ca57587e3017bb52993bec6fa720694ffa48daf99e6fa3ac2a/PolynomialBounds.lean)

ConstraintBounds has a different scale discrepancy. Its radius is 1/(1+Σ_j 2(B_j+1)head_j), while radius_lt_each reasons with division by head_j to obtain radius<head_j/[2(B_j+1)]. Positivity and radius≤1 do not imply that stronger row bound. For one row with head=1/10 and B=1, the written radius is 5/7. Taking ε=1/5 and constant remainder −1 meets the displayed remainder assumptions but gives head+ε·remainder=−1/10, despite ε being inside that radius. The reciprocal-head construction above must therefore remain distinct from this variant; the source's positive_inside_radius conclusion cannot be promoted through the mismatched formula, and no compiler rejection is being reported. [A750-T50-141](../research/t20-v6-20261012/sources/c829255dc7fb762efb5b296bd46fce0871ffddc4b36b30682eb8a997c71b28ca/ConstraintBounds.lean#L10-L49) [A750-T50-141](../research/t20-v6-20261012/sources/c829255dc7fb762efb5b296bd46fce0871ffddc4b36b30682eb8a997c71b28ca/ConstraintBounds.lean#L52-L65)

For the data $`(s,z,w,h_1,h_2,h_z,h_w)=(1/4,1/2,1/2,1,0,0,0)`$, the [companion scale-audit source][formal-scale-fixture] states $`\delta_{20}=31562496/25265441833`$ and contains an arithmetic proof script. This records the source's fixture claim; no new kernel execution or independent numerical evaluation is asserted.


The geometry-boundary guide also separates proof layers. Its kernel scope covers the critical-zero and finite linear-programming certificates, boundary readback and exact primal/dual binding. The mixed-rank extension and exponential positive comparator are ordinary results at that earlier seal; their later formalization and the full-jet flat-perturbation work have separate identities. An earlier seal cannot be retroactively described as certifying those later additions. [GUIDE105-G044]

The unsuccessful auditor normalization attempts and the deliberately rejected mutations are retained historical failures. They do not count as accepted source qualification. General optimized-regret asymptotics remain ordinary mathematics where the guide says so. These records add evidence boundaries to the existing positive constructions and obstructions; they do not alter the source proofs or create another common-repair result from the number of successful build modules. [GUIDE105-G023] [GUIDE105-G040] [GUIDE105-G044]


## 10. An obstruction invisible to the full Taylor data

The joint-hull example changes the truth constraints while preserving the whole score functions. A different obstruction keeps the truth hull fixed and changes the generators by a smooth perturbation that is flat at the coherent context.

### 10.1 Two globally smooth positive-curvature potentials

Let $`s_0=1/2`$. Choose a smooth cutoff $`0\leq\chi\leq1`$, equal to one on an interval $`I`$ around $`s_0`$, with support contained in $`(1/4,3/4)`$. Define

```math
r_0(s)=1+\chi(s)\left(\frac{s}{1-s}-1\right),
```

with the expression extended by $`1`$ outside the support. It is positive and $`C^\infty`$ on the real line. On $`I`$ it is exactly $`s/(1-s)`$. Put

```math
h(s)=
\begin{cases}
0,&s\leq s_0,\\
\exp\bigl(-1/(s-s_0)^2\bigr),&s>s_0,
\end{cases}
\qquad
r_1(s)=r_0(s)e^{h(s)}.
\quad\text{(76)}\quad
```

The function $`h`$ and all its derivatives vanish at $`s_0`$, while it is strictly increasing to its right. Integrate $`r_0,r_1`$ twice to obtain potentials $`\psi_0,\psi_1`$, normalized by
$`\psi_i(s_0)=\psi_i'(s_0)=0`$.
Both are globally smooth with positive curvature, and every derivative of $`\psi_0`$ and $`\psi_1`$ agrees at $`s_0`$.

On the diagonal segment compare the same quadratic potential $`G(x,y)=(x^2+y^2)/2`$ with, separately,
$`F_i(x,y)=\psi_i(x)+\psi_i(y)`$.

### 10.2 Exact common repair for the unperturbed potential

For $`t_1,t_2\in I`$, let

```math
q=\sqrt{\frac{t_1^2+t_2^2}{2}}.
\quad\text{(77)}\quad
```

This lies between $`t_1,t_2`$, hence in $`I`$. For the quadratic score, the truth-zero loss is unchanged, while truth-one loss decreases because the root mean square is at least the arithmetic mean.

For $`B_0(t)=D_{\psi_0}(1,t)`$, one has $`B_0'(t)=-t`$ on $`I`$, so $`B_0(t)=C_0-t^2/2`$. The nonlinear truth-one loss is therefore also unchanged by (77). For $`A_0(t)=D_{\psi_0}(0,t)`$, the derivative of $`u\mapsto A_0(\sqrt u)`$ is $`r_0(\sqrt u)/2`$, which is increasing. Jensen's inequality shows that the truth-zero loss does not increase.

Thus (77) is a common weak repair. Its signed optimal worst excess is exactly zero. Any smaller coherent $`q`$ worsens the nonlinear truth-one loss; any larger one worsens the quadratic truth-zero loss. These comparisons also exclude candidates outside $`I`$, using global monotonicity of the endpoint loss.

### 10.3 No exact common repair after the flat perturbation

Take the ray $`t_1=s_0`$, $`t_2=s_0+\varepsilon`$, for small $`\varepsilon>0`$. Put

```math
u_0=t_1^2,\quad u_1=t_2^2,\quad
m=\frac{u_0+u_1}{2}.
```

The quadratic truth-zero constraint requires $`q^2\leq m`$. For
$`B_1(t)=D_{\psi_1}(1,t)`$, equation (76) gives

```math
B_1(t)=C_1-\frac12K(t^2),
\qquad K'(u)=e^{h(\sqrt u)}
\quad\text{(78)}\quad
```

on the relevant interval. The derivative $`K'`$ is strictly increasing for $`u>u_0`$, so $`K`$ is strictly convex there. The nonlinear truth-one constraint would require

```math
K(q^2)\geq\frac{K(u_0)+K(u_1)}2>K(m),
\quad\text{(79)}\quad
```

contradicting $`q^2\leq m`$. A candidate $`q\leq s_0`$ also fails, since the strictly decreasing $`B_1`$ then exceeds the average of its values at $`s_0`$ and $`s_0+\varepsilon`$. All remaining possible candidates lie in the local interval on which (78) holds. Thus there is no common weak repair.

### 10.4 Positive obstruction smaller than every power

Let $`R_1(\varepsilon)`$ be the signed minimax excess under $`G,F_1`$. Continuity on the compact coherent segment guarantees attainment. Since no weak repair exists,
$`R_1(\varepsilon)>0`$.
At the old root-mean-square candidate $`q=\sqrt m`$, every comparison except the nonlinear truth-one comparison remains nonpositive. For the nonlinear truth-zero comparison this follows again from Jensen: $`r_1`$ is increasing on the local interval.

The only positive excess is

```math
J_\varepsilon=
\frac{K(u_0)+K(u_1)}2-K(m).
```

Write $`L=u_1-u_0=\varepsilon+\varepsilon^2`$. On this interval,
$`1\leq K'(u)\leq e^{h(s_0+\varepsilon)}`$, so

```math
0\lt{}R_1(\varepsilon)\leq J_\varepsilon
\leq\frac L2\left(e^{h(s_0+\varepsilon)}-1\right)
\leq(\varepsilon+\varepsilon^2)e^{-1/\varepsilon^2}
\quad\text{(80)}\quad
```

for sufficiently small $`\varepsilon`$. In particular, $`R_1(\varepsilon)=o(\varepsilon^N)`$ for every fixed $`N`$, while it remains strictly positive. For the unperturbed pair, $`R_0(\varepsilon)=0`$.

The generators have the same full Taylor data at the coherent context, but exact repair differs. One qualification is essential: the uncentered losses $`D_{\psi_i}(v,t)`$ can differ in their constant truth terms $`\psi_i(v)`$. The losses actually relevant to the repair decision can be centered:

```math
\widetilde D_{\psi_i}(v,t)
=D_{\psi_i}(v,t)-D_{\psi_i}(v,s_0).
\quad\text{(81)}\quad
```

These centered losses have the same entire forecast jet at $`s_0`$, including their values, and centering does not alter any repair comparison.

**Theorem 9 — Smooth jet data do not decide exact local repair.** In the class of smooth positive-curvature scoring problems, even the complete jets of the generators, or of the centered truth losses, at a coherent context do not determine whether exact common repair exists nearby. Every tolerance bounded below by a positive polynomial power eventually absorbs the particular obstruction (80).

This does not assert that the optimized regret is itself differentiable to all orders. The point is its size bound and exact positivity. Nor does it identify a smooth jet with a function germ: distinct smooth germs can share a jet.

For real-analytic germs, the full Taylor series determines the local function, so this particular full-jet ambiguity is unavailable. A fixed finite jet remains insufficient without further restrictions. Replacing the flat $`h`$, near $`s_0`$, by $`(s-s_0)^{2m}`$ preserves any prescribed finite collection of derivatives when $`m`$ is large enough, while the strict-convexity argument on the positive ray still supplies failure. The resulting germs are analytic near $`s_0`$; the global cutoff extension is smooth, and no claim of analyticity on the whole truth neighborhood is being substituted. A known finite polynomial-degree bound is additional information and can make finitely many coefficients determine a polynomial.

## 11. Interpretation and unresolved scope

The results separate three levels of information. First-order curvature identifies which corrections can agree to sublinear accuracy. On higher-rank additive blocks, compatibility across every coherent context forces a strong exact relationship between standards. On rank-one blocks, the admissible relationship is wider and is governed by endpoint-mean comparison. Beyond those classifications, exact repair can depend on the joint truth constraints and on information invisible to finite, or even infinite smooth, Taylor data at one point.

These distinctions constrain applications to rational revision, recognition and restoration. A mechanism that observes only marginals or a local metric cannot be assumed to implement every shared improvement available under a richer truth model. A successful repair can also reveal information about relative scoring weights, as Section 2.4 demonstrates. Neither conclusion identifies which weights have objective authority, or establishes that an agent has cognitively adopted a particular representation. Mathematical feasibility, a proposed interpretation, empirical implementation and justified normativity remain distinct claims.

Several questions remain outside the proved scope:

- At a boundary coherent context, tangent-cone geometry replaces the relative-interior arguments. The positive-weight and tangent-ball proofs cannot simply be reused.
- The higher-rank theorem does not classify arbitrary coupled hulls with rank-one blocks. The polynomial example proves that isolated-block classification alone is insufficient.
- A zero second-order margin requires further information. The present counterexamples rule out a universal decision from that margin; they do not characterize every zero-margin analytic problem.
- Infinite families with only local Hessian agreement need additional uniformity hypotheses for a common tolerance or strict margin. The exact anchor theorem and rank-one interval theorem use stronger global structure.
- The representation obstructions do not determine a unique minimal sufficient description, nor do they prove that a proposed noetic field, differential model or cognitive process realizes these finite structures.

The exposition preserves both positive constructions and negative results. The fact that one representation is insufficient is not a replacement proof of a different philosophical or scientific conclusion.

## 12. References and verification scope

### 12.1 Primary literature

1. L. M. Bregman. “The relaxation method of finding the common point of convex sets and its application to the solution of problems in convex programming.” U.S.S.R. Computational Mathematics and Mathematical Physics 7(3), 200–217 (1967). [DOI and publication record][1].
2. R. T. Rockafellar. “The elementary vectors of a subspace of $`R^n`$.” In Combinatorial Mathematics and its Applications, edited by R. C. Bose and T. A. Dowling, University of North Carolina Press, 104–127 (1969). [Author-hosted text][2].
3. Graham Denham. “Toric and tropical compactifications of hyperplane complements.” Annales de la Faculté des Sciences de Toulouse, série 6, 23(2), 297–333 (2014), Proposition 2.12. [Author's preprint][3].
4. Zsolt Páles. Signed Remark 5 in “Report of Meeting: The Second Debrecen–Katowice Winter Seminar on Functional Equations and Inequalities.” Annales Mathematicae Silesianae 16 (2003), printed 97–99. [Primary report, theorem and proof][4].
5. Janusz Matkowski. “Generalized weighted quasi-arithmetic means and the Kolmogorov–Nagumo theorem.” Colloquium Mathematicum 133(1) (2013), Section 5, Remark 3, printed 45–46. [Primary article][5].
6. Jason Konek. “Degrees of incoherence, Dutch bookability & guidance value.” Philosophical Studies 180, 395–428 (2023; first published online 2022). [Publication record][6]; [accepted author manuscript][konek-manuscript].
7. Mika Meitz and Alexander Shapiro. “Minimax asymptotics.” arXiv:2504.11269v1 (2025), Proposition 2.3. [Primary preprint][7].
8. Frank Nielsen. “Curved representational Bregman divergences and their applications.” arXiv:2504.05654v5, Sections 2 and 4. [Primary preprint][8].

**Nearest-result attribution.** The received [primary-literature comparison][literature-scope] identifies several antecedents that constrain interpretation of the results. [Joyce, *Accuracy and Coherence*](https://fitelson.org/topics/joyce_2009.pdf), §§10–12, already distinguishes one dominator for each legitimate score from a dominator common to all scores. [Schervish, Seidenfeld and Kadane, *Proper Scoring Rules, Dominated Forecasts, and Coherence*](https://www.stat.cmu.edu/tr/tr865/tr865.pdf) supplies the single-score dominance/coherence ancestry with explicit regularity and boundary distinctions. That report is theirs, not Predd's. The separate [Predd and collaborators paper, *Probabilistic Coherence and Proper Scoring Rules*](https://www.princeton.edu/~kulkarni/Papers/Journals/j071_2009_PreSeirLieOshKulPoo_TransIT.pdf), establishes the Bregman-projection mechanism used in single-score coherent dominance. Common-correction quantifiers and projection sufficiency are therefore not introduced here.

[Leitgeb and Pettigrew, *An Objective Justification of Bayesianism I*](https://fitelson.org/coherence/leitgeb_pettigrew.pdf), derives score restrictions under its Euclidean inaccuracy conditions; the present compatibility classification does not independently select the quadratic form. [Pettigrew, *Aggregating Incoherent Agents Who Disagree*](https://doi.org/10.1007/s11229-017-1613-7), gives the complementary-symmetry condition in the published Theorem 12(iii), and his [2018 replies](https://research-information.bris.ac.uk/files/165202389/PPR_replies.pdf), manuscript p. 16 and footnote 8, give the arithmetic correction for complementary binary forecasts. The binary quadratic/log example in §4.3 is a specialization of that prior mechanism. The latter argument's convex forecast losses must not be conflated with mere convexity of the Bregman generator.

Two differently scoped comparisons also matter. [Forbes, *Compatible Weighted Proper Scoring Rules*](https://arxiv.org/pdf/1311.1131), studies compatibility of baseline maximization, which is not the common statewise coherent-endpoint condition used here. [Kelley, *A Contextual Accuracy Dominance Argument for Probabilism*](https://doi.org/10.1111/phpr.70098), treats arbitrary opinion sets through scorable contexts; the finite-dimensional local theorems here do not subsume that programme. These bibliographic comparisons retain the received review's exact distinctions and edition cautions. The comparison records a pending check of Konek's published correction and distinguishes Pettigrew's published theorem numbering from the earlier draft; it does not supply a completed new collation of either. They are not a new systematic primary-literature review or a certificate of global originality.

### 12.2 Public mathematical predecessors

The following citations identify the public mathematical source edition underlying this exposition. Their historical filenames authenticate the sources; the definitions, proofs and scientific organization of this chapter stand on their own.

- [Quadratic local repair and quantitative identification][quadratic] and [dependency-weight rigidity][dependency] support Sections 1–3.
- [Smooth categorical rigidity][categorical], [general higher-rank blocks][blocks], and [the fixed-anchor family theorem][anchor] support Section 4.
- [Local approximate equivalence][approximate], [common nudges and endpoint separation][nudges], [the context-dependent-standard counterexample][fixed-standard], and [faithful transport][transport] support Section 5.
- [The independent rank-one proof and attribution review][rank-one-review] supports the mean-comparison reconciliation in Section 6. The complete proof is reproduced above; this citation is not a claim to have received every earlier original manuscript cited within that review.
- [First-order minimax repair][first-order], [second-order repair and its dual][second-order], and [the critical-zero counterexample][critical-zero] support Sections 7–8.
- [The polynomial coupled construction][polynomial-construction], [the mixed-rank development][mixed-rank], [its independent correction review][mixed-review], and [the joint-hull representation corollary][joint-hull] support Section 9.
- [The smooth full-jet obstruction][full-jet] supports Section 10.

These references are public source editions, not substitutes for independent scholarly review of the present exposition. Historical statements about an original proof packet retain their original scope; they do not establish fresh receipt or fresh execution of an unavailable packet.

### 12.3 Inspectable formal dependencies

The following received Lean sources provide formal statements and proofs for the finite polynomial constructions and their exact algebraic controls:

| Mathematical role | Source and identifying result |
|---|---|
| Positive weights for every listed truth | [Finite barycentric bridge][formal-barycentric], `FiniteHullWeights.intrinsicInterior_positive_barycentric` |
| Curvature, actual divergence and finite positivity table | [Polynomial identities][formal-polynomial], `PolynomialAND.certificateP_lower` and scalarDiv_expansion |
| Positive correction coefficients | [Correction proof][formal-correction], `ANDCorrection.all_leading_positive` |
| Actual four-coordinate gains and hull weights | [Score identities][formal-score], `ANDScore.g_gain_identity`, f_gain_identity and hull_of_inequalities |
| Isolated quartic impossibility on a rational interval | [Isolated obstruction][formal-isolated], `IsolatedObstruction.no_isolated_common_repair` |
| Six-coordinate membership | [Mixed hull][formal-hull], `MixedHull.candidate_eventually_mem` |
| Genuine derivatives and nonlinear gains | [Mixed score][formal-mixed-score], `MixedScore.potentialF_hasFDerivAt`, gainG and gainF |
| Universal mixed-rank strict repair | [Mixed repair][formal-repair], `MixedRepair.universal_strict_Bregman_repair` |
| Tangent, Hessian normals and absence of free coordinates | [Mixed geometry][formal-geometry], `MixedGeometry.span_directions_eq`, common_hessian_normal and no_free_coordinate |
| Four actual product-truth impossibility | [Product obstruction][formal-product], ProductObstruction.no_product_four_tests |
| Rational optimal margins and actual gain binding | [Coupling certificates][formal-lp], `CouplingLPValues.coupled_primal`, coupled_dual_upper, product_primal, product_dual_upper, coefficientG_binding and coefficientF_binding |

The source bodies have been inspected in preparing this exposition. No new kernel execution or complete formalization of all the general smooth theorems is asserted here. The formal dependencies and independent review records retain their own evidential roles; incorporating a prose argument does not by itself justify removing them.

The [geometry proof review][geometry-proof-review], [finite-hull review][finite-hull-review], [nudge review][nudge-review] and [smooth robustness review][smooth-robustness-review] supply separate checks on orientation, finite truth populations, universal-versus-pointwise quantifiers and sublinear tolerance. Their proof explanations and countercontrols are incorporated at the relevant arguments above. The [formalization scope][formalization-scope] distinguishes particular kernel targets from the ordinary diagonal-stabilizer and higher-rank classification arguments. Historical successful compilation, mutation rejection or finite-enumeration reports concern those original targets and receipts. They do not establish that this assembled exposition has been executed, nor that every general theorem or philosophical application is kernel-certified.

[1]: https://doi.org/10.1016/0041-5553(67)90040-7
[2]: https://sites.math.washington.edu/~rtr/papers/rtr020-ElemVectors.pdf
[3]: https://arxiv.org/html/1306.3519v1
[4]: https://journals.us.edu.pl/index.php/AMSIL/article/download/14111/10836/40243
[5]: https://www.impan.pl/shop/publication/transaction/download/product/87225
[6]: https://link.springer.com/article/10.1007/s11098-022-01860-z
[konek-manuscript]: https://research-information.bris.ac.uk/ws/portalfiles/portal/336592657/Staffel_Comments.pdf
[7]: https://arxiv.org/html/2504.11269v1
[8]: https://arxiv.org/html/2504.05654v5


[quadratic]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/a9eb8521054eb3769ff424037f438ae38f0f0c113d73624efc9d05dea3b35483.md
[dependency]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/55dc1c64cb207d0a4425ec989aab9c94a65490bda4191814fa4a055d5e148aab.md
[categorical]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be.md
[blocks]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/fbf8481b03ad278b916bebf337cf340f44597697764f7e9a6fffe219f2707805.md
[anchor]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/edb8d215fa5d1aa568c596d749385b42710030e9ff3215347cdaec5185f0e854.md
[approximate]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/c08f6d75254247a8c68f49f6b4e88bedc510790c38e9d7f8c493281eafc5c418.md
[nudges]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/1a5d94a8d7a2bca031de09dafcb3fc929797b94488d10836ddb696b0e6a1be0d.md
[fixed-standard]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/0113c7c7e1e78bd51645e77ee3646c856faac79f178e9b5760285c28aeeceac2.md
[transport]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/752593a77fa180409da3bf6aa55816508362669bb055233a79ba775cd55bdd5a.md
[first-order]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/a972fc4836f42db0ca2275134ba70388eb52b7e8e53937dac969995907f052ce.md
[second-order]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/9fea0e2238e657472dd44f65855fb07db1022f26f3f3484d83221ef40bcbb9a4.md
[critical-zero]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/9c6025d6b5bdedaf238a6294e5801470756cdbf213c1696f91007fd0844ae5af.md
[mixed-rank]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/6b108a747a7674bd09ee0c34995cf877185913c270a15102ba7c0b3e9391b543.md
[full-jet]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/7b8487cdf0e216631e0277a879cf8b869ea59c47f1c0fda2058341d1c191070f.md
[rank-one-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/2fcb5545ef8694c1ddb5f0c7af321fde0c5a4f5acd6fe79153864c876ee0d9bf.md
[polynomial-construction]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/a14075e3fedc4c137316f41aea04d48e361eeddbb68a6883d1957d54c15cf664/POLYNOMIAL_AND_KERNEL_TARGET.md
[mixed-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/9c5817df2c8f6f2d0ed3fbbb172b1e924349ab0ca9c0a2414e5dead1b481e643/MIXED_RANK_REVIEW.md
[joint-hull]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/research-v6/root_math/geometry_audit_annex/JOINT_HULL_OBSTRUCTION.md
[formal-barycentric]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/ac0ed23555915fcd324b9aa575cc5acde4d57cbcbe4edacd0ef6b64665f33ef5.lean
[formal-polynomial]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/3c1721046ecb48ff4b4d1d9bde2e483cfa6ed532b69009bbd02c27ed8d9a36a5.lean
[formal-correction]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/9b040710b99321214095e434c1096b3caa1e9135e1a2bde4bf7e09eee473be94.lean
[formal-score]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/684841d865cfddb7e9f8db226a7405c39c01ed53888f8e9535906f97465ff125.lean
[formal-isolated]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/46a16f9a1886a206ec371e328c8fd2e1f0a76aa060b03889aaae00efc4c1463e.lean
[formal-hull]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/0ffac3a36170239eff7abe256d1d6cad3efdced877c284f0e09fe94cc7e27e56.lean
[formal-mixed-score]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/a7bf5cbb8651eed6571b1f3cd7aff586a0640c9eeff4b99594e2fadace16690a.lean
[formal-repair]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/2a6e62d40b426e0760d2307494c7c4abb028c680c8e888a314314c79d9f10bac.lean
[formal-geometry]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/6aed37421110678ab4ce732ee00ba61dc97397ffadc5f16941169309d1ccc44e.lean
[formal-product]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/eb26c550b7ab1aaa3f74a29ffe945d8d00c84913b0cb8b588b3f88420b89bc13.lean
[formal-lp]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/bcbdbaca18e8c2f5ab3c25e38b19587b128e215719ae3d9fc7823d7823935ed2.lean

[formal-rowwise-budgets]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/c26354ffa7da15f07620f32c208bd5afef75ec5e26d0be4a535621aa25e9c6f6.lean
[formal-rowwise-radius]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/446be356118af1bc2ea8af2adedbfdd3c861172169a6e9261a537349d8210247.lean
[formal-twenty-row-repair]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/5800709b1381958aaa2e30ae8ca0da34fb2af1df6fafe1200b65d37183eacca9.lean
[formal-scale-fixture]: https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/experiments/orthemology-v5-continuations/source-store/48480e64f691652b5204acb7fcf07a895513d952a2889ff5c9858a922893b9ba.lean


[approximate-iff-source]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/e46c8d347ed1864c6c65270b0b7e90eef0146815804bb9f783fa465cd3fbc8bc.md
[block-classification-pre-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/b0ec9163de7f6deb49f44bb10ef1f279151ee78a30b9d2dd7ca9736d8bb62750.md
[geometry-proof-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/4f3d54cd93718e479f1485c182058bcd5ee40c13e4b9f598e4a011e6a92adaa0.md
[finite-hull-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/3efb043df2749e965a70ae815003952d0f7e3c1d203d4e04e04e24fd0892a20c.md
[hull-interface-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/5c9fcd3012d9c41bc951cf78e2ccc29591ab8151a0037e6cd0ff07cabb0e54f4.md
[nudge-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/36bf84b786280660b3ec4a5e3a110f04d98598cdbe49e7680a438de344a0dd06.md
[smooth-robustness-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/1fa9f620cbab16c728d931520d777e8ef25090c52520dca39144ed43e2790459.md
[root-cold-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/51c98ce4cbc011f1e4d4d2af7fa9a34319f53713b876977bc9b16c74f0e258dc.md
[formalization-scope]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e.md
[literature-scope]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/45ffbb9679d23bd16a43b4930ec615bb55f4c0c56705e5a0c90f0fec425a2a3e.md
[source-bridge-synthesis]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/21f9e48328bfbf843b5f0371168f84c51768dec6260b3798fca4a461900aa006.md


## Source guides for the additional arguments and qualifications

These exact public guides identify the reported results, historical review scopes and dependencies used in the additional discussion. A guide citation does not claim receipt or renewed verification of every linked proof, primary source or execution record.

- [GUIDE105-G023] Mixed rank kernel successor audit.
- [GUIDE105-G040] Explicit polynomial scale audit.
- [GUIDE105-G044] Geometry boundary delta audit.

[GUIDE105-G023]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/39510850bf6cce0af6b35f98367240015afad94db5eebe5c4fa5db60f79dbb8b/README.md
[GUIDE105-G040]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/726ce66e66d1b1ab39571baf9009b4ee7803e8b1fa9b1a39a3ed58c94cdfdf1f/README.md
[GUIDE105-G044]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/805e6b3b36cb6b4c25efbcd76e4e93dac970ce31deaa0ae2b9e86558e82e589d/README.md
