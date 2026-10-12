# Exact gradient transport under probability coarse-graining

9 October 2026 UTC. Separate, conditional T20 mathematical continuation. Ordinary proofs and exact algebraic controls; no protected repository edits, implementation claim, empirical claim, formal-kernel certification, or closure claim.

## 1. Result and the three different preservation questions

For the weighted quadratic simplex potential

\[
f_\mu(p)=\frac12\sum_{i=1}^n\frac{p_i^2}{\mu_i},\qquad \mu_i>0,
\]

transporting the reference vector by a column-stochastic channel, \(\nu=K\mu\), has two different consequences:

1. Its Bregman divergence contracts under every such channel.
2. Its canonical natural-gradient dynamics commute with that channel for **every pulled-back coarse objective, in the same time parameter**, exactly when each column of the channel is a point mass. After unused outputs are removed, these are deterministic partitions, including permutations and noninjective lumpings.

For a noisy channel the projected fine dynamics still have an exact constructive description: use the **induced quotient metric**, whose cometric is \(K G_\mu K^T\), instead of replacing it with the separately prescribed canonical coarse cometric \(G_{K\mu}\). This metric exists on the reachable tangent image; it exists on the full coarse simplex tangent space when \(K\) has full row rank.

These statements concern an explicitly supplied, objective-driven tangent correction. The inherited normalization-only radial correction remains a different operation: it commutes with **all** mass-preserving \(K\) when its radial potential is held fixed. Adding a tangent objective generally destroys the inherited equal decrease in every truth-state loss. Neither descent nor commutation authenticates the objective, reference measure, channel, prior, evidence, or actual noetic interpretation.

The initial mobility identity and deterministic-column conjecture were supplied by the parent; the parent also independently supplied the quotient construction. This packet verifies them, proves the qualifications and constructive quotient identity, supplies counterexamples, and compares the actual pinned sources. No external novelty claim is made.

## 2. Spaces, intrinsic derivatives, and the inverse tangent metric

Let

\[
\Delta_n^\circ=\{p\in\mathbb R^n:p_i>0,\ \mathbf1_n^Tp=1\},
\qquad T_n=\ker\mathbf1_n^T.
\]

Fix \(\mu\in\mathbb R_{++}^n\), put \(M=\mathbf1_n^T\mu\), and write \(D_\mu=\operatorname{diag}(\mu)\). The reference vector is fixed geometric data throughout each flow and is transported as auxiliary structure under \(K\). It need not be a probability law, and it is not silently replaced by the evolving point \(p\). Replacing it by the current state, or revising the criterion during the flow, changes the geometric problem and is not automatically covered. The symbol \(\mu\) here denotes only reference masses; it does not denote the repository’s metaortheme register or ecology notation.

The Hessian metric of \(f_\mu\) on the simplex is

\[
h_\mu(u,v)=u^TD_\mu^{-1}v,\qquad u,v\in T_n.
\]

It is positive definite there. A differential of an objective on the affine simplex is intrinsically a covector on \(T_n\). An ambient representative \(g\in\mathbb R^n\) is defined only modulo \(c\mathbf1_n\). Define

\[
G_\mu=D_\mu-\frac{\mu\mu^T}{M}.\tag{1}
\]

This is the inverse tangent metric, expressed on ambient covectors modulo constants. It is **not** the ordinary full-space inverse of \(D_\mu^{-1}\). Indeed,

\[
\mathbf1_n^TG_\mu=0,
\qquad D_\mu^{-1}G_\mu=I-\mathbf1_n\mu^T/M.
\]

Consequently, for every \(v\in T_n\),

\[
h_\mu(G_\mu g,v)=g^Tv.
\]

The defining metric-duality condition therefore gives

\[
\operatorname{grad}_{h_\mu}J=G_\mu g,
\qquad \dot p=-G_\mu g.\tag{2}
\]

The expression is invariant under adding a constant to \(g\). Also

\[
z^TG_\mu z=\sum_i\mu_i(z_i-\bar z_\mu)^2,
\qquad \bar z_\mu=\frac{\sum_i\mu_i z_i}{M},
\]

