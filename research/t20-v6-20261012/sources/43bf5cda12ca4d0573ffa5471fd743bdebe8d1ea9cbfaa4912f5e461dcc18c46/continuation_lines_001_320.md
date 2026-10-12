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
