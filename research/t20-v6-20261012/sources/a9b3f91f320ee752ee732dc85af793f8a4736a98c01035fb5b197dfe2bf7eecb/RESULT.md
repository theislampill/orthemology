# Nonseparable Bayes-compatible Bregman repair

9 October 2026 UTC. Separate T20 mathematical continuation. Ordinary written proof and exact executable controls only; no protected source, product implementation, release state, or closure claim is changed.

## 1. Decisive result and scope

On the full strictly positive cone, first-argument Bregman projection onto the probability simplex is ordinary normalization exactly when the generator is a perspective of its coherent-state restriction plus a function of total mass:

\[
F(sp)=s f(p)+a(s),\qquad f=F|_{\Delta^\circ},\quad a(1)=0.
\]

Thus the previously proved common-negative-entropy uniqueness is a **separable-generator theorem**, not a restriction on the coherent scoring geometry of every Bayes-compatible Bregman repair. Every differentiable strictly convex simplex potential admits such a strictly convex extension by choosing any differentiable strictly convex radial function. With positive-definite tangent Hessian and positive radial second derivative, the inherited full-Hessian correction is radial and converges globally forward to the normalized state.

The concrete example

\[
F_0(b)=\frac{\|b\|^2}{2\sum_i b_i}+\frac12\left(\sum_i b_i\right)^2
\]

has the Brier/squared-Euclidean divergence on coherent states, is strictly convex with positive-definite Hessian on the positive cone, and implements ordinary normalization. This does not contradict the older quadratic countermodel: that countermodel uses the different ambient extension \(\|b\|^2/2\).

The proof below first treats the full cone and then **separately proves** the open-box counterpart. It does not infer a full-cone result from likelihood attenuations of coherent priors alone. Strict convexity is kept separate from Hessian invertibility. Reversing the projection orientation is checked explicitly and does not supply the converse theorem.

## 2. Definitions and hypotheses

Fix \(n\ge2\). Write

\[
C=\mathbb R_{++}^n,\qquad
\Delta^\circ=\{p\in C:\mathbf1^Tp=1\},\qquad
T=\{v:\mathbf1^Tv=0\}.
\]

For \(b\in C\), put \(s=\mathbf1^Tb\) and \(N(b)=p=b/s\). Assume \(F:C\to\mathbb R\) is \(C^1\) and strictly convex. Use the first-argument convention

\[
D_F(x,y)=F(x)-F(y)-\nabla F(y)^T(x-y).
\]

The normalization-projection property means that, for every \(b\in C\), \(N(b)\) is the unique minimizer of \(q\mapsto D_F(q,b)\) over \(\Delta^\circ\). This formulation does not assume that an arbitrary generator has a minimizer on the open simplex.

When projection onto the **closed** simplex or finite losses at vertices are desired, additionally assume that \(f=F|_{\Delta^\circ}\) extends continuously and finitely to \(\Delta\). Define \(F(q)=\bar f(q)\) for the boundary first argument only. Then the closed-simplex objective is continuous on a compact set and has a minimizer. The theorem shows that its unique minimizer is the same strictly positive \(N(b)\). No derivative at a vertex is needed for \(D_F(e_i,b)\), since the differentiated argument is \(b\).

A finite boundary **first** argument does not automatically permit a boundary **second** argument. Gradients at zero coordinates need not exist. Consequently the learning formulas here assume positive likelihoods and interior reports; zero-likelihood posteriors require a separately defined extended divergence or additional boundary differentiability. The concrete quadratic perspective is smooth on the nonnegative cone away from the origin, but this is not asserted for every potential.

For a differentiable potential \(f\) on the affine simplex, its derivative \(df_p\) is intrinsically a linear functional on \(T\), and

\[
D_f(r,p)=f(r)-f(p)-df_p(r-p).
\]

All uses of \(D_f\) respect this intrinsic convention. For \(C^2\) claims, the Hessian \(\operatorname{Hess}f(p)\) is the Hessian on that affine space.

## 3. Full-cone classification

