# Information retained by inquiry

## Prediction, decisions, and Fisher dynamics

### Abstract

A representation can preserve every conditional answer to an inquiry while losing the probabilities, values, or geometric dynamics associated with those answers. We develop these distinctions in one finite model. Invariant observable spaces give exact predictive states, including their admissible cones and a sharp continuous-coordinate bound. A synchronized tensor construction, together with a separate feasibility test, characterizes the weaker equivalence of all posterior answers. For a fixed audit, missing information forms an affine fibre of audit weights. This gives an exact expected-value criterion and a three-outcome example that reverses the preferred inquiry decision. For the categorical Fisher metric of the full joint law, we derive a different criterion, prove descent of maximal source trajectories, and establish a sharp threshold: with more audit outcomes than target states, every globally descending smooth objective is target-marginal-only on the signature image. Gram-determinant objectives show why the strict inequality is necessary. Finally, we determine the supplementary information required by finite, expected-value, and full-metric contracts.

This is a consolidated exposition of the source mathematics cited below. Its proofs are ordinary mathematical arguments; computational corroboration, kernel certification, empirical interpretation, literature priority, and owner adoption are distinct. The edition and review boundary appears at the end.

## 1. What must a representation preserve?

“Preserving information” is incomplete until the required operations and outputs have been specified.

| Contract | Required output |
|---|---|
| Posterior answers | Feasible observation words and the target posterior after each feasible word |
| Full prediction | Those answers and the probabilities of the observation words |
| Decision value | Expected losses, rewards, or costs in the declared decision problem |
| Geometric dynamics | Evolution under the specified source metric, objective, clock, and domain |

Full prediction preserves the values of bounded-depth adaptive policy trees when their terminal observables and costs are included. Posterior answers alone need not. Even an objective determined by retained answers can have a source gradient that depends on discarded information. Conversely, an individual objective may descend although an entire metric does not.

These distinctions concern supplied mathematical models. They do not authenticate an actual source, establish its calibration, or equate a numerical loss with epistemic warrant.

## 2. Finite instruments and exact predictive states

### 2.1 The model

Let the latent space have $n$ elements, and fix a finite, explicitly supplied action–observation alphabet $\Sigma$. A live unnormalized state is a column vector $x\geq0$ with $ux>0$, where $u=(1,\ldots,1)$. Each symbol $a\in\Sigma$ has a nonnegative column-substochastic matrix $M_a$. The outcome matrices belonging to one action sum to a column-stochastic matrix. Let $C$ be a fixed column-stochastic target readout. The constructions below test every finite word in $\Sigma^*$, including the empty word.

For a chronological word $w=a_1\cdots a_t$, set
$$
M_w=M_{a_t}\cdots M_{a_1},\qquad M_\varepsilon=I.
$$
Its conditional probability and posterior target law are
$$
\Pr_x(w)=\frac{uM_wx}{ux},\qquad
q_w(x)=\frac{CM_wx}{uM_wx}\quad\text{if }uM_wx>0.               \tag{1}
$$
At zero denominator the observation is impossible: no posterior is invented. Nonnegativity implies $uM_wx=0\Rightarrow M_wx=0$.

The target, model, and permitted alphabet are fixed. History-dependent permissions require an explicit controller or a separately proved restricted-language construction. If the target concerns an initial label that transitions can change, retain that label in the state.

### 2.2 The invariant observable construction

Define
$$
W_0=\operatorname{span}(\{u\}\cup\operatorname{rows}C),\qquad
W_{h+1}=W_h+\sum_aW_hM_a.                                    \tag{2}
$$

**Theorem 1 — Exact predictive reduction.** The sequence stabilizes at the least invariant row space $W$ containing $W_0$. For a full-row-rank basis matrix $B$ of $W$, there are unique matrices and coefficients satisfying
$$
BM_a=T_aB,\qquad u=\nu B,\qquad C=LB.                         \tag{3}
$$
For normalized $x,y$, equality $Bx=By$ is equivalent to equality of every future word probability and every feasible-word target posterior. The reduced state $z=Bx$ has admissible cone
$$
K=B\mathbb R_+^n=\operatorname{cone}\{Be_i\}
$$
and, on the normalized slice $\nu z=1$, exact update
$$
z\longmapsto\frac{T_az}{\nu T_az}\quad\text{if }\nu T_az>0.    \tag{4}
$$

**Proof.** Induction shows that $W_h$ is the span of $uM_w$ and $cM_w$ for words of length at most $h$ and rows $c$ of $C$. Every strict inclusion increases dimension, giving at most $n-\dim W_0$ strict increases. Equality at one stage gives invariance, so later growth is impossible. Every invariant space containing $W_0$ contains the entire sequence. Invariance and full row rank give (3).

The commuting equations recover probabilities and numerators from $Bx$, and therefore the positive-branch posteriors. Conversely, equal probabilities and posteriors give equal target numerators on feasible words; both numerators vanish on impossible words. Thus $x-y$ annihilates every generator of $W$.

If $z=Bx$ with $x\geq0$, then $T_az=BM_ax\in K$. Also $\nu z=ux\geq0$, with zero mass forcing $x=0$ and $z=0$. Hence impossible successors are zero and cannot be normalized. The same fact proves pointedness: $z,-z\in K$ forces $\nu z=0$, hence $z=0$. Equation (4) follows. $\square$

The matrices $T_a$ can have signed entries in a chosen basis. Positivity means preserving $K$, not a freely substituted coordinate orthant. For live unnormalized laws the predictive equivalence concerns $Bx/(ux)$; absolute evidence mass is an additional requirement.

Adding finite terminal utilities, costs, or safety observables to $W_0$ preserves their corresponding values for bounded-depth adaptive policy trees. Each policy-tree leaf contributes a numerator $fM_wx$; summing leaves gives the expectation, and randomized policies add finite convex combinations. Target observations alone do not thereby preserve every reward. [1], [2]