so \(G_\mu\) is positive semidefinite with kernel \(\operatorname{span}\{\mathbf1_n\}\) and range \(T_n\). Here “natural gradient” means the Riemannian gradient for this declared Hessian metric. It does not identify the metric with the Fisher metric on all probability states.

Let \(K\) be a nonnegative \(m\)-by-\(n\) matrix satisfying \(\mathbf1_m^TK=\mathbf1_n^T\). Remove any zero output rows. Then \(\nu=K\mu>0\), \(\mathbf1_m^T\nu=M\), and \(Kp\in\Delta_m^\circ\) whenever \(p\in\Delta_n^\circ\). Thus the coarse potential \(f_\nu\) is defined even when \(K\) has deficient rank.

## 3. The canonical commutation theorem

Let \(\bar J\) be a smooth objective on \(\Delta_m^\circ\), and set \(J(p)=\bar J(Kp)\). At \(q=Kp\), choose an ambient representative \(g\) of \(d\bar J_q\). The chain rule and (2) give

\[
\dot p=-G_\mu K^Tg,
\qquad \dot q_{\rm projected}=-A g,
\qquad A:=K G_\mu K^T.\tag{3}
\]

The canonical coarse geometry instead gives

\[
\dot q_{\rm canonical}=-B g,
\qquad B:=G_\nu.\tag{4}
\]

### Theorem 1

Under the stated positivity and stochasticity assumptions, the following are equivalent:

- (3) and (4) agree for every smooth coarse objective, at any fixed interior fine point;
- \(A=B\);
- every column of \(K\) is a point mass.

Equivalently, for every initial \(p_0\in\Delta_n^\circ\) and every smooth coarse objective, the projected fine flow and canonical coarse flow with initial condition \(Kp_0\) agree on their common interval of interior existence precisely for deterministic \(K\). “Every objective” is essential.

### Proof

The rank-one terms in (1) cancel, since \(K\mu=\nu\) and both reference masses total \(M\). Thus

\[
C:=B-A=\operatorname{diag}(K\mu)-K\operatorname{diag}(\mu)K^T.\tag{5}
\]

Write \(k_i\) for column \(i\) of \(K\). For every \(z\in\mathbb R^m\),

\[
\begin{aligned}
z^TCz
 &=\sum_i\mu_i\left(\sum_jK_{ji}z_j^2-
              \left(\sum_jK_{ji}z_j\right)^2\right)\\
 &=\sum_i\mu_i\,\operatorname{Var}_{Y\sim k_i}(z_Y)\ge0.\tag{6}
\end{aligned}
\]

This proves positive semidefiniteness by an ordinary finite variance identity. If every column is a point mass, each variance vanishes, so \(C=0\). Conversely,

\[
\operatorname{tr}C=\sum_i\mu_i\left(1-\sum_jK_{ji}^2\right).
\]

Every summand is nonnegative. Since every \(\mu_i>0\), a zero trace forces \(\sum_jK_{ji}^2=1\) in every probability column, which forces that column to have one entry 1 and all others 0. Thus \(C=0\) exactly for deterministic columns.

Both \(A\) and \(B\) annihilate \(\mathbf1_m\). Accordingly, equality of the intrinsic maps on coarse covectors modulo constants is the same as equality of their displayed matrices. There is no hidden normal/gauge exception. More directly, the linear objectives \(\bar J(q)=z^Tq\) realize every ambient covector class. Equality for all of them gives \(Cz=0\) for every \(z\), hence \(C=0\). This proves the vector-field equivalence.

For a smooth objective the fields are locally Lipschitz in affine charts. Initial fine and coarse points are interior; continuity supplies a nonzero time interval on which both remain interior. If \(A=B\), the projected fine curve solves the same coarse initial-value problem, and local uniqueness gives equality throughout their common interior interval. Conversely, equality of those curves for every linear objective implies equality of their derivatives at time zero, giving the already proved matrix condition. No global interior existence is used. \(\square\)

### A particular objective can still commute through noise

At a given point the necessary and sufficient condition is merely

\[
C g=0.\tag{7}
\]

