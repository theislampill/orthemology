# Information retained by inquiry

## Prediction, decisions, Fisher dynamics, and certified action

### Abstract

A representation can preserve every conditional answer to an inquiry while losing the probabilities, values, or geometric dynamics associated with those answers. We develop these distinctions in related finite models. Invariant observable spaces give exact predictive states, including their admissible cones and a sharp continuous-coordinate bound. A synchronized tensor construction, together with a separate feasibility test, characterizes the weaker equivalence of all posterior answers. For a fixed audit, missing information forms an affine fibre of audit weights. This gives an exact expected-value criterion and a three-outcome example that reverses the preferred inquiry decision. For the categorical Fisher metric of the full joint law, we derive a different criterion, prove descent of maximal source trajectories, and establish a sharp threshold: with more audit outcomes than target states, every globally descending smooth objective is target-marginal-only on the signature image. Gram-determinant objectives show why the strict inequality is necessary. Finally, we determine the supplementary information required by finite, expected-value, and full-metric contracts, distinguish selecting a valid certificate from identifying a state, and give complete finite proofs for model-bound temporal guarantees and versioned evidence transport. Graph-constrained parity operations make the action dependence explicit: the exact connecting-tree cost determines which moments a finite horizon can reveal. For proof-producing inquiry, residual evidence supports and terminal checking prices give a canonical continuation summary and an exact finite completion criterion. Finite grounded rules compile that summary even in the presence of cycles, while shared proof graphs expose a limit of intermediate cost-only pruning. When the governing quadratic standard is unknown, shrinking disturbances impose a decoding requirement on every good repair. This yields finite-sample lower and upper bounds, and a countability obstruction to eventual exact correction when informative acts are target-bad. Common-reference and actual causal-oracle proofs identify the information premise precisely; sublinear tolerance and atomic blind guessing delimit the result.

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

Copies do not increase the sample count. If *k* records are functions of *N* original fresh outcomes and independent randomness, they remain a postprocessing of the same experiment, so (28) counts *N*, not *k*. A provenance label alone establishes neither authenticity nor independence. Additional conditionally informative observations must be evaluated using their actual conditional law.

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

The exact formal source [30] proves the visited-support inequality, synthesis from a finite connected witness, the optimum under a minimum-witness premise, and the local character pullback identity. Its constructive connected-set predicate is not separately identified inside Lean with an imported graph-connectivity predicate, and its unlabelled idle constructor is harmless for an at-most horizon only. Whole physical-word correspondence, the probability-simplex/topological lower bound, fixed-root strengthening, graph counts and saturation remain written proofs. The finite support/price formalization [31] proves normalization, the inverse, necessity and persistent updating in an arbitrary linearly ordered price type with a newly adjoined infeasibility top. Its catalogue, supports and acquisitions are finite; the ambient token type need not be. It supplies original pairs, not admitted derivation objects, authentication or actual terminal execution.

The predecessor reports and reviews record Lean 4.19 certification of these exact formal bodies with the standard dependencies `propext`, `Classical.choice` and `Quot.sound`, and preserve false-strengthening controls. Their historical execution claims remain bound to those sources and their recorded environments. Source inspection here is not a fresh kernel replay, an audit of cached transitive dependencies, or receipt of every historical raw log. The Bellman criterion, semantic cover, finite rule compilation, and tree/shared-graph distinction have ordinary proofs and bounded historical finite checks; they are not added to the kernel certificate by association. The earlier distinction between a finite proof and unrestricted logical or epistemic completeness remains in force. Referenced ancestor manuscripts outside the actual received population receive no new whole-document reading or replacement credit.

Section 9.7 reconciles the complete public continuum-restoration exposition [32] and finite-information bridge [33]. The repair geometry, local-minimax experiment, copied-record boundary, target-preserving positive construction, finite-query obstruction, countable sharpness and philosophical limitations retain their separate premises. The explicit affinity proof, Bernoulli moment-generating-function argument, common-reference lemma and seed/finite-word factorization are written out here. Countability of atoms, contraction under measurable postprocessing, concentration and summable-event reasoning are established mathematical mechanisms; no field-wide novelty is claimed. The concentration antecedent is Hoeffding [34]. The original programme's latent identification, persistent restoration, metric and source-binding connections are expressed here by subject, without using its historical organizational labels as scientific structure.

The two prose sources are public navigation-only projections. This edition incorporates those exact public bodies, not their private originals or custody diffs. The broader support README includes other composition and restoration results and is not replaced in full by this section. Historical “pending” sentences and later recorded formal successes have different scopes: later reports of compilation or copied-source review for particular causal modules do not retroactively certify every ordinary assertion in the initial prose.

The selected formal sources [35–41] distinguish a generic dominated-readout theorem from a concrete evaluator that discharges the domination obligation. The locality proof bounds only one run. The actual finite-query measure construction uses finite words with positive reference mass; it does not dominate every infinite oracle law. The correlated-law construction permits seed/oracle dependence. Its earlier exact-restoration endpoints [38–39] specialize to a common probability seed marginal and probability input laws. Theorem 24 gives the dominated-marginal extension as an ordinary proof here; [40]'s approximate causal endpoint itself allows merely dominated seed marginals and does not require normalized input laws for its measure-theoretic countability conclusion. Probability interpretations impose normalization separately. The formal approximate score inequalities allow real outputs without an extra coherence premise, so the impossibility covers coherent outputs as a subset; the positive constructions here impose their stated range conditions. Source [41] proves the exact atom-mass identity for the literal zero-query evaluator, while the existence and effective-sampling qualifications for an arbitrary countable guessing law remain ordinary mathematics.

These seven public formal bodies were inspected at source level. Their transitive dependency closure, including the imported restoration-countability bridge and Mathlib modules, was not newly read or built for this edition. The predecessor records compilation, axiom-readback and independent copied-source review at their original bounded scopes; source inspection, printed proof-check commands and this exposition's ordinary proofs are not fresh kernel execution or receipt of every historical raw log. In particular the statistical sample bounds, philosophical interpretation and the whole two-source incorporation are not added to a kernel certificate by association. The existing source/adoption and accepted-edition boundaries remain.

**Edition status:** new source-bound consolidated exposition. The companion review record binds the exact text, source population, independent findings, corrections, and proposed predecessor retirement. Review of this exposition does not confer owner acceptance or silently amend an accepted paper. None of those records is needed to follow the mathematical arguments above.

### References

1. Orthemology. *Continuation-Complete Orthings: Sharp information loss, minimal predictive memory, and safe strategic composition*, “Continuation completion, including observations and feedback,” Theorem 2 and proof. [Exact source][1].
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
