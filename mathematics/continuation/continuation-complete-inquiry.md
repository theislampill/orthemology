---
title: "Continuation-Complete Orthings"
subtitle: "Sharp information loss, minimal predictive memory, and safe strategic composition"
author: "Research synthesis developed with the Orthemology project owner"
date: "8 September 2026 — research supplement v1"
abstract: |
  This supplement strengthens the previous representation-first formalisation by asking what information a witnessed discharge must retain for the inquiries it leaves available. In a declared finite reference model, a duality theorem identifies the exact worst-case error left by a moment summary and produces indistinguishable countermodels. An action–observation closure constructs the least space of observables required by future inquiries. Its dimension, minus the known constant, is the exact minimum number of continuous real coordinates needed for universal exact prediction over all state laws. For a family of pairwise updates on binary states, this cost is computed exactly at every horizon and reaches an exponential value. An approximation bound shows that this obstruction is not confined to zero-error requirements for linear moment summaries. The same missing interaction can alter a future safety verdict and the unique equilibrium of a declared game. Additional results separate strategic incentives from joint feasibility and quantify a restricted coordination requirement. Fluid dynamics supplies the methodological problem of unresolved interactions and memory; the theorems contribute to Orthemology, not to solving Navier–Stokes. The general ingredients have substantial prior art. The contribution is a scoped mathematical extension and a sharpened research candidate, not an independently confirmed novelty or meniscus claim.
---

# Central contribution and unchanged boundary

The problem addressed here is not whether Orthemology can describe a fluid proof. It is whether a representation of an orthing can discard information while retaining the capacity to answer every future inquiry that its own governance still permits.

The previous manuscript, *Graded Representations, Witnessed Revision, and Inquiry Landscapes* [R1], supplied finite typed representations, obligation-retention witnesses, an optional finite-game layer, and a deterministic future-safe quotient criterion. The present supplement takes its stated stochastic extension forward. It constructs an explicit test for future informational adequacy, computes its exact cost in a nontrivial finite family, and derives consequences for strategic assessment and joint safety.

The headline is unchanged:

$$
\mathsf{Orthing}_A,\qquad e\in E_A,\qquad
\rho_A:E_A\longrightarrow T_{\mathcal T}(V).
$$

An episode is not its tensor representation. Each represented episode has finite typed support. No result below gives an intrinsic tensor ontology, a universal tensor degree, or an unbounded-degree theorem about actual episodes. Nor does it promote a representation arm or identify anything with controller G.

**The proposed strengthening.** Historical traceability of a discharged item is necessary where the record contract requires it, but is not by itself sufficient for future operational use. Within a declared reference model, the retained information must also determine—or bound to the declared tolerance—the consequences of the continuations that remain authorised. Otherwise the procedure must reacquire information, refine its representation, narrow its certified inquiry scope, or hold the affected claim.

This is a stronger condition on *what witnessed discharge guarantees*, not a replacement for the existing record and authority conditions.

## Input basis and status

The inputs are the supplied conversation and its corrections; the delivered v1 manuscript and verification package [R1]; the supplied Fefferman problem statement, including its errata [F1]; the supplied 107-page Euler manuscript [F2]; and targeted repository reads at commit `f50dc1aee52356cc6adbef342387576b02afc124` [R2–R5]. Earlier claims in the conversation are treated as proposals to check, not as proof authority.

Fefferman's file states a problem, not a Navier–Stokes solution. Its breakdown alternatives allow appropriately regular forcing with positive viscosity. The supplied Euler paper explicitly leaves quantitative certifications outstanding. Nothing in this supplement assumes that an announced Euler result, an eventual NS extension, or any conjectured physical singularity has been independently established here.

External mathematical sources were used for comparison with existing moment duality, predictive-state, invariant-observable, and game-abstraction methods [P1–P9]. Source-derived statements and the deductions proved here are kept distinct. The general mathematics is not claimed as newly invented.

## The actual step beyond the previous draft

The following three questions are now answered for one expressly finite, fully specified model class.

**How much information was lost?** An exact minimax defect, computable by linear programming, measures the inability to recover a selected future expectation. Its dual returns two reference laws that agree on everything retained but disagree on that future consequence.

**What is the smallest sufficient information space?** Close the required observables under the permitted action–observation operators. The resulting space gives both an explicit predictive representation and a sharp lower bound against all continuous encoders that must work for every reference law.

**Can pairwise operations justify a permanently pairwise summary?** No. A concrete family of binary, pairwise operations has a horizon-dependent minimal predictive dimension

$$
\boxed{
 d_{\min}(n,h)=\sum_{k=1}^{\min(n,h+1)}\binom nk.
}
$$

At horizon $n-1$ this is $2^n-1$. The result concerns a summary of an uncertain law, not a fully observed $n$-bit sample. This distinction is essential to the theorem.

# From fluid reduction to an Orthemological obligation

## Why eliminating a component can create a new obligation

The relevant fluid-mechanical lesson is that omission need not commute with evolution. A reduced model may require additional effective interactions or memory to preserve the influence of variables it no longer carries. Mori–Zwanzig methods explicitly study this problem [P4]. The following calculation is an independent elementary illustration, not an NS theorem.

Consider

$$
\dot x=-ax+bxy,\qquad
\varepsilon\dot y=-y+cx^2,\qquad\varepsilon>0.
$$

Variation of constants gives the exact identity

$$
y(t)=e^{-t/\varepsilon}y(0)
 +\frac c\varepsilon\int_0^t e^{-(t-s)/\varepsilon}x(s)^2\,ds.
$$

Substitution into the first equation removes the explicit variable $y$, but leaves a dependence on its initial value and on the past of $x$. The formal algebraic limit $\varepsilon=0$ instead gives $y=cx^2$ and the reduced equation

$$
\dot x=-ax+bcx^3.
$$

That limit requires its own approximation argument. Simply deleting $y$ and retaining $\dot x=-ax$ has no such justification. Lower state dimension can accompany higher effective polynomial degree; neither quantity is the tensor degree of an episode record.

There is an analogous exact algebraic issue in incompressible NS. On a common interval where a finite family of solutions $u^s$ is smooth, let $\pi_s$ be fixed probabilities and define

$$
\bar u=\sum_s\pi_su^s,\qquad
R=\sum_s\pi_s(u^s-\bar u)\otimes(u^s-\bar u).
$$

Averaging the equations, using incompressibility and
$\sum_s\pi_su^s\otimes u^s=\bar u\otimes\bar u+R$, yields

$$
\partial_t\bar u+(\bar u\cdot\nabla)\bar u
 =\nu\Delta\bar u-\nabla\bar p+\bar f-\nabla\cdot R.
$$

A mean representation alone need not determine the extra covariance term. This is a derivation from the equations in [F1], not a use of an unproved blowup claim.

The direction of transfer is now precise: **Orthemology's discharge rule needs a way to identify missing continuation-relevant interactions, rather than only a record saying that a component was discharged.** The finite results below provide one such way.

## Discovery is not the certificate

Page 33 of the supplied Euler manuscript [F2] separates numerical discovery, a spline representation, interval certificates, and a stability argument. Its low/high-energy discussion and residual margin motivate looking for *explicit error certificates* instead of trusting a promising approximation. They do not themselves supply a model of noetic or agentic dynamics.

Here the analogue is operative: a learned representation may propose features, but a finite dual problem can either certify a stated prediction error or exhibit an indistinguishable pair that defeats it. The finite reference-model certificate remains distinct from evidence that the model correctly describes a particular agent, person, or external system.