### 2.3 Continuous memory

Put $m=\dim W$. On the full normalized simplex, exactly $m-1$ continuous real coordinates are necessary and sufficient for this predictive contract, even with arbitrary decoders.

A basis $u,f_1,\ldots,f_{m-1}$ gives sufficiency. For necessity select $m$ latent states with linearly independent basis-evaluation columns. Their nonconstant evaluation vectors are affinely independent, so all required expectations distinguish every law on the $(m-1)$-simplex supported on these states. Any exact encoder is injective there. On its relative interior, a continuous injection into $\mathbb R^d$ for $d<m-1$, followed by zero-padding, contradicts invariance of domain: the image would be open in $\mathbb R^{m-1}$ while lying in a lower-dimensional plane. The zero-dimensional case is immediate. [1], [10]

This counts exact continuous coordinates, not bits, physical degrees of freedom, or finitely many reachable histories. It does not constrain discontinuous encodings of unlimited exact precision.

## 3. The information hidden between target and audit marginals

Let target $\Theta$, source type $T$, report $Y$, and verifier $V$ be binary. The target and type are independent and uniform. The report is $9/10$-accurate for a good source and $1/2$-accurate for a bad source. The verifier is $4/5$-accurate and conditionally independent of the report given $(\Theta,T)$. Define
$$
D=\mathbf1[V\ne Y],\qquad A=(T,D).
$$
Reading this already existing audit is a diagonal projector. After reading the report, the eight joint masses of $(\Theta,T,D)$ suffice for future readings of $A$. If $G$ groups the sixteen latent masses and $P_a$ selects audit value $a$, then $GM_a=P_aG$, and the target readout factors through $G$. Target indicators multiplied by audit selectors give all eight joint indicators, proving closure rank eight. Adding future report readings on the unrestricted latent-law simplex raises the rank to sixteen: $(\Theta,T,Y,D)$ determines $V$.

The stated prior gives
$$
\Pr(\Theta=1\mid Y=1)=\frac7{10},\quad
\Pr(A=(\mathrm{Bad},1)\mid Y=1)=\frac14,\quad
\Pr(\Theta=1\mid Y=1,A=(\mathrm{Bad},1))=\frac15.
$$

On the known-bad slice, in the order $(\Theta,D)=(0,0),(0,1),(1,0),(1,1)$, the two report histories give
$$
\pi_0=(2/5,1/10,1/10,2/5),\qquad
\pi_1=(1/10,2/5,2/5,1/10).                                   \tag{5}
$$
Both target and audit marginals are uniform. Nevertheless $D=1$ gives target-one posterior $4/5$ or $1/5$. The missing datum is a joint numerator, not an audit marginal.

Use the moments of $1,\tau,\delta,\tau\delta$, with $\tau=(-1)^\Theta$ and $\delta=(-1)^D$. Write them $(m,t,d,h)$. Multiplying by the projector $(1+s\delta)/2$, $s=(-1)^b$, yields
$$
m'=(m+sd)/2,\quad t'=(t+sh)/2,\quad d'=sm',\quad h'=st'.       \tag{6}
$$
When $m'>0$, the target-one posterior is $(1-t'/m')/2$. The vector $(1,0,0,2)$, despite plausible separate marginals, reconstructs signed masses $(3/4,-1/4,-1/4,3/4)$ and can yield a negative posterior. It is excluded by the admissible cone.

Rereading the same result is not a fresh observation. Matching projectors are idempotent; after posterior $1/5$, the matching reread has probability one and leaves that posterior unchanged. A contradictory reread is impossible. Two fresh conditionally independent disagreements instead give
$$
\frac{(1-\alpha)^2}{(1-\alpha)^2+\alpha^2}=\frac1{17}
\quad\text{when }\alpha=4/5.
$$
The instruments differ. Also, rank four for arbitrary laws on $(\Theta,D)$ does not demand three real coordinates for the two particular histories in (5); those two histories need only one distinguishing bit. [2]


### 3.1 The higher-order interaction and its loss

The known-bad model has a general form. Let $\Theta,Y$ be independent fair bits, and let the verifier satisfy $\Pr(V=\Theta\mid\Theta,Y)=\alpha\in(0,1)$. Thus its error is conditionally independent of the report given the target. Put $D=Y\mathbin{\mathsf{xor}}V$ and $\rho=2\alpha-1$. Then
$$
\Pr(\Theta=t,Y=y,D=d)=\frac{1+\rho(-1)^{t+y+d}}8.              \tag{24}
$$
Summing any index eliminates the signed term, so every one-variable and two-variable marginal is uniform. Yet
$$
\mathbb E[(-1)^\Theta(-1)^Y(-1)^D]=\rho.
$$
The probability array is a three-slot tensor. Marginalization contracts a slot against the all-ones covector and kills this signed component; contracting all three slots against sign covectors recovers it. This is a tensor-slot statement, not a tensor-decomposition-rank claim.

Conditioning (24) gives
$$
\Pr(\Theta=1\mid Y=y,D=d)=\frac{1-\rho(-1)^{y+d}}2.
$$
Erasing $Y$ while retaining $D$ returns $1/2$. Under half-Brier loss the excess risk is the square of the binary posterior error, $\rho^2/4$, at every outcome and hence in expectation. At accuracy $4/5$, it is $9/100$. This is a concrete use of the classical parity-interaction mechanism. It does not make every neutral historical datum necessary: relevance arises from the specifically admitted future audit. A reduction correct for a smaller family of immutable-factor operations need not remain correct after this joint observation is added. [11]

### 3.2 Conditioning cannot choose a model revision at a null audit

