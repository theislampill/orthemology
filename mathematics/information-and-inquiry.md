# Information retained by inquiry

## Prediction, decisions, Fisher dynamics, and certified action

### Abstract

A representation can preserve every conditional answer to an inquiry while losing the probabilities, values, or geometric dynamics associated with those answers. We develop these distinctions in related finite models. Invariant observable spaces give exact predictive states, including their admissible cones and a sharp continuous-coordinate bound. A synchronized tensor construction, together with a separate feasibility test, characterizes the weaker equivalence of all posterior answers. For a fixed audit, missing information forms an affine fibre of audit weights. This gives an exact expected-value criterion and a three-outcome example that reverses the preferred inquiry decision. For the categorical Fisher metric of the full joint law, we derive a different criterion, prove descent of maximal source trajectories, and establish a sharp threshold: with more audit outcomes than target states, every globally descending smooth objective is target-marginal-only on the signature image. Gram-determinant objectives show why the strict inequality is necessary. Finally, we determine the supplementary information required by finite, expected-value, and full-metric contracts, distinguish selecting a valid certificate from identifying a state, and give complete finite proofs for model-bound temporal guarantees and versioned evidence transport.

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

These distinctions concern supplied mathematical models. They do not authenticate an actual source, establish its calibration, or equate a numerical loss with epistemic warrant.

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
q_w(x)=\frac{CM_wx}{uM_wx}\quad\text{if }uM_wx>0.               \tag{1}
```

At zero denominator the observation is impossible: no posterior is invented. Nonnegativity implies $`uM_wx=0\Rightarrow M_wx=0`$.

The target, model, and permitted alphabet are fixed. History-dependent permissions require an explicit controller or a separately proved restricted-language construction. If the target concerns an initial label that transitions can change, retain that label in the state.

### 2.2 The invariant observable construction

Define

```math
W_0=\mathrm{span}(\{u\}\cup\mathrm{rows}\,C),\qquad
W_{h+1}=W_h+\sum_aW_hM_a.                                    \tag{2}
```

**Theorem 1 — Exact predictive reduction.** The sequence stabilizes at the least invariant row space $`W`$ containing $`W_0`$. For a full-row-rank basis matrix $`B`$ of $`W`$, there are unique matrices and coefficients satisfying

```math
BM_a=T_aB,\qquad u=\nu B,\qquad C=LB.                         \tag{3}
```

For normalized $`x,y`$, equality $`Bx=By`$ is equivalent to equality of every future word probability and every feasible-word target posterior. The reduced state $`z=Bx`$ has admissible cone

```math
K=B\mathbb R_+^n=\mathrm{cone}\{Be_i\}
```

and, on the normalized slice $`\nu z=1`$, exact update

```math
z\longmapsto\frac{T_az}{\nu T_az}\quad\text{if }\nu T_az>0.    \tag{4}
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
\pi_1=(1/10,2/5,2/5,1/10).                                   \tag{5}
```

Both target and audit marginals are uniform. Nevertheless $`D=1`$ gives target-one posterior $`4/5`$ or $`1/5`$. The missing datum is a joint numerator, not an audit marginal.

Use the moments of $`1,\tau,\delta,\tau\delta`$, with $`\tau=(-1)^\Theta`$ and $`\delta=(-1)^D`$. Write them $`(m,t,d,h)`$. Multiplying by the projector $`(1+s\delta)/2`$, $`s=(-1)^b`$, yields

```math
m'=(m+sd)/2,\quad t'=(t+sh)/2,\quad d'=sm',\quad h'=st'.       \tag{6}
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
\Pr(\Theta=t,Y=y,D=d)=\frac{1+\rho(-1)^{t+y+d}}8.              \tag{24}
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
P_\epsilon(\theta,0)=p(\theta)-\epsilon q(\theta).             \tag{25}
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
v(x\otimes y)=0\quad\text{for every }v\in U.                  \tag{7}
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
F(w,P)=(p_1,\ldots,p_k,q).                                    \tag{8}
```

The empty word returns $`q`$; a nonempty constant audit word returns its $`p_j`$; a word with distinct audit labels is impossible. Thus (8), together with feasibility, gives all future posterior answers for this fixed-audit repertoire.

At fixed $`P,q`$, the hidden weights form

```math
W_{P,q}=\{w>0:Qw=q\}.                                        \tag{9}
```

Assume this set is nonempty and $`q`$ is normalized. Column stochasticity already implies $`\sum_jw_j=1`$. Every difference of representatives lies in $`\ker Q`$; conversely, for $`w^0\in W_{P,q}`$ and $`v\in\ker Q`$, the vectors $`w^0\pm\epsilon v`$ remain in the fibre for sufficiently small $`\epsilon>0`$.

For two feasible outcomes, distinct posterior columns determine the audit weight uniquely from $`q=(1-t)p_0+tp_1`$. Coincident columns both equal $`q`$, leaving the audit frequency undetermined. For a binary target, the signature therefore reconstructs the joint law off independence but collapses its audit-frequency fibre on independence. Boundary feasibility identifies the supported outcome at $`t=0`$ or $`1`$. The strictly positive off-independence family contains an open three-dimensional set on which the signature is injective; invariance of domain therefore still excludes a globally exact continuous encoder into fewer than three real coordinates. [2]

### 5.1 The expectation criterion

**Theorem 3 — Expected quantities on a positive fibre.** For $`h\in\mathbb R^k`$, the value $`h^\mathsf Tw`$ is constant on the whole fibre (9) if and only if $`h^\mathsf T\in\mathrm{row}\,Q`$.

**Proof.** If $`h^\mathsf T=b^\mathsf TQ`$, its value is $`b^\mathsf Tq`$. Conversely, constancy on $`w^0\pm\epsilon v`$ implies $`h^\mathsf Tv=0`$ for every $`v\in\ker Q`$. The equality $`(\ker Q)^\perp=\mathrm{row}\,Q`$ completes the proof. $`\square`$

For a Bayes-risk function $`H`$, finite at the relevant laws, set $`h_j=H(p_j)`$. Expected improvement is

```math
H(q)-\sum_jw_jH(p_j).                                        \tag{10}
```

A constant audit cost subtracts a constant. Outcome-dependent costs introduce their own expectation vector. On a restricted reachable family, use the span of actual admissible weight differences instead of the full $`\ker Q`$. On a boundary face, restrict to active support when the relative fibre has a positive point. These qualifications prevent a sufficient whole-fibre criterion from becoming a false necessity on smaller domains. [3]

### 5.2 A decision reversal with three outcomes

For a binary target, take conditional target-one probabilities

```math
(1/4,1/2,3/4),\qquad w=(a,1-2a,a),\quad 0<a<1/2.
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
+\sum_jw_j\sum_i\frac{\delta p_{ji}\eta p_{ji}}{p_{ji}}.       \tag{11}
```

The cross terms vanish. Since

```math
dE=\sum_j\langle h,p_j\rangle dw_j+
\sum_j\langle J_j+w_jh,dp_j\rangle,
```

and the inverse simplex Fisher operator is $`C(p)`$, negative gradient descent is

```math
\dot w_j=-w_j\langle h,p_j-q\rangle,\qquad
\dot p_j=-C(p_j)h-\frac{a_j}{w_j}.                            \tag{12}
```

The covariance decomposition

```math
\sum_jw_jC(p_j)+\sum_jw_j(p_j-q)(p_j-q)^\mathsf T=C(q)
```

then yields

```math
\dot q=-C(q)h-\sum_ja_j,\qquad
\dot\mu_{ji}=-\mu_{ji}(h_i-\langle q,h\rangle)-a_{ji}.          \tag{13}
```

The objective decreases:

```math
\dot E=
-\sum_jw_j\langle h,p_j-q\rangle^2
-\sum_j\frac{(J_j+w_jh)^\mathsf TC(p_j)(J_j+w_jh)}{w_j}
\leq0.                                                       \tag{14}
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
=\mathrm{rank}\,Q.                                      \tag{15}
```

Indeed a kernel vector with nonzero $`j`$-component expresses column $`j`$ as a linear combination of the others, and conversely. Small positive kernel perturbations establish the fibre equivalence.

**Theorem 4 — Pointwise Fisher descent.** The full projected velocity $`(\dot P,\dot q)`$ is independent of the representative $`w\in W_{P,q}`$ exactly when

```math
C(p_j)J_j=0\quad\text{for every variable index }j.            \tag{16}
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
V(T_\lambda z)=T_\lambda V(z).                               \tag{17}
```

The first equality follows because both its $`z`$-term and its $`a_j`$-term vanish. Thus the field is tangent to the affine slice. Restriction to that embedded submanifold and source uniqueness make the slice invariant for the entire maximal trajectory; it is relatively closed and has no additional boundary within the positive source domain.

The second equality intertwines trajectories. Moreover $`T_\lambda`$ maps $`K_\lambda`$ bijectively onto $`K_{\lambda^{-1}}`$. If one source trajectory extended beyond the other's maximal interval, this map or its inverse would transfer the extension, preserving positivity and normalization, contradicting maximality. Thus intervals and signatures agree. Conversely, equal projected trajectories near time zero have equal initial derivatives, and Theorem 4 yields (16). $`\square`$

This proves actual source-flow descent. It does not generally prove continuity of the projected velocity in the ordinary subspace topology of $`S`$, or that $`S`$ carries a reduced Riemannian metric. With the abstract quotient topology, the descended maximal flow is continuous: the source flow factors through the quotient on its open saturated domain, and product with the locally compact Hausdorff time line preserves quotient maps. The stronger ordinary-signature regularity below is proved separately. [4]

## 7. A sharp threshold for globally descending objectives

### 7.1 Rigidity when the audit has more outcomes than the target

**Lemma 6 — Dense fully variable signatures.** If $`k>r`$, matrices $`Q`$ for which every $`r`$-column minor is nonzero are dense in $`(\Delta_r^\circ)^k`$. At each such matrix all audit weights are variable.

**Proof.** Choose distinct $`t_j\in(0,1)`$ and $`0<\delta<1/[r(r-1)]`$. Let

```math
p_i(t)=1/r+\delta t^i\ (i<r),\qquad
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
\dot p_j=-C(p_j)h(q),\qquad \dot q=-C(q)h(q).                  \tag{18}
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
w'_j=\frac{w_jZ_{p_j}(\ell)}{Z_q(\ell)}.                      \tag{19}
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
-LG(x)^{-1}L^\mathsf T\nabla j(Lx).                           \tag{20}
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
\sum_{t\in D}K_a(s,o,t)=\sum_{t\in D}K_a(s',o,t).              \tag{21}
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
-\mathrm{rank}\,Q.                                      \tag{22}
```

**Corollary 9 — Exact continuous utility supplement.** On this fixed fibre, $`s`$ continuous real coordinates are necessary and sufficient to recover $`Hw`$, allowing arbitrary decoders. A finite-valued exact supplement exists if and only if $`s=0`$.

**Proof.** Choose a basis of the independent restrictions of the rows of $`H`$ to $`N`$. Retaining those linear values determines all other required values up to constants fixed by $`Qw=q`$, giving sufficiency. For necessity choose an $`s`$-dimensional subspace $`L\subseteq N`$ on which $`H`$ is injective. A sufficiently small open ball in $`w^0+L`$ lies in the positive fibre. An exact supplement must be injective on this ball, since equal encoded values imply equal $`Hw`$. Invariance of domain excludes a continuous injection into fewer than $`s`$ coordinates. If $`s>0`$, $`Hw`$ takes infinitely many values along a positive line segment, excluding a finite alphabet even without encoder continuity. If $`s=0`$, no supplement is needed. $`\square`$

Equation (22) follows because adjoining the rows of $`H`$ to $`Q`$ adds exactly their independent restrictions to $`\ker Q`$. This corollary combines the existing expectation-fibre and continuous-dimension arguments; its explicit combined formulation and proof are part of this exposition's independent review, not retroactively attributed to an earlier review. It concerns one fixed audit and a finite set of expected quantities. Future interventions require closure of the enlarged observable contract, not merely this one-step supplement.

### 9.3 The full-source metric requires all hidden weights

For a conditional coordinate $`p_{ji}`$, (11) gives its ambient Fisher squared gradient norm:

```math
\|\mathrm{grad}_g\,p_{ji}\|^2
=\frac{p_{ji}(1-p_{ji})}{w_j}.                               \tag{23}
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

   ```math
   R=\max_{o\in\omega(S)}\rho(\omega^{-1}(o)).
   ```

2. If the encoder knows only $`\eta(s)`$, for a supplied map $`\eta:S\to E`$, a message map $`c:\eta(S)\to M`$ is feasible exactly when every nonempty bucket

   ```math
   B(o,m)=\{s:\omega(s)=o,\ c(\eta(s))=m\}
   ```

   satisfies

   ```math
   \bigcap_{s\in B(o,m)}\mathcal A(s)\ne\varnothing.
   ```

   The minimum alphabet is the minimum number of used messages over such maps; no compatible map means impossibility.

**Proof.** A decoder returns one object for each observation/message pair. In a fixed cell, the objects returned by its used messages must cover every state, giving $`\rho(C)\leq|M|`$. Conversely, choose a minimum cover, assign each state to a covering object, and send its index. Because the decoder sees $`o`$, message names can be reused between cells, proving the maximum formula. With restricted encoder information, all states in a bucket necessarily receive the same decoded object, which must lie in their common intersection. Conversely, choose an object in each nonempty intersection and define the decoder accordingly. All choices are finite. $`\square`$

The exact-state cover number is not a solution when the sender cannot distinguish the relevant states. If $`\omega(s_0)=\omega(s_1)`$, $`\eta(s_0)=\eta(s_1)`$ and the two admissible sets are disjoint, no number of messages repairs that encoder-information deficit.

Several strict boundaries follow.

- With admissible sets $`\{a,b\},\{b,c\},\{a,c\}`$ in one cell, every pair has a common output but all three do not. Two objects cover the cell, while one message is impossible. Thus pairwise compatibility alone is insufficient for a general relation.
- An empty admissible set at even one possible state makes the fixed task impossible. Information cannot create a missing valid certificate.
- If $`\mathrm{act}:K\to U`$ retains only a surface action, then the action-cover number is at most $`\rho(C)`$: projecting any certificate cover gives an action cover. The inequality is strict for $`\mathcal A(s_0)=\{k_0\}`$ and $`\mathcal A(s_1)=\{k_1\}`$ with distinct certificates but $`\mathrm{act}(k_0)=\mathrm{act}(k_1)`$. Agreement on an action need not preserve its source, version or authority. If two same-byte version contexts require respectively an old-version execution certificate and a new-version hold/revalidation certificate, with no common admitted fallback, their cover number is two. One truthful distinguishing bit is then necessary and sufficient only when the encoder actually knows the relevant version.
- For a nonempty finite set of possible model completions $`\Theta(s)`$, robust admissibility is

  ```math
  \mathcal A_{\rm all}(s)=\bigcap_{\theta\in\Theta(s)}\mathcal A_\theta(s).
  ```

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


## 10. Assumptions, negative results, and open scope

The positive-fibre and Fisher theorems quantify over the full strictly positive joint-law family. On a constrained reachable family, use its actual differences; the density proof may fail. For example, with three audit outcomes, a binary target, fixed weights $`w_j=1/3`$, and $`J=p_{1,1}`$, equation (12) has $`\dot w=0`$. The section is invariant and its signature is injective, so the flow descends there despite conditional dependence at fixed $`q`$. This does not contradict the full-domain rigidity theorem.

Strict positivity supplies small kernel perturbations, division by weights, feasible audit outcomes, and nondegenerate conditional Fisher tangents. Boundary strata and null events need their own analysis. Ambient $`C^1`$ regularity supports the global classification; $`C^2`$ gives the stated unique $`C^1`$ source flow. Pointwise coincidence at one signature is not a trajectory theorem.

The preserved negative findings are substantive: separate marginals can lose audit-dependent answers; posterior equivalence can lose inquiry value; a conditional loss can have nonprojectable Fisher dynamics; a projectable complete flow can lack ordinary-signature velocity continuity; a target-only flow can reach the boundary in finite time; and finite labels cannot encode a positive-dimensional exact metric fibre.

Unresolved generalizations should be stated as such. This treatment does not classify every globally descending objective for $`k\leq r`$ beyond the exact criterion, provide global minimal charts across changing rank, solve arbitrary adaptive value preservation from posterior-only equivalence, or give stable approximate/noisy variants of every exact construction. Nor does it turn the declared probability law, loss, or metric into an empirical model of cognition or a philosophical judgment about actual warrant.

The certificate-selection and temporal results have a separate finite contract. The message encoder must possess the stated information and supply it truthfully with whatever authorization the application requires. Admissibility, model completeness, source/version eligibility, semantic preservation and actually discharged obligations are premises to be independently established. A one-shot zero-error cover bound is not an expected-rate, privacy, interactive, cryptographic, distributed-synthesis or bounded-error result. The complete temporal characterization assumes a finite common-state game; the rank certificate under incomplete observation is sufficient only. Neither theorem authenticates a source, supplies common knowledge or independent provenance, establishes causal restoration in a real system, or transfers authority to act. Dynamic membership or changed states, observations, targets and transitions require a new adequate model rather than an unproved reuse of the old ranks.

## 11. Attribution, evidence, and edition boundary

The predictive observable theorem and its continuous-coordinate proof are inherited from *Continuation-Complete Orthings*, with the established predictive-state ancestry in [8]. Support-sensitive fibre factorization is also developed in the information-and-revision lineage [7]. The audit transport, paired posterior test, fixed-audit classification, and inquiry-value separation are consolidated from [2]–[3]; their exact final source versions have separately bound ordinary reviews. The Fisher classification and its row-rescaling maximal-flow proof come from [4]. That source credits the row-rescaling proof to its finite-audit mathematical contributor; it is not counted as independent corroboration merely because the contributor also served in a review role. The finite and continuous supplement arguments reconcile [5–6].

The explicit discontinuous-signature sequence in §7.4 and the combined utility-coordinate corollary in §9.2 are deductions written out for this exposition. They make no field-wide priority claim and require review as part of this edition. The sources' historical finite controls corroborate their own bounded statements; they do not constitute new execution of this text, universal proof by enumeration, or Lean certification.

The historical sidecar review is conditional on the ambient norm identity and requested normalization of $`q`$; both the identity and normalization are proved or explicit here. A review of audit covariance is not treated as a review of the full Fisher classification. Frozen source text that once said “review pending” is distinguished from its later exact-version review. No unavailable historical output is manufactured.

Section 9.4 incorporates the complete-certificate relation-selection results [13], the repaired distinction between invariant-core entry and co-Büchi persistence [14], model-bound temporal-certificate guards [15], and versioned evidence composition and eligibility reopening [16]. The encoder-information, robust-completion and adversarial-channel boundaries preserve their substantive corrections. The observation-cell qualifier on label distance, explicit optimal five-bit code, inner-removal-rank completeness proof against history-dependent controllers, and fresh-hidden-branch construction are written out in this edition and require its own independent review. They are expository clarifications or deductions, with no new-priority claim. Witsenhausen's exact reconstruction, Orlitsky–Roche's asymptotic function computation, Karp's covering complexity, and Emerson–Jutla's parity-game fixed points supply classical antecedents under their respective premises [17–20]; the present finite statements are proved here.

The four finite certificate/temporal sources have bounded later reviews and preserved earlier failure records. Those historical assessments do not qualify this new exposition by inheritance. Their public adoption boundary continues to distinguish scoped ordinary mathematical results from external review and owner adoption, which remain pending. The original standalone evidence-transport ancestor packets were not newly received; the source's indexed reconciliation is not represented as direct custody of those missing bodies. No private paper or accepted edition is replaced by these finite proposals.

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
