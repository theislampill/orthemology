# A nonlinear Hessian flow need not descend to its coarse state

9 October 2026 UTC. Additive ordinary mathematical countermodel. The completed fixed-reference packet is unchanged. No protected edits, cognitive implementation, empirical claim, formal-kernel certification, or closure claim.

## 1. Exact result

The constant weighted-quadratic metric in the earlier transport theorem was consequential. In the permitted nonseparable repair family, a fixed nonlinear coherent potential can have a state-dependent Hessian. For negative entropy, a noisy probability channel can send two positive fine states to the same coarse state while sending their natural-gradient velocities to different coarse velocities, even for the same pulled-back linear objective.

Thus, for this example, there is no single coarse vector field depending only on the coarse state that represents the projected correction for every fine state in its fibre. This is stronger than disagreement with a separately chosen canonical coarse metric. It does **not** say that pointwise quotient metrics fail to exist, that no richer coarse state works, or that every nonlinear potential has this problem. Deterministic channels provide an exact positive control.

## 2. A fixed nonlinear potential within the inherited family

On the positive probability simplex use

\[
f(p)=\sum_i p_i\log p_i,
\qquad h_p(u,v)=\sum_i\frac{u_i v_i}{p_i},
\qquad \mathbf1^Tu=\mathbf1^Tv=0.
\]

This is a fixed negative-entropy generator with its Fisher simplex metric. Its inverse tangent metric is

\[
G(p)=\operatorname{diag}(p)-pp^T.\tag{1}
\]

The metric varies because the Hessian of the **fixed** generator varies with its base point. This is not a silent substitution of the current state into the fixed auxiliary reference vector of the previous quadratic theorem.

For a column-stochastic \(K\), let \(q=Kp\), fix a smooth coarse objective \(\bar J\), and put \(J(p)=\bar J(Kp)\). If \(g\) represents \(d\bar J_q\), then

\[
\dot p=-G(p)K^Tg,
\qquad \dot q=-A(p)g,
\qquad A(p)=K\operatorname{diag}(p)K^T-qq^T.\tag{2}
\]

All covectors are understood modulo constants; both \(G(p)\) and \(A(p)\) annihilate the relevant constant vector. Gauge choice does not cause the failure below.

This potential is admitted by the earlier nonseparable construction. For example,

\[
F(sp)=s f(p)+\frac12(s-1)^2
\]

has a positive-definite full Hessian on the positive cone, by the earlier tangent/radial criterion. With objective

\[
E(sp)=\frac12(s-1)^2+\bar J(Kp),
\]

the full-Hessian flow has \(\dot s=-(s-1)\) and \(\dot p=-G(p)K^Tg/s\). At coherent initial mass \(s=1\), mass stays 1 and (2) is exactly its tangent flow. The countermodel therefore lies within that conditional full-Hessian family; it does not challenge the earlier normalization-only radial theorem.

## 3. Same coarse state, different projected corrections

Set

\[
K=\begin{pmatrix}1&0&1/2\\0&1&1/2\end{pmatrix},
\quad
p=(1/4,1/4,1/2)^T,
\quad
r=(3/8,3/8,1/4)^T.
\]

Both fine states are strictly positive and normalized, while

\[
Kp=Kr=q=(1/2,1/2)^T.
\]

Writing \(L=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\), direct exact multiplication gives

\[
A(p)=\frac18L,
\qquad A(r)=\frac3{16}L.\tag{3}
\]

Choose \(\bar J(q)=q_1\), so \(g=(1,0)^T\) and \(K^Tg=(1,0,1/2)^T\). The two fine velocities are

\[
\dot p=(-1/8,1/8,0)^T,
\qquad \dot r=(-3/16,3/16,0)^T,
\]

and their projected velocities are

\[
K\dot p=(-1/8,1/8)^T,
\qquad K\dot r=(-3/16,3/16)^T.\tag{4}
\]

A vector field \(V(q)\) cannot take both values at the same \(q\). Hence no \(q\)-only coarse vector field represents this one objective's projected dynamics for all fine states. The canonical coarse Fisher velocity, \(-G(q)g=(-1/4,1/4)^T\), is a third value, but the obstruction does not depend on proposing that canonical choice.

More generally, for a differentiable fine vector field \(X\), a projected field depending only on \(q=Kp\) requires

\[
Kp=Kr\Longrightarrow KX(p)=KX(r).\tag{5}
\]

For every pulled-back smooth objective in (2), the necessary and sufficient **pointwise factorization** condition is that \(A(p)\) be constant on each fibre of \(K\). Sufficiency is substitution; necessity follows by testing all linear objectives, whose differentials realize every covector class. The example violates this condition, and (4) already violates it for one specific objective.

### The obstruction is not boundary or rank degeneracy

The channel has full row rank, and its image of the positive simplex is the entire positive binary simplex: for \(0<x<1\), choose any \(0<z<2\min(x,1-x)\), and

\[
u=(x-z/2,1-x-z/2,z)^T>0,
\qquad Ku=(x,1-x)^T.
\]

Along this fibre,

\[
A(u)=\left(x(1-x)-\frac z4\right)L,\tag{6}
\]

so the hidden fine coordinate \(z\) directly changes the projected mobility. The coefficient is positive throughout the declared interior range.

