# Classical source interface: positive, distinct atomic probability measures

Date: 2026-10-10. Scope: ACTIVE T20, additive mathematical source check. The calculations below are independent deductions from the stated action. They do not claim a new global existence, convergence, or geodesic theorem.

## 1. Source anchors and conventions

**KV:** Kondratyev–Vorotnikov, [arXiv:1809.03430v2](https://arxiv.org/html/1809.03430v2), §3.3, Definitions 3.14–3.15. On the flat torus, its spherical distance minimizes

\[
 A(\rho,v,\alpha)=\int_0^1\!\int (|v|^2+|\alpha|^2)\,d\rho_t\,dt,
 \qquad \partial_t\rho+\operatorname{div}(\rho v)=\rho\alpha,
 \qquad \rho_t(X)=1.
\]

The infimum is over measure-valued paths, without a fixed atomic-rank condition. Remark 1.1 gives the formal centered gradient formula for convex domains or the torus. Its analytic results concern nonlinear density energies: hypotheses (1.5)/(3.7) require \(f_u<0\); Theorem 3.7 starts from bounded densities. For \(E(x,u)=uF(x)\), \(f=-F\) has \(f_u=0\), and atomic initial measures are not bounded densities. Thus those existence/convergence theorems do not apply here. Section 3.3 explicitly specializes to the torus; it does not itself supply a theorem on \(\mathbb R^d\).

**LM:** Laschos–Mielke, [arXiv:1712.01888v2](https://arxiv.org/html/1712.01888v2), introduction, §§3.1–3.3, and §3.5/Theorem 3.7. Their base space is geodesic Polish; the PDE discussion specializes to closed convex Euclidean subsets. Their spherical metric is an **angle**, defined by

\[
 S_{\alpha,\beta}=\arccos(1-\beta H_{\alpha,\beta}^2/8),
 \qquad H_{\alpha,\beta}^2=(4/\beta)H_\ell^2,
 \qquad \ell^2=\beta/(4\alpha).
\]

Theorem 3.4 gives angular diameter at most \(\pi/2\). Its geodesic proof normalizes conic mass and reparametrizes time; it does not assert preservation of atomic rank.

**LMS:** Liero–Mielke–Savaré, [arXiv:1509.00068v2](https://arxiv.org/pdf/1509.00068v2), introduction and §4, especially Theorems 4.5–4.6 and their concluding equivalence argument. The article works on compact convex Euclidean domains. Its general parameters use Onsager operator \(-\alpha\operatorname{div}(\rho\nabla\xi)+\beta\rho\xi\); its usual \((1,4)\) convention has reaction action coefficient \(1/4\) when written with the actual reaction rate. This is not KV's unit/unit convention.

## 2. Exact fixed-path action identity

Work on a flat torus, or define the same dynamic action directly on \(\mathbb R^d\). For Euclidean domains with boundary, restrict this argument to interior atoms and admissible interior paths. Let

\[
 \rho_t=\sum_{i=1}^n w_i(t)\delta_{x_i(t)},\qquad
 w_i>0,\quad \sum_iw_i=1,\quad x_i\ne x_j\ (i\ne j),
\]

with \(C^1\) coordinates. At a fixed time write \(a_i=\dot w_i\), \(b_i=\dot x_i\). For every smooth test function,

\[
 \frac d{dt}\int\phi\,d\rho_t
 =\sum_i a_i\phi(x_i)+\sum_iw_i b_i\cdot\nabla\phi(x_i).
\]

The continuity equation gives the same expression with \(a_i\) replaced by \(w_i\alpha(x_i)\) and \(b_i\) by \(v(x_i)\). Disjoint bump functions permit arbitrary independent values and first derivatives at these finitely many distinct points. Consequently, every representing pair has

\[
 \alpha(x_i)=a_i/w_i,\qquad v(x_i)=b_i.
\]

Conversely these values define an admissible pair along the curve. Therefore the exact infimum over fields representing this **specified curve** is

\[
 A=\int_0^1 g_{(w,x)}((\dot w,\dot x),(\dot w,\dot x))\,dt,
 \quad
 g((a,b),(c,d))=\sum_i\frac{a_ic_i}{w_i}+\sum_iw_i b_i\cdot d_i,
 \quad \sum_i a_i=\sum_i c_i=0.
\]

This is a positive-definite Riemannian metric on the labeled positive, collision-free stratum, invariant under simultaneous permutation of labels. It descends to its local unlabeled charts. Even if one restricts to potential fields \(v=\nabla\psi\), \(\alpha=\psi-\int\psi\,d\rho\), no additional cost appears: prescribe \(\psi(x_i)=a_i/w_i\), \(\nabla\psi(x_i)=b_i\); the prescribed values already have mean zero.

## 3. Ambient local speed equals this norm

This conclusion is stronger than the preceding fixed-path identity but still local. It has the following direct proof, requiring no imported atomic gradient-flow theorem.

For a smooth bounded test function with bounded derivatives, define

\[
 Q_\mu(\phi)=\int |\nabla\phi|^2\,d\mu+
 \int\phi^2\,d\mu-\left(\int\phi\,d\mu\right)^2.
\]

Mass conservation gives \(\int\alpha\,d\mu=0\). Cauchy–Schwarz along any admissible probability path yields

\[
 |\langle\phi,\mu_1-\mu_0\rangle|
 \le \sqrt{A}\left(\int_0^1Q_{\mu_s}(\phi)\,ds\right)^{1/2}.
\]

For \(\rho_h\) on the given atomic curve, its own action shows \(d_S(\rho_h,\rho_0)=O(|h|)\). Choose ambient connecting paths with action at most \(d_S^2+h^4\). Their actions are \(O(h^2)\). Applied to each bounded smooth test function, the same estimate shows that its integral stays uniformly \(O(|h|)\)-close to its value at \(\rho_0\). Apply this to \(\phi\), \(\phi^2\), and \(|\nabla\phi|^2\): along these connecting paths, \(Q_{\mu_s}(\phi)\to Q_{\rho_0}(\phi)\) uniformly.

Choose a smooth test function with jets \(\phi(x_i)=a_i/w_i\), \(\nabla\phi(x_i)=b_i\). On \(\mathbb R^d\) it may be compactly supported. Then both the first derivative of \(\langle\phi,\rho_h\rangle\) and \(Q_{\rho_0}(\phi)\) equal \(g((a,b),(a,b))\). The preceding estimate gives the lower speed bound. Time-rescaling the given atomic curve gives the matching upper bound. Hence

\[
 \lim_{h\to0}\frac{d_S(\rho_{t+h},\rho_t)}{|h|}
 =\left(\sum_i\frac{\dot w_i^2}{w_i}+\sum_iw_i|\dot x_i|^2\right)^{1/2}.
\]

The zero-tangent case follows from the upper bound alone. This proves equality of ambient metric speed with the stratum's Riemannian speed along these curves. It does **not** prove equality of global distances or identify the full ambient tangent cone with this finite-dimensional tangent space.

## 4. The exact intrinsic gradient and weak measure equation

Let \(J(w,x)=\sum_iw_iF(x_i)\), \(\bar F=J\), with \(F\in C^1\). Direct differentiation and the metric above give

\[
 \operatorname{grad}_gJ
 =\big((w_i(F(x_i)-\bar F))_i,(\nabla F(x_i))_i\big).
\]

Its negative gradient is precisely

\[
 \dot x_i=-\nabla F(x_i),\qquad
 \dot w_i=-w_i(F(x_i)-\bar F).
\]

Whenever these coordinates solve the ODE and remain in the stratum, they solve, in the test-function sense,

\[
 \partial_t\rho=\operatorname{div}(\rho\nabla F)-\rho(F-\langle F,\rho\rangle),
\]

and obey the exact identity

\[
 \dot J=-\sum_iw_i|\nabla F(x_i)|^2-\sum_iw_i(F(x_i)-\bar F)^2.
\]

These are direct finite-dimensional and distributional calculations. They do not assert EVI, ambient geodesic convexity, global minimization, or convergence. Those require their own hypotheses and proof. Local ODE uniqueness, if needed, follows under a locally Lipschitz gradient, for example \(F\in C^2\).

## 5. Why the global distances differ

Let \(d_{n,g}\) minimize length among collision-free positive rank-\(n\) curves (with labels quotiented as appropriate). Inclusion of admissible curves gives

\[
 d_S(\rho_0,\rho_1)\le d_{n,g}(\rho_0,\rho_1),
\]

but equality is false in general. At rank one, \(w_1=1\), so the intrinsic metric is the base metric. For two distinct points the admissible ambient path

\[
 \rho_t=\cos^2(\pi t/2)\delta_x+\sin^2(\pi t/2)\delta_y
\]

has \(v=0\), constant action density \(\pi^2\), and length \(\pi\). Its reaction rates diverge at the endpoints but their weighted squares are integrable; endpoint values are irrelevant. It changes rank from one to two and back. Thus whenever the base separation exceeds \(\pi\), ambient distance is strictly smaller than rank-one intrinsic distance. This example works directly on \(\mathbb R^d\), or on a flat torus whose geodesic diameter exceeds \(\pi\). It should not be presented using an unspecified unit torus.

As an optional static check in LM's standard global construction, let \(r=d_X(x,y)\) and \(\ell=1/2\). Its entropy-transport problem for unit Diracs reduces to

\[
 \inf_{q\ge0}\{2(q\log q-q+1)-2q\log\cos(r/2)\}
 =2-2\cos(r/2)\quad(r<\pi),
\]

where \(q=\cos(r/2)\). At \(r\ge\pi\), only \(q=0\) has finite cost, giving 2. The angular formula then gives \(S_{1,1}=\min\{r/2,\pi/2\}\). The corresponding twice-angle value in LM's construction is therefore \(\min\{r,\pi\}\). Identifying that value globally with an explicitly defined dynamic metric requires a separately justified dynamic/static identification on the chosen domain; no such identification on all of \(\mathbb R^d\) is imported here. The elementary reaction path already establishes the required mismatch without relying on this optional static check.

## 6. Normalization and domain guardrails

1. In the actual-rate form of the general metric, action coefficients are \(1/\alpha\) for transport and \(1/\beta\) for reaction. Here \(\alpha=\beta=1\). With \(q_i=2\sqrt{w_i}\), the weight part is \(\sum_i dq_i^2\) on the sphere of radius 2.
2. The normalization dictionary, wherever the conic/spherical dynamic and static constructions have been identified on the chosen domain, is as follows: with the matching unit/unit parameters, \(d_S=2S_{1,1}=2S_{\ell=1/2}\). Correspondingly \(d_{HK}=2H_{\ell=1/2}\). One can see the factor directly from \(\rho=r^2\nu\): the unit/unit conic action splits into \(4\dot r^2+r^2A_\nu\), so radial coordinate \(R=2r\) leaves spherical angular action \(A_\nu/4\).
3. On \(\mathbb R^d\), Sections 2–5's action calculations are statements about the explicitly defined dynamic action, not an extension of KV's PDE theorem. LM supplies a general metric construction. LMS's cited dynamic/static proof has its own compact-convex scope. Do not silently merge those domains.
4. At zero weights or collisions, the coordinate chart and independent-jet argument fail. A separate boundary/stratified analysis is needed. Endpoint rank changes remain allowed by the ambient action.
5. The appropriate claim is: **an exact atomic restriction of the unit/unit spherical transport-reaction action, with matching local Riemannian speeds and an intrinsic gradient calculation**. “The global spherical HK distance restricted to the fixed-rank manifold” would be stronger and generally false if it means intrinsic endpoint-distance equality.