# Objects, contracts, and the quantity being compressed

Fix a declared analysis $A$ and a finite nonempty reference state set $X$. An element $x\in X$ represents a possible configuration in the selected model. A probability law $\lambda\in\Delta(X)$ is a belief or ensemble law according to a separately declared interpretation. It is not the configuration itself and is not automatically an empirical frequency distribution.

The representation problem in this supplement is compression of $\lambda$ for declared questions about future behaviour. It is not compression of a fully observed point $x$. For example, a point in $\{-1,+1\}^n$ is determined by its $n$ coordinates, whereas the $n$ coordinate means of a law do not determine its joint distribution.

Let $\mathscr F_A\subseteq\mathbb R^X$ be a finite set of required terminal observables. Depending on the application, these may include target indicators, failure indicators, prerequisites, witness/disposition predicates, or payoff differences. Adding a predicate to this set does not prove that its interpretation is correct. Its source, version, and reference meaning must be supplied independently.

The tensor representation $\rho_A(e)$ can carry the features, coefficients, certificates, and records used below, but the feature space is a separate mathematical object. To avoid confusing it with the factor space $V$ of the tensor algebra, denote the retained observable space by

$$
\mathscr V\subseteq\mathbb R^X,\qquad 1\in\mathscr V.
$$

If $\phi_0=1,\phi_1,\ldots,\phi_d$ is a basis, the informative moment summary is

$$
m_{\mathscr V}(\lambda)
 =\bigl(\langle\lambda,\phi_1\rangle,\ldots,
         \langle\lambda,\phi_d\rangle\bigr),
\qquad
\langle\lambda,f\rangle=\sum_x\lambda(x)f(x).
$$

The constant coordinate is known to equal one. The choice of basis does not change which expectations the summary determines. A nonlinear decoder of these moments is allowed throughout the next theorem.

The full-simplex assumption is load-bearing. A product-law assumption, a fixed parametric family, or a known finite set of attainable beliefs can greatly reduce the necessary information. Such restrictions must be justified rather than silently assumed.

# Sharp information loss: a certificate or a countermodel

**Theorem 1 — Exact defect of a moment summary.** For finite $X$, a linear space $\mathscr V$ containing constants, and $f\in\mathbb R^X$, define

$$
d_{\mathscr V}(f)=\min_{g\in\mathscr V}\|f-g\|_\infty.
$$

Then