Because \(C\) is positive semidefinite, (6) proves that this holds exactly when \(g_j\) is constant on the support of each column \(k_i\). Equivalently, form a graph on output labels, connecting two labels if they both have positive probability in some one input column. The kernel consists of vectors constant on each connected component. Transitive closure supplies the equivalence; isolated outputs are separate components.

For a fixed objective, require (7) along the trajectory, or throughout the relevant region for a regional vector-field statement. Noise therefore does not force failure for every objective. If that support graph is connected, only constant covectors survive, and both corresponding gradients vanish. The rank-deficient case still permits extra restrictions on which points are reachable, but does not invalidate Theorem 1's quantification over full coarse-simplex objectives.

At a common state the two objective decrease rates differ by the exact nonnegative amount \(g^TCg\):

\[
\left(-\frac{d\bar J}{dt}\right)_{\rm canonical}
-
\left(-\frac{d\bar J}{dt}\right)_{\rm projected}
=g^TCg.\tag{8}
\]

This compares velocities at the same state, not entire trajectories at equal later times. It is a model-relative dissipation identity, not a truth or warrant measure.

## 4. Exact finite counterexamples

### 4.1 Binary noise changes the actual time-dependent correction

Take

\[
\mu=(1/2,1/2)^T,
\qquad K=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix},
\qquad \bar J(q)=q_1.
\]

Then \(\nu=\mu\), and

\[
B=\frac14\begin{pmatrix}1&-1\\-1&1\end{pmatrix},
\quad A=\frac1{16}\begin{pmatrix}1&-1\\-1&1\end{pmatrix},
\quad C=\frac3{16}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\]

At \(p_0=(1/2,1/2)^T\),

\[
\dot p=(-1/8,1/8)^T,
\quad K\dot p=(-1/16,1/16)^T,
\quad \dot q_{\rm canonical}=(-1/4,1/4)^T.
\]

For \(0\le t<2\), both curves are interior, with

\[
Kp(t)=(1/2-t/16,1/2+t/16)^T,
\quad q_{\rm canonical}(t)=(1/2-t/4,1/2+t/4)^T.
\]

At \(t=1\), these equal \((7/16,9/16)\) and \((1/4,3/4)\), respectively. The fine curve itself remains interior up to \(t=4\); the common interval is limited by the coarse curve. This example is exact, with no simulation or numerical integration.

At the same time the divergence contracts correctly. For \(p=(3/4,1/4)\) and \(r=(1/4,3/4)\),

\[
D_{f_\mu}(p,r)=1/2,
\qquad D_{f_\nu}(Kp,Kr)=1/8.
\]

Thus correct divergence processing does not give canonical dynamic commutation. The contraction claim is specific to this reference-weighted quadratic family, not to an arbitrary coherent Bregman potential from the wider nonseparable repair family.

### 4.2 Ternary noise changes direction, not just speed

Take \(\mu=(1/3,1/3,1/3)^T\) and

\[
K=\begin{pmatrix}3/4&1/4&0\\1/4&3/4&0\\0&0&1\end{pmatrix},
\qquad \bar J(q)=q_1.
\]

Again \(K\mu=\mu\). At every interior point the projected and canonical velocities are, respectively,

\[
(-7/72,-1/72,1/9)^T,
\qquad (-2/9,1/9,1/9)^T.\tag{9}
\]

They are not collinear: the second coordinate has opposite signs while their equal, nonzero third coordinates would force any scalar multiplier to be 1. No time reparameterization reconciles their local paths. A block-constant objective, such as \(q_1+q_2\), does commute, as the particular-objective criterion predicts.

The distinction also occurs for a target-directed quadratic objective, rather than only for a linear one. With the same ternary metric, let \(r=(1/6,1/3,1/2)\), \(q_0=(1/3,1/3,1/3)\), and \(\bar J(q)=D_{f_\mu}(r,q)\). Its canonical velocity at \(q_0\) is \(r-q_0\); its projected fine velocity is \(-A D_\mu^{-1}(q_0-r)\), not collinear with \(r-q_0\). The target is stipulated mathematical data, not a warranted true state.

