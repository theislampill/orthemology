# Exact moment closure and continuation for Fisher coarse-gradient dynamics

9 October 2026 UTC. Conditional ordinary mathematics with exact algebraic controls. This is an additive continuation of the state-dependent Fisher calculation. It does not revise the fixed-reference metric results in `noetic-gradient-transport-20261009/RESULT.md`, edit protected sources, claim empirical identification, certify a formal kernel proof, or close T20.

## 1. Main result

For a known, fixed finite channel, the first coarse moment can forget distinctions that determine its next velocity. The lost information has a precise graded tensor representation. Moments through degree **N−1**, where N is the number of distinct channel columns, are sufficient to recover all aggregate weights and close the entire controlled dynamics exactly. This is a sufficient bound for known support, not a universally optimal degree.

Two positive initial fine states have identical coarse continuations under every real constant or piecewise-constant objective covector exactly when they give the same total weight to each class of identical channel columns. Indeed, one fixed generic constant covector, with its exact scalar response observed on any interval starting at zero of positive length, already distinguishes every unequal pair of such aggregate laws.

This is a substantive connection between a declared natural-gradient correction, consequential higher-order tensor information, and continuation-preserving representations. It is a conditional application of classical replicator dynamics, exponential tilting, finite interpolation, and observation congruence. No external novelty claim is made.

## 2. Declared state, metric, control, and duplicate classes

Let K be an m-by-n nonnegative column-stochastic matrix. Its columns k_i lie in the closed probability simplex Δ_m; zero output rows are harmless here. The fine state p lies in the open simplex Δ_n°. Its Fisher/Shahshahani metric is

\[
h_p(a,b)=\sum_i a_i b_i/p_i,\qquad \mathbf1^Ta=\mathbf1^Tb=0.
\]

This is the Hessian metric of negative entropy on the open simplex. At time t use the pulled-back linear objective J_g(p)=g(t)·Kp, where g(t)∈R^m is an externally specified covector. Controls are piecewise constant with finitely many switches on each bounded time interval. Each value is finite; no amplitude or sign restriction is imposed. The inverse tangent metric is diag(p)−ppᵀ, so

\[
\dot p_i=-p_i\bigl(g\cdot k_i-g\cdot q\bigr),
\qquad q=Kp. \tag{1}
\]

For example, if b is tangent then h_p((diag(p)−ppᵀ)Kᵀg,b)=g·Kb, which verifies (1) intrinsically. Adding any scalar multiple of 1_m to g changes neither the flow nor any claim below.

Let κ_1,…,κ_N be the distinct column values, and I_j={i:k_i=κ_j}. Define

\[
w_j=\sum_{i\in I_j}p_i>0,
\qquad \sum_jw_j=1,
\qquad q=\sum_jw_j\kappa_j.
\]

Summing (1) gives the same replicator equation for the aggregate state:

\[
\dot w_j=-w_j\bigl(g\cdot\kappa_j-g\cdot q\bigr). \tag{2}
\]

Within I_j, p_i/w_j is constant. Thus aggregate weights suffice for this specific control/output interface, while different within-class allocations remain genuine differences of fine state. Every positive aggregate law is realised by a positive fine state, for example by splitting w_j equally among I_j.

## 3. Exact graded hierarchy

Write V=R^m, identify g with the covector z↦g·z, and define the symmetric tensor moments

\[
M_0=1,\qquad M_r=\sum_{j=1}^Nw_j\kappa_j^{\otimes r}
\in\operatorname{Sym}^r(V)\quad(r\ge1).
\]

The use of symmetric powers is justified by interchangeable repeated copies of the same numerical channel-vector type. It is not a symmetrisation of different semantic roles. In particular, M_1=q and M_2=Σ_jw_jκ_jκ_jᵀ.

For a symmetric (r+1)-tensor, let ι_g contract its last slot against g, so ι_g(κ^{⊗(r+1)})=(g·κ)κ^{⊗r}. This is one-slot evaluation, with no r+1 multiplier from summing over slots. Differentiating the finite sum using (2) proves, for every r≥0 and every nonswitching time,