$$
\begin{aligned}
d_{\mathscr V}(f)
&=\frac12\max_{\substack{\lambda,\lambda'\in\Delta(X)\\
                    m_{\mathscr V}(\lambda)=m_{\mathscr V}(\lambda')}}
       |\langle\lambda-\lambda',f\rangle|\\
&=\inf_{\psi}\sup_{\lambda\in\Delta(X)}
       |\langle\lambda,f\rangle-\psi(m_{\mathscr V}(\lambda))|.
\end{aligned}
$$

The infimum is over all real-valued decoders on the attained summary image, not merely linear or continuous decoders. In particular, universal exact recovery holds if and only if $f\in\mathscr V$.

*Proof.* For every $g\in\mathscr V$ and every pair with equal summaries,

$$
|\langle\lambda-\lambda',f\rangle|
=|\langle\lambda-\lambda',f-g\rangle|
\le2\|f-g\|_\infty.
$$

Also, $\lambda\mapsto\langle\lambda,g\rangle$ is computable from the retained moments and has error at most $\|f-g\|_\infty$. This proves both required upper bounds.

Finite-dimensional norm duality, equivalently linear-programming duality, gives

$$
d_{\mathscr V}(f)=
\max\{\langle v,f\rangle:v\perp\mathscr V,\ \|v\|_1\le1\}.
$$

For positive distance, a maximiser has $\|v\|_1=1$: otherwise rescaling would improve the positive objective. Since $1\in\mathscr V$, $\sum_xv(x)=0$, so the positive and negative parts each have mass $1/2$. Set $\lambda=2v_+$ and $\lambda'=2v_-$. They are probability laws with the same retained moments and separation $2d_{\mathscr V}(f)$. Every decoder outputs the same number for this pair and therefore incurs error at least half their separation. For zero distance all equalities are immediate. This also proves exact recovery iff membership, since finite-dimensional subspaces are closed. $\square$

This theorem is a finite-space specialisation of established approximation/moment-matching duality; [P1, Lemma 25] gives a closely related probability-measure statement. Its use here is as a *continuation-discharge certificate*, not as a new general duality theorem.

## An executable specification

Write the basis evaluations as rows of a matrix $\Phi$. The primal certificate solves

$$
\min_{a\in\mathbb R^{d+1},\,t\ge0}t\quad\text{subject to}\quad
-t\le f(x)-\sum_ja_j\phi_j(x)\le t\quad\text{for all }x,
$$

where only $t$ is constrained nonnegative; the coefficients $a_j$ are unrestricted. The matching countermodel programme maximises

$$
\tfrac12\langle\lambda-\lambda',f\rangle
$$

subject to equal moments, nonnegative entries, and unit masses. Rational data admit rational basic certificates. A floating-point optimiser may propose them; their inequalities and equalities can then be checked exactly, as in the supplied script.

For a binary failure indicator $f$, the defect lies in $[0,1/2]$. A defect of $1/2$ is maximal ambiguity: two laws compatible with the retained information assign failure probabilities zero and one.

## Local certificates can be stronger than universal ones

For a particular attained summary $y$, define

$$
\mathcal P(y)=\{\lambda\in\Delta(X):m_{\mathscr V}(\lambda)=y\}.
$$

For an inquiry or protocol $c$ with failure observable $b_c\in[0,1]^X$, compute

$$
\underline r(y,c)=\min_{\lambda\in\mathcal P(y)}\langle\lambda,b_c\rangle,
\qquad
\overline r(y,c)=\max_{\lambda\in\mathcal P(y)}\langle\lambda,b_c\rangle.
$$

Both are finite linear programmes. A global positive defect does not preclude a safe local fibre. The global theorem concerns a promise to work for *all* laws; the local interval concerns this retained record. Statistical uncertainty in measured moments must enlarge the feasible set, for example to interval constraints on $\Phi\lambda$, rather than treating noisy moments as exact.

# Continuation completion, including observations and feedback

## Action–observation instruments

Let the permitted actions $a$ and observations $o$ range over finite sets. A model step is given by a nonnegative matrix

$$
K_{a,o}(x,x'),\qquad
\sum_{o,x'}K_{a,o}(x,x')=1.
$$

Thus $K_{a,o}$ is sub-stochastic, and $\lambda K_{a,o}$ is the unnormalised successor law for the branch in which observation $o$ occurs after action $a$. The action on observables is

$$
(K_{a,o}f)(x)=\sum_{x'}K_{a,o}(x,x')f(x').
$$

A blocked attempt can be represented by an explicit refusal state and observation. This does not license the prohibited action or make refusal a successful completion. It lets the model preserve the distinction rather than omitting it. More restrictive, history-dependent permissions can be represented by a finite controller state or by an expressly smaller set of permitted action–observation words.

For a word $w=((a_1,o_1),\ldots,(a_k,o_k))$, write $K_w=K_{a_1,o_1}\cdots K_{a_k,o_k}$. Then $\langle\lambda,K_w1\rangle$ is the branch probability, and $\langle\lambda,K_wf\rangle$ is the likelihood-weighted terminal expectation.

Define

$$
\mathscr C_0=\operatorname{span}(\{1\}\cup\mathscr F_A),\qquad
\mathscr C_{h+1}=\mathscr C_h+
       \sum_{a,o}K_{a,o}\mathscr C_h.
$$

All sums here are sums of linear subspaces. These spaces are not themselves sets of admissible inquiries; they are the observable spans required to evaluate a declared family of inquiries. The distinction avoids turning $\mathcal L_t$ into a vector subspace.

**Theorem 2 — Continuation completeness and minimal predictive memory.** In the above finite model:

(a) $\mathscr C_h$ is exactly the span of $K_wf$ for words of length at most $h$ and $f\in\{1\}\cup\mathscr F_A$.

(b) A moment summary $m_{\mathscr V}$ permits exact evaluation of all those branch probabilities and terminal numerators, for every law, if and only if

$$
\boxed{\mathscr C_h\subseteq\mathscr V.}
$$

(c) This suffices for the corresponding bounded adaptive policy trees: their branch-weighted values are finite sums of the same kind of functions. Conditional terminal expectations are recoverable on branches of positive probability.

(d) The hierarchy stabilises at a least common invariant space $\mathscr C_\infty\subseteq\mathbb R^X$. There are at most $|X|-\dim\mathscr C_0$ strict dimension increases. Its basis gives closed, unnormalised predictive updates.

(e) Put $r_h=\dim\mathscr C_h$. Among all continuous encoders $E:\Delta(X)\to\mathbb R^d$ that allow exact recovery of every required horizon-$h$ expectation for all laws, even with arbitrary nonlinear decoders, the minimum possible $d$ is

$$
\boxed{d_{\min}=r_h-1.}
$$

*Proof.* Part (a) follows by induction, separating the first step of each word. Part (b) follows from Theorem 1 applied to the spanning family. Necessity refers to preservation of every specified branch numerator and probability, not only a single unconditional final score.

For (c), a deterministic adaptive policy tree chooses an action at each observed history. Each leaf contributes $K_wf$ for its realised branch; summing leaves gives its expected value. Randomised policies add the corresponding finite convex combinations. Conditioning divides by $\langle\lambda,K_w1\rangle$ when this is positive; no posterior assertion is made at zero probability.

For (d), the increasing sequence of dimensions is bounded by $|X|$. If $\mathscr C_{h+1}=\mathscr C_h$, that space is invariant under every $K_{a,o}$, so the hierarchy cannot grow later. Any invariant subspace containing the initial contract contains every $\mathscr C_h$, proving minimality. If $B$ is a row-basis evaluation matrix, invariance supplies matrices $M_{a,o}$ with

$$
B K_{a,o}^{\mathsf T}=M_{a,o}B.
$$

Thus $B(\lambda K_{a,o})^{\mathsf T}=M_{a,o}B\lambda^{\mathsf T}$. At a non-stabilised finite horizon, the analogous map goes from $\mathscr C_h$ coordinates to $\mathscr C_{h-1}$ coordinates; a fixed horizon space must not be called invariant prematurely.

For (e), a basis $1,f_1,\ldots,f_{r_h-1}$ gives the continuous encoder of $r_h-1$ expectations, proving the upper bound. For the lower bound, the evaluation vectors $(1,f_1(x),\ldots,f_{r_h-1}(x))$ span an $r_h$-dimensional row space. Choose $r_h$ states with independent such vectors. Their nonconstant evaluation vectors are affinely independent. The simplex of laws supported on these states therefore has dimension $r_h-1$, and all the required expectations together distinguish its points. Any exact encoder must be injective on that simplex.

If $d<r_h-1$, restrict the encoder to the relative interior of the simplex, identify this interior with an open subset of $\mathbb R^{r_h-1}$, and include $\mathbb R^d$ in $\mathbb R^{r_h-1}$ by zero-padding. The resulting continuous injection would have open image by invariance of domain [P5, Theorem 2B.3], yet its image lies in a lower-dimensional coordinate plane with empty interior. Contradiction. The zero-dimensional case is immediate. $\square$

The invariant-span and predictive-update mechanism has strong ancestry in predictive-state representations [P2], feedback/options extensions [P3], and invariant-observable methods [P6]. Theorem 2 does not rebrand those theories as a new general invention. It specialises them to an explicit continuation contract and combines them with the exact defect and dimension results needed for this discharge question.

## What the theorem does and does not preserve

To preserve a reference-model safety probability, include its event observable. To preserve an authorised action's prerequisite, include that prerequisite. To preserve game incentives, include the relevant unilateral gain functions. A span built only from answer correctness does not mysteriously preserve reason provenance or authority. The predicate families and their semantics remain declared inputs.

Reward-predictive state representations [P9] are an especially close antecedent: they already show why preserving observation predictions need not preserve rewards, and augment the predictive representation accordingly. Replacing rewards by several declared contract functions is not, on its own, a new general principle. The sharper scope here is the full-law minimax defect, horizon-dependent exact and approximate memory bounds, and augmentation costs used to assess discharge.

The minimal dimension is a count of exact continuous real coordinates, not a count of bits, stored words, persons, physical degrees of freedom, or tensor factors. It does not cover discontinuous encoders with unbounded exact precision. It also does not assume that every law is reachable from one fixed starting condition: the theorem deliberately quantifies over the full declared simplex. Restricting that class is an explicit and potentially useful way to reduce the bound.

# A sharp horizon law for pairwise interaction dynamics

The next construction turns T300's static higher-order warning [R4] into a dynamic and quantitative obstruction. Its reference system is finite and contains no PDE singularity.

Let

$$
X_n=\{-1,+1\}^n,\qquad n\ge2,
$$

and permit every local update $F_{ij}$ with $i\ne j$:

$$
F_{ij}(x)_i=x_ix_j,\qquad
F_{ij}(x)_k=x_k\quad(k\ne i).
$$

Each update touches two coordinates and is its own inverse. Observations carry no new information; there is one trivial observation per action. The initial contract contains the unary observables $x_1,\ldots,x_n$ and the constant. A horizon counts elementary updates, not simultaneous rounds of an unrestricted parallel circuit.

For $S\subseteq\{1,\ldots,n\}$ define the Walsh character

$$
\chi_S(x)=\prod_{i\in S}x_i,\qquad \chi_\varnothing=1.
$$

**Theorem 3 — Exact horizon, interaction, and memory spectrum.** For this declared model,

$$
\boxed{
\mathscr C_h=
\operatorname{span}\{\chi_S:|S|\le\min(n,h+1)\}.
}
$$

Consequently,

$$
\boxed{
\dim\mathscr C_h=\sum_{k=0}^{\min(n,h+1)}\binom nk,
\qquad
 d_{\min}(n,h)=\sum_{k=1}^{\min(n,h+1)}\binom nk.
}
$$

The second equality is the exact minimum continuous summary dimension over all laws in Theorem 2, not only the number of coordinates used by this particular Walsh representation.

*Proof.* Direct calculation gives

$$
\chi_S\circ F_{ij}=
\begin{cases}
\chi_{S\triangle\{j\}},&i\in S,\\
\chi_S,&i\notin S.
\end{cases}
$$

A pullback therefore raises character degree by at most one. Starting from unary characters, every character reached within $h$ steps has degree at most $h+1$. Conversely, for any nonempty $S$ of cardinality $k$, select an accumulating coordinate $i\in S$ and successively multiply it by every other coordinate of $S$. After $k-1$ updates its value is $\chi_S$. Thus all the listed characters are reachable.

Walsh characters are linearly independent: under the uniform law their inner product is zero for distinct subsets and one for equal subsets. Counting subsets gives the first dimension formula; Theorem 2 gives the continuous-encoder lower bound and attainment. $\square$

For eight binary factors, the exact costs are:

| Permitted elementary-update horizon $h$ | Maximum generated character degree | Required continuous coordinates |
|:--|:--|--:|
| 0 | 1 | 8 |
| 1 | 2 | 36 |
| 2 | 3 | 92 |
| 3 | 4 | 162 |
| 7 or more | 8 | 255 |

**Interpretation.** A system may truthfully retain all current unary expectations, and every permitted update may be pairwise, while preserving the entire future inquiry menu eventually requires all $2^n-1$ degrees of freedom of an arbitrary probability law. Local interaction rules do not justify a permanently local statistical summary.

This is not a theorem that real orthing episodes possess exponentially many essential ontological constituents. It is an exact obstruction to a specified architecture: a fixed small continuous summary of arbitrary joint uncertainty, no reacquisition, and a promise to answer every unary inquiry after every allowed local-update sequence.

## A maximally separating continuation

Define two laws

$$
\lambda_\pm(x)=2^{-n}(1\pm\chi_{[n]}(x)).
$$

They are uniform on opposite parity classes. For every proper subset $S\subsetneq[n]$, their $\chi_S$ expectations agree. Equivalently, all proper-subset marginals agree. This is the standard parity mechanism underlying [R4].

Apply the updates $F_{12},F_{13},\ldots,F_{1n}$ and then ask the unary question whether the first coordinate is negative. Its pulled-back failure indicator is

$$
b(x)=\frac{1-\chi_{[n]}(x)}2.
$$

The answers are

$$
\langle\lambda_+,b\rangle=0,
\qquad
\langle\lambda_-,b\rangle=1.
$$

Even retaining *all proper-subset moments* gives defect $d_{\mathscr V}(b)=1/2$. The constant approximation $1/2$ achieves that error, and the two laws prove that no decoder does better universally.

The missing correlation was not invented by the future update; the update made an already-hidden relation decisive for an ordinary unary assessment. This is the precise sense in which a discharged high-order distinction can return as a low-order obligation.

A synthetic Orthemological reading is composition of binary-preserving or binary-reversing transformations. Each transformation can preserve or reverse a selected property; composing two multiplies their signs. A later route asks the resulting sign. This is a finite formal pipeline example, not evidence about human cognition, restoration, or a physical implementation.

## The obstruction is not confined to exact equality

Let $m_h=d_{\min}(n,h)$, and consider the $m_h$ distinct nonconstant characters required at horizon $h$. The corresponding binary questions are $b_S=(1-\chi_S)/2$.

**Proposition 4 — Approximate memory lower bound for moment summaries.** Suppose a summary retains $d$ independent nonconstant linear moments, with arbitrary decoder functions afterwards. If every required $b_S$ expectation can be approximated for every law with absolute error at most $\epsilon$, then

$$
\boxed{d\ge m_h(1-4\epsilon^2).}
$$

The meaningful range is $0\le\epsilon\le1/2$; take the integer ceiling when a coordinate count is required. This is a necessary bound, not an asserted exact optimum at intermediate tolerances.

*Proof.* Use the uniform-law inner product and let $P$ be the orthogonal projection onto $\mathscr V$. Since constants belong to $\mathscr V$ and the selected characters are orthogonal to constants, their projections use at most $d$ nonconstant dimensions. The trace/Bessel inequality gives

$$
\sum_{S}\|P\chi_S\|_2^2\le d,
\qquad
\sum_S\|\chi_S-P\chi_S\|_2^2\ge m_h-d.
$$

For some $S$, the squared $L^2$ projection error is at least $1-d/m_h$. Uniform approximation error is at least best $L^2$ approximation error. Constants in $\mathscr V$ also give

$$
d_{\mathscr V}(b_S)=\tfrac12d_{\mathscr V}(\chi_S).
$$

Theorem 1 therefore implies

$$
\epsilon\ge\frac12\sqrt{\max(0,1-d/m_h)}.
$$

Rearrangement proves the claim. $\square$

At $n=8$ and horizon at least seven, error at most $0.1$ for every required event probability needs at least $245$ linear moment coordinates, even if the downstream decoders are nonlinear. Exact continuous encoders need $255$. The approximate statement is deliberately narrower: it is not a lower bound for arbitrary approximate nonlinear encoders.

# What changes in witnessed discharge and inquiry landscapes

## A continuation-sensitive discharge condition

The previous record invariant requires initially recorded obligations to remain historically traceable through a finite chain [R1, Theorem 6.5]. Retain it. Add a distinct *operational certificate* for a proposed reduction from an accessible information space to $\mathscr V'$:

$$
\operatorname{ContExact}_{A,h}(\mathscr V')
\quad\Longleftrightarrow\quad
\mathscr C_h\subseteq\mathscr V'.
$$

This is an exact characterisation in the declared finite model, not a requirement that every practical episode retain all possible information. The contract can instead name a smaller inquiry family or tolerate specified error. For a finite normalised list of actual continuation questions $\mathscr Q_h$, define

$$
\Delta_{A,h}(\mathscr V')
 =\max_{f\in\mathscr Q_h}d_{\mathscr V'}(f).
$$

The maximum is over the actual question family, not the entire unbounded linear span. Scaling arbitrary elements of a deficient span would make a numerical defect meaningless or infinite. Zero defect is equivalent to containing that family's span; positive defect gives a sharp worst-case error for at least one named question.

A full discharge witness should therefore contain, in addition to the existing source and disposition record: the model and contract versions; the accessible statistic; the authorised continuation family and horizon; a zero-defect proof or quantified error certificate; and an explicit reacquisition route or inquiry restriction where exact preservation fails. A stored archive that the continuation can genuinely retrieve is part of accessible information and must be included in the model. An inaccessible hash or a historical reference is not automatically such access.

Transfer and supersession remain distinct from resolution. They can move ownership or active representation without proving that the underlying issue no longer matters. A tensor contraction is just the algebraic operation; its continuation certificate is what establishes the declared operational consequence.

## Objective possibilities versus certifiable possibilities

Keep the historical ecology $\Gamma_t^\mu$ separate from the objective prospective landscape $\mathcal L_A(x)$, where the latter is supplied by the reference model and includes its feasibility and authorisation conditions. A third object is required when information is incomplete:

$$
\widehat{\mathcal L}^{\mathrm{cert}}_{A,\epsilon}(y)
 =\{c:\text{the declared permission checks pass and }
                     \overline r(y,c)\le\epsilon\}.
$$

This is the set of continuations certifiable from the retained information, not a replacement definition of what is physically or logically possible. If a sound uncertainty set contains the reference law, the certified risk bound applies to it. The premise that the reference law lies in that uncertainty set remains independent evidence.

For example, the parity continuation may objectively have failure probability zero under $\lambda_+$, yet be uncertifiable from its proper marginals because $\lambda_-$ remains compatible with those marginals. The action has not become physically impossible; its safe execution is not warranted by that summary.

**Corollary 5 — No silent preservation of the future option set.** In the model of Theorem 3, retaining fewer than $d_{\min}(n,h)$ continuous coordinates cannot preserve every horizon-$h$ future expectation for every law. A procedure that makes such a reduction must give up at least one premise: universal law coverage, exactness, unchanged continuation menu, absence of information reacquisition, or the chosen memory bound.

This is an impossibility result, not a recommendation to retain everything forever. Its positive use is to make the trade-off explicit and to identify the particular missing question or relation by Theorem 1.

## An implementable certify–refine rule

Given a proposed summary and a newly live continuation, first form its reference-model pulled-back observable. Solve the finite approximation or local fibre programme. If the certificate meets the declared threshold, carry the claim only with that certificate and its scope. Otherwise the dual provides a concrete separating pair. A refinement can add a differentiating observable, add a permitted query that resolves the pair, restore an accessible archived component, or explicitly limit the affected continuation.

For exact full-law coverage, adding one missing observable raises the retained span dimension by at least one. Continuing under the declared instruments terminates at $\mathscr C_\infty$ after finitely many strict increases. This is an existing invariant-span computation used as a concrete Orthemological repair operation, not a claim that real-world scientific inquiry or noetic restoration must terminate.

Expanding the permitted continuation menu can increase the required rank without changing $A$ when the analysis already parameterises that menu. Revising the analysis is a separate event. Likewise, restricting the menu can reduce the memory obligation while sacrificing useful opportunities. The value of those opportunities is not their count or their rank; valuation remains separately declared, as in [R1].

# Strategic consequences of the same missing interaction

## Equilibrium can be wrong because the reference game is not identified

Nash existence does not supply the missing payoff information. The parity construction makes this point on exactly the same continuation system, rather than introducing a separate fluid game.

After the accumulating updates, let $B=(1-x_1^{\mathrm{final}})/2$. Under $\lambda_+$ it is certainly zero; under $\lambda_-$ it is certainly one. Declare two players with actions $s_i\in\{0,1\}$ and payoffs

$$
U_i(x,s)=\mathbf1\{s_i=B(x)\}
       +c\,\mathbf1\{s_1=s_2\},\qquad 0<c<1.
$$

The first term rewards matching the reference outcome; the second rewards coordination. This is a declared synthetic strategic layer. It does not assert that an external fact is a player or that actual people have these utilities.

**Proposition 6 — A strategically decisive hidden continuation.** The reference game under $\lambda_+$ has unique equilibrium $(0,0)$; the game under $\lambda_-$ has unique equilibrium $(1,1)$. Any extraction rule that sees only their common proper-subset moments returns the same represented game or strategy recommendation for both and cannot recover both reference equilibria correctly.

For any fixed independently mixed recommendation $p=(p_1,p_2)$, each player has regret at least $(1-c)/2$ in at least one of the two reference games.

*Proof.* When $B$ is deterministic, switching from the incorrect action to $B$ gains at least $1-c>0$, regardless of the opponent. The correct action is strictly dominant, proving uniqueness. Equal input summaries cannot be deterministically decoded as two distinct equilibrium sets.

For player $i$, the wrong-action probabilities in the two games are $p_i$ and $1-p_i$. Deviation to the correct action improves expected payoff by at least $(1-c)$ times the respective wrong-action probability. Their maximum is at least $(1-c)/2$. $\square$

At $c=1/2$, the unavoidable worst-case regret is at least $1/4$ for each player somewhere in the pair. The result is about a recommendation computed from insufficient information. It does not exclude acquiring more evidence or conditioning later play on new observations.

This gives a precise contribution to the mental/reference distinction: apparent equilibrium within a representation can fail because the representation cannot determine which reference game is operative. The finite-game existence theorem remains correct; its input game is what has not been identified.

## Incentives require advantages, not every payoff level

For a declared finite game whose payoffs depend on reference state $x$, set

$$
g_{i,b_i,s}(x)=U_i(x,b_i,s_{-i})-U_i(x,s).
$$

These unilateral gain observables, together with the relevant observation branches, are the quantities to insert in the continuation contract if the goal is to preserve Nash incentives. Additive offsets depending only on opponents' actions do not affect them. Full payoff recovery is sufficient but can be unnecessary.

**Proposition 7 — Direct incentive-error transport.** Suppose a valid approximate normal-form game estimates each pure unilateral gain with error at most $\eta_i$ under the reference law. For any independent mixed profile $p$,

$$
\operatorname{Reg}^{\mathrm{ref}}_i(p)
 \le\operatorname{Reg}^{\mathrm{approx}}_i(p)+\eta_i.
$$

*Proof.* For each pure deviation $b_i$, its mixed expected gain is a probability-weighted average of the pure gain entries. Its approximation error is at most $\eta_i$. Taking the maximum over deviations preserves that bound; mixed deviations cannot improve on the best pure deviation in a finite normal-form game. $\square$

The earlier $\delta_i+2\varepsilon_i$ payoff-entry bound in [R1] is recovered when each gain is obtained by subtracting two payoffs estimated within $\varepsilon_i$. This is not a universal factor-of-two improvement; it identifies the more focused observable family. Independently regressed gain values need not form a consistent payoff table, so existence of an approximate Nash equilibrium still requires a genuinely specified game.

Nature's uncertainty and players' strategic randomisation are also distinct. The factorisation $\lambda(x)\prod_i p_i(s_i)$ requires an ex ante independence declaration. State-dependent play and different player observations should be represented through contingent strategies or the action–observation model, not by silently imposing this product.

# Mixed strategies, hard feasibility, and coordination cost

A Nash certificate concerns unilateral incentives. A hard joint restriction needs an additional, non-negotiable support check.

**Proposition 8 — Support criterion for independent feasibility.** For finite nonempty action sets, joint feasible set $F\subseteq\prod_i S_i$, and independent mixed actions $p_i$,

$$
\Pr_p(s\in F)=1
\quad\Longleftrightarrow\quad
\prod_i\operatorname{supp}(p_i)\subseteq F.
$$

*Proof.* Every tuple in the product of supports has positive probability. Thus a forbidden supported tuple has positive violation probability; conversely no violation can occur outside the support. $\square$

## Finite penalties are not a universal replacement for hard constraints

Consider $n\ge2$ binary players with

$$
U_i(s)=c s_i-M\prod_j s_j,\qquad M>c>0,
$$

and mark the all-one tuple as forbidden. The pure equilibria are exactly the $n$ profiles with $n-1$ active players. They are feasible. There is also a symmetric mixed equilibrium

$$
p_i=(c/M)^{1/(n-1)}.
$$

Indeed the difference between activation and inactivity is $c-M\prod_{j\ne i}p_j=0$. Its violation probability is

$$
\boxed{\Pr(\text{forbidden})=(c/M)^{n/(n-1)}>0.}
$$

For pure equilibria, fewer than $n-1$ active players lets an inactive player gain $c$ by activating; all active makes deactivation profitable; exactly $n-1$ active makes every unilateral switch unattractive. This proves the characterisation.

The counterfamily refutes a universal guarantee that finite penalties make every equilibrium almost surely admissible. It does not assert that every penalised game is unsafe. If a joint feasibility constraint changes each player's allowed deviations, the appropriate equilibrium problem is constrained or generalised, and the ordinary product-simplex argument cannot simply be reused.

## A quantitative diversity–coordination obstruction

Let feasible joint outputs be the even-sign-parity set

$$
F_+=\{z\in\{-1,+1\}^n:\prod_i z_i=+1\}.
$$

If players mix independently and $p_i=\Pr(z_i=-1)$, then

$$
\Pr(z\notin F_+)=\frac{1-\prod_i(1-2p_i)}2.
$$

For prescribed marginal exploration $p_i\in[\eta,1-\eta]$, $0<\eta\le1/2$,

$$
\boxed{
\Pr(z\notin F_+)\ge\frac{1-(1-2\eta)^n}2.
}
$$

This follows from $|1-2p_i|\le1-2\eta$ and is sharp when all $p_i=\eta$. With unbiased independent marginals the violation probability is $1/2$, although a correlated uniform distribution on $F_+$ has the same unary marginals and zero violations.

Every nonempty Cartesian rectangle contained in $F_+$ is a singleton: if one coordinate could vary while the others were fixed, the product sign would flip. Consequently a conditionally independent mixture generating the *uniform* law on $F_+$ through a finite shared variable $Z$ requires

$$
\boxed{|\operatorname{supp}Z|\ge2^{n-1},\qquad H(Z)\ge n-1\text{ bits}.}
$$

To prove this, nonnegative mixture terms cannot put mass outside $F_+$. Each term's rectangular support is therefore a singleton. At least one positive term is needed for every feasible tuple. The generated tuple is a deterministic function of $Z$, so its entropy $n-1$ is bounded by $H(Z)$. Taking $Z$ itself uniform on the feasible tuples attains both bounds.

This is a specialised support-rectangle/nonnegative-factorisation result, directly related to the repository's existing BF analysis [R5]. It is not a new general rank theorem. The bound is about one specified shared-latent implementation of a joint law, not the number of minds, persons, sources, or independent evidential roots. An impersonal mediator achieves it. A protocol with interactive communication has a different resource model and is not ruled out.

The contribution to Orthemology is the explicit architectural choice: independent local diversity, a non-rectangular hard joint condition, and guaranteed feasibility cannot all be retained without a suitable coordinating or restricting mechanism. Nash existence by itself supplies none of that mechanism.

# Minimal repair and the integrated preservation claim

## How much information must be restored?

A discharge need not be reversed in its entirety. The continuation space identifies the missing directions, not a demand to recover every historical variable.

**Proposition 9 — Exact augmentation cost.** Retain the moment summary for $\mathscr V$ and require all expectations in $\mathscr C_h$. Over the full simplex, the minimum number of additional continuous real-valued statistics of the law that suffice for exact recovery is

$$
\boxed{
 a_{\min}=\dim(\mathscr V+\mathscr C_h)-\dim\mathscr V.
}
$$

*Proof.* Extend a basis of $\mathscr V$ to a basis of $\mathscr V+\mathscr C_h$ using $a_{\min}$ elements of $\mathscr C_h$. Their expectations give an attainable augmentation.

For necessity, regard laws as points in an affine hyperplane and restrict the required expectation map to the tangent kernel of the retained moment map. Elementary rank subtraction gives rank $a_{\min}$ on that kernel. Choose $a_{\min}$ tangent vectors with independent images. Starting at a strictly positive law, a sufficiently small open box of combinations of those vectors consists of valid laws, has constant retained summary, and has pairwise distinct required continuation values. Any sufficient continuous additional statistic must be injective on that box. The same invariance-of-domain argument used in Theorem 2 forces at least $a_{\min}$ extra coordinates. $\square$

This is an information-storage lower bound under ideal access to the law, not the number of observations needed to estimate those statistics. Query cost, noise, source custody, and feasibility of acquiring the extra information remain distinct. One measurement could supply several coordinates; conversely estimating one coordinate can require many observations.

## What the integrated result permits one to certify

Taken together, Theorems 1–3 and Propositions 4 and 9 provide a single continuation-completeness family:

$$
\begin{gathered}
\text{specified dynamics and future contract}
\ \longrightarrow\ \mathscr C_h,\\
\mathscr C_h\subseteq\mathscr V
\ \Longleftrightarrow\ \text{universal exact continuation recovery},\\
\mathscr C_h\not\subseteq\mathscr V
\ \longrightarrow\ \text{separating reference laws and an exact defect},\\
\dim(\mathscr V+\mathscr C_h)-\dim\mathscr V
\ =\ \text{minimum exact continuous augmentation cost}.
\end{gathered}
$$

If the contract includes reference safety indicators and game gain observables, the same construction applies to those quantities. This does not equate them. A gain certificate licenses a regret statement; a failure-probability certificate licenses a risk statement; an authenticated witness predicate licenses only what its separately justified semantics permit.

The added benefit to Orthemology is an operative discriminator between three reductions that may have identical-looking completion records:

**Future-complete reduction:** the accessible retained representation contains the required continuation span.

**Quantified reduction:** it has a nonzero certified defect within the permitted tolerance, with probability-conditioning and operating margins accounted for.

**Scope-changing reduction:** it cannot preserve some live inquiry and therefore requires reacquisition, new evidence, or an explicit change in the certified continuation scope. Calling this third case merely “completed” would conceal a change in future capability.

These are not new core verdict IDs. They are candidate mathematical tests for a selected representation and discharge contract.

## Conditional estimates must retain conditioning margins

The instrument construction handles posterior updates by normalising an unnormalised law. Exact arithmetic poses no issue on a positive-probability branch. Approximation does: rare observations can magnify a small numerator or likelihood error.

For $0\le N\le p$, $p\ge\beta>0$, and estimates satisfying $|\widehat N-N|\le\epsilon_N$ and $|\widehat p-p|\le\epsilon_p<\beta$, put $q=N/p$. Then

$$
\left|q-\operatorname{clip}_{[0,1]}\frac{\widehat N}{\widehat p}\right|
 \le\frac{\epsilon_N+\epsilon_p}{\beta-\epsilon_p}.
$$

Indeed $\widehat p\ge\beta-\epsilon_p$ and
$|\widehat N-q\widehat p|\le\epsilon_N+q\epsilon_p\le\epsilon_N+\epsilon_p$; clipping cannot increase distance to $q\in[0,1]$. A certificate of small unnormalised error is therefore not automatically a certificate of small conditional error. This is another specific preservation obligation, not a general claim of convergence.

# Adversarial comparison and contribution status

## What is genuinely added to the working packet

The earlier v1 quotient theorem answered a deterministic factorisation question for one update, target, and landscape. This supplement supplies an explicit finite stochastic/action–observation counterpart, a universal approximation defect with a constructive dual, a minimal continuous memory theorem, and an exact horizon-growth family. It also shows that the hidden continuation can change the unique equilibrium of a declared strategic layer and that hard joint admissibility needs a separate certificate.

Those additions are mathematically substantive relative to that predecessor: there are now quantities to calculate, lower bounds to test, and explicit conditions for refusing or repairing a purportedly future-safe discharge. They do not establish superiority over all existing state-abstraction or control methods.

The sharp new-to-this-packet calculation is the *joint use* of the horizon law, minimax defect, and augmentation formula to delimit a declared Orthemological continuation promise. Its general-novelty status remains unestablished. The underlying binary transformations, Walsh basis, observability closure, duality, and topological dimension obstruction are established mathematics or direct consequences of it.

## Strong rivals and explicit exits

A full joint-law representation survives the lower bound and achieves exactness. A predictive-state representation built from the continuation span also survives; it is an ancestry and comparator, not an adversary defeated by changing its name. A faithful archive with permitted retrieval can avoid permanent information loss, though it incurs access and processing obligations. Restricting the law class, horizon, allowed operations, or target family can make a much smaller representation sufficient.

Nonlinear predictive-state representations can achieve exponential compression in some deterministic settings [P8]. That surviving result prevents any general claim that nonlinearity never helps. Its deterministic binary predictions are not a promise to encode all arbitrary joint laws on the full simplex in our theorem.

A nonlinear exact encoder of the full law does not evade the continuous dimension bound. An arbitrary discontinuous infinite-precision code lies outside that bound; it cannot be silently dismissed, but neither is it a demonstrated robust implementation. The approximation lower bound is restricted to linear moment acquisition and does not exclude every approximate neural representation.

The hard-safety parity result excludes independent exploration at the stated level, not a correlated mediator or communication protocol. The mediator may be impersonal. No result here selects a personal, theological, or metaphysical ontology, repairs the source–world bridge by mathematical fiat, or establishes human restoration. Mental representations and reference-world claims remain different levels of assertion.

A historical record can retain a witness while its current summary loses future evaluative ability. Conversely, a summary can predict all declared outcomes while discarding provenance that the governing contract independently requires. Neither dimension substitutes for the other.

## Meniscus-facing assessment

The owner-supplied charter [R3] requires more than mathematical correctness or many theorem labels: novelty plausibility after comparison, importance beyond one application, integration across several milestones, rival survival, custody, freezing, cold audit, and a distinct rereview. It also requires an actual change in the research frontier for a break claim.

This supplement directly advances the following mathematical fronts, without completing the milestones themselves:

| Milestone | Concrete contribution in this supplement |
|:--|:--|
| M3: dynamic identification | Sharp indistinguishability witnesses and a horizon-sensitive sufficient statistic. |
| M7: restorative/transition calculus | A checkable condition for preserving future operational capability through discharge. |
| M12: cross-layer transport | Separate contracts and error bounds for answers, risk, incentives, and witness predicates. |
| M13: method transfer | Exact conversion of a nonlinear-reduction concern into a finite invariant-span problem and lower bound. |
| M14: executable library | Rational certificates and reproducible finite tests, but no Lean/kernel proof. |

The principal mathematical no-go is now precise: **a small continuous summary of arbitrary joint uncertainty cannot retain the whole specified future inquiry menu under the local pairwise dynamics of Theorem 3.** The exact menu-dependent memory and augmentation costs sharpen the earlier qualitative statement that future information may be lost.

However, the invariant-span backbone is already present in predictive-state and control mathematics, and reward-predictive representations already augment that backbone for a changed consequence surface [P9]. A meniscus claim cannot be based on failing to recognise that ancestry. The current status is therefore **a proved, scoped research extension with executable checks, directed towards meniscus—not a charter-qualified MENISCUS_CANDIDATE or MENISCUS_REACHED declaration**. Independent cold audit and distinct rereview were not performed in this session.

## The next substantive frontier, now narrower

The mathematically consequential next problem is no longer “can we encode an episode as a tensor?” It is the joint optimisation of *information retained, information reacquired, admissible future scope, and error tolerated* under a justified model class.

The present full-simplex rank law is exact. It provides the baseline against which a proposed compressed, learned, distributed, or dynamically expanding architecture must earn an advantage. To advance beyond that baseline, one should establish a structurally justified restricted family of laws and operators, then prove a sharper attainable memory–query–risk frontier for it. A realistic source/authority contract can be included as test observables, but the justification of their semantics cannot be supplied by a rank calculation.

An especially focused extension is an adaptive discharge problem: choose which witness information to keep now and which queries to reserve later, under a fixed budget, while preserving the selected safe continuation family. The sharp defect identifies the exact ambiguous pair a query must separate; the augmentation theorem quantifies missing dimensions; the strategic corollaries distinguish incentives to acquire evidence from guaranteed feasibility. This is a concrete research problem generated by the results, not a declaration that it has already been solved.

# Appendix A — Proof assumptions and claim ledger

**Theorem 1.** Requires finite nonempty $X$, all probability laws on $X$, a linear observable space containing constants, and uniform absolute error. It permits arbitrary decoders. It proves information recovery, not truth of reference-model assumptions.

**Theorem 2.** Requires finite instruments with specified observation probabilities and a declared contract. The stated horizon is finite, or the hierarchy must be stabilised. Branch probabilities and terminal numerators are included; conditional answers require positive branch mass. The minimal-coordinate statement additionally requires a continuous encoder and full-simplex coverage.

**Theorem 3.** Requires exactly the stated pairwise sign updates and a horizon measured in elementary updates. It is not a bound for all conceivable update families. A fully observed sample is not the unknown law being compressed.

**Proposition 4.** Bounds linear moment summaries, even with nonlinear decoders. It is not an exact intermediate-tolerance optimum or an approximate nonlinear-encoder lower bound.

**Propositions 6–8.** Apply to explicitly declared finite games, independent mixed strategies where stated, and externally specified reference payoffs/feasibility. Game existence is not assumed to identify those payoffs, ensure selection, or force safe play.

**Proposition 9.** Counts added continuous statistics of a law with an already-retained moment summary. It is not a sample-complexity or causal-identification theorem.

**No hidden promotion.** Tensor degree, number of real coordinates, common-signal alphabet size, entropy, player count, and physical modal resolution are separately typed. No one of these measures determines the others without an explicit construction.

# Appendix B — Verification and review record

The included `verify_frontier.py` has nine groups. The final recorded run passed all groups. These checks test finite instances and symbolic identities; the general proofs are the arguments in the manuscript, not consequences of enumeration.

| Check family | Final coverage |
|:--|:--|
| Sharp defect | 105 rational primal/dual certificates; 79 positive defects. |
| Pairwise horizon spectrum | 44 horizon cases for $n=2,\ldots,9$; 81,032 pointwise pullback checks; six complete Walsh orthogonality checks. |
| Future parity separation | 1,012 proper-moment comparisons and 1,020 exact forward trajectories. |
| Observations and feedback | A four-state instrument example with dimensions $2\to4$; 120 unnormalised updates and 120 positive-mass posterior comparisons. |
| Direct incentive transport | 1,000 exact two-player profile/player comparisons. |
| Independent joint safety | 3,276 rectangles, 126 safe rectangles; 3,276 exploration profiles; six finite-penalty game families. |
| Approximate dimension bound | 53 rational projection tests and corresponding rational uniform-error upper certificates. |
| Hidden strategic continuation | Two uniquely solved pure reference games and 162 mixed-profile/player checks. |
| Reduction identities | Five symbolic or exact checks, including the memory formula's ODE and initial condition. |

The continuous-encoder lower bounds use invariance of domain on paper; they are not established by the enumerations. The entropy lower bound is also a paper argument. No proof-assistant or independent specialist review is claimed.

One test implementation initially failed because coefficients and an optimum returned by a floating-point LP solver were rationalised separately. The rounded coefficient vector did not necessarily satisfy the separately rounded optimum. The approximate-dimension test was repaired to recompute the exact sup error of the rational coefficient proposal. That check now certifies an *upper bound*, not exact LP optimality. The separate sharp-defect group continues to check exact primal–dual equality. This was a certificate-reconstruction defect in the checker, not a change to the theorem.

A self-review checked the sample/law distinction, constant-coordinate count, finite-horizon update direction, mixed-strategy independence, word-order typing, reference-model assumptions, conditional-probability denominators, and novelty classification. It is labelled self-review, not cold audit or distinct fresh rereview.

# Appendix C — Source register and comparison

The source IDs below distinguish supplied material, repository authority, and external ancestry. The local input hashes are recorded in `provenance.json`; the repository was read only through the connector and was not modified.

## Supplied and repository sources

**[R1]** *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, version 1, 8 September 2026. The supplied Markdown, LaTeX, PDF, and verification archive. The main predecessor used here is Section 11, particularly Theorem 11.2 and its explicit stochastic-extension boundary; Sections 3–8 supply representation, discharge, landscape, and game definitions. All three delivered formats were present; the Markdown was the principal mathematical reading copy.

**[R2]** `theislampill/orthemology`, pinned at `f50dc1aee52356cc6adbef342387576b02afc124`. Canonical episode, dynamic-orthing, and multi-actor distinctions are retained. Targeted reads and the prior supplied extracts were used; no claim of rereading all repository files is made. Permanent repository locator: <https://github.com/theislampill/orthemology/tree/f50dc1aee52356cc6adbef342387576b02afc124>.

**[R3]** Owner-supplied *AR8R / Orthemology Meniscus Milestone Architecture*, repository path `docs/project-closure/ar8r-v11/programs/AR8R-ORTHEMOLOGY-MENISCUS-MILESTONE-ARCHITECTURE-V1.md`, and companion `AR8R-ORTHEMOLOGY-MENISCUS-MILESTONES-V1.yaml`, at [R2]. The charter is non-adoptive research-program authority, not scientific attainment. Its historical repository-observation dates were not mistaken for current branch identity.

**[R4]** `docs/project-closure/ar8r-v11/theorems/ar8r-t300-lower-order-alignment-blind-restoration.md`, at [R2]. Repaired, scoped parity diagnostic, explicitly no general probability novelty or empirical restoration claim. The present dynamic activation and rank calculations are deductions, not silently attributed to T300.

**[R5]** *PMR-007 Deep Round BF V2 — real nonnegative latent-product complexity and rival-width boundary*, at [R2], under `docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_THEOREM_FILES/`. A proposal-only record of nonnegative rank, normalised product mixtures, support rectangles, and surviving impersonal rivals. The multivariate parity coordination result is classified as a specialisation of this established mechanism, not a newly discovered ontology or general factorisation theorem.

**[F1]** Charles L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, supplied six-page `navierstokes.pdf`, including errata. The equations, admissible-forcing scope, and distinction between smooth and weak solutions are its role here. It is not a proof of any breakdown alternative. Official source: <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>.

**[F2]** Adarsh Ganeshram, Valentin Duruisseaux, and Anima Anandkumar, *Stable Singularity of the Euler Equations on R3*, supplied 107-page `Euler.pdf`. The residual-certification and low/high-control architecture is methodological input. The file's own outstanding-certification statements remain in force. Page 33's pipeline was inspected visually. No current final theorem or full Lean replay is claimed from the supplied draft.

**[F3]** The supplied Tao discussion and screenshot concerning the value of mathematical discovery before and after publication. These motivate inquiry-landscape externalities. They are not used as mathematical axioms or as an independently verified historical claim that open problems are literally non-renewable.

## External mathematical ancestry

**[P1]** Yanjun Han, Jiantao Jiao, and Tsachy Weissman, “Local moment matching: A unified methodology for symmetric functional estimation and distribution estimation under Wasserstein distance.” *Proceedings of Machine Learning Research* 75 (COLT 2018), 3189–3221. Section 2.2 and Lemma 25 explicitly develop moment-matching/uniform-approximation duality. The finite linear-space version here is separately proved. <https://proceedings.mlr.press/v75/han18b.html>.

**[P2]** Michael L. Littman, Richard S. Sutton, and Satinder Singh, “Predictive Representations of State.” *Advances in Neural Information Processing Systems* 14, conference 2001. The PDF identifies all three authors; the proceedings HTML metadata omits Singh. Action-conditional tests, sufficient prediction vectors, rank-based construction, and normalised updates are direct ancestry of Section 5. <https://proceedings.neurips.cc/paper_files/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf>.

**[P3]** Britton Wolfe and Satinder Singh, “Predictive state representations with options.” *Proceedings of ICML 2006*. DOI: `10.1145/1143844.1143973`. The accessible bibliographic/abstract evidence identifies the extension from open-loop tests to closed-loop options. Full publisher text was not retrieved in this run. This is a warning against claiming that adding feedback itself is novel, not a source for an uninspected theorem.

**[P4]** Ayoub Gouasmi, Eric J. Parish, and Karthik Duraisamy, “A priori estimation of memory effects in reduced-order models of nonlinear systems using the Mori–Zwanzig formalism.” *Proceedings of the Royal Society A* 473 (2017), 20170385. DOI: `10.1098/rspa.2017.0385`. Accessible abstract/bibliographic evidence supports the memory-effect ancestry; the exact elementary convolution used here is derived directly. The full-text endpoint was inaccessible during this run. <https://pubmed.ncbi.nlm.nih.gov/28989314/>.

**[P5]** Allen Hatcher, *Algebraic Topology*. Cambridge University Press, 2002, Theorem 2B.3, invariance of domain. Author-hosted chapter inspected; theorem and its proof provide the imported topological fact used in the dimension lower bounds. <https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf>.

**[P6]** Steven L. Brunton, Bingni W. Brunton, Joshua L. Proctor, and J. Nathan Kutz, “Koopman Invariant Subspaces and Finite Linear Representations of Nonlinear Dynamical Systems for Control.” *PLOS ONE* 11(2), e0150171, 2016. DOI: `10.1371/journal.pone.0150171`. Invariant spaces of observables and lifted control representations are direct ancestry; no general claim that nonlinear dynamics have small exact invariant subspaces is imported. <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0150171>.

**[P7]** Hiroki Ishibashi, Kenshi Abe, and Atsushi Iwasaki, “Approximate State Abstraction for Markov Games.” *Proceedings of AAAI* 39(17), 17555–17563, 2025. DOI: `10.1609/aaai.v39i17.33930`. Primary article metadata/abstract establish relevant prior work on abstraction and approximate equilibrium guarantees in two-player zero-sum games. The simple finite unilateral-gain bound in Section 8 is independently proved, not presented as new game-abstraction theory. <https://ojs.aaai.org/index.php/AAAI/article/view/33930>.

**[P8]** Matthew R. Rudary and Satinder Singh, “A Nonlinear Predictive State Representation.” *Advances in Neural Information Processing Systems* 16, conference 2003, proceedings 2004, 855–862. Theorem 2 and Section 4 treat deterministic binary predictions and examples of exponential compression. This is a surviving comparator; our full-simplex lower bound must not be extrapolated to those different assumptions. <https://papers.neurips.cc/paper_files/paper/2003/file/72e6d3238361fe70f22fb0ac624a7072-Paper.pdf>.

**[P9]** Andrea Baisero and Christopher Amato, “Reconciling Rewards with Predictive State Representations.” *Proceedings of IJCAI 2021*, 2170–2176. DOI: `10.24963/ijcai.2021/299`. Theorem 1 gives a column-space criterion for accurate reward representation; Section 4 constructs reward-predictive representations. The source was read specifically as close prior art, not omitted to inflate novelty of contract-observable augmentation. <https://www.ijcai.org/proceedings/2021/0299.pdf>.

## Prior-art disposition

There is no general-novelty claim for moment duality, invariant/predictive spans, Walsh independence, dimension obstruction, payoff perturbation, support rectangles, or conditional expectation error amplification. The exact horizon-specific synthesis, its approximate-memory corollary, and its use as an operational discharge criterion are the candidate contribution examined here. No located source was claimed to contain—or not contain—the entire same combined result without a full comparison. An exhaustive novelty review remains open.

This register therefore supports a scoped formal advance over the delivered v1 packet. It does not certify a field-wide breakthrough, historical priority, empirical validity, or repository adoption.