### 4.3 Even exact deterministic commutation does not ensure a global interior lift

Let \(\mu=(1,1,1)^T\),

\[
K=\begin{pmatrix}1&1&0\\0&0&1\end{pmatrix},
\qquad p_0=(1/12,5/12,1/2)^T,
\qquad \bar J(q)=q_1.
\]

Then \(\dot p=(-1/3,-1/3,2/3)^T\). At \(t=1/4\), the first fine coordinate reaches zero, but its coarse image is still \((1/3,2/3)^T\), strictly interior. Extending the algebraic affine ODE beyond that point is not a positive-probability trajectory. Any boundary-constrained continuation is a further operation requiring its own definition and transport proof.

## 5. Faithful quotient geometry for every channel

The canonical geometry is one choice. To transport the actual fine correction, retain

\[
A=K G_\mu K^T.
\]

Let \(S=K T_n\subseteq T_m\). Since

\[
z^TAz=(K^Tz)^TG_\mu(K^Tz),
\]

we have

\[
\ker A=\{z:K^Tz\in\operatorname{span}(\mathbf1_n)\}=S^\perp,
\qquad \operatorname{range}A=S.\tag{10}
\]

Thus \(A\) is positive definite as an operator on \(S\), even if singular on the full coarse tangent space. The reachable set \(R=K\Delta_n^\circ\) is relatively open and convex in its affine hull \(q_0+S\); this follows because the restricted linear map onto \(S\) is surjective and hence open in finite dimensions. Its tangent space is \(S\).

### Theorem 2: exact least-energy quotient identity

For \(w\in S\), define

\[
\|w\|_Q^2:=\min_{v\in T_n:\ Kv=w}v^TD_\mu^{-1}v.\tag{11}
\]

Then the unique minimizing lift and its energy are

\[
v_* =G_\mu K^T A^+w,
\qquad \|w\|_Q^2=w^T A^+w,\tag{12}
\]

where \(A^+\) is the Moore–Penrose inverse in the chosen standard Euclidean coordinates. These formulas represent an intrinsic quotient of the fine inner-product space by \(\ker(K|_{T_n})\). The constrained minimum in (11), not a coordinate-free status of a pseudoinverse matrix, establishes that intrinsic meaning.

### Proof

By (10), \(AA^+w=w\), so \(Kv_*=w\); also \(v_*\in T_n\). Every other feasible vector is \(v_*+h\), where \(h\in T_n\) and \(Kh=0\). The tangent duality identity in Section 2 gives

\[
v_*^TD_\mu^{-1}h=(A^+w)^TKh=0.
\]

Pythagorean expansion therefore yields

\[
(v_*+h)^TD_\mu^{-1}(v_*+h)
=v_*^TD_\mu^{-1}v_*+h^TD_\mu^{-1}h.
\]

The last term is strictly positive unless \(h=0\). Finally,

\[
v_*^TD_\mu^{-1}v_*=(A^+w)^TKv_*=w^TA^+w.
\]

This proves existence, uniqueness, and the asserted energy. \(\square\)

Polarizing (11) defines the quotient metric \(h_Q(u,w)=u^TA^+w\) on \(S\). For an objective differential represented by \(g\),

\[
h_Q(Ag,w)=g^Tw\quad(w\in S),
\]

so its negative gradient is exactly \(-Ag\), the projected fine field (3). Covector representatives now differ by elements of \(S^\perp\), all annihilated by \(A\). A quadratic potential \(\tfrac12(q-q_0)^TA^+(q-q_0)\) on \(q_0+S\) realizes this constant Hessian metric, if a potential is desired.

There is a genuine quotient metric on the **whole coarse tangent space** exactly when \(S=T_m\), equivalently \(\operatorname{rank}K=m\). Indeed the image of \(K\) is the direct sum of \(K T_n\) and one mass-nonzero direction, so \(\operatorname{rank}A=\operatorname{rank}K-1\). Even with full row rank, \(K\Delta_n^\circ\) can be a proper subset of the coarse simplex: the binary noisy example reaches only \(1/4<q_1<3/4\). The resulting constant metric can be extended to all coarse states, but this extension does not supply positive fine lifts for unreachable states. A rank-one reset channel has \(S=\{0\}\), \(A=0\), and a single reachable law. It has no positive-dimensional induced correction, even though \(G_\nu\) may be nonzero.