Let the target have at least two states and let $p(\theta)>0$ be normalized. Take a baseline law
$$
P_0(\theta,A=0)=p(\theta),\qquad P_0(\theta,A=1)=0.
$$
For any positive target law $q$ and
$0<\epsilon<\min_\theta p(\theta)/q(\theta)$, define
$$
P_\epsilon(\theta,1)=\epsilon q(\theta),\qquad
P_\epsilon(\theta,0)=p(\theta)-\epsilon q(\theta).             \tag{25}
$$
Every cell is positive, the target marginal remains exactly $p$, and
$$
P_\epsilon(\theta\mid A=1)=q,\qquad
\|P_\epsilon-P_0\|_{\mathrm{TV}}=\epsilon.
$$
The variation identity follows because the absolute changes in the two audit columns sum to $2\epsilon$.

Choose two distinct positive $q$'s. Both positive-model families approach the same baseline with the same target marginal, but their audit-conditioned posteriors have different limits. Therefore the impossible event has no unique continuous conditional extension selected by the baseline alone. A smoothing rule supplies additional modelling information.

A fixed positive model has a unique posterior. The result does not prohibit rational revision of a zero-probability assessment; it separates such revision from conditioning inside the original model. Applied after a retained history, the argument uses its full positive support and says nothing about hypotheses excluded by that support. Changing the target, source claim, or audit authentication requires its own warranted modelling justification. [12]

## 4. Posterior equivalence and its finite tensor test

Two live states are posterior-equivalent if they admit the same words and give the same target posterior after every feasible word, including the empty word. They need not predict word probabilities.

For example, keep a uniform target independent of a source bit $S$, and observe source-only likelihoods $f(0)=1/4,f(1)=3/4$ and $1-f$. Beliefs with $\Pr(S=0)=3/4$ and $1/4$ give the same uniform target posterior after every word; all words are possible. Their next first-outcome probabilities are $3/8$ and $5/8$.

For each target row $c$, define
$$
d_c=c\otimes u-u\otimes c,\qquad N_a=M_a\otimes M_a.
$$
Let $U$ be the least row space containing the $d_c$ and invariant under right multiplication by the $N_a$.

**Theorem 2 — Posterior comparison.** Live nonnegative $x,y$ are posterior-equivalent exactly when their feasible-word languages agree and
$$
v(x\otimes y)=0\quad\text{for every }v\in U.                  \tag{7}
$$

**Proof.** On a common feasible word, posterior equality is equivalent to
$$
(cM_wx)(uM_wy)-(uM_wx)(cM_wy)=0.
$$
The left side is $d_c(M_w\otimes M_w)(x\otimes y)$. The mixed-product identity gives $N_w=M_w\otimes M_w$; both factors use the same word. These rows span $U$. Both successors vanish on a jointly impossible word. Conversely, common feasibility permits division precisely on the positive branches. $\square$

All generators are antisymmetric under factor exchange, and each $N_a$ preserves that subspace. Consequently $\dim U\leq n(n-1)/2$. The tensor dimension is the size of a comparison construction, not a one-belief memory minimum. Under the column convention, right multiplication of a row by $N_a$ prepends $a$ to its chronological word. A witness-producing implementation must retain that convention.

The feasibility guard is essential. If only one successor is zero, every cross-product at that word still vanishes. Two states with the same target and different perfectly observed source bits illustrate this failure.

Nonnegative supports update by
$$
F_a(S)=\{i:\ M_a[i,j]>0\text{ for some }j\in S\}.
$$
Explore support pairs under synchronized $(F_a,F_a)$. Exactly one empty component witnesses a language difference; otherwise complete exploration establishes equality. There are at most $4^n$ pairs. With the finite supplied alphabet and rational, explicitly supplied $M_a,C,x,y$, this test and invariant-space closure are exact terminating algorithms. Arbitrary uncomputable real coefficients or an unspecified infinite alphabet do not provide that guarantee.

A common feasible first observation preserves all continuation comparisons, giving a set-theoretic partial quotient. This does not supply a convenient linear or finite-dimensional posterior-state parameterization. The product and invariant-span methods have established predictive-state and weighted-automata antecedents. [2], [8], [9]

## 5. Fixed audits and the value of inquiry

Let a single already existing audit have $k$ labelled outcomes and the target have $r$ states. Let $p_j$ be the conditional target law, $w_j>0$ its audit weight, and
$$
Q=[p_1\ \cdots\ p_k],\qquad q=Qw.
$$
The posterior-only signature is
$$
F(w,P)=(p_1,\ldots,p_k,q).                                    \tag{8}
$$
The empty word returns $q$; a nonempty constant audit word returns its $p_j$; a word with distinct audit labels is impossible. Thus (8), together with feasibility, gives all future posterior answers for this fixed-audit repertoire.

At fixed $P,q$, the hidden weights form
$$
W_{P,q}=\{w>0:Qw=q\}.                                        \tag{9}
$$
Assume this set is nonempty and $q$ is normalized. Column stochasticity already implies $\sum_jw_j=1$. Every difference of representatives lies in $\ker Q$; conversely, for $w^0\in W_{P,q}$ and $v\in\ker Q$, the vectors $w^0\pm\epsilon v$ remain in the fibre for sufficiently small $\epsilon>0$.

For two feasible outcomes, distinct posterior columns determine the audit weight uniquely from $q=(1-t)p_0+tp_1$. Coincident columns both equal $q$, leaving the audit frequency undetermined. For a binary target, the signature therefore reconstructs the joint law off independence but collapses its audit-frequency fibre on independence. Boundary feasibility identifies the supported outcome at $t=0$ or $1$. The strictly positive off-independence family contains an open three-dimensional set on which the signature is injective; invariance of domain therefore still excludes a globally exact continuous encoder into fewer than three real coordinates. [2]