### Theorem 1

Under the \(C^1\), strict-convexity hypotheses above, the following are equivalent:

1. For every \(b\in C\), the first-argument simplex minimizer is \(N(b)\).
2. For every \(p\in\Delta^\circ\), \(s>0\), and \(v\in T\),
   \[
   (\nabla F(sp)-\nabla F(p))^Tv=0.
   \]
3. There is a \(C^1\) function \(a:(0,\infty)\to\mathbb R\), with \(a(1)=0\), such that
   \[
   F(sp)=s f(p)+a(s),\qquad f=F|_{\Delta^\circ}.
   \]

With the literal choice \(f=F|_{\Delta^\circ}\), the function \(a\) is unique.

#### Proof: projection gives the normal-gradient condition

For fixed \(b=sp\), the feasible point \(p\) is interior relative to the affine simplex. First-order optimality in every tangent direction gives

\[
(\nabla F(p)-\nabla F(sp))^Tv=0\quad(v\in T).
\]

This uses the gradient in the first argument of the stated divergence; the orientation has not been swapped. Conversely, this stationarity condition is sufficient because \(q\mapsto F(q)-\nabla F(b)^Tq\) is strictly convex on the simplex. Thus 1 and 2 are equivalent.

#### Proof: the normal-gradient condition gives the representation

Fix \(s>0\). On the connected simplex define

\[
G_s(p)=F(sp)-sF(p).
\]

Its directional derivative is

\[
dG_s(p)[v]=s(\nabla F(sp)-\nabla F(p))^Tv=0\quad(v\in T).
\]

Any two simplex points are joined by a line segment within \(\Delta^\circ\). Integrating the zero directional derivative along that segment shows that \(G_s\) is constant. Fix the barycenter \(u=\mathbf1/n\) and define

\[
a(s)=F(su)-sF(u).
\]

This gives the representation, \(C^1\) regularity, \(a(1)=0\), and uniqueness.

#### Proof: the representation gives projection

For \(h\in\mathbb R^n\), set \(\tau=\mathbf1^Th\) and \(v=h-p\tau\in T\). Differentiating the representation gives

