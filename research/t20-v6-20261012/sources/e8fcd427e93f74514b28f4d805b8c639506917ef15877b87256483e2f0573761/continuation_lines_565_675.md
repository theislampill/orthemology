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