### 5.1 The expectation criterion

**Theorem 3 — Expected quantities on a positive fibre.** For $h\in\mathbb R^k$, the value $h^\mathsf Tw$ is constant on the whole fibre (9) if and only if $h^\mathsf T\in\operatorname{row}Q$.

**Proof.** If $h^\mathsf T=b^\mathsf TQ$, its value is $b^\mathsf Tq$. Conversely, constancy on $w^0\pm\epsilon v$ implies $h^\mathsf Tv=0$ for every $v\in\ker Q$. The equality $(\ker Q)^\perp=\operatorname{row}Q$ completes the proof. $\square$

For a Bayes-risk function $H$, finite at the relevant laws, set $h_j=H(p_j)$. Expected improvement is
$$
H(q)-\sum_jw_jH(p_j).                                        \tag{10}
$$
A constant audit cost subtracts a constant. Outcome-dependent costs introduce their own expectation vector. On a restricted reachable family, use the span of actual admissible weight differences instead of the full $\ker Q$. On a boundary face, restrict to active support when the relative fibre has a positive point. These qualifications prevent a sufficient whole-fibre criterion from becoming a false necessity on smaller domains. [3]

### 5.2 A decision reversal with three outcomes

For a binary target, take conditional target-one probabilities
$$
(1/4,1/2,3/4),\qquad w=(a,1-2a,a),\quad 0<a<1/2.
$$
Every joint cell is positive and $q=1/2$ for every $a$. Posterior answers and feasibility agree for all words.

For half-Brier loss, $H(p)=p(1-p)$. Expected improvement is
$$
\frac14-\left(\frac{3a}{16}+\frac{1-2a}{4}+\frac{3a}{16}\right)
=\frac a8.
$$
At $a=1/4$ and $1/8$, the gains are $1/32$ and $1/64$. A common cost $3/128$ gives net values $+1/128$ and $-1/128$, reversing the preferred audit-versus-skip action.

The boundary example with posteriors $(0,1/2,1)$ has gain $a/2$; a cost $3/32$ gives net values $\pm1/32$ for the same weights. The interior example proves that the obstruction is not a zero-cell artifact.

For distinct interior target laws $p_0,p_1$, midpoint $p_*=(p_0+p_1)/2$, and finite strictly concave Bayes risk on these laws, the analogous gain is
$$
a\bigl(2H(p_*)-H(p_0)-H(p_1)\bigr)>0.
$$
Thus the phenomenon is not restricted to binary targets or quadratic loss.

Three outcomes are minimal for this particular value-loss obstruction. With two distinct posterior columns the weights are determined; with coincident columns the expected value of every finite function of the posterior is fixed and risk improvement is zero. A single feasible outcome also gives zero improvement. This is a theorem for one fixed audit, finite posterior risk, and constant cost, not for arbitrary fresh experiments, outcome-dependent costs, or adaptive policies. The posterior matrix $Q=\Pr(\Theta\mid D)$ and the target law are fixed here; the forward channel $\Pr(D\mid\Theta)$ generally varies with $w$. [3]

## 6. The categorical Fisher dynamics of the full source

Assume $r,k\geq2$ and every joint cell is positive. Write
$$
X=\Delta_k^\circ\times(\Delta_r^\circ)^k,\qquad
\mu_{ji}=w_jp_{ji},\qquad S=F(X)\subseteq A=(\Delta_r^\circ)^{k+1}.
$$
Let $J(P,q)$ be an ambient $C^2$ objective and $E=J\circ F$. The metric is the categorical Fisher metric of the joint law $\mu$. It is not a separately stipulated metric on retained coordinates.

Let $J_j$ denote the derivative in slot $p_j$, let $h=J_q$, and define
$$
C(p)=\operatorname{diag}(p)-pp^\mathsf T,\qquad a_j=C(p_j)J_j.
$$
Derivatives are intrinsic to simplex affine spaces; Euclidean representatives may differ by constants times the all-ones vector.

### 6.1 Derivation

Expanding $d\mu_{ji}=p_{ji}\,dw_j+w_j\,dp_{ji}$, with $\sum_i dp_{ji}=0$, gives
$$
g((\delta w,\delta P),(\eta w,\eta P))
=\sum_j\frac{\delta w_j\eta w_j}{w_j}
+\sum_jw_j\sum_i\frac{\delta p_{ji}\eta p_{ji}}{p_{ji}}.       \tag{11}
$$
The cross terms vanish. Since
$$
dE=\sum_j\langle h,p_j\rangle dw_j+
\sum_j\langle J_j+w_jh,dp_j\rangle,
$$
and the inverse simplex Fisher operator is $C(p)$, negative gradient descent is
$$
\dot w_j=-w_j\langle h,p_j-q\rangle,\qquad
\dot p_j=-C(p_j)h-\frac{a_j}{w_j}.                            \tag{12}
$$
The covariance decomposition
$$
\sum_jw_jC(p_j)+\sum_jw_j(p_j-q)(p_j-q)^\mathsf T=C(q)
$$
then yields
$$
\dot q=-C(q)h-\sum_ja_j,\qquad
\dot\mu_{ji}=-\mu_{ji}(h_i-\langle q,h\rangle)-a_{ji}.          \tag{13}
$$
The objective decreases:
$$
\dot E=
-\sum_jw_j\langle h,p_j-q\rangle^2
-\sum_j\frac{(J_j+w_jh)^\mathsf TC(p_j)(J_j+w_jh)}{w_j}
\leq0.                                                       \tag{14}
$$

For positive $p$,
$$
z^\mathsf TC(p)z=\sum_ip_i(z_i-\langle p,z\rangle)^2,
$$
so $\ker C(p)=\operatorname{span}\{1\}$. Every formula is gauge-invariant, and $a_j=0$ means that the intrinsic differential in slot $p_j$ vanishes.

