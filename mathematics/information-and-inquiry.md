# Information retained by inquiry

## Prediction, decisions, Fisher dynamics, and certified action

### Abstract

A representation can preserve every conditional answer to an inquiry while losing the probabilities, values, or geometric dynamics associated with those answers. We develop these distinctions in related finite models. Invariant observable spaces give exact predictive states, including their admissible cones and a sharp continuous-coordinate bound. A synchronized tensor construction, together with a separate feasibility test, characterizes the weaker equivalence of all posterior answers. For a fixed audit, missing information forms an affine fibre of audit weights. This gives an exact expected-value criterion and a three-outcome example that reverses the preferred inquiry decision. For the categorical Fisher metric of the full joint law, we derive a different criterion, prove descent of maximal source trajectories, and establish a sharp threshold: with more audit outcomes than target states, every globally descending smooth objective is target-marginal-only on the signature image. Gram-determinant objectives show why the strict inequality is necessary. Finally, we determine the supplementary information required by finite, expected-value, and full-metric contracts, distinguish selecting a valid certificate from identifying a state, and give complete finite proofs for model-bound temporal guarantees and versioned evidence transport. Graph-constrained parity operations make the action dependence explicit: the exact connecting-tree cost determines which moments a finite horizon can reveal. For proof-producing inquiry, residual evidence supports and terminal checking prices give a canonical continuation summary and an exact finite completion criterion. Finite grounded rules compile that summary even in the presence of cycles, while shared proof graphs expose a limit of intermediate cost-only pruning. When the governing quadratic standard is unknown, shrinking disturbances impose a decoding requirement on every good repair. This yields finite-sample lower and upper bounds, and a countability obstruction to eventual exact correction when informative acts are target-bad. Common-reference and actual causal-oracle proofs identify the information premise precisely; sublinear tolerance and atomic blind guessing delimit the result. For a fixed positive disturbance, a complementary cost theory separates pointwise eventual repair from uniform and prior-averaged budgets. It gives exact Beta endpoint thresholds, finite-horizon rates and deterministic reporting-clock criteria, and extends those rates to controlled endpoint densities with separately handled atoms.

This is a consolidated exposition of the source mathematics cited below. Its proofs are ordinary mathematical arguments; computational corroboration, kernel certification, empirical interpretation, literature priority, and owner adoption are distinct. The edition and review boundary appears at the end.

## 1. What must a representation preserve?

“Preserving information” is incomplete until the required operations and outputs have been specified.

| Contract | Required output |
|---|---|
| Posterior answers | Feasible observation words and the target posterior after each feasible word |
| Full prediction | Those answers and the probabilities of the observation words |
| Decision value | Expected losses, rewards, or costs in the declared decision problem |
| Geometric dynamics | Evolution under the specified source metric, objective, clock, and domain |
| Certified action | An output admitted by the supplied source, version, evidence, and temporal contract |

Full prediction preserves the values of bounded-depth adaptive policy trees when their terminal observables and costs are included. Posterior answers alone need not. Even an objective determined by retained answers can have a source gradient that depends on discarded information. Conversely, an individual objective may descend although an entire metric does not.

These distinctions concern supplied mathematical models. They do not authenticate an actual source, establish its calibration, or equate a numerical loss with epistemic warrant. The graph example in §2.4 concerns operational prediction; §§9.5–9.6 concern the missing premises and checking costs of admitted proofs. Neither converts a coordinate count into an acquisition price or supplies a source entitlement.

## 2. Finite instruments and exact predictive states

### 2.1 The model

Let the latent space have $`n`$ elements, and fix a finite, explicitly supplied action–observation alphabet $`\Sigma`$. A live unnormalized state is a column vector $`x\geq0`$ with $`ux>0`$, where $`u=(1,\ldots,1)`$. Each symbol $`a\in\Sigma`$ has a nonnegative column-substochastic matrix $`M_a`$. The outcome matrices belonging to one action sum to a column-stochastic matrix. Let $`C`$ be a fixed column-stochastic target readout. The constructions below test every finite word in $`\Sigma^*`$, including the empty word.

For a chronological word $`w=a_1\cdots a_t`$, set

```math
M_w=M_{a_t}\cdots M_{a_1},\qquad M_\varepsilon=I.
```

Its conditional probability and posterior target law are

```math
\Pr_x(w)=\frac{uM_wx}{ux},\qquad
q_w(x)=\frac{CM_wx}{uM_wx}\quad\text{if }uM_wx>0.               \quad\text{(1)}\quad
```

At zero denominator the observation is impossible: no posterior is invented. Nonnegativity implies $`uM_wx=0\Rightarrow M_wx=0`$.

The target, model, and permitted alphabet are fixed. History-dependent permissions require an explicit controller or a separately proved restricted-language construction. If the target concerns an initial label that transitions can change, retain that label in the state.

### 2.2 The invariant observable construction

Define

```math
W_0=\mathrm{span}(\{u\}\cup\mathrm{rows}\,C),\qquad
W_{h+1}=W_h+\sum_aW_hM_a.                                    \quad\text{(2)}\quad
```

**Theorem 1 — Exact predictive reduction.** The sequence stabilizes at the least invariant row space $`W`$ containing $`W_0`$. For a full-row-rank basis matrix $`B`$ of $`W`$, there are unique matrices and coefficients satisfying

```math
BM_a=T_aB,\qquad u=\nu B,\qquad C=LB.                         \quad\text{(3)}\quad
```

For normalized $`x,y`$, equality $`Bx=By`$ is equivalent to equality of every future word probability and every feasible-word target posterior. The reduced state $`z=Bx`$ has admissible cone

```math
K=B\mathbb R_+^n=\mathrm{cone}\{Be_i\}
```

and, on the normalized slice $`\nu z=1`$, exact update

```math
z\longmapsto\frac{T_az}{\nu T_az}\quad\text{if }\nu T_az>0.    \quad\text{(4)}\quad
```

**Proof.** Induction shows that $`W_h`$ is the span of $`uM_w`$ and $`cM_w`$ for words of length at most $`h`$ and rows $`c`$ of $`C`$. Every strict inclusion increases dimension, giving at most $`n-\dim W_0`$ strict increases. Equality at one stage gives invariance, so later growth is impossible. Every invariant space containing $`W_0`$ contains the entire sequence. Invariance and full row rank give (3).

The commuting equations recover probabilities and numerators from $`Bx`$, and therefore the positive-branch posteriors. Conversely, equal probabilities and posteriors give equal target numerators on feasible words; both numerators vanish on impossible words. Thus $`x-y`$ annihilates every generator of $`W`$.

If $`z=Bx`$ with $`x\geq0`$, then $`T_az=BM_ax\in K`$. Also $`\nu z=ux\geq0`$, with zero mass forcing $`x=0`$ and $`z=0`$. Hence impossible successors are zero and cannot be normalized. The same fact proves pointedness: $`z,-z\in K`$ forces $`\nu z=0`$, hence $`z=0`$. Equation (4) follows. $`\square`$

The matrices $`T_a`$ can have signed entries in a chosen basis. Positivity means preserving $`K`$, not a freely substituted coordinate orthant. For live unnormalized laws the predictive equivalence concerns $`Bx/(ux)`$; absolute evidence mass is an additional requirement.

Adding finite terminal utilities, costs, or safety observables to $`W_0`$ preserves their corresponding values for bounded-depth adaptive policy trees. Each policy-tree leaf contributes a numerator $`fM_wx`$; summing leaves gives the expectation, and randomized policies add finite convex combinations. Target observations alone do not thereby preserve every reward. [1], [2]

### 2.3 Continuous memory

Put $`m=\dim W`$. On the full normalized simplex, exactly $`m-1`$ continuous real coordinates are necessary and sufficient for this predictive contract, even with arbitrary decoders.

A basis $`u,f_1,\ldots,f_{m-1}`$ gives sufficiency. For necessity select $`m`$ latent states with linearly independent basis-evaluation columns. Their nonconstant evaluation vectors are affinely independent, so all required expectations distinguish every law on the $`(m-1)`$-simplex supported on these states. Any exact encoder is injective there. On its relative interior, a continuous injection into $`\mathbb R^d`$ for $`d<m-1`$, followed by zero-padding, contradicts invariance of domain: the image would be open in $`\mathbb R^{m-1}`$ while lying in a lower-dimensional plane. The zero-dimensional case is immediate. [1], [10]

This counts exact continuous coordinates, not bits, physical degrees of freedom, or finitely many reachable histories. It does not constrain discontinuous encodings of unlimited exact precision.

### 2.4 How a constrained action graph changes the necessary information

The permitted transformations can make a higher-order interaction accessible before a lower-order one. This is a precise obstruction to choosing retained moments solely by their order. It also gives a concrete finite-horizon version of the observable-space construction.

Let $`G=(V,E_G)`$ be a finite simple undirected graph of named slots, with state space $`X=\{-1,+1\}^V`$. For each adjacent pair, both ordered elementary updates are available:

```math
(F_{ij}x)_i=x_ix_j,\qquad (F_{ij}x)_k=x_k\quad(k\ne i).
```

The contract is to predict each **individual terminal coordinate** after any fixed, silent sequence of at most $`h`$ such updates. The word is chosen independently of the hidden state; intermediate states are not observed. An individual sign's expectation determines its law, since its probability of $`-1`$ is $`(1-\mathbb E[x_i])/2`$. The contract does not request the joint law of several terminal coordinates. It counts sequential elementary gates, not parallel layers, physical storage bits, or acquisition cost. [21–22]

For a subset $`S\subseteq V`$, define its Walsh character by $`\chi_S(x)=\prod_{v\in S}x_v`$, with $`\chi_\varnothing=1`$. Direct multiplication, using $`x_j^2=1`$, gives

```math
\chi_S\circ F_{ij}=
\begin{cases}
\chi_{S\mathbin{\triangle}\{j\}},&i\in S,\\
\chi_S,&i\notin S.
\end{cases}
```

Thus an active slot can toggle an adjacent slot in the character's support. Writing $`x_i=(-1)^{b_i}`$ identifies the update with the Boolean operation $`b_i\leftarrow b_i\mathbin{\mathrm{XOR}}b_j`$, a CNOT with control $`j`$ and target $`i`$. This algebraic correspondence carries no quantum or cognitive interpretation. Pulling back a terminal character reverses the chronological order of the state updates. All reversed words are still permitted and have the same length.

For nonempty $`S`$, let $`\tau_G(S)`$ be the minimum cardinality of a connected induced vertex set containing $`S`$. Set it to $`+\infty`$ if no such set exists. Let $`d_G(S)`$ be the minimum number of updates whose pullback turns some unary character into $`\chi_S`$; the terminal coordinate may be chosen freely.

**Theorem 1A — Exact graph-constrained parity cost.** For every nonempty $`S`$,

```math
d_G(S)=2\tau_G(S)-|S|-1.
```

If the terminal coordinate is fixed at $`r`$, the corresponding minimum is

```math
d_{G,r}(S)=2\tau_G(S\cup\{r\})-|S|-1.
```

An infinite connected-superset cost means that the character is unreachable. The empty support is never reached from a singleton.

**Proof.** Consider any support path $`A_0=\{r\},A_1,\ldots,A_\ell=S`$ and its visited set $`U=\bigcup_t A_t`$. Every first appearance of a vertex other than $`r`$ attaches it to a currently active adjacent vertex. Consequently $`G[U]`$ is connected. If $`r\in S`$, each vertex of $`S\setminus\{r\}`$ must be toggled at least once, and each vertex of $`U\setminus S`$ at least twice. Therefore

```math
\ell\geq(|S|-1)+2(|U|-|S|)=2|U|-|S|-1.
```

If $`r\notin S`$, each vertex of $`S`$ must enter, $`r`$ must leave, and every other transient vertex must both enter and leave. This gives the same inequality:

```math
\ell\geq |S|+1+2(|U|-|S|-1)=2|U|-|S|-1.
```

Revisits and steps that leave the character unchanged cannot improve this bound. Since $`U`$ contains both $`S`$ and $`r`$, it proves the stated lower bounds.

For attainment with a freely chosen coordinate, take a smallest connected superset $`U`$, a spanning tree of $`G[U]`$, and root it at some $`r\in S`$. Activate the vertices in parent-before-child order, using $`|U|-1`$ toggles. Then remove exactly $`U\setminus S`$ in decreasing depth, using its tree parent as the active neighbour. That parent remains active: it either belongs to $`S`$ or has not yet been removed. These removals cost $`|U|-|S|`$, giving the claimed total. With prescribed $`r\notin S`$, activate a minimum tree containing $`S\cup\{r\}`$ from $`r`$, then reroot the fully active tree at any member of $`S`$ before performing the same removals. Finally, every elementary gate is an invertible linear transvection on the binary support vector, so it cannot send a nonzero support to zero. $`\square`$

The Steiner-tree cost and fill/eliminate construction are already present in the CNOT synthesis literature. Vandaele, Martiel, and Goubault de Brugière give the same formula for a chosen connecting tree; their practical algorithm approximates that tree. Here $`\tau_G`$ denotes the actual optimum, and the visited-set argument proves a lower bound against every permitted word. Neither the formula nor its synthesis ancestry is claimed as a new discovery. [23]

#### Finite horizons, continuous coordinates, and saturation

Put

```math
\mathcal R_h=\{S\ne\varnothing:d_G(S)\leq h\},\qquad
\mathcal W_h=\mathrm{span}\{\chi_S:S\in\mathcal R_h\},\qquad
\mathcal V_h=\mathrm{span}(\{1\}\cup\mathcal W_h).
```

The last space includes the mass coordinate, as the predictive space in §2.2 does. Walsh orthogonality gives

```math
\dim\mathcal W_h=|\mathcal R_h|,\qquad
\dim\mathcal V_h=1+|\mathcal R_h|.
```

**Corollary 1B — Sharp finite-horizon information.** On the full probability simplex on $`X`$, the smallest dimension of a continuous exact encoder for this terminal-unary contract is $`|\mathcal R_h|`$. The decoder need not be continuous.

**Proof.** Retaining the indicated moments proves sufficiency. For necessity, let $`q=|\mathcal R_h|`$ and, for $`\sum_S|a_S|<1`$, define

```math
p_a(x)=2^{-|V|}\left(1+\sum_{S\in\mathcal R_h}a_S\chi_S(x)\right).
```

These laws are strictly positive and normalized. Orthogonality gives $`\mathbb E_{p_a}[\chi_S]=a_S`$ for every retained support. An exact encoder is therefore injective on this continuously parametrized open subset of $`\mathbb R^q`$. If its dimension were smaller than $`q`$, the zero-padding argument from §2.3 would contradict invariance of domain. The case $`q=0`$ is immediate. $`\square`$

This subtracts one from the **augmented** dimension, not from the raw span. It is an exact continuous-coordinate result for all laws; a constrained reachable law family or a discontinuous encoding needs its own analysis. Moreover, finite-horizon sufficiency is a remaining-horizon hierarchy:

```math
F_{ij}^*\mathcal V_{h-1}\subseteq\mathcal V_h.
```

It need not give $`F_{ij}^*\mathcal V_h\subseteq\mathcal V_h`$. Only saturation supplies the invariant space required for indefinite updating. The convention “at most $`h`$” also matters. If the graph has an edge, one can pad any singleton-starting support word with no-ops by orienting that edge so its first index is not the active singleton. With an edgeless graph and no explicit identity command, positive exact-length words do not exist, although the at-most-horizon contract still includes the initial unary observations.

On the complete graph with $`n=|V|`$, every support is connected, so $`d_G(S)=|S|-1`$ and

```math
\dim\mathcal V_h=\sum_{k=0}^{\min(n,h+1)}\binom nk.
```

On a path, the connected hull of a support has $`L`$ vertices, where $`L=\max S-\min S+1`$. Its cost is $`2L-|S|-1`$. Counting supports by their two extreme vertices gives the exact profile

```math
\dim\mathcal V_h
=1+n+\sum_{L=2}^{n}(n-L+1)
\sum_{k=\max(2,2L-h-1)}^{L}\binom{L-2}{k-2},
```

where an inner sum with lower endpoint above $`L`$ is zero. There are $`n-L+1`$ intervals of length $`L`$ and $`\binom{L-2}{k-2}`$ supports of size $`k`$ whose hull is that interval; Theorem 1A gives the lower endpoint on $`k`$.

For the four-vertex path $`1-2-3-4`$, the augmented dimensions at horizons $`0,1,2,3,4,5`$ are $`5,8,10,13,15,16`$. The full support costs only three gates, whereas the endpoint pair $`\{1,4\}`$ costs five. The accessible supports are therefore not downward closed. Chronological words $`F_{34},F_{23},F_{12}`$ and $`F_{12},F_{23},F_{34},F_{23},F_{12}`$ make the terminal first coordinate respectively the full parity and the endpoint parity.

This distinction has an exact probabilistic witness. The two laws

```math
p_\pm(x)=\frac1{16}\bigl(1\pm\chi_{\{1,4\}}(x)\bigr)
```

are nonnegative and normalized. Every horizon-three moment agrees between them, including the full four-way moment, because the endpoint character is orthogonal to every accessible character. The five-gate endpoint readout instead has negative-sign probabilities $`0`$ and $`1`$. Any prediction based only on the common horizon-three data has worst-case absolute error at least $`1/2`$ on these two laws; the constant prediction $`1/2`$ attains that bound.

For a star, a support containing the centre costs $`|S|-1`$; a singleton leaf costs zero; a support of $`k\geq2`$ leaves costs $`k+1`$. This follows immediately by including the centre in the minimum connected hull. The four-vertex star consequently has augmented profile $`5,8,11,15,16`$ through horizon four.

More generally, if a tree $`T`$ has $`n\geq2`$ vertices and $`L_T`$ leaves, its saturation horizon is exactly

```math
h_{\rm sat}(T)=2n-L_T-1.
```

To prove the upper bound, let the hull of $`S`$ have $`m`$ vertices. An original leaf of $`T`$ lying in this minimal hull must belong to $`S`$, while at most $`n-m`$ original leaves lie outside it. Hence $`L_T\leq |S|+n-m`$ and

```math
d_T(S)=2m-|S|-1\leq n+m-L_T-1\leq2n-L_T-1.
```

Taking $`S`$ to be all original leaves attains equality: every edge of a finite tree lies on a path between leaves, so their hull is all of $`T`$. A one-vertex tree saturates at zero. For any connected graph on $`n\geq2`$ vertices, a spanning tree gives the universal upper bound $`2n-3`$; paths attain it. A connected graph eventually requires all $`2^n-1`$ law coordinates under this full-law contract, even though each individual question requests only one terminal coordinate.

Disconnected graphs preserve a smaller and precisely described part of a law. A singleton-starting support never leaves its connected component, and every nonempty support within one component is reachable. For components $`B`$,

```math
\dim\mathcal V_\infty=1+\sum_B(2^{|B|}-1).
```

The saturated observables are exactly the functions $`c+\sum_B f_B(x_B)`$. Thus two initial laws are indistinguishable exactly when their component marginals agree. This does **not** assume independence: arbitrary cross-component dependence is permitted but invisible to the specified questions. Every tuple of component marginals is realizable by its product law, and Corollary 1B gives minimum continuous dimension $`\sum_B(2^{|B|}-1)`$. Two disjoint edges require six coordinates rather than the fifteen of their full joint law. Simultaneous joint readouts, recorded observations from several components, or feedback can introduce cross-component products and change this conclusion.

The hypotheses identify the application boundary. A fixed terminal coordinate uses the fixed-root formula; directed-only gates, clean auxiliary slots, restoration of other coordinates, reset or noisy gates, hidden state-dependent control, and parallel scheduling specify different problems. The formal source separately proves the visited-set bound, connected-witness synthesis and local character identity. The Walsh geometry, whole-word semantic correspondence, continuous lower bound and saturation arguments above remain ordinary mathematical proofs rather than new kernel claims. [21–22], [30]


### 2.5 Quantifying the information lost by a moment summary

Exact closure answers whether the required expectations can be recovered. When a proposed reduction omits part of the required observable space, there is also an exact answer to how much prediction error it necessarily permits. The answer supplies both an approximation that attains the best uniform error and two indistinguishable reference laws that prevent any decoder from improving it. This concerns uncertainty about a law on a fixed finite state space; it is not a claim about the memory needed to store one fully observed state. [1, Theorem 1][1]

#### Exact error and a pair of indistinguishable laws

Let $`X`$ be finite and nonempty, and let $`\mathcal V\subseteq\mathbb R^X`$ be a linear space containing the constant function one. Choose a basis $`1,\phi_1,\ldots,\phi_d`$ and retain only

```math
m_{\mathcal V}(\lambda)
  =\bigl(\mathbb E_\lambda\phi_1,\ldots,
          \mathbb E_\lambda\phi_d\bigr),
\qquad \lambda\in\Delta(X).
```

The mass coordinate is already known to equal one. For a required real function $`f`$, put

```math
\delta_{\mathcal V}(f)
  =\min_{g\in\mathcal V}\|f-g\|_\infty.
```

**Theorem 1C — Sharp recovery error from retained moments.** On the full probability simplex,

```math
\begin{aligned}
\delta_{\mathcal V}(f)
&=\frac12\max_{\substack{\lambda,\lambda'\in\Delta(X)\\
           m_{\mathcal V}(\lambda)=m_{\mathcal V}(\lambda')}}
       \left|\mathbb E_\lambda f-\mathbb E_{\lambda'}f\right|\\
&=\inf_\psi\sup_{\lambda\in\Delta(X)}
       \left|\mathbb E_\lambda f-
                 \psi\bigl(m_{\mathcal V}(\lambda)\bigr)\right|.
\end{aligned}
```

The decoder $`\psi`$ ranges over all real-valued functions on the attained summary image. It need not be linear or continuous. In particular, exact recovery for every law is possible if and only if $`f\in\mathcal V`$.

**Proof.** If two laws have the same retained moments, then for every $`g\in\mathcal V`$,

```math
\left|\mathbb E_\lambda f-\mathbb E_{\lambda'}f\right|
 =\left|\mathbb E_\lambda(f-g)-\mathbb E_{\lambda'}(f-g)\right|
 \leq2\|f-g\|_\infty.
```

Also, $`\mathbb E_\lambda g`$ is an affine function of the retained moments, with error at most $`\|f-g\|_\infty`$ for every law. A best approximation exists because this is a finite-dimensional approximation problem. These observations give the two upper bounds.

Finite-dimensional norm duality, equivalently the finite linear-programming dual below, gives

```math
\delta_{\mathcal V}(f)
 =\max\left\{\sum_{x\in X}v(x)f(x):
        v\perp\mathcal V,\ \sum_{x\in X}|v(x)|\leq1\right\}.
```

If the maximum is positive, a maximizer has $`\|v\|_1=1`$: a smaller norm could be scaled up to increase the positive objective. Orthogonality to the constant gives $`\sum_xv(x)=0`$, so the positive and negative parts each have mass $`1/2`$. Thus $`\lambda=2v_+`$ and $`\lambda'=2v_-`$ are probability laws. They have equal retained moments and their required expectations differ by $`2\delta_{\mathcal V}(f)`$. Any decoder returns the same number on their common summary, so its error on at least one law is at least half that separation. This proves both lower bounds. If the defect is zero, a best approximation equals $`f`$ and all equalities follow directly. $`\square`$

Nonlinear decoding therefore cannot improve the **uniform** optimum for this linear moment record and full-law contract. It can still choose a more informative answer on a particular fibre, and the theorem does not compare this record with arbitrary nonlinear encoders. Nor does it make the full-simplex necessity statement valid on a smaller justified family of laws. The approximation/moment-matching duality has the established antecedent identified in the source's comparison with Han, Jiao and Weissman; this finite application makes no new general duality claim. [1, “Sharp information loss” and Appendix C, P1][1]

#### Finite certificates and a particular retained record

Let $`\Phi`$ have basis evaluations as its rows, including the constant row. The approximation problem has the explicit finite form

```math
\begin{gathered}
\min_{a\in\mathbb R^{d+1},\ t\geq0}t,\\
-t\leq f(x)-\sum_{j=0}^{d}a_j\phi_j(x)\leq t
\quad(x\in X),\qquad \phi_0=1.
\end{gathered}
```

Only $`t`$ is constrained to be nonnegative; the approximation coefficients are unrestricted. A matching countermodel problem maximizes

```math
\frac12\sum_{x\in X}\bigl(\lambda(x)-\lambda'(x)\bigr)f(x)
```

subject to $`\Phi\lambda=\Phi\lambda'`$, nonnegative law entries and unit mass for both laws. Interchanging the two laws supplies either sign. Theorem 1C proves that its optimum equals the approximation optimum. Rational finite data admit rational optimal certificates; an approximate optimizer can propose coefficients and laws, while their stated inequalities, normalization and objective equality require their own exact verification. No execution is needed for the general proof above. [1, “An executable specification”][1]

For a particular attained record $`y`$, the compatible laws form the nonempty compact polytope

```math
\mathcal P(y)=\{\lambda\in\Delta(X):m_{\mathcal V}(\lambda)=y\}.
```

For a declared failure observable $`b\in[0,1]^X`$, its lowest and highest compatible risks are

```math
\underline r(y)=\min_{\lambda\in\mathcal P(y)}\mathbb E_\lambda b,
\qquad
\overline r(y)=\max_{\lambda\in\mathcal P(y)}\mathbb E_\lambda b.
```

Both are finite linear programs. Their midpoint minimizes the largest absolute error on this fibre, with error $`(\overline r(y)-\underline r(y))/2`$: the two endpoint laws force that lower bound, and the midpoint is within it of every value between the endpoints. A positive global defect can coexist with a local upper risk small enough for the declared task. Conversely, a universal guarantee must survive every attained fibre. For any such bounded observable, the constant prediction $`1/2`$ gives $`\delta_{\mathcal V}(b)\leq1/2`$; equality entails compatible laws with risks zero and one. [1, Theorem 1 and “Local certificates”][1]

These intervals are conditional on the supplied state space, observable and actual uncertainty set. Noisy moment estimates must be represented by constraints that contain the possible true moments, such as interval constraints on $`\Phi\lambda`$, rather than equated to exact data. A numerical risk bound is useful only when the actual reference law is covered. It supplies neither the semantic validity of the failure observable nor an independent warrant for the source model.

#### A lower bound even when approximate answers are allowed

Return to the complete-graph pairwise sign dynamics of §2.4, on $`X=\{-1,+1\}^n`$, with $`n\geq2`$ and a nonnegative integer horizon $`h`$ counting elementary updates. The already proved exact horizon law requires the nonconstant characters with $`1\leq|S|\leq\min(n,h+1)`$. Write their number as

```math
m_h=\sum_{k=1}^{\min(n,h+1)}\binom nk,
\qquad b_S=(1-\chi_S)/2.
```

Each $`b_S`$ is the negative-sign event for an admitted terminal unary readout. Suppose the retained record consists of linear moments whose span together with constants has dimension $`d+1`$, with a separate arbitrary decoder for each required event probability. Thus $`d`$ counts informative coordinates independently of the known mass.

**Proposition 1D — Approximate linear-moment memory.** If every required $`\mathbb E_\lambda b_S`$ can be recovered with absolute error at most $`\epsilon`$ for every law, where $`0\leq\epsilon\leq1/2`$, then

```math
d\geq m_h(1-4\epsilon^2).
```

**Proof.** Equip functions on $`X`$ with the normalized uniform-law inner product, and let $`P`$ be orthogonal projection onto the retained space $`\mathcal V`$, including constants. The selected Walsh characters are orthonormal and orthogonal to the constant. Their projections therefore use only the $`d`$-dimensional nonconstant part of $`\mathcal V`$. Bessel's inequality gives

```math
\sum_S\|P\chi_S\|_2^2\leq d,
\qquad
\sum_S\|\chi_S-P\chi_S\|_2^2\geq m_h-d.
```

If $`d\geq m_h`$, the claimed bound is immediate. Otherwise some character has squared projection error at least $`1-d/m_h`$. Best uniform approximation error is at least best normalized $`L^2`$ approximation error. Since constants belong to $`\mathcal V`$,

```math
\delta_{\mathcal V}(b_S)=\tfrac12\delta_{\mathcal V}(\chi_S).
```

Theorem 1C applies to the corresponding arbitrary decoder and yields

```math
\epsilon\geq\frac12\sqrt{1-d/m_h}.
```

Rearranging proves the result. $`\square`$

The integer coordinate count requires the ceiling of the displayed bound. For eight slots and horizon at least seven, $`m_h=255`$. Error at most $`0.1`$ on every required event probability therefore needs at least $`245`$ linear moment coordinates, even with nonlinear decoders. At zero error the bound gives $`d\geq m_h`$; at error $`1/2`$ it permits the constant predictions. Intermediate tolerances are necessary bounds, not claimed exact optima. The approximate theorem concerns linear moment acquisition. The stronger allowance of arbitrary **continuous encoders** in the exact theorem of §2.4 does not extend to this approximate statement. [1, Proposition 4][1]

#### Applying the defect to a future inquiry

For a fixed finite horizon, §2.2 supplies the branch-probability and terminal-numerator functions that must be evaluated on the initial law. Theorem 1C can be applied to each of those functions relative to the actually retained space. A finite declared family $`\mathcal Q`$ of normalized questions has uniform defect $`\max_{f\in\mathcal Q}\delta_{\mathcal V}(f)`$. Taking the maximum over an unrestricted linear span would be inappropriate: scaling any missing function would make its nonzero error unbounded. Likewise, a small error for branch numerators is not automatically a small error for conditional answers. [1, “A continuation-sensitive discharge condition”][1]

To make the latter distinction quantitative, suppose a branch has probability $`p\geq\beta>0`$ and an event numerator $`0\leq N\leq p`$. Assume estimates obey $`|\widehat N-N|\leq\epsilon_N`$ and $`|\widehat p-p|\leq\epsilon_p\lt{}\beta`$. Put $`q=N/p`$. Then

```math
\left|q-\mathrm{clip}_{[0,1]}
                  \left(\frac{\widehat N}{\widehat p}\right)\right|
\leq\frac{\epsilon_N+\epsilon_p}{\beta-\epsilon_p}.
```

Indeed $`\widehat p\geq\beta-\epsilon_p>0`$, and

```math
|\widehat N-q\widehat p|
\leq|\widehat N-N|+q|p-\widehat p|
\leq\epsilon_N+\epsilon_p.
```

Division by the positive lower bound and the fact that clipping cannot increase distance to $`q\in[0,1]`$ prove the assertion. The positive margin is a substantive premise. Section 3.2 separately explains why a null event does not select a unique limiting posterior. [1, “Conditional estimates must retain conditioning margins”][1]

The resulting options are precise. Retain enough observables for exact recovery; retain a smaller record with a proved task-specific error; acquire missing information through an admitted operation; or reduce the promised future question family. Section 9.2 gives the existing rank argument for the extra continuous coordinates needed for selected expected values on a fixed positive fibre. For a future contract, the required rows must first include its admitted continuation functions, as in §2.2. Neither that coordinate count nor the defect is a price for acquiring the information. A retrievable archive contributes only the information that the declared operations can actually recover, and a risk bound does not replace the independent premises for permission, source authenticity or epistemic warrant.

### 2.6 What a reduction must preserve for the next inquiry

A record can correctly show how an earlier obligation was handled while omitting information needed for an admitted future question. Conversely, a sufficient predictive statistic can omit a source or version condition required for the legitimate use of its answer. The historical record, the future predictive contract and the conditions for an actually usable proof are distinct. Sections 9.4–9.5 already give the robust-certificate and accessible-evidence arguments; the continuation result supplies the additional question of which future quantities survive a reduction. [1, “What changes in witnessed discharge”][1]

Fix the finite model, its declared action–observation instruments and a finite horizon. Let $`W_h`$ be the span of the actual required branch-probability and terminal-numerator functions, as in §2.2, and let $`\mathcal V`$ be the linear span of the constants and the currently retained moment functions. Exact recovery after the reduction is equivalent to

```math
W_h\subseteq\mathcal V.
```

This is the existing predictive criterion applied to the retained space. If containment fails, at least one actual generating question lies outside $`\mathcal V`$; otherwise their span would be contained in it. Theorem 1C supplies two laws with the same retained record and different answers to that question, together with the exact best uniform error. A smaller declared question family or a quantified error tolerance can be sufficient for a different contract. The contract cannot promise the unchanged family at exact accuracy merely by recording that the old representation was transferred, superseded or discharged.

The missing information need not be the entire discarded record. Retaining the existing moments, the exact minimum number of additional **continuous real statistics of the law**, over the full simplex, is

```math
a_{\min}=\dim(\mathcal V+W_h)-\dim\mathcal V.
```

For sufficiency, extend a basis of $`\mathcal V`$ to a basis of $`\mathcal V+W_h`$ using functions in $`W_h`$ and retain their expectations. For necessity, let $`\Phi`$ and $`H`$ have bases of $`\mathcal V`$ and $`W_h`$ as rows. The rank calculation already used in §9.2 gives

```math
\mathrm{rank}(H|_{\ker\Phi})
 =\mathrm{rank}\,\begin{bmatrix}\Phi\\H\end{bmatrix}
        -\mathrm{rank}\,\Phi
 =a_{\min}.
```

Because $`\Phi`$ includes the constant row, these kernel directions preserve mass. At a strictly positive law, a small open neighbourhood in a subspace on which this restricted map is injective stays within one retained-moment fibre. The continuous-coordinate obstruction proved in §9.2 therefore requires at least $`a_{\min}`$ added coordinates for any scheme that works on the full simplex. The basis construction works on boundary laws as well. This applies the existing rank mechanism to the continuation rows; it introduces no additional topological assumption or new proof of invariance of domain. If the rank is zero, no supplement is needed. [1, Proposition 9][1]

The count presumes access to the stated statistics of a law. It is neither the number of measurements needed to estimate them nor the price of a permitted query. An admitted retrieval operation can make an archived component part of the accessible information, while a hash or historical pointer with no usable retrieval path supplies no such access. [Source Context and Reacquisition, §§6.5 and 7.3](../epistemology/source-context-and-reacquisition.md#65-information-preserved-and-access-preserved) gives an explicit example in which equally authentic retained witnesses leave different future acquisition costs. An operational reduction must consequently be interpreted at its actual model and contract version, available statistic, future menu, horizon and error scope; algebraic contraction alone does not establish these application premises.

There is a further distinction between meeting a reference-model requirement and being able to establish that fact from the retained record. Let $`\mathcal M`$ be a finite family of continuation protocols whose feasibility and permission premises have been separately supplied, and let $`b_c\in[0,1]^X`$ be each protocol's reference-model failure observable. For a risk threshold $`\epsilon`$, define

```math
\mathcal L_\epsilon(\lambda)
 =\{c\in\mathcal M:\mathbb E_\lambda b_c\leq\epsilon\},
\qquad
\widehat{\mathcal L}_\epsilon(y)
 =\{c\in\mathcal M:
       \sup_{\mu\in\mathcal P(y)}\mathbb E_\mu b_c\leq\epsilon\}.
```

If the actual reference law $`\lambda`$ belongs to the declared uncertainty set $`\mathcal P(y)`$, then $`\widehat{\mathcal L}_\epsilon(y)\subseteq\mathcal L_\epsilon(\lambda)`$, since the supremum includes that law. This is the risk-specific application of the robust-completion intersection in §9.4, rather than a replacement definition of physical or logical possibility. The premise that the uncertainty set contains the actual law remains independent evidence, and the risk inequality does not supply permission.

The inclusion can be strict. On the complete-graph sign system, let $`\lambda_+`$ and $`\lambda_-`$ be uniform on the two opposite full-parity classes. Their proper-subset moments agree. The accumulating pairwise continuation from §2.4 has terminal failure observable $`b=(1-\chi_{\{1,\ldots,n\}})/2`$, with expectations zero and one respectively. If the actual law is $`\lambda_+`$ but the retained record consists only of proper-subset moments, both laws remain compatible. For $`0\leq\epsilon\lt{}1`$, this continuation meets the actual reference-model risk bound but cannot be certified from that record. Its actual modelled capability has not disappeared; the available information does not establish it. The same pair gives the hidden-reference-game argument in [Collective Inquiry, §5.2](collective-inquiry-and-strategic-coordination.md#52-a-hidden-interaction-changes-the-equilibrium). [1, “Objective possibilities versus certifiable possibilities”][1]

A historical witness can therefore remain traceable while the operative summary loses a future distinction. In the other direction, a summary that preserves all declared probabilities may omit a provenance or source-version distinction required for a complete admissible output, as §9.4's same-action/different-certificate example shows. A transfer of custody is not itself a proof that a still-relevant issue has been resolved. These comparisons concern the declared representation and evidence contracts, not whether a subject actually believes or knows the decoded proposition.

These constraints admit constructive alternatives. A full joint-law record always suffices, and a predictive-state record based on the required continuation span preserves the exact contract without retaining every historical detail. A justified restricted law family, shorter horizon or narrower menu can reduce the cost. The source also retains Rudary and Singh’s nonlinear predictive-state examples of exponential compression for deterministic binary predictions; that contract does not encode all arbitrary joint laws on the full simplex assumed here. It identifies Baisero and Amato’s reward-predictive representations as close prior art for adding consequence observables to a prediction model. These positive comparisons prevent a general claim that nonlinearity never helps or that adding consequence functions is itself a new general principle. [1, Appendix C, P8–P9][1]

The positive repair is correspondingly targeted. Form the pulled-back function for the newly required continuation. Its finite approximation or compatible-fibre program can establish the declared error or risk bound. If the uniform defect exceeds the permitted prediction tolerance, the dual supplies an indistinguishable pair on which no common answer meets that tolerance. Added information must distinguish this pair to meet the same uniform contract. Where the declared service supplies the needed access, a repair can retain a missing observable, use a justified informative query, or restore an accessible archive; alternatively, it can revise the affected future menu. A separating query for one pair is not by itself a proof of adequacy for every compatible law; the resulting record must still meet the actual contract. [1, “An implementable certify–refine rule”][1]

Under fixed finite instruments, adding a missing observable strictly increases the retained span, and taking its continuation closure terminates after finitely many strict increases by §2.2. This is termination of a finite algebraic construction, not a guarantee that the required observations can be acquired or that real-world inquiry and restoration terminate. Expanding a menu can increase the required rank within an analysis that already parameterizes that menu; changing the analysis itself is a separate revision. Restricting the menu can lower the information burden while losing useful opportunities, whose value is not their number or their rank. Full-law coverage, exactness, the future menu, reacquisition and memory capacity are consequently explicit premises in any preservation promise. Optimizing retained information, later queries, permitted continuations and tolerated error under a justified model remains a further problem. [1, Corollary 5 and “The next substantive frontier”][1]

## 3. The information hidden between target and audit marginals

Let target $`\Theta`$, source type $`T`$, report $`Y`$, and verifier $`V`$ be binary. The target and type are independent and uniform. The report is $`9/10`$-accurate for a good source and $`1/2`$-accurate for a bad source. The verifier is $`4/5`$-accurate and conditionally independent of the report given $`(\Theta,T)`$. Define

```math
D=\mathbf1[V\ne Y],\qquad A=(T,D).
```

Reading this already existing audit is a diagonal projector. After reading the report, the eight joint masses of $`(\Theta,T,D)`$ suffice for future readings of $`A`$. If $`G`$ groups the sixteen latent masses and $`P_a`$ selects audit value $`a`$, then $`GM_a=P_aG`$, and the target readout factors through $`G`$. Target indicators multiplied by audit selectors give all eight joint indicators, proving closure rank eight. Adding future report readings on the unrestricted latent-law simplex raises the rank to sixteen: $`(\Theta,T,Y,D)`$ determines $`V`$.

The stated prior gives

```math
\Pr(\Theta=1\mid Y=1)=\frac7{10},\quad
\Pr(A=(\mathrm{Bad},1)\mid Y=1)=\frac14,\quad
\Pr(\Theta=1\mid Y=1,A=(\mathrm{Bad},1))=\frac15.
```

On the known-bad slice, in the order $`(\Theta,D)=(0,0),(0,1),(1,0),(1,1)`$, the two report histories give

```math
\pi_0=(2/5,1/10,1/10,2/5),\qquad
\pi_1=(1/10,2/5,2/5,1/10).                                   \quad\text{(5)}\quad
```

Both target and audit marginals are uniform. Nevertheless $`D=1`$ gives target-one posterior $`4/5`$ or $`1/5`$. The missing datum is a joint numerator, not an audit marginal.

Use the moments of $`1,\tau,\delta,\tau\delta`$, with $`\tau=(-1)^\Theta`$ and $`\delta=(-1)^D`$. Write them $`(m,t,d,h)`$. Multiplying by the projector $`(1+s\delta)/2`$, $`s=(-1)^b`$, yields

```math
m'=(m+sd)/2,\quad t'=(t+sh)/2,\quad d'=sm',\quad h'=st'.       \quad\text{(6)}\quad
```

When $`m'>0`$, the target-one posterior is $`(1-t'/m')/2`$. The vector $`(1,0,0,2)`$, despite plausible separate marginals, reconstructs signed masses $`(3/4,-1/4,-1/4,3/4)`$ and can yield a negative posterior. It is excluded by the admissible cone.

Rereading the same result is not a fresh observation. Matching projectors are idempotent; after posterior $`1/5`$, the matching reread has probability one and leaves that posterior unchanged. A contradictory reread is impossible. Two fresh conditionally independent disagreements instead give

```math
\frac{(1-\alpha)^2}{(1-\alpha)^2+\alpha^2}=\frac1{17}
\quad\text{when }\alpha=4/5.
```

The instruments differ. Also, rank four for arbitrary laws on $`(\Theta,D)`$ does not demand three real coordinates for the two particular histories in (5); those two histories need only one distinguishing bit. [2]


### 3.1 The higher-order interaction and its loss

The known-bad model has a general form. Let $`\Theta,Y`$ be independent fair bits, and let the verifier satisfy $`\Pr(V=\Theta\mid\Theta,Y)=\alpha\in(0,1)`$. Thus its error is conditionally independent of the report given the target. Put $`D=Y\mathbin{\mathsf{xor}}V`$ and $`\rho=2\alpha-1`$. Then

```math
\Pr(\Theta=t,Y=y,D=d)=\frac{1+\rho(-1)^{t+y+d}}8.              \quad\text{(24)}\quad
```

Summing any index eliminates the signed term, so every one-variable and two-variable marginal is uniform. Yet

```math
\mathbb E[(-1)^\Theta(-1)^Y(-1)^D]=\rho.
```

The probability array is a three-slot tensor. Marginalization contracts a slot against the all-ones covector and kills this signed component; contracting all three slots against sign covectors recovers it. This is a tensor-slot statement, not a tensor-decomposition-rank claim.

Conditioning (24) gives

```math
\Pr(\Theta=1\mid Y=y,D=d)=\frac{1-\rho(-1)^{y+d}}2.
```

Erasing $`Y`$ while retaining $`D`$ returns $`1/2`$. Under half-Brier loss the excess risk is the square of the binary posterior error, $`\rho^2/4`$, at every outcome and hence in expectation. At accuracy $`4/5`$, it is $`9/100`$. This is a concrete use of the classical parity-interaction mechanism. It does not make every neutral historical datum necessary: relevance arises from the specifically admitted future audit. A reduction correct for a smaller family of immutable-factor operations need not remain correct after this joint observation is added. [11]

### 3.2 Conditioning cannot choose a model revision at a null audit

Let the target have at least two states and let $`p(\theta)>0`$ be normalized. Take a baseline law

```math
P_0(\theta,A=0)=p(\theta),\qquad P_0(\theta,A=1)=0.
```

For any positive target law $`q`$ and
$`0<\epsilon<\min_\theta p(\theta)/q(\theta)`$, define

```math
P_\epsilon(\theta,1)=\epsilon q(\theta),\qquad
P_\epsilon(\theta,0)=p(\theta)-\epsilon q(\theta).             \quad\text{(25)}\quad
```

Every cell is positive, the target marginal remains exactly $`p`$, and

```math
P_\epsilon(\theta\mid A=1)=q,\qquad
\|P_\epsilon-P_0\|_{\mathrm{TV}}=\epsilon.
```

The variation identity follows because the absolute changes in the two audit columns sum to $`2\epsilon`$.

Choose two distinct positive $`q`$'s. Both positive-model families approach the same baseline with the same target marginal, but their audit-conditioned posteriors have different limits. Therefore the impossible event has no unique continuous conditional extension selected by the baseline alone. A smoothing rule supplies additional modelling information.

A fixed positive model has a unique posterior. The result does not prohibit rational revision of a zero-probability assessment; it separates such revision from conditioning inside the original model. Applied after a retained history, the argument uses its full positive support and says nothing about hypotheses excluded by that support. Changing the target, source claim, or audit authentication requires its own warranted modelling justification. [12]

## 4. Posterior equivalence and its finite tensor test

Two live states are posterior-equivalent if they admit the same words and give the same target posterior after every feasible word, including the empty word. They need not predict word probabilities.

For example, keep a uniform target independent of a source bit $`S`$, and observe source-only likelihoods $`f(0)=1/4,f(1)=3/4`$ and $`1-f`$. Beliefs with $`\Pr(S=0)=3/4`$ and $`1/4`$ give the same uniform target posterior after every word; all words are possible. Their next first-outcome probabilities are $`3/8`$ and $`5/8`$.

For each target row $`c`$, define

```math
d_c=c\otimes u-u\otimes c,\qquad N_a=M_a\otimes M_a.
```

Let $`U`$ be the least row space containing the $`d_c`$ and invariant under right multiplication by the $`N_a`$.

**Theorem 2 — Posterior comparison.** Live nonnegative $`x,y`$ are posterior-equivalent exactly when their feasible-word languages agree and

```math
v(x\otimes y)=0\quad\text{for every }v\in U.                  \quad\text{(7)}\quad
```

**Proof.** On a common feasible word, posterior equality is equivalent to

```math
(cM_wx)(uM_wy)-(uM_wx)(cM_wy)=0.
```

The left side is $`d_c(M_w\otimes M_w)(x\otimes y)`$. The mixed-product identity gives $`N_w=M_w\otimes M_w`$; both factors use the same word. These rows span $`U`$. Both successors vanish on a jointly impossible word. Conversely, common feasibility permits division precisely on the positive branches. $`\square`$

All generators are antisymmetric under factor exchange, and each $`N_a`$ preserves that subspace. Consequently $`\dim U\leq n(n-1)/2`$. The tensor dimension is the size of a comparison construction, not a one-belief memory minimum. Under the column convention, right multiplication of a row by $`N_a`$ prepends $`a`$ to its chronological word. A witness-producing implementation must retain that convention.

The feasibility guard is essential. If only one successor is zero, every cross-product at that word still vanishes. Two states with the same target and different perfectly observed source bits illustrate this failure.

Nonnegative supports update by

```math
F_a(S)=\{i:\ M_a[i,j]>0\text{ for some }j\in S\}.
```

Explore support pairs under synchronized $`(F_a,F_a)`$. Exactly one empty component witnesses a language difference; otherwise complete exploration establishes equality. There are at most $`4^n`$ pairs. With the finite supplied alphabet and rational, explicitly supplied $`M_a,C,x,y`$, this test and invariant-space closure are exact terminating algorithms. Arbitrary uncomputable real coefficients or an unspecified infinite alphabet do not provide that guarantee.

A common feasible first observation preserves all continuation comparisons, giving a set-theoretic partial quotient. This does not supply a convenient linear or finite-dimensional posterior-state parameterization. The product and invariant-span methods have established predictive-state and weighted-automata antecedents. [2], [8], [9]

## 5. Fixed audits and the value of inquiry

Let a single already existing audit have $`k`$ labelled outcomes and the target have $`r`$ states. Let $`p_j`$ be the conditional target law, $`w_j>0`$ its audit weight, and

```math
Q=[p_1\ \cdots\ p_k],\qquad q=Qw.
```

The posterior-only signature is

```math
F(w,P)=(p_1,\ldots,p_k,q).                                    \quad\text{(8)}\quad
```

The empty word returns $`q`$; a nonempty constant audit word returns its $`p_j`$; a word with distinct audit labels is impossible. Thus (8), together with feasibility, gives all future posterior answers for this fixed-audit repertoire.

At fixed $`P,q`$, the hidden weights form

```math
W_{P,q}=\{w>0:Qw=q\}.                                        \quad\text{(9)}\quad
```

Assume this set is nonempty and $`q`$ is normalized. Column stochasticity already implies $`\sum_jw_j=1`$. Every difference of representatives lies in $`\ker Q`$; conversely, for $`w^0\in W_{P,q}`$ and $`v\in\ker Q`$, the vectors $`w^0\pm\epsilon v`$ remain in the fibre for sufficiently small $`\epsilon>0`$.

For two feasible outcomes, distinct posterior columns determine the audit weight uniquely from $`q=(1-t)p_0+tp_1`$. Coincident columns both equal $`q`$, leaving the audit frequency undetermined. For a binary target, the signature therefore reconstructs the joint law off independence but collapses its audit-frequency fibre on independence. Boundary feasibility identifies the supported outcome at $`t=0`$ or $`1`$. The strictly positive off-independence family contains an open three-dimensional set on which the signature is injective; invariance of domain therefore still excludes a globally exact continuous encoder into fewer than three real coordinates. [2]

### 5.1 The expectation criterion

**Theorem 3 — Expected quantities on a positive fibre.** For $`h\in\mathbb R^k`$, the value $`h^\mathsf Tw`$ is constant on the whole fibre (9) if and only if $`h^\mathsf T\in\mathrm{row}\,Q`$.

**Proof.** If $`h^\mathsf T=b^\mathsf TQ`$, its value is $`b^\mathsf Tq`$. Conversely, constancy on $`w^0\pm\epsilon v`$ implies $`h^\mathsf Tv=0`$ for every $`v\in\ker Q`$. The equality $`(\ker Q)^\perp=\mathrm{row}\,Q`$ completes the proof. $`\square`$

For a Bayes-risk function $`H`$, finite at the relevant laws, set $`h_j=H(p_j)`$. Expected improvement is

```math
H(q)-\sum_jw_jH(p_j).                                        \quad\text{(10)}\quad
```

A constant audit cost subtracts a constant. Outcome-dependent costs introduce their own expectation vector. On a restricted reachable family, use the span of actual admissible weight differences instead of the full $`\ker Q`$. On a boundary face, restrict to active support when the relative fibre has a positive point. These qualifications prevent a sufficient whole-fibre criterion from becoming a false necessity on smaller domains. [3]

### 5.2 A decision reversal with three outcomes

For a binary target, take conditional target-one probabilities

```math
(1/4,1/2,3/4),\qquad w=(a,1-2a,a),\quad 0\lt{}a<1/2.
```

Every joint cell is positive and $`q=1/2`$ for every $`a`$. Posterior answers and feasibility agree for all words.

For half-Brier loss, $`H(p)=p(1-p)`$. Expected improvement is

```math
\frac14-\left(\frac{3a}{16}+\frac{1-2a}{4}+\frac{3a}{16}\right)
=\frac a8.
```

At $`a=1/4`$ and $`1/8`$, the gains are $`1/32`$ and $`1/64`$. A common cost $`3/128`$ gives net values $`+1/128`$ and $`-1/128`$, reversing the preferred audit-versus-skip action.

The boundary example with posteriors $`(0,1/2,1)`$ has gain $`a/2`$; a cost $`3/32`$ gives net values $`\pm1/32`$ for the same weights. The interior example proves that the obstruction is not a zero-cell artifact.

For distinct interior target laws $`p_0,p_1`$, midpoint $`p_*=(p_0+p_1)/2`$, and finite strictly concave Bayes risk on these laws, the analogous gain is

```math
a\bigl(2H(p_*)-H(p_0)-H(p_1)\bigr)>0.
```

Thus the phenomenon is not restricted to binary targets or quadratic loss.

Three outcomes are minimal for this particular value-loss obstruction. With two distinct posterior columns the weights are determined; with coincident columns the expected value of every finite function of the posterior is fixed and risk improvement is zero. A single feasible outcome also gives zero improvement. This is a theorem for one fixed audit, finite posterior risk, and constant cost, not for arbitrary fresh experiments, outcome-dependent costs, or adaptive policies. The posterior matrix $`Q=\Pr(\Theta\mid D)`$ and the target law are fixed here; the forward channel $`\Pr(D\mid\Theta)`$ generally varies with $`w`$. [3]

### 5.3 What changes when the future inquiry menu changes

The fixed-audit calculation holds one inquiry repertoire constant. An inquiry can also change which later inquiries are feasible. The formalisation source separates that change from the truth of its result and supplies a bounded way to compare its consequences. [FORM, §7][FORM]

Fix an analysis $`A`$ and a full environment state $`z`$ that can include available information, access rights, resources, governing conditions and retained history. Let $`\gamma_A(z)`$ describe the historical inquiry graph. Independently define a universe $`\mathscr J_A`$ of finitely described actions or bounded contingent plans, with a declared feasibility predicate, and put

```math
\mathcal L_A(z)
 =\{q\in\mathscr J_A:\mathrm{Feas}_A(z,q)=1\}.
```

The historical graph, the currently feasible menu and an agent's estimate $`\widehat{\mathcal L}_A(z)`$ are different objects. They can be related by substantive rules; their separate definitions do not require statistical independence. The menu can be infinite even when each plan has a finite description. The risk-based distinction between actual and certifiable options in §2.6 is one specialised instance of the information question, with permission and physical feasibility still supplied separately.

A plan's typed shape cannot generally determine its eligibility. Two source-access plans can have the same argument roles while one has the required permission and the other lacks it. Their shapes agree and their feasibility values differ. Two individually feasible plans can also compete for an exclusive resource, as the support criterion in [Collective Inquiry, §5.3](collective-inquiry-and-strategic-coordination.md#53-independent-feasibility-is-a-support-property) proves. The menu is therefore neither a set of tensor degrees nor a vector space closed under arbitrary combination.

Let an admitted closure action carry $`z`$ to $`z'`$ while $`A`$ stays fixed. A publication, for example, can remove the opportunity for a particular actor's independent discovery *before seeing that disclosure*, while enabling learning, another proof or a new investigation. That change does not require a new analysis. If inquiry identities are comparable in a common universe, the definitions

```math
C=\mathcal L_A(z)\setminus\mathcal L_A(z'),
\qquad
N=\mathcal L_A(z')\setminus\mathcal L_A(z)
```

give the exact identity $`\mathcal L_A(z')=(\mathcal L_A(z)\setminus C)\cup N`$. This records a set change. Causal attribution requires a justified comparison of alternative transitions from the relevant pre-state; the identity alone establishes neither causation nor harm. A change of analysis or inquiry identity needs its own comparison maps. [FORM, “Landscape evolution with a fixed analysis”][FORM]

For a chosen horizon $`h`$, let $`\mathscr J_A^h`$ be the admitted plan family and $`J_A(z,q)`$ a bounded real value, with costs, uncertainty and whose interests count explicitly fixed. Include a stop option of value zero and define

```math
\mathrm{Opt}_{A,h}(z)
 =\sup\bigl(\{0\}\cup
 \{J_A(z,q):q\in\mathcal L_A(z)\cap\mathscr J_A^h\}\bigr).
```

Boundedness and the stop option make this a finite nonnegative value; no maximising plan is assumed to exist in an infinite menu. With a deterministic successor $`F_A(z,a)`$, an immediate reward can be joined to the prospective value as

```math
\mathrm{Tot}_{A,h}(z,a)
 =R_A^{\mathrm{imm}}(z,a)
  +\mathrm{Opt}_{A,h}(F_A(z,a)).
```

A stochastic or set-valued successor needs a declared expectation, worst-case or other comparison rule. Incomparable objectives can instead retain an attainable-value set or partial order. None of these evaluations removes a hard admissibility requirement.

**Correctness leaves future option value undetermined.** Take an initial menu whose best option has value $`6`$. Two admissible closures establish the same true theorem and have equal immediate reward. A thin closure leaves only a reconstruction option valued $`2`$; an expository closure leaves a transferable-mechanism option valued $`10`$. Their prospective changes are $`-4`$ and $`+4`$. Correctness is identical, while future value differs; interchanging the two successor assignments reverses the comparison without changing correctness. This finite countermodel establishes that correctness does not determine prospective value under the declared data. Its numbers are not measurements of researchers, communities or AI-assisted mathematics. The publication-race example in [Collective Inquiry, §3.3](collective-inquiry-and-strategic-coordination.md#33-changing-inquiry-can-change-incentives) adds a separate incentive structure to this distinction. [FORM, Proposition 7.2][FORM]

Cardinality also fails to determine the value. Removing an option valued $`2`$ while retaining a maximiser valued $`6`$ gives a strict menu contraction with unchanged optimum. Replacing a two-option menu of values $`1,2`$ by one option valued $`10`$ gives fewer options and a larger optimum. The second comparison changes the menu or its state-dependent values; deleting options alone while keeping every retained value fixed cannot increase a supremum. Thus the conclusion is compatible with ordinary value monotonicity under set inclusion. Closing a refuted or dominated route can remove waste without sacrificing the best available value. The appropriate comparison concerns the stated values, costs and constraints, rather than a universal requirement to keep the largest number of questions open. [FORM, Proposition 7.3][FORM]

## 6. The categorical Fisher dynamics of the full source

Assume $`r,k\geq2`$ and every joint cell is positive. Write

```math
X=\Delta_k^\circ\times(\Delta_r^\circ)^k,\qquad
\mu_{ji}=w_jp_{ji},\qquad S=F(X)\subseteq A=(\Delta_r^\circ)^{k+1}.
```

Let $`J(P,q)`$ be an ambient $`C^2`$ objective and $`E=J\circ F`$. The metric is the categorical Fisher metric of the joint law $`\mu`$. It is not a separately stipulated metric on retained coordinates.

Let $`J_j`$ denote the derivative in slot $`p_j`$, let $`h=J_q`$, and define

```math
C(p)=\mathrm{diag}(p)-pp^\mathsf T,\qquad a_j=C(p_j)J_j.
```

Derivatives are intrinsic to simplex affine spaces; Euclidean representatives may differ by constants times the all-ones vector.

### 6.1 Derivation

Expanding $`d\mu_{ji}=p_{ji}\,dw_j+w_j\,dp_{ji}`$, with $`\sum_i dp_{ji}=0`$, gives

```math
g((\delta w,\delta P),(\eta w,\eta P))
=\sum_j\frac{\delta w_j\eta w_j}{w_j}
+\sum_jw_j\sum_i\frac{\delta p_{ji}\eta p_{ji}}{p_{ji}}.       \quad\text{(11)}\quad
```

The cross terms vanish. Since

```math
dE=\sum_j\langle h,p_j\rangle dw_j+
\sum_j\langle J_j+w_jh,dp_j\rangle,
```

and the inverse simplex Fisher operator is $`C(p)`$, negative gradient descent is

```math
\dot w_j=-w_j\langle h,p_j-q\rangle,\qquad
\dot p_j=-C(p_j)h-\frac{a_j}{w_j}.                            \quad\text{(12)}\quad
```

The covariance decomposition

```math
\sum_jw_jC(p_j)+\sum_jw_j(p_j-q)(p_j-q)^\mathsf T=C(q)
```

then yields

```math
\dot q=-C(q)h-\sum_ja_j,\qquad
\dot\mu_{ji}=-\mu_{ji}(h_i-\langle q,h\rangle)-a_{ji}.          \quad\text{(13)}\quad
```

The objective decreases:

```math
\dot E=
-\sum_jw_j\langle h,p_j-q\rangle^2
-\sum_j\frac{(J_j+w_jh)^\mathsf TC(p_j)(J_j+w_jh)}{w_j}
\leq0.                                                       \quad\text{(14)}\quad
```

For positive $`p`$,

```math
z^\mathsf TC(p)z=\sum_ip_i(z_i-\langle p,z\rangle)^2,
```

so $`\ker C(p)=\mathrm{span}\{1\}`$. Every formula is gauge-invariant, and $`a_j=0`$ means that the intrinsic differential in slot $`p_j`$ vanishes.

Two ambient objectives agreeing on $`S`$ have identical source pullbacks and intrinsic source gradients. Arbitrary off-image values are irrelevant. Decreasing the stipulated loss does not establish that an actual belief change is warranted. [4]

### 6.2 The exact pointwise criterion

An index $`j`$ is **variable** at $`(P,q)`$ if some two weights in (9) differ in component $`j`$. Equivalently,

```math
\exists v\in\ker Q:\ v_j\ne0
\quad\Longleftrightarrow\quad
\mathrm{rank}(Q\text{ with column }j\text{ deleted})
=\mathrm{rank}\,Q.                                      \quad\text{(15)}\quad
```

Indeed a kernel vector with nonzero $`j`$-component expresses column $`j`$ as a linear combination of the others, and conversely. Small positive kernel perturbations establish the fibre equivalence.

**Theorem 4 — Pointwise Fisher descent.** The full projected velocity $`(\dot P,\dot q)`$ is independent of the representative $`w\in W_{P,q}`$ exactly when

```math
C(p_j)J_j=0\quad\text{for every variable index }j.            \quad\text{(16)}\quad
```

**Proof.** Equation (13) for $`\dot q`$ has no weight dependence. In each separately retained conditional slot in (12), the only such dependence is $`a_j/w_j`$. If $`w_j`$ varies, equality forces $`a_j=0`$; if it is fixed, its denominator is already determined. No cancellation between different conditional slots is possible. $`\square`$

A nontrivial fibre need not make every index variable. For

```math
p_1=p_2=(1/2,1/4,1/4),\qquad p_3=(1/4,1/4,1/2),
```

the kernel is spanned by $`(1,-1,0)`$. The objective $`J=p_{3,1}`$ satisfies (16) at that signature even though its third conditional differential is nonzero. The stronger global classification below requires an additional density argument.

### 6.3 From velocities to maximal source trajectories

Projectability at a point is not, by itself, a theorem about complete trajectories on a singular quotient. Here the special source equations supply the missing argument.

**Theorem 5 — Exact maximal-flow descent.** For ambient $`C^2`$ $`J`$, condition (16) at every admissible signature is equivalent to descent of the actual maximal source flow: equivalent initial source laws have identical signature trajectories and the same maximal interior time interval.

**Proof.** The source field in (13) is $`C^1`$, so ordinary differential-equation uniqueness applies. Given equivalent positive joint laws $`\mu,\nu`$, there are constants $`\lambda_j>0`$ with

```math
\nu=T_\lambda\mu,\qquad (T_\lambda z)_{ji}=\lambda_jz_{ji}.
```

Consider the affine slice

```math
K_\lambda=\left\{z>0:\sum_{j,i}z_{ji}=1,\
\sum_j(\lambda_j-1)z_{ji}=0\text{ for each }i\right\}.
```

For every $`z`$ on this slice, $`T_\lambda z`$ is a positive normalized law with the same signature. If $`\lambda_j\ne1`$, the corresponding weight differs, so (16) gives $`a_j(F(z))=0`$.

Writing $`V`$ for the source field, (13) now gives

```math
\sum_j(\lambda_j-1)V_{ji}(z)=0,\qquad
V(T_\lambda z)=T_\lambda V(z).                               \quad\text{(17)}\quad
```

The first equality follows because both its $`z`$-term and its $`a_j`$-term vanish. Thus the field is tangent to the affine slice. Restriction to that embedded submanifold and source uniqueness make the slice invariant for the entire maximal trajectory; it is relatively closed and has no additional boundary within the positive source domain.

The second equality intertwines trajectories. Moreover $`T_\lambda`$ maps $`K_\lambda`$ bijectively onto $`K_{\lambda^{-1}}`$. If one source trajectory extended beyond the other's maximal interval, this map or its inverse would transfer the extension, preserving positivity and normalization, contradicting maximality. Thus intervals and signatures agree. Conversely, equal projected trajectories near time zero have equal initial derivatives, and Theorem 4 yields (16). $`\square`$

This proves actual source-flow descent. It does not generally prove continuity of the projected velocity in the ordinary subspace topology of $`S`$, or that $`S`$ carries a reduced Riemannian metric. With the abstract quotient topology, the descended maximal flow is continuous: the source flow factors through the quotient on its open saturated domain, and product with the locally compact Hausdorff time line preserves quotient maps. The stronger ordinary-signature regularity below is proved separately. [4]

## 7. A sharp threshold for globally descending objectives

### 7.1 Rigidity when the audit has more outcomes than the target

**Lemma 6 — Dense fully variable signatures.** If $`k>r`$, matrices $`Q`$ for which every $`r`$-column minor is nonzero are dense in $`(\Delta_r^\circ)^k`$. At each such matrix all audit weights are variable.

**Proof.** Choose distinct $`t_j\in(0,1)`$ and $`0<\delta<1/[r(r-1)]`$. Let

```math
p_i(t)=1/r+\delta t^i\ (i\lt{}r),\qquad
p_r(t)=1/r-\delta\sum_{i=1}^{r-1}t^i.
```

These columns are positive. They are an invertible linear transform of the vectors $`(1,t,\ldots,t^{r-1})^\mathsf T`$, so Vandermonde nonsingularity makes every $`r`$-column minor of the resulting $`Q_*`$ nonzero.

For any positive $`Q`$, set $`Q_\epsilon=(1-\epsilon)Q+\epsilon Q_*`$. Each minor is a polynomial nonzero at $`\epsilon=1`$, and has only finitely many zeros. Arbitrarily small positive $`\epsilon`$ avoid the finitely many forbidden values. To get density in the actual signature image, choose a positive representative $`w`$ and set $`q_\epsilon=Q_\epsilon w`$; do not perturb $`Q`$ while arbitrarily fixing $`q`$.

Deleting any column leaves at least $`r`$ columns, of rank $`r`$, so (15) makes every index variable. $`\square`$

**Theorem 7 — Global classification for $`k>r`$.** For ambient $`C^1`$ $`J`$, the following are equivalent:

1. The projected negative source Fisher velocity is representative-independent everywhere on $`S`$.
2. $`C(p_j)J_j=0`$ for every conditional slot at every point of $`S`$.
3. There is a $`C^1`$ function $`\phi:\Delta_r^\circ\to\mathbb R`$ with $`J(P,q)=\phi(q)`$ on $`S`$.

If $`J`$ is $`C^2`$, then $`\phi`$ is $`C^2`$, and these conditions are also equivalent to the maximal-flow descent in Theorem 5.

**Proof.** Theorem 4 forces all $`a_j`$ to vanish on the dense signatures of Lemma 6; continuity extends the vanishings to all of $`S`$. Define $`\phi(q)=J(q,\ldots,q,q)`$. At any $`(P,q)\in S`$, choose a positive representative $`w`$ and contract

```math
p_j(s)=(1-s)p_j+sq,\qquad 0\leq s\leq1.
```

This remains positive and has $`\sum_jw_jp_j(s)=q`$. Each $`J_j`$ is constant across target coordinates and therefore annihilates the tangent $`q-p_j`$. The chain rule shows that $`J`$ stays constant along the contraction, proving $`J(P,q)=\phi(q)`$. This also proves the fixed-$`q`$ slice is star-shaped.

Conversely, equality on $`S`$ makes the source pullback precisely $`\phi(Qw)`$. Its projected equations are the weight-independent equations in §7.2, regardless of the off-image extension. Theorem 5 supplies the $`C^2`$ flow statement. $`\square`$

The conclusion is about the restricted objective on the admitted image. A smooth term supported outside that image is invisible to the source pullback.

### 7.2 Positive target tilts and maximal intervals

For $`E=\phi(q)`$, equations (12)–(13) reduce to

```math
\dot w_j=-w_j\langle h(q),p_j-q\rangle,\qquad
\dot p_j=-C(p_j)h(q),\qquad \dot q=-C(q)h(q).                  \quad\text{(18)}\quad
```

Unlike a merely set-theoretic projected field, the $`(P,q)`$ equations are $`C^1`$ on all of $`A`$ when $`\phi`$ is $`C^2`$.

For a positive target weight vector $`\ell`$, define

```math
Z_p(\ell)=\sum_i\ell_ip_i,\qquad
L_\ell(p)=\frac{\mathrm{diag}(\ell)p}{Z_p(\ell)}.
```

Tilting the joint law by its target coordinate gives

```math
\mu'_{ji}=\frac{\ell_i\mu_{ji}}{Z_q(\ell)},\quad
p'_j=L_\ell(p_j),\quad q'=L_\ell(q),\quad
w'_j=\frac{w_jZ_{p_j}(\ell)}{Z_q(\ell)}.                      \quad\text{(19)}\quad
```

Thus the signature update needs only $`P,q`$. Composition multiplies tilt vectors coordinatewise; reciprocal tilts invert the operation, and a common positive scalar is irrelevant. Rank and the set of variable indices are unchanged because $`Q'`$ is obtained by invertible diagonal row and column scalings.

Along a target solution let

```math
\ell_i(t)=\exp\!\left(-\int_0^t h_i(q(s))\,ds\right).
```

Differentiating (19) gives (18). On every compact subinterval of the target's maximal interior interval, the tilt remains finite and positive. Formula (19) therefore lifts that whole interval to a source solution. Conversely, any source extension gives a target extension. Source, target, and signature trajectories have the same maximal interior interval, and the signature flow is continuous in its ordinary subspace topology.

This does not imply completeness for arbitrary $`C^2`$ $`\phi`$. If the coordinate differences of $`h`$ are bounded, a scalar gauge makes the tilt finite and positive on every finite interval, giving completeness. But $`\phi(q)=\log q_1`$ yields

```math
\dot q_1=-(1-q_1),\qquad
q_1(t)=1-(1-q_1(0))e^t,
```

which reaches zero at the finite time $`\log(1/(1-q_1(0)))`$. No positive-domain extension is asserted.

### 7.3 Sharpness for every $`2\leq k\leq r`$

Set

```math
J(P,q)=H(P)=\det(Q^\mathsf TQ).
```

By Cauchy–Binet,

```math
H(P)=\sum_{\substack{I\subseteq\{1,\ldots,r\}\\ |I|=k}}
\det(Q_I)^2.
```

When $`\mathrm{rank}\,Q<k`$, every determinant in the sum vanishes, and therefore the whole first differential of $`H`$ vanishes. These are exactly the matrices with nonsingleton weight fibres. They give stationary source states. At full column rank every weight fibre is a singleton. Theorem 4 therefore gives global velocity descent, and Theorem 5 gives maximal-flow descent.

The source flow is complete. Since $`J_q=0`$, the weights are constant. Polynomial derivatives of $`H`$ are bounded on the product of closed simplexes. For each fixed positive $`w`$, equation (12) consequently bounds every $`d\log p_{ji}/dt`$ on finite time intervals. No conditional probability reaches zero in finite positive or negative time; compactness and ordinary continuation extend the flow for all real times.

Nevertheless $`H`$ is not a function of $`q`$. Choose $`k`$ affinely independent target-tangent vectors $`v_j`$ with $`\sum_jv_j=0`$, possible because $`k-1\leq r-1`$. For small $`\epsilon>0`$, set $`p_j=q+\epsilon v_j`$, $`w_j=1/k`$. Their average stays $`q`$, and their columns are linearly independent: summing a putative column relation gives zero sum of coefficients, after which affine independence forces every coefficient to vanish. Hence $`H>0`$. At $`p_j=q`$ for all $`j`$, with the same target marginal, $`H=0`$.

For $`r=k=2`$, if $`p_1=(a,1-a)`$, $`p_2=(b,1-b)`$, then $`H=(a-b)^2`$. For $`k>r`$, the Gram determinant is identically zero, so it cannot contradict Theorem 7. The strict threshold is sharp. No simpler global classification for all $`k\leq r`$ is asserted beyond Theorems 4–5. [4]

### 7.4 Descent need not give a continuous signature velocity

The binary example also separates two regularity claims. Take

```math
a=\frac12+\epsilon,\quad b=\frac12,\quad w_1=\epsilon^2,
\qquad 0<\epsilon<\frac12.
```

For $`H=(a-b)^2`$, equation (12) gives

```math
\dot a=-\frac{2a(1-a)(a-b)}{w_1}
=-\frac{2(1/4-\epsilon^2)}{\epsilon}.
```

The signatures tend to $`p_1=p_2=q=(1/2,1/2)`$, whose source fibres are stationary, but the displayed velocity is unbounded. Every member of the sequence has strictly positive joint cells. Thus a representative-independent, complete source flow can coexist with a discontinuous projected velocity in the ordinary signature topology.

This explicit specialization follows from the preceding source equations and is included to make their regularity limitation concrete. It is not an assertion that the source vector field is discontinuous, or a field-wide novelty claim.

## 8. Preserving one objective versus preserving an entire metric

The pointwise Fisher criterion differs from the expected-value row-space criterion. For the interior three-outcome example, use columns

```math
p_1=(1/4,3/4),\quad p_2=(1/2,1/2),\quad p_3=(3/4,1/4),
```

and weights $`w=(1/4,1/2,1/4)`$, $`w'=(1/8,3/4,1/8)`$. Both give $`q=(1/2,1/2)`$. With $`J=p_{1,1}`$,

```math
a_1=(3/16,-3/16),\qquad h=0,\qquad a_2=a_3=0.
```

The first conditional velocity is $`(-3/4,3/4)`$ at $`w`$ and $`(-3/2,3/2)`$ at $`w'`$, while both target velocities equal $`(-3/16,3/16)`$. Equal target speed does not preserve the retained conditional answers' speed.

For a general linear readout there is a useful separate criterion. Let $`U_0\subseteq\mathbb R^n`$ be open, $`L:\mathbb R^n\to\mathbb R^m`$ have full row rank, and $`G(x)`$ be a smooth positive-definite metric. For every smooth objective $`j(Lx)`$, the projected negative gradient is

```math
-LG(x)^{-1}L^\mathsf T\nabla j(Lx).                           \quad\text{(20)}\quad
```

It depends only on $`Lx`$, for every such objective, if and only if the cometric

```math
A(x)=LG(x)^{-1}L^\mathsf T
```

is constant on each readout fibre.

For sufficiency, fibre constancy gives a smooth $`\bar A(z)`$, locally through linear sections, and (20) is the gradient for coarse metric $`\bar A(z)^{-1}`$. Positivity follows from

```math
v^\mathsf TA(x)v=(L^\mathsf Tv)^\mathsf TG(x)^{-1}(L^\mathsf Tv)>0.
```

For necessity, apply (20) to every coordinate objective $`j(z)=z_i`$; its projected field reads the $`i`$-th column of $`A`$. Every column must be fibre-constant. [6]

The necessity quantifies over all objectives. One objective can be insensitive to a varying cometric direction. This infinitesimal theorem also does not identify source and quotient maximal lifetimes: boundary behaviour requires additional proof, supplied for the special Fisher model by Theorem 5. For example, retaining only a visible coordinate while discarding a two-valued metric label can turn the same objective's velocity from $`1`$ to $`2`$, changing arrival time at a visible threshold from $`1`$ to $`1/2`$. Rescaling time changes the clock contract.

## 9. How much supplementary information is necessary?

### 9.1 The exact finite-state answer

Let $`E`$ be a nonempty finite set of declared information states. Each state has a visible record $`r(s)`$, a required label, enabled actions, costs, and a joint outcome/next-state kernel $`K_a(s,o,t)`$. A partition preserves the contract if equal-block states have equal records, labels, permissions, costs, and, for every block $`D`$,

```math
\sum_{t\in D}K_a(s,o,t)=\sum_{t\in D}K_a(s',o,t).              \quad\text{(21)}\quad
```

This is a joint-kernel requirement, stronger than unrestricted equality of selected traces.

Start with the partition $`P_0`$ determined by the record, labels, actions, and costs. Repeatedly split blocks according to the outcome-indexed transition masses into the current blocks.

**Theorem 8 — Coarsest finite refinement and minimum supplement.** The iteration terminates after at most $`|E|-|P_0|`$ strict refinements and produces the coarsest contract-preserving partition $`P_*`$. If $`N_z`$ is the number of $`P_*`$-blocks inside $`r^{-1}(z)`$, the minimum common alphabet of a deterministic supplementary label, retained alongside $`r`$, has size

```math
M_*=\max_zN_z,\qquad b_*=\lceil\log_2M_*\rceil
```

fixed-length bits.

**Proof.** Each strict split increases the number of blocks. At stabilization, (21) and the initial requirements hold. Any other preserving partition refines $`P_0`$. If it refines $`P_i`$, each $`P_i`$-block is a union of its blocks, so equality of transition masses into those smaller blocks implies equality into every $`P_i`$-block. It therefore refines $`P_{i+1}`$. Induction proves coarseness.

Within an $`r`$-fibre, the supplementary label must distinguish its $`N_z`$ final blocks. Conversely, enumerate those blocks separately in each fibre, reusing labels in different fibres because $`r`$ is retained. An alphabet of size $`M_*`$ suffices. $`\square`$

Adding actions or required observables can only refine $`P_*`$ and cannot reduce this minimum. The result does not preserve every narrative detail: four states differing in two independently relevant support/cost distinctions need two bits only when both distinctions belong to the contract. It is a finite alphabet result, not a bound for a continuum of hidden weights. [6]

### 9.2 Supplementing selected expected values

Fix the positive fibre (9), and let a finite matrix $`H`$ list required expectation rows. Set $`N=\ker Q`$ and

```math
s=\mathrm{rank}(H|_N)
=\mathrm{rank}\,\begin{bmatrix}Q\\H\end{bmatrix}
-\mathrm{rank}\,Q.                                      \quad\text{(22)}\quad
```

**Corollary 9 — Exact continuous utility supplement.** On this fixed fibre, $`s`$ continuous real coordinates are necessary and sufficient to recover $`Hw`$, allowing arbitrary decoders. A finite-valued exact supplement exists if and only if $`s=0`$.

**Proof.** Choose a basis of the independent restrictions of the rows of $`H`$ to $`N`$. Retaining those linear values determines all other required values up to constants fixed by $`Qw=q`$, giving sufficiency. For necessity choose an $`s`$-dimensional subspace $`L\subseteq N`$ on which $`H`$ is injective. A sufficiently small open ball in $`w^0+L`$ lies in the positive fibre. An exact supplement must be injective on this ball, since equal encoded values imply equal $`Hw`$. Invariance of domain excludes a continuous injection into fewer than $`s`$ coordinates. If $`s>0`$, $`Hw`$ takes infinitely many values along a positive line segment, excluding a finite alphabet even without encoder continuity. If $`s=0`$, no supplement is needed. $`\square`$

Equation (22) follows because adjoining the rows of $`H`$ to $`Q`$ adds exactly their independent restrictions to $`\ker Q`$. This corollary combines the existing expectation-fibre and continuous-dimension arguments; its explicit combined formulation and proof are part of this exposition's independent review, not retroactively attributed to an earlier review. It concerns one fixed audit and a finite set of expected quantities. Future interventions require closure of the enlarged observable contract, not merely this one-step supplement.

### 9.3 The full-source metric requires all hidden weights

For a conditional coordinate $`p_{ji}`$, (11) gives its ambient Fisher squared gradient norm:

```math
\|\mathrm{grad}_g\,p_{ji}\|^2
=\frac{p_{ji}(1-p_{ji})}{w_j}.                               \quad\text{(23)}\quad
```

The numerator is known and strictly positive. Retaining these norms for a fixed target coordinate $`i`$ and $`j=1,\ldots,k-1`$ recovers those weights; normalization recovers the last. Thus any record preserving the signature and this norm family is injective on the whole source domain. No regularity assumption on that record is needed for this reconstruction.

On a fixed $`P,q`$ fibre,

```math
d=k-\mathrm{rank}\,Q
```

is its affine dimension. If $`d>0`$, no finite-valued supplement preserves (23) exactly. Among continuous real-coordinate supplements, precisely $`d`$ are necessary and sufficient: injectivity and invariance of domain give the lower bound, and coordinates in a basis of $`\ker Q`$ attain it. At $`d=0`$, no supplement is needed. [4], [5]

These are norms of ambient source gradients. They are not gradients computed after fixing $`P`$ inside the fibre, where the conditional coordinates themselves are constant. The lower bound is for a fixed fibre, not a globally continuous minimal chart across rank-changing strata. Arbitrary discontinuous one-real encodings are outside the continuous-coordinate assertion. A discretization changes the exact problem.

The hierarchy is now explicit. Posterior answers need no supplement beyond $`F`$. Selected expectations need $`s\leq d`$ continuous coordinates. The full norm contract needs $`d`$. A chosen reduced metric can avoid that last requirement only by changing the metric contract, not by claiming to preserve the original one.

### 9.4 Selecting a valid certificate rather than recovering a state

The finite partition in §9.1 preserves an entire future-operation contract. A different task may require only one output that is valid in the actual state. Several outputs can be valid at one state, and one output can be valid at several states. The minimum information for this relation-selection task need not recover the state, a preassigned output label, or the full predictive partition.

Let $`S`$ be a nonempty finite state set, $`\omega:S\to O`$ the decoder's observation, $`K`$ a finite set of complete certificate objects, and $`\mathcal A(s)\subseteq K`$ the objects admitted at $`s`$. A certificate can include an action together with its source, version, authority, provenance, invalidator, target and temporal-model conditions. “Complete” refers to the declared output contract. The mathematical input $`\mathcal A`$ does not itself authenticate those conditions. [13]

For a nonempty observation cell $`C=\omega^{-1}(o)`$, put

```math
S_C(k)=\{s\in C:k\in\mathcal A(s)\},\qquad
\rho(C)=\min\left\{|L|:L\subseteq K,\ C\subseteq\bigcup_{k\in L}S_C(k)\right\},
```

with $`\rho(C)=\infty`$ if no cover exists.

**Theorem 10 — Exact information for finite relation selection.**

1. If the encoder knows the exact state, a feasible deterministic protocol on $`C`$ exists exactly when $`\rho(C)<\infty`$; its minimum message alphabet then has size $`\rho(C)`$. Over all observed cells, feasibility means $`R<\infty`$, and the minimum common size is

   $`R=\max_{o\in\omega(S)}\rho(\omega^{-1}(o)).`$

2. If the encoder knows only $`\eta(s)`$, for a supplied map $`\eta:S\to E`$, a message map $`c:\eta(S)\to M`$ is feasible exactly when every nonempty bucket

   $`B(o,m)=\{s:\omega(s)=o,\ c(\eta(s))=m\}`$

   satisfies

   $`\bigcap_{s\in B(o,m)}\mathcal A(s)\ne\varnothing.`$

   The minimum alphabet is the minimum number of used messages over such maps; no compatible map means impossibility.

**Proof.** A decoder returns one object for each observation/message pair. In a fixed cell, the objects returned by its used messages must cover every state, giving $`\rho(C)\leq|M|`$. Conversely, choose a minimum cover, assign each state to a covering object, and send its index. Because the decoder sees $`o`$, message names can be reused between cells, proving the maximum formula. With restricted encoder information, all states in a bucket necessarily receive the same decoded object, which must lie in their common intersection. Conversely, choose an object in each nonempty intersection and define the decoder accordingly. All choices are finite. $`\square`$

The exact-state cover number is not a solution when the sender cannot distinguish the relevant states. If $`\omega(s_0)=\omega(s_1)`$, $`\eta(s_0)=\eta(s_1)`$ and the two admissible sets are disjoint, no number of messages repairs that encoder-information deficit.

Several strict boundaries follow.

- With admissible sets $`\{a,b\},\{b,c\},\{a,c\}`$ in one cell, every pair has a common output but all three do not. Two objects cover the cell, while one message is impossible. Thus pairwise compatibility alone is insufficient for a general relation.
- An empty admissible set at even one possible state makes the fixed task impossible. Information cannot create a missing valid certificate.
- If $`\mathrm{act}:K\to U`$ retains only a surface action, then the action-cover number is at most $`\rho(C)`$: projecting any certificate cover gives an action cover. The inequality is strict for $`\mathcal A(s_0)=\{k_0\}`$ and $`\mathcal A(s_1)=\{k_1\}`$ with distinct certificates but $`\mathrm{act}(k_0)=\mathrm{act}(k_1)`$. Agreement on an action need not preserve its source, version or authority. If two same-byte version contexts require respectively an old-version execution certificate and a new-version hold/revalidation certificate, with no common admitted fallback, their cover number is two. One truthful distinguishing bit is then necessary and sufficient only when the encoder actually knows the relevant version.
- For a nonempty finite set of possible model completions $`\Theta(s)`$, robust admissibility is

  $`\mathcal A_{\rm all}(s)=\bigcap_{\theta\in\Theta(s)}\mathcal A_\theta(s).`$

  A union is unsound: completions admitting only $`k_0`$ and only $`k_1`$ admit no common robust output. On fixed state and certificate sets, shrinking admissible sets can only increase the cover requirement, possibly to infinity.

When $`R<\infty`$, the minimum fixed-length binary communication is $`\lceil\log_2R\rceil`$ bits. This is also the minimum worst-case length of a binary prefix-free code: at most $`2^L`$ codewords can have maximum length $`L`$, and fixed-length words attain the bound. For one message the empty word is allowed. Expected length requires a distribution; framed variable-length, interactive, private and bounded-error tasks have different contracts.

Input-independent randomization does not improve the pointwise zero-error alphabet in this finite model. Represent all encoder/decoder randomness by a common seed space independent of $`s`$. For each state, successful seeds have probability one. Their finite intersection has probability one; fixing any seed in it gives a deterministic protocol with the same alphabet. This argument concerns exact correctness at every state, not average or bounded-error success.

The cover formula does not promise efficient optimization. For an explicitly listed admissibility matrix and an input integer $`k`$, deciding $`\rho(C)\leq k`$ is NP-complete: selected objects form a polynomially verifiable certificate, and any Set Cover instance is represented by taking its universe as $`C`$ and its listed subsets as the supports $`S_C(k)`$. This is the standard Set Cover result, not new complexity theory. Classical side-information coding and function computation supply antecedents, but their reconstruction and asymptotic error models must not be substituted for the present one-shot relation contract. [17]–[19]

#### Adversarial transmission and the cost of an unnecessary label

Fix an encoder $`v:S\to\Gamma^n`$ over a finite alphabet, and allow at most $`r`$ Hamming substitutions. If the sender is information-restricted, $`v`$ must respect that restriction. For received word $`y`$, define

```math
B(o,y)=\{s:\omega(s)=o,\ d_H(v(s),y)\leq r\}.
```

**Proposition 11 — Robust relation decoding.** A deterministic decoder returning an admitted certificate for every permitted state/error pair exists exactly when every nonempty $`B(o,y)`$ has a nonempty common admissible set.

**Proof.** One output at $`(o,y)`$ must be admitted at every state that can produce that received pair. Conversely, select one member of each nonempty intersection. $`\square`$

For exact recovery of a prescribed label $`\ell(s)`$, codewords of differently labelled states **within the same observation cell** must have distance greater than $`2r`$. Otherwise their error balls intersect: divide the differing coordinates between two words to construct a received word within radius $`r`$ of both. Conversely, that distance condition makes conflicting-label balls disjoint within each cell. Different observations already distinguish states and impose no such cross-cell distance requirement.

This stronger label task can cost more. Take four states $`s_0,\ldots,s_3`$ with one observation, four objects $`k_0,\ldots,k_3`$, and

```math
\mathcal A(s_i)=K\setminus\{k_i\}.
```

Encode the states by $`00,01,10,11`$ and allow one bit flip. Every received word's ambiguity ball contains three states. The common admitted object is precisely the object indexed by the excluded fourth state. The decoder therefore succeeds with two bits although it cannot identify the actual state. One bit cannot suffice: under one flip its ambiguity set contains all four states, whose admissible sets have empty intersection.

Any nonconstant binary label needs at least three bits because its two classes require distance at least three; $`000`$ and $`111`$ attain that bound. Four distinct labels need at least five bits. Their disjoint radius-one balls have size $`n+1`$, so $`4(n+1)\leq2^n`$; this excludes every $`n\leq4`$. The length-five code

```math
\{00000,\ 00111,\ 11001,\ 11110\}
```

has all pairwise distances at least three and attains the bound. The distinction is thus two bits for a valid relational output, three for a nonconstant binary label, and five for complete four-state recovery. [13]

#### Temporal guarantees require a transition model

A certificate valid now need not support a policy that remains valid. To state that further burden, let $`S`$ be a finite common-state game: the controller knows the current state when choosing its action. Each state has a finite nonempty eligible action menu $`\Pi(s)`$; each action has a finite nonempty set $`\mathrm{Succ}(s,a)`$ of adversarial successors. The controller chooses the action and the adversary chooses its successor. Assume $`\mathrm{Target}\subseteq\mathrm{Safe}\subseteq S`$, and write $`\mathrm{Bad}=\mathrm{Safe}\setminus\mathrm{Target}`$. The common state and action eligibility are supplied model assumptions, not consequences of a transmitted certificate.

Define

```math
\mathrm{Pre}(X)=\{s\in\mathrm{Safe}:
 \exists a\in\Pi(s),\ \mathrm{Succ}(s,a)\subseteq X\}.
```

All fixed points below range over subsets of $`\mathrm{Safe}`$. Here $`\mu`$ denotes the least fixed point and $`\nu`$ the greatest; finite monotone iteration computes both. Set

```math
K_0=\nu X\,(\mathrm{Target}\cap\mathrm{Pre}(X)),\qquad
W_{\rm core}=\mu Y\,(K_0\cup\mathrm{Pre}(Y)).
```

The set $`K_0`$ is the largest target region in which the controller can keep every successor inside that region. For eventual target persistence, define instead

```math
F_Z(X)=(\mathrm{Target}\cap\mathrm{Pre}(X))
 \cup(\mathrm{Bad}\cap\mathrm{Pre}(Z)),\qquad
H(Z)=\nu X\,F_Z(X),\qquad W_{\rm pers}=\mu Z\,H(Z).
```

**Theorem 12 — Two finite temporal objectives.** The region $`W_{\rm core}`$ consists exactly of states from which the controller can force finite entry into $`K_0`$ and remain there safely. The region $`W_{\rm pers}`$ consists exactly of states from which it can stay safe and visit $`\mathrm{Bad}`$ only finitely often, the co-Büchi objective. Memoryless strategies suffice for both.

**Proof.** For core entry, start the attractor iteration at $`Y_0=K_0`$. At a state first admitted to $`Y_i`$, choose an action whose every successor lies in $`Y_{i-1}`$; inside $`K_0`$, choose a preserving action. The least layer strictly decreases until the kernel is reached. Conversely, outside the final attractor every action has a successor outside it. The adversary can keep the play away from $`K_0`$ or make it unsafe, against any controller strategy.

For persistence put $`Z_0=\varnothing`$ and $`Z_{i+1}=H(Z_i)`$. Monotonicity and finiteness give stabilization at $`W_{\rm pers}`$. If $`j(s)`$ is a state's first positive admission index, choose at target states an action with successors in $`Z_{j(s)}`$, and at bad states an action with successors in $`Z_{j(s)-1}`$. The inner fixed-point equation supplies these actions. Thus $`j`$ never increases and strictly decreases after every bad-state occurrence. All successors stay safe, so only finitely many bad visits occur.

For completeness, put $`W=W_{\rm pers}=H(W)`$ and compute the inner greatest fixed point by $`X_0=\mathrm{Safe}`$, $`X_{i+1}=F_W(X_i)`$. Every safe state outside $`W`$ has a finite first removal index $`d(s)\geq1`$. At a target state removed at step $`d`$, every controller action has a successor outside $`X_{d-1}`$: the adversary can leave safety or choose another state outside $`W`$ with strictly smaller removal index. At a bad state outside $`W`$, membership in $`\mathrm{Pre}(W)`$ fails, so every action has a successor outside $`W`$. The adversary can therefore remain outside $`W`$ unless safety already fails. An infinite safe play cannot eventually contain only target states, because its positive removal index would then strictly decrease forever. It must visit bad states infinitely often. This defeats even history-dependent controller strategies outside $`W`$, while the earlier construction supplies memoryless winning strategies inside it. $`\square`$ [14], [20]

The source also gives an independent induced-graph check for a fixed memoryless strategy. Such a strategy is winning from a start exactly when no unsafe state and no bad-containing directed cycle is reachable: repeating such a cycle defeats persistence, while infinitely many bad visits in a finite graph force a bad vertex to recur. Thus a winning path cannot repeat a bad vertex. Let $`R_k`$ contain states from which every induced path stays safe and has at most $`k`$ future bad occurrences, counting the current state, and set $`R_{-1}=\varnothing`$. Target states in $`R_k`$ have all selected successors in $`R_k`$; bad states have them in $`R_{k-1}`$. Consequently $`R_k\subseteq F_{R_{k-1}}(R_k)`$, hence $`R_k\subseteq H(R_{k-1})`$. Induction gives $`R_k\subseteq Z_{k+1}`$. Every winning start for that strategy belongs to some $`R_k`$, recovering the fixed-policy converse by a different route. [14]

Core entry is sufficient for persistence but not necessary. With all states safe, target $`\{0,2\}`$, and sole successor sets

```math
0\mapsto\{0\},\qquad1\mapsto\{0\},\qquad2\mapsto\{0,1,2\},
```

we have $`K_0=\{0\}`$, $`W_{\rm core}=\{0,1\}`$ and $`W_{\rm pers}=\{0,1,2\}`$. From $`2`$, a play may stay at target state $`2`$ forever or make a final visit to bad state $`1`$ before remaining at $`0`$. No play has infinitely many bad visits, but no strategy forces departure from $`2`$ into the common kernel. Equating the two objectives would discard a genuine winning case.

A simpler certificate need not compute the whole winning region. Supply $`W\subseteq\mathrm{Safe}`$ and $`r:W\to\mathbb N`$. Admit a certificate at $`s`$ only if its selected action has nonempty successors in $`W`$, every successor has rank at most $`r(s)`$ at a target state and strictly less at a non-target state, and its model/version and non-temporal guards hold. Choosing such an object at every visited state keeps the play in $`W`$ and permits at most $`r(s_0)`$ non-target visits. This follows by induction and strict descent in $`\mathbb N`$. A common admitted certificate for each actual information bucket is sufficient for the same argument. It is not a characterization of all partial-observation co-Büchi strategies.

Nor does one successful present selection establish future information sufficiency. Let an initial state have one valid waiting certificate whose hidden successors are $`x`$ and $`y`$. They have the same next observation. At $`x`$, only one action reaches a target $`g`$, while the other loops at $`x`$; at $`y`$, the roles reverse. Let $`g`$ be the only target, give ranks $`2,1,1,0`$ to the initial state, $`x,y,g`$, respectively, and let $`g`$ remain at itself. The present cell needs one certificate, but the merged future cell needs two. A message sent before the adversary chooses this fresh hidden branch cannot reveal its outcome. Observable history can reduce later ambiguity only when it actually distinguishes the relevant states. [13]

#### Local closure, model identity, and universal progress

An event-local closure record that does not specify future transitions cannot determine either temporal objective. The same current record can have a one-state target self-loop extension, or an extension that moves from that target to an absorbing safe non-target state. The first is winning for both objectives and the second for neither. A historical analysis of a corrective-transition validator supplies a concrete instance of this nonidentifiability at its recorded implementation edition; it is not a fresh audit of today's runtime. [15]

A checkable temporal certificate must therefore identify its model, not merely quote the current local record. The repaired source contract canonically binds the state, safe and target sets, action/successor relation, source/version epoch, eligibility references and epochs, and the declared model-completeness scope. Certificate kind and claimed answer are kept outside that model identity, so two objectives over the same model do not become two different models merely by declaration.

Given those exact inputs, a full-region certificate can be checked by recomputing $`K_0,W_{\rm core}`$ or $`W_{\rm pers}`$ and the corresponding least-layer ranks. Check that every selected action is eligible; kernel actions keep every successor in the kernel; non-kernel core actions strictly reduce attractor rank; and persistence actions weakly reduce rank at targets and strictly reduce it at bad states. The selected finite graph must also have no reachable bad-containing cycle for persistence. These are model-relative checks. A digest does not prove that the real successor relation is complete, that an eligibility reference is true, or that the represented target is substantively adequate.

Universal progress is essential. From a non-target state, an action with successors $`\{g,s\}`$ can reach a target $`g`$ but lets the adversary remain at $`s`$ forever. It is not a core-entry witness. The valid alternative $`\{g\}`$ strictly reduces rank on every successor. Wrong regions, stale eligibility epochs, absent completeness declarations, nonexistent selected actions, false ranks, changed model digests and nonforcing strategies are distinct rejection reasons; a recomputed digest cannot repair the others. [15]

#### Versioned evidence and compositional eligibility

The admissibility relation itself can depend on a reason-certificate path. At each boundary retain the version, frozen claim, provenance root, finite reason-node and directed dependency-edge sets, and the obligations actually discharged. A proposed edge must match that complete input boundary. Its node map must have exactly the input node set as domain and send every input dependency edge to an output dependency edge. The output node set is exactly the map's image, and every output dependency-edge endpoint must belong to that set.

Let $`D_i`$ be the actual input discharged set, $`P_i`$ the obligations to be preserved, $`R_i`$ those independently revalidated for the next context, and $`T_{i+1}`$ its complete required set. Require

```math
P_i\subseteq D_i,\qquad T_{i+1}\subseteq P_i\cup R_i,\qquad
D_{i+1}=P_i\cup R_i.
```

Also require preservation of the frozen claim's meaning under the declared semantic maps, actual provenance-root custody, valid authority and any necessary intermediate redelegation, and no open registered invalidator. These premises concern actual discharged or revalidated obligations; merely setting a Boolean or copying an obligation's name does not prove them.

**Proposition 13 — Finite certificate-path composition.** For a nonempty finite path, under these boundary, dependency, obligation, semantic, authority and invalidator conditions at every edge, the final certificate discharges its complete declared target contract. For a zero-edge path, the same conclusion requires the separate initial condition $`T_0\subseteq D_0`$.

**Proof.** For a zero-edge path the conclusion is exactly the stated initial condition. For a nonempty path, induct along its edges. Exact input equality makes each edge act on the preceding output rather than a compatible-looking substitute. The node map preserves its actual dependency edges. Since $`P_i\subseteq D_i`$, preservation introduces no unsupported obligation; independently validated $`R_i`$ supplies the permitted additions, and their union covers $`T_{i+1}`$. The output is then the exact next input. Composing the maps preserves the declared meaning and dependency relations, while the stated root, delegation and invalidator premises maintain their respective conditions. The final required set is therefore discharged. $`\square`$ [16]

This structural argument does not prove that the original reasons are sound, independently validate an authority assertion, or infer acyclicity from an arbitrary graph map. Any required logical validity or acyclicity is a separate input/output condition. A new independent source root likewise requires its own evidence; forwarding or reformatting a certificate does not create one.

The decisive failure modes are concrete. An obligation absent from $`D_i`$ cannot become discharged by being called preserved. Equal version/claim labels do not permit a second edge to substitute an alien reason node or dependency graph. Pairwise compatibility is not a composable path; a revoked source cannot be made current by dropping its invalidator; permission to receive a delegation need not include permission to redelegate it; and a changed claim meaning breaks semantic transport. [16]

Finally, on fixed states, predicates, observations and successor relations, restricting eligible actions makes $`\mathrm{Pre}`$ pointwise smaller. Monotonicity of the least, greatest and nested fixed points gives

```math
K_0'\subseteq K_0,\qquad W_{\rm core}'\subseteq W_{\rm core},
\qquad W_{\rm pers}'\subseteq W_{\rm pers}.
```

For a sharp example, let $`g`$ be a target with a self-loop and let $`s`$ have repair $`\{g\}`$ and linger $`\{s\}`$. Both states are initially winning. If the repair's version guard fails while its bytes remain unchanged, only linger remains at $`s`$; the winning regions shrink to $`\{g\}`$. Same bytes therefore do not entail same applicability or temporal eligibility. Source/version changes can require new admissibility data, a new model binding and recomputation. If the version also changes states, targets, observations or successors, the fixed-model monotonicity assertion alone gives no comparison.

Two related comparisons preserve the same exact temporal scope. With menus and state predicates fixed, enlarging adversarial successor sets makes $`\mathrm{Pre}`$ smaller and can only shrink all three winning sets: every newly controllable predecessor would already have been controllable before enlargement, and monotone fixed-point iteration preserves inclusion. At a single state, an eligible action whose successor set contains another eligible action's successor set is dominated for these universal objectives. Whenever the larger set lies in $`X`$, so does the smaller one; deleting the larger-set action therefore leaves $`\mathrm{Pre}(X)`$ unchanged for every $`X`$, and hence leaves the kernel and both winning regions unchanged. Additional action-specific costs or output obligations are separate contracts and can defeat that dominance comparison. [14]

These arguments explain how information, evidence and temporal obligations fit together without identifying them. Finite selection assumes an admissibility relation; temporal certification assumes an adequate transition model; evidence transport assumes its semantic and authority premises. None supplies the others by relabelling a successful output.


#### Retained history and the status of a disposition

Certificate-path eligibility and historical traceability answer different questions. Proposition 13 concerns what a final certificate actually discharges under its semantic and authority premises. A reduction can also be required to preserve what earlier obligations were, how their statuses changed and which issues remain live elsewhere. The formalisation source gives a finite preservation argument for that additional contract. [FORM, §6][FORM]

Write a modelled state as $`z=(x,B,\mathscr H)`$, where $`x`$ is the active representation, $`B`$ the current obligation records and $`\mathscr H`$ the retained history. A transition has a witness binding the actual input and output, their analysis and representation versions, and the operation's parameters and affected obligations. Call the witness **record-valid** when it retains every old obligation's identity and previous status in the new history, and each old live obligation either persists, has explicitly linked successor obligations, or receives an explicit authorised disposition. A replacement must leave a successor to trace, unless a separate terminal disposition supplies the endpoint. Historical entries and their links are extended faithfully rather than silently overwritten. The declared preservation checks and hard constraints remain premises.

A resolution entry must refer to its resolution grounds; a transfer identifies its destination and transfer witness; supersession retains its lineage. “Deferred”, “assigned”, “risk accepted” and “transferred” do not mean “proved resolved”. An issue can leave one active record while remaining live elsewhere. **Semantic validity** additionally requires the substantive truth and applicability of the witness's claims, including its authority and grounds. A complete-looking record cannot produce these facts merely by having the right fields.

**Finite history preservation.** Along a finite sequence of record-valid transitions, every initially recorded obligation remains addressable in the final retained history and has a finite trace of persistence, replacement or disposition. If every substantive disposition made along the sequence is also semantically valid, none of those dispositions is unwarranted relative to the declared contract. This does not retrospectively validate an earlier assertion merely because the initial history contains it.

**Proof.** At zero transitions the initial records and their existing statuses supply the claim. For one transition it is exactly the retention and coverage premise. For the induction step, an already terminal entry and its witness remain in the extended history. A current live record persists, is linked to its successors, or receives its declared endpoint; the new witness retains its predecessor links. Applying this reasoning to every current descendant extends the trace for each initial obligation. After finitely many transitions the history still addresses the original entries and the finite sequence of their changes. The semantic conclusion uses the validity of each substantive link; its mere presence proves no such validity. ∎ [FORM, Theorem 6.5][FORM]

This preservation rule allows genuine active simplification. A guarded contraction can replace an active tensor $`x`$ by $`C_{j,\varphi}x`$ after the required disposition is justified, while the old state, obligation records and witness remain faithfully retained or referenced in history. The active degree can fall while the retained record grows. Conversely, changing a status coefficient can leave every tensor degree unchanged. The contraction and fibre counterexample in [Tensor Moments, §1.3](tensor-moments-and-corrective-dynamics.md#13-degree-shifts-contractions-and-a-higher-order-distinction) shows why degree reduction alone cannot establish a valid disposition.

Addressability does not itself provide an authenticated, permitted and affordable retrieval operation. [Source Context and Reacquisition, §§6.5–7.3](../epistemology/source-context-and-reacquisition.md#65-information-preserved-and-access-preserved) treats that further access question. Nor does a fully traceable history ensure that the active summary preserves the future observables of §2.6. A retained false claim remains a false claim available for later appraisal; representing it again at a higher level does not change its truth. The record-validity conditions are an explicit model of a proposed history-preserving process, not universal reflective conditions on every warranted belief.

### 9.5 Which missing evidence must survive, and what does completion cost?

The certificate-selection problem in §9.4 begins with the outputs already admissible at each state. Inquiry has a further question: which acquisitions would make an actual proof available, and how expensive would it be to complete and check that proof? A present licence bit or a list of true propositions can lose precisely this information. A finite persistent-evidence model admits an exact answer. [24–25]

#### Evidence, conclusions, and terminal checking

Fix a claim and its version, a declared semantics and source commitments, and a finite set $`\mathcal Y`$ of scoped conclusions. These conclusions can include positive support, independently supported negation, inconsistency of a specified premise set, a syntax/type failure, semantic ambiguity, or absence of a certificate in a specified finite search at a fixed inventory/time snapshot. They are distinct output types and need not be mutually exclusive. The task supplies its substantive goal set $`\mathcal G\subseteq\mathcal Y`$. An always-available “defer” record does not count as resolution unless that bounded diagnosis is itself the requested goal.

Let $`E`$ be a finite set of distinguishable evidence tokens. A token identifies content, source or acquisition route, target/version, scope, and authentication conditions. The usable inventory $`K\subseteq E`$ contains currently accessible authenticated tokens. Copying an artifact does not create a different premise or an independent source. Authentication establishes the declared identity and integrity conditions; the commitments under which its contents support a premise remain additional assumptions. A test that returns only uninterpreted or unauthenticated text can have an empty usable payload.

Let $`\Gamma`$ be a finite admitted collection of inspectable valid derivations. For each $`\pi\in\Gamma`$, retain its evidence support $`S_\pi\subseteq E`$, exact conclusion $`v_\pi\in\mathcal Y`$, finite terminal assembly/checking price $`\kappa_\pi\geq0`$, and the derivation with its rule and interpretation references. A rule/scope check of an admitted derivation is guaranteed to succeed when its support meets the stipulated conditions. An unchecked candidate that may fail is an outcome-bearing inquiry step, not a guaranteed terminal action. The collection need not contain every proof of an unrestricted logic; all optimality statements initially concern exactly its permitted derivations. Section 9.6 gives a finite grammar for which that completeness assumption can be proved.

If admitted source commitments support the leaves and each rule preserves the scoped judgement, induction over a derivation proves conditional soundness of the resulting conclusion. This does not authenticate the leaves, prove the commitments or show that any person believes, competently uses, or knows the conclusion. Availability of $`S_\pi`$ makes $`\pi`$ eligible for checking; completion requires actually producing and checking it and paying $`\kappa_\pi`$. Reuse of an already checked proof may instead have an explicit token and priced reuse rule. Authentication paid on acquisition is not silently charged again, and unexecuted terminal checking is not silently made free.

Throughout this subsection, tokens remain valid, accessible and reusable; acquisitions do not revoke them or defeat previously admitted proofs. The semantics, source commitments, proof collection and prices stay fixed. Supports are sets, not consumable multisets. These persistence assumptions concern warrant conditions as well as artifact survival.

#### The canonical residual frontier

For each $`v`$, form the finite support–price set

```math
A_v(K)=\{(S_\pi\setminus K,\kappa_\pi):\pi\in\Gamma,\ v_\pi=v\}.
```

Say $`(D,c)`$ dominates $`(D',c')`$ when $`D\subseteq D'`$ and $`c\leq c'`$. Remove duplicate pairs and each strictly dominated pair; write $`R_v(K)`$ for the resulting Pareto frontier. A retained pair still needs a realizing derivation. Different proofs with the same pair are interchangeable only for the specified availability-and-cost observations.

For additional evidence $`U\subseteq E`$, define

```math
F_{K,v}(U)
=\min\{\kappa_\pi:S_\pi\subseteq K\cup U,\ v_\pi=v\},
\qquad\min\varnothing=+\infty.
```

This is the least price of an eligible terminal proof, not a claim that checking has occurred.

**Theorem 14 — Canonical proof-sensitive continuation.** The tuple $`(R_v(K))_{v\in\mathcal Y}`$ is the coarsest equivalence-class summary of inventories preserving every conclusion's least terminal checking price after every additional evidence set. More explicitly:

```math
F_{K,v}(U)=\min\{c:(D,c)\in R_v(K),\ D\subseteq U\},
```

and

```math
\bigl(\forall v, R_v(K)=R_v(K')\bigr)
\quad\Longleftrightarrow\quad
\bigl(\forall v,U, F_{K,v}(U)=F_{K',v}(U)\bigr).
```

Acquiring $`T`$ updates the frontier by subtraction and renormalization:

```math
R_v(K\cup T)
=\mathrm{Pareto}\{(D\setminus T,c):(D,c)\in R_v(K)\}.
```

Thus equal frontier tuples remain equal after every common acquisition.

**Proof.** Eligibility is equivalent to $`S_\pi\setminus K\subseteq U`$. A dominated pair cannot lower the minimum, proving recovery. Conversely, write $`f(U)=F_{K,v}(U)`$. The frontier can be recovered from the function itself:

```math
R_v(K)=
\left\{(D,f(D)):
 f(D)<\infty\ \text{and}\quad
 f(D\setminus\{d\})>f(D)\ \text{for every }d\in D\right\}.
```

If $`(D,c)`$ is undominated, eligibility gives $`f(D)\leq c`$, while a strictly cheaper eligible pair would dominate it; hence $`f(D)=c`$. Any proper subset with price at most $`c`$ would likewise dominate it. For the converse, finiteness supplies an attaining pair $`(D',f(D))`$ with $`D'\subseteq D`$. If containment were proper, choose $`d\in D\setminus D'`$: the pair would remain eligible after deleting $`d`$, contrary to the strict inequality. Thus $`D'=D`$, and the same argument excludes every strict dominator. Immediate one-token deletions suffice because $`f`$ is antitone under inclusion. The empty-support deletion condition is vacuous, but finite price is still required.

This inverse proves necessity as well as sufficiency of frontier equality. For updating, $`(S_\pi\setminus K)\setminus T=S_\pi\setminus(K\cup T)`$. Dominance survives subtraction, so deleting dominated pairs before or after acquisition has the same final effect. Equivalently,

```math
F_{K\cup T,v}(U)=F_{K,v}(T\cup U).
```

Finally, any summary from which every $`F_{K,v}(U)`$ can be decoded must distinguish inventories with different such functions; the inverse identifies exactly those classes, while recovery and updating construct a sufficient summary. This is uniqueness of the normalized frontier and its equivalence classes, not of their encoding. $`\square`$

The finite-price condition matters. If an actual proof price $`+\infty`$ is identified with the same $`+\infty`$ used for infeasibility, a collection containing only an infinite-price empty-support proof and an empty collection have identical cost observations but different frontiers. The formal source avoids this collapse by adjoining a new top above every admitted price. [25], [31]

Necessity quantifies over all additional sets $`U`$. It is operationally exact when each token has a permanently permitted single-token retrieval action, finite sequences are allowed, and a comparison continuation may request a token already held. Each $`U`$ is then obtainable by a sequence of $`|U|`$ ordinary acquisitions. With a restricted inquiry menu, frontier equality is still sufficient but may distinguish more states than necessary. A token that can never arrive supplies no actual distinguishing continuation. The coarsest quotient for such a menu must compare only its feasible continuations, response possibilities and prices.

The frontier also does not preserve every provenance distinction or replace the proof and evidence themselves. A realizing witness must remain recoverable when the terminal action executes, with any retrieval cost explicitly priced. This is not a minimum physical-RAM theorem that treats an external source of the missing distinctions as free and uncounted memory.

#### Exact feasibility and optimal inquiry cost

Let $`\Omega`$ be a finite nonempty set of response scenarios. Each remaining test $`a`$ in a finite menu $`Q`$ has a fixed response $`o_a(x)`$ in scenario $`x`$, finite nonnegative acquisition/authentication price $`c_a`$, and usable payload $`\tau(a,o)\subseteq E`$. Tests can be used once, remain available until used, and have order-independent responses and payloads. The response model is not a truth oracle.

A planning state is $`(K,B,Q)`$, with nonempty $`B\subseteq\Omega`$ the scenarios compatible with the transcript. For a feasible response $`o`$, put

```math
B_{a,o}=\{x\in B:o_a(x)=o\},\qquad
(K,B,Q)\longmapsto
(K\cup\tau(a,o),B_{a,o},Q\setminus\{a\}).
```

The policy chooses tests or a terminal proof from its observed history. It must finish with a checked $`\mathcal G`$-proof on every remaining scenario. Its cost is the worst-case sum of executed test prices plus the final checking price. Policies are deterministic; allowing randomization with a maximum also over random choices gives the same pathwise objective. Worst-case **expected** cost under private randomization is different.

**Theorem 15 — Completion and least execution cost.** Put

```math
t_{\mathcal G}(K)
=\min\{\kappa_\pi:S_\pi\subseteq K,\ v_\pi\in\mathcal G\}.
```

Then the minimum guaranteed execution cost is the finite Bellman recurrence

```math
D(K,B,Q)=\min\left\{
t_{\mathcal G}(K),
\ \min_{a\in Q}\left[
c_a+\max_{o:B_{a,o}\ne\varnothing}
D(K\cup\tau(a,o),B_{a,o},Q\setminus\{a\})
\right]\right\}.
```

Every finite optimum is attained. Writing

```math
K_x^{\rm all}=K\cup\bigcup_{a\in Q}\tau(a,o_a(x)),
```

guaranteed finite completion is possible exactly when

```math
\forall x\in B\ \exists\pi\in\Gamma:
\quad v_\pi\in\mathcal G\quad\text{and}\quad S_\pi\subseteq K_x^{\rm all}.
```

For fixed $`B,Q`$, equal complete per-conclusion frontiers preserve $`D`$, cost-optimal test actions and optimal abstract terminal conclusion/price choices. The concrete proof identifiers need not agree.

**Proof.** Induct on $`|Q|`$. A successful policy either immediately checks an eligible goal proof or first executes some test $`a`$. In the latter case its worst continuation cost is at least the maximum of the optimum values over feasible responses. Conversely, choose a minimizing terminal proof or first test and recursively optimal policies at each feasible successor. Finitely many proofs, tests and responses ensure attainment of every finite choice. Even when a proof is eligible, a test may make a much cheaper proof available, so the recurrence must allow continued inquiry.

For necessity of the completion criterion, follow a successful policy in any scenario $`x`$. Persistence and order independence place all its acquired evidence inside $`K_x^{\rm all}`$, so its terminal proof is available there. For sufficiency, execute every remaining test in a fixed order. Scenarios with the same full response transcript give the same payload inventory; the condition guarantees a goal proof in that inventory. Inspect the fixed finite collection, select one and check it. The sum of the finite test prices plus the largest proof price bounds this strategy's worst-case cost.

Finally, Theorem 14 gives equal terminal costs and identical successor frontiers after each payload. The same $`B,Q`$ give the same feasible responses, prices and actions. Induction in the recurrence yields equal values and abstract optimal choices. A concrete witness must still be selected for its own inventory. $`\square`$

The recurrence prices execution, not offline proof compilation or policy search, and it implies no polynomial complexity bound. Exact implementation additionally needs effectively represented, comparable prices, such as rationals; finite arbitrary real prices suffice for the mathematical minimum. A scenario failing the full-transcript condition is an obstruction to this stipulated proof-producing protocol. It does not establish that the target is false, unknowable by other means, or unresolvable after admitting different rules or tests.

#### Sharp distinctions between available answers, memory, and search

With one proof requiring $`E=\{e_1,\ldots,e_n\}`$ and terminal price $`k`$, the frontier is $`\{(E\setminus K,k)\}`$. All $`2^n`$ inventories are continuation-distinct. For $`K\ne K'`$, orient them so some $`e\in K\setminus K'`$ exists and acquire exactly $`E\setminus K`$. This common sequence, of at most $`n`$ single-token actions, completes the first inventory while leaving $`e`$ absent from the second. Thus an exact finite-state controller for all these continuations needs $`2^n`$ distinguishable states, or $`n`$ bits in a fixed-length binary encoding. Storing $`K`$ attains the bound. The present availability bit has only two values when $`n\geq1`$; for $`n\geq2`$ it loses distinctions. With unit retrieval prices, the current optimum $`n-|K|+k`$ also merges equally sized but differently populated inventories.

A single frontier can itself be exponentially large. Include, for every $`D\subseteq E`$, a same-conclusion proof with support $`D`$ and price $`n-|D|`$. A smaller support has a larger price, so all $`2^n`$ pairs survive. This is maximal: at most the least price survives for a fixed support. If all prices are equal, the retained supports form an inclusion antichain and the sharp maximum is $`\binom n{\lfloor n/2\rfloor}`$. For completeness, each support $`D`$ occupies a fraction $`1/\binom n{|D|}`$ of permutations in which its elements are the initial $`|D|`$ positions. Two distinct antichain members cannot both be initial sets of one permutation. Consequently $`\sum_D1/\binom n{|D|}\leq1`$, which bounds the number of members by the central binomial coefficient; all subsets of middle size attain it. These are state and frontier bounds, not claims that every individual state needs an exponentially long encoding. [24–25]

Terminal price changes legitimate dominance. A proof needing $`\{a\}`$ at price $`10`$ and another needing $`\{a,b\}`$ at price $`1`$ must both survive. At inventory $`\{a\}`$ their residual pairs are $`(\varnothing,10)`$ and $`(\{b\},1)`$. If obtaining $`b`$ costs one, acquisition plus the second check costs two, better than stopping at ten. Discarding the larger support solely because it contains the smaller one gives the wrong optimum.

Certificate size also fails to price discovery. Suppose exactly one of $`n`$ locations holds an authenticated refutation witness. A unit-cost inspection supplies its location's token only when positive; any positive token supports a proof with fixed check price $`k`$. Every realized certificate needs one token, but worst-case search requires all $`n`$ tests: after $`n-1`$ negative inspections the remaining location can still be the witness, and the specified proof requires actually obtaining it. Inspecting all locations attains $`n+k`$. If an independently warranted promise together with the negative findings is instead admitted as a proof that avoids obtaining the last token, that is a different proof collection. The response model alone does not supply that inference licence. The distinction between certificates and query complexity is classical. [29]

The randomized qualification is sharp even with two scenarios and two unit-cost tests. Let test one return the needed token only in scenario one, and test two only in scenario two; failed tests return no usable token and terminal checking is free. Every deterministic order has worst-case cost two. Uniformly randomizing the order has worst-case expected cost $`3/2`$, while its pathwise worst case remains two. Theorem 15 concerns the latter objective.

Finally, equal displayed content need not mean equal evidential entitlement. An authenticated report $`e`$ of $`P`$ from an admitted source and an unauthenticated copy $`r`$ can display identical text. A rule requiring $`e`$ and an independently justified bridge $`b:P\Rightarrow Q`$ makes $`Q`$ available at $`K_1=\{e,b\}`$. A display containing $`r`$ with usable inventory only $`K_2=\{b\}`$ does not meet that rule. If all remaining tests merely repeat $`r`$, the second state cannot complete under this menu. The example does not make authenticated testimony automatically true or unauthenticated testimony automatically false; it isolates an explicit source-sensitive premise. A new warranted route can change the result.

The coordinate counts of §§2–9.3 measure functions of a law. Evidence acquisition concerns identified tokens and scoped proofs. A single action may supply many tokens, or one necessary token may be unavailable or arbitrarily expensive. Rescaling one acquisition price changes $`D`$ without changing a retained observable span. No universal conversion from coordinate dimension to inquiry cost follows.

#### Clarification, semantic cover, and version fidelity

Semantic clarification can be a legitimate inquiry, but it has its own evidential burden. Fix a justified finite interpretation family $`I`$ for the submitted claim version; interpretation $`i`$ gives precise content $`q_i`$. An admitted proof $`s_J`$ may establish that the intended interpretation belongs to nonempty $`J\subseteq I`$. Under the rule requiring $`s_J`$ and a proof of $`\neg q_j`$ for each $`j\in J`$, the conclusion is that the intended content of this version is refuted. The negations must concern the same intended domain and version.

**Proposition 16 — Semantic cover.** If $`s_J`$ uses support $`A`$ and the chosen refutation of each $`q_j`$ uses $`C_j`$, this rule produces support

```math
A\cup\bigcup_{j\in J}C_j.
```

Taking all admissible $`J`$, their semantic proofs and their premise-proof choices enumerates exactly the supports generated by the rule. Shared evidence is acquired once; the actual combined derivation determines its checking price.

**Proof.** The support is the union of the rule's evidence leaves. Every admitted choice realizes that union, and every instance has such a choice. Soundness is conditional on $`s_J`$: the intended interpretation is one member of $`J`$, and its negation is among the proved premises. $`\square`$

With two possible meanings, separate refutations of both, a common refuting certificate, and clarification followed by one refutation can have different costs. Theorem 15 compares those legitimate routes. An investigator's convenient reinterpretation supplies no $`s_J`$ and cannot erase the original task. Nor must every imaginable interpretation be investigated: admissibility of $`I`$ is a substantive input.

The same discipline governs a proof carried across versions. A proof of $`(q_0,\sigma_0)`$ does not prove $`(q_1,\sigma_1)`$ merely because their displayed words agree. An admitted interpretation-transport proof adds its own support, scope and checking price. An untagged availability summary can otherwise merge a history containing that bridge with one lacking it, changing possible completion into impossible completion. Erasing tags need not lose a bridge token that is separately retained; the failure concerns the specified lossy summary. This finite application complements §9.4's version-transport proof without supplying its semantic or authority premises. It leaves actual philosophical conclusions and human operative basing to their proper evidence.

Persistence is indispensable. If a proof requires $`p,q`$, a test obtaining $`p`$ expires $`q`$, and a test obtaining $`q`$ expires $`p`$, then the union of all historically returned tokens is $`\{p,q\}`$ but no reachable active inventory from the empty state contains both. The full-transcript criterion would be false for that model. Expiry, consumption, defeat, source withdrawal or changing permissions must be represented in an expanded state before a new Bellman theorem is applied; simple set subtraction and monotone accumulation cannot be inherited without proof.

#### Exact predicate decisions as a zero-checking-price case

A useful specialization asks whether a proposed revision meets a fixed admission rule. Fix a transition $`x\to y`$, a bounded target $`T`$, a finite nonempty set $`C`$ of compatible situations, and a supplied Boolean predicate $`g:C\to\{0,1\}`$. For example, $`g(w)=1`$ can mean that the transition is authorised, feasible and preferred under $`T`$ in situation $`w`$. Hard constraints act as vetoes. Preference can be a strict partial or lexicographic order; a scalar loss comparison is optional. No numerical weighting or gradient is required. The evidence procedure cannot choose the target or fill in an unspecified preference. Minimising answer length alone, for instance, can favour an empty answer over fulfilment of a request. [42]

Let $`\mathcal Q`$ be a finite menu of authorised probes with known deterministic response maps $`h:C\to Y_h`$ and fixed finite prices $`c_h>0`$. Probes leave the situation unchanged or operate on resettable copies; their meanings, prices and availability remain fixed. The actual situation $`w_*`$ is assumed to lie in $`C`$. Protocols are deterministic, observations are exact, and a run pays the sum of its probe prices. The supplied tables for $`g`$ and the responses do not themselves reveal $`w_*`$ or establish probe reliability. Unrepresented noise, drift and unreliable observations lie outside this model.

A transcript leaves a nonempty residual $`S\subseteq C`$. Uniform soundness permits a Boolean answer $`b`$ only when $`g(w)=b`$ throughout $`S`$. Otherwise a protocol may inquire or report unresolved; an empty residual signals model inconsistency. The optimization below requires a decision on **every** remaining situation, so an always-unresolved protocol does not qualify. Put $`S_{h,a}=\{w\in S:h(w)=a\}`$ and define

```math
V_g(S)=
\begin{cases}
0,& |g(S)|=1,\\[3pt]
\displaystyle\min_{\substack{h\in\mathcal Q\\|h(S)|>1}}
\left(c_h+\max_{a\in h(S)}V_g(S_{h,a})\right),& |g(S)|>1,
\end{cases}
\qquad \min\varnothing=+\infty.
```

Every child of an informative probe is a nonempty proper subset of $`S`$, so this recurrence is well founded. It is the predicate-decision specialization of Theorem 15, with **zero terminal checking price**. To see the specialization precisely, use the chosen initial compatible set as the scenario space, give each observed response its identified token $`(h,a)`$, and admit a model-relative derivation for each consistent partial response assignment whose compatible situations all have the same $`g`$-label. Both labels are goal conclusions, and all these terminal derivations have price zero. The collection is finite. A terminal derivation is eligible exactly when the current residual is monochromatic. The supplied model tables and their interpretation are premises of these derivations, rather than conclusions certified by their availability.

After a probe has been used, its response is constant on every later residual, so repeating it cannot help. An unused probe constant on the current residual also leaves that residual and every future information possibility unchanged. Deleting either kind of probe reduces positive cost without losing a possible decision. This justifies the one-use convention of Theorem 15 and the restriction to informative probes here. It does **not** justify deleting constant-response acquisitions from the general theorem: those can supply genuinely needed evidence tokens when terminal proofs have different admission conditions. Theorem 15 therefore supplies the lower bound, attainment of every finite value, and impossibility when the value is infinite; its induction need not be repeated.

In particular, write $`O(w)=(h(w))_{h\in\mathcal Q}`$. A decision is possible on every situation exactly when

```math
O(w)=O(v)\ \Longrightarrow\ g(w)=g(v).
```

Indeed, equal complete observations force an adaptive deterministic protocol to choose the same first probe, receive the same answer and then repeat that agreement at every later choice. Its terminal answer cannot distinguish opposite labels. Conversely, querying every probe leaves one complete-observation fibre; constancy of $`g`$ there supplies the answer. This is the full-transcript criterion of Theorem 15 in the present specialization. It establishes possibility, while $`V_g`$ prices that possibility. A finite value above the available budget and an infinite value are different obstructions; neither is the negative admission verdict $`g=0`$. Some branches may remain affordable when a finite worst-case optimum exceeds the budget, but they do not give a guarantee for every situation.

If $`g`$ is constant on $`S`$, stop with its unique label. Otherwise, if $`V_g(S)<\infty`$, choose a minimizing probe, execute it and continue on $`S_{h,h(w_*)}`$. If the remaining budget covers $`V_g(S)`$, the recurrence ensures that every child continuation fits after paying $`c_h`$. Affording just the next probe is insufficient. A heuristic policy needs its own argument for any cost guarantee. The source compares this concrete/symbolic feedback with directed and concolic testing [42]. Here the symbolic state is a set of compatible situations, not necessarily a program path condition; program execution semantics, constraint-solving machinery and evidence that an actual execution followed the procedure remain separate requirements.

This optimum prices probes alone. It excludes model construction, verification of probe reliability and computation of the inquiry policy, which may involve exponentially many residual sets. Zero terminal checking price is an explicit idealization of this specialization, not a change to the general theorem's account of actual proof checking.

#### Retained records and changed questions

Suppose a retained record $`r:C\to Z`$ has known, unchanged meaning and is available with no additional access cost. Its earlier acquisition cost is excluded from the additional budget. With $`C_z=\{w\in C:r(w)=z\}`$, the exact costs before and after its value is specified are

```math
V_g(C\mid r)=\max_{z\in r(C)}V_g(C_z),
\qquad
\text{cost after observing }z=V_g(C_z).
```

The freely observed record first selects a nonempty fibre. Theorem 15 gives an attainable optimum separately on each fibre; the worst of these values is necessary and sufficient before the record value is known. Thus a finite nonnegative budget $`\beta`$ guarantees a decision exactly when $`V_g(C\mid r)\leq\beta`$, or $`V_g(C_z)\leq\beta`$ after the particular value is observed. An inaccessible or semantically changed record does not meet these premises. [42]

If the question changes to a specified predicate $`g'`$ while situations and record meanings stay fixed, substitute $`g'`$ in the formula. No new probe is needed exactly when $`g'`$ is constant on every record fibre. Earlier acceptance under $`g`$ does not establish that condition. More generally, a freely available record suffices for **every** Boolean decision on $`C`$ exactly when it is injective: an injective record identifies the situation; if $`r(w)=r(v)`$ for distinct situations, a predicate assigning them opposite labels cannot be decided from that record. For a restricted family $`\mathcal F`$, the exact condition is only

```math
r(w)=r(v)\ \Longrightarrow\quad
\bigl(\forall f\in\mathcal F,\ f(w)=f(v)\bigr).
```

This is the target-relative fibre criterion of [Physical Realisation, §9.3](physical-realisation-and-continuation.md#93-lossless-abstraction-is-target-relative), applied to the intended future questions. Smaller records may therefore suffice, and collecting rich evidence before its eventual use is chosen remains legitimate. The same decision architecture can serve different purposes while their evidence requirements differ. When an artifact or an observation's meaning changes, a justified relation to the new situation space is additionally needed. Section 9.4's semantic-transport conditions address that separate burden: a digest can check retained bytes, but supplies neither the semantic bridge nor factual truth.

#### An exact adaptive advantage

The address construction in [42] gives a strict comparison under the same exact observation model. For an integer $`k\geq1`$, use the **full** domain

```math
C=\{0,1\}^{k}\times\{0,1\}^{2^k},\qquad
\mathrm{index}(a)=\sum_{j=1}^{k}2^{k-j}a_j,\qquad
g(a,z)=z_{\mathrm{index}(a)},
```

where the data coordinates are $`z_0,\ldots,z_{2^k-1}`$. Every address/data assignment is admitted independently. The only probes read individual bits at unit positive cost, with deterministic responses on unchanged inputs or resettable copies. Reading the $`k`$ address bits and then the selected data bit decides the output in $`k+1`$ queries.

For the matching lower bound, every one of the $`n=k+2^k`$ input variables is essential. Each data bit is the output for its own address. Flipping any address bit changes the selected index; assigning different values to those two data positions witnesses essentiality of that address bit. If an essential variable labels no query node anywhere in an exact decision tree, the two witnessing inputs differing only in that variable follow the same path and reach the same answer, a contradiction. Hence the **whole tree** has at least $`n`$ internal nodes. A binary tree of depth at most $`k`$ has at most

```math
1+2+\cdots+2^{k-1}=2^k-1\lt{}k+2^k
```

internal nodes. Depth $`k`$ is impossible, and the attaining construction proves that the optimal adaptive cost is exactly $`k+1`$. This lower bound counts nodes across the entire tree; it does not say that one adaptive path queries every essential variable.

A nonadaptive battery fixes all queried coordinates before receiving any answer. Omitting an essential variable makes its two witnessing inputs indistinguishable to that fixed battery. Every coordinate must therefore be included, and querying all of them attains the exact cost $`k+2^k`$. At $`k=4`$, the costs are five adaptive queries and twenty fixed queries. The separation is exponential in address length $`k`$; it concerns additive query cost, not elapsed parallel time, and promises no adaptive advantage for every task. Restricting the input domain or changing the allowed probes changes the problem.

#### Revising the rule can revisit the same pair

An object-level revision changes the artifact; a method-level revision changes how such revisions are judged. In this modelled process, a proposed method change must meet the predecessor's admission rule, while the evidence that remains sufficient under the successor rule must be assessed separately. The successor's declaration that it is acceptable cannot serve as its sole warrant. Composing conditional local decisions does not independently certify their premises. [42]

Strict local improvement also leaves a termination question. Let the artifact be $`x\in\{0,1\}`$, and let the two methods use losses

```math
L_0(x)=x,\qquad L_1(x)=1-x,
```

with the same stipulated permissions and feasibility conditions. Suppose both displayed method/artifact changes are permitted, with no additional constraint or change cost vetoing them. Then

```math
(L_0,1)\longrightarrow(L_1,0)\longrightarrow(L_0,1)
```

satisfies strict improvement under the predecessor loss at each step:

```math
L_0(0)=0<1=L_0(1),\qquad
L_1(1)=0<1=L_1(0).
```

The complete method/artifact pair repeats, so these permitted steps can continue indefinitely without any error in the displayed local comparisons. If the process also retains an ever-growing history, as in §9.4, that larger historical state need not repeat; the counterexample concerns the active pair. A single common well-founded order strictly decreased by every accepted transition would suffice for termination, because an infinite accepted run would give an infinite descending chain. Changing local losses supply no such order, and strict decrease of arbitrary real values alone need not be well founded. Section 9.4 obtains its distinct persistence guarantees from explicitly specified transition models and ranks; those hypotheses do not follow from local loss comparisons.

#### Behavioural parity and a missing delivery-cost observation

Agreement on every task output need not determine the effort required to obtain, invoke or maintain a representation. The following two-world construction makes the missing observation explicit [42]. Fix representations $`p_0,p_1`$ that, in both situations $`w_-,w_+`$, return the same fixed value $`b(u)`$ on every admitted task input $`u`$. Authorisation and feasibility also agree across the worlds. Give their delivery costs the values

```math
\begin{array}{c|cc}
 & w_- & w_+\\\hline
d(p_0,\cdot)&1&1\\
d(p_1,\cdot)&0&2
\end{array}.
```

The predicate “same task behaviour and lower delivery cost” admits $`p_1`$ precisely in $`w_-`$: $`g(w_-)=1`$ and $`g(w_+)=0`$. With $`C=\{w_-,w_+\}`$, every behaviour-only probe has equal responses in the two worlds. The full-observation criterion therefore gives $`V_g(C)=+\infty`$ for that menu, however many such task-correctness tests it contains.

Now add exactly one authorised probe

```math
h_\Delta(w)=d(p_1,w)-d(p_0,w),\qquad c_{h_\Delta}=1.
```

Its responses are $`-1`$ and $`1`$. One query separates the worlds and leaves a free terminal decision, so the enlarged menu has value at most one. Any deciding protocol must use this probe, since every other response is identical across the opposite-labelled worlds; its value is therefore **exactly one**. Repeating behaviour-only probes cannot supply the missing coordinate. A probe measuring installation or invocation effort is not behaviour-only in this construction.

The example stipulates an independent delivery-cost coordinate without a linking assumption from behaviour. It measures no actual representation's cost and establishes no empirical cheaper-representation claim. The contract and interface distinctions in [Physical Realisation, §§2.1–2.2](physical-realisation-and-continuation.md#21-a-contract-before-an-experiment) explain what a real replacement must preserve; [§10.5](physical-realisation-and-continuation.md#105-resources-include-the-controller) includes the controller and its own resource use. The present $`V_g`$ comparison retains its narrower accounting: model-building, policy-computation and reliability-verification costs are excluded.

Finally, constructing a candidate for measurement and admitting it for use are different proposed transitions. Bounded exploration can satisfy its own purpose, permissions, costs and constraints while leaving the final adoption predicate unresolved. Specifying a decision, obtaining separating observations and pricing their continuation gives a conditional inquiry procedure; it does not select the purpose, authenticate its own premises or ensure universal convergence.

### 9.6 From finite inference rules to complete certificate frontiers

The preceding theory starts with an admitted finite proof collection. It can cover **all finite derivations** of a declared finite grounded rule system, even when its dependency graph has cycles. The resulting theorem distinguishes two genuinely different checking costs: charging every occurrence in a tree and charging each shared node of a proof graph once. [26]

#### The grounded-rule contract

Let $`J`$ be a finite set of fully scoped judgements and $`E`$ a finite evidence universe; put $`n=|J|`$ and $`m=|E|`$. Let $`\mathcal R`$ be a finite set of ground rule instances. Each $`r\in\mathcal R`$ has a head $`h(r)\in J`$, a finite ordered premise list $`p_1(r),\ldots,p_{k(r)}(r)`$, local evidence requirement $`B(r)\subseteq E`$, and finite nonnegative checking price $`w(r)`$. The list may repeat a premise. Nullary rules are explicitly admitted leaves, including whatever evidence they require.

A judgement includes every parameter needed for substitution of proofs: proposition or type, context, version, source restrictions, resource conditions and independence requirements. Each premise must accept **any valid proof of that same scoped judgement**. There are no hidden shape-, history-, or proof-dependent admission tests. Rules are positive operationally: content expressing a negation is allowed, but absence of a proof is not an evidence-producing rule, and a cycle alone is not a proof. Soundness of the admitted grammar remains a separate premise.

Evidence is persistent and reusable, combined by union. Two repeated occurrences of $`P`$ permit reuse of one proof of $`P`$; they cannot encode a demand for two independent sources. Such a demand must survive in source-labelled judgements or an independently justified relation. If the necessary refinement makes $`J`$ infinite, the finite theorem does not apply. A finite printed list of schemata is not a finite set of their scoped ground instances.

In the **tree contract**, every rule occurrence is checked and charged. For a tree with root rule $`r`$ and premise trees $`T_i`$,

```math
\mathrm{supp}(T)=B(r)\cup\bigcup_i\mathrm{supp}(T_i),\qquad
c_{\rm tree}(T)=w(r)+\sum_i c_{\rm tree}(T_i).
```

Copying a subtree into two premise positions charges its checking twice while acquiring its evidence only once. In the **shared-graph contract**, a finite acyclic graph contains a rule at each node and one premise reference per ordered premise position. Every node is reachable from the root. Its support is the union of local requirements and its cost is the sum of local prices over distinct nodes. A price includes checking the node's own premise references; a repeated reference does not recheck the referenced subtree. These are declared terminal checking models, not empirical runtime claims. Compilation and final witness reconstruction/checking remain distinct operations.

#### Cycles do not require an infinite tree catalogue

**Theorem 17 — Finite tree compilation.** Under the grounded-rule and tree contracts, every finite proof of $`q`$ is dominated in support and cost by one of height at most $`n`$, where height counts rule nodes. The full frontier of all finite $`q`$-proofs is finite, attained, and has at most $`2^m`$ pairs. It is computed with actual witnesses after at most $`n`$ synchronous frontier rounds, starting from no proofs.

**Proof of the height bound.** If two nodes on one branch carry the same scoped judgement, replace the ancestor's entire subtree by the descendant's subtree. Exact substitution makes the result legal. The replacement support is a subset, and its price is no greater because the deleted occurrences and side subtrees have nonnegative prices. The number of nodes strictly decreases even when a deleted loop has zero price. Repeat to termination. No judgement then repeats on a branch, so height is at most $`n`$.

**Proof of finite attainment.** There are finitely many trees of bounded height over a finite grammar of finite arity. Let $`H_q`$ be those of height at most $`n`$. Every finite proof is dominated by a member of $`H_q`$, and every member of $`H_q`$ is dominated by a retained element of its finite normalized pair set. A retained pair cannot be strictly dominated by an unrestricted finite proof: reducing that proof would supply a strictly dominating member of $`H_q`$, a contradiction. Thus the finite normalized set is exactly the unrestricted frontier, and every globally undominated pair has a bounded-height realizing tree. At most one price survives for each of the $`2^m`$ supports.

**Construction and proof of saturation.** Initialize $`A_0(q)=\varnothing`$. Form $`A_{h+1}(q)`$ by normalizing the union of $`A_h(q)`$ and all pairs

```math
\left(B(r)\cup\bigcup_{i=1}^{k(r)}S_i,
       w(r)+\sum_{i=1}^{k(r)}c_i\right),
\qquad h(r)=q,\quad (S_i,c_i)\in A_h(p_i(r)).
```

A nullary rule contributes $`(B(r),w(r))`$ by the empty-product convention. Store the actual rule and immutable child witnesses for every retained pair. Inductively, $`A_h(q)`$ is the normalized pair set of trees of height at most $`h`$. Replacing any child by a dominating child can only shrink the parent's union of supports and lower its additive price, so discarded child pairs cannot produce a uniquely undominated parent. Conversely, each generated pair has the displayed realizing tree. The height bound shows that $`A_n`$ is the unrestricted frontier; one further round changes no pair set. Equality of all pair sets at an earlier round is also a sound stopping test, since the recurrence then reproduces them forever. Witness identities need not match for this test. $`\square`$

The antichains themselves need not grow by set inclusion: a better pair can replace an earlier pair. What grows is the upward closure of dominated possibilities. A chain of $`n`$ distinct judgements ending in a leaf shows the height bound is sharp. If maximum rule arity is $`a`$, a height-$`n`$ witness can still have $`1+a+\cdots+a^{n-1}`$ nodes, and exponentially many support/price alternatives can survive. No efficient scaling bound follows from finite termination.

The theorem preserves Pareto possibilities, not every exact proof support. For example, a leaf proof of $`q`$ requiring $`a`$ and a self-rule additionally requiring $`b`$ give a two-node proof with support $`\{a,b\}`$ dominated by the leaf with support $`\{a\}`$. If a different task requires an **exact** support, delete an ancestor–descendant pair only when both judgement and subtree support agree. This preserves support, does not increase cost, and still decreases node count. Along a branch supports are nested and can strictly shrink at most $`m`$ times; within each of at most $`m+1`$ constant-support blocks, no judgement repeats after pruning. Height $`n(m+1)`$ therefore suffices to attain the minimum price of every occurring exact support. It does not enumerate every proof or preserve its full derivation structure.

#### Sharing needs a whole-graph argument

**Theorem 18 — Finite shared-graph compilation.** Under the shared-graph contract, every finite proof graph is dominated by one with at most one node for each fully scoped judgement. Its exact terminal frontier is consequently computable by finite rule-choice enumeration.

**Proof.** Order the original graph topologically, premises before parents. For each judgement choose its earliest occurrence. At that selected node keep its original rule, but redirect every premise reference to the earliest occurrence of the required premise judgement. If the original premise has index $`i`$ and the selected parent index is $`j`$, its selected replacement has index at most $`i<j`$. Every redirected edge therefore still goes strictly earlier; the graph remains acyclic and every premise has the required scoped judgement. Use the selected occurrence of the original root judgement as root and discard unreachable selected nodes.

The retained nodes are a subset of the original occurrences. Their local requirements and prices are unchanged, so union support and the sum of nonnegative prices cannot increase. There is at most one node per judgement. Enumerate one rule or “absent” for each judgement; from the proposed root, reject missing premises and recursion-stack cycles and keep the reachable subgraph. This finite family contains every reduced graph just constructed. Normalization therefore gives the exact frontier of all finite graphs, with a realizing graph for each retained pair. $`\square`$

There are at most $`\prod_{q\in J}(1+|\{r:h(r)=q\}|)`$ rule selections. Root-unreachable choices are immaterial; an unsupported reachable self-loop is rejected rather than accepted as a zero-cost proof. No topological order needs to be guessed in advance. Repeated premise references may point to the same chosen node precisely because the contract permits that reuse.

The tree recurrence nevertheless cannot be reused as a shared-graph optimizer. Consider judgements $`p,a,b,t`$, one evidence token $`e`$, and these rules:

| Head | Premises | Local evidence | Local price |
|---|---|---|---:|
| $`p`$ | none | $`\{e\}`$ | 5 |
| $`a`$ | $`p`$ | none | 0 |
| $`a`$ | none | $`\{e\}`$ | 4 |
| $`b`$ | $`p`$ | none | 0 |
| $`t`$ | $`a,b`$ | none | 0 |

Every terminal proof has support $`\{e\}`$. The standalone frontier for $`a`$ discards its route through $`p`$, of price five, in favour of the direct proof of price four. Tree checking makes the best $`t`$-proof cost $`4+5=9`$; copying the $`p`$-proof in both branches would cost ten. A shared graph instead uses one $`p`$-node for both $`a`$ and $`b`$, so its optimum is five. If intermediate graph proofs were pruned using only their standalone support and cost, that optimal sharing opportunity would already be lost, leaving nine.

Local dominance is thus not preserved by contexts that can share internal checked nodes. A compositional graph method needs additional sharing information, or it can use the finite whole-graph enumeration above. Once the complete **terminal** graph frontier has been compiled, ordinary support/price normalization and Theorem 14 apply without change. This distinction concerns the declared once-per-node price; it is not a result about arbitrary caching, scheduling or machine execution.

#### Scope and the interface back to inquiry

Choose the tree or shared-graph checking contract, compile the frontier for each terminal judgement and retain its witnesses. Residualizing at inventory $`K`$ then gives exactly the least checking price over **all finite derivations of that admitted grammar** whose support lies in $`K\cup U`$. Every finite optimum is attained. An empty frontier means no finite proof in that grammar, not falsehood and not absence of a proof in a stronger logic. Theorem 15 can use these compiled witnesses without an independently postulated finite catalogue; source authentication and rule soundness still have to be supplied.

The arguments use finiteness and nonnegative additive prices, not discreteness. They apply to finite nonnegative rational or real rule prices; effective exact compilation additionally requires effective addition and comparison. Several different failures must be kept separate:

- A price-$`-1`$ self-rule and a price-zero leaf yield finite proof prices $`0,-1,-2,\ldots`$ with no minimum. Nonnegative-cost pruning fails.
- Infinitely many nullary rules with one support and prices $`1,1/2,1/3,\ldots`$ have no least price despite all prices being positive. Finiteness of ground instances fails.
- A finite schema list containing $`P(0)`$ and $`P(x)\Rightarrow P(s(x))`$ generates infinitely many scoped judgements. Printed finiteness does not establish finite grounding.
- A total price $`1/(1+\text{number of nodes})`$ is nonnegative but violates fixed additive local pricing; looping syntax can then produce an unattained decreasing sequence.
- Consumable evidence, erased source-independence conditions, order-sensitive authority or proof-dependent side conditions can invalidate exact substitution. They require a separately justified state and rule interface.

In particular, neither theorem supplies a finite complete interface for unrestricted natural-language inference, dependent typing or impredicative proof systems. Contexts, types and conversion premises cannot be erased merely to manufacture finitely many judgement labels. The existence of a particular finite proof establishes neither that all relevant proofs fall in that finite grammar nor a subject's knowledge or use of its premises. The inherited open derivation and interpretation questions retain their status.

Positive provenance and weighted deduction provide the mathematical ancestry: alternative derivations combine differently from joint premises, and recursive systems may need fixed-point semantics. Green, Karvounarakis and Tannen develop provenance semantics for positive queries and recursive Datalog; Goodman treats semiring deduction and explains why non-improving Viterbi loops can be omitted. Here the support/price order and explicit tree-versus-sharing contract support the self-contained finite arguments above. They make no field-wide originality claim. [27–28]


### 9.7 Unknown standards: the information needed for persistent repair

The earlier results ask what information a representation must retain once its prediction, value, geometry, or certificate contract is supplied. A different question arises when the rule governing correct repair is itself unknown. Selecting an admissible action need not generally identify a hidden state (§9.4). In the following family, however, increasingly exact repairs force the output to identify the standard. Finite information then limits not only confidence at one opportunity, but the probability of indefinite eventual correctness. The two source treatments [32–33] distinguish that obstruction from a positive construction when informative observations can be acquired without violating the target.

#### Repair geometry and its decoding requirement

Fix a supplied parameter *α* in (0,1), two truth vertices *v*<sub>i</sub> = (*i*,1−*i*) for *i* = 0,1, and the quadratic loss

```math
L_\alpha(x,v)=\alpha(x_1-v_1)^2+(1-\alpha)(x_2-v_2)^2.
```

At an opportunity with disturbance 0 < *ε* ≤ 1/4, the input is *b*<sub>ε</sub> = (1/2+*ε*,1/2). A coherent repair has the form *c* = (*q*,1−*q*), with 0 ≤ *q* ≤ 1. It is **good** if it weakly improves the loss at both truth vertices. This simultaneous requirement is stronger than improvement in an average taken under a declared distribution of truth states. The parameter is the supplied standard in this model; an observation channel related to it is an additional premise.

Put *r*<sub>α</sub> = 1/2+*αε* and *D*<sub>α</sub> = *α*(1−*α*)*ε*². Completing the square gives, for each *i*,

```math
L_\alpha(b_\epsilon,v_i)=(r_\alpha-i)^2+D_\alpha,
\qquad
L_\alpha(c,v_i)=(q-i)^2. \quad\text{(26)}\quad
```

Thus a known standard permits the exact repair *q* = *r*<sub>α</sub>, with common improvement *D*<sub>α</sub>. It is strictly positive in the interior, and zero at the endpoint standards 0 and 1.

**The same calculation for an arbitrary binary disturbance.** The earlier integration probe [45] starts from an arbitrary incoherent input $`x=(x_1,x_2)`$, rather than the particular $`b_\epsilon`$. Put

```math
\Delta=x_1+x_2-1\ne0,\qquad
r_\alpha(x)=x_1-(1-\alpha)\Delta,\qquad
k_\alpha=\alpha(1-\alpha).
```

For either truth vertex, write $`u=x_1-i`$. The other input error is $`\Delta-u`$, and

```math
\alpha u^2+(1-\alpha)(\Delta-u)^2
 =\bigl(u-(1-\alpha)\Delta\bigr)^2+k_\alpha\Delta^2.
```

Thus $`L_\alpha(x,v_i)=(r_\alpha(x)-i)^2+k_\alpha\Delta^2`$, while a coherent output still has loss $`(q-i)^2`$. Since $`0\le q\le1`$, the complete set of weak improvements at both truth vertices is exactly

```math
\left[
 1-\sqrt{(1-r_\alpha(x))^2+k_\alpha\Delta^2},
 \ \sqrt{r_\alpha(x)^2+k_\alpha\Delta^2}
\right]\cap[0,1].
```

Both endpoint inequalities are needed. If $`r_\alpha(x)\in[a,1-a]`$ for $`0\lt{}a\le1/2`$, a member of this interval satisfies

```math
|q-r_\alpha(x)|\le\frac{k_\alpha\Delta^2}{2a},
\qquad
\widehat\alpha=\frac{q-x_1+\Delta}{\Delta},
\qquad
|\widehat\alpha-\alpha|
 \le\frac{k_\alpha|\Delta|}{2a}
 \le\frac{|\Delta|}{8a}.
```

For $`q\ge r_\alpha(x)`$, subtracting the zero-vertex losses gives
$`2r_\alpha(x)(q-r_\alpha(x))+(q-r_\alpha(x))^2\le k_\alpha\Delta^2`$.
For $`q\le r_\alpha(x)`$, the one-vertex inequality gives the corresponding
linear coefficient $`2(1-r_\alpha(x))`$. Both coefficients are at least
$`2a`$. Dropping the nonnegative square proves the first bound; the exact
identity $`q-r_\alpha(x)=\Delta(\widehat\alpha-\alpha)`$ proves the decoder
bound for either sign of the nonzero disturbance. In the particular family
$`x=b_\epsilon`$, one has $`\Delta=\epsilon`$ and
$`r_\alpha(x)=1/2+\alpha\epsilon\in[1/2,3/4]`$. Taking $`a=1/4`$ gives the
bound in the next lemma. The more general formula does not by itself supply
an observation model, a uniform statistical rate over arbitrary inputs, or
a dynamic restoration theorem.

**Lemma 19 — A good repair decodes the standard.** Every good repair satisfies

```math
|q-r_\alpha|\leq 2D_\alpha\leq\epsilon^2/2,
\qquad
\left|\frac{q-1/2}{\epsilon}-\alpha\right|\leq\epsilon/2. \quad\text{(27)}\quad
```

If *q* ≥ *r*<sub>α</sub>, goodness at *i* = 0 gives

```math
2r_\alpha(q-r_\alpha)+(q-r_\alpha)^2\leq D_\alpha.
```

If *q* < *r*<sub>α</sub>, goodness at *i* = 1 gives the same inequality with the linear term $`2(1-r_\alpha)(r_\alpha-q)`$. Since 1/2 ≤ *r*<sub>α</sub> ≤ 3/4, the relevant linear coefficient is at least 1/2. Discarding the nonnegative square proves the first bound; $`\alpha(1-\alpha)\leq1/4`$ and division by *ε* prove the rest. The calculation also holds for endpoint standards and for real *q* before imposing coherence. ∎

Let *G*<sub>α,ε</sub> be the set of good coherent repairs. If two standards are separated by more than *ε*, their good-repair sets are disjoint: an output in their intersection would, by (27), decode within *ε*/2 of both. Equation (27) is a **necessary** condition. An arbitrary estimate within *ε*/2 need not produce a good repair; a separate sufficient bound is given below.

**Checking the exact target rather than only its decoder.** The source audits
[46–47] distinguish three boundaries by literal loss calculations. At
$`\alpha=1/2`$, $`\epsilon=1/4`$ and $`q=21/32`$, the center is $`r_\alpha=5/8`$.
The decoded error is exactly $`1/8=\epsilon/2`$, so the necessary bound (27)
holds. Nevertheless the zero-vertex excess loss is

```math
q^2-\bigl(r_\alpha^2+D_\alpha\bigr)
 =\frac{441-400-16}{1024}
 =\frac{25}{1024}>0.
```

This output is not good. The sufficient tolerance used in (30) consequently
cannot be replaced by the larger necessary decoder radius.

A fixed disturbance also leaves genuine common repair cells. At
$`\epsilon=1/4`$, the input losses are
$`1/4+5\alpha/16`$ at the zero vertex and $`1/4-3\alpha/16`$ at the one vertex.
The following two source controls therefore follow by direct substitution:

| Fixed output | Admitted standards | Input loss minus output loss at the two vertices |
|---|---|---|
| $`q=5/8`$ | $`\alpha\in[9/20,7/12]`$ | $`(20\alpha-9)/64`$ and $`(7-12\alpha)/64`$ |
| $`q=9/16`$ | $`\alpha\in[1/4,5/16]`$ | $`(80\alpha-17)/256`$ and $`(15-48\alpha)/256`$ |

Each displayed pair is nonnegative throughout its stated interval. One
constant output can thus repair a nontrivial interval of standards at a
fixed positive disturbance; no exact limiting identification follows until
the shrinking-disturbance premise is supplied. At $`\epsilon=0`$,
$`q=1/2`$ is a common weak repair for every standard. At an endpoint standard
and within the admitted disturbance range, $`D_\alpha=0`$ and the two weak
inequalities force $`q=r_\alpha`$, so strict improvement at both vertices is
impossible there. The interior strict-repair construction and these weak
endpoint statements have different domains. These computations explain
the controls; they do not claim a new execution of the historical audit
fixtures.

#### A finite-sample lower bound and the meaning of a fresh observation

For the next result, each informative probe returns a fresh independent Bernoulli(*α*) observation. Before issuing its repair, an algorithm may obtain at most *N* such observations at adaptively chosen times. Its other information and private randomization contain no additional parameter information. Equivalently, its transcript and output are a common measurable postprocessing of *N* independent probe outcomes and parameter-independent randomness. Any additional informative feedback requires a different, explicitly specified experiment.

**Theorem 20 — Local finite-confidence cost.** For 0 < *ε* ≤ 1/4, put $`\alpha_- = 1/2-\epsilon`$ and $`\alpha_+ = 1/2+\epsilon`$. Every algorithm in this experiment has

```math
\begin{aligned}
\max_{\alpha\in\{\alpha_-,\alpha_+\}}
 P_\alpha\{q\notin G_{\alpha,\epsilon}\}
&\geq \frac{1-\sqrt{1-(1-4\epsilon^2)^N}}{2}\\
&\geq \frac{(1-4\epsilon^2)^N}{4}
 \geq \frac14\exp\!\left(-\frac{16}{3}N\epsilon^2\right).
\end{aligned} \quad\text{(28)}\quad
```

Consequently a guarantee of failure at most *δ* < 1/4 uniformly over $`\alpha\in[1/4,3/4]`$ requires

```math
N\geq \frac{3}{16\epsilon^2}\log\frac{1}{4\delta}. \quad\text{(29)}\quad
```

**Proof.** Use the output as a test: choose the minus alternative when $`q\in G_{\alpha_-,\epsilon}`$ and the plus alternative otherwise. The minus testing error equals the minus repair failure. Since the two good-repair sets are disjoint, the plus testing error is at most the plus repair failure. For any decision event *A* and transcript laws *P*<sub>−</sub>, *P*<sub>+</sub>, the sum of testing errors is

```math
P_-(A^{\mathsf c})+P_+(A)
=1-(P_-(A)-P_+(A))
\geq 1-\mathrm{TV}(P_-,P_+),
```

where total variation is the supremum of the absolute difference on measurable events. The larger repair failure is at least half this sum.

Predrawing *N* coins is legitimate even if the algorithm actually stops earlier: unused coins are discarded by the same postprocessing rule under both alternatives. Common randomization and measurable postprocessing cannot increase total variation. For probability densities *p*, *s* with respect to a common dominating measure, write their affinity as $`F=\int\sqrt{ps}`$. Cauchy–Schwarz gives

```math
\mathrm{TV}(P,S)
=\frac12\int|\sqrt p-\sqrt s|(\sqrt p+\sqrt s)
\leq\sqrt{1-F^2}.
```

The one-coin affinity for the symmetric alternatives is $`\sqrt{1-4\epsilon^2}`$. Independence multiplies affinities, so $`F_N^2=(1-4\epsilon^2)^N`$. This proves the first line of (28), including *N* = 0. For 0 ≤ *u* ≤ 1, $`1-\sqrt{1-u}\geq u/2`$ gives the second bound. Finally,

```math
-\log(1-4\epsilon^2)
\leq\frac{4\epsilon^2}{1-4\epsilon^2}
\leq\frac{16}{3}\epsilon^2,
```

which gives the exponential bound and (29). ∎

The first expression in (28) is an exact formula for a universal **lower bound**, not an assertion that it is the optimal testing risk. The finite Bernoulli experiment's actual optimal testing risk can be obtained from its binomial probabilities, including exact rational arithmetic for rational parameters; no new numerical experiment is asserted here. The alternatives vary with *ε*. This is a local minimax result, not a pointwise rate for every fixed standard or a general empirical law of cognition.

The testing reduction includes private randomization of arbitrary
cardinality. On each finite word $`w`$, let $`K_w`$ be one probability
law on real repair outputs, shared by both standards. The probability
of accepting the minus hypothesis is then
$`K_w(G_{\alpha_-,\epsilon})\in[0,1]`$. Applying the finite testing
bound to these acceptance probabilities and integrating the failure
events gives the same repair lower bound. No finite list of random
seeds is required. A parameter-dependent output kernel would instead
give the algorithm information absent from the experiment.

The initial formal source [46] treats those real-valued randomized
tests on the finite word space and proves the bound by one quarter of the squared affinity for $`0\le\epsilon\le1/2`$. The affinity calculation
and $`1-\sqrt{1-u}\ge u/2`$ remain valid on that wider interval.
Its literal repair bridge uses $`0\lt{}\epsilon\le1/4`$, the same
output law $`K_w`$ under both standards, and measurable acceptance
sets. Allowing every real repair output strengthens the obstruction
relative to restricting outputs to $`[0,1]`$; it does not provide a
positive coherent-output construction. The square-root and
exponential refinements proved above remain ordinary mathematics
in the historical audit's division of formal and informal results.

Copies do not increase the sample count. If *k* records are functions of *N* original fresh outcomes and independent randomness, they remain a postprocessing of the same experiment, so (28) counts *N*, not *k*. A provenance label alone establishes neither authenticity nor independence. Additional conditionally informative observations must be evaluated using their actual conditional law.

**Conditional information in acquired feedback.** The integration probe
[45] also points to the adaptive version of the copied-record distinction.
It has a precise finite-horizon form. Consider two candidate standards
and $`n`$ acquisition stages. The initial information has the same
law under both. Given the complete acquired history $`h`$, the
action-choice kernel is shared. The acquired feedback, including any
informative provenance field, has conditional laws
$`K_0(\,\cdot\,\mid h,a)`$ and $`K_1(\,\cdot\,\mid h,a)`$.
Suppose these laws are mutually absolutely continuous and their
likelihood ratios have a jointly measurable version
$`r(y\mid h,a)=dK_0/dK_1`$. Standard Borel histories with the stated
measurable kernels provide the usual setting; an unmodeled side
channel is additional information.

Induction through the successive conditional kernels gives the
likelihood ratio of the complete acquired transcript:

```math
\frac{dP_0^{H_n}}{dP_1^{H_n}}
 =\prod_{t=0}^{n-1}r(Y_t\mid H_t,A_t).
```

The common initial and action-choice factors cancel. Taking the
logarithm, integrating under the first law, and conditioning each
summand on its acquired history and chosen action gives

```math
D(P_0^{H_n}\Vert P_1^{H_n})
 =\sum_{t=0}^{n-1}
    \mathbb E_0
    D\!\left(K_0(\,\cdot\,\mid H_t,A_t)
       \Vert K_1(\,\cdot\,\mid H_t,A_t)\right).
```

The identity is valid as an extended nonnegative entropy. For each
conditional ratio, its negative log part under the first law is
bounded in integral by
$`\int_{\{r\lt{}1\}}-r\log r\,dK_1\le1/e`$.
Thus a finite sum introduces no undefined cancellation even if a
positive part has infinite expectation. This supplies the elementary
justification for the logarithm and conditional-expectation argument.

A deterministic copy of an already acquired record has the same
conditional point law under both standards and contributes zero to
this sum. A shared random formatting or copying rule likewise has
zero conditional divergence. A genuinely additional sensor
observation is governed by its actual conditional law; matching
one-time marginals does not establish freshness or independence.
This identity describes the full transcript experiment. It does not
assign an independent-sample interpretation to an arbitrary adaptive
channel, authenticate provenance, or replace the stipulated Bernoulli
experiment in (28).

#### Positive correction when acquiring information preserves the target

There is a matching order of growth for finite-confidence repair away from the degenerate endpoint standards. Fix 0 < *a* < 1/2, suppose $`\alpha\in[a,1-a]`$, and define *A* = *a*(1−*a*) and *c* = *A*/4. From *n* independent Bernoulli(*α*) observations, form the sample mean and clip it to [*a*,1−*a*], giving $`\widetilde\alpha`$. Return $`q=1/2+\epsilon\widetilde\alpha`$, which is coherent.

On $`|\widetilde\alpha-\alpha|\leq c\epsilon`$, set *d* = *q*−*r*<sub>α</sub>. Then $`|d|\leq c\epsilon^2`$. Equation (26), with $`|r_\alpha-i|\leq1`$, shows that the improvement at either truth vertex is at least

```math
\begin{aligned}
D_\alpha-2|d|-d^2
&\geq \epsilon^2(A-2c-c^2\epsilon^2)\\
&\geq \epsilon^2(A/2-A^2/256)>0.
\end{aligned} \quad\text{(30)}\quad
```

The causal source audit [47] also records the corresponding pointwise
sufficient tolerance. At one fixed interior standard, put
$`k=\alpha(1-\alpha)`$. If
$`|\widehat\alpha-\alpha|\le k\epsilon/4`$, then
$`d=\epsilon(\widehat\alpha-\alpha)`$ satisfies
$`|d|\le k\epsilon^2/4`$. The same two loss comparisons give improvement
at each vertex of at least
$`\epsilon^2(k/2-k^2/256)>0`$.
Also $`|\widehat\alpha-\alpha|\le\min(\alpha,1-\alpha)/16`$,
so the estimate is interior and the issued output is coherent.
The uniform constant $`A=a(1-a)`$ used in (30) makes this condition
available without knowing the exact interior standard. Neither
sufficient bound is the necessary decoder radius (27).

Clipping cannot increase error when the true parameter is in the clipping interval. The Bernoulli concentration bound therefore gives

```math
P_\alpha\{\text{repair fails to improve both states strictly}\}
\leq 2e^{-2nc^2\epsilon^2}. \quad\text{(31)}\quad
```

For completeness, this bound does not depend on an unproved normal approximation. For one Bernoulli variable *X*, the log moment-generating function $`K(\lambda)=\log\mathbb E e^{\lambda(X-\alpha)}`$ has $`K(0)=K'(0)=0`$ and second derivative equal to a tilted Bernoulli variance, at most 1/4. Hence $`K(\lambda)\leq\lambda^2/8`$ for either sign of *λ*. Independence and the exponential Markov inequality, optimized at $`\lambda=4u`$, give $`P\{\overline X-\alpha\geq u\}\leq e^{-2nu^2}`$; applying the same argument to the lower tail proves (31). This is the bounded-sum concentration argument associated with Hoeffding [34].

**Proposition 21 — Eventual strict correction with target-preserving samples.** Let the disturbance sequence $`0<\epsilon_t\leq1/4`$ be deterministic, and choose $`0<\delta_t<1`$ with $`\sum_t\delta_t<\infty`$. At opportunity *t*, use at least

```math
n_t=\max_{0\leq s\leq t}
\left\lceil\frac{\log(2/\delta_s)}{2c^2\epsilon_s^2}\right\rceil \quad\text{(32)}\quad
```

fresh observations from a common growing sample, and apply the preceding estimator. If these observations can be obtained through licensed actions that preserve the specified target, almost surely all sufficiently late issued repairs strictly improve both truth states.

Indeed, (31) bounds failure at opportunity *t* by *δ*<sub>t</sub>. For every *T*, the probability of any failure after *T* is at most $`\sum_{t\geq T}\delta_t`$, which tends to zero. Thus only finitely many failures occur almost surely. Reusing a growing sample makes failures at different opportunities dependent; the summable union bound, or first Borel–Cantelli lemma, needs no independence between those failure events. ∎

The availability and target-preservation premises matter. Equation (32) does not make harmful exploration harmless or grant access to a sensor. It concerns the correctness of issued actions at the declared opportunities. If every recurring disturbance itself counts as a bad physical state, infinitely many disturbances already prevent eventual uninterrupted physical coherence. Sampling and interstage latency must likewise be classified by the actual target contract.

#### A shared feedback controller with literal score targets

The preceding estimator assumes that the required observations can be acquired through licensed actions. A concrete two-standard experiment connects that information contract to an actual sequence of repairs [43–44]. It specializes the common-history controller in [Collective Inquiry, §7.11](collective-inquiry-and-strategic-coordination.md#711-controlled-observations-and-eventual-correctness) to the same quadratic score used above. The standard, action target and observation law have explicit, separate roles.

Fix one disturbance $`0\lt{}\epsilon\leq1/4`$ for the **entire run**, and let the two possible standards be

```math
\alpha_0=\frac12-\epsilon,
\qquad \alpha_1=\frac12+\epsilon.
```

The true index $`\theta\in\{0,1\}`$ is unknown to the controller. Action $`a\in\{0,1\}`$ issues the coherent forecast

```math
c_a=(q_a,1-q_a),
\qquad q_a=\frac12+\alpha_a\epsilon.
```

Its target is the actual pair of inequalities

```math
L_{\alpha_\theta}(c_a,v_i)
\leq L_{\alpha_\theta}(b_\epsilon,v_i)
\quad(i=0,1),
```

called `BinaryGood` in the predecessor. Coherence follows from the displayed bounds on $`\epsilon`$ and $`\alpha_a`$. When $`a=\theta`$, equation (26) gives the strictly positive improvement $`\alpha_\theta(1-\alpha_\theta)\epsilon^2`$ at both truth vertices. When $`a\ne\theta`$, the distance between the issued center and the correct center is $`2\epsilon^2`$, exceeding the necessary $`\epsilon^2/2`$ bound in Lemma 19. Consequently

```math
\operatorname{BinaryGood}(\theta,a)
\quad\Longleftrightarrow\quad a=\theta.
```

Thus the action target is derived from the loss. It is not an extra declaration that two unrelated labels count as good. At $`\epsilon=0`$ the centers coincide and both labels are accepted; the strict positivity hypothesis is necessary for this identification.

After each action, the controller receives a fresh Boolean observation with Bernoulli($`\alpha_\theta`$) law. Both actions are permitted, and this law is the same for either chosen action. In particular the eventual correct action continues to provide distinguishing information. The coupling between the sensor parameter and the scoring standard, freshness of the observations, and permission to use the actions are premises of this mathematical experiment. Frequencies alone do not authenticate them in an application.

**The common controller and its generated history.** One realization uses the normalized independent product of Bernoulli($`\alpha_\theta`$) variables indexed by action and sample number. On the next use of action $`a`$, consume its first unused stack entry. The history at time $`t`$ contains exactly the $`t`$ acquired action/observation pairs; the sum of the two stack counts is $`t`$. Given a finite history, a fixed parameter-independent tie rule chooses a maximizer of

```math
\Lambda_t(j)
=\prod_{s\lt{}t}
  \alpha_j^{Y_s}(1-\alpha_j)^{1-Y_s},
\qquad j\in\{0,1\},
```

and issues action $`a_t=j`$. At time zero the empty products are one, so the fixed tie rule supplies the initial action. The true $`\theta`$ indexes the probability law used to assess the policy; it is not an input to this decision rule.

Induction on the acquired history establishes both nonanticipation and its law. The next choice is a function of the recorded prefix. Altering an unacquired stack entry cannot change that choice. The chosen next coordinate is fresh and independent of the acquired coordinates, with the stipulated Bernoulli law. Therefore every consistent length-$`t`$ action/observation history has the product probability specified by the controller and observation kernels. Because those kernels are action-independent here, the acquired observations themselves have the ordinary independent Bernoulli product law. This connects the policy to its generated observations rather than assuming that a theorem about a different path law transfers to it.

Each candidate support is the singleton containing its matching repair. A support block is therefore one repair action in this example. The completed-block clock and the issued-repair clock coincide. In a model with several physical actions per block, that identification would require the separate queue and clock argument given in Collective Inquiry; no such multi-action or continuous-time claim is being imported here.

**Eventual repair and its ordinary expected-error bound.** The common controller eventually issues only `BinaryGood` repairs almost surely under either true standard. A direct affinity argument also bounds its expected number of wrong repairs in this specified model. Put

```math
\rho
=\sqrt{\alpha_0\alpha_1}
 +\sqrt{(1-\alpha_0)(1-\alpha_1)}
=\sqrt{1-4\epsilon^2}\lt{}1.
```

Under true index $`\theta`$, a wrong choice at time $`t`$ requires $`\Lambda_t(1-\theta)\geq\Lambda_t(\theta)`$, regardless of how ties are resolved. All likelihood factors are positive. Markov's inequality applied to the square root of their ratio, followed by the generated product law, gives

```math
\begin{aligned}
P_\theta(a_t\ne\theta)
&\leq \mathbb E_\theta
   \sqrt{\frac{\Lambda_t(1-\theta)}{\Lambda_t(\theta)}}
=\rho^t,\\
\mathbb E_\theta\sum_{t\geq0}\mathbf 1\{a_t\ne\theta\}
&\leq \sum_{t\geq0}\rho^t
=\frac1{1-\rho}
=\frac{1+\sqrt{1-4\epsilon^2}}{4\epsilon^2}
\leq\frac1{2\epsilon^2}.
\end{aligned}
```

The first expectation factors because only fresh acquired observations enter the likelihood. The second line uses monotone convergence for a nonnegative sum. A nonnegative count with finite expectation is finite almost surely, proving the eventual score conclusion. Time zero is included: its error is zero or one for a given true model according to the fixed tie choice, and the bound $`\rho^0=1`$ covers both cases.

This is an ordinary mathematical calculation for the specified common policy and generated law. The predecessor's reported formal endpoint establishes almost-sure eventual repair; its displayed expected-action comparison was not presented as a separately kernel-linked result. The calculation here does not change that historical execution boundary. Likewise the finite-sample lower bound (28) concerns the error of one repair after an observation budget, whereas the last display concerns a cumulative action-error count. Their inverse-square dependence on the fixed separation has a common information source, but the performance quantities and their quantifiers remain different.

**What changes the conclusion.** The source audit isolates the needed premises with substantive countercontrols [44]. If the sensor-to-standard coupling is flipped, the same likelihood rule learns $`1-\theta`$ and eventually issues score-wrong repairs under the intended standard. If both standards instead give the same observation law, the matching singleton actions do not distinguish them; full support by itself supplies no information. Independence is also stronger than correct one-coordinate marginals. Set every stack entry equal to one persistent Bernoulli bit. Each coordinate has the declared marginal, but after any positive number of observations the likelihood rule follows that bit. At $`\epsilon=1/4`$, its eventual error probability is $`1/4`$ under either standard. That infinite constant-tape conclusion is an ordinary calculation; the predecessor's exact-rational controls check finite instances and repeated choices. Its flipped-coupling result has a separately reported compiled-theorem scope.

The audit also rejects source changes that consult the first unused stack entry, reverse the generated sensor's hidden-model index, or collapse both output labels to a single forecast. These affect respectively the acquired-history contract, the sensor/score coupling, and the literal target calculation. Its strictly intermediate finite-error observations concern the tested positive prefix lengths; they do not override the deterministic time-zero tie case.

Within this example $`\epsilon`$ and the two candidate standards remain fixed. Varying $`\epsilon`$ across the family does not describe a drifting true standard or Proposition 21's shrinking within-run disturbance schedule. Early wrong actions are permitted. Almost-sure eventual correctness gives neither correctness on every tape, a deterministic last-error deadline, nor a finite certificate that the last error has occurred. Exact real likelihood comparison defines a measurable mathematical policy; the source's noncomputable definitions supply no extracted executable controller or physical sampler. Rational instances allow exact comparison, but no new implementation or numerical-noise guarantee is supplied here. Sensor authentication, normative authority and application-level action permissions remain independent obligations.


#### Finite harmful probing and eventual exact repair

Now fix a deterministic sequence $`0<\epsilon_t\leq1/4`$ tending to zero. At each round, one shared measurable controller chooses either a **Probe**, which returns a fresh Bernoulli(*α*) result and is target-bad, or **Repair**(*q*), with 0 ≤ *q* ≤ 1. Given the observed history and chosen repair, the subsequent repair-feedback kernel is independent of *α*. Controller randomization is parameter-independent. Histories, actions and kernels are standard Borel; only the permitted observations carry parameter information.

The trace records actual actions and actually received observations, and may include the controller's private seed. It excludes an unused parameter-dependent infinite oracle tail. Distinct infinite Bernoulli-product laws can be mutually singular even when the controller reads no bit; that fact is irrelevant to the information in its actual trace.

Let *E*<sub>α</sub> mean that after some finite random round every action is a good repair. This is one eventual action target. In particular success entails finitely many probes, but the last probe is not presumed to be a stopping time.

**Theorem 22 — Countability of positive eventual success.** For every shared controller in this model, the set

```math
\{\alpha\in(0,1):P_\alpha(E_\alpha)>0\}
```

is at most countable.

**Proof.** Let *F* be the measurable event that only finitely many probes occur, and let *F*<sub>N</sub> be the event of no probe after the deterministic round *N*. Then $`F=\bigcup_NF_N`$. Fix the reference standard 1/2.

For each *N*, the observed prefixes through round *N* have mutually absolutely continuous laws for any two interior standards. At each informative step both Bernoulli probabilities are positive; the controller and other feedback kernels are common. Thus a null prefix event under one law is null under the other, even with adaptive choices and a continuous private seed.

After that fixed prefix, use a killed continuation: an attempted probe is sent to a common cemetery, while repair steps use their common feedback kernels. The event of surviving forever is exactly *F*<sub>N</sub>. Common measurable continuation kernels preserve absolute continuity of prefix measures, so the full trace laws restricted to *F*<sub>N</sub> are mutually absolutely continuous. A countable union gives

```math
P_\alpha|_F\ \ll\ P_{1/2}|_F
\quad\text{and}\quad
P_{1/2}|_F\ \ll\ P_\alpha|_F. \quad\text{(33)}\quad
```

This argument uses deterministic prefix lengths and killed continuations; it does not condition at a random “last probe.”

On a repair round define $`z_t=(q_t-1/2)/\epsilon_t`$ and use any fixed value on probe rounds. By Lemma 19, on *E*<sub>α</sub> the sequence eventually satisfies $`|z_t-\alpha|\leq\epsilon_t/2`$, and hence converges to *α*. Let *Z* be its real limit when it exists and −1 otherwise. The convergence set and this limit are measurable, so

```math
E_\alpha\subseteq F\cap\{Z=\alpha\}. \quad\text{(34)}\quad
```

If the left event has positive *P*<sub>α</sub>-mass, one-way absolute continuity in (33) makes $`P_{1/2}(F\cap\{Z=\alpha\})`$ positive. The pushforward of the finite measure $`P_{1/2}|_F`$ by *Z* has at most countably many positive atoms: for each positive integer *k*, only finitely many disjoint atoms can have mass at least 1/*k*, and their union over *k* contains every positive atom. This proves the theorem. ∎

Three consequences retain their distinct quantifiers. For each controller, Lebesgue-almost every interior standard has **zero**, not merely less than one, probability of eventual correct repair. Every nonatomic prior has prior-averaged success zero, provided the parameter/trace family and success event have the joint measurability needed to form that integral. Finally,

```math
\sup_{\pi}\inf_{\alpha\in(0,1)}
 P_\alpha^\pi(E_\alpha)=0. \quad\text{(35)}\quad
```

The exceptional countable set may depend on the controller *π*. There is no assertion that one fixed parameter defeats every possible controller; a controller supplied that exact parameter can use (26).

#### A common reference is enough

The atom argument uses only one direction of (33). Its general content can be stated independently of the Bernoulli model [35].

**Lemma 23 — Dominated exact readouts.** Let *F* be measurable, *Z* a measurable readout into a parameter space with measurable singletons, and *ν* a common finite measure. If $`\mu_\theta|_F\ll\nu|_F`$ for every parameter and $`E_\theta\subseteq F\cap\{Z=\theta\}`$, then only countably many parameters have $`\mu_\theta(E_\theta)>0`$. The same conclusion holds when *ν* is a countable sum of finite measures.

For a finite reference this is the proof following (34). For the latter case, write $`\nu=\sum_j\nu_j`$ with each component finite. Positive mass of a readout fibre under *ν* entails positive mass under some component. Each component contributes countably many such fibres, so their union is countable. This countable-sum condition is often called *s-finiteness*; it must be established for any proposed component construction. ∎

**A common readout and a finite reference are mathematical premises.**
The generic source theorem [46] does not need the success subsets themselves
to be measurable if their mass is interpreted as outer measure. If
$`E_\theta\subseteq F\cap\{Z=\theta\}`$ has positive outer mass, the containing
measurable fibre must have positive actual mass. Domination then gives
positive reference mass, and the same countability argument applies.
Calling this quantity a probability of success requires a measurable event;
the eventual score events above have that additional property. Likewise,
an arbitrary component representation is not enough: the sum of reference
components must actually be s-finite. An uncountable index in a formal
statement does not remove that explicit requirement.

Two countermodels isolate these conditions. On a one-point probability
space with the same point law for every real parameter, the
parameter-indexed map $`Z_\theta(\omega)=\theta`$ would report exact
identification with probability one for every parameter. There is no
single readout with those values. This is why the readout in Lemma 23 must
be shared, just as the repair policy must be shared.

Alternatively, let the observation itself equal the real parameter, with
actual law $`\delta_\theta`$ and shared readout $`Z(x)=x`$. Real counting
measure dominates every such point law, since its only null set is the
empty set, but it is not s-finite. To prove the failure, each finite
measure has only countably many positive singleton masses; a countable
sum of finite measures therefore does too. Domination of every
$`\delta_\theta`$ would require a positive mass at every real singleton,
which is impossible for such a sum. In particular
$`\delta_\theta`$ is not dominated by Lebesgue measure, which assigns
$`\{\theta\}`$ mass zero. Exact parameter revelation changes the
information contract instead of contradicting the countability theorem.

One-way domination must also be kept separate from equivalence. The two
laws $`\delta_0`$ and $`\delta_1`$ are both dominated by
$`(\delta_0+\delta_1)/2`$ but are mutually singular. One observed symbol
identifies this finite hidden class exactly. This is compatible with a
countable positive-success set, while it defeats the two-model
almost-sure impossibility argument that needs mutual tail absolute
continuity. Actual zero probabilities are therefore allowed by the
common-reference lemma without being allowed by every later use of
two-way transfer.

A useful observation-model condition follows. Suppose informative outputs use one **common countable alphabet** *Y*, and choose a probability *r* with positive mass on every element. An artificial environment can return *r* at each probe, while using the same controller and parameter-independent nonprobe feedback. Whatever the actual parameter-dependent probe kernels, including history dependence and zeros, each finite actual prefix law is absolutely continuous in the required direction with respect to this reference. The killed-continuation proof then gives domination on *F*, and Lemma 23 applies.

The reference need not be a possible true standard. Adaptive real-valued choices of query are allowed when they are actions of the shared controller and all observations, including timing, satisfy the stated kernel contract. Alphabets that are separately countable for different parameters but have uncountable union do not supply a common countable alphabet. An unrecorded parameter-revealing side channel invalidates the model.

More generally the same reasoning works when informative kernels have a common measurable dominating probability kernel, including many continuous noisy channels. A dominating measure alone must be accompanied by the measurable kernel construction needed for the path law. An exact real-valued observation of the parameter is a different case: uncountably many distinct point laws cannot all be dominated by one sigma-finite measure, since that would require uncountably many positive singleton masses. Such a sensor can identify a continuum standard in one query because it deletes the domination premise. Conversely a finite alphabet may reveal a member of a finite class exactly, but cannot create an uncountable positive-success set after only finitely many such queries under the common-reference contract.

#### Domination for an actual causal oracle evaluator

The preceding domination hypothesis is discharged by a concrete evaluator in the sources [36–39]. This is a broader observation model than the independent Bernoulli experiment used for (28). Its result concerns an arbitrary oracle law and does not transfer the Bernoulli sample-cost constants to that law.

Let *S* be a standard Borel state space. A common measurable Boolean function *ask* decides whether the next oracle bit is read. A common transition function *next*, measurable in the state for each fixed bit, maps a state and a bit to a new state; on a nonquery step its bit argument is fixed to false. The initial state contains the private seed. For an infinite binary oracle *ω*, the actual counter *k*<sub>t</sub> starts at zero and the execution is

```math
\begin{aligned}
a_t&=\mathrm{ask}(s_t),\\
u_t&=
 \begin{cases}\omega(k_t),&a_t=1,\\0,&a_t=0,\end{cases}\\
s_{t+1}&=\mathrm{next}(s_t,u_t),
\qquad k_{t+1}=k_t+a_t .
\end{aligned} \quad\text{(36)}\quad
```

All score readouts *q*<sub>t</sub>(*s*<sub>t</sub>) are measurable and parameter-independent. Unlimited autonomous computation between queries is allowed; uncounted reads, a parameter-dependent transition, or an unmodeled informative output are not.

**Theorem 24 — Finite-query trace domination.** Suppose each parameter chooses a joint law *μ*<sub>α</sub> of the seed and oracle whose seed marginal is absolutely continuous with respect to one fixed probability *ρ*. The seed and oracle may be correlated; the actual oracle may be dependent over time, singular or deterministic. The laws of the **actual trace**, restricted to finite-query executions, are all absolutely continuous with respect to the same evaluator driven by a *ρ*-distributed seed and an independent fair binary oracle. Therefore an eventual repair event that decodes the parameter, as in (34), has positive mass for at most countably many parameters.

**Proof.** First prove a deterministic locality statement. If one run makes at most *N* queries, any oracle with the same first *N* bits and the same seed gives the same entire run. Induct on time, carrying equality of state and counter. On a nonquery step both transitions are the same. On a query step the counter in the bounded run is strictly less than *N*, so the common prefix supplies the same bit. The second run's boundedness follows from equality; it is not a second assumption.

For a seed *s* and length-*N* word *w*, execute its extension by zeros. Let $`B_N(s,w)`$ say that this execution never asks beyond the *N* available bits. Locality in either direction shows that this event and the full trace on this event are the same for **every** infinite extension of *w*. Both are measurable: counter-boundedness is a countable intersection of measurable finite-time events, and each finite stage of the zero-extended run is measurable. Thus restriction to the event of at most *N* queries factors through a measurable function of (*s*,*w*).

Let $`\widetilde\mu_{\alpha,N}`$ be the actual joint law of the seed and those first *N* bits, and let *u*<sub>N</sub> be the uniform law on the finite word set. Then

```math
\widetilde\mu_{\alpha,N}\ll\rho\otimes u_N. \quad\text{(37)}\quad
```

To see this without an independence assumption, a set null under the product reference has a *ρ*-null seed section for every word, since every word has positive reference mass. Each actual section has zero mass because the actual seed marginal is dominated by *ρ*. Taking the finite union proves (37). The same reasoning works for a countable word alphabet with a full-support reference.

Restrict (37) to *B*<sub>N</sub> and push it through the measurable trace function. Under the reference product, this is exactly the trace law of the evaluator with a *ρ* seed and independent fair infinite oracle, restricted to at most *N* queries. The reference is the **same** law for all *N*. Countable union now proves domination on the finite-query event.

Finally, the nondecreasing integer counter is bounded exactly when only finitely many increments occur, which is exactly eventual absence of queries. Combining this with eventual goodness makes the target “eventually no query and every output good” a single tail event. Lemma 19 supplies the exact limiting readout for shrinking disturbances, and Lemma 23 proves the conclusion. ∎

This proof establishes domination of observed executions on the finite-query event. It makes no claim that the unused infinite actual oracle law is dominated by the infinite fair-coin law. Nor does an artificial reference sensor provide evidence that a real source is authentic. Probability language requires normalized input laws. The underlying domination and positive-mass argument can be formulated for more general measures under the same marginal domination; the corresponding formal endpoints have their own explicit premises, recorded in §11.

The boundary cases in the causal audit [47] make the reference construction
concrete. For $`N=0`$, the finite-word space has one empty word of reference
mass one, and the entire no-query execution is a function of its initial
state. Two different deterministic unused oracle tapes therefore give the
same trace from that state. For an infinite unused Bernoulli tape, the
sample-mean limit is instead the tape's parameter almost surely; the
events of different limits separate the raw laws. Keeping that tape in
the observed object would assert domination of information the evaluator
never acquired.

Common marginal domination is equally substantive. If the initial state
is set to the true parameter itself, a no-query evaluator can keep that
state and issue $`q_t=1/2+\alpha\epsilon_t`$ forever. Its initial marginals
are the point laws $`\delta_\alpha`$. The preceding singleton argument
shows that a continuum of these marginals admits no common s-finite
dominating measure, and hence no common probability reference of the
kind required in Theorem 24. Dependence between an admissible seed and
its oracle is permitted; parameter information inserted through
inadmissible seed marginals is a different operation.

The final target remains the eventual conjunction of no query and good
output. Boundedness of the integer query counter and eventual absence of
increments are equivalent, including the zero-query case; combining
their eventual index with the eventual-goodness index gives one common
tail. Replacing conjunction by disjunction would accept a permanently
bad no-query policy. Similarly, reading an unused bit, failing to count a
query, or using a degenerate reference that gives some finite words mass
zero removes a premise of the locality or domination proof. The audit's
rejected source mutations test these particular interfaces; they are not
positive proofs of the altered statements.

#### Approximate scores and the scale at which the obstruction changes

Allow nonnegative tolerance *η*<sub>t</sub> in **each** truth-state comparison:

```math
L_\alpha(c_t,v_i)\leq L_\alpha(b_{\epsilon_t},v_i)+\eta_t
\quad(i=0,1). \quad\text{(38)}\quad
```

The proof of Lemma 19 with *D*<sub>α</sub>+*η* in place of *D*<sub>α</sub> yields

```math
\left|\frac{q_t-1/2}{\epsilon_t}-\alpha\right|
\leq \frac{\epsilon_t}{2}+\frac{2\eta_t}{\epsilon_t}. \quad\text{(39)}\quad
```

**Corollary 25 — Sublinear tolerance retains the barrier.** If $`\epsilon_t\to0`$ and $`\eta_t/\epsilon_t\to0`$, eventual satisfaction of (38) still decodes the standard. Thus Theorem 22, or the broader common-reference and causal-evaluator conclusions, holds with eventual approximate goodness in place of exact goodness.

The relative scale cannot be dropped [40]. The constant coherent output *q* = 1/2, without any query, satisfies (38) for every $`\alpha\in[0,1]`$ when *η* = *ε* ≥ 0. At the two vertices its excess losses are respectively $`-\alpha\epsilon-\alpha\epsilon^2`$ and $`\alpha\epsilon-\alpha\epsilon^2`$, each at most *ε*. Hence vanishing absolute tolerance alone does not retain the obstruction. This establishes an order-of-magnitude separation between the sublinear regime and a sufficient linear tolerance. It does not assert that every positive linear coefficient suffices or determine an exact minimax coefficient for arbitrary standard families.

#### Sharpness and the finite-class contrast

**Proposition 26 — Exact atomic success.** Draw one guess *g* from a probability law *ρ* supported on [0,1], never query, leave the guess unchanged, and issue $`q_t=1/2+g\epsilon_t`$. In the actual evaluator (36), for each true $`\alpha\in[0,1]`$,

```math
E_\alpha=\{g=\alpha\},
\qquad P_\alpha(E_\alpha)=\rho(\{\alpha\}). \quad\text{(40)}\quad
```

If the guess is correct, (26) proves goodness at every round. If eventual goodness holds, (27) forces $`|g-\alpha|\leq\epsilon_t/2`$ eventually and hence *g* = *α*. This proves both identities. The output is coherent because the guess lies in [0,1] and *ε* ≤ 1/4. Arbitrary correlation with the unused oracle changes nothing. Strict improvement holds for a correct interior guess; the endpoint conclusion is weak goodness. ∎

For any specified nonempty finite or countable set $`S\subseteq[0,1]`$, assign a positive atom to each member, with total mass one. The resulting controller has positive eventual success **exactly** on *S*. An enumeration and normalized positive weights give the usual countable construction; the empty exceptional set is realized by always querying. This is an ideal measurable construction. Effective implementation additionally needs an effective sampling representation and sufficient computability and precision for the chosen constants. A finite rational candidate set admits a direct effective version; neither an arbitrary noncomputable set nor a new software implementation is supplied here. The formal source proves the evaluator's exact atom formula, not a separate theorem constructing a measure from every countable set [41].

For two distinct known **interior** candidate standards, the contrast is stronger than blind guessing. A finite Bernoulli batch distinguishes them with error at most any prescribed *δ* > 0: compare the sample mean with their midpoint and apply the two one-sided concentration bounds. Then commit to the chosen candidate's exact repair law forever. The finitely many initial harmful probes do not spoil the eventual target. Its success probability is at least 1−*δ* under both standards.

No single controller can have success probability one under both standards in this harmful-probe model. Such success would put probability one on *F* and on one exact readout value under the first standard; mutual absolute continuity on *F* would force that same value almost surely under the other, contradicting its distinct required limit. Thus the finite two-standard **limit-sure** value is one, while an almost-sure policy for both does not exist. These are probabilities of an infinite eventual event. They are distinct from a finite-horizon error guarantee, and from the continuum minimax value zero in (35).

#### Operational and philosophical scope

The obstruction depends on the combination of shrinking disturbance, simultaneous score correctness, finitely many informative acts forced by the target, and a shared information contract. A known standard admits direct repair. Target-preserving informative feedback permits Proposition 21. A fixed nonvanishing disturbance or finitely many opportunities no longer forces exact identification by the output limit; this removes that proof mechanism without promising every alternative task solvable. Sufficiently relaxed tolerance, an exactly parameter-revealing sensor, or an action valid under every standard can likewise change the problem. Parameter-coded private randomness or a hidden norm oracle violates the original shared-controller premise; in the broader evaluator theorem its admissibility must be tested against the common marginal-domination condition.

The model connects latent-parameter identification, metric-sensitive correction, persistent action targets and the distinction between fresh information and copied records. It does not establish that normative truth is statistically inferred from arbitrary frequencies: Bernoulli(*α*) is a stipulated informative channel for a stipulated loss parameter. An operationally identified metric supplies neither source authority nor an intellectual, personal, necessary or ultimate bearer of that metric. The mathematical conclusion states what an indefinite reliable-repair promise must supply in this model, and which changes of information or performance contract avoid its particular obstruction.



### 9.8 Literal repair with a fixed disturbance: counts, priors and reporting clocks

The shrinking target in §9.7 can force an output to identify its hidden standard exactly. A fixed positive disturbance gives a different statistical problem: an interval of estimates can repair a given interior standard. One empirical policy then makes only finitely many mistakes at each fixed model, while its expected count necessarily becomes unbounded near the endpoints. Averaging over an unknown but fixed standard introduces a further distinction. Under a Beta prior, the endpoint powers decide whether a finite expected lifetime count is possible; changing the declared reporting clock changes that threshold. The same rate argument extends to a precisely specified class of nonconjugate priors. These conclusions concern the literal repair event, not the magnitude of the excess loss. [48–54]

#### The experiment and the accepted intervals

Fix $`0<\varepsilon\leq1/4`$. Draw or fix one $`\alpha\in[0,1]`$ and retain it throughout the experiment. Conditional on α, receipts are independent Bernoulli(α) bits. At index n, including n=0, a common measurable policy issues a report after exactly n receipts. Its report is a function $`Q_n(R,w)`$ of the acquired word w and a private seed R with one law independent of both the parameter and the randomness generating the receipts. In a prior experiment the full law is $`\rho(dR)\mu(d\alpha)P_\alpha(dy)`$. Marginal independence of R from α alone would not establish the conditional arguments below. Reports neither alter the passive receipts nor receive an additional correctness label. There is no abstention or extra uncounted acquisition.

The two all-truth excesses are

```math
D_0(\alpha,\varepsilon,q)=q^2-\frac14-\alpha\varepsilon(1+\varepsilon),
\qquad
D_1(\alpha,\varepsilon,q)=(1-q)^2-\frac14+\alpha\varepsilon(1-\varepsilon).
```

A weak repair is coherent and has both excesses nonpositive; equality is accepted. A strict repair has both negative. Write f(α,q) for the weak-failure indicator, counting an incoherent output as a failure if the interface permits it, and put

```math
C_\alpha=\mathbb E_\alpha\sum_{n\geq0} f(\alpha,Q_n(R,Y_1\cdots Y_n)).
```

This is an extended nonnegative expected **number** of incorrect reports. It is neither accumulated excess magnitude nor an expected last-error time. [48–49]

At α=0 the unique weak repair is $`q_0=1/2`$; at α=1 it is $`q_1=1/2+\varepsilon`$. Both facts follow by intersecting the two square inequalities with coherence. Strict endpoint repair is impossible. At an interior α, the report $`q_\alpha=1/2+\varepsilon\alpha`$ has both excesses equal to $`-\varepsilon^2\alpha(1-\alpha)<0`$. The endpoint reports instead obey

```math
D_1(\alpha,\varepsilon,q_0)=\alpha\varepsilon(1-\varepsilon)>0
\quad(\alpha>0),
\qquad
D_0(\alpha,\varepsilon,q_1)=(1-\alpha)\varepsilon(1+\varepsilon)>0
\quad(\alpha<1).
```

Any report accepted for at least one parameter lies in $`[1/2,1/2+\varepsilon]`$. For q in that interval, acceptance is exactly α in $`[\ell(q),u(q)]`$, where

```math
\ell(q)=\frac{q^2-1/4}{\varepsilon(1+\varepsilon)},
\qquad
u(q)=\frac{1/4-(1-q)^2}{\varepsilon(1-\varepsilon)}.
```

Direct substitution gives $`0\leq\ell\leq u\leq1`$; clipping is unnecessary for these nonempty intervals. Writing $`q=1/2+x`$ shows

```math
u\leq R_0\ell,\qquad R_0=\frac{1+\varepsilon}{1-\varepsilon}>1.
```

For the reflected parameter $`\beta=1-\alpha`$, write $`q=1/2+\varepsilon-z`$. The accepted β interval has endpoints

```math
\ell_1=\frac{z(1-2\varepsilon+z)}{\varepsilon(1-\varepsilon)},
\quad
u_1=\frac{z(1+2\varepsilon-z)}{\varepsilon(1+\varepsilon)},
\quad
u_1\leq R_1\ell_1,
\quad
R_1=\frac{(1+2\varepsilon)(1-\varepsilon)}{(1-2\varepsilon)(1+\varepsilon)}>1.
```

Thus one accepted report covers only a bounded multiplicative interval at either endpoint. An endpoint report accepts only that endpoint. These are prior-free geometric facts. At ε=0 the constant report 1/2 repairs every parameter, so the positive-disturbance hypothesis cannot be dropped. [50–51,54]

#### Pointwise finite expectation and an unavoidable endpoint cost

Take $`q_0=1/2`$ and, after n≥1 receipts, use $`q_n=1/2+\varepsilon h_n`$, where hₙ is their empirical mean. Put $`v=\alpha(1-\alpha)`$. For an interior parameter, deviation $`|h_n-\alpha|\leq v\varepsilon/4`$ gives a coherent strict repair. Indeed, writing $`m=v\varepsilon^2`$ and $`d=\varepsilon(h_n-\alpha)`$, the two excesses are

```math
-m+(1+2\alpha\varepsilon)d+d^2,
\qquad
-m-(1-2\alpha\varepsilon)d+d^2.
```

Here $`|d|\leq m/4`$, $`d^2\leq|d|`$ and both linear coefficients have absolute value at most 2, so each excess is at most $`-m/4`$.

For centered independent Bernoulli variables, expansion of the fourth moment leaves only fourfold and paired indices. It gives

```math
\mathbb E(h_n-\alpha)^4
=\frac{nv(1-3v)+3n(n-1)v^2}{n^4}
\leq\frac{v}{n^3}+\frac{3v^2}{n^2}.
```

Markov's inequality and the repair radius bound the post-acquisition failure probability by

```math
\min\left(1,\frac{A}{n^3}+\frac{B}{n^2}\right),
\qquad A=\frac{256}{v^3\varepsilon^4},\quad B=\frac{768}{v^2\varepsilon^4}.
```

Let $`K=1/(v\varepsilon^2)\geq64`$ and $`N=\lceil28K\rceil`$. Bounding the first N terms by one and the decreasing tails by integrals gives

```math
\sum_{n\geq1}\Pr_\alpha(\text{failure at }n)
\leq N+\frac{A}{2N^2}+\frac{B}{N}
\leq\left(28+\frac1{64}+\frac1{98}+\frac{192}{7}\right)K<56K.
```

The initial report contributes at most one. Consequently

```math
C_\alpha\leq1+\frac{56}{\alpha(1-\alpha)\varepsilon^2}
\qquad(0<\alpha<1).
```

Tonelli justifies summing these probabilities without independence of the errors across reporting times. Finite expectation implies almost-sure eventual weak repair, and the same radius argument gives eventual strict repair in the interior. For this clock the exact endpoint weak costs are $`(C_0,C_1)=(0,1)`$. The displayed interior bound is uniform on every compact interval $`[\eta,1-\eta]`$ with η>0. This is the retained empirical learner and sharper ordinary bound, not a new learner inferred from a simulation. [48–49]

The divergence of the bound near an endpoint is not merely an artifact of that learner. Suppose first that an arbitrary common policy eventually repairs α=0 almost surely. On the counterfactual all-zero history let

```math
E_N=\{r:Q_n(r,0^n)=q_0\text{ for every }n\geq N\}.
```

Endpoint uniqueness implies $`\rho(E_N)\uparrow1`$. These are measurable seed events, not observable stopping events. For each n≥N, the report on E_N fails at every α>0 whenever the acquired prefix is all zeros. Independence gives

```math
C_\alpha\geq\rho(E_N)\sum_{n\geq N}(1-\alpha)^n
=\rho(E_N)\frac{(1-\alpha)^N}{\alpha}.
```

Taking α down to zero with N fixed, then increasing N, proves

```math
\liminf_{\alpha\downarrow0}\alpha C_\alpha\geq1.
```

The corresponding endpoint-one correctness premise gives $`\liminf_{\alpha\uparrow1}(1-\alpha)C_\alpha\geq1`$. No finite expected settling time at an endpoint is assumed.

A related finite-parameter inequality requires only a finite endpoint cost. Put $`p_n=\rho(Q_n(R,0^n)=q_0)`$. Endpoint uniqueness gives $`C_0=\sum_n(1-p_n)`$, while causality gives $`C_\alpha\geq\sum_n(1-\alpha)^np_n`$. If C₀ is finite, the subtracted series is finite and

```math
C_\alpha\geq\frac1\alpha-C_0,
\qquad C_\alpha+C_0\geq\frac1\alpha.
```

If C₀ is infinite the latter extended sum inequality already holds; no infinity-minus-infinity subtraction is used. Reflection gives $`C_\alpha+C_1\geq1/(1-\alpha)`$.

For an arbitrary fixed policy, α↦Cα is lower semicontinuous. For a fixed report, failure is a strict positive violation of a continuous polynomial, or parameter-independent incoherence. Its indicator is therefore lower semicontinuous. For each finite word w, the weight $`\alpha^{\#1(w)}(1-\alpha)^{\#0(w)}`$ is continuous and nonnegative, so its product with that indicator remains lower semicontinuous, including at zero word mass. Fatou on the common seed space, finite word/horizon sums and then the supremum over finite horizons yield

```math
C_a\leq\liminf_{\alpha\to a}C_\alpha.
```

If C₀ is infinite, this inequality forces interior costs to diverge near zero. If C₀ is finite, the paired trade-off does. The symmetric argument applies at one. **Every common always-issued policy therefore has unscaled expected cost tending to infinity at both endpoints**, even without endpoint correctness. This excludes a uniform finite bound on any parameter family accumulating at an excluded endpoint: its policy table still defines the hypothetical endpoint experiment. The scaled constants above retain their endpoint-correctness premises. [48–49]

#### Two minimax pairs and the exact initial report

The initial report is part of the experiment, so two commonly conflated examples must be kept separate.

| Models | Policy | Expected lifetime failures |
|---|---|---|
| $`\{0,1/2\}`$ | Initially report $`1/2+\varepsilon/2`$; thereafter use that report after at least one receipt equal to 1 has been observed and use $`q_0`$ otherwise | $`(1,1)`$ |
| $`\{0,1/2\}`$ | The same post-acquisition rule, initially reporting $`q_0`$ | $`(0,2)`$ |
| $`\{0,1\}`$ | Initially randomize fairly between $`q_0,q_1`$; use the exact endpoint report after the first receipt | $`(1/2,1/2)`$ |

For the first pair, $`C_0+C_{1/2}\geq2`$ gives minimax cost at least 1 even for arbitrary independent-seed real-report policies. The first policy attains it: the zero source has just the initial error; the half source has an error at n≥1 exactly on an all-zero prefix, and $`\sum_{n\geq1}2^{-n}=1`$. Changing only the initial report to q₀ removes the zero-source error but adds a half-source error. For the endpoint pair, no initial report repairs both models, so the two initial failure probabilities sum to at least 1. The fair choice attains randomized minimax 1/2. A deterministic initial report has minimax 1 instead. These are different model pairs and different policies. [48–49]

The recovered endpoint-code review separately reports a 59-byte incremental program and a 105-byte prefix program with stated cache, receipt and rational-readout adapters and ordinary pair $`(0,2)`$. Their statement-transition meter excludes arithmetic, acquisition, codecs, host time and bit complexity. The mathematical initial-report modification above is not a claim that those exact programs implement the minimax variant, nor does their recovered source/execution identity restore the missing formal closure. [57]

#### A sharp Beta-prior lifetime boundary

Now draw α once from Beta(a,b), with a,b>0. Its density is $`\alpha^{a-1}(1-\alpha)^{b-1}/B(a,b)`$. Conditional receipts are iid, but the mixed process is exchangeable and generally not an iid fair coin. For example, the uniform-prior probability of two zeros is 1/3, not 1/4. Let $`C_{a,b}=\int C_\alpha\,\mathrm{Beta}(a,b)(d\alpha)`$.

**Theorem (finite Beta-averaged budget).** There exists a common always-issued policy with $`C_{a,b}<\infty`$ if and only if a>1 and b>1. If either shape is at most one, every such policy has infinite expected lifetime literal failures. The necessary direction makes no endpoint-correctness assumption. [50–51]

After n≥1 zero receipts the posterior is Beta(a,b+n). If F is its CDF, then for R≥1 and z∈[0,1], substitution gives

```math
F(z/R)=R^{-a}K_n\int_0^z x^{a-1}(1-x/R)^{b+n-1}\,dx
\geq R^{-a}F(z),
```

because b+n−1≥0. The positive normalizing constant Kₙ is finite even for an integrable endpoint singularity. Since $`\ell\geq u/R_0`$, an accepted interval has posterior mass at most $`1-R_0^{-a}`$. Every issued report therefore fails with conditional probability at least $`R_0^{-a}`$ after that prefix. Conditioning on the fixed acquired word leaves the seed independent of α, so the same bound holds after averaging arbitrary private randomization. Reflection gives lower failure probability $`R_1^{-b}`$ after n ones.

The two extreme-prefix events are disjoint for n≥1, with unconditional probabilities

```math
M_0(n)=\frac{B(a,b+n)}{B(a,b)}=\mathbb E(1-\alpha)^n,
\qquad
M_1(n)=\frac{B(a+n,b)}{B(a,b)}=\mathbb E\alpha^n.
```

Thus every policy obeys

```math
p_n\geq R_0^{-a}M_0(n)+R_1^{-b}M_1(n).
```

Tonelli and the geometric series give

```math
C_{a,b}\geq
R_0^{-a}\mathbb E\frac{1-\alpha}{\alpha}
+R_1^{-b}\mathbb E\frac{\alpha}{1-\alpha}.
```

The first Beta integral diverges exactly when a≤1, and the second exactly when b≤1. For a,b>1 the displayed finite lower bound is $`R_0^{-a}b/(a-1)+R_1^{-b}a/(b-1)`$. For a=b=1 and ε=1/4, $`R_0^{-1}=3/5`$ and $`R_1^{-1}=5/9`$, giving the exact lower bound $`(52/45)(H_{N+1}-1)`$ over indices 1 through N. The n=0 extreme events coincide and must not be counted twice; the posterior CDF scaling also need not hold there when a complementary exponent is negative.

For sufficiency, integrate the retained empirical bound using

```math
\mathbb E\frac1{\alpha(1-\alpha)}
=(a+b-1)\left(\frac1{a-1}+\frac1{b-1}\right).
```

It gives

```math
C_{a,b}^{\rm emp}\leq1+
\frac{56}{\varepsilon^2}(a+b-1)
\left(\frac1{a-1}+\frac1{b-1}\right)<\infty.
```

This proves both directions. Nevertheless the empirical learner has finitely many failures almost surely under **every** proper Beta prior, since it does so at every fixed interior α and the prior has no endpoint atoms. Almost-sure finite count and finite prior expectation are different statements. Neither implies a bound on the time of the last error. [50–51]

#### Finite-horizon rates and an exact Bayes existence statement

The same experiment admits matching all-policy lower and empirical upper orders. For every n≥1 there are finite c,C>0 depending on a,b,ε, but not the policy or n, such that

```math
p_n(\pi)\geq c(n^{-a}+n^{-b})\quad\text{for every policy }\pi,
\qquad
p_n({\rm emp})\leq C(n^{-a}+n^{-b}).
```

Here the empirical learner needs neither prior shape. For completeness the concentration and integration arguments are given explicitly. At $`q_h=1/2+\varepsilon h`$, for h∈[0,1], the changes from qα in D₀ and D₁ have absolute values at most $`(3/2)\varepsilon|h-\alpha|`$ and $`\varepsilon|h-\alpha|`$. Hence the radius $`r=v\varepsilon/4`$ suffices. For $`X=Y-\alpha`$, $`\mathbb EX=0`$, $`|X|\leq1`$, and $`\mathbb E|X|^k\leq v`$ for every integer k≥2. Using $`k!\geq2\cdot3^{k-2}`$, for 0≤λ<3,

```math
\mathbb E e^{\lambda X}
\leq1+\frac{v\lambda^2}{2(1-\lambda/3)}
\leq\exp\!\left(\frac{v\lambda^2}{2(1-\lambda/3)}\right).
```

The same bound holds for −X. Independence, exponential Markov inequality and $`\lambda=r/(v+r/3)<3`$ yield

```math
\Pr(|h_n-\alpha|\geq r)
\leq2\exp\!\left(-\frac{nr^2}{2(v+r/3)}\right)
\leq2\exp\!\left(-\frac{nv\varepsilon^2}{33}\right).
```

The last inequality follows from $`r^2/[2(v+r/3)]=v\varepsilon^2/[32(1+\varepsilon/12)]`$ and ε≤1/4. This fixed-index estimate can exceed one at small n without invalidating the bound.

Put $`t=\varepsilon^2/66`$ and $`K(s)=\max(1,2^{1-s})`$. On α≤1/2, v≥α/2 and $`(1-\alpha)^{b-1}\leq K(b)`$; reflect the other half. Extending nonnegative integrals to [0,∞) gives

```math
p_n({\rm emp})\leq\frac{2}{B(a,b)}
\left[\frac{K(b)\Gamma(a)}{(tn)^a}
+\frac{K(a)\Gamma(b)}{(tn)^b}\right].
```

For a lower bound put $`k(s)=\min(1,2^{1-s})`$ and restrict M₀(n) to $`0\leq\alpha\leq1/(n+1)`$. On this interval $`(1-\alpha)^{b-1}\geq k(b)`$ and $`(1-\alpha)^n\geq[n/(n+1)]^n\geq e^{-1}`$. Therefore

```math
M_0(n)\geq\frac{e^{-1}k(b)2^{-a}}{aB(a,b)}n^{-a},
\qquad
M_1(n)\geq\frac{e^{-1}k(a)2^{-b}}{bB(a,b)}n^{-b}.
```

Combining these with the posterior lower bound proves the positive constant c without a gamma-ratio limit or asymptotic exchange. Every lower bound holds even for a horizon-dependent policy, while one horizon-independent empirical policy supplies all the upper bounds. [52]

Writing $`H_N(s)=\sum_{n=1}^N n^{-s}`$ and $`m=\min(a,b)`$, the optimal expected count through N is $`\Theta(H_N(a)+H_N(b))`$: it grows as $`\Theta(N^{1-m})`$ for m<1, $`\Theta(\log(N+1))`$ for m=1, and $`\Theta(1)`$ for m>1. If a,b>1, the optimal expected future count over n>N has order $`N^{1-a}+N^{1-b}`$; otherwise every policy has infinite expected tail after every deterministic cutoff. These are unconditional original-prior expectations, not bounds asserted uniformly over every realized posterior.

The empirical policy is optimal **in order**, not necessarily in leading constant or exact risk. An exact Bayes minimizer nevertheless exists in this passive experiment. After a word of length n with k ones, the posterior is Beta(a+k,b+n−k). Its continuous CDF F makes the success function $`F(u(q))-F(\ell(q))`$ continuous on the compact report interval. Choose its least maximizer, which exists because the nonempty maximizer set is compact. There are only countably many finite histories, so this deterministic selection is measurable. Randomization cannot exceed the maximum, and reports cannot affect later receipts. Conditional expectation and Tonelli therefore show that the same policy minimizes every per-index risk, every finite-horizon sum, every prescribed tail and the extended lifetime count. An infinite lifetime minimum can be vacuous; the finite-horizon conclusion remains substantive. This is an ordinary existence result, not a certified numerical argmax algorithm. Approximate maximization does not automatically preserve exact literal correctness. [52]

#### A declared deterministic reporting clock

Suppose instead that evaluated report j sees exactly nⱼ receipts, where (nⱼ) is a fixed deterministic nondecreasing sequence of positive integers. Charge every declared evaluation, including repeated nⱼ. Apply the all-n lower and upper bounds separately to each report. Independence between errors is unnecessary. A finite expected total evaluated-report count is possible exactly when

```math
\sum_j(n_j^{-a}+n_j^{-b})<\infty,
\qquad\text{equivalently}\qquad
\sum_j n_j^{-\min(a,b)}<\infty.
```

The empirical learner witnesses sufficiency; the lower bound excludes every common independently randomized policy when the sum diverges. If $`n_j\asymp j^\gamma`$, the condition is $`\gamma m>1`$. For $`n_j\asymp j^\gamma[\log(j+1)]^p`$ it is γm>1, or γm=1 with pm>1; it fails when γm<1 or at equality with pm≤1. Assume the schedule is eventually positive and nondecreasing; finitely many initial terms do not matter. A geometrically increasing receipt count works for every proper Beta prior. For the uniform prior, the schedule $`j[\log(j+1)]^p`$ works exactly when p>1, whereas linear acquisition cannot give a finite budget. [53]

This trades more acquisitions for fewer evaluated reports. It does not remove the costs of intervening reports if a physical interface still requires their evaluation. A data-dependent acquisition time changes the posterior-history events and needs another proof; fixed-index concentration is not a stopping-time theorem. A bounded schedule repeated infinitely often cannot satisfy the criterion.

#### Endpoint-density robustness, with atoms handled separately

The rate conclusion is not confined to Beta conjugacy. Suppose one fixed prior has the decomposition

```math
\mu=p_0\delta_0+p_1\delta_1
+f_0(\alpha)\mathbf1_{(0,\delta)}\,d\alpha
+f_1(\alpha)\mathbf1_{(1-\delta,1)}\,d\alpha+\nu,
```

where 0<δ<1/2, ν is any finite nonnegative measure supported on [δ,1−δ], the total mass is one, and for some a,b>0 and finite positive constants,

```math
m_0\alpha^{a-1}\leq f_0(\alpha)\leq M_0\alpha^{a-1},
\qquad
m_1(1-\alpha)^{b-1}\leq f_1(\alpha)\leq M_1(1-\alpha)^{b-1}
```

almost everywhere on the respective punctured endpoint neighborhoods. The interior may contain atoms or singular continuous mass, including an affine Cantor measure. There is no additional unspecified singular mass near either endpoint. The constants concern this fixed prior, not a uniform class of priors. [54]

The geometric ingredient is a prior-free missing-mass bound. For s>0, R≥1, t>0 and $`0\leq\ell\leq u\leq R\ell`$,

```math
\int_{(0,t)\setminus[\ell,u]}x^{s-1}\,dx
\geq\frac{R^{-s}t^s}{s}.
```

If u≤t, multiplying the excluded mass by s gives $`\ell^s+t^s-u^s\geq t^s-(1-R^{-s})u^s\geq R^{-s}t^s`$. If u>t and ℓ<t, the excluded interval (0,ℓ) has mass at least $`(t/R)^s/s`$. If ℓ≥t the entire interval is excluded. Empty acceptance sets also satisfy the inequality. The upper complement when u<t is essential: the claim ℓ≥t/R for every report would be false.

Set $`t=\delta/(n+1)`$. On the zero prefix and 0<α<t, the likelihood is at least e⁻¹. Fixing a seed fixes the report, so the lower density envelope and missing-mass lemma give an **unnormalized joint** failure-and-zero-prefix mass at least $`e^{-1}m_0R_0^{-a}t^a/a`$. The same inequality holds for every seed; the product law and Tonelli justify averaging. Reflection gives the one-prefix mass, and disjointness for n≥1 permits addition:

```math
p_n(\pi)\geq c_0n^{-a}+c_1n^{-b},
\quad
c_0=\frac{e^{-1}m_0R_0^{-a}\delta^a}{a2^a},
\quad
c_1=\frac{e^{-1}m_1R_1^{-b}\delta^b}{b2^b}.
```

No conjugate posterior or optimal selector is needed. Endpoint atoms cannot weaken this lower bound, but they invalidate a tempting conditional shortcut. For $`\mu=(99/100)\delta_0+(1/100)\mathrm{Uniform}[0,1]`$, reporting q₀ after n zeros has posterior failure probability

```math
\frac{1/[100(n+1)]}{99/100+1/[100(n+1)]}\longrightarrow0.
```

A positive constant conditional failure bound copied from the Beta posterior lemma would therefore be wrong. The unnormalized tail calculation is what survives. [54]

For the upper bound put $`\kappa=\varepsilon^2/33`$. At α=0 or 1 the empirical learner is exact after the first receipt, so its n≥1 endpoint-atom cost is zero. On (0,δ), $`\alpha(1-\alpha)\geq(1-\delta)\alpha`$, and the concentration estimate integrates to $`2M_0\Gamma(a)[\kappa(1-\delta)n]^{-a}`$. Reflect the other endpoint. If $`w=\nu([\delta,1-\delta])`$ and $`h=\kappa\delta(1-\delta)>0`$, the interior contribution is at most $`2w e^{-hn}`$. Thus

```math
p_n({\rm emp})\leq A_0n^{-a}+A_1n^{-b}+2we^{-hn},
\qquad
A_0=\frac{2M_0\Gamma(a)}{[\kappa(1-\delta)]^a},
\quad
A_1=\frac{2M_1\Gamma(b)}{[\kappa(1-\delta)]^b}.
```

This integrates a uniform pointwise bound against the entire interior measure; no density or finite atomic support is required there. With r=⌈a⌉, $`e^{-hn}\leq r!h^{-r}n^{-r}\leq r!h^{-r}n^{-a}`$ for n≥1, yielding a finite polynomial upper constant for all n.

Consequently the same optimal cumulative orders, finite-budget iff a,b>1, deterministic-cutoff tail orders and deterministic reporting-clock criterion hold. They give an upper rate for the empirical or optimal policy, not for every policy: an always-wrong policy can have risk one. The empirical learner is eventually accepted almost surely under every prior in this class, including those with infinite expected count. Endpoints are exact after one receipt; at each interior α the strong law eventually places hₙ in its positive repair radius. Integrating the probability-one conclusion is legitimate.

Both density envelopes matter. A pure endpoint prior has zero empirical post-acquisition cost and cannot be assigned arbitrary positive lower tail powers. Lower comparability alone cannot control the upper rate: adding a uniform component to a prior with faster endpoint powers preserves those weaker lower bounds but introduces the critical uniform-prior risk. A full-prior inverse-moment slogan is also false in the presence of atoms. For $`\mu=(1/2)\delta_0+(1/2)\mathrm{Beta}(2,2)`$, the interior integral of $`1/[\alpha(1-\alpha)]`$ is 3, while its full extended integral is infinite. The endpoint atom has zero actual post-acquisition error cost. It must not be inserted into a zero-variance upper formula as if the formula's infinite value were an error count. [54]

The density theorem does not cover uncontrolled singular endpoint tails, holes in the positive lower envelope, unbounded slowly varying factors, changing α, informative extra feedback or control-dependent sampling. The Beta continuous-CDF maximizer argument is not imported across atoms; no exact Bayes selector or computable argmax is asserted for this larger class. An α-revealing seed would permit the exact report qα everywhere and defeat the universal lower bound, which is why the independent-information contract is substantive. These statistical guarantees authenticate neither a scoring source nor any normative or metaphysical authority.


### 9.9 Common observations, acquired-history laws and physical action time

The preceding impossibility results use several different comparisons of probability laws. Their directions and their observable objects matter. A reference measure that dominates every model supports a countability argument; a nonzero measure dominated by every model transfers all of their almost-sure requirements to common paths. A construction with the right one-time marginals is still insufficient to realize a causal controller. This section makes those interfaces explicit and connects them to the controlled-restoration proof in [Collective Inquiry, §7.11](collective-inquiry-and-strategic-coordination.md#711-controlled-observations-and-eventual-correctness). The argument uses the public common-observation, necessity, generated-process and physical-clock sources cited below; their execution reports retain their separate historical scopes.

#### A common lower reference and compatible eventual targets

Let $`\nu_\theta`$ be probability laws on one measurable complete-path space $`\Omega`$, and let $`X_t:\Omega\to A`$ be one common measurable sequence of action readouts. Fix measurable target sets $`G_\theta\subseteq A`$. Suppose there is a nonzero measure $`\mu`$ such that


```math
\mu\ll\nu_\theta\quad\text{for every }\theta,
\qquad
\nu_\theta(E_\theta)=1,\qquad
E_\theta=\{\exists N\ \forall t\ge N:\ X_t\in G_\theta\}.
```



**Proposition — Common-path target obstruction.** If the model family is finite, then $`\bigcap_\theta G_\theta\ne\varnothing`$. The same conclusion holds for an arbitrary model family when the action set $`A`$ is finite.

For a finite family, absolute continuity makes every $`E_\theta`$ conull for $`\mu`$. Their finite intersection is conull and nonempty, since $`\mu`$ is nonzero. On a path in that intersection, take the maximum of the finitely many tail cutoffs; any later action belongs to every target. For finite $`A`$ and an arbitrary family, if the total intersection were empty, choose for each $`a\in A`$ one model whose target rejects it. This gives a finite subfamily with empty intersection, contradicting the first case. No uniform cutoff over all paths has been used. [common-observation-review], [common-observation-source]

This is the opposite direction of domination from Lemma 23. There the actual restricted laws are dominated by one upper reference, and disjoint positive-mass readout events give a countability bound. An upper reference alone cannot impose compatible targets: the two Dirac laws at 0 and 1 are both dominated by their mixture, and the common readout $`X_t(\omega)=\omega`$ succeeds forever at the disjoint singleton targets. A zero lower reference would also be vacuous. The common readout is substantive: allowing a different constant action map for each model would replace one controller by a collection of model-informed controllers.

There is a useful compactness extension. Let $`A`$ be a metric space with its Borel sets, let every $`G_\theta`$ be closed, and suppose that for some compact $`K\subseteq A`$ the common action sequence is eventually in $`K`$ almost everywhere for $`\mu`$. For each finite set of models, the preceding finite-intersection argument supplies a point in $`K`$ and all of those targets. The closed subsets $`K\cap G_\theta`$ therefore have the finite intersection property. Compactness gives


```math
K\cap\bigcap_\theta G_\theta\ne\varnothing.
```


This establishes compatible target values, not that the controller ever visits their total intersection. For $`K=[0,1]`$, $`G_n=[0,1/(n+1)]`$ and $`X_t=1/(t+1)`$, every individual target eventually contains the sequence, but the total intersection is $`\{0\}`$ and the sequence never reaches it. Without finite actions or a compact confinement condition, even compatibility can fail: on $`A=\mathbb N`$, take $`G_n=\{a:a\ge n\}`$ and $`X_t=t`$.

The lower-reference assumption concerns complete paths. Consistent references on every finite observation prefix do not suffice. Compare the all-one Dirac sequence with independent fair bits. On each finite prefix, the all-one Dirac law is a nonzero common lower reference, but the complete all-one path has probability zero under the fair law. The controller that outputs 0 until the first observed zero and 1 thereafter succeeds eventually at $`\{0\}`$ in the Dirac model and at $`\{1\}`$ in the fair model. Thus prefix domination must be joined to an appropriate continuation argument before it can support a tail impossibility. This is precisely the role of the killed continuations in Theorem 22 and in the controlled-restoration necessity proof.

#### Recurrence gives a positive event, not an observable last exit

For a finite action set and an infinite issued-action sequence, define its exact recurrent set


```math
U_\infty=\{a:\ \forall N\ \exists t\ge N,\ X_t=a\}.
```


It is nonempty. There are finitely many possible nonempty values $`U`$, and the events $`E_U=\{U_\infty=U\}`$ partition the path space. Under a probability law some $`E_U`$ has positive probability. Every action outside such a $`U`$ occurs only finitely often on $`E_U`$, so


```math
E_U=\bigcup_{N\ge0}F(U,N),\qquad
F(U,N)=E_U\cap\{\forall t\ge N:\ X_t\in U\}.
```


Some deterministic $`N`$ therefore gives a positive-probability event $`F(U,N)`$. Under eventual target success, a positive such cell can be chosen with $`U\subseteq G_\theta`$. [recurrence-review], [recurrence-scope]

The exact recurrent-set condition is needed when concluding that a rival must accept every member of $`U`$. An arbitrary superset may contain actions that are never used. Strict positivity of the chosen cell is also needed for transfer; mere nonnegative probability says nothing. Finiteness of $`A`$ cannot be omitted from this selection: the sequence $`X_t=t`$ uses every natural-number action only once. Finally, $`N`$ is selected from a countable cover after establishing positive probability. It is neither a policy-observable final probe nor a stopping time, and no deterministic bound on all last errors follows.

The substantive next step is an actual-law comparison. In the finite full-support model, a rival agreeing with the source on every action in $`U`$ has equivalent seed-and-prefix laws at each fixed $`N`$ and the same continuation after the process is killed on leaving $`U`$. That transfers positive mass of $`F(U,N)`$. The recurrence argument supplies the event; it does not supply those law identities. The controlled-restoration theorem consequently has one common policy before its universal model quantifier. Model-specific successful policies cannot discharge it. [necessity-proof], [micro-equivalence-review]

#### Binding the causal simulator to the acquired experiment

The causal oracle method gives another route to the same finite-information transfer. Its input representation must first be shown to generate the controller's actual experiment. Take finite action and observation alphabets, a model-independent private seed $`R`$ with law $`\rho`$, and a common measurable causal policy $`\pi(R,h)`$. The action is chosen from the acquired history before the next observation is revealed. With fresh feedback law $`P_{\theta,a}`$, a finite history $`h=((a_s,y_s))_{s<n}`$ has, for every measurable seed set $`D`$, the joint probability


```math
\Pr_\theta(R\in D,H_n=h)
 =\rho(D\cap C_h)\prod_{s\lt{}n}P_{\theta,a_s}(y_s),
\qquad
C_h=\{r:\ \pi(r,h_s)=a_s\text{ for every }s\lt{}n\}.
```


The product uses every acquired observation with its multiplicity. Its proof is induction on the history length, using the conditional law of the fresh observation at the newly selected action. Equality of this formula for every finite history yields equality of the generated infinite-history laws on their product sigma algebra. Equality of one-time marginals would not do so. [seeded-necessity-review], [necessity-proof]

For a comparison between models agreeing on $`U`$, represent feedback from actions in $`U`$ by common independent stacks, indexed by the action and its use count. Represent feedback outside $`U`$ by an independent sequence of rows in $`Y^A`$, drawing a new row at each outside-$`U`$ query and reading only its chosen-action coordinate. The private seed and the inside-$`U`$ stacks have one common law; the outside rows carry the model difference. Different requests consume different coordinates. The current action is fixed before the new outside row is read. Applying the joint-cylinder calculation shows that the simulated acquired histories have the stipulated controlled-feedback law under each model.

It would be incorrect to condition a freshness argument on an enlarged state that already contains future stack values and then call the next coordinate independent of that entire state. The cylinder proof conditions on what the policy has acquired. The common stacks may be packaged with the simulator's seed for a measure comparison, but that packaging grants the controller no access to their unread entries.

For strictly positive finite row laws $`p`$ and $`q`$, let
$`c=\min_w q(w)/p(w)>0`$; necessarily $`c\le1`$. On the first $`n`$ outside rows their density ratio is at least $`c^n`$. Prefix locality then gives, for a measurable successful trace event restricted to at most $`n`$ outside queries,


```math
\Pr_q(B\cap F_n)\ \ge\ c^n\Pr_p(B\cap F_n),
```


provided the common seed law and the same causal readout are used. The unbounded finite-query event is the countable union of the $`F_n`$. Positive mass on it lies in some bounded piece and transfers to the actual rival law. No single positive lower constant is asserted for that whole union, and no absolute continuity of the complete infinite outside tapes is required. [generic-query-review]

The qualitative transfer has a broader countable-alphabet form. Let the oracle alphabet $`Y`$ be nonempty and countable with its discrete sigma algebra, and let the evaluator state space be arbitrary measurable. Measurable transitions for each fixed symbol give a jointly measurable transition at this countable interface. Prefix locality factors the trace restricted to $`F_n`$ through the common initial state and the first $`n`$ oracle symbols. An actual full-support iid rival gives strictly positive mass to every finite word. On the countable word space its only null subset is empty, so every source finite-prefix law is absolutely continuous with respect to that rival prefix law. With the same independent seed measure in both product inputs, the stated SFinite hypotheses—countable sums of finite measures—permit the product, restriction and measurable-pushforward steps. They yield domination of bounded-query trace laws and, by the countable union over $`n`$, of finite-query trace laws. A positive source event in this region therefore has positive mass under the actual rival. No positive minimum likelihood ratio is asserted over an infinite word population; the finite $`c^n`$ bound above is a stronger quantitative special case. Probability language additionally requires normalized input laws. The audited primitive also states an outer-measure-set transfer; the tail-event applications here use measurable events and do not rely on that stronger interface. [generic-query-review]

A trace space may contain malformed records that the evaluator never produces, such as a constant action record paired with an ever-growing outside-query counter. Let $`B`$ be the measurable tail event expressing the required action property, and let $`F_n`$ be the measurable event of at most $`n`$ outside queries in the trace. Prove from the evaluator's action/counter invariant that generated source runs in $`B`$ have finitely many such queries. Under the actual source trace law this gives $`\Pr_p(B)=\Pr_p(B\cap\bigcup_n F_n)`$. Positive source mass then lies in some measurable $`B\cap F_n`$. Transfer that bounded piece and push it through the established measurable action readout; the actual-law identity gives positive rival probability to the same observable tail property. This argument never forms the image of the evaluator as a measurable set. A relation proved only on generated runs is used to establish the source-law equality, not imposed on every element of the ambient trace space. [seeded-necessity-review]

Theorem 24's common upper-reference construction permits correlated actual seed/oracle laws when their seed marginals are appropriately dominated. That theorem does not by itself prove transfer to a specified rival. Equal seed marginals and equal observation marginals do not determine the joint acquired law: let $`R`$ and $`Y`$ be fair independent bits in one model and let $`Y=1-R`$ in another. Both marginals agree, but $`\Pr(R=Y)`$ changes from $`1/2`$ to zero. The product feedback construction above is a sufficient actual-law premise; a replacement with correlations must prove the required joint or conditional comparison.

These interfaces also delimit the policy theorem's permissions claim. For one fixed common menu $`\Gamma`$, the full-support theorem applies to the restricted targets $`G_\theta\cap\Gamma`$. Its queue construction is legal at every finite history, including histories the policy never reaches, because every chosen plan is nonempty and lies in $`\Gamma`$. An out-of-menu default is harmless only when the construction proves it is never used. Early target errors can still be permitted actions. A changing menu needs a different invariant. Likewise, a zero-probability revealing observation can allow one bad probe followed by correct repair forever even when the recurrent good sets themselves are indistinguishable; it invalidates the full-support necessity argument, rather than contradicting it. [static-license-review], [seeded-necessity-review]

#### From finite blocks to a measurable physical action stream

A macro-process whose outcomes are finite action lists must be connected to physical time. For a path of lists $`B_0,B_1,\ldots`$, define


```math
L_0=0,\qquad L_n=\sum_{j\lt{}n}|B_j|.
```


Assume $`L_n\to\infty`$. For each physical time $`t`$, choose the least index $`k`$ with $`L_{k+1}>t`$ and read entry $`t-L_k`$ of $`B_k`$. Minimality ensures $`L_k\le t<L_{k+1}`$, so the entry exists. This concatenates the actual lists in order, including when some lists are empty. If every action in $`B_j`$ is good for all $`j\ge N`$, every physical action at time $`t\ge L_N`$ is good. No uniform upper bound on block lengths is required. Unbounded cumulative length is essential: an infinite sequence of empty blocks satisfies eventual block goodness vacuously and issues no infinite action stream. [physical-flattening-review]

A fixed finite-prefix decoder has a stronger contract. Suppose $`A`$ is countable and $`B_j`$ are measurable finite-list random variables. Define a total decoder $`D_t`$ by concatenating only $`B_0,\ldots,B_t`$, taking entry $`t`$ if it exists and a fixed default otherwise. It is measurable: the finite tuple of lists ranges over a countable discrete space, and each output fibre is a countable union of measurable tuple fibres. If every block is nonempty, then $`L_{t+1}\ge t+1`$, so $`D_t`$ agrees with the physical concatenation for every $`t`$. Pointwise nonemptiness almost surely for each $`j`$ suffices, by taking the countable intersection of those probability-one events. [measurable-physical-review]

Mere unbounded cumulative length does not justify this particular prefix budget. With blocks $`(0),(),(1),(),(2),(),\ldots`$ and default 99, the full concatenation has action 1 at physical time 1, while $`D_1`$ sees only $`(0),()`$ and returns 99. The pathwise flattening lemma remains true; the proposed decoder is the part that fails. One can instead use a suitably measurable first-crossing construction, or prove the stronger nonemptiness premise before using $`D_t`$. The two constructions must not be identified without that proof.

A decoder measurable in completed block records is not thereby causal at each physical action. A two-action block's completed record can contain the observation obtained after its second action; a function of that record could inspect it when selecting a purported first action. Physical nonanticipation therefore needs a further invariant: the next issued action is determined by the common seed and the already acquired physical history. The queue reconstruction in [Collective Inquiry, §7.12](collective-inquiry-and-strategic-coordination.md#712-recursive-restoration-with-zero-observation-probabilities) proves this for its policy by induction on that history. It does not retroactively enlarge the earlier decoder's measurable-function theorem.

#### Planned costs, observed exits and realized error counts

The finite generated-process argument and its recursive successor count different objects. A planned block is a proposed list; a realized record must say how much of it was executed, which observations were acquired and whether an exit changed the next phase. A state-only reset can forget the exit observation and cannot recover its acquisition law merely from the new phase label. The recorded construction retains that observation and the executed prefix. When an observation changes the surviving support and hence the permitted menu, its old suffix may need to be abandoned. This differs from the fixed full-support queue in Collective Inquiry §7.11, whose proof deliberately completes a nonempty plan before replanning. [generated-process-review], [recursive-action-review]

With zero observation probabilities, truth retention is a statement about positive-probability outcomes: updating the candidate support by the observed feedback cannot remove the true model on such a transition. A strict decrease of the finite surviving support bounds the number of such support changes. These facts support the recursive construction, but the stopped-outcome law must still account for its exit mass as well as its nonexit trajectories. An unnormalized killed law is not a normalized law of complete outcomes.

For a physical error conclusion, let $`C_j`$ be the nonnegative integer number of bad actions in the realized $`j`$th record, counted with multiplicity. If the generated law proves


```math
\sum_j\mathbb E[C_j]<\infty,
```


monotone convergence gives finite expectation of $`\sum_j C_j`$, hence $`\sum_jC_j<\infty`$ almost surely. There are therefore only finitely many records containing bad actions. Together with unbounded physical length and eventual block goodness, this proves finitely many actual errors. The integer count is load-bearing: the real charges $`2^{-j}`$ have a finite sum and are positive at every index. Nor does an almost-surely finite count alone establish a finite expected count.

Indexing matters when the record of a just-completed block is stored in its successor state. The initial state may carry an empty placeholder; the first $`n`$ executed plans then correspond to the next $`n`$ records, rather than the first $`n`$ state labels. If every post-initial record is nonempty almost surely, discard the placeholder and use the countable-intersection argument before applying the fixed decoder. A planned-cost bound can replace the realized-count bound only after an explicit inequality and this index correspondence have been proved.

These are mathematical interfaces between a process law, its records and the action stream it actually generates. They do not supply a new execution receipt, an expected-time guarantee absent from the hypotheses, or a real sensor model. The common-observation and physical-time conclusions sharpen what a restoration argument must establish; they do not authenticate a normative target or identify the source of its authority.

### 9.10 Sparse priors, cluster width and the cost of compulsory reports

The endpoint-density result in §9.8 assumes a positive density envelope throughout an endpoint neighbourhood. A prior supported on separated clusters can have very different reporting costs. Its gaps can make the next relevant scale identifiable cheaply, while a small change in the shape inside each cluster can make every policy have infinite expected cost. The difference concerns one fixed literal acceptance test and one acquired experiment; it does not arise from changing the target after seeing the data.

This section uses the positive reporting clock $`n=1,2,\ldots`$. Draw a parameter $`\alpha`$ once, draw a private seed independently of it and of the entire innovation stream, and acquire $`Y_j=\mathbf1\{U_j\leq\alpha\}`$ from independent uniform innovations. At time $`n`$ one report is compulsory and may use the seed, time and complete ordered word $`Y_1\ldots Y_n`$. The policy receives neither the parameter nor its cluster index, an unacquired innovation, a correctness label or an unpriced extra sample. The literal excesses are the same as in §9.8:

```math
D_0(\alpha,\varepsilon,q)=q^2-\frac14-\alpha\varepsilon(1+\varepsilon),
\qquad
D_1(\alpha,\varepsilon,q)=(1-q)^2-\frac14+\alpha\varepsilon(1-\varepsilon).
```

Acceptance means both excesses are nonpositive; equality is accepted. Let $`e_n`$ indicate failure and write

```math
C_N(\mu)=\inf_{\pi}\mathbb E_\mu^\pi\sum_{n=1}^N e_n,
\qquad
C_\infty(\mu)=\inf_{\pi}\mathbb E_\mu^\pi\sum_{n=1}^\infty e_n.
```

The negative results allow measurable real reports and all independent-seed policies. Positive witnesses below give coherent reports in $`[0,1]`$. All infinite sums and integrals of costs are nonnegative extended integrals, so their interchange uses Tonelli, not an assumed finite budget. A possible initial report at $`n=0`$ adds at most one; it is excluded from every displayed exact positive-time identity. Infinite expected count does not assert infinitely many failures almost surely.

#### Sparse spacing gives a complete criterion for narrow clusters

Fix $`0\lt\varepsilon\leq1/4`$ and a half-separated sequence

```math
0\lt a_{i+1}\leq\frac{a_i}{2},\qquad a_0\leq\frac12,
\qquad
r_i=\frac{a_{i+1}}{a_i},\quad L_i=\log(1/r_i),\quad
Z=\sum_{i\geq0}a_i,\quad S=\sum_{i\geq0}r_iL_i.
```

Here $`0\lt Z\leq1`$. For each $`i`$, let $`\nu_i`$ be any Borel probability supported on $`I_i=[(1-\delta)a_i,(1+\delta)a_i]`$, and set $`\mu=Z^{-1}\sum_i a_i\nu_i`$. When $`0\leq\delta\leq\varepsilon/4`$, the complete criterion is

```math
\frac{e^{-1}}{9Z}S\ \leq\ C_\infty(\mu)\ \leq\ \frac{30000}{Z}S.
```

Thus a finite-cost policy exists exactly when $`S`$ is finite, uniformly over every choice of the component laws. The upper bound is attained as a bound by the explicit scale selector below; it does not require computation of a posterior maximizer. [sparse-cluster]

First, the centre report $`q_i=1/2+\varepsilon a_i`$ accepts the whole cluster. Direct substitution gives

```math
D_0=-\varepsilon^2a_i(1-a_i)+(a_i-\alpha)\varepsilon(1+\varepsilon)
       \leq-\frac3{16}\varepsilon^2a_i,
\qquad
D_1=-\varepsilon^2a_i(1-a_i)+(\alpha-a_i)\varepsilon(1-\varepsilon)
       \leq-\frac14\varepsilon^2a_i.
```

Conversely, one report cannot accept parameters in two distinct clusters. Writing $`t=q-1/2`$, acceptance at positive $`\alpha\geq\beta`$ implies

```math
t-t^2\geq\alpha\varepsilon(1-\varepsilon)\gt0,
\qquad
t+t^2\leq\beta\varepsilon(1+\varepsilon),
\qquad
\frac\alpha\beta\leq\frac{1+\varepsilon}{1-\varepsilon}\leq\frac53.
```

Since $`\delta\leq1/16`$, parameters from successive clusters have ratio at least $`2(1-\delta)/(1+\delta)\geq30/17\gt5/3`$. At zero, the only accepted report is $`1/2`$, which accepts no positive parameter.

For a word $`w`$ of length $`n`$, put $`m_i(w)=(a_i/Z)\int P_\alpha(w)\,d\nu_i(\alpha)`$. The sequence is summable, tends to zero, and has a positive attained maximum. The least maximizing index gives a deterministic measurable rule on the countable set of finite words. Its centre report accepts exactly the mass of that cluster, so it minimizes every stage risk and every finite horizon simultaneously. This is a classical selector, not a claim of effective maximization over an infinite prior. Independent randomization cannot lower that conditional minimum.

For any nonnegative summable sequence with maximum at $`j`$,

```math
\sum_{i\geq0}\min(m_i,m_{i+1})\leq\sum_i m_i-m_j:
```

charge the term with $`i\lt j`$ to $`m_i`$ and the term with $`i\geq j`$ to $`m_{i+1}`$. No posterior-unimodality assumption is used. On the all-zero word, $`\alpha\leq17a_i/16`$ and $`1-\alpha\geq15/32`$ imply $`\log(1-\alpha)\geq-3a_i`$. For $`0\leq n\leq L_i/(3a_i)`$ this gives

```math
m_i(0^n)\geq\frac{a_{i+1}}Z,
\qquad
m_{i+1}(0^n)\geq\frac{a_{i+1}}Z e^{-r_iL_i}
                  \geq\frac{e^{-1}a_{i+1}}Z.
```

Passing from $`n`$ to $`n+1`$ loses at most a factor $`1/3`$. There are at least $`L_i/(3a_i)`$ such nonnegative integer starting times. Summing their positive-time overlaps therefore contributes at least $`e^{-1}r_iL_i/(9Z)`$. The adjacent-overlap inequality and Tonelli give the universal lower bound. It remains valid pointwise in the seed, and hence after seed integration. This proof uses separation and $`\delta\leq1/16`$, but does not need a report that accepts an entire cluster.

For the constructive upper bound define $`K=320/3`$ and

```math
b_i=a_i\min\left\{\frac34,
       \max\left\{\frac32r_i,\frac1{KL_i}\right\}\right\},
\qquad
H_n=\frac1n\sum_{j=1}^nY_j,
\qquad x_n=\max(H_n,1/n).
```

The boundaries satisfy $`(3/2)a_{i+1}\leq b_i\leq(3/4)a_i`$ and $`b_{i+1}\leq b_i/2`$. Thus $`J_n=\min\{i:x_n\gt b_i\}`$ exists; boundary equality selects the next index. Report $`q_{J_n}`$. The positive floor is essential: the nearest positive support point to an empirical mean of zero need not exist.

Here is a bound that will also be used for wider clusters. For a Bernoulli variable of mean $`\alpha`$ and $`|t|\leq1`$,

```math
\mathbb E\exp(t(Y-\alpha))\leq\exp(t^2\alpha(1-\alpha)).
```

Indeed, the centred first moment vanishes, every absolute moment of order at least two is at most the variance, and $`e^{|t|}-1-|t|\leq t^2`$. Chernoff's argument with $`t=\pm1/10`$ yields

```math
\alpha\leq4b/5\ \Longrightarrow\ \Pr(H_n\geq b)\leq e^{-nb/100},
\qquad
b\leq4\alpha/5\ \Longrightarrow\ \Pr(H_n\leq b)\leq e^{-n\alpha/100}.
```

If the true cluster is $`i`$, selection of a different cluster requires $`x_n\gt b_{i-1}`$ or $`x_n\leq b_i`$, with no first event for $`i=0`$. For all $`\delta\leq1/16`$, the parameter lies between $`15a_i/16`$ and $`17a_i/16`$. The upper-boundary sum is at most $`101/b_{i-1}`$: at most $`1/b_{i-1}`$ early times can be caused by the floor, and the geometric tail is at most $`100/b_{i-1}`$. The lower event requires $`n\geq1/b_i`$ and has summed probability at most

```math
\frac{101}\alpha e^{-\alpha/(100b_i)}
\leq\frac{1616}{15a_i}\exp\left(-\frac{3a_i}{320b_i}\right).
```

After weighting by $`a_i/Z`$, the total expected number of wrong cluster selections is at most

```math
\frac{101}Z\sum_i\frac{a_{i+1}}{b_i}
 +\frac{1616}{15Z}\sum_i\exp\left(-\frac{3a_i}{320b_i}\right).
```

The boundary definition gives

```math
\frac{a_{i+1}}{b_i}\leq\left(K+\frac4{3\log2}\right)r_iL_i,
\qquad
\exp\left(-\frac{3a_i}{320b_i}\right)
\leq e^{-1/(160r_i)}+r_i\leq(1+160/e)r_i.
```

Since $`\sum r_i\leq S/\log2`$, the coefficient is at most

```math
101\left(K+\frac4{3\log2}\right)
 +\frac{1616}{15\log2}(1+160/e)
 \leq\frac{427432}{15}\lt30000.
```

Here only $`\log2\geq1/2`$ and $`e\geq2`$ were used in the last estimate. Whole-cluster acceptance converts correct classification into a correct report in the narrow-width case. The classification estimate itself remains valid up to $`\delta=1/16`$; it must not be confused with that narrower acceptance premise.

For example, $`a_i=e^{-(i+1)^2}`$ has $`r_i=e^{-(2i+3)}`$ and

```math
S=e^{-3}\left(\frac3{1-e^{-2}}+\frac{2e^{-2}}{(1-e^{-2})^2}\right)\lt\infty.
```

Uniform component laws with positive $`\delta`$ give an absolutely continuous prior of constant density $`1/(2\delta Z)`$ on the disjoint cluster intervals. Nevertheless $`\int\alpha^{-1}\,d\mu=\infty`$, since every component contributes at least $`1/[(1+\delta)Z]`$. This does not contradict §9.8: arbitrarily large relative gaps destroy a positive density envelope throughout an endpoint neighbourhood. Inside a sufficiently wide gap one can choose $`x`$ with no mass in $`(x,2x]`$, so its endpoint distribution function also has $`F(2x)=F(x)`$; a strict lower-growth premise would fail. If alternative weights satisfy $`c\,a_i/Z\leq w_i\leq C\,a_i/Z`$ for constants $`0\lt c\leq C\lt\infty`$ and the same component laws, then their measures and every policy cost satisfy the same two-sided comparison. Finiteness is preserved. The displayed $`S`$ criterion is not a classification for arbitrary unrelated weights. [sparse-cluster], [sparse-earlier-review]

For this continuous prior, adding a zero atom gives a different result: every policy for $`\mu_\theta=\theta\delta_0+(1-\theta)\mu`$, with $`0\lt\theta\lt1`$, has infinite expected count, even when redesigned for that mixture. For any fixed common policy, write $`C_\alpha`$ for its conditional expected count. On this section's positive report clock, the zero-history argument of §9.8 gives $`C_\alpha+C_0\geq\sum_{n\geq1}(1-\alpha)^n=(1-\alpha)/\alpha`$. If $`C_0=\infty`$, the zero atom already forces divergence. If $`C_0\lt\infty`$, integrating against $`\mu`$ and using its infinite inverse first moment forces $`\int C_\alpha\,d\mu=\infty`$. Nonnegative mixture linearity proves the claim without subtracting infinite quantities. The pure-zero endpoint $`\theta=1`$ is excluded. [sparse-cluster]

For later atomic examples it is useful to retain the sharper source bound $`C_\infty\leq256S/Z`$ for $`\nu_i=\delta_{a_i}`$. An ordinary derivation makes its scope explicit. On a word with $`k`$ ones, the unnormalized scores $`a_i^{k+1}(1-a_i)^{n-k}`$ are unimodal along the ordered support. Consequently the adjacent-minimum inequality above becomes equality. For adjacent parameters $`a`$ and $`b\leq a/2`$, summing over all words gives

```math
\sum_w\min(aP_a(w),bP_b(w))
 \leq\min\{b,\sqrt{ab}\,\rho^n\},
\qquad
\rho=\sqrt{ab}+\sqrt{(1-a)(1-b)}.
```

The identity for $`1-\rho`$ as half the sum of two squared square-root differences gives $`1-\rho\geq a/32`$, because $`\sqrt{b/a}\leq1/\sqrt2\leq3/4`$. We may weaken this to $`\rho^n\leq e^{-na/64}`$. A decreasing-function integral bounds its positive-time sum by

```math
\int_0^\infty\min\{b,\sqrt{ab}e^{-at/64}\}\,dt
 =64\frac ba\left(1+\frac12\log(a/b)\right)
 \leq256\frac ba\log(a/b).
```

Sum over adjacent pairs and divide by $`Z`$. This proof uses the weights proportional to the support locations and the attained classical Bayes selector. It neither supplies an algorithm for exact infinite maximization nor licenses adjacent-minimum equality for arbitrary weights. [sparse-crossover], [sparse-nonconvex-review]

#### Strict width, the critical width, and the shape of a component

The narrow-width criterion extends to every $`0\leq\delta\lt\varepsilon`$ with $`\delta\leq1/16`$, but the report and finite-head treatment must change. Set

```math
q_i^*=\frac12+\varepsilon a_i(1-\delta\varepsilon),
\qquad R=\frac{\varepsilon-\delta}{2\varepsilon}.
```

The two worst endpoint excesses coincide:

```math
D_0((1-\delta)a_i,\varepsilon,q_i^*)
 =D_1((1+\delta)a_i,\varepsilon,q_i^*)
 =\varepsilon a_i\{\delta-\varepsilon+
                 \varepsilon a_i(1-\delta\varepsilon)^2\}.
```

For $`a_i\leq R`$ this is at most $`-\varepsilon a_i(\varepsilon-\delta)/2`$, so the entire tail cluster is accepted. Let $`H`$ be the first index with $`a_H\leq R`$. Use the same observable selector $`J_n`$; when $`J_n\lt H`$ report the empirical repair $`1/2+\varepsilon H_n`$, and otherwise report $`q_{J_n}^*`$. The true index appears only in the proof, not in the rule. [sparse-width]

A useful empirical constant follows directly from the same moment bound. Put $`v=\alpha(1-\alpha)`$, $`m=\varepsilon^2v`$ and $`d=\varepsilon(H_n-\alpha)`$. The excesses of the empirical report are

```math
-m+(1+2\alpha\varepsilon)d+d^2,
\qquad -m-(1-2\alpha\varepsilon)d+d^2.
```

If $`|H_n-\alpha|\leq\varepsilon v/2`$, then $`|d|\leq m/2`$; the absolute linear coefficients are at most $`3/2`$ and $`m\leq1/64`$, so both expressions are negative. Chernoff with $`t=\pm\varepsilon/4`$ bounds the failure probability by $`2e^{-n\varepsilon^2v/16}`$. Hence

```math
\mathbb E_\alpha\sum_{n\geq1}e_n(\mathrm{emp})
 \leq\frac{32}{\varepsilon^2\alpha(1-\alpha)}.
```

This is an additional pointwise estimate with its proof, not a change to the separately derived constants in §9.8. Define

```math
M_{\mathrm{head}}=\sum_{i\lt H}\frac{a_i}Z
       \int\frac{d\nu_i(\alpha)}{\alpha(1-\alpha)}.
```

Charge a wrong selected index to the already proved classification bound, and charge a correctly selected head index to the empirical bound. The result is

```math
C_\infty(\mu)\leq\frac{30000S}Z+
                         \frac{32M_{\mathrm{head}}}{\varepsilon^2}.
```

For the minimal head, each head parameter is at least $`15R/16`$ and at most $`17/32`$. Thus $`M_{\mathrm{head}}\leq512/(225R)`$, and the additive term is at most $`32768/[225\varepsilon(\varepsilon-\delta)]`$. It diverges as $`\delta`$ approaches $`\varepsilon`$; no uniform limit at the boundary is asserted. The preceding zero-word lower bound still applies, so finiteness is equivalent to $`S\lt\infty`$ throughout this strict-width class. [sparse-width], [sparse-final-extension]

The boundary $`\delta=\varepsilon`$ is sharp for a theorem uniform over all component shapes. More generally, whenever $`\varepsilon\leq\delta\leq1/16`$, an allowed component may give half its mass to each of

```math
\ell_i=(1-\varepsilon)a_i,\qquad u_i=(1+\varepsilon)a_i.
```

No real report accepts both. With $`t=q-1/2`$ and $`s_i=\varepsilon a_i(1-\varepsilon^2)\gt0`$, acceptance of the lower point gives $`t+t^2\leq s_i`$, whereas acceptance of the upper gives $`t-t^2\geq s_i`$. Their combination forces $`t=0`$ and then contradicts positivity of $`s_i`$. Strict positivity of the disturbance matters: at $`\varepsilon=0`$, the common report $`q=1/2`$ is accepted for every parameter. For every fixed seed and zero prefix at least one member of each pair fails. Its weighted risk is at least $`a_i(1-u_i)^n/(2Z)`$. The positive-time geometric sum is

```math
\frac{1-u_i}{2(1+\varepsilon)Z}\geq\frac3{20Z}.
```

Every one of infinitely many components therefore contributes a fixed positive amount, and every policy has infinite expected cost. This argument is within each pair; it needs no false claim that reports cannot be shared across different pairs. [sparse-width], [sparse-width-review]

The same failure can be absolutely continuous, with no endpoint atom. Put $`h_i=\varepsilon a_i^2/16`$ and place half of each component uniformly on each strip $`[\ell_i,\ell_i+h_i]`$ and $`[u_i-h_i,u_i]`$. If one report accepted a point in both strips, acceptance of an upper-strip point would give $`t\geq3\varepsilon a_i/4`$. Adding the most favourable endpoint inequalities would instead give $`t^2\leq\varepsilon h_i=\varepsilon^2a_i^2/16`$, a contradiction. At least one entire strip is rejected. On a zero word its likelihood is at least $`(1-u_i)^n`$, so the same divergent lower bound applies.

In contrast, a uniform law on each **whole** critical interval has a finite-cost witness whenever $`S`$ is finite. Assume $`\delta=\varepsilon\leq1/16`$, and first consider a tail centre $`a\leq1/8`$. Write

```math
\ell=(1-\varepsilon)a,\quad u=(1+\varepsilon)a,\quad
s=\varepsilon a(1-\varepsilon^2),\quad h=2\varepsilon^2a^2,
\quad W=4\varepsilon a^2,
\qquad q_L=\frac12+s-h,\quad q_R=\frac12+s+h.
```

The left report accepts $`[\ell,u-W]`$, and the right report accepts $`[\ell+W,u]`$. The four extreme excesses are

```math
D_0(\ell,q_L)=s^2-h-2sh+h^2,
\quad D_1(u,q_R)=s^2-h+2sh+h^2,
```

```math
D_1(u-W,q_L)=s^2+h-2sh+h^2-W\varepsilon(1-\varepsilon),
\quad D_0(\ell+W,q_R)=s^2+h+2sh+h^2-W\varepsilon(1+\varepsilon).
```

The suppressed middle argument in these four expressions is $`\varepsilon`$. For $`E=\varepsilon^2a^2`$, one has $`s^2\leq E`$ and $`2sh+h^2\leq E(4\varepsilon a+4\varepsilon^2a^2)\leq E`$. Also $`W\varepsilon(1-\varepsilon)\geq15E/4`$ and $`W\varepsilon(1+\varepsilon)\geq4E`$. All four excesses are nonpositive, and both reports are coherent. Since $`W\leq\varepsilon a/2`$, the accepted intervals overlap. [sparse-uniform]

Choose $`q_L`$ when $`H_n\leq a`$ and $`q_R`$ otherwise; equality chooses the left report. Only the two edge strips, of combined uniform mass $`4a`$, can suffer a wrong-side report. At either edge, choosing the wrong side requires a sample-mean deviation of at least $`\varepsilon a/2`$. The variance is at most $`5a/4`$; Chernoff with $`t=\pm\varepsilon/8`$ bounds that probability by

```math
e^{-11n\varepsilon^2a/256}\leq e^{-n\varepsilon^2a/32}.
```

The positive-time sum is at most $`32/(\varepsilon^2a)`$. Multiplication by the edge mass $`4a`$ gives $`128/\varepsilon^2`$ for the component average. Use the original scale selector, the empirical report for selected centres above $`1/8`$, and this two-report rule for selected tail centres. The classification, head and local edge costs give

```math
C_\infty(\mu)\leq\frac{30000S}Z+
       \frac{128}{\varepsilon^2}+
       \frac{32M_{\mathrm{head}}}{\varepsilon^2}.
```

With the minimal head $`H\leq2`$, head parameters lie in $`[15/128,17/32]`$, so $`M_{\mathrm{head}}\leq4096/225`$. The additive bound is therefore $`[128+131072/225]/\varepsilon^2`$. The universal spacing lower bound proves necessity of $`S\lt\infty`$. Uniform whole intervals and thin endpoint strips thus have opposite answers at exactly the same critical width and with the same component weights. Width alone does not determine the answer. The minimal-head constants are the final extension; the earlier width and uniform editions are retained as predecessors, not silently treated as identical source text. [sparse-uniform], [sparse-final-extension], [sparse-width-previous], [sparse-uniform-previous]

#### Endpoint contamination has an exact finite-horizon increment

For this paragraph take an atomic prior $`\mu=\sum_iw_i\delta_{a_i}`$ on a half-separated positive support, with arbitrary positive weights summing to one. Write $`s=1-\theta`$ and $`\mu_\theta=\theta\delta_0+s\mu`$. Distinct positive atoms, and zero versus any positive atom, cannot share an accepted report. Word by word, the least maximizing posterior atom gives one policy that minimizes all horizons. The only word whose score acquires an endpoint contribution is $`0^n`$. If

```math
M_n=\max_i w_i(1-a_i)^n,
```

then the exact identity is

```math
C_N(\mu_\theta)=sC_N(\mu)+D_N(\theta),
\qquad D_N(\theta)=\sum_{n=1}^N\min\{\theta,sM_n\}.
```

To see this, let $`A_n=\sum_iw_i(1-a_i)^n`$. The old zero-word error is $`A_n-M_n`$ and the new one is $`\theta+sA_n-\max(\theta,sM_n)`$. Subtract $`s(A_n-M_n)`$; every other word's error simply scales by $`s`$. Summability ensures that the maximum is attained. This identity is valid for $`\theta=0,1`$ as well; both endpoints have $`D_N=0`$. In particular $`0\leq D_N\leq\theta N`$ and $`|C_N(\mu_\theta)-C_N(\mu)|\leq\theta N`$. The increment is not the total cost: the known pure-zero model at $`\theta=1`$ has cost zero. [sparse-crossover]

For $`0\lt\theta\lt1`$ define the finite threshold

```math
T_\theta=\max\left(\{0\}\cup
 \left\{\frac{\log(sw_i/\theta)}{-\log(1-a_i)}:sw_i\gt\theta\right\}\right),
\qquad m=\lfloor T_\theta\rfloor.
```

Only finitely many weights can exceed $`\theta/s`$. For $`n\leq m`$ the endpoint contribution is the smaller score, and beyond $`m`$ every positive-atom score is smaller. Therefore

```math
D_N(\theta)=\theta\min(N,m)+s\sum_{n=m+1}^N M_n,
```

with an empty tail understood as zero. If $`T_\theta`$ is an integer, equality of the scores makes either expression agree at that time. This is the exact crossover, not a universal multiple of $`1/\theta`$.

For weights $`w_i=a_i/Z`$, the inequality $`-\log(1-a_i)\geq a_i`$ gives $`\theta T_\theta\leq s/(eZ)`$. Even a matching positive lower constant is false. For the exponential-square support put $`t_i=\sqrt{a_i a_{i+1}}`$ and $`\theta_i=t_i/(Z+t_i)`$. The eligible support locations are precisely $`a_j\geq a_i`$. For large $`i`$, $`x\mapsto\log(x/t_i)/x`$ decreases on that range, so

```math
\theta_iT_{\theta_i}\leq
\frac{\sqrt{r_i}\log(1/r_i)}{2(Z+t_i)}\longrightarrow0.
```

The support gaps can therefore move the crossover far below the nominal inverse-contamination scale.

There is also a uniform support-count description for $`w_i=a_i/Z`$. Set $`t=\theta Z/s`$ and

```math
L_N=\frac{s}Z\sum_{a_i\leq t}(1-a_i)\{1-(1-a_i)^N\},
\qquad
K(N,t)=\#\{i:1/N\leq a_i\leq t\}.
```

The full small-atom zero-word mass is unavoidable: if the endpoint wins, all small atoms fail; if a positive atom wins, its score is no greater than the endpoint score when it is small, so replacing it by that endpoint score still covers the small-atom sum. Consequently

```math
L_N\leq C_N(\mu_\theta)
 \leq sC_N(\mu)+L_N+\frac{s}Z(2+4\log2).
```

For the upper bound use $`\min(t,\max_i x_i)\leq\sum_i\min(t,x_i)`$. At a head location $`a_i\gt t`$, the decreasing-function integral gives

```math
\sum_{n\geq1}\min\{t,a_i(1-a_i)^n\}
 \leq\frac{t}{a_i}\{1+\log(a_i/t)\}.
```

There is at most one location in each half-open band $`[2^kt,2^{k+1}t)`$. Summing the bounds $`2^{-k}[1+(k+1)\log2]`$ gives $`2+4\log2`$. At the small locations the geometric sum is exactly the term defining $`L_N`$.

Let $`Q_N=ZL_N/s`$. Locations below $`1/N`$ contribute less than $`N\sum_{a_i\lt1/N}a_i\leq2`$. Each of the $`K`$ remaining locations contributes at most one. Its deficit from one is at most $`a_i+e^{-Na_i}`$; the sum of the first terms is at most one, and the numbers $`Na_i\geq1`$ are separated by factors of at least two, so the exponential terms sum to less than one. Hence

```math
K(N,t)-2\leq Q_N\leq K(N,t)+2.
```

If $`B=C_\infty(\mu)\lt\infty`$, the resulting two-sided bound is

```math
\frac{s}Z\{K(N,t)-2\}\leq C_N(\mu_\theta)
 \leq sB+\frac{s}Z\{K(N,t)+4+4\log2\}.
```

For $`a_i=e^{-(i+1)^2}`$ this count is exactly

```math
K(N,t)=\max\{0,A(N)-H(t)+1\},\qquad
A(N)=\lfloor\sqrt{\log N}\rfloor,
\quad H(t)=\max\{1,\lceil\sqrt{\max(0,\log(1/t))}\rceil\}.
```

The formula includes $`N=1`$ and equality at either support boundary. For fixed $`0\lt\theta\lt1`$,

```math
\frac{C_N(\mu_\theta)}{\sqrt{\log N}}\longrightarrow\frac{1-\theta}Z.
```

For jointly varying $`\theta,N`$, retaining the integer $`K`$ gives the more precise statement $`C_N=(s/Z)K+E`$ with $`-2s/Z\leq E\leq sB+s(4+4\log2)/Z`$. The uncontaminated lifetime cost is finite, while every fixed interior contamination weight has infinite lifetime cost. Thus taking $`N\to\infty`$ and then $`\theta\downarrow0`$ gives a different answer from taking those limits in the reverse order. This example concerns this sparse family; it does not overturn the endpoint-atom plus Beta example in §9.8.

Two failed shortcuts clarify the proof. On support $`(1/2,1/4,1/8)`$ with weights $`(9/20,1/10,9/20)`$, the one-zero scores are $`(9/40,3/40,63/160)`$. Their sum minus their maximum is $`3/10`$, whereas the sum of adjacent minima is $`3/20`$. Arbitrary weights do not have the unimodality needed for equality. Nor can an empirical zero be assigned an unspecified nearest positive support point: that infimum need not be attained. The explicit positive floor and the correctly restricted atomic equality above avoid those failures. [sparse-crossover], [sparse-earlier-review]

#### Interior contamination and a nonconvex finite-cost domain

An endpoint atom is not essential to instability. Let $`\mu`$ be the centre prior on the exponential-square support and let $`\sigma`$ use the incompatible critical pairs, or the two thin continuous strips, at the same centres and weights. The former has a finite-cost policy and every policy for the latter has infinite expected count. For $`0\lt\theta\leq1`$,

```math
\widetilde\mu_\theta=(1-\theta)\mu+\theta\sigma
\quad\Longrightarrow\quad
C_\infty(\widetilde\mu_\theta)=\infty,
\qquad
\|\widetilde\mu_\theta-\mu\|_{\mathrm{TV}}\leq\theta,
```

where total variation is the supremum over measurable events. For each policy, linearity of the nonnegative prior integral gives a contribution $`\theta\cdot\infty`$ from $`\sigma`$. This also covers a policy redesigned for that particular mixture. Every new parameter is within relative distance $`\varepsilon`$ of a centre; no mass is placed at zero or one. For $`\varepsilon\leq1/16`$, a fully absolutely continuous version mixes the finite-cost uniform whole critical clusters with the divergent thin strips inside those same intervals. Both the positive and negative components can therefore be continuous, with unchanged cluster locations and weights. [sparse-interior], [sparse-final-extension]

At each finite horizon, every fixed policy's cost function lies in $`[0,N]`$, so total variation gives

```math
|C_N(\widetilde\mu_\theta)-C_N(\mu)|\leq\theta N.
```

Apply the bound to policies approaching either infimum; an optimal-policy existence assertion is unnecessary. This finite-horizon continuity and the infinite-cost jump are compatible. The exact minimum-of-two-scores crossover formula in the endpoint case is not asserted for interior contamination.

There is a stronger two-prior example. Choose half-separated centres with $`S\lt\infty`$ and $`(1+\varepsilon)a_0\leq1/2`$; for example $`a_i=(1/2)e^{-(i+1)^2}`$. Define

```math
b_i^-=(1-\varepsilon)a_i,\qquad b_i^+=(1+\varepsilon)a_i,
\qquad Z_\pm=(1\pm\varepsilon)Z,
\qquad
\mu^\pm=\sum_i\frac{b_i^\pm}{Z_\pm}\delta_{b_i^\pm}
       =\sum_i\frac{a_i}Z\delta_{b_i^\pm}.
```

Both one-sided priors are half-separated atomic families with the same ratios $`r_i`$. The atomic criterion supplies finite budgets $`256S/[(1-\varepsilon)Z]`$ and $`256S/[(1+\varepsilon)Z]`$, respectively. Yet every proper mixture

```math
\mu_\theta=\theta\mu^-+(1-\theta)\mu^+,
\qquad 0\lt\theta\lt1,
```

has infinite cost for every allowed policy. The incompatible pair at scale $`i`$ contributes on $`0^n`$ at least

```math
\min(\theta,1-\theta)\frac{a_i}Z(1-b_i^+)^n.
```

Its lifetime sum is at least $`3\min(\theta,1-\theta)/(10Z)`$. Summing over infinitely many scales proves divergence. Equivalently, if one policy had finite cost for a proper mixture, nonnegative linearity would make its costs finite under both side priors, and therefore under their balanced mixture, contradicting the same pair bound. This alternative avoids subtracting infinite quantities. [sparse-nonconvex-review]

The two side supports are disjoint: $`b_{i+1}^+\leq(1+\varepsilon)a_i/2\lt(1-\varepsilon)a_i=b_i^-`$. Thus $`\|\mu_\theta-\mu_\phi\|_{\mathrm{TV}}=|\theta-\phi|`$, with the minus-support event attaining the bound. The domain of priors admitting a finite expected count is neither convex nor open in total variation. Each fixed-policy lifetime cost is a nonnegative linear functional of the prior, and their infimum is concave in the extended sense; concavity does not make its finite-value domain convex.

If a truthful side tag is supplied before the first report, the policy can select the appropriate finite-cost side rule and has a finite mixture budget. That tag is informative about the latent parameter and changes the observation contract. It cannot be replaced by an independent private seed. The negative theorem already includes adaptive switching, randomized strategies and policies using the full ordered prefix.

Nor does the divergence contradict almost-sure eventual acceptance. At every fixed interior parameter the empirical report eventually enters a positive literal-acceptance neighbourhood by the strong law, as in §9.8. Integrating this probability-one statement against the bad mixture still gives finitely many failures almost surely. Their expected number is nevertheless infinite. Finite expectation, almost-sure finiteness and a uniform deterministic cutoff remain three different claims.

#### Transport must preserve the acquired process and the literal count

The prior comparisons above should all be interpreted on one actual experiment. A latent-index distribution and its real-parameter pushforward can have the same parameter integrals without yet identifying two policy interfaces. The source sequence first established the prior pushforward and literal score identities, and later supplied the full observation-and-policy transport. Those are distinct obligations. [sparse-paired-review], [sparse-transport-review]

For a fixed $`\alpha\in[0,1]`$, the threshold map $`u\mapsto\mathbf1\{u\leq\alpha\}`$ pushes uniform measure to the Bernoulli law of parameter $`\alpha`$. Applied coordinatewise to an independent uniform stream, it gives the Bernoulli product law on every finite cylinder, hence on the sigma algebra of complete bit streams. Equality of one-time marginals alone would not prove that result. No invertible map of paths is needed: the unobserved innovation magnitudes are discarded.

A word of fixed length $`n`$ can also be encoded by the set of its one positions. The pair consisting of that set and $`n`$ recovers the ordered word, so composing a policy with this encoding preserves every history-dependent decision. Replacing the set by its cardinality would be a different claim: words such as 01 and 10 have equal counts but a position-sensitive policy may distinguish them. This is why the full transport uses positions, even though the particular empirical selector later uses only counts.

Transport the policy by the measurable history map while retaining the same time and independent seed. At each actual sample point, its old and new reports then coincide, and substitution in the two literal excesses gives equality of the stage indicators. Nonnegative infinite sums give equality of the total counts without an integrability premise. The stream pushforward identifies their conditional expectations. Finally, if $`\alpha=f(i)`$ is drawn from a normalized latent distribution, push that distribution forward, expand the resulting countable mixture, and use Tonelli together with seed independence. This identifies the unconditional expected count on the common real-parameter, seed and uniform-innovation space.

That order matters: prove the stream law and actual readout first, then integrate the actual parameter map. Replacing $`f`$ by a constant would generally change the inverse moment and the cost even if one retained similar-looking symbolic formulas. Neither a correct parameter marginal alone nor an assumed conditional-loss equation supplies the full policy transport. Conversely, a forward measurable map is sufficient; recovery of the unused uniform magnitudes is not required. On the common interface, all-policy lower bounds still cover policies redesigned after the prior changes. [sparse-transport-review]

#### A finite observation loss cannot represent this literal indicator

There is a precise obstruction to importing an observed-symbol loss theorem directly into this example. If a finite family has strictly positive weights $`p(w)`$, a common nonnegative table $`\ell(w)`$ satisfies

```math
\sum_w p(w)\ell(w)=0\quad\Longrightarrow\quad
\ell(w)=0\text{ for every }w.
```

Normalization of $`p`$ is unnecessary. The same table then has zero weighted sum under every other finite weight family. Interior Bernoulli laws give positive probability to every word of each fixed finite length.

Take $`\varepsilon=1/4`$ and $`q=9/16`$. At $`\alpha=1/4`$ both excesses equal $`-3/256`$, so the literal failure indicator is zero. At $`\alpha=1/2`$, the excesses are $`-23/256`$ and $`9/256`$, so the indicator is one. A common nonnegative loss on the next bit, or on any fixed finite future word, cannot have expectations equal to those two literal values: the first zero expectation forces every entry to vanish. A signed next-bit table with values $`(-1,3)`$ does have expectations zero and one, respectively. Adding a constant to make it nonnegative adds a per-stage baseline and destroys the zero-loss and finite-total-cost contract. At an endpoint, some word probabilities vanish, so the full-support premise is substantive. [sparse-observation-review]

Hutter's *General Loss Bounds for Universal Sequence Prediction* studies a common nonnegative bounded loss attached to the observed outcome and the chosen decision; its binary loss bound transfers finite known-law cumulative loss to the Bayes mixture under its hypotheses. The later *Optimality of Universal Bayesian Sequence Prediction for General Loss and Alphabet* develops the broader alphabet-and-loss framework. These are relevant antecedents, but the parameter-indexed literal zero-one indicator above has just failed that common finite-observation-loss representation. A Bayes mixture of the two sequence laws may dominate both without supplying the missing loss interface. [sparse-hutter-2001], [sparse-hutter-2003]

The obstruction concerns that exact nonnegative finite-observation representation. It does not refute proper scoring, posterior convergence, parameter estimation, a signed or approximate loss, a different feedback model, an infinite-stream observation, or every possible indirect reduction. It is not a dispute about finite versus countable model classes. The sources retain that limited comparison rather than claiming a contradiction with universal prediction.

#### An exact rational witness and its interface limits

The preceding real-logarithm selector is an ordinary mathematical construction. An effective version can avoid logarithms, floating point, integration over the component laws, the normalizer $`Z`$ and an infinite posterior maximization. Assume first that each $`a_i`$ and the next centre can be computed exactly as positive rationals with the stated half-separation. Let $`m_i`$ be the least integer $`m\geq1`$ with $`2^m r_i\geq1`$. Then

```math
2^{-m_i}\leq r_i\lt2^{-(m_i-1)},\qquad
L_i\leq m_i\leq4L_i.
```

Use rational boundaries

```math
b_i=a_i\min\left\{\frac34,
       \max\left\{\frac32r_i,\frac1{128m_i}\right\}\right\}.
```

They retain $`(3/2)a_{i+1}\leq b_i\leq(3/4)a_i`$ and the same factor-two decrease. The earlier classification calculation applies, now with

```math
\frac{a_{i+1}}{b_i}\leq(512+8/3)r_iL_i,
\qquad
\exp\left(-\frac{3a_i}{320b_i}\right)
 \leq e^{-1/(160r_i)}+e^{-6m_i/5}\leq81r_i.
```

The first exponential is at most $`80r_i`$ using $`e\geq2`$; the second is at most $`2^{-m_i}\leq r_i`$. Since $`\sum r_i\leq2S`$, the total coefficient is bounded by

```math
101(512+8/3)+\frac{1616}{15}\,162
 =\frac{1041512}{15}\lt70000.
```

Thus replace $`30000S/Z`$ by $`70000S/Z`$ in the strict-width and uniform-critical positive bounds; their head and edge terms are unchanged. The input promises remain different: strict width allows arbitrary component laws, while the critical-width rule requires a uniform law on the entire cluster. A finite observed word does not verify either prior promise. [sparse-effective-theorem], [sparse-rational-contract]

For the concrete rational family

```math
a_i=2^{-(i+1)^2},\qquad r_i=2^{-(2i+3)},\qquad m_i=2i+3,
\qquad S=\frac{11}{18}\log2,\qquad \frac12\leq Z\leq\frac47,
```

the bounds are explicit. This is a dyadic-square family, distinct from the exponential-square example above. Its inverse first moment is again infinite. At a valid input $`n\geq1`$, $`0\leq k\leq n`$, use $`x=\max(k/n,1/n)`$ and select the least $`i`$ with $`x\gt b_i`$. With

```math
B=(n-1).\mathrm{bit\_length}()=\lceil\log_2 n\rceil,
```

half-separation gives $`a_B\leq2^{-B-1}`$, hence $`b_B\leq3/(8\cdot2^B)\lt1/n\leq x`$. The finite search through indices $`0,\ldots,B`$ always terminates. Equality at a boundary proceeds to the next index. In strict-width mode, a selected centre above $`R`$ uses the empirical report and equality at $`R`$ belongs to the tail. In uniform-critical mode, selected centres above $`1/8`$ use the empirical report; a tail empirical mean equal to its centre chooses the left report.

For a general rational ratio, integer bit lengths give a bracket of two consecutive candidate ranks, and an exact shifted-integer comparison decides $`m_i`$. The word route counts the acquired bits and calls the same count core. For this symmetric rule, a truthful count pair and the corresponding ordered word give the same output. The count API does not establish that the caller acquired or truthfully summarized $`n`$ observations; the general history transport above still preserves positions. In the dyadic family, the search uses at most $`\lceil\log_2n\rceil+1`$ candidates, the largest centre denominator has bit length of order $`(\log n)^2`$, and reading a word takes order $`n`$ operations. Arithmetic also depends on the bit lengths of $`\varepsilon`$ and $`\delta`$. These are finite-input termination and representation statements, not unit-cost arithmetic on arbitrary integers or a physical real-time guarantee.

The historical implementation sequence made three consequential distinctions. First, the initial guarded interfaces admitted word lengths from 1 to 1,000,000, count and parameter components up to 4096 bits, and decimal components up to 1234 digits. They required actual integers rather than booleans, exact rational parameters, valid ranges and the appropriate mode promise. These interfaces implement a bounded restriction of the rule. They do not supply a policy on every positive reporting time. Merely switching to the empirical report beyond a fixed cap would not prove a finite budget for a prior whose inverse moment diverges. The first independent review accordingly retained a partial verdict. [sparse-candidate1-review], [sparse-rational-contract]

Second, the later typed cores `decide_counts_unbounded` and `decide_word_unbounded` removed preset length, integer and rational caps, and the word route called the uncapped count core directly. Their exact finite-input termination gives the infinite report family in the mathematical sense. The old guarded APIs and command-line interface remain bounded restrictions, and the uncapped typed core does not promise unlimited memory, unlimited decimal transport or verification of the host interpreter. The source's scope clarification explicitly superseded the first version's insufficient bounded-core claim. [sparse-unbounded-scope], [sparse-unbounded-readme], [sparse-effective-theorem]

Third, removing mathematical caps did not repair a separate decimal-parser defect. With a host integer-string guard set to 640 decimal digits, the whole-string parser rejected the valid count $`n=10^{1000},k=0`$. That input has 1001 decimal digits and 3322 bits, within both advertised guarded caps, although it succeeded with the default guard of 4300. The report formulas were not falsified; the admitted transport domain was. A chunked output routine already worked under the 640-digit guard, including a 4711-digit denominator, so the original result had an input/output asymmetry. [sparse-parser-correction], [sparse-candidate1-review]

The corrected parser validates syntax and length, then accumulates decimal chunks of at most nine digits by $`V\leftarrow10^kV+c`$. Induction on chunks proves equality with the signed decimal value, including leading zeros. Denominator positivity, rational normalization and the advertised bit bounds are checked explicitly. The output routine applies the inverse base-$`10^9`$ decomposition. The correction preserves the host guard, including settings 640, 4300 and zero, and leaves the report formulas and guarded caps intact. It repairs the finite JSON interface; it does not turn that interface into an unlimited serializer. [sparse-rational-final-review]

A distinct test gap was also retained. The initial author's grid omitted the zero-width case, and a mutation replacing the strict-head comparison by its equality-inclusive counterpart survived that grid, even though the original comparison was correct. The independent default-mode check detected it, and the final revision added the missing coverage. A repaired test and parser do not retroactively turn the earlier partial review into a pass. The final candidate's exact version, historical test scope and the distinction between mathematical proof and Python execution are recorded with the source boundary below. [sparse-rational-final-review], [sparse-rational-review-readme]

Together these results distinguish four obligations: the literal target, the joint law of acquired observations, the prior-shape assumptions and the effective reporting interface. Finiteness of an expected error count does not certify a prior from samples, authenticate a normative source, establish a physical sensing process, or grant authority to act. The examples and algorithms make no field-wide novelty claim, and the source reviews do not by themselves qualify this new exposition.



## 10. Assumptions, negative results, and open scope

The positive-fibre and Fisher theorems quantify over the full strictly positive joint-law family. On a constrained reachable family, use its actual differences; the density proof may fail. For example, with three audit outcomes, a binary target, fixed weights $`w_j=1/3`$, and $`J=p_{1,1}`$, equation (12) has $`\dot w=0`$. The section is invariant and its signature is injective, so the flow descends there despite conditional dependence at fixed $`q`$. This does not contradict the full-domain rigidity theorem.

Strict positivity supplies small kernel perturbations, division by weights, feasible audit outcomes, and nondegenerate conditional Fisher tangents. Boundary strata and null events need their own analysis. Ambient $`C^1`$ regularity supports the global classification; $`C^2`$ gives the stated unique $`C^1`$ source flow. Pointwise coincidence at one signature is not a trajectory theorem.

The preserved negative findings are substantive: separate marginals can lose audit-dependent answers; posterior equivalence can lose inquiry value; a conditional loss can have nonprojectable Fisher dynamics; a projectable complete flow can lack ordinary-signature velocity continuity; a target-only flow can reach the boundary in finite time; and finite labels cannot encode a positive-dimensional exact metric fibre.

Unresolved generalizations should be stated as such. This treatment does not classify every globally descending objective for $`k\leq r`$ beyond the exact criterion, provide global minimal charts across changing rank, solve arbitrary adaptive value preservation from posterior-only equivalence, or give stable approximate/noisy variants of every exact construction. Nor does it turn the declared probability law, loss, or metric into an empirical model of cognition or a philosophical judgment about actual warrant.

The certificate-selection and temporal results have a separate finite contract. The message encoder must possess the stated information and supply it truthfully with whatever authorization the application requires. Admissibility, model completeness, source/version eligibility, semantic preservation and actually discharged obligations are premises to be independently established. A one-shot zero-error cover bound is not an expected-rate, privacy, interactive, cryptographic, distributed-synthesis or bounded-error result. The complete temporal characterization assumes a finite common-state game; the rank certificate under incomplete observation is sufficient only. Neither theorem authenticates a source, supplies common knowledge or independent provenance, establishes causal restoration in a real system, or transfers authority to act. Dynamic membership or changed states, observations, targets and transitions require a new adequate model rather than an unproved reuse of the old ranks.

The graph continuation result fixes named binary slots, both edge orientations, silent state-independent words and individual terminal readouts. Its finite-horizon moment family can fail downward closure, and its invariant saturation can omit arbitrary cross-component dependence. A different output or action contract must be analyzed in its own right. The fixed-root strengthening and tree saturation formulas are exact within those stated restrictions.

The proof-cost results require scoped valid derivations, separately warranted source commitments, persistent reusable evidence and the declared terminal checking contract. Their full-acquisition canonical quotient may be finer than a restricted test menu needs. A finite persistent menu gives the complete-transcript criterion; expiry or defeat defeats that simple criterion. Tree compilation tolerates cycles because it prunes finite derivations under exact substitution and nonnegative additive costs, not because cycles prove their own premises. Shared-node checking needs whole-graph information before terminal normalization. These results do not settle unrestricted logical completeness, source trust, semantics, actual cost calibration, or a human subject's epistemic basing.

The unknown-standard results in §9.7 have a different information contract. Their finite-sample constants assume fresh independent Bernoulli observations; their countability conclusions require only the stated common-reference or causal-evaluator hypotheses. Finite harmful probing and infinitely many target-preserving samples support different targets and cannot be substituted for one another. Relative score tolerance, coherence, endpoint slack, measurable prior mixtures and effective realizability remain explicit. No result determines a real normative standard's authority or origin, or treats an unused oracle tail as observed evidence.

## 11. Attribution, evidence, and edition boundary

The predictive observable theorem and its continuous-coordinate proof are inherited from *Continuation-Complete Orthings*, with the established predictive-state ancestry in [8]. Support-sensitive fibre factorization is also developed in the information-and-revision lineage [7]. The audit transport, paired posterior test, fixed-audit classification, and inquiry-value separation are consolidated from [2]–[3]; their exact final source versions have separately bound ordinary reviews. The Fisher classification and its row-rescaling maximal-flow proof come from [4]. That source credits the row-rescaling proof to its finite-audit mathematical contributor; it is not counted as independent corroboration merely because the contributor also served in a review role. The finite and continuous supplement arguments reconcile [5–6].

The explicit discontinuous-signature sequence in §7.4 and the combined utility-coordinate corollary in §9.2 are deductions written out for this exposition. They make no field-wide priority claim and require review as part of this edition. The sources' historical finite controls corroborate their own bounded statements; they do not constitute new execution of this text, universal proof by enumeration, or Lean certification.

The historical sidecar review is conditional on the ambient norm identity and requested normalization of $`q`$; both the identity and normalization are proved or explicit here. A review of audit covariance is not treated as a review of the full Fisher classification. Frozen source text that once said “review pending” is distinguished from its later exact-version review. No unavailable historical output is manufactured.

Section 9.4 incorporates the complete-certificate relation-selection results [13], the repaired distinction between invariant-core entry and co-Büchi persistence [14], model-bound temporal-certificate guards [15], and versioned evidence composition and eligibility reopening [16]. The encoder-information, robust-completion and adversarial-channel boundaries preserve their substantive corrections. The observation-cell qualifier on label distance, explicit optimal five-bit code, inner-removal-rank completeness proof against history-dependent controllers, and fresh-hidden-branch construction are written out in this edition and require its own independent review. They are expository clarifications or deductions, with no new-priority claim. Witsenhausen's exact reconstruction, Orlitsky–Roche's asymptotic function computation, Karp's covering complexity, and Emerson–Jutla's parity-game fixed points supply classical antecedents under their respective premises [17–20]; the present finite statements are proved here.

The four finite certificate/temporal sources have bounded later reviews and preserved earlier failure records. Those historical assessments do not qualify this new exposition by inheritance. Their public adoption boundary continues to distinguish scoped ordinary mathematical results from external review and owner adoption, which remain pending. The original standalone evidence-transport ancestor packets were not newly received; the source's indexed reconciliation is not represented as direct custody of those missing bodies. No private paper or accepted edition is replaced by these finite proposals.

Section 2.4 incorporates the exact graph-constrained result [21] and the independent review's fixed-root formula, horizon convention, counting formulas and limiting cases [22]. The CNOT/Steiner construction has the established antecedent [23]. The full-law interpretation and explicit separating laws retain their distinct mathematical scope; no physical or metaphysical application premise is inferred from the gates.

Sections 9.5–9.6 reconcile the complete warranted-completion treatment [24], its finite support/price kernel supplement [25], and the cyclic/shared rule-compilation treatment [26]. The proofs retain the reviewed corrections: finite admitted prices are distinguished from infeasibility, failed candidate checks are not guaranteed terminal actions, raw reports stay outside the authenticated inventory, a restricted menu need not realize all acquisitions, optimal abstract choices do not identify concrete witnesses, snapshot-negative outputs preserve their scope, and pathwise worst-case cost differs from randomized expected cost. The permutation proof of the equal-price frontier bound writes out a consequence stated in the predecessor's review. The provenance, weighted-deduction and certificate/search antecedents [27–29] are acknowledged without claiming general novelty.

The predicate-decision application in §9.5 comes from [42]. Its cost recurrence is the zero-terminal-price specialization of Theorem 15; the address example, changing-objective cycle and two-world delivery-cost construction retain their own stated domains and model boundaries. These ordinary arguments make no new-priority claim and supply no general concolic-testing, empirical-delivery or self-certification guarantee. The source's bibliographic attributions remain source-relative as specified in its reference entry.

The exact formal source [30] proves the visited-support inequality, synthesis from a finite connected witness, the optimum under a minimum-witness premise, and the local character pullback identity. Its constructive connected-set predicate is not separately identified inside Lean with an imported graph-connectivity predicate, and its unlabelled idle constructor is harmless for an at-most horizon only. Whole physical-word correspondence, the probability-simplex/topological lower bound, fixed-root strengthening, graph counts and saturation remain written proofs. The finite support/price formalization [31] proves normalization, the inverse, necessity and persistent updating in an arbitrary linearly ordered price type with a newly adjoined infeasibility top. Its catalogue, supports and acquisitions are finite; the ambient token type need not be. It supplies original pairs, not admitted derivation objects, authentication or actual terminal execution.

The predecessor reports and reviews record Lean 4.19 certification of these exact formal bodies with the standard dependencies `propext`, `Classical.choice` and `Quot.sound`, and preserve false-strengthening controls. Their historical execution claims remain bound to those sources and their recorded environments. Source inspection here is not a fresh kernel replay, an audit of cached transitive dependencies, or receipt of every historical raw log. The Bellman criterion, semantic cover, finite rule compilation, and tree/shared-graph distinction have ordinary proofs and bounded historical finite checks; they are not added to the kernel certificate by association. The earlier distinction between a finite proof and unrestricted logical or epistemic completeness remains in force. Referenced ancestor manuscripts outside the actual received population receive no new whole-document reading or replacement credit.

Section 9.7 reconciles the complete public continuum-restoration exposition [32] and finite-information bridge [33]. The repair geometry, local-minimax experiment, copied-record boundary, target-preserving positive construction, finite-query obstruction, countable sharpness and philosophical limitations retain their separate premises. The explicit affinity proof, Bernoulli moment-generating-function argument, common-reference lemma and seed/finite-word factorization are written out here. Countability of atoms, contraction under measurable postprocessing, concentration and summable-event reasoning are established mathematical mechanisms; no field-wide novelty is claimed. The concentration antecedent is Hoeffding [34]. The original programme's latent identification, persistent restoration, metric and source-binding connections are expressed here by subject, without using its historical organizational labels as scientific structure.

The two prose sources are public navigation-only projections. This edition incorporates those exact public bodies, not their private originals or custody diffs. The broader support README includes other composition and restoration results and is not replaced in full by this section. Historical “pending” sentences and later recorded formal successes have different scopes: later reports of compilation or copied-source review for particular causal modules do not retroactively certify every ordinary assertion in the initial prose.

The selected formal sources [35–41] distinguish a generic dominated-readout theorem from a concrete evaluator that discharges the domination obligation. The locality proof bounds only one run. The actual finite-query measure construction uses finite words with positive reference mass; it does not dominate every infinite oracle law. The correlated-law construction permits seed/oracle dependence. Its earlier exact-restoration endpoints [38–39] specialize to a common probability seed marginal and probability input laws. Theorem 24 gives the dominated-marginal extension as an ordinary proof here; [40]'s approximate causal endpoint itself allows merely dominated seed marginals and does not require normalized input laws for its measure-theoretic countability conclusion. Probability interpretations impose normalization separately. The formal approximate score inequalities allow real outputs without an extra coherence premise, so the impossibility covers coherent outputs as a subset; the positive constructions here impose their stated range conditions. Source [41] proves the exact atom-mass identity for the literal zero-query evaluator, while the existence and effective-sampling qualifications for an arbitrary countable guessing law remain ordinary mathematics.

These seven public formal bodies were inspected at source level. Their transitive dependency closure, including the imported restoration-countability bridge and Mathlib modules, was not newly read or built for this edition. The predecessor records compilation, axiom-readback and independent copied-source review at their original bounded scopes; source inspection, printed proof-check commands and this exposition's ordinary proofs are not fresh kernel execution or receipt of every historical raw log. In particular the statistical sample bounds, philosophical interpretation and the whole two-source incorporation are not added to a kernel certificate by association. The existing source/adoption and accepted-edition boundaries remain.

Section 5.3 and the retained-history argument in §9.4 incorporate the corresponding bounded constructions in [FORM], *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, version 1 research draft, 8 September 2026. The option values are constructed countermodels; the history theorem is conditional on actual record retention and the separately stated semantic premises. The finite typed representation and future-quotient application appear in [Tensor Moments, §§1.1–1.4](tensor-moments-and-corrective-dynamics.md#11-finite-typed-words-and-their-declared-meaning), while the dynamical estimates appear in [Physical Realisation, §§5.5–5.6](physical-realisation-and-continuation.md#55-coupled-estimates-and-a-residual-error-floor). These mathematical components do not establish a production schema, a completed empirical programme, or the unfinished original N-person theory.

Section 9.8 consolidates the fixed-disturbance continuum proof and its independent ordinary review [48–49], the Beta lifetime boundary and its separate review [50–51], the finite-horizon and deterministic-clock sources [52–53], and the endpoint-density proof [54]. It preserves the empirical learner's sharper pointwise constant, all-policy endpoint quantifiers, initial-report distinctions, seed independence and restrictions on priors and clocks. The elementary proofs are supplied in the subject treatment, so their scientific content does not require reconstruction of a historical research packet.

These references are exact public navigation-only projections. The original private texts and their custody diffs are distinct editions. The recovery introduction and status index [55–56] distinguish recovered source identity, retained predecessor evidence, fresh ordinary review and unavailable earlier formal closures. Their pending-review wording and later source-bound reviews retain their original scopes. In particular, the rate and density sources' separate successor reviews are described by the recovery indexes and integrated-report review; those statements do not claim that every original review archive or raw output has been received or re-executed for this edition. The integrated report's recovered endpoint-program identities and bounded meter remain separate from the ordinary minimax policy variants [57]. No missing fourth formal closure, historical-priority verdict or normative-source authority is supplied by the new synthesis. The historical finite controls corroborate their stated source versions; independent qualification of this new exposition is its own obligation.

### Sparse-prior continuation: source and verification boundary

Section 9.10 consolidates twenty-five exact public continuation notes into the existing fixed-disturbance inquiry treatment. The cluster theorem supplies the spacing criterion and explicit selector [sparse-cluster]; the width and uniform-cluster sources supply the sharp shape distinction [sparse-width], [sparse-uniform]; and the crossover and nonconvexity sources supply the finite-horizon and prior-mixture counterexamples [sparse-crossover], [sparse-nonconvex-review]. The strict-width and uniform sources have both earlier and final editions. Their earlier bodies [sparse-width-previous], [sparse-uniform-previous] and the original ordinary review [sparse-width-review] are preserved as distinct historical evidence. The final extension separately checks the minimal-head constants and interior contamination [sparse-final-extension], [sparse-interior]. A review of an earlier exact text is not automatically a review of a changed paragraph.

The proof here makes explicit the empirical constant 32, the atomic affinity bound, the zero-word overlap charges and the actual observation transport needed to connect those results. Those derivations are part of this exposition's own ordinary-mathematical review obligation. They do not claim a new discovery, an independent rediscovery of their source results, or a fresh formal proof. Classical mechanisms used here include Chernoff's inequality, affinity bounds, Tonelli's theorem, uniqueness of product laws from cylinders, elementary Bayesian decision rules and the strong law. The Hutter comparison credits the primary prediction results under their own observed-loss premises, rather than claiming that the present literal loss contradicts them [sparse-hutter-2001], [sparse-hutter-2003]. The finite observation-loss obstruction and its signed-loss, full-support and scope countercontrols are preserved from [sparse-observation-review].

The earlier root ordinary review checked the crossover and cluster arguments at its named draft identity, with 24 finite cases and 481 rational assertions [sparse-earlier-review]. The later width/shape report distinguishes the ordinary proofs from the formal endpoints [sparse-final-review]. The complete positive smoothing classification, strict-width and uniform-critical upper bounds, continuous bad strips and absolutely continuous contamination are ordinary arguments. The reported formal terminal results concern the actual-process atomic paired prior and atomic non-endpoint mixture, together with selected local geometry and finite-stage kernels. Certifying such kernels does not certify the complete positive classification by association.

The mechanical review reports ten fresh continuation modules and 61 selected author axiom footprints, with 22 reused compiled objects checked against their identities. Its independent probes comprise eight selected footprints, 26 definition expansions and nine theorem readbacks [sparse-mechanical-review]. The corresponding historical rational checks comprise 307,378 author assertions—53,317 base, 92,101 width and 161,960 critical—and 14,460 independent rational controls, including finite interval calculations. Finite controls corroborate those inputs; they do not replace the arguments over all real parameters or infinite time. The source does not claim a fresh build of the full 32-source closure or of upstream Mathlib. It retains a development critical-uniform snapshot that failed to compile while coherence was being added, and a review probe that initially failed because of lexical spacing. Those failures precede the corrected, source-bound successful checks; neither failed snapshot is represented as the accepted final body.

The nonconvexity review separately reports a terminal actual-process Lean nonconvexity theorem [sparse-nonconvex-review]. Its two endpoint priors have coherent `FiniteBudget` witnesses with measurable reports in $`[0,1]`$; the negative conclusion covers all measurable real-report policies for every proper mixture, using the same positive report clock, complete ordered histories and fixed independent seed law. The terminal theorem establishes endpoint finiteness and universal mixture impossibility. The displayed numerical 256 budgets, total-variation and finite-horizon bounds, and the benefit of a truthful supplied side tag remain ordinary mathematical consequences, rather than additional conclusions of that terminal theorem. This incorporation performs no fresh formal replay.

The actual-process comparison has a separate history. The paired review establishes the real-prior pushforward, support and moment identities, and the literal predicate relation; its initial before-and-after policy representations still differed [sparse-paired-review]. The later transport review discharges the full stream-law, history-encoding, policy, indicator and nonnegative-cost transport [sparse-transport-review]. The recorded selections contain eight paired and thirteen transport footprints, 37 expanded declarations and seven independent probes. The source identities cover 20 paired and 21 transport dependency files or objects; the independent rational grid records 12,985 assertions and the author's grid 34,973. The portable replay route described in the accompanying README has a full 22-source/137-path option, but the reported actual verification was incremental. Neither this exposition nor that incremental report claims a fresh execution of that full option or a fresh upstream bootstrap [sparse-transport-readme]. The reviewer had contributed to the earlier sparse-prior proof, but did not author the new bridge and transport implementations; that supports the stated implementation/contract review, not a claim of independent discovery or priority.

The observation-loss report records four fresh modules and eight selected standard-only axiom footprints. Its comparison with Hutter is an interface analysis, not a new proof or re-execution of the cited prediction theorems. Across these historical formal reports, the listed standard dependencies are `propext`, `Classical.choice` and `Quot.sound`. Their reported kernel and dependency results remain attached to the exact original bodies and environments. Reading them here is not a new kernel run, receipt of every historical raw output, or certification of the whole new prose.

The rational implementation records preserve a different kind of evidence. The initial contract and independent candidate-one review distinguish the correct rational decision formulas from the missing uncapped reporting family, the in-domain decimal-parser failure and a missed mutation [sparse-rational-contract], [sparse-candidate1-review]. The later scope clarification and README introduce the uncapped typed core while retaining the guarded interfaces [sparse-unbounded-scope], [sparse-unbounded-readme]. The effective theorem supplies the rational rank bound, finite search and cost proof [sparse-effective-theorem]. The parser correction identifies the restrictive host guard as a transport failure on an otherwise admitted input [sparse-parser-correction]. The final exact-version review then assesses the repaired interface and added zero-width coverage [sparse-rational-final-review], [sparse-rational-review-readme]. None of those later results erases the earlier partial verdict.

The first candidate's historical author suite recorded 11,184 assertions and three mutation controls; the independent review recorded 16,784 assertions over 2,089 decisions. Its ten semantic mutations included the eventually detected overly broad critical-tolerance change, and the strict-head equality mutation exposed the author's original zero-width gap. The final candidate's author results recorded 14,892 guarded assertions, 673 uncapped assertions, 24 checks across host decimal-guard settings and five mutations. The independent final review retained the 16,784 earlier checks and added 436, totalling 17,220 assertions, including 91 uncapped decisions. Its large-input controls included 65,537-bit values, a word of length 1,200,001 and a 78,914-digit denominator with the decimal guard set to 640. Ten general and seven repair-specific mutation controls and five nested archive identities are reported. These are historical bounded tests, not a proof of the Python interpreter or of every possible resource environment.

The final reference implementation is identified in that review by SHA-256 `28dcd6c5c6e2a5a43fe186c7d099f2165f319c864821024de9dd6e14d11744b9`. Its predecessor implementation and the review archives have their own retained identities in the cited notes. The finite JSON cap, external prior-shape promises, truthful-count premise and independent-seed contract remain part of the result even after the parser is corrected. No historical program, scorer or formal replay is newly executed by incorporating these notes, and no unchanged predecessor scientific result is counted as a new incorporation merely because it is invoked in a proof.

All twenty-five references below identify the exact public note bodies at a fixed repository revision. Their incoming-packet dates, filenames, replay locators and verdicts are historical provenance, not instructions or present authority. This amendment supplies a subject-level home for their arguments, countermodels, interface failures, credits and limits. Its independent scientific review and owner adoption remain separate obligations. It neither replaces private or held source editions nor claims access to their bodies, and it supplies no normative-source authentication or field-wide priority adjudication.


### Generated binary experiment: source and audit boundary

The fixed-disturbance example in §9.7 incorporates the complete public mathematical benchmark *One exact composition of score repair and controlled restoration* [43] and its independent composition audit [44]. The earlier geometry, statistical and continuum incorporations remain distinct; this addition does not count those already incorporated sources again. The new ordinary affinity calculation concerns the stated common likelihood policy and acquired-history law, and confers no new kernel-execution status.

The predecessor identifies `IntegratedBinary.good_iff_same`, `IntegratedBinary.supports_self_verifying`, `IntegratedBinary.canonical_repairs_eventually_good`, `infinite_product_coordinate_law`, `infinite_product_coordinates_independent`, and `IntegratedBinary.generated_experiment_eventually_repairs` as its source endpoints. The last endpoint has the disturbance and its interval hypotheses, the true index identifying the law, and a fixed initial choice. The reported dependency chain proves its literal target relation, normalization, coordinate laws, independence and selector maximization. It does not treat the unknown true index or an unacquired observation as a controller input. The eventual event is measurable because `selectedRepair` and the actual score predicate are measurable and the eventual-event formula uses countable unions and intersections. This is a sufficient full-support two-model result; a complete general necessity or zero-support classification has a separate scope.

The audit reports fresh compilation of eleven copied modules under Lean 4.19.0 and pinned Mathlib: the three root modules `ProductObservationLaw`, `IntegratedBinaryRestoration` and `GeneratedBinaryExperiment`, plus eight full-support control modules. The ten-module causal closure and `BlindGuessSharpness` are eleven **retained prerequisites**, whose earlier fresh objects, sources and receipts were checked rather than rebuilt. Its 107 declaration type/axiom readbacks include definitions and instances; they are not 107 separately proved theorems. The reported axioms are `propext`, `Classical.choice` and `Quot.sound`. It also reports thirteen independent theorem controls, a final-signature guard and three rejected source mutations. The finite rational controls cover both fixed Boolean list orders, are distinct from the measure-theoretic eventual result and are not extracted execution of the noncomputable selector.

Those are historical source-report claims, preserved at their original scope. This consolidation did not rerun the compiler, inspect every original raw log or regenerate prerequisite objects. The audit's failed attempt to evaluate a noncomputable finite-set list remains a failed development attempt, not accepted proof evidence. Its positive logs and expected-rejection logs retain their different roles. The accepted-record names are `REPLAY_RESULT.json`, `AXIOM_READBACK.json`, `CONTROL_RESULT.json`, `FINITE_CONTROLS.json` and `RETAINED_PREREQUISITES.json`; their recorded original-packet locators and the source's seal `cb19cd28f4d7f033a22a16c1f6cd6896607d0fbe44681f13d6a140e462cba4e1` are custody identities, not portable commands or newly acquired archives. Reproduction would require the actual pinned prerequisites and source-order checks; no such reproduction is asserted here. Independent model-assisted review remains separate from external peer review, novelty, canonical adoption and release acceptance.


### From the integration probe to the causal countability endpoint

The ordinary research probe *Local correction geometry → information cost
→ persistent restoration* [45] proposed a composition problem, with
constants, quantifiers and the adaptive finite-probe proof still open in
that note. Its arbitrary-input identity and interior decoder estimate
are proved in §9.7 above. Theorem 20 supplies the later explicit
finite-confidence constants for the specified Bernoulli experiment,
not a pointwise rate at every fixed standard. Theorem 22 supplies the
observed-trace argument through deterministic prefixes. Proposition 21
supplies the target-preserving positive construction. Their common
output and loss must remain the same when these results are composed;
the action, observation and permission hypotheses remain additional
premises. The probe's request to investigate primary literature and a
real application was a research duty, not an assertion that either was
completed. Its original date, pending wording and lack of a kernel or
priority claim retain that historical meaning.

The complete public *Independent fresh proof-spine audit* [46] and
*Causal finite-query restoration: independent audit* [47] explain which
parts of that progression were reported as formal proofs. Their
populations are different:

| Historical source stage | Reported positive scope | Boundary that remains |
|---|---|---|
| Initial fresh proof spine | Four modules: `StatisticalRepair`, `CountableIdentification`, `RepairObstruction` and `RepairTestingBridge`; a separate five-module snapshot adds `RestorationCountability`. | The finite formal testing result is the bound by one quarter of the squared affinity. The stronger square-root bound, exponential simplification, sample complexity, concentration construction and adaptive postprocessing reduction are ordinary arguments. |
| Generic and applied countability | A shared measurable readout with an s-finite common reference; literal eventual score inequalities imply convergence, and a restricted-domination premise gives countability. | The generic result permits an outer-measure reading of success. The initial applied theorem does not construct the controller, its observed law, the finite-probe event or the domination proof. |
| Later causal/query-chain closure | Ten copied modules; actual Boolean-query locality, finite-word trace domination, seed/oracle correlation and one measurable eventual score/no-query event. | Its exact-restoration endpoint uses common probability seed marginals. The dominated-marginal extension proved here and the later additive-tolerance successor have separate scopes. This report does not certify that later successor. |

The initial applied theorem uses a real-indexed measure family. An
application on the open parameter interval can extend that family
harmlessly outside the interval; this typing choice neither adds a
physical standard nor proves the observed-law construction. The
probability interpretation still needs normalized actual laws and
measurable success events.

The first audit reports twelve independent boundary theorems, an
additional event-measurability lemma, three deliberately rejected
extensions and 6,797 exact-rational checks. Its zero-sample control has
exact randomized testing risk $`1/2`$; the weaker formal lower bound
$`1/4`$ is not an exact-risk formula. Its refreshed snapshot records the
correction from an unused raw-oracle path to the observable trace and
from a sigma-finite label to the explicit s-finite hypothesis. The
initial snapshot and failed audit-control drafts retain their earlier
status. The original four-, five- and refreshed-snapshot compilations
and the separately named immutable replay are separate execution
records, not populations to add as newly proved theorems.

The causal audit reports type and axiom readback for 100 named
declarations, including definitions and instances, an explicit final
signature guard, eighteen boundary theorems and four rejected source
mutations. Its finite controls report 244,944 prefix/lasso checks across
5,832 three-state Boolean-query controllers, including 34,992 checks
with zero query budget; 44,880 exact-rational strict-repair cases; and
two opposite correlated joint laws with all sixteen finite joint
events. These finite populations supplement its general proof. The
package-root, formatting-option and control-elaboration development
failures remain failed attempts, distinct from the accepted terminal
receipts and intended negative results.

Both reports describe their pinned Lean 4.19.0/Mathlib environments,
audit-local custom objects and standard axiom dependencies
`propext`, `Classical.choice` and `Quot.sound`. They report no `sorryAx`
or new source axiom in the inspected targets. This paragraph preserves
their claims; it does not reproduce a toolchain bootstrap, a fresh
kernel replay, dependency-cache validation or receipt of every
original log. Their manifests, exact commands, object hashes,
readbacks and negative fixtures remain historical reproducibility
records at the pinned source editions. The mathematical proofs and
counterexamples needed for this chapter appear above. No original
private source, general arbitrary-sensor realization, normative
authority, effective deployment, external peer review or canonical
adoption follows from those reported checks.

**Edition status:** new source-bound consolidated exposition. The companion review record binds the exact text, source population, independent findings, corrections, and proposed predecessor retirement. Review of this exposition does not confer owner acceptance or silently amend an accepted paper. None of those records is needed to follow the mathematical arguments above.

### Common-path and physical-action interfaces

Section 9.9 incorporates the [common-observation proof and controls][common-observation-review], its [compactness extension][common-observation-source], the [ordinary necessity proof][necessity-proof] and the [seeded actual-law review][seeded-necessity-review]. The recurrence selection is also documented in the [independent recurrence review][recurrence-review] and its [formal scope note][recurrence-scope]. The [generic query review][generic-query-review] supports the finite-query transfer with its product-law premise; the more permissive common upper-reference theorem in §9.7 retains its different conclusion.

The [policy-equivalence review][micro-equivalence-review] and [static-menu review][static-license-review] are reconciled with the already developed controlled-restoration theorem in Collective Inquiry §7.11. The [generated-process review][generated-process-review], [recursive-action review][recursive-action-review], [pathwise flattening review][physical-flattening-review] and [measurable decoder review][measurable-physical-review] distinguish planned blocks, stopped outcomes, recorded acquisitions and physical actions. The proofs above preserve their nonempty-block, freshness, true-retention and index conditions. The [root review][root-cold-review] and [formalization register][formalization-scope] retain the finite-model and standard-Borel boundaries of their respective arguments; an ordinary statistical passage is not certified by a neighboring formal module. Source code, historical target counts and execution logs remain independently scoped evidence, not newly executed tests or new incorporation credit for results already present in the accepted works.

### References

1. Orthemology. *Continuation-Complete Orthings: Sharp information loss, minimal predictive memory, and safe strategic composition*, finite predictive closure, sharp moment recovery, approximate memory and continuation-preserving reduction, treated in §§2.2–2.6. Its reduction identities and strategic arguments are treated in [Physical Realisation, §5.4](physical-realisation-and-continuation.md#54-what-an-eliminated-variable-can-leave-behind) and [Collective Inquiry, §5](collective-inquiry-and-strategic-coordination.md#5-strategically-sufficient-information-and-hard-coordination). [Exact source][1].
2. Orthemology. *Audit-aware continuation: exact predictive state and posterior-only tensor test*. [Exact final result][2]. Its final independent review binds that version separately.
3. Orthemology. *Posterior continuation is insufficient for expected inquiry value*. [Exact final result][3]. Its later independent review establishes the scoped ordinary-proof disposition despite the earlier pending-review sentence.
4. Orthemology. *Finite-audit Fisher descent: exact criterion and sharp cardinality threshold*. [Complete proof source][4].
5. Orthemology. *When the finite sidecar theorem meets a continuous audit fibre*. [Corrected corollary][5].
6. Orthemology. *Operation-preserving representations*, finite refinement and minimum supplement theorems, and the all-objectives cometric criterion. [Source, selected results only][6].
7. Orthemology. *Information, Composition, and Self-Revision: Local Descriptions and Operative Access*, feasible-support factorization and observation congruence. [Source][7].
8. Michael L. Littman, Richard S. Sutton, and Satinder Singh. “Predictive Representations of State.” *Advances in Neural Information Processing Systems 14* (2001 conference). [Primary proceedings paper][8].
9. Stefan Kiefer, Andrzej S. Murawski, Joël Ouaknine, Björn Wachter, and James Worrell. “On the Complexity of Equivalence and Minimisation for Q-Weighted Automata.” *Logical Methods in Computer Science* 9(1:08), 2013. DOI: 10.2168/LMCS-9(1:08)2013. [Primary paper][9]. Used for product and finite-span ancestry, not an attribution of the exact posterior theorem.
10. L. E. J. Brouwer. “Beweis der Invarianz des n-dimensionalen Gebiets.” *Mathematische Annalen* 71 (1911), 305–313. DOI: [10.1007/BF01456846](https://doi.org/10.1007/BF01456846). The publisher dates the article September 1911; the [digitized bound volume][10] is catalogued as 1912. The classical invariance-of-domain theorem is invoked in the continuous lower bounds; its proof is not rederived here.
11. Orthemology. *Audit selection as a genuine higher-order information interface*. [Exact parity and regret derivation][11].
12. Orthemology. *Zero-probability audit: an exact finite boundary*. [Corrected null-event argument][12].

13. Orthemology. *Certificate-object refinement, robust relation selection, and temporal custody*, final corrected finite source exposition. Git blob `0481d18ba723490d8eaf910d8f319138df95decc`, in the [pinned public baseline][13].
14. Orthemology. *Invariant-core entry versus general co-Büchi restoration*, corrected finite source exposition. Git blob `84d5005582da703ab146f9e2d26e8baa4aa08ed9`, in the [pinned public baseline][14].
15. Orthemology. *Local closure, temporal nonidentifiability, and model-bound restoration certificates*, corrected source exposition. Git blob `232ff53bbdad7d402fc9e521eaf3c82e32dd5e78`, in the [pinned public baseline][15].
16. Orthemology. *Version-custody transport, reason-graph composition, and temporal eligibility reopening*, corrected finite source exposition. Git blob `b665083608bc30a5dcf8faf54a1c1efdccae4621`, in the [pinned public baseline][16].
17. H. Witsenhausen. “The zero-error side information problem and chromatic numbers (Corresp.).” *IEEE Transactions on Information Theory* 22(5) (1976), 592–593. DOI: [10.1109/TIT.1976.1055607](https://doi.org/10.1109/TIT.1976.1055607). Reconstruction with decoder side information supplies ancestry, not a substitute for the relation-selection proofs.
18. Alon Orlitsky and James R. Roche. “Coding for computing.” *IEEE Transactions on Information Theory* 47(3) (2001), 903–917. DOI: [10.1109/18.915643](https://doi.org/10.1109/18.915643). The [author manuscript][18] uses normalized block rates and vanishing error; that formulation is distinguished from the one-shot pointwise zero-error contract here.
19. Richard M. Karp. “Reducibility among Combinatorial Problems.” In R. E. Miller and J. W. Thatcher (eds.), *Complexity of Computer Computations*, Plenum Press, 1972, 85–103. DOI: [10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9). Set Covering is item 6 of the completeness theorem; see the [authorized reprint][19], original p. 94.
20. E. Allen Emerson and Charanjit S. Jutla. “Tree Automata, Mu-Calculus and Determinacy (Extended Abstract).” *Proceedings of the 32nd Annual Symposium on Foundations of Computer Science*, 1991, 368–377. DOI: [10.1109/SFCS.1991.185392](https://doi.org/10.1109/SFCS.1991.185392). The [author manuscript][20], §§4.1–4.2, supplies nested fixed-point and history-free parity-game ancestry; Theorem 12 proves the stated finite specialization directly.

21. Orthemology. *Graph-constrained unary continuation and exact parity cost*. [Complete result][21].
22. Orthemology. *Independent review of graph-restricted unary continuation masks*. [Exact review][22], including the fixed-root formula and finite-horizon counts.
23. Vivien Vandaele, Simon Martiel, and Timothée Goubault de Brugière. *Phase polynomials synthesis algorithms for NISQ architectures and beyond*. arXiv:2104.00934v1 (2021), §§2 and 4.1. [Primary paper][23]. The connecting-tree formula is explicit on PDF p. 10.
24. Orthemology. *Warranted completion with proof-sensitive memory and inquiry cost*. [Complete final result][24]. Its independently reviewed revision separates terminal eligibility from executed checking and retains the restricted-menu and randomized-objective qualifications.
25. Orthemology. *Kernel certification of the canonical residual-certificate theorem*. [Exact scope report][25], covering the finite support/price theorem rather than the Bellman or epistemic claims.
26. Orthemology. *Compiling certificate frontiers from finite grounded rules*. [Complete final result][26], with separate tree and shared-graph checking contracts.
27. Todd J. Green, Grigoris Karvounarakis, and Val Tannen. “Provenance Semirings.” *Proceedings of the 26th ACM SIGMOD-SIGACT-SIGART Symposium on Principles of Database Systems* (2007), §§3–5. [Primary paper][27]. Positive annotations, derivation-tree semantics and recursive fixed points provide ancestry; the current Pareto statements are proved above.
28. Joshua Goodman. “Semiring Parsing.” *Computational Linguistics* 25(4) (1999), 573–606, especially §3.2 and the discussion of non-improving Viterbi loops. [Primary paper][28].
29. Harry Buhrman and Ronald de Wolf. “Complexity Measures and Decision Tree Complexity: A Survey.” *Theoretical Computer Science* 288(1) (2002), 21–43, introduction and §4.1. [Author manuscript][29]. This supplies the standard certificate/query distinction, not the source-entitlement premises of §9.5.
30. Orthemology. *Graph continuation: finite support synthesis and observable identity*. [Exact Lean source][30]. The independent source review distinguishes formalized claims from the surrounding ordinary mathematics.
31. Orthemology. *Finite certificate frontiers and persistent acquisition*. [Exact Lean source][31]. The separate positive controls distinguish cost-sensitive pruning, present-cost insufficiency and collapsed-infinity failure.

32. Orthemology. *Continuum standards: the finite-information restoration barrier*. [Complete public projected exposition][32], including its common-reference, causal-evaluator, approximate-tolerance and blind-guess successors. Private originals and custody diffs are outside this edition's received body population.
33. Orthemology. *Finite-information cost of unknown-standard repair*. [Complete public projected bridge][33]. Its geometric necessity, local-minimax cost and target-preserving sufficient construction have distinct hypotheses.
34. Wassily Hoeffding. “Probability Inequalities for Sums of Bounded Random Variables.” *Journal of the American Statistical Association* 58(301) (1963). DOI: [10.1080/01621459.1963.10500830](https://doi.org/10.1080/01621459.1963.10500830). The needed Bernoulli specialization is proved above.
35. Orthemology. *Countable Identification*. [Exact public Lean source][35], for common-reference exact readouts, restricted events and explicit countable-sum reference conditions.
36. Orthemology. *Finite Query Locality*. [Exact public Lean source][36], for actual Boolean-query execution and one-run prefix locality.
37. Orthemology. *Finite Query Measure*. [Exact public Lean source][37], for common trace domination from an independent seed and arbitrary actual oracle law, with its declared imported bridge.
38. Orthemology. *Correlated Oracle Measure*. [Exact public Lean source][38], separating marginal domination from its specialized exact-restoration endpoint.
39. Orthemology. *Eventual Causal Restoration*. [Exact public Lean source][39], for one eventual target on actual executions.
40. Orthemology. *Approximate Repair Identification*. [Exact public Lean source][40], for relative-tolerance decoding, the causal countability endpoint and the no-information linear-tolerance counterexample.
41. Orthemology. *Blind Guess Sharpness*. [Exact public Lean source][41], for the literal evaluator's exact atomic success mass.

42. Orthemology. *Reflexive Revision under an Evidence Budget: Decision cost, evidence reuse, and self-application*. [Exact version 3 source][42]. Its bibliography supplies the attributions to *Knowledge and common knowledge in a distributed environment*; *Complexity measures and decision tree complexity: a survey* (also listed above as [29]); *DART: directed automated random testing*; *CUTE: a concolic unit testing engine for C*; and *Predictive testing: amplifying the effectiveness of software testing*. Those five primary bodies were not reacquired or newly verified for this addition; their source-provided metadata remain available in the linked bibliography.

43. Orthemology. *One exact composition of score repair and controlled restoration*. [Complete public projected benchmark][43], for the two fixed standards, literal score target and generated common feedback controller.
44. Orthemology. *Generated binary experiment: independent composition audit*. [Complete public projected audit][44], preserving its coupled-sensor and dependence controls, historical proof boundary and failed development attempt.

45. Orthemology. *Local correction geometry → information cost → persistent restoration*. [Complete public projected integration probe][45], begun 30 September 2026. Its candidate status, research duties and original evidence limits are retained in §11; the general binary identity and decoder are proved in §9.7.
46. Orthemology. *Independent fresh proof-spine audit*. [Complete public projected audit][46], 30 September 2026. Initial and extension snapshots, ordinary adaptive-observation reasoning, counterexamples and formal ceilings retain their separate historical scopes.
47. Orthemology. *Causal finite-query restoration: independent audit*. [Complete public projected audit][47]. The ten-module exact causal/query closure, correlated-law controls and finite checks are distinct from the later additive-tolerance successor.

48. Orthemology public research. *Continuum literal-repair cost boundary: fresh recovery successor*. Complete public projected proof, including the fourth-moment constant, endpoint semicontinuity argument and distinct minimax pairs. [Exact public edition][continuum-cost].
49. Orthemology public research. *Fresh independent review of continuum literal-repair costs*. Complete projected ordinary review of the exact recovered proof, with its finite controls and missing-formal-evidence limits. [Exact public edition][continuum-cost-review].
50. Orthemology public research. *A sharp Beta-prior boundary for finite expected literal mistakes*. Complete public projected derivation, preserving the passive fixed-parameter clock and all-policy quantifiers. [Exact public edition][beta-budget].
51. Orthemology public research. *Fresh independent review: Beta-prior finite-mistake boundary*. Complete projected ordinary review, including real-shape CDF scaling, seed conditioning, the initial-prefix countercontrols and the inherited empirical upper. [Exact public edition][beta-budget-review].
52. Orthemology public research. *Optimal finite-horizon growth under Beta uncertainty*. Complete public projected proof of the rate comparison, concentration estimate and exact Bayes existence statement. [Exact public edition][beta-rates].
53. Orthemology public research. *The exact deterministic reporting-clock trade-off*. Complete public projected corollary, with repeated evaluations and the adaptive-clock exclusion. [Exact public edition][report-clock].
54. Orthemology public research. *Endpoint-density robustness of the literal-failure rates*. Complete public projected proof for two-sided punctured-endpoint density envelopes, arbitrary compact-interior measure and separately handled endpoint atoms. [Exact public edition][endpoint-density].
55. Orthemology public research. *Fourth research recovery return*. Public projected recovery introduction. Its index describes a broader source population than the mathematical bodies integrated in §9.8; indexing is not scientific proof or a new receipt. [Exact public edition][t4-recovery-introduction].
56. Orthemology public research. *Recovery evidence status*. Public projected status index distinguishing fresh ordinary review, recovered source custody and unavailable original formal closures. [Exact public edition][t4-recovery-status].
57. Orthemology public research. *Final integrated fourth-tranche claim review*. Public projected review of a separately frozen 21-page report, its text companion and source membership. Its original report identities and source-specific scope are not reassigned to the present work. [Exact public edition][t4-report-review].

Repository references identify exact public source editions, not mutable current filenames. The broader works in references 1, 6, and 7 contain additional results and are not replaced in their entirety by this chapter.

[1]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/theory/lineages/h-continuation/continuation_complete_orthing.md
[2]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/3add44ffbe7e0bf188f870259bce338387385e1e5c04a5d98a3716cb2c2a84cc/RESULT.md
[3]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/5f6f84b1af7e5049139a381142a791eb7aeebdb57ebf9095e14fa49cfc652fcf/RESULT.md
[4]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md
[5]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/research-v6/root_math/FINITE_SIDECAR_GEOMETRY_BOUNDARY.md
[6]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/8aad39f6fb030620059edd4e0639f58078537a10181836b64089f6d82dbe10f4/whole.md
[7]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex
[8]: https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf
[9]: https://people.mpi-sws.org/~joel/publications/Q_weighted_automata13.pdf
[10]: https://gdz.sub.uni-goettingen.de/id/PPN235181684_0071
[11]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/84b17193706810cbf7d85b62b7dd9fffc1f5d9712816ae4558a9a342af9dc4fc/TRIPLE_INTERACTION.md
[12]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/c202f660a5458a6fbc5f597b9e1645fc9a0d25361055abdcf8b8dd45d5186016/ZERO_AUDIT_BOUNDARY.md

[13]: https://github.com/theislampill/orthemology/commit/a7ff0e33d1a299db640041c46b1af81ca70851f6
[14]: https://github.com/theislampill/orthemology/commit/a7ff0e33d1a299db640041c46b1af81ca70851f6
[15]: https://github.com/theislampill/orthemology/commit/a7ff0e33d1a299db640041c46b1af81ca70851f6
[16]: https://github.com/theislampill/orthemology/commit/a7ff0e33d1a299db640041c46b1af81ca70851f6
[18]: https://9p.io/cm/ms/former/alon/papers/funcom.ps.gz
[19]: https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf
[20]: https://www.cs.utexas.edu/users/emerson/Pubs/1991-10.ej.FOCS.ta-games-mu.ps

[21]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP19/graph-constrained-continuation-20261009/RESULT.md
[22]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP19/graph-continuation-review-20261009/review.md
[23]: https://arxiv.org/pdf/2104.00934
[24]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-research-20261009/RESULT.md
[25]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/RESULT.md
[26]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/RESULT.md
[27]: https://www.cs.ucdavis.edu/~green/papers/pods07.pdf
[28]: https://aclanthology.org/J99-4004.pdf
[29]: https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf
[30]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP19/graph-constrained-continuation-20261009/GraphContinuation.lean
[31]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CertificateFrontier.lean

[32]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f.md
[33]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e.md
[35]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/2df7c47363350f3eb58e07495b1b20319baab5847d3cc0998d7aef2d02a09720.lean
[36]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/13eab28f535c45cdf0347e27913ebd5b18f5dda07f6dac8f2774afd2ad57c8c6.lean
[37]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f018854d64b5885a992b41c1180a551063dfe66603951901a9d2b65645883280.lean
[38]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/2807aaf24bd997dd5b61acbbadef86d6dbae18ef3c986c7f49252e36fe26d4cb.lean
[39]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/7551d3dbf744250a840e0cbb224654a6d8973da353aaa1f6cede18d64ea47a4d.lean
[40]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/16f467976b9d30b5fe1bfa5997e7378dcf391e989d17aaed4e69224da0686261.lean
[41]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/75d8ceba960b2ae9698515d20e05badd9257fcab10a8a60bf295aad36eb21395.lean

[FORM]: https://github.com/theislampill/orthemology/blob/28679eaed33ee48cf0c5d15ba6dc3b27aac9067b/theory/lineages/h-formalisation/orthing_formalisation_v1.md

[42]: https://github.com/theislampill/orthemology/blob/c1a30e5ab19c2160e469b0632d3bdad48ad4b0e8/theory/lineages/h-reflexive-v3/reflexive_revision_evidence_budget_v3.tex

[43]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/b0672a56d007c718a42a7ee6fdc875c915630ad95dff5cfbae7f7e9a419d5349.md
[44]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/0da619bf120570139cb2708ea79ba2a05bf20f8be6718f1e21fc3140632610d6.md

[45]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/c2ad91390d3bb80c2e1d0a371494b146222aa7c4d6608abef0dff703d83f111b.md
[46]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/f2d0dc0727817a58c17361252a3c2be4c020cc4d287b627535e742e3b276efef.md
[47]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/4568e570dee3bc029c65f4208c8d1e969578096d3aef529df0a1609173c7b4fa.md


[continuum-cost]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/196728a62cb7bdb24160b33c0ae3627a822f8b2b031fe033e275d6d284efa7df.md
[continuum-cost-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/575700cb383a6f0849e2a952ba6652e6de75920eb74ebcb9a7eb0ed21517a696.md
[beta-budget]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/285a7061f8f090946e27e5ff6bd7597b7a0f0472100c7e4b3cb57ea5ac12f6a7.md
[beta-budget-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/826c824188b79a5e734c77f4aaa24f5ecf15d1a73e7af0d68ad8b8955bb674ab.md
[beta-rates]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/3b8f7d96fa99674b73cb8f822cc3291d455c52879b2f1110630be67660883317.md
[report-clock]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/3b7cdb283b858339136beb1e0d62cbd32adce0ee9f0562db8961a9f819f52000.md
[endpoint-density]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9.md
[t4-recovery-introduction]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/c8dc35d9a1f4ae42417737923ca5bc276d80d60a0865655a34b55de83570d6ee.md
[t4-recovery-status]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/32266a84e5e96404970a7420dc690e71db78323281fd10805a899c6ca67b52e2.md
[t4-report-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/9412522bec33bc12a790e1610d328b160a00cf25eea03126ec219f01abc5e5ac.md

[common-observation-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/ad15c28206a020cc7c063c17309d6bd3c05e182377a398c7507875523df7feb4.md
[generated-process-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/1b7488aeafc74b7115479a8cf73c0abf04d89c3924109aa922ee6099e32be2d8.md
[generic-query-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/9e00aaaaa63828e05d252e134dc225e2718461540301138a30567fbb63a24eb9.md
[micro-equivalence-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/673111801ec83a2118743de3cd851f7a3db8e6c9580750f3fe766a9626b0f498.md
[static-license-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/bd5e18cb3616a7ead45cc407da8ebe72274358edcd12459f4109ad155e2f53b2.md
[necessity-proof]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/50cf2306b486db59fd7a2ecf77d07b3b54c3e486745f0b7308cb091de1c3ec61.md
[recurrence-scope]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/1f97b7f6e879f4ebe42b26620aac0c75095345f4ec65bfe2979ecd32aa538dbf.md
[measurable-physical-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/e6be2257c2dabfd15057f1c59603518d1ba20976068579bd31512ec1f5bfafce.md
[physical-flattening-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/ad4909aa4015f759a7494c5a0b5ddfa0c4ccaaf6d14ad7c89386db53e01385d6.md
[recurrence-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/63494364aeb423cecee01e1b347a4dfed7e2c4b544c90d456465520378810d40.md
[recursive-action-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/18c1e07537712caaadf60d6bf8f25272aaf8c1767722bd56b3b5f1ed7258ee73.md
[common-observation-source]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/71899f46c0346c901fd19697436beaa511b9814f879835604bbe23264d062aeb.md
[root-cold-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/51c98ce4cbc011f1e4d4d2af7fa9a34319f53713b876977bc9b16c74f0e258dc.md
[seeded-necessity-review]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/890c6bc8949f630878e9d3de6bed22c7070d0b4f0d7c43d7fa96f4c7a6d91607.md
[formalization-scope]: https://github.com/theislampill/orthemology/blob/b4d58482ae00f138782276ee5c4034c48bb2df19/docs/provenance/v5-research-continuations/notes/71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e.md


[sparse-rational-review-readme]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/0ba213e9f1cd5c985925864d7edcc505c3adb16fa30036338b39ad04b77ea54f.md
[sparse-paired-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/22c70614cb4a011790e348461f3e2fbea5e13b2eeb788dcd2124560fb0ef0f07.md
[sparse-rational-contract]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/236f78b5ecc313f47085a765f26ef2f0482fdaff154c2aebb7393a8c01c59236.md
[sparse-rational-final-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/251394f394fe75f9062aaa4dea33da2b3ffa3370572e14ba60e52ceb1c68a30b.md
[sparse-final-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/3cdf7cb6582b44a2198ce9527847416ee834aa7636999871081e1677600a9f60.md
[sparse-effective-theorem]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/6b796642b23d6280cfec717f7a762a55fe76a2fbc67b16f6c6b0fc1008599476.md
[sparse-width]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/767be5173842b1520af940db691120091d868677754e7b452a0c7467ece4665d.md
[sparse-earlier-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/87cad31677966946661ca6effed55165db3505d1bca45bfa6ba2428946cca88c.md
[sparse-mechanical-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/893aabc2774f6a31df5777a9dab8cc4de2840a2f01d95691ce913f0406ab489c.md
[sparse-final-extension]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/99847d69a9a9df978a7e596cc35b75b744e7661b72dd514d29bc3cf4d897cc6c.md
[sparse-unbounded-scope]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/9c7508259cb9916b1ba6b0557584cff186487d256dac3918269052b4cd5626b6.md
[sparse-transport-readme]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/b0edcf2ebfe71957a789033dec063424e658fe8971ef28e1f2fe9a4956e5d18e.md
[sparse-interior]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/b1a029f0cd442ff623d9783c15e09260cd6063bf976290010b3fba07ec0548bf.md
[sparse-cluster]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/b3403229c91a718f3e8c61068649590ec090d208206d9922da2270f71e956658.md
[sparse-nonconvex-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/b545637a8dc1bdfda4a949dfe3a6084b469c5ef8639af8ae97b8e5fef683e0d3.md
[sparse-observation-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/b6a6db5048293e4de7f286689ea635448ea61aec5f9a08acff0968892e10b5bb.md
[sparse-crossover]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/c079f7733904976a602adae47284062ad23141dd9c79b04652e3561e74692a50.md
[sparse-unbounded-readme]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/cab3e124b6ef2faad2c945c20d22d50e7fc2d1455367bcd4cb6dcf633908b3b9.md
[sparse-width-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/d519d3b51e5f03f7b55db3c22c2a423bdb6cf5a702e726e4a57459e527ab8dbd.md
[sparse-width-previous]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/daa7e92aaeee1cc9ae5601877a01ddfbb8ce2cf9cabf3f4f693ec8a7c8a0893b.md
[sparse-uniform]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/e2afa027d652771010f909eb34642d5512c102a34c85a0ef90ff466b9fd7e0ae.md
[sparse-uniform-previous]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/e2cf470975d1d6f344d3dd788410c911b5d6f9d93fa528709339322bcb4d8f6b.md
[sparse-transport-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/e40d89c1d65f9053bafc6aea41ba93af0b510586ba188e14ba5a8f6d9a50c71f.md
[sparse-parser-correction]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/f0fe93679a7c062a452bd3b3b2615c886dcdf8b96579af2d1ddd2c17c6df6459.md
[sparse-candidate1-review]: https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/f7f610f5225df88d97fb6a60f984a7ec976632697e2e3f7854f4777994601d4a.md
[sparse-hutter-2001]: https://hutter1.net/ai/ploss.pdf
[sparse-hutter-2003]: https://arxiv.org/abs/cs/0311014