\[
\boxed{\dot M_r=-\iota_gM_{r+1}+(g\cdot M_1)M_r.}\tag{3}
\]

For r=0 this says 0=−g·q+g·q. At a control switch the moments remain continuous and have the appropriate one-sided derivatives. Hence (3) also holds almost everywhere and in integrated form. No exchange of infinite sums and derivatives is involved.

The first equation is

\[
\dot q=-\bigl(M_2-qq^T\bigr)g.\tag{4}
\]

The projected mobility is the covariance of the fixed support vectors. It need not be a function of q alone. The next equation is \(\dot M_2=-\iota_gM_3+(g\cdot q)M_2\); higher information can therefore be needed for continuation even after the immediate velocity is known.

The full sequence (M_r)_{r≥0} generally has infinitely many nonzero grades. In fact contraction of M_r against 1_m in every slot is 1 for every r. It belongs naturally to a graded product/formal sequence space, **not** the algebraic direct sum used in the inherited graded manuscript. Only the finite retained state constructed next is placed in that direct sum. Also, (3) is nonlinear because of its normalization term; it is not a linear degree-shift operator on the whole moment state.

## 4. Finite sufficient closure by interpolation

### Theorem 1

For fixed known distinct κ_1,…,κ_N, the record R(w)=(M_0,…,M_{N−1}) determines w exactly. Every higher M_r is a fixed linear function of this record. Consequently (3) induces an exact finite closed ODE on the admissible image R(Δ_N°).

### Proof

For N≥2 choose v∈R^m so that a_j=v·κ_j are pairwise distinct. Such vectors exist: the forbidden set is the finite union of the proper hyperplanes v·(κ_j−κ_ℓ)=0. Define projected moments

\[
s_r=\langle v^{\otimes r},M_r\rangle
=\sum_jw_j a_j^r,\qquad 0\le r\le N-1.
\]

The Vandermonde matrix A=(a_j^r)_{0≤r≤N−1,1≤j≤N} is invertible. Equivalently, expand each Lagrange polynomial

\[
L_j(x)=\prod_{\ell\ne j}\frac{x-a_\ell}{a_j-a_\ell}
=\sum_{r=0}^{N-1}c_{jr}x^r.
\]

Since L_j(a_ℓ)=δ_{jℓ},

\[
\boxed{w_j=\sum_{r=0}^{N-1}c_{jr}s_r.}\tag{5}
\]

It follows for every ℓ≥0 that

\[
M_\ell=\sum_{r=0}^{N-1}
\left(\sum_jc_{jr}\kappa_j^{\otimes\ell}\right)s_r.\tag{6}
\]

In particular use (6) for M_N in the top equation of (3), and for any other required output. The record is a linear embedding of the aggregate simplex with the displayed linear inverse. Thus the closed ODE is exactly conjugate to (2) on its admissible image. This proves both closure and preservation of the record constraints by the resulting trajectories. Arbitrary tensor tuples outside this image are not declared valid states.

For N=1, w_1=M_0=1, q=κ_1, every M_r=κ_1^{⊗r}, and the dynamics vanish. Degree zero suffices because the single support point is known. This covers the degenerate case separately. □

### Constructivity and its limits

This is an explicit finite algebraic construction when the support admits exact arithmetic and equality tests. For example set v(t)=(1,t,…,t^{m−1}). Each pair difference defines a nonzero polynomial of degree at most m−1. With B=(m−1)N(N−1)/2, at least one t among 0,…,B separates all points. Testing this finite list and forming Lagrange coefficients yields the closure over rational or otherwise suitably decidable exact coefficient fields. For arbitrary unspecified real constants, the theorem gives existence and real-arithmetic formulas, not a general computability or bit-complexity guarantee.

No unknown-support recovery, noise tolerance, finite-sample inference, or stability bound is asserted. Interpolation can be ill-conditioned. N−1 is not asserted optimal: for affinely independent support points, M_1 already recovers the weights. Also, because 1_m·κ_j=1, contracting a tensor moment against 1_m recovers the preceding degree; the listed tuple is intentionally transparent and can contain redundant coordinates.