Two ambient objectives agreeing on $S$ have identical source pullbacks and intrinsic source gradients. Arbitrary off-image values are irrelevant. Decreasing the stipulated loss does not establish that an actual belief change is warranted. [4]

### 6.2 The exact pointwise criterion

An index $j$ is **variable** at $(P,q)$ if some two weights in (9) differ in component $j$. Equivalently,
$$
\exists v\in\ker Q:\ v_j\ne0
\quad\Longleftrightarrow\quad
\operatorname{rank}(Q\text{ with column }j\text{ deleted})
=\operatorname{rank}Q.                                      \tag{15}
$$
Indeed a kernel vector with nonzero $j$-component expresses column $j$ as a linear combination of the others, and conversely. Small positive kernel perturbations establish the fibre equivalence.

**Theorem 4 — Pointwise Fisher descent.** The full projected velocity $(\dot P,\dot q)$ is independent of the representative $w\in W_{P,q}$ exactly when
$$
C(p_j)J_j=0\quad\text{for every variable index }j.            \tag{16}
$$

**Proof.** Equation (13) for $\dot q$ has no weight dependence. In each separately retained conditional slot in (12), the only such dependence is $a_j/w_j$. If $w_j$ varies, equality forces $a_j=0$; if it is fixed, its denominator is already determined. No cancellation between different conditional slots is possible. $\square$

A nontrivial fibre need not make every index variable. For
$$
p_1=p_2=(1/2,1/4,1/4),\qquad p_3=(1/4,1/4,1/2),
$$
the kernel is spanned by $(1,-1,0)$. The objective $J=p_{3,1}$ satisfies (16) at that signature even though its third conditional differential is nonzero. The stronger global classification below requires an additional density argument.

### 6.3 From velocities to maximal source trajectories

Projectability at a point is not, by itself, a theorem about complete trajectories on a singular quotient. Here the special source equations supply the missing argument.

**Theorem 5 — Exact maximal-flow descent.** For ambient $C^2$ $J$, condition (16) at every admissible signature is equivalent to descent of the actual maximal source flow: equivalent initial source laws have identical signature trajectories and the same maximal interior time interval.

**Proof.** The source field in (13) is $C^1$, so ordinary differential-equation uniqueness applies. Given equivalent positive joint laws $\mu,\nu$, there are constants $\lambda_j>0$ with
$$
\nu=T_\lambda\mu,\qquad (T_\lambda z)_{ji}=\lambda_jz_{ji}.
$$
Consider the affine slice
$$
K_\lambda=\left\{z>0:\sum_{j,i}z_{ji}=1,\
\sum_j(\lambda_j-1)z_{ji}=0\text{ for each }i\right\}.
$$
For every $z$ on this slice, $T_\lambda z$ is a positive normalized law with the same signature. If $\lambda_j\ne1$, the corresponding weight differs, so (16) gives $a_j(F(z))=0$.

Writing $V$ for the source field, (13) now gives
$$
\sum_j(\lambda_j-1)V_{ji}(z)=0,\qquad
V(T_\lambda z)=T_\lambda V(z).                               \tag{17}
$$
The first equality follows because both its $z$-term and its $a_j$-term vanish. Thus the field is tangent to the affine slice. Restriction to that embedded submanifold and source uniqueness make the slice invariant for the entire maximal trajectory; it is relatively closed and has no additional boundary within the positive source domain.

The second equality intertwines trajectories. Moreover $T_\lambda$ maps $K_\lambda$ bijectively onto $K_{\lambda^{-1}}$. If one source trajectory extended beyond the other's maximal interval, this map or its inverse would transfer the extension, preserving positivity and normalization, contradicting maximality. Thus intervals and signatures agree. Conversely, equal projected trajectories near time zero have equal initial derivatives, and Theorem 4 yields (16). $\square$

This proves actual source-flow descent. It does not generally prove continuity of the projected velocity in the ordinary subspace topology of $S$, or that $S$ carries a reduced Riemannian metric. With the abstract quotient topology, the descended maximal flow is continuous: the source flow factors through the quotient on its open saturated domain, and product with the locally compact Hausdorff time line preserves quotient maps. The stronger ordinary-signature regularity below is proved separately. [4]

## 7. A sharp threshold for globally descending objectives

### 7.1 Rigidity when the audit has more outcomes than the target

**Lemma 6 — Dense fully variable signatures.** If $k>r$, matrices $Q$ for which every $r$-column minor is nonzero are dense in $(\Delta_r^\circ)^k$. At each such matrix all audit weights are variable.

**Proof.** Choose distinct $t_j\in(0,1)$ and $0<\delta<1/[r(r-1)]$. Let
$$
p_i(t)=1/r+\delta t^i\ (i<r),\qquad
p_r(t)=1/r-\delta\sum_{i=1}^{r-1}t^i.
$$
These columns are positive. They are an invertible linear transform of the vectors $(1,t,\ldots,t^{r-1})^\mathsf T$, so Vandermonde nonsingularity makes every $r$-column minor of the resulting $Q_*$ nonzero.

For any positive $Q$, set $Q_\epsilon=(1-\epsilon)Q+\epsilon Q_*$. Each minor is a polynomial nonzero at $\epsilon=1$, and has only finitely many zeros. Arbitrarily small positive $\epsilon$ avoid the finitely many forbidden values. To get density in the actual signature image, choose a positive representative $w$ and set $q_\epsilon=Q_\epsilon w$; do not perturb $Q$ while arbitrarily fixing $q$.

Deleting any column leaves at least $r$ columns, of rank $r$, so (15) makes every index variable. $\square$

**Theorem 7 — Global classification for $k>r$.** For ambient $C^1$ $J$, the following are equivalent:

1. The projected negative source Fisher velocity is representative-independent everywhere on $S$.
2. $C(p_j)J_j=0$ for every conditional slot at every point of $S$.
3. There is a $C^1$ function $\phi:\Delta_r^\circ\to\mathbb R$ with $J(P,q)=\phi(q)$ on $S$.

If $J$ is $C^2$, then $\phi$ is $C^2$, and these conditions are also equivalent to the maximal-flow descent in Theorem 5.

**Proof.** Theorem 4 forces all $a_j$ to vanish on the dense signatures of Lemma 6; continuity extends the vanishings to all of $S$. Define $\phi(q)=J(q,\ldots,q,q)$. At any $(P,q)\in S$, choose a positive representative $w$ and contract
$$
p_j(s)=(1-s)p_j+sq,\qquad 0\leq s\leq1.
$$
This remains positive and has $\sum_jw_jp_j(s)=q$. Each $J_j$ is constant across target coordinates and therefore annihilates the tangent $q-p_j$. The chain rule shows that $J$ stays constant along the contraction, proving $J(P,q)=\phi(q)$. This also proves the fixed-$q$ slice is star-shaped.

Conversely, equality on $S$ makes the source pullback precisely $\phi(Qw)$. Its projected equations are the weight-independent equations in §7.2, regardless of the off-image extension. Theorem 5 supplies the $C^2$ flow statement. $\square$

The conclusion is about the restricted objective on the admitted image. A smooth term supported outside that image is invisible to the source pullback.

### 7.2 Positive target tilts and maximal intervals

For $E=\phi(q)$, equations (12)–(13) reduce to
$$
\dot w_j=-w_j\langle h(q),p_j-q\rangle,\qquad
\dot p_j=-C(p_j)h(q),\qquad \dot q=-C(q)h(q).                  \tag{18}
$$
Unlike a merely set-theoretic projected field, the $(P,q)$ equations are $C^1$ on all of $A$ when $\phi$ is $C^2$.

For a positive target weight vector $\ell$, define
$$
Z_p(\ell)=\sum_i\ell_ip_i,\qquad
L_\ell(p)=\frac{\operatorname{diag}(\ell)p}{Z_p(\ell)}.
$$
Tilting the joint law by its target coordinate gives
$$
\mu'_{ji}=\frac{\ell_i\mu_{ji}}{Z_q(\ell)},\quad
p'_j=L_\ell(p_j),\quad q'=L_\ell(q),\quad
w'_j=\frac{w_jZ_{p_j}(\ell)}{Z_q(\ell)}.                      \tag{19}
$$
Thus the signature update needs only $P,q$. Composition multiplies tilt vectors coordinatewise; reciprocal tilts invert the operation, and a common positive scalar is irrelevant. Rank and the set of variable indices are unchanged because $Q'$ is obtained by invertible diagonal row and column scalings.

Along a target solution let
$$
\ell_i(t)=\exp\!\left(-\int_0^t h_i(q(s))\,ds\right).
$$
Differentiating (19) gives (18). On every compact subinterval of the target's maximal interior interval, the tilt remains finite and positive. Formula (19) therefore lifts that whole interval to a source solution. Conversely, any source extension gives a target extension. Source, target, and signature trajectories have the same maximal interior interval, and the signature flow is continuous in its ordinary subspace topology.

This does not imply completeness for arbitrary $C^2$ $\phi$. If the coordinate differences of $h$ are bounded, a scalar gauge makes the tilt finite and positive on every finite interval, giving completeness. But $\phi(q)=\log q_1$ yields
$$
\dot q_1=-(1-q_1),\qquad
q_1(t)=1-(1-q_1(0))e^t,
$$
which reaches zero at the finite time $\log(1/(1-q_1(0)))$. No positive-domain extension is asserted.

### 7.3 Sharpness for every $2\leq k\leq r$

Set
$$
J(P,q)=H(P)=\det(Q^\mathsf TQ).
$$
By Cauchy–Binet,
$$
H(P)=\sum_{\substack{I\subseteq\{1,\ldots,r\}\\ |I|=k}}
\det(Q_I)^2.
$$
When $\operatorname{rank}Q<k$, every determinant in the sum vanishes, and therefore the whole first differential of $H$ vanishes. These are exactly the matrices with nonsingleton weight fibres. They give stationary source states. At full column rank every weight fibre is a singleton. Theorem 4 therefore gives global velocity descent, and Theorem 5 gives maximal-flow descent.

The source flow is complete. Since $J_q=0$, the weights are constant. Polynomial derivatives of $H$ are bounded on the product of closed simplexes. For each fixed positive $w$, equation (12) consequently bounds every $d\log p_{ji}/dt$ on finite time intervals. No conditional probability reaches zero in finite positive or negative time; compactness and ordinary continuation extend the flow for all real times.

Nevertheless $H$ is not a function of $q$. Choose $k$ affinely independent target-tangent vectors $v_j$ with $\sum_jv_j=0$, possible because $k-1\leq r-1$. For small $\epsilon>0$, set $p_j=q+\epsilon v_j$, $w_j=1/k$. Their average stays $q$, and their columns are linearly independent: summing a putative column relation gives zero sum of coefficients, after which affine independence forces every coefficient to vanish. Hence $H>0$. At $p_j=q$ for all $j$, with the same target marginal, $H=0$.

For $r=k=2$, if $p_1=(a,1-a)$, $p_2=(b,1-b)$, then $H=(a-b)^2$. For $k>r$, the Gram determinant is identically zero, so it cannot contradict Theorem 7. The strict threshold is sharp. No simpler global classification for all $k\leq r$ is asserted beyond Theorems 4–5. [4]

### 7.4 Descent need not give a continuous signature velocity