All quotient-gradient claims remain local in the reachable set and in a positive fine lift. A quotient trajectory need not keep a particular initial fine lift inside the simplex forever, as Section 4.3 demonstrates even for deterministic \(K\). The minimum-energy statement is a tangent statement, not a claim that arbitrary finite displacements preserve positivity.

## 6. Relation to divergence contraction and radial repair

For \(\delta=p-r\), the coherent Bregman divergence is

\[
D_{f_\mu}(p,r)=\frac12\sum_i\frac{\delta_i^2}{\mu_i}.
\]

For each output \(j\), weighted Cauchy–Schwarz gives

\[
\frac{(\sum_iK_{ji}\delta_i)^2}{\sum_iK_{ji}\mu_i}
\le \sum_iK_{ji}\frac{\delta_i^2}{\mu_i}.
\]

Summing and using column stochasticity proves contraction. Equality holds precisely when \(\delta_i/\mu_i\) is constant over the input support of each output row. This is a **row-support condition on a given state pair**. The dynamic criterion (6) is a **column-support condition on objective covectors**. They are different statements, so neither contraction nor pairwise divergence equality should be substituted for full dynamic commutation. Deterministic lumping may strictly contract divergence between some fine states while still commuting with every pulled-back coarse objective.

For the nonseparable family retained in the previous packet,

\[
F_\mu(sp)=s f_\mu(p)+a(s),\qquad a''(s)>0,
\]

the Hessian metric in mass/simplex coordinates is

\[
g_{F_\mu}=a''(s)\,ds^2+s h_\mu(dp,dp).\tag{13}
\]

The inherited normalization correction, the negative \(g_{F_\mu}\)-gradient of \(\tfrac12(s-1)^2\), is

\[
\dot s=-\frac{s-1}{a''(s)},\qquad \dot p=0.
\]

With the same radial \(a\), a column-stochastic \(K\) preserves mass and sends \(sp\) to \(sKp\), so this field commutes with every such \(K\). Its stronger global radial existence result remains untouched.

### Optional augmented full-Hessian correction

An explicitly supplied coarse objective can be incorporated into

\[
E(sp)=\frac12(s-1)^2+\bar J(Kp).
\]

Using (13), its negative gradient is

\[
\dot s=-\frac{s-1}{a''(s)},\qquad
\dot p=-\frac1sG_\mu K^T d\bar J_{Kp}.\tag{14}
\]

The canonical coarse version has \(\dot q=-G_\nu d\bar J_q/s\); the faithfully induced version has \(\dot q=-A d\bar J_q/s\). Thus the same deterministic criterion or quotient construction applies, with a shared positive scalar clock factor \(1/s\). For ordinary local uniqueness, \(a\in C^3\), \(a''>0\), and \(\bar J\in C^2\) are sufficient. No all-time interior conclusion is claimed for the tangent component.

Adding \(\bar J\) is consequential: it generally removes equal all-truth improvement. For each truth vertex \(e_i\), the earlier divergence split and (14) give

\[
\frac{d}{dt}D_{F_\mu}(e_i,sp)
=-(s-1)^2+\frac1s\,d\bar J_{Kp}^T(K e_i-Kp).\tag{15}
\]

The second term depends on \(i\) and can be positive. In the binary example, at \(s=1,p=(1/2,1/2)\), the two truth-state loss derivatives are \(+1/4\) and \(-1/4\). The chosen objective still decreases. Thus a decrease in \(E\) supplies no universal accuracy, epistemic warrant, or restoration guarantee.

## 7. Source-faithful comparison with inherited work

The local source bytes and Git blob hashes are recorded in `SOURCE_LEDGER.json`. No source is edited. The relevant distinctions are:

- The retained pinned note, [*Common local repair characterizes smooth additive scores*](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be.md), already treats Hessian-orthogonal coherent repair and the second-argument loss derivative. Its S1 concerns agreement of local normal repair projections; S6 explicitly separates common normal correction from differing tangent normative comparisons in a nonseparable example. This packet does not discover that distinction. It adds a concrete stochastic map and tests preservation of the entire specified tangent objective flow across that map. The source's retained verification-status banner is preserved, not upgraded by this comparison.
- `nonseparable-bayes-repair-20261009/RESULT.md`, Sections 3–8 and 11, supplies the perspective family, tangent/radial Hessian split, Bregman orientation, and all-truth normalization-only field. Those formulas are inherited inputs. The comparison above keeps its full-cone and positive-Hessian premises and does not weaken its global radial result.
- The pinned [H-ICS v5 manuscript](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex), its output-determination proposition and observation-congruence theorem, already distinguishes descent of an operation to a quotient from acquisition of a new distinction. The present projected vector field automatically descends through \(K\) because the fine metric is constant and the objective is pulled back; the further question is whether that descended field agrees with a **separately specified** canonical coarse geometry. This does not contradict the inherited congruence result, and does not extend that finite exact-observation theorem to empirical continuous cognition.
- The pinned [CP12 finite-geometric-score packet](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/research/t20-live-20261009/checkpoints/CP12/t20-next-frontier-20261008/finite-geometric-score/RESULT.md) defines a calibrated endpoint/skyline testing statistic and its resource bounds. Its “score” is not the simplex Hessian metric of this packet. No identity between those differently typed scores is assumed.
- The pinned [sound-descent comparison](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md) keeps literal differentiable G2 geometry conditional and requires hard constraints, provenance, uncertainty, and whole-state rereading separately from route ranking. The pinned [DAEE formalism](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/algebraic-notation-and-noetic-formalism.md) types its route-gradient as a ranking functional and its public-output coupling as partial. This packet supplies one conditional numerical submodel and a falsifiable transport test within it. It does not identify runtime registers or an actual person's noetic condition with simplex coordinates.

Only these targeted loci are compared. In particular, absence of the present construction from H-ICS or CP12 is not evidence that the wider project lacks inherited Hessian geometry; the pinned local-repair source positively demonstrates that it has such geometry.

## 8. Primary-literature ancestry and verification scope

Natural/Riemannian gradients and constrained Hessian flows are classical. [Alvarez, Bolte, and Brahic, *Hessian Riemannian gradient flows in convex programming*, Section 2.2, equations (7)–(10)](https://arxiv.org/pdf/1811.10331) explicitly gives the metric-projected inverse-Hessian gradient under affine constraints. Equation (1) above is its one-affine-constraint, diagonal-Hessian specialization. The source's broader global results use additional Legendre/existence hypotheses; those are not imported for this nonbarrier quadratic metric. The inspected scope was the abstract, introduction, and Section 2.2, not the entire paper.

The variance calculation, weighted Cauchy–Schwarz contraction, and least-energy quotient are proved directly here. They carry standard linear-algebra, conditional-variance, and information-processing ancestry. The parent's separate targeted reference-measure work records the f-divergence ancestry; this packet does not claim a new external theorem or undertake a general literature survey.

`verify.py` uses SymPy exact arithmetic. The executed `verification.txt` records 33 control groups: symbolic tangent duality; deterministic mobility equality; exact binary and ternary failures; selected-objective survival; all 27 binary-output channels whose three columns have probabilities in \(\{0,1/2,1\}\); full-rank and rank-deficient quotient lifts, energies and orthogonality; the reset case; fine-boundary failure; target-divergence correction; the augmented full-Hessian split; radial commutation; and opposite truth-loss derivative signs. These controls supplement the ordinary proofs; finitely many channels do not prove the general iff.

What is newly established for this conditional model is an exact operational discriminator: transporting normalization, transporting a contracting discrepancy, and transporting a whole prescribed correction field are different obligations. A noisy channel can meet the first two and fail the third if the coarse metric is independently reset to its canonical reference-based form. Transporting the actual quotient geometry repairs that third obligation on reachable directions. None of these operations establishes source authentication, source independence, cognitive realization, acquisition authority, truth of a target, proper function, or T20 closure.