The finite state lies in \(\bigoplus_{r=0}^{N-1}\operatorname{Sym}^r(V)\), a declared finite graded subspace of the ordinary tensor algebra. Its mathematical sufficient information is exactly w. The theorem does not claim that the tensor coordinates compress w more efficiently than direct weight storage.

### A bounded worst-case sharpness statement

For N≥2 distinct collinear support points κ_j=(x_j,1−x_j) in Δ_2, the degree bound N−1 is necessary for injectivity within the family of moment records containing all degrees up to a cutoff. Indeed, the truncated Vandermonde matrix with rows 0,…,N−2 has a nonzero null vector h, while its degree-(N−1) row does not annihilate h because the full Vandermonde is invertible. In particular Σ_jh_j=0. For sufficiently small ε>0, w±=(1/N,…,1/N)±εh are positive laws. They agree in every scalar moment of degree at most N−2 and differ at degree N−1. Every component of κ_j^{⊗r} is a polynomial in x_j of degree at most r, so the full tensor records also agree through degree N−2. Theorem 2 then makes them continuation-distinct. Thus N−1 is worst-case sharp for this explicitly restricted moment-jet representation family. It is not the minimal degree for every support, nor a lower bound on arbitrary nonlinear or direct-weight encodings.

## 5. Exponential solutions and exact continuation equivalence

Put u(t)=∫₀ᵗg(s)ds. For an initial aggregate law w, define

\[
Z_w(u)=\sum_jw_j e^{-u\cdot\kappa_j}>0,
\qquad (T_uw)_j=\frac{w_je^{-u\cdot\kappa_j}}{Z_w(u)}.
\tag{7}
\]

Direct differentiation gives (2), including continuity across switches. Conversely, subtracting the logarithmic equations for any two positive weights determines their ratios, and normalization determines the weights, proving uniqueness. Every finite time has finite u(t), so all weights remain positive at finite time. There is no finite-time boundary loss for these controls. A weight may approach zero asymptotically.

The transformations satisfy T_aT_b=T_{a+b}, and

\[
q_w(u)=\sum_j(T_uw)_j\kappa_j=-\nabla_u\log Z_w(u).
\tag{8}
\]

Only the integrated control matters for an endpoint. Nevertheless different paths have their respective continuous output histories. Since controls can have either sign, every u∈R^m is reachable at any prescribed positive duration T by choosing g=u/T. Negative time is unnecessary. The gauge T_{u+c1}=T_u agrees with the intrinsic covector description.

### Theorem 2

For positive fine initial states p and p′ with the same known K, the following are equivalent:

1. Their aggregate weights on every identical-column class agree.
2. Their q outputs agree at every future time under every common piecewise-constant real control.
3. Their q outputs agree at every future time under every common constant real control.
4. For one v separating the distinct columns, their scalar responses y(t)=v·q(t) under the single constant control g=v agree for all t∈[0,ε], for any fixed ε>0.
5. Their initial moment records (M_0,…,M_{N−1}) agree.

### Proof

(1) implies (2) by (7), (2) implies (3), and (3) implies (4). Theorem 1 proves equivalence of (1) and (5).

For (4)⇒(1), write a_j=v·κ_j and z_w(t)=Z_w(tv)=Σ_jw_je^{−ta_j}. Equation (8) gives

\[
y_w(t)=-\frac{d}{dt}\log z_w(t).
\]

Equal scalar responses give equal logarithmic derivatives. Since z_w(0)=z_{w′}(0)=1, integration yields z_w(t)=z_{w′}(t) throughout [0,ε]. These finite exponential sums are smooth, so their right derivatives at zero, of orders r=0,…,N−1, agree:

\[
\sum_j(w_j-w'_j)(-a_j)^r=0.
\]

The Vandermonde matrix is invertible, hence w=w′. This also proves the elementary finite exponential independence needed here. N=1 is immediate. □

This is equality of exact continuous real responses on a nonzero interval. It is not equality of a finite list of sampled values, a statistical identification theorem, or a practical recovery guarantee. The existential separating direction and the algebraic reconstruction are separate from physically obtaining that response. Positivity is the standing Fisher-metric assumption; the finite exponential and Vandermonde argument itself also works for normalized nonnegative weights on the fixed support.

### Objective-driven versus externally controlled evolution

Each constant control is a single linear coarse objective; each piecewise-constant control changes that objective at declared times. There is no asserted common decreasing energy across arbitrary switches. Equation (3) also holds along a well-posed feedback flow g=∇J(q) for a chosen smooth objective, but the integrated u then depends on the trajectory. Equality of aggregate weights still preserves such trajectories under ordinary uniqueness hypotheses. The converse in Theorem 2 quantifies over the stated rich control family and need not hold for one fixed objective: J≡constant reveals only the initial q forever.

## 6. Exact first-moment failure and its two-moment repair

Take the channel columns (1,0), (0,1), (1/2,1/2), with

\[
p=(1/4,1/4,1/2),\qquad p'=(3/8,3/8,1/4).
\]

Both yield q=(1/2,1/2), while

\[
M_2(p)=\begin{pmatrix}3/8&1/8\\1/8&3/8\end{pmatrix},
\qquad
M_2(p')=\begin{pmatrix}7/16&1/16\\1/16&7/16\end{pmatrix}.
\]

For g=(1,0), their q velocities are (−1/8,1/8) and (−3/16,3/16). An exact q-only snapshot therefore fails to determine even the next correction.

There is a constructive finite repair. Let x be the first coordinate of a support point, so x∈{1,0,1/2}; put Q=E[x], S=E[x²], and λ=g_1−g_2. On this known support,

\[
x^3=\tfrac32x^2-\tfrac12x.
\]

Consequently the exact closed dynamics are

\[
\boxed{\dot Q=-\lambda(S-Q^2),\qquad
\dot S=-\lambda\bigl((\tfrac32-Q)S-\tfrac12Q\bigr).}\tag{9}
\]

The weights at x=1,1/2,0, in that order, are

\[
(2S-Q,\;4(Q-S),\;1-3Q+2S).\tag{10}
\]

Their strict positivity defines the admissible open triangle of moment states. Thus (Q,S) restores the information needed for every permitted continuation and is exactly the two-dimensional aggregate state in moment coordinates. The original two laws have S=3/8 and S=7/16 respectively. No unknown parameter or closure approximation is introduced.

A higher-order exact control confirms that immediate velocity sufficiency is weaker than continuation sufficiency. On x∈{0,1/3,2/3,1}, use weights w⁺=(5,9,3,7)/24 and w⁻=(7,3,9,5)/24. Their first and second moments coincide; their third moments differ by 1/54. Under λ=1, the first derivatives of Q coincide but the second derivatives differ by 1/54, since Q″=E[x³]−3QS+2Q³. This is a finite symbolic control, not a sampling experiment.

## 7. Optional sharp criterion for q-only descent

### Proposition 3

On the entire positive aggregate simplex, (4) is a well-defined function of (q,g) for every g if and only if the distinct support points κ_j are affinely independent. This criterion concerns existence of some descended q dynamics, not equality with the separately prescribed canonical coarse Fisher metric.

### Proof

Affine independence makes w uniquely determined by q, so M_2 and the dynamics descend.

Conversely, let A have columns (1,κ_j), and let V be its row span, viewed as functions on the N support points. For any h∈ker A, small positive and negative perturbations of a strictly positive law by h remain positive and have the same q. Descent for every g then gives Σ_jh_jκ_jκ_jᵀ=0. Therefore every coordinate product x_ax_b annihilates ker A, so belongs to V. Since V is spanned by 1 and coordinate functions, V is closed under pointwise multiplication. It contains the separating function a_j=v·κ_j; hence it contains every Lagrange polynomial L_j(a), that is, every coordinate indicator δ_j. Thus V=R^N and A has column rank N, proving affine independence. □

This explains precisely when the first grade is enough, while Theorem 1 gives a finite sufficient replacement when it is not. It does not say every pair with the same q has different immediate velocities, nor does it replace Theorem 2's future distinction with an immediate one.

## 8. Source-faithful bridge and limits of the quotient

The exact inherited graded source is [INHERITED_GRADED_INTERFACE.md at CP08, pin 7efc6217](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/INHERITED_GRADED_INTERFACE.md), Git blob c094a9c44fae26484426df67ac5afd9e2190eb4d, identical to the retained H-formalisation manuscript. Its §§3–4 declare the algebraic tensor algebra and fibre-based adequacy; §5 exhibits consequential higher-order information; §6 types contractions and warns that contraction can erase a required distinction; §11 requires updates and relevant observables to descend together for future-safe compression.

Here those obligations have concrete witnesses: the numerical type V, the finite symmetric moment state, the explicitly declared covector contraction, the exact nonlinear moment dynamics, and the inverse (5). For each finite tilt T_u, equal retained moment records give equal retained records after T_u and equal q outputs. The set-theoretic future-safe quotient criterion therefore applies to this deterministic state update and declared q target. No inquiry landscape has been specified, so preservation of such an additional component is not claimed. The full infinite hierarchy is not silently inserted into the inherited algebraic direct sum, and no workflow composition is identified with tensor multiplication.

The pinned [H-ICS v5 manuscript](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex) explicitly distinguishes constancy of an answer on a record fibre (lines 53–60), determination of an output law (200–226), and observation congruence under operations (236–255). The present q counterexample is exactly a failure of fibre preservation by an admitted update, followed by an explicit sufficient refinement. However, the present state space and control repertoire are continuous. The manuscript's finite-state, finite-repertoire belief-state decision theorem is not imported; this note directly proves its own continuation equivalence.

The earlier [H-Continuation supplement, §5 and Theorem 2](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-continuation/continuation_complete_orthing.md) already formalizes closure of required observable spaces under specified finite action–observation instruments, exact moment sufficiency, and closed predictive updates. That is positive internal ancestry for the continuation-preservation obligation. The normalized real-controlled tilt system here is separately defined and proved; no finite-instrument theorem, dimension lower bound for unrestricted encoders, or branch-probability interpretation is transferred without its premises.

The previous fixed-reference packet uses a metric independent of p. Its projected fine field automatically depends only on q, so its quotient construction remains correct. This note changes the metric to the actual evolving Fisher metric. Its p-dependent covariance can fail to factor through q. Replacing a fixed reference by a current state is a new geometric problem, not a correction to the earlier theorem.

Finally, the equivalence in Theorem 2 is **relative to precisely these controls and this output**. Equal numerical channel columns do not identify source tokens, evidence events, carriers, or provenance. Individual-source withdrawal, named-token interventions, extra outputs, channel revision, or other authorized operations may distinguish states that the tilt/q interface merges. Those operations require their own preservation test; this result does not authorize deleting their records. The tensor state supplies exact sufficient information for the declared numerical correction, not authentication, actual noetic realization, target truth, epistemic warrant, or permission to act.

## 9. Classical ancestry and verification scope

[Harper, *Information Geometry and Evolutionary Game Theory*](https://arxiv.org/abs/0911.1383), §§2.2–3.1 and 3.5, explicitly connects the categorical Fisher/Shahshahani metric with replicator gradients and exponential-family solutions. [Karev, *Replicator Equations and the Principle of Minimal Production of Information*](https://doi.org/10.1007/s11538-009-9484-9), preprint §§3–4, gives normalized exponential solutions, partition functions, and covariance/Price-equation evolution of trait expectations. Equation (3) is the tensor-moment specialization of that classical covariance calculation. These targeted source sections were inspected; no entire-literature review or novel general replicator theorem is claimed.

Finite Vandermonde/Lagrange interpolation and independence of distinct finite exponentials are elementary classical algebra, proved above where used. The inherited fibre and continuation principles are positively credited, rather than inferred absent from narrower later packets.

`verify.py` executes 21 exact SymPy control groups for the displayed identities, duplicate grouping, normalization and composition of tilts, interpolation, finite closure, control-gauge invariance, rank/affine-independence cases, and the stated countermodels. The executed results are in `verification.txt`. These finite checks supplement the ordinary general proofs and do not prove them by enumeration. All calculations are symbolic or rational; no numerical sampling, empirical result, formal-kernel certificate, protected-source change, or closure status is claimed.