The binary example also separates two regularity claims. Take
$$
a=\frac12+\epsilon,\quad b=\frac12,\quad w_1=\epsilon^2,
\qquad 0<\epsilon<\frac12.
$$
For $H=(a-b)^2$, equation (12) gives
$$
\dot a=-\frac{2a(1-a)(a-b)}{w_1}
=-\frac{2(1/4-\epsilon^2)}{\epsilon}.
$$
The signatures tend to $p_1=p_2=q=(1/2,1/2)$, whose source fibres are stationary, but the displayed velocity is unbounded. Every member of the sequence has strictly positive joint cells. Thus a representative-independent, complete source flow can coexist with a discontinuous projected velocity in the ordinary signature topology.

This explicit specialization follows from the preceding source equations and is included to make their regularity limitation concrete. It is not an assertion that the source vector field is discontinuous, or a field-wide novelty claim.

## 8. Preserving one objective versus preserving an entire metric

The pointwise Fisher criterion differs from the expected-value row-space criterion. For the interior three-outcome example, use columns
$$
p_1=(1/4,3/4),\quad p_2=(1/2,1/2),\quad p_3=(3/4,1/4),
$$
and weights $w=(1/4,1/2,1/4)$, $w'=(1/8,3/4,1/8)$. Both give $q=(1/2,1/2)$. With $J=p_{1,1}$,
$$
a_1=(3/16,-3/16),\qquad h=0,\qquad a_2=a_3=0.
$$
The first conditional velocity is $(-3/4,3/4)$ at $w$ and $(-3/2,3/2)$ at $w'$, while both target velocities equal $(-3/16,3/16)$. Equal target speed does not preserve the retained conditional answers' speed.

For a general linear readout there is a useful separate criterion. Let $U_0\subseteq\mathbb R^n$ be open, $L:\mathbb R^n\to\mathbb R^m$ have full row rank, and $G(x)$ be a smooth positive-definite metric. For every smooth objective $j(Lx)$, the projected negative gradient is
$$
-LG(x)^{-1}L^\mathsf T\nabla j(Lx).                           \tag{20}
$$
It depends only on $Lx$, for every such objective, if and only if the cometric
$$
A(x)=LG(x)^{-1}L^\mathsf T
$$
is constant on each readout fibre.

For sufficiency, fibre constancy gives a smooth $\bar A(z)$, locally through linear sections, and (20) is the gradient for coarse metric $\bar A(z)^{-1}$. Positivity follows from
$$
v^\mathsf TA(x)v=(L^\mathsf Tv)^\mathsf TG(x)^{-1}(L^\mathsf Tv)>0.
$$
For necessity, apply (20) to every coordinate objective $j(z)=z_i$; its projected field reads the $i$-th column of $A$. Every column must be fibre-constant. [6]

The necessity quantifies over all objectives. One objective can be insensitive to a varying cometric direction. This infinitesimal theorem also does not identify source and quotient maximal lifetimes: boundary behaviour requires additional proof, supplied for the special Fisher model by Theorem 5. For example, retaining only a visible coordinate while discarding a two-valued metric label can turn the same objective's velocity from $1$ to $2$, changing arrival time at a visible threshold from $1$ to $1/2$. Rescaling time changes the clock contract.

## 9. How much supplementary information is necessary?

### 9.1 The exact finite-state answer