Each individual fine metric has a well-defined positive quotient metric on the coarse tangent. Its least-lift-energy cometric is \(A(p)\) or \(A(r)\), respectively, by the earlier pointwise linear-algebra proof. For the same tangent displacement \(w=(1,-1)^T\), the two quotient energies are

\[
w^TA(p)^+w=8,
\qquad w^TA(r)^+w=16/3.
\]

The failure is that these positive pointwise metrics do not agree over the same coarse base point, so they do not define a common metric there for all lifts.

### Genuine trajectories, without a boundary qualification doing the work

For this linear objective put \(a=(1,0,1/2)^T\). Starting from either positive fine state \(u_0\), the exact solution is

\[
u_i(t)=\frac{u_{0i}e^{-a_i t}}{\sum_j u_{0j}e^{-a_j t}}.\tag{7}
\]

Differentiation verifies (2). Every coordinate remains positive for every finite \(t\ge0\), and the mass is 1. Their common coarse initial value has the different derivatives in (4), so the projected curves disagree locally. This explicit global positive solution is asserted only for this specified linear-objective example. Arbitrary smooth objectives retain their ordinary local-existence qualifications.

## 4. Positive deterministic-channel control

If every column \(k_i\) of \(K\) is a point mass, then

\[
K\operatorname{diag}(p)K^T
=\sum_i p_i k_i k_i^T
=\operatorname{diag}(Kp).
\]

Therefore

\[
K G(p)K^T=G(Kp).\tag{8}
\]

Every pulled-back coarse objective then has exactly the canonical coarse Fisher-gradient field, at every interior point. Subject to the usual common interior existence interval, its projected trajectories commute as well. Thus state-dependent Hessian geometry does not by itself prevent transport; the channel and the fibre dependence of its induced metric matter.

## 5. Immediate graded-tensor identity

This same numerical model gives a literal, typed tensor relation. Keep the channel columns \(k_i\in\mathbb R^m\) fixed, and define symmetric moment tensors

\[
M_\ell=\sum_i p_i k_i^{\otimes\ell},\qquad
M_0=1,\quad M_1=q.
\]

For \(\ell\ge0\), let \(\iota_g M_{\ell+1}\) contract the last tensor factor with the covector \(g\). Equation (2) says

\[
\dot p_i=-p_i\bigl(g(k_i)-g(M_1)\bigr).
\]

Since the \(k_i\) are fixed, termwise differentiation immediately proves

\[
\boxed{\dot M_\ell=-\iota_g M_{\ell+1}+g(M_1)M_\ell.}\tag{9}
\]

In components, contraction means

\[
(\iota_g M_{\ell+1})_{j_1\ldots j_\ell}
=\sum_{j=1}^m (M_{\ell+1})_{j_1\ldots j_\ell j}\,g_j.
\]

In particular,

\[
\dot q=-M_2g+(q^Tg)q,
\qquad
\dot M_2=-\iota_g M_3+(q^Tg)M_2.\tag{10}
\]

The first moment alone can therefore lose information needed for its correction law, as (3) demonstrates through differing \(M_2\). Evolving the displayed second moment uses the third. These are exact graded-tensor contractions, not an analogy to a field or to an unspecified noetic tensor. No claim about a minimal sufficient moment order, general finite closure, or impossibility of a richer state is made here.

Equation (9) also holds for a prescribed time-varying numerical covector \(g(t)\) in the same controlled replicator equation. Calling it a natural-gradient objective flow additionally requires the relevant objective differential, for example \(g=d_q\bar J(t,q)\). If one differentiates the first equation of (10) again, terms involving \(\dot g\) must also be retained; the second equation of (10) is the evolution of \(M_2\), not an assertion that \(\ddot q\) depends only on \(M_3\). Time-varying channel columns would add further terms and are outside (9).

## 6. Inherited source comparison and scope

The previous `noetic-gradient-transport-20261009/RESULT.md` proves the exact fixed-reference quadratic theorem and its quotient construction. Its constant fine cometric makes \(K G_\mu K^T\) independent of the fine base point, so its projected flow genuinely depends only on \(Kp\). That packet remains unchanged. The present countermodel identifies why this part of its conclusion does not automatically extend to every coherent potential allowed by `nonseparable-bayes-repair-20261009/RESULT.md`.

The pinned [H-ICS v5 observation-congruence theorem](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex) already uses equality on observation fibres as the criterion for a quotient action. Equation (5) is the directly proved continuous vector-field factorization condition for this declared probability model. It is consistent with that inherited criterion, not a claim that its finite exact-observation theorem already covers all nonlinear flows.

The constrained inverse-Hessian gradient formula has classical ancestry; see [Alvarez, Bolte, and Brahic, Section 2.2, equations (7)–(10)](https://arxiv.org/pdf/1811.10331), as read for the preceding packet. The negative-entropy specialization here is checked directly, and the finite countermodel and tensor derivative identity are ordinary calculations, without an external priority claim.

The parent supplied the candidate channel, pair of fine states, and moment identity. This packet independently checked them, supplied the exact trajectories, the full-fibre formula, the pointwise-quotient guard, the deterministic control, and the source-faithful scope. `verify.py` gives 19 exact control groups, including componentwise moment identities through order four. Those finite tests supplement the general written derivation, not replace it. No source authenticity, cognitive realization, actual correction efficacy, metaphysical warrant, or T20 closure follows from this numerical model.