\[
dF_{sp}(h)=df_p(v)+(f(p)+a'(s))\tau.\tag{1}
\]

For tangent \(h\), this is \(df_p(h)\), independent of \(s\). Consequently condition 2 holds, and its already proved sufficiency gives 1. Alternatively, the divergence decomposition in Section 5 proves global minimization directly. \(\square\)

### Boundary justification

The continuous extension \(\bar f\) is convex on \(\Delta\), as follows by taking limits of interior convexity inequalities. For interior \(p\) and any distinct boundary \(r\), the supporting inequality is strict:

\[
\bar f(r)> f(p)+df_p(r-p).
\]

If equality held, convexity and the supporting inequality would force equality along the entire segment from \(p\) to \(r\), contradicting strict convexity on its interior portion. Hence the normalized interior point uniquely minimizes even over the closed simplex. This does not require strict convexity along every boundary face as a separate assumption.

### Affine gauges

Adding \(\ell^Tb+c\) to \(F\) leaves its Bregman divergence unchanged. With the literal restriction convention, it changes

\[
f(p)\mapsto f(p)+\ell^Tp+c,\qquad
a(s)\mapsto a(s)+c(1-s).
\]

The normalization \(a(1)=0\) persists. In particular, for the displayed \(F_0\), the literal restriction is \(f_0(p)=\|p\|^2/2+1/2\), and the matching radial term is \(a_0(s)=(s^2-s)/2\). Choosing \(f(p)=\|p\|^2/2\) instead and \(a(s)=(s^2-1)/2\) produces \(F_0-1/2\), which has exactly the same divergence.

## 4. Exact convexity and Hessian criteria

### Proposition 2: strict convexity

For a function represented as in Theorem 1, \(F\) is strictly convex on \(C\) **if and only if** both \(f\) on \(\Delta^\circ\) and \(a\) on \((0,\infty)\) are strictly convex.

Necessity follows by restricting \(F\) to the simplex and to any ray \(s\mapsto sp\): on a ray the term \(sf(p)\) is affine.

For sufficiency, take \(b=sp\), \(c=tq\), and \(0<\theta<1\). Set \(r=\theta s+(1-\theta)t\) and \(\alpha=\theta s/r\). Their convex combination is \(r(\alpha p+(1-\alpha)q)\). Convexity of \(f\) and \(a\) gives

\[
F(\theta b+(1-\theta)c)
\le\theta s f(p)+(1-\theta)t f(q)+\theta a(s)+(1-\theta)a(t).
\]

If \(p\ne q\), the \(f\) inequality is strict. If \(p=q\) and \(b\ne c\), then \(s\ne t\), and the \(a\) inequality is strict. This proves the claim. The same argument with non-strict inequalities gives the convexity equivalence. \(\square\)

This proves that **any \(C^1\) strictly convex coherent potential can be extended** into the classified full-cone family. If finite vertex scores are required, take a coherent potential with a finite continuous boundary extension.

### Proposition 3: full Hessian

Assume \(f,a\) are \(C^2\). For \(b=sp\), \(h\in\mathbb R^n\), \(\tau=\mathbf1^Th\), and \(v=h-p\tau\),

\[
h^TH_F(b)h
=\frac1s\operatorname{Hess}f(p)[v,v]+a''(s)\tau^2.\tag{2}
\]

To verify this, differentiate along \(b+\epsilon h\). At zero,

\[
s'=\tau,\qquad p'=v/s,\qquad p''=-2\tau v/s^2.
\]

In the second derivative of \(sf(p)\), the two first-derivative terms \(2\tau df_p(p')\) and \(sdf_p(p'')\) cancel. The remaining term is the displayed tangent Hessian term, and \(a(s)\) contributes \(a''(s)\tau^2\).

The decomposition \(h\leftrightarrow(v,\tau)\) is a linear bijection between \(\mathbb R^n\) and \(T\times\mathbb R\). Therefore

\[
H_F(b)\succ0
\iff \operatorname{Hess}f(p)|_T\succ0\ \text{and}\ a''(s)>0.\tag{3}
\]

By polarization of (2),

\[
H_F(sp)p=a''(s)\mathbf1,
\qquad H_F(sp)^{-1}\mathbf1=\frac{p}{a''(s)}\quad\text{when (3) holds}.\tag{4}
\]

In mass/simplex coordinates, writing \(db=p\,ds+s\,dp\), equation (2) gives the Hessian metric

\[
g_F=a''(s)\,ds^2+s\,\operatorname{Hess}f(p)[dp,dp],
\]

with zero mixed radial/tangent term. This is a geometric orthogonality statement, not statistical independence of categorical coordinates.

Strict convexity of a \(C^2\) function does **not** imply (3). For example, with \(f(p)=\|p\|^2/2\) and \(a(s)=(s-1)^4\), both functions and hence \(F\) are strictly convex, but the radial Hessian vanishes at \(s=1\). Inverse-Hessian conclusions require (3) separately.

## 5. Exact divergence and scoring split

For \(x=sp\), \(y=tq\), formula (1) evaluated at \(y\) gives

\[
dF_y(x-y)=s\,df_q(p-q)+(f(q)+a'(t))(s-t).
\]

Subtracting this from \(F(x)-F(y)\) proves

\[
\boxed{D_F(sp,tq)=sD_f(p,q)+D_a(s,t)},\tag{5}
\]

where \(D_a(s,t)=a(s)-a(t)-a'(t)(s-t)\). In particular, for \(r\in\Delta^\circ\), or \(r\in\Delta\) when the boundary extension exists,

\[
D_F(r,sp)=D_f(r,p)+D_a(1,s).\tag{6}
\]

Thus normalization removes an outcome-independent mass penalty. The statewise repair credit is exactly

\[
D_F(e_i,b)-D_F(e_i,N(b))=D_a(1,s)=D_F(N(b),b).\tag{7}
\]

The coherent divergence and associated proper score depend on \(f\), whereas the off-simplex mass penalty depends on \(a\). For \(r,p\in\Delta^\circ\), with the finite vertex first arguments supplied by the boundary extension,

\[
\sum_i r_iD_F(e_i,p)
=\sum_i r_iD_f(e_i,r)+D_f(r,p).
\]

This is the familiar strict-propriety identity. It does not justify a prior, channel, or actual truth linkage.

The perspective portion of (5) is a specialization of the published scaled Bregman identity (Section 12). The radial addition follows from the linearity of the divergence in its generator. Here it also supplies a direct independent algebraic check of the projection proof.

## 6. Bayes semantics and the precise quantifiers

For a positive likelihood vector \(L\), define \(B_L(p)=N(L\odot p)\). Every generator in the classified family satisfies

\[
P_F(L\odot b)=N(L\odot b)=B_L(P_F(b)).\tag{8}
\]

Consequently it also satisfies the older weak order-composition contract. As in the earlier separable theorem, for a simplex retraction defined on the whole declared domain, **all-input scalar neutrality**

\[
P_F(cb)=P_F(b),\qquad 0<c\le1,
\]

implies \(P_F(b)=N(b)\): compare \(b\) with \(N(b)\), scaling whichever has the larger mass downward. Conversely, normalization gives neutrality and strong Bayes equivariance. These statements use only admissible arguments in the domain.

However, testing only

\[
P_F(cp)=p\qquad(p\in\Delta^\circ,\ 0<c\le1)
\]

probes masses at most one. Without separability, this is **insufficient to force the global cone or box classifier**. Section 9 gives an exact strictly convex counterexample that passes every such attenuation test and nevertheless fails normalization at a point of \((0,1)^2\) with mass greater than one. The old separable corollary had extra structural content and remains intact.

For a genuinely specified finite channel and prior, the previous information-minus-implementation-regret identities still apply, now with coherent divergence \(D_f\). This family makes the implementation-regret term zero for positive ordinary likelihood updates, independently of whether \(f\) is entropy or quadratic. It does not remove misspecification, provenance, conditional-dependence, evidence-access, or warrant obligations.

## 7. Constructive global full-Hessian correction

Assume the positive-definite conditions (3) everywhere. Consider the inherited canonical correction field

\[
\dot b=-(s-1)H_F(b)^{-1}\mathbf1.\tag{9}
\]

For a classified generator, (4) reduces it exactly to

\[
\dot b=-\frac{s-1}{a''(s)}p,\qquad
\dot s=-\frac{s-1}{a''(s)},\qquad
\dot p=0.\tag{10}
\]

Thus the full-Hessian path stays on the ray through its input, and its endpoint is the same ordinary normalization implemented by the projection. This correction repairs total mass only and preserves all relative beliefs. Evidence-driven discrimination still requires the separately justified likelihood action; a richer generator does not discover a true prior or correct relative belief by itself.

### Global forward existence, uniqueness, and convergence with only \(C^2\)

If \(s_0=1\), the unique forward solution is constant. If \(s_0\ne1\), let \(I\) be the compact interval joining \(s_0\) and 1. Since \(a''\) is positive and continuous, there exist \(0<m\le M<\infty\) bounding it on \(I\). The scalar field points toward 1 and never leaves \(I\).

Away from 1, separation of variables defines a unique solution through a strictly monotone time integral. The time to reach 1 is infinite because the integrand is \(a''(u)/|u-1|\), whose integral diverges using the lower bound \(m>0\). Hence the solution exists for every forward time, stays positive, and satisfies

\[
|s_0-1|e^{-\tau/m}\le |s(\tau)-1|
\le |s_0-1|e^{-\tau/M}.\tag{11}
\]

In particular \(s(\tau)\to1\) and \(b(\tau)\to p_0=N(b_0)\). At the equilibrium a solution cannot depart in forward time because the field points strictly toward it on both sides; this gives uniqueness there without assuming a third derivative or local Lipschitz regularity of \(a''\).

For every truth-state vertex with finite score,

\[
\frac{d}{d\tau}D_F(e_i,b(\tau))=-(s(\tau)-1)^2.\tag{12}
\]

Indeed, \(\nabla_bD_F(e_i,b)=H_F(b)(b-e_i)\), and substitution of (9) gives (12). This derivative identity is **inherited and generic** for that field whenever the Hessian is invertible; it is not specific to this classifier. The additional result here is the radial reduction, the admissible full-Hessian family, and the global endpoint proof.

Equations (6) and (10) also give the exact integrated accounting

\[
\int_0^\infty(s(\tau)-1)^2\,d\tau=D_a(1,s_0).
\]

If \(a''=1\), then \(s(\tau)=1+(s_0-1)e^{-\tau}\). In contrast, the strictly convex but Hessian-degenerate example \(a(s)=(s-1)^4\) gives, away from 1,

\[
\dot s=-\frac{1}{12(s-1)},\qquad
(s(\tau)-1)^2=(s_0-1)^2-\tau/6.
\]

It reaches the singular mass in finite time \(6(s_0-1)^2\), where the inverse-Hessian field is undefined. This is an explicit negative control against dropping condition (3).

## 8. Concrete Brier-compatible repair

For \(F_0(b)=\|b\|^2/(2s)+s^2/2\),

\[
\nabla F_0(b)=p-\frac12\|p\|^2\mathbf1+s\mathbf1,
\]

and

\[
H_{F_0}(b)=\frac{I}{s}
-\frac{b\mathbf1^T+\mathbf1b^T}{s^2}
+\frac{\|b\|^2}{s^3}\mathbf1\mathbf1^T
+\mathbf1\mathbf1^T.
\]

The Hessian quadratic form is \(\|h-p\mathbf1^Th\|^2/s+(\mathbf1^Th)^2\), hence positive definite. Off-diagonal entries are not identically zero; for \(b=(3/8,1/8)\) the Hessian is

\[
\begin{pmatrix}5/4&1/4\\1/4&13/4\end{pmatrix}.
\]

This verifies that the extension is genuinely nonseparable. Its divergence is

\[
D_{F_0}(sp,tq)=\frac{s}{2}\|p-q\|^2+\frac12(s-t)^2.\tag{13}
\]

For the older independent-channel example, take prior \(p=(3/4,1/4)\) and either null likelihood \(L=(1/2,1/2)\). The raw vector is \(b=(3/8,1/8)\). The new repair returns \(p\), with zero posterior regret, coherent expected score \(3/16\), and identical raw-to-repaired score reduction \(1/8\) in both truth states. The old ambient Euclidean repair returns \((5/8,3/8)\), with expected score \(13/64\) and regret \(1/64\). Both ambient generators give exactly the same Brier-type loss on the simplex. In fact the affine-equivalent choice \(F_{\rm new}(b)=\|b\|^2/(2s)+(s-1)^2/2\) agrees **in value** with \(F_{\rm old}(b)=\|b\|^2/2\) on the entire simplex, since \(F_{\rm new}=F_0-s+1/2\). Thus even the same coherent potential values, proper scores, and tangent Hessian data do not determine a Bayes-compatible ambient repair extension. Their distinct off-simplex extensions explain the difference. Raw off-simplex scores from the different generators are not being equated.

As a positive informative-channel control, let \(L_+=(4/5,1/5)\) and \(L_-=(1/5,4/5)\). The outcome probabilities are \(13/20\) and \(7/20\), with posteriors \((12/13,1/13)\) and \((3/7,4/7)\). The extension implements both exactly. Expected posterior Brier loss is \(12/91\), and the gain from prior loss \(3/16\) is \(81/1456\), equal to the corresponding expected coherent Bregman information term. These are declared finite models, not empirical or psychological evidence.

## 9. Orientation and attenuation negative control

Every classified generator also happens to have normalized **reverse** projection, because (5) gives

\[
D_F(b,r)=sD_f(p,r)+D_a(s,1),\qquad r\in\Delta^\circ,
\]

which has its unique minimum at \(r=p\). This agreement does not mean that reversing the orientation preserves the characterization.

In dimension two define the globally \(C^3\), strictly convex function

\[
\widetilde F(b)=F_0(b)+(2b_1+b_2-2)_+^4,
\qquad u_+=\max\{u,0\}.
\]

The added term is convex, being a convex nondecreasing fourth power of a positive part composed with an affine function. The positive-definite Hessian of \(F_0\) is therefore preserved. The added value and gradient vanish everywhere on the simplex, including its boundary. Hence, as a function of the simplex **second** argument, \(D_{\widetilde F}(b,r)\) differs from \(D_{F_0}(b,r)\) only by the constant \(\widetilde F(b)-F_0(b)\). Its reverse projection is normalization for every \(b\).

The perturbation also vanishes with its gradient whenever \(s\le1\), because \(2b_1+b_2\le2s\le2\). Thus it passes all null attenuations of coherent priors. More generally, it agrees with the baseline on every coherent-prior finite-channel input \(p\odot L\) with \(0<L_i\le1\), because \(\sum_i p_iL_i\le1\). This additional observation concerns conditional-probability likelihoods, not arbitrary likelihood ratios or unbounded densities.

Nevertheless take \(b=(3/4,3/4)\), so \(s=3/2\) and \(p=(1/2,1/2)\). The perturbation gradient at \(b\) is \((1/8,1/16)\), whereas it is zero at \(p\). The first-argument KKT residual has nonzero coordinate difference \(-1/16\). Therefore \(p\) is not its forward projection; the actual forward minimizer is \((17/32,15/32)\), obtained by the affine-simplex quadratic first-order equation. This counterexample is inside the original open box as well as the full cone. It simultaneously guards against an orientation swap and against extrapolating subprobability-only tests to all masses.

A separate omission control is the pure perspective \(F(b)=s f(p)\) with no radial curvature. It still normalizes under first-argument projection when \(f\) is strictly convex, but it is affine along rays, is not strictly convex on the cone, and has a singular Hessian. It cannot support the inverse-Hessian claim. This does not contradict the strict-convexity theorem's stated hypotheses.

## 10. Separately proved open-box counterpart

Let \(U=(0,1)^n\), with \(F:U\to\mathbb R\) \(C^1\) and strictly convex, and use the same simplex first-argument objective. Normalization of every \(b\in U\) is equivalent to

\[
F(b)=s f(b/s)+a(s),\qquad 0<s<n,\qquad a(1)=0,
\]

where \(f=F|_{\Delta^\circ}\), and the formula is asserted only for admissible pairs \((s,p)\) with \(sp\in U\).

Here is the required additional domain argument. For fixed \(s\in(0,n)\), define

\[
\Delta_s=\{p\in\Delta^\circ: sp_i<1\ \text{for every }i\}.
\]

This set is nonempty, convex, and connected, and contains the barycenter \(u\), because \(s/n<1\). The same KKT argument gives zero tangent derivative for \(F(sp)-sF(p)\) on \(\Delta_s\), so it equals \(a(s)=F(su)-sF(u)\) there. This proves necessity on the entire box, including masses greater than one. Differentiation as in (1), or the divergence split, proves sufficiency.

The strict-convexity criterion still holds: necessity for \(a\) uses the barycenter ray for every \(s\in(0,n)\); the perspective convexity proof applies to any two box points and their segment. The Hessian and divergence formulas remain valid at admissible points. For the radial flow, both \(b_0\) and \(N(b_0)\) lie in the box, and every intermediate point of their ray segment does also. The global-forward proof therefore remains within the box under its corresponding Hessian hypotheses.

This theorem covers nonseparable generators on the box but does not alter the previous separable classification or its hypotheses. Under the older \(C^2\) separable hypotheses, intersecting either classifier with separability gives the common-entropy family from the earlier result. On the full cone, in the \(C^2\) case, one can also see this directly: differentiating the separable KKT pair conditions under scaling forces \(t f_i''(t)\) to be the same positive constant for all coordinates and all \(t>0\).

## 11. Coordinate-free mathematical transport

Let \(V\) be a finite-dimensional real vector space, \(C\subset V\) a nonempty open convex cone invariant under every positive scaling, and \(\ell\in V^*\) a linear functional strictly positive on \(C\). Set \(B=C\cap\{\ell=1\}\). This base is nonempty, convex, and connected; boundedness is unnecessary. Every \(b\in C\) is uniquely \(sp\), with \(s=\ell(b)>0\), \(p=b/s\in B\).

Replacing \(\mathbf1^T\) by \(\ell\), \(\Delta^\circ\) by \(B\), and \(T\) by \(\ker\ell\) leaves every step of Theorem 1 and Propositions 2–3 unchanged. Thus a \(C^1\) strictly convex generator projects every point onto its normalized base point exactly when \(F(sp)=s f(p)+a(s)\). For \(C^2\) data the Hessian formula uses \(h-p\ell(h)\). Viewing the Hessian as \(H_F:V\to V^*\), the positive-definite condition gives

\[
H_F(sp)p=a''(s)\ell,\qquad
\dot b=-(\ell(b)-1)H_F(b)^{-1}\ell.
\]

The same radial/global-forward proof applies. The cone of positive-definite symmetric or Hermitian matrices, with \(\ell=\operatorname{tr}\), is a valid conditional mathematical example. This corollary neither specifies a matrix Bayes action nor proves that arbitrary noetic tensors belong to a positive cone. The componentwise likelihood semantics of Section 6 remain a categorical specialization. Compact-boundary existence arguments require their own boundary hypotheses and are not silently transferred to an unbounded base.

## 12. Primary-literature ancestry and bounded attribution

Perspective convexity is classical; see Boyd and Vandenberghe, *Convex Optimization*, §3.2.6, available from the [authors' site](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf). The perspective part of (5) is an affine-scaling case of Nock, Menon, and Ong, [*A scaled Bregman theorem with applications*, Theorem 1](https://papers.neurips.cc/paper/6176-a-scaled-bregman-theorem-with-applications.pdf), NIPS 2016. The general statewise derivative in (12) and the prior information/regret accounting are inherited project inputs, not discoveries of this packet. The necessity classification, strict-convexity qualifications, domain guards, and constructive family are proved here for this project's question; no field-wide novelty or priority claim is made. The parent's exact reading scope is recorded in `../nonseparable-repair-prior-check-20261009/NOTE.md`: main abstract and §§1–2, and the supplementary Theorem 1 proof, not the whole paper or its applications. This narrow check does not constitute a complete survey.

## 13. Verification and preserved boundaries

`verify.py` checks exact symbolic identities for the concrete quadratic family, exact rational projection/scoring examples, an additional nonquadratic coherent potential, the orientation/attenuation counterexample, the degenerate-Hessian control, and the explicit quadratic radial path. It uses SymPy exact arithmetic, without statistical sampling or numerical optimization. `verification.txt` records the executed output. These finite and symbolic controls supplement, and do not replace, the ordinary general proofs above. No proof-assistant certification is claimed.

The initial perspective-classification conjecture, divergence/Hessian identities, and canonical radial-flow direction were supplied independently by the parent. This worker supplied the detailed ordinary proof, regularity and boundary qualifications, exact executable controls, separately written box proof, and the combined orientation/attenuation counterexample. A separate reviewer is assessing the finished packet.

Preserved boundaries: a coherent score does not establish a warranted prior; a likelihood-compatible implementation does not establish its channel; projection does not authenticate evidence, resolve shared-source dependence, confer acquisition authority, prove proper faculty function, establish divine warrant, or close T20. Earlier separable results, provenance constraints, source distinctions, and formal-versus-operative boundaries remain unchanged. This packet adds a conditional numerical construction and sharply identifies the separability dependence of the older entropy uniqueness result.