Let $E$ be a nonempty finite set of declared information states. Each state has a visible record $r(s)$, a required label, enabled actions, costs, and a joint outcome/next-state kernel $K_a(s,o,t)$. A partition preserves the contract if equal-block states have equal records, labels, permissions, costs, and, for every block $D$,
$$
\sum_{t\in D}K_a(s,o,t)=\sum_{t\in D}K_a(s',o,t).              \tag{21}
$$
This is a joint-kernel requirement, stronger than unrestricted equality of selected traces.

Start with the partition $P_0$ determined by the record, labels, actions, and costs. Repeatedly split blocks according to the outcome-indexed transition masses into the current blocks.

**Theorem 8 — Coarsest finite refinement and minimum supplement.** The iteration terminates after at most $|E|-|P_0|$ strict refinements and produces the coarsest contract-preserving partition $P_*$. If $N_z$ is the number of $P_*$-blocks inside $r^{-1}(z)$, the minimum common alphabet of a deterministic supplementary label, retained alongside $r$, has size
$$
M_*=\max_zN_z,\qquad b_*=\lceil\log_2M_*\rceil
$$
fixed-length bits.

**Proof.** Each strict split increases the number of blocks. At stabilization, (21) and the initial requirements hold. Any other preserving partition refines $P_0$. If it refines $P_i$, each $P_i$-block is a union of its blocks, so equality of transition masses into those smaller blocks implies equality into every $P_i$-block. It therefore refines $P_{i+1}$. Induction proves coarseness.

Within an $r$-fibre, the supplementary label must distinguish its $N_z$ final blocks. Conversely, enumerate those blocks separately in each fibre, reusing labels in different fibres because $r$ is retained. An alphabet of size $M_*$ suffices. $\square$

Adding actions or required observables can only refine $P_*$ and cannot reduce this minimum. The result does not preserve every narrative detail: four states differing in two independently relevant support/cost distinctions need two bits only when both distinctions belong to the contract. It is a finite alphabet result, not a bound for a continuum of hidden weights. [6]

### 9.2 Supplementing selected expected values

Fix the positive fibre (9), and let a finite matrix $H$ list required expectation rows. Set $N=\ker Q$ and
$$
s=\operatorname{rank}(H|_N)
=\operatorname{rank}\begin{bmatrix}Q\\H\end{bmatrix}
-\operatorname{rank}Q.                                      \tag{22}
$$

**Corollary 9 — Exact continuous utility supplement.** On this fixed fibre, $s$ continuous real coordinates are necessary and sufficient to recover $Hw$, allowing arbitrary decoders. A finite-valued exact supplement exists if and only if $s=0$.

**Proof.** Choose a basis of the independent restrictions of the rows of $H$ to $N$. Retaining those linear values determines all other required values up to constants fixed by $Qw=q$, giving sufficiency. For necessity choose an $s$-dimensional subspace $L\subseteq N$ on which $H$ is injective. A sufficiently small open ball in $w^0+L$ lies in the positive fibre. An exact supplement must be injective on this ball, since equal encoded values imply equal $Hw$. Invariance of domain excludes a continuous injection into fewer than $s$ coordinates. If $s>0$, $Hw$ takes infinitely many values along a positive line segment, excluding a finite alphabet even without encoder continuity. If $s=0$, no supplement is needed. $\square$

Equation (22) follows because adjoining the rows of $H$ to $Q$ adds exactly their independent restrictions to $\ker Q$. This corollary combines the existing expectation-fibre and continuous-dimension arguments; its explicit combined formulation and proof are part of this exposition's independent review, not retroactively attributed to an earlier review. It concerns one fixed audit and a finite set of expected quantities. Future interventions require closure of the enlarged observable contract, not merely this one-step supplement.

### 9.3 The full-source metric requires all hidden weights

For a conditional coordinate $p_{ji}$, (11) gives its ambient Fisher squared gradient norm:
$$
\|\operatorname{grad}_g p_{ji}\|^2
=\frac{p_{ji}(1-p_{ji})}{w_j}.                               \tag{23}
$$
The numerator is known and strictly positive. Retaining these norms for a fixed target coordinate $i$ and $j=1,\ldots,k-1$ recovers those weights; normalization recovers the last. Thus any record preserving the signature and this norm family is injective on the whole source domain. No regularity assumption on that record is needed for this reconstruction.

On a fixed $P,q$ fibre,
$$
d=k-\operatorname{rank}Q
$$
is its affine dimension. If $d>0$, no finite-valued supplement preserves (23) exactly. Among continuous real-coordinate supplements, precisely $d$ are necessary and sufficient: injectivity and invariance of domain give the lower bound, and coordinates in a basis of $\ker Q$ attain it. At $d=0$, no supplement is needed. [4], [5]

These are norms of ambient source gradients. They are not gradients computed after fixing $P$ inside the fibre, where the conditional coordinates themselves are constant. The lower bound is for a fixed fibre, not a globally continuous minimal chart across rank-changing strata. Arbitrary discontinuous one-real encodings are outside the continuous-coordinate assertion. A discretization changes the exact problem.

The hierarchy is now explicit. Posterior answers need no supplement beyond $F$. Selected expectations need $s\leq d$ continuous coordinates. The full norm contract needs $d$. A chosen reduced metric can avoid that last requirement only by changing the metric contract, not by claiming to preserve the original one.

## 10. Assumptions, negative results, and open scope

The positive-fibre and Fisher theorems quantify over the full strictly positive joint-law family. On a constrained reachable family, use its actual differences; the density proof may fail. For example, with three audit outcomes, a binary target, fixed weights $w_j=1/3$, and $J=p_{1,1}$, equation (12) has $\dot w=0$. The section is invariant and its signature is injective, so the flow descends there despite conditional dependence at fixed $q$. This does not contradict the full-domain rigidity theorem.

Strict positivity supplies small kernel perturbations, division by weights, feasible audit outcomes, and nondegenerate conditional Fisher tangents. Boundary strata and null events need their own analysis. Ambient $C^1$ regularity supports the global classification; $C^2$ gives the stated unique $C^1$ source flow. Pointwise coincidence at one signature is not a trajectory theorem.

The preserved negative findings are substantive: separate marginals can lose audit-dependent answers; posterior equivalence can lose inquiry value; a conditional loss can have nonprojectable Fisher dynamics; a projectable complete flow can lack ordinary-signature velocity continuity; a target-only flow can reach the boundary in finite time; and finite labels cannot encode a positive-dimensional exact metric fibre.

Unresolved generalizations should be stated as such. This treatment does not classify every globally descending objective for $k\leq r$ beyond the exact criterion, provide global minimal charts across changing rank, solve arbitrary adaptive value preservation from posterior-only equivalence, or give stable approximate/noisy variants of every exact construction. Nor does it turn the declared probability law, loss, or metric into an empirical model of cognition or a philosophical judgment about actual warrant.

## 11. Attribution, evidence, and edition boundary

The predictive observable theorem and its continuous-coordinate proof are inherited from *Continuation-Complete Orthings*, with the established predictive-state ancestry in [8]. Support-sensitive fibre factorization is also developed in the information-and-revision lineage [7]. The audit transport, paired posterior test, fixed-audit classification, and inquiry-value separation are consolidated from [2]–[3]; their exact final source versions have separately bound ordinary reviews. The Fisher classification and its row-rescaling maximal-flow proof come from [4]. That source credits the row-rescaling proof to its finite-audit mathematical contributor; it is not counted as independent corroboration merely because the contributor also served in a review role. The finite and continuous supplement arguments reconcile [5–6].

The explicit discontinuous-signature sequence in §7.4 and the combined utility-coordinate corollary in §9.2 are deductions written out for this exposition. They make no field-wide priority claim and require review as part of this edition. The sources' historical finite controls corroborate their own bounded statements; they do not constitute new execution of this text, universal proof by enumeration, or Lean certification.

The historical sidecar review is conditional on the ambient norm identity and requested normalization of $q$; both the identity and normalization are proved or explicit here. A review of audit covariance is not treated as a review of the full Fisher classification. Frozen source text that once said “review pending” is distinguished from its later exact-version review. No unavailable historical output is manufactured.

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




