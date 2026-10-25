# Common repair and the geometry of coherent forecasts

## Status and scope

This chapter is a mathematical exposition of public Orthemology research on repairing an incoherent forecast when several scoring standards remain admissible. It consolidates proofs, corrections and counterexamples; it does not amend an accepted paper, assert new priority for classical results, or confer scientific acceptance on an application. The mathematical object is a finite truth hull with specified losses. Claims about epistemic authority or human cognitive implementation require additional premises.

The central question is whether **one coherent forecast improves on the same disturbed forecast under every specified standard and every admissible truth**. For quadratic losses, agreement of weighted projections answers the question exactly. For smooth additive losses, this local geometry yields strong rigidity on dependency blocks of rank at least two. Rank-one blocks admit a larger class governed by comparison of generalized means. At the boundary, first-order agreement need not yield exact repair, a zero second-order margin does not decide feasibility, and even the complete Taylor data at one point can fail to determine the answer. A further counterexample holds the entire score functions fixed: changing only the admissible joint truth hull changes repair from possible to impossible.

All necessary arguments and concrete counterexamples are given below. Historical formal sources are identified at the end as inspectable verification dependencies; reading this chapter does not require executing them.

## 1. The common-repair problem

### 1.1 Truth, coherence and a shared decision

Let $`v_1,\ldots,v_m`$ be a nonempty finite list in $`\mathbb R^n`$, and put

```math
C=\mathrm{conv}\{v_1,\ldots,v_m\},\qquad
p\in\mathrm{ri}C,\qquad
T=\mathrm{span}(C-p).
```

Here relative interior is taken in the affine hull of $`C`$. The vectors $`v_j`$ need not be affinely independent, and repeated entries are allowed. A coherent forecast belongs to $`C`$. We examine

```math
b_\varepsilon=p+\varepsilon h,\qquad \varepsilon>0,
```

where the direction $`h\notin T`$ is transverse and the forecast remains in the domain of every loss for sufficiently small $`\varepsilon`$. Transversality makes $`b_\varepsilon`$ incoherent. A **common weak repair** is one $`c\in C`$ satisfying

```math
L_k(c,v_j)\leq L_k(b_\varepsilon,v_j)
\quad\text{for every }k,j.
```

A common strict repair makes every inequality strict. An $`\eta`$-repair replaces the right side by $`L_k(b_\varepsilon,v_j)+\eta`$, where $`\eta\geq0`$ is measured in the fixed units of the losses. The repair may depend on $`p,h,\varepsilon`$ and the family of standards, but it cannot depend on the unknown truth or on which standard will eventually be used.

There are two different local quantifiers. Existence along a sequence $`\varepsilon_\nu\downarrow0`$ is a weak requirement useful in necessity arguments. Existence for every sufficiently small positive $`\varepsilon`$ is a stronger conclusion. We state the distinction whenever it matters.

### 1.2 Positive barycentric weights

Every $`p\in\mathrm{ri}C`$ admits

```math
p=\sum_{j=1}^m\lambda_jv_j,\qquad
\lambda_j>0,\qquad \sum_j\lambda_j=1.
\quad\text{(1)}\quad
```

To prove this for the entire listed population, let $`\bar v=m^{-1}\sum_jv_j`$. Relative interior permits a point $`y=p+t(p-\bar v)\in C`$ for some $`t>0`$. Express $`y=\sum_j a_jv_j`$ with $`a_j\geq0`$ and $`\sum_j a_j=1`$. Then

```math
p=\frac{t}{1+t}\bar v+\frac1{1+t}y
  =\sum_j\left(\frac{t}{m(1+t)}+\frac{a_j}{1+t}\right)v_j.
```

Every displayed weight is positive. In particular, if numbers $`q_j\geq0`$ have $`\sum_j\lambda_jq_j=0`$, each $`q_j`$ is zero. Several rigidity proofs below depend on this implication; replacing relative interior by an arbitrary boundary point would lose it.

### 1.3 Bregman losses and two identities

For a differentiable strictly convex potential $`F`$, use the truth-first Bregman convention

```math
D_F(v,b)=F(v)-F(b)-\nabla F(b)\cdot(v-b),
\qquad L_F(b,v)=D_F(v,b).
\quad\text{(2)}\quad
```

Thus the forecast is the second argument. Affine additions to $`F`$ do not change $`D_F`$; multiplying $`F`$ by a positive constant multiplies the loss.

The score difference between two forecasts is affine in $`v`$. Consequently inequalities verified at every listed truth extend to every $`v\in C`$, and averaging with (1) gives

```math
\sum_j\lambda_j\bigl(D_F(v_j,c)-D_F(v_j,b)\bigr)
 =D_F(p,c)-D_F(p,b).
\quad\text{(3)}\quad
```

A direct expansion also gives the three-point identity

```math
D_F(v,b)-D_F(v,c)
=D_F(c,b)+
 \bigl(\nabla F(c)-\nabla F(b)\bigr)\cdot(v-c).
\quad\text{(4)}\quad
```

These identities separate two optimization problems that should not be confused. To construct a coherent projection, minimize $`c\mapsto D_F(c,b)`$, with the candidate in the first argument. This is a strictly convex function of $`c`$. The truth-indexed forecast loss $`c\mapsto D_F(v,c)`$ need not be convex.

If $`F`$ is $`C^3`$ near $`p`$, write $`H_F=\nabla^2F(p)`$ and $`K_F=\nabla^3F(p)`$. Differentiation in the forecast gives

```math
\nabla_bD_F(v,b)=\nabla^2F(b)(b-v),
\qquad
D_b^2D_F(v,p)[u,u]
=H_F[u,u]+K_F[p-v,u,u].
\quad\text{(5)}\quad
```

The divergence and projection framework originates with Bregman [1]. The results below concern simultaneous repair under several standards, rather than priority for that framework.

## 2. Quadratic repair: exact compatibility and quantitative separation

### 2.1 A directionwise equivalence

Let $`\mathcal W`$ be any nonempty family of positive-definite symmetric matrices, including an infinite family, and define

```math
L_W(b,v)=\|b-v\|_W^2=(b-v)^\top W(b-v).
```

Let $`P_W`$ be the $`W`$-orthogonal projection onto $`T`$, and let $`Q_W=I-P_W`$.

**Theorem 1 — Exact quadratic common repair.** For fixed $`p\in\mathrm{ri}C`$ and $`h\notin T`$, the following are equivalent:

1. There are $`\varepsilon_\nu\downarrow0`$ and common weak repairs $`c_\nu\in C`$.
2. The vector $`P_Wh`$ is the same for every $`W\in\mathcal W`$.
3. For some $`z\in T`$, the single rule $`c_\varepsilon=p+\varepsilon z`$ is a common strict repair for every sufficiently small positive $`\varepsilon`$.

If these conditions hold, $`z=P_Wh`$ and

```math
L_W(b_\varepsilon,v)-L_W(c_\varepsilon,v)
=\varepsilon^2\|Q_Wh\|_W^2>0
\quad(v\in C).
\quad\text{(6)}\quad
```

**Proof.** Fix one matrix $`W_0`$. Averaging the weak-repair inequalities yields

```math
\|c_\nu-p\|_{W_0}^2
\leq \varepsilon_\nu^2\|h\|_{W_0}^2.
```

Hence $`z_\nu=(c_\nu-p)/\varepsilon_\nu`$ is bounded in $`T`$. Pass to a subsequence with $`z_\nu\to z\in T`$. For each fixed $`W`$ and each listed truth, expand the gain and divide by $`\varepsilon_\nu`$. The limit is

```math
2(p-v_j)^\top W(h-z)\geq0.
```

Its strictly positive barycentric average is zero, so every term is zero. The vectors $`p-v_j`$ span $`T`$, whence $`h-z`$ is $`W`$-orthogonal to $`T`$, and $`z=P_Wh`$. The same convergent subsequence works for every fixed $`W`$; no extraction over the possibly infinite family is required.

Conversely, if the projected vector is common, relative interior makes $`p+\varepsilon z\in C`$ for all sufficiently small $`\varepsilon`$. Its difference from $`b_\varepsilon`$ is $`W`$-normal to $`T`$. Pythagorean expansion proves (6). Since $`h\notin T`$, the normal vector is nonzero. The implication from strict to weak repair is immediate. $`\square`$

There is no asserted uniform positive gain over an infinite family of matrices. The common feasible scale is geometric, but the positive numbers $`\|Q_Wh\|_W^2`$ may have infimum zero.

Universal directionwise repair is equivalent to equality of the projection operators. All projections already agree on $`T`$, so it is enough to compare their action on directions spanning $`\mathbb R^n/T`$. This is a sufficient finite test set, not a theorem that a particular query count is minimal.

### 2.2 The simplex reveals relative weights

For the categorical simplex $`C=\{x\geq0:\sum_i x_i=1\}`$, its tangent is $`T=\{u:\sum_i u_i=0\}`$. If $`W=\mathrm{diag}(w_1,\ldots,w_n)`$, then

```math
P_Wh=h-\left(\sum_i h_i\right)r_W,\qquad
(r_W)_i=\frac{w_i^{-1}}{\sum_jw_j^{-1}}.
\quad\text{(7)}\quad
```

Thus one transverse direction already identifies the relative diagonal weights: common repair for that direction requires the same normalized reciprocal vector, equivalently proportional weight vectors.

A symmetry conclusion needs an explicit premise about one fixed decision problem. Suppose a normalized candidate class of weights is closed under a permutation group, and one repair must work for every member of that class. Theorem 1 forces the class to be a singleton, so the surviving weights are constant on each group orbit; a transitive group forces equal weights. Merely relabelling the entire problem covariantly does not provide the premise that one fixed output must accommodate all the relabelled standards.

### 2.3 A finite-scale error bound

Choose $`r>0`$ with the Euclidean tangent ball $`B_T(p,r)\subset C`$. Let

```math
m_W=\lambda_{\min}(W),\qquad q_W=\|Q_Wh\|_W^2,
\qquad x_W=p+\varepsilon P_Wh.
```

If $`\varepsilon\|P_Wh\|_2\leq r/2`$, every all-state $`\eta`$-repair obeys

```math
\|c-x_W\|_2\leq
\frac{\varepsilon^2q_W+\eta}{r\,m_W}.
\quad\text{(8)}\quad
```

Indeed, put $`d=c-x_W`$. If $`d\ne0`$, the truth point

```math
v=x_W-\rho\,\frac d{\|d\|_W},
\qquad \rho=\frac r2\sqrt{m_W},
```

belongs to $`C`$. By (6), its repair gain is
$`\varepsilon^2q_W-2\rho\|d\|_W-\|d\|_W^2`$.
The $`\eta`$-condition bounds the two nonnegative subtracted terms by $`\varepsilon^2q_W+\eta`$, proving (8).

For two matrices $`W,Z`$, let $`d_0=\|P_Wh-P_Zh\|_2`$. Applying (8) twice gives

```math
\varepsilon d_0\leq\varepsilon^2A+\eta B,
\quad
A=\frac1r\left(\frac{q_W}{m_W}+\frac{q_Z}{m_Z}\right),
\quad
B=\frac1r\left(\frac1{m_W}+\frac1{m_Z}\right).
\quad\text{(9)}\quad
```

Therefore an error allowance $`\eta=o(\varepsilon)`$ still forces exact projection compatibility. Errors of order $`\varepsilon`$ can conceal disagreement.

Randomization independent of truth and standard does not circumvent the quadratic result if the requirement is expected loss. If a random repair $`X`$ lies in $`C`$, its mean lies in $`C`$, and
$`L_W(\mathbb EX,v)\leq\mathbb EL_W(X,v)`$.
The mean is consequently a deterministic repair whenever the randomized rule is one.

### 2.4 Exact binary repair cells and the information they encode

Take $`p=(1/2,1/2)`$, $`b_\varepsilon=(1/2+\varepsilon,1/2)`$, $`0<\varepsilon\leq1/4`$, and $`W_\alpha=\mathrm{diag}(\alpha,1-\alpha)`$ with $`0<\alpha<1`$. Write a coherent candidate as $`(t,1-t)`$. The exact $`\eta`$-repair cell is

```math
\left[
1-\sqrt{\frac14-\alpha\varepsilon+\alpha\varepsilon^2+\eta},
\quad
\sqrt{\frac14+\alpha\varepsilon+\alpha\varepsilon^2+\eta}
\right]\cap[0,1].
\quad\text{(10)}\quad
```

The quadratic projection is $`t_\alpha=1/2+\alpha\varepsilon`$, with gain $`D_\alpha=\alpha(1-\alpha)\varepsilon^2`$. Directly from the two endpoint inequalities,

```math
|t-t_\alpha|\leq2(D_\alpha+\eta)
\leq\frac{\varepsilon^2}{2}+2\eta.
\quad\text{(11)}\quad
```

For example, when $`t-t_\alpha\geq0`$, the loss increase at the zero endpoint is at least $`2t_\alpha(t-t_\alpha)`$; the opposite sign is controlled by the other endpoint. The weaker common bound uses $`t_\alpha,1-t_\alpha\geq1/4`$.

If $`\alpha`$ ranges over $`[a,b]\subset(0,1)`$, the common cell has the endpoints in (10) with $`\alpha=b`$ in the lower bound and $`\alpha=a`$ in the upper bound. Put

```math
A=\frac14-b\varepsilon+b\varepsilon^2+\eta,\qquad
B=\frac14+a\varepsilon+a\varepsilon^2+\eta.
```

It is nonempty exactly when $`\sqrt A+\sqrt B\geq1`$. For $`A,B\geq0`$, this is equivalent to
$`A+B\geq1`$ or $`4AB\geq(1-A-B)^2`$.
For $`\eta=0`$, write $`m=(a+b)/2`$ and $`d=b-a`$. In the branch $`A+B<1`$, the same condition is

```math
d^2\varepsilon^3-4d\varepsilon^2m+2d
 +4\varepsilon m^2-4\varepsilon m\leq0.
\quad\text{(12)}\quad
```

In a compact subinterval of $`0<m<1`$, the limiting admissible width is
$`d\leq2m(1-m)\varepsilon+O(\varepsilon^3)`$.

Every exact repair supplies the estimate
$`\widehat\alpha=(t-1/2)/\varepsilon`$ with
$`|\widehat\alpha-\alpha|\leq\varepsilon/2`$; with tolerance, the bound becomes
$`\varepsilon/2+2\eta/\varepsilon`$.
Consequently exact repair cells of parameters separated by more than $`\varepsilon`$ are disjoint. If a deterministic observation with $`N`$ possible outputs supports exact repair throughout $`[a,b]`$, each observation class has diameter at most $`\varepsilon`$, so
$`N\varepsilon\geq b-a`$.
A packing of $`M`$ pairwise separated parameters requires $`M`$ distinct observation classes, hence at least $`\lceil\log_2M\rceil`$ bits in a fixed-length binary encoding. A zero-error randomized output cannot assign positive probability to an output incompatible with the true parameter.

These are operational distinguishability statements. They do not establish that a repairer consciously represents the estimate, or that geometric identifiability makes a scoring standard normatively authoritative.

## 3. Dependency blocks and diagonal rigidity

An elementary vector of $`T`$ is a nonzero $`u\in T`$ whose support contains no strictly smaller support of a nonzero vector in $`T`$. Join two coordinates when they occur in the support of one elementary vector, and take the connected components $`B`$ of this graph, including isolated coordinates. Set

```math
T_B=T\cap\mathbb R^B.
```

The elementary vectors span $`T`$. To see this, if a vector is not elementary, choose a nonzero vector with smaller support and subtract a suitable multiple to cancel one nonzero coordinate. Both resulting vectors have strictly smaller support, and induction applies. The elementary supports therefore give

```math
T=\bigoplus_B T_B.
\quad\text{(13)}\quad
```

This is coordinate dependence in the affine truth structure. It is not probabilistic independence.

**Theorem 2 — Diagonal metrics agree exactly blockwise.** For positive diagonal matrices $`W=\mathrm{diag}(w_i)`$ and $`Z=\mathrm{diag}(z_i)`$, the following are equivalent:

1. $`P_W=P_Z`$.
2. $`D=\mathrm{diag}(z_i/w_i)`$ preserves $`T`$.
3. The ratio $`z_i/w_i`$ is constant on each dependency block.

**Proof.** The kernel of $`P_W`$ is $`W^{-1}T^\perp`$. Equality of the kernels is equivalent to $`D T^\perp=T^\perp`$. Since $`D`$ is symmetric and invertible, this is equivalent to $`DT=T`$.

Suppose $`D`$ preserves $`T`$, and let $`u`$ be elementary. The spectral projection onto each eigenspace of $`D`$ is a polynomial in $`D`$, by finite Lagrange interpolation on its distinct eigenvalues. It preserves $`T`$. If the support of $`u`$ met two eigenspaces, one nonzero projection would give a vector of strictly smaller support in $`T`$, a contradiction. Thus the diagonal entries of $`D`$ agree on every elementary support and hence on each connected block. Conversely, blockwise constancy makes every elementary vector an eigenvector. Their span is invariant. $`\square`$

The elementary-vector method has classical antecedents in Rockafellar [2]. The diagonal stabilizer statement is the positive-real form of the matroid-component description in Denham, Proposition 2.12 [3]. If a matrix has row space $`T`$, the minimal supports used here are cocircuits of its column matroid, equivalently circuits of the dual; a circuit/cocircuit reversal would misidentify the stated representation, although the component partition is unchanged by duality.

Singleton blocks require care. A singleton can be free, with $`e_i\in T`$, or constant, with $`u_i=0`$ for all $`u\in T`$. Both allow arbitrary diagonal scaling at the purely quadratic level. The smooth theorem below excludes constant coordinates and states separately what happens on free ones. If $`T=\mathbb R^n`$, there is no transverse incoherence to repair; if $`T=\{0\}`$, the coherent hull is a singleton and all projections vanish.

## 4. Smooth additive rigidity on higher-rank blocks

### 4.1 Hessian agreement is a necessary local condition

Assume first that

```math
F(x)=\sum_i f_i(x_i),\qquad G(x)=\sum_i g_i(x_i),
\quad\text{(14)}\quad
```

where the scalar functions are finite and continuous on $`[0,1]`$, are $`C^2`$ on $`(0,1)`$, and satisfy $`f_i'',g_i''>0`$ there. Truth vectors lie in $`[0,1]^n`$, and every coordinate varies on $`C`$, so every $`p\in\mathrm{ri}C`$ has coordinates in $`(0,1)`$.

Suppose a common weak repair exists along $`\varepsilon_\nu\downarrow0`$. Equation (3) gives
$`D_F(p,c_\nu)\leq D_F(p,b_{\varepsilon_\nu})=O(\varepsilon_\nu^2)`$.
This forces $`c_\nu\to p`$, even when the derivatives of $`f_i`$ diverge at endpoints. For a scalar coordinate,

```math
D_f(p_i,x)=\int_x^{p_i}(p_i-u)f''(u)\,du.
\quad\text{(15)}\quad
```

The integral is positive away from $`x=p_i`$, and on any fixed interval around $`p_i`$ it is bounded below by a positive quadratic. Leaving that interval cannot make it tend to zero. After localization, (15) yields $`c_\nu-p=O(\varepsilon_\nu)`$. The first-order expansion and positive barycentric averaging used in Theorem 1 then show

```math
P_{H_F(p)}h=P_{H_G(p)}h.
\quad\text{(16)}\quad
```

Here and below a boundary candidate for which a forecast loss is undefined or infinite is not an admissible finite-loss repair.

The same conclusion holds for common $`\eta_\nu`$-repairs with $`\eta_\nu=o(\varepsilon_\nu)`$, but averaging alone is insufficient: it would give only a square-root bound in $`\eta_\nu`$. The all-state inequalities supply the missing control. Choose $`B_T(p,r)\subset C`$, put $`\xi=c-p`$, and $`u=\nabla F(c)-\nabla F(b_\varepsilon)`$. By affinity in truth, comparison at all $`p+t`$, $`\|t\|_2\leq r`$, gives

```math
r\|P_Tu\|_2
\leq D_F(p,b_\varepsilon)+\eta-D_F(p,c)
\leq O(\varepsilon^2)+\eta.
\quad\text{(17)}\quad
```

After $`c\to p`$, expand
$`u=H_F(p)\xi-\varepsilon H_F(p)h+o(\|\xi\|)+o(\varepsilon)`$.
The operator $`P_TH_F(p)`$ restricted to $`T`$ is positive definite. Absorbing the small remainder in (17) yields
$`\xi=O(\varepsilon+\eta)=O(\varepsilon)`$.
Divide the original inequalities by $`\varepsilon`$ and apply (1) to recover (16).

### 4.2 A categorical rigidity theorem

**Theorem 3 — Universal categorical repair.** Let $`C`$ be the categorical simplex with $`n\geq3`$, and let the fixed additive generators satisfy (14). The following are equivalent:

1. For every $`p\in\mathrm{ri}C`$, weak common repairs exist along a sequence approaching $`p`$ on the single transverse direction $`h=e_1`$.
2. For every interior $`p`$ and every transverse $`h`$, strict common repair exists for every sufficiently small positive $`\varepsilon`$.
3. There are one constant $`a>0`$ and constants $`b_i,d_i`$ such that

```math
f_i(x)=a\,g_i(x)+b_ix+d_i\qquad(0\leq x\leq1).
\quad\text{(18)}\quad
```

Replacing condition 1 by the existence of $`o(\varepsilon)`$-repairs gives the same equivalence.

**Proof.** Equation (7) applied to the Hessians makes (16) equivalent to

```math
r_i(p_i):=\frac{f_i''(p_i)}{g_i''(p_i)}=a(p)
\quad\text{for every }i.
\quad\text{(19)}\quad
```

Fix two values $`s,t\in(0,1)`$ for coordinate $`i`$. Choose another coordinate $`j`$ and a small $`u>0`$ with $`s+u<1`$ and $`t+u<1`$. Because there is a third coordinate, both pairs can be completed to strictly positive simplex points. Equation (19) gives $`r_i(s)=r_j(u)=r_i(t)`$. Thus each ratio is constant; feasible pairs show that the constants agree. Integrating twice and using endpoint continuity gives (18).

Conversely, minimize $`D_G(c,b_\varepsilon)`$ over the compact set $`C`$. Its unique minimizer tends to $`p`$: the objective converges uniformly on $`C`$ to $`D_G(c,p)`$, whose unique minimum is $`p`$. It therefore lies in $`\mathrm{ri}C`$ for small $`\varepsilon`$, and
$`\nabla G(c)-\nabla G(b_\varepsilon)\perp T`$.
Equation (4) gives gain $`D_G(c,b_\varepsilon)>0`$ at every truth. By (18) the $`F`$-gain is $`a`$ times this gain. $`\square`$

The conclusion depends on fixed generators across contexts, additive separability, at least three categorical coordinates, and relative interior. None is an innocuous convention.

### 4.3 Binary and nonseparable counterexamples

For the binary coherent segment $`C=\{(t,1-t):0\leq t\leq1\}`$, take quadratic coordinate potentials and binary-entropy coordinate potentials

```math
f(x)=x^2,\qquad
g(x)=x\log x+(1-x)\log(1-x).
```

For an interior incoherent forecast $`(x,y)`$, the arithmetic correction
$`t=(x+1-y)/2`$ is a strict common repair. It is the Euclidean projection. For the logarithmic loss the two comparisons reduce to

```math
t^2-x(1-y)=\frac{(x+y-1)^2}{4},\qquad
(1-t)^2-(1-x)y=\frac{(x+y-1)^2}{4}.
\quad\text{(20)}\quad
```

Both are positive for an incoherent forecast. The curvatures $`2`$ and $`1/[x(1-x)]`$ are not proportional. Section 6 explains the broader rank-one reason.

Separability also matters. On the three-outcome simplex let $`a=(1,-1,0)`$ and

```math
F(x)=\frac12\|x\|_2^2,\qquad
G(x)=\frac12\bigl(\|x\|_2^2+(a\cdot x)^2\bigr).
\quad\text{(21)}\quad
```

Both Hessians have the same normal line spanned by $`(1,1,1)`$, so they have the same projection and common repair at every context. Yet the potentials are not positive affine rescalings. They can reverse rankings among coherent forecasts: at truth $`e_3`$, the points
$`c=(49/100,1/100,1/2)`$ and $`d=(1/3,1/3,1/3)`$
have unscaled squared losses $`2451/5000<2/3`$, whereas after adding $`(a\cdot x)^2`$ the first loss becomes $`3603/5000>2/3`$.

### 4.4 The general higher-rank theorem

Let $`l_i=\min_Cx_i`$, $`u_i=\max_Cx_i`$, and $`I_i=(l_i,u_i)`$. Assume $`l_i<u_i`$ for every coordinate. Use the dependency blocks of $`T`$ from Section 3. Suppose every nonsingleton block satisfies $`\dim T_B\geq2`$; singleton blocks are then free because constant coordinates have been excluded.

**Theorem 4 — Smooth rigidity by dependency block.** For fixed additive $`F,G`$ as in (14), universal local common repair is equivalent to the existence of constants $`a_B>0`$ such that

```math
f_i(x)=a_Bg_i(x)+b_ix+d_i
\quad\text{for }i\in B,\quad x\in[l_i,u_i],
\quad\text{(22)}\quad
```

on every nonsingleton block. No proportionality is required on a free singleton. “Universal local common repair” may mean weak repair along a sequence at every $`p,h`$, or existence of $`o(\varepsilon)`$-repairs there. Under (22), one gets strict repair for all sufficiently small positive $`\varepsilon`$.

**Proof of necessity.** The Hessian projections agree at each $`p`$. Theorem 2 makes $`r_i(p_i)=f_i''(p_i)/g_i''(p_i)`$ equal to one value $`a_B(p)`$ on a block. Since $`\dim T_B\geq2`$, two coordinate functionals on $`T_B`$ are linearly independent. Their joint map sends a relative neighborhood of $`p`$ to an open rectangle in $`\mathbb R^2`$. On that rectangle, $`r_i(s)=r_j(t)`$, so both are locally constant and $`a_B`$ is locally constant on $`\mathrm{ri}C`$. This relative interior is convex and connected, hence $`a_B`$ is constant. The image of $`\mathrm{ri}C`$ under coordinate $`i`$ is exactly $`I_i`$, so integration and continuity give (22).

**Proof of sufficiency.** Take the unique minimizer $`c`$ of $`D_G(c,b_\varepsilon)`$ on the actual hull $`C`$. As before, it tends to $`p`$ and lies in relative interior. First-order optimality holds separately on every $`T_B`$. Equation (22) multiplies each block's gradient difference by the constant $`a_B`$, so the $`F`$-gradient difference also annihilates each nonsingleton $`T_B`$. On a free singleton, stationarity reads $`g_i'(c_i)=g_i'(b_i)`$; positive curvature implies $`c_i=b_i`$, so the $`F`$-gradient difference vanishes there too. Equation (4) proves strict gain for both standards. No product decomposition of $`C`$ was assumed: the minimization took place on the full joint hull. $`\square`$

Only the attained coordinate intervals occur in (22); the theorem supplies no information about parts of a generator that the truth hull never visits. Nor does it classify rank-one constrained blocks.

### 4.5 One anchor can serve an arbitrary family

Under the hypotheses of Theorem 4, let $`G`$ be fixed and let $`\{F_k\}_{k\in K}`$ be any family. If every pair $`(F_k,G)`$ has universal local common repair, (22) holds separately for each $`k`$. The one $`G`$-minimizer constructed above then strictly improves every $`F_k`$ and $`G`$. Its existence scale depends on the anchor and the local geometry, not on the cardinality of $`K`$.

This conclusion uses the blockwise proportionality theorem. It is not an inference from arbitrary pairwise intersections of repair sets. An infinite family with only pointwise Hessian compatibility would need uniform remainder control for analogous approximate statements.

## 5. What local compatibility does and does not establish

### 5.1 Approximate equivalence for a finite family

At one fixed interior $`p`$, consider finitely many $`C^2`$ potentials with positive-definite Hessians. Under the localization conditions of Section 4.1, common Hessian projection is equivalent to the existence of some common $`\eta_\varepsilon=o(\varepsilon)`$ repair.

Necessity is (17). For sufficiency, let the common projected vector be $`z`$ and set $`c_\varepsilon=p+\varepsilon z`$. Every loss difference
$`\Delta_{k,j}(\varepsilon)=D_{F_k}(v_j,c_\varepsilon)-D_{F_k}(v_j,b_\varepsilon)`$
has vanishing first-order term, so $`\Delta_{k,j}=o(\varepsilon)`$. The finite sum
$`\eta_\varepsilon=\sum_{k,j}|\Delta_{k,j}(\varepsilon)|`$
is nonnegative, is $`o(\varepsilon)`$, and bounds every excess.

This is an existential tolerance statement. It does not give exact repair, does not satisfy every prescribed $`o(\varepsilon)`$ allowance, and need not yield $`o(\varepsilon^2)`$ error. Necessity works for an arbitrary family by fixing one standard at a time; this sufficiency argument uses finiteness.

### 5.2 Universal nudges versus an individual endpoint

A strict common descent direction at a forecast $`b`$ is a nonzero $`d`$ with

```math
\nabla_bD_{F_k}(v_j,b)\cdot d<0
\quad\text{for all }k,j.
\quad\text{(23)}\quad
```

Such a direction improves the losses for a sufficiently short movement. It need not carry the forecast to a coherent endpoint.

For fixed additive $`F,G`$ on a categorical simplex with $`n\geq3`$, universal local existence of a common descent direction is nevertheless rigid. Suppose at every interior $`p`$, along arbitrarily small forecasts $`p+\varepsilon e_1`$, a common descent direction exists. Normalize these directions to unit length and extract a limit $`d\ne0`$. At the coherent limit, (23) becomes
$`(p-v_j)^\top H_F(p)d\leq0`$ and its $`G`$-analogue. Their positive barycentric averages are zero. Hence

```math
H_F(p)d\in\mathrm{span}\{\mathbf1\},
\qquad
H_G(p)d\in\mathrm{span}\{\mathbf1\}.
```

The two Hessian-normal lines therefore coincide. Equations (7) and (19), followed by the three-coordinate argument, give (18). Conversely, when (18) holds, put $`s=\sum_i b_i`$ and

```math
d_i=\frac{1-s}{f_i''(b_i)}.
\quad\text{(24)}\quad
```

Every $`F`$-loss has directional derivative $`-(s-1)^2`$, and the $`G`$-derivative is a positive multiple of it. There is also a coherent-directed nudge: define

```math
r_i(b)=\frac{f_i''(b_i)^{-1}}{\sum_jf_j''(b_j)^{-1}},
\qquad
c=b-(s-1)r(b).
\quad\text{(25)}\quad
```

Near an interior coherent point, $`c`$ is in the simplex, and the derivative along $`c-b`$ is
$`-(s-1)^2/\sum_jf_j''(b_j)^{-1}<0`$.
Thus universal local nudges, universal coherent-directed nudges, and universal endpoint repair impose the same fixed-generator rigidity here. This extends neither to an arbitrary isolated forecast nor to all geometries.

For a concrete pointwise separation, use unscaled quadratic matrices
$`I`$ and $`\mathrm{diag}(1,2,2)`$, and set

```math
b=(1/2,7/20,7/20),\qquad d=(-13/10,-1,-1).
```

The three derivatives are $`(-1/10,-7/10,-7/10)`$ for $`I`$, and $`(-3/2,-1/10,-1/10)`$ for the second matrix. Moreover

```math
b+\frac2{33}d=(139/330,191/660,191/660)
```

is coherent, so the common nudge points toward a coherent target. Yet no common weak coherent endpoint exists. If $`c_0+c_1+c_2=1`$, the $`I`$-loss at truth $`e_0`$ forces
$`(1-c_0)^2\leq33/100`$.
Averaging the second loss over $`e_1,e_2`$, and minimizing over $`c_1,c_2`$ with their sum fixed, forces $`c_0^2\leq17/100`$. Their sum implies $`c_0^2+(1-c_0)^2\leq1/2`$, hence $`c_0=1/2`$, contradicting $`c_0^2\leq17/100`$.

Konek's analysis of common improvements under epistemic and practical scoring standards is an important antecedent [6]. The distinction here is between an initial derivative and a complete endpoint, together with the stated universal quantifiers; it is not a claim that common-descent analysis began with this exposition.

### 5.3 A fixed numerical obstruction for entropy and quadratic loss

The categorical theorem predicts disagreement between the Euclidean and binary-entropy generators. It can also be witnessed without relying on a limiting argument. Let

```math
p=(1/2,1/3,1/6),\quad h=e_1,\quad
b=p+\varepsilon e_1,\quad
q=p+\varepsilon(2/3,-1/3,-1/3).
```

The entropy Hessian has normalized reciprocal vector
$`(9/22,4/11,5/22)`$, unlike the Euclidean normal vector $`(1/3,1/3,1/3)`$.
The tangent ball with radius $`1/6`$ lies in the simplex. Equation (8) shows that every exact Euclidean repair has
$`\|c-q\|_2\leq2\varepsilon^2`$, hence
$`\|c-q\|_1<4\varepsilon^2`$.

At categorical truth $`e_j`$, the entropy loss is
$`-\log P_j(x)`$, where $`P_j(x)=x_j\prod_{i\ne j}(1-x_i)`$.
Each $`P_j`$ is Lipschitz with constant one for the $`\ell^1`$ norm on the cube. Direct multiplication gives

```math
P_3(b)-P_3(q)=
\frac{5\varepsilon}{108}-\frac{\varepsilon^2}{18}
-\frac{2\varepsilon^3}{27}.
\quad\text{(26)}\quad
```

At $`\varepsilon=1/1000`$, subtracting $`4\varepsilon^2`$ leaves
$`63361/1500000000>0`$.
Consequently $`P_3(c)<P_3(b)`$ for every Euclidean repair $`c`$: the entropy loss at that truth is worse. Boundary candidates with zero $`P_3`$ cannot rescue the comparison. This is an exact finite obstruction, not a rounded numerical search.

### 5.4 Why the standards must remain fixed across contexts

The order of quantifiers in Theorem 3 cannot be changed. On the three-outcome simplex let $`F(x)=\tfrac12\sum_i x_i^2`$. For each coherent interior point $`p`$, define a different generator

```math
G_p(x)=\sum_i\left(\frac{(x_i-p_i)^2}{2}+(x_i-p_i)^4\right).
\quad\text{(27)}\quad
```

Its Hessian at its chosen $`p`$ is $`I`$. For $`b=p+\varepsilon e_1`$, the Euclidean correction $`q=p+\varepsilon(2/3,-1/3,-1/3)`$ has $`F`$-gain $`\varepsilon^2/6`$. Direct Bregman expansion gives

```math
D_{G_p}(v,b)-D_{G_p}(v,q)
=\frac{\varepsilon^2}{6}
 +\frac{7\varepsilon^4}{3}
 -\frac{8\varepsilon^3}{3}(v_1-p_1)>0
\quad\text{(28)}\quad
```

for $`0<\varepsilon<1/16`$, after also restricting to the local feasible scale. Nevertheless $`G_p`$ is not an affine rescaling of $`F`$, as its fourth coordinate derivative is $`24`$. The construction establishes a generator chosen separately for each context. It does not furnish one fixed nonquadratic generator satisfying the universal categorical theorem.

### 5.5 Faithful changes of representation

A change of coordinates must preserve the actual loss comparisons, not merely the appearance of a potential. For a differentiable map $`L`$,

```math
D_{F\circ L}(x,y)
=D_F(Lx,Ly)
 +dF_{Ly}\bigl(Lx-Ly-dL_y(x-y)\bigr).
\quad\text{(29)}\quad
```

Calling the left side a Bregman divergence additionally requires convexity of $`F\circ L`$. Affine $`L`$ makes the remainder vanish. Nonlinear injectivity does not. With $`L(x)=x^2`$ on the positive line and $`F(z)=z^2/2`$, the remainder is $`y^2(x-y)^2`$; at $`x=2,y=1`$, the pulled-back loss is $`9/2`$, while the divergence of the composite potential is $`11/2`$.

Any transport of a repair theorem must therefore specify the truth set, feasible forecasts, disturbances, and the whole transformed loss. Additive separability need not survive a general coordinate change. Curved representational divergences provide a broader setting for this distinction [8]; equation (29) is the exact elementary identity needed here.

## 6. Rank-one blocks and comparison of means

### 6.1 Normalizing an isolated segment

Consider an isolated one-dimensional coherent segment. An affine coordinate change sends its endpoints to $`(0,\ldots,0)`$ and $`(1,\ldots,1)`$; if an original coordinate has negative orientation, reflect it. A transformed scalar potential has curvature $`u_i^2f_i''(a_i+u_it)>0`$. The Bregman comparisons are unchanged by this affine pullback.

Thus a forecast is $`t=(t_1,\ldots,t_d)\in(0,1)^d`$, $`d\geq2`$, and a coherent repair has all coordinates equal to $`q`$. For each standard $`k`$, let the coordinate potentials $`\psi_{ki}`$ be finite and continuous on $`[0,1]`$, $`C^3`$ on $`(0,1)`$, and have positive curvature there. Define

```math
A_{ki}(t)=D_{\psi_{ki}}(0,t),\qquad
B_{ki}(t)=D_{\psi_{ki}}(1,t).
```

Then
$`A_{ki}'(t)=t\psi_{ki}''(t)>0`$ and
$`B_{ki}'(t)=-(1-t)\psi_{ki}''(t)<0`$.
The all-truth repair interval for standard $`k`$ is

```math
L_k(t)\leq q\leq U_k(t),
\quad\text{(30)}\quad
```

where

```math
U_k(t)=\left(\sum_iA_{ki}\right)^{-1}
             \left(\sum_iA_{ki}(t_i)\right),
\qquad
L_k(t)=\left(\sum_i(-B_{ki})\right)^{-1}
             \left(\sum_i(-B_{ki}(t_i))\right).
\quad\text{(31)}\quad
```

Both are between $`\min_i t_i`$ and $`\max_i t_i`$. Intermediate truth points add no constraint, since score differences are affine in truth.

### 6.2 The comparison lemma

For strictly increasing $`C^2`$ functions $`a_i,b_i`$ with positive derivatives, define
$`M_a(t)=(\sum_i a_i)^{-1}(\sum_i a_i(t_i))`$, and similarly $`M_b`$.
Then

```math
M_a(t)\leq M_b(t)\quad\text{for every }t
\quad\text{(32)}\quad
```

holds exactly when all ratios $`b_i'(s)/a_i'(s)`$ equal one function $`\rho(s)`$, and $`\rho`$ is nondecreasing.

Here is a direct proof. At a diagonal tuple $`(s,\ldots,s)`$, the difference of the means is zero and has a minimum. Equality of first derivatives gives
$`b_i'/\sum_jb_j'=a_i'/\sum_ja_j'`$, hence the common ratio. For a nonzero direction $`w`$ with $`\sum_i a_i'(s)w_i=0`$, the second derivative of $`M_b-M_a`$ is

```math
\frac{\rho'(s)}{\rho(s)\sum_i a_i'(s)}
\sum_i a_i'(s)w_i^2.
```

It must be nonnegative; such a nonzero direction exists because $`d\geq2`$, so $`\rho'\geq0`$.

For sufficiency, for any $`u,t_i`$ monotonicity gives

```math
b_i(t_i)-b_i(u)
 -\rho(u)\bigl(a_i(t_i)-a_i(u)\bigr)
=\int_u^{t_i}(\rho(s)-\rho(u))a_i'(s)\,ds\geq0.
```

Choose $`u=M_a(t)`$ and sum. The $`a_i`$-terms cancel, so $`\sum_i b_i(t_i)\geq\sum_i b_i(u)`$, which proves (32).

The two-coordinate differential comparison is classical: Páles's signed Remark 5 gives the corresponding criterion [4]. Matkowski's later general-coordinate formulation places these comparisons in a convexity framework [5]. The present use is a scoring-rule application with its hypotheses and normalization made explicit.

### 6.3 Exact rank-one compatibility

Universal local repair first forces the curvature profiles to factor as

```math
\psi_{ki}''(s)=r_k(s)w_i(s),
\qquad r_k(s),w_i(s)>0,
\quad\text{(33)}\quad
```

where the coordinate functions $`w_i`$ are shared across standards. This is the rank-one Hessian-projection condition. Given (33), compare a lower mean $`L_\ell`$ with an upper mean $`U_k`$. The derivative ratio in the comparison lemma is

```math
\rho_{k\ell}(s)=
\frac{s\,r_k(s)}{(1-s)r_\ell(s)}.
\quad\text{(34)}\quad
```

**Theorem 5 — Isolated rank-one criterion.** Under (33), a common weak repair exists for every forecast tuple if and only if, for every pair $`k,\ell`$,

```math
\left|\frac{d}{ds}\log\frac{r_k(s)}{r_\ell(s)}\right|
\leq\frac1{s(1-s)}\qquad(0<s<1).
\quad\text{(35)}\quad
```

Universal local weak repair along every small transverse direction at every diagonal context is already sufficient to force (33) and (35).

**Proof.** A common interval exists exactly when $`L_\ell(t)\leq U_k(t)`$ for every ordered pair. The lemma makes this equivalent to nondecrease of (34). Applying it in both orders gives (35). Conversely these comparisons make
$`\sup_k L_k(t)\leq\inf_kU_k(t)`$;
both sides lie in the compact interval between the smallest and largest forecast coordinates. Thus even an arbitrary family has a common weak repair.

For the local necessity, a negative first derivative of $`U_k-L_\ell`$ at a diagonal point would rule out repair for every sufficiently small step in the corresponding direction. Applying the same argument to the opposite direction forces the first derivative to vanish and yields (33). A negative second derivative in a nonzero weighted-mean-zero direction would likewise rule out arbitrarily small repair; the second derivative in the comparison lemma then yields (35). These directions are transverse to the diagonal. $`\square`$

No uniform strict margin over an arbitrary family follows from this weak-interval theorem. Also, the theorem concerns an isolated segment; projecting one block out of a coupled truth hull need not preserve its repair problem.

### 6.4 Why pairwise comparison with an anchor can fail here

Take common coordinate weights $`w_i=1`$ and three curvature factors

```math
r_0(s)=1,\qquad
r_+(s)=\frac{s}{1-s},\qquad
r_-(s)=\frac{1-s}{s}.
\quad\text{(36)}\quad
```

Each of $`r_+`$ and $`r_-`$ satisfies (35) with the anchor $`r_0`$, at the boundary of the bound. Their mutual logarithmic derivative has magnitude $`2/[s(1-s)]`$, so they fail it with each other.

There is a direct witness. For $`r_+`$, the lower mean is the root mean square of the coordinates. For $`r_-`$, the upper mean is one minus the root mean square of their complements. At the tuple $`(1/4,3/4)`$, these are
$`\sqrt5/4`$ and $`1-\sqrt5/4`$, respectively. The first exceeds the second. Each standard may have a repair in common with the anchor, while the whole family has none.

The potentials obtained by integrating (36) twice are finite at the endpoints and smooth in the open interval. Their endpoint-singular curvatures must not be used as examples satisfying a theorem that requires a $`C^3`$ potential on an open neighborhood of the whole closed truth hull.

## 7. How much error is unavoidable?

### 7.1 First-order minimax loss for quadratic standards

For finitely many fixed quadratic matrices $`W_k`$, define the signed optimal excess

```math
R(\varepsilon)=
\min_{c\in C}\max_{k,j}
\bigl(L_{W_k}(c,v_j)-L_{W_k}(p+\varepsilon h,v_j)\bigr).
\quad\text{(37)}\quad
```

The smallest nonnegative permissible error is $`\max\{0,R(\varepsilon)\}`$. A negative value of $`R`$ records strict simultaneous improvement and must not be truncated when studying the asymptotics.

**Theorem 6 — First-order incompatibility cost.** The finite linear program

```math
\kappa(h)=
\min_{z\in T}\max_{k,j}
2(p-v_j)^\top W_k(z-h)
\quad\text{(38)}\quad
```

attains a nonnegative value, and

```math
R(\varepsilon)=\varepsilon\kappa(h)+O(\varepsilon^2).
\quad\text{(39)}\quad
```

Moreover, $`\kappa(h)=0`$ if and only if all $`P_{W_k}h`$ agree.

**Proof.** The barycentric average of each standard's linear terms in (38) is zero, so the maximum is nonnegative. A tangent ball in $`C`$ gives, for one anchor matrix,
$`\max_j2(p-v_j)^\top W_0 z\geq2r\,m_{W_0}\|z\|_2`$.
Subtracting the bounded $`h`$-terms proves coercivity and attainment of (38).

Writing $`u=c-p`$, the exact loss excess is

```math
2(p-v_j)^\top W_k(u-\varepsilon h)
 +\|u\|_{W_k}^2-\varepsilon^2\|h\|_{W_k}^2.
\quad\text{(40)}\quad
```

The feasible choice $`c=p`$ gives $`R(\varepsilon)=O(\varepsilon)`$ from above. The same anchor coercivity in (40), with the nonnegative quadratic term retained, forces actual minimizers to have $`u=O(\varepsilon)`$. On this bounded rescaling, (40) is its first-order expression plus a uniform $`O(\varepsilon^2)`$ remainder. Conversely, a minimizing $`z`$ in (38) gives the feasible candidate $`p+\varepsilon z`$ for small $`\varepsilon`$. These two comparisons prove (39).

If $`\kappa=0`$, every displayed linear term at a minimizer is nonpositive. Its positive barycentric average is zero, so every term vanishes, giving $`z=P_{W_k}h`$ for all $`k`$. The converse follows by the same orthogonality. $`\square`$

Thus incompatibility forces $`R(\varepsilon)\geq\kappa\varepsilon/2>0`$ eventually. Compatibility gives the stronger exact bound
$`R(\varepsilon)\leq-\varepsilon^2\min_k\|Q_{W_k}h\|_{W_k}^2<0`$.
Adding a tangent vector to $`h`$ does not change $`\kappa`$. Independent positive rescalings of the losses change its numerical value, although they do not change whether it is zero. General minimax sensitivity theory supplies a wider antecedent; Meitz and Shapiro's Proposition 2.3 is a relevant convex minimax result [7]. The proof here establishes the finite geometric case directly.

For the binary family $`W_\alpha`$, $`\alpha\in[l,u]\subset[0,1]`$, one can compute the whole minimax value. Set $`m=(l+u)/2`$ and now let $`d=(u-l)/2`$ be the **half-width**. For $`0<\varepsilon\leq1/4`$,

```math
t_*=\frac12+m\varepsilon-d\varepsilon^2,
\qquad
R(\varepsilon)=d\varepsilon-m(1-m)\varepsilon^2
 -2md\varepsilon^3+d^2\varepsilon^4.
\quad\text{(41)}\quad
```

Indeed, the worst excess is the maximum of the increasing function
$`t^2-1/4-l\varepsilon(1+\varepsilon)`$
and the decreasing function
$`(1-t)^2-1/4+u\varepsilon(1-\varepsilon)`$.
Their intersection lies in $`[0,1]`$ and gives (41). The formula extends algebraically to degenerate endpoint weights, although those endpoints fall outside the positive-definite hypotheses of Theorems 1 and 6.

### 7.2 Second-order control after first-order compatibility

Let $`F_1,\ldots,F_N`$ be $`C^3`$ on an open convex neighborhood of the entire compact hull $`C`$, with positive-definite Hessians there. Additive separability is not required. Fix a transverse $`h`$, and suppose there is one $`z\in T`$ with

```math
H_k(h-z)\perp T\quad\text{for every }k,
\qquad H_k=\nabla^2F_k(p),\quad K_k=\nabla^3F_k(p).
\quad\text{(42)}\quad
```

Define

```math
\begin{aligned}
E_k&=\frac12\bigl(H_k[h,h]-H_k[z,z]\bigr)
    =\frac12H_k[h-z,h-z]>0,\\
B_{kj}&=E_k+
\frac12\bigl(K_k[p-v_j,h,h]-K_k[p-v_j,z,z]\bigr),\\
A_{kj}(w)&=B_{kj}-H_k[p-v_j,w],\qquad w\in T,\\
\tau_*&=\max_{w\in T}\min_{k,j}A_{kj}(w).
\end{aligned}
\quad\text{(43)}\quad
```

**Theorem 7 — Optimized second-order repair.** The program (43) has a finite attained value. For the actual signed excess

```math
R(\varepsilon)=
\min_{c\in C}\max_{k,j}
\bigl(D_{F_k}(v_j,c)-D_{F_k}(v_j,p+\varepsilon h)\bigr),
```

one has

```math
R(\varepsilon)=-\tau_*\varepsilon^2+o(\varepsilon^2).
\quad\text{(44)}\quad
```

If $`\tau_*>0`$, strict common repair exists for every sufficiently small positive $`\varepsilon`$. If $`\tau_*<0`$, no common weak repair exists there, and no $`o(\varepsilon^2)`$ tolerance can suffice. The case $`\tau_*=0`$ is undecided by (44).

**Proof.** For one anchor standard, the tangent-ball argument gives
$`\max_j H_0[p-v_j,w]\geq c_0\|w\|_2`$, $`c_0>0`$.
Thus $`\min_{k,j}A_{kj}(w)\leq\max_j B_{0j}-c_0\|w\|_2`$, proving attainment and finiteness from above. A barycentric average of $`A_{kj}(w)`$ is $`E_k`$, which is another useful upper bound.

Compactness of $`C`$ gives actual minimizers. The feasible trial $`p+\varepsilon z`$ has excess $`O(\varepsilon^2)`$. Averaging under one standard gives the lower bound $`R(\varepsilon)\geq-D_{F_0}(p,b_\varepsilon)=-O(\varepsilon^2)`$, so $`R=O(\varepsilon^2)`$. Equation (3), together with positive curvature on the compact hull, forces every optimizing $`c_\varepsilon`$ to satisfy $`c_\varepsilon-p=O(\varepsilon)`$.

Set $`x_\varepsilon=c_\varepsilon-p-\varepsilon z\in T`$. Taylor expansion using (42) makes each anchor excess
$`H_0[p-v_j,x_\varepsilon]+O(\varepsilon^2)`$.
Its maximum is $`O(\varepsilon^2)`$, so the same coercivity yields $`x_\varepsilon=O(\varepsilon^2)`$. Actual minimizers therefore have the bounded form

```math
c_\varepsilon=p+\varepsilon z+\varepsilon^2w_\varepsilon,
\qquad w_\varepsilon=O(1).
\quad\text{(45)}\quad
```

Equation (5) now gives, uniformly for bounded $`w`$,

```math
D_{F_k}(v_j,b_\varepsilon)-
D_{F_k}(v_j,p+\varepsilon z+\varepsilon^2w)
=\varepsilon^2A_{kj}(w)+o(\varepsilon^2).
\quad\text{(46)}\quad
```

Using (45) bounds the optimum on one side. Using a maximizing $`w_*`$ from (43), whose corresponding candidate remains in $`C`$ by relative interior, bounds it on the other. This proves (44). The same localization argument applies to any exact-repair sequence, not just optimizers. $`\square`$

The open-neighborhood hypothesis matters. A potential whose Hessian blows up at truth endpoints does not meet this theorem merely because it is smooth at $`p`$.

### 7.3 Finite certificates

Finite-dimensional linear-programming duality gives

```math
\tau_*=
\min_{\lambda}
\sum_{k,j}\lambda_{kj}B_{kj},
\quad\text{(47)}\quad
```

subject to

```math
\lambda_{kj}\geq0,\quad
\sum_{k,j}\lambda_{kj}=1,\quad
\sum_{k,j}\lambda_{kj}H_k[p-v_j,w]=0
\quad\text{for all }w\in T.
\quad\text{(48)}\quad
```

The dual is feasible: put the positive barycentric weights on any one standard. For every feasible $`\lambda`$, averaging cancels the $`w`$-terms, so $`\min_{k,j}A_{kj}(w)\leq\sum\lambda_{kj}B_{kj}`$. The reverse equality follows from the separating-hyperplane theorem for the finite system $`A_{kj}(w)\geq\tau`$; coercivity established above prevents escape of a maximizing sequence.

A positive primal margin and a negative dual value are directly checkable certificates for opposite conclusions. With rational tensors and truth data, these are rational linear programs. This does not make arbitrary smooth generators effectively decidable from unspecified analytic descriptions. Independent positive rescaling preserves the sign classifications, but not a numerical common regret measured in fixed units.

## 8. A zero second-order margin does not decide exact repair

Use the diagonal binary segment, the quadratic potential $`G(x,y)=(x^2+y^2)/2`$, and $`F(x,y)=\psi(x)+\psi(y)`$, where

```math
\psi(t)=\frac{z^2}{2}+\frac23z^3+z^4,\qquad z=t-\frac12.
\quad\text{(49)}\quad
```

Its curvature
$`r(t)=1+4z+12z^2=12(z+1/6)^2+2/3`$
is positive on the whole real line. Thus this is a globally regular polynomial example, not an endpoint singularity.

At $`p=(1/2,1/2)`$, $`h=(1,0)`$, the common first-order correction is $`z_h=(1/2,1/2)`$. Write a tangent second-order correction as $`(w,w)`$. The four coefficients in (43), ordered by standard and endpoint truth, are

```math
A_{G,0}=\frac14-w,\quad A_{G,1}=\frac14+w,\quad
A_{F,0}=\frac34-w,\quad A_{F,1}=-\frac14+w.
\quad\text{(50)}\quad
```

Their minimum is maximized at $`w=1/4`$, with $`\tau_*=0`$.

Nevertheless no exact common weak repair exists for $`0<\varepsilon\leq1/100`$. Let

```math
A=\frac{(1/2+\varepsilon)^2+(1/2)^2}{2},
\qquad
u=\frac12+\frac{\varepsilon}{2}
 +\frac{\varepsilon^2}{4}-\frac{\varepsilon^3}{8}.
```

The quadratic comparison at truth zero forces $`q^2\leq A`$. But

```math
u^2-A=
\frac{\varepsilon^3}{64}
\bigl(\varepsilon^3-4\varepsilon^2-4\varepsilon+8\bigr)>0,
```

so $`q<u`$. Define $`L(q)=2D_\psi(1,q)`$. It is strictly decreasing on $`[0,1]`$, because $`L'(q)=-2(1-q)r(q)<0`$ in the interior. Exact expansion gives

```math
L(u)-D_\psi(1,1/2+\varepsilon)-D_\psi(1,1/2)
=\frac{\varepsilon^3}{6144}P(\varepsilon),
\quad\text{(51)}\quad
```

where

```math
\begin{aligned}
P(\varepsilon)={}&2304-17280\varepsilon+4992\varepsilon^2
 +1696\varepsilon^3-2304\varepsilon^4-816\varepsilon^5\\
&+592\varepsilon^6+72\varepsilon^7
 -72\varepsilon^8+9\varepsilon^9.
\end{aligned}
```

For $`0<\varepsilon\leq1/100`$, discard positive terms and bound the four negative terms by their endpoint magnitudes:

```math
P(\varepsilon)\geq
2304-\frac{17280}{100}-\frac{2304}{100^4}
-\frac{816}{100^5}-\frac{72}{100^8}>0.
```

Thus $`L(q)>L(u)`$ already exceeds the disturbed nonlinear loss, a contradiction. The first positive term of this witness is $`3\varepsilon^3/8`$.

For comparison, the globally regular potential

```math
\psi_+(t)=\frac1{16}e^{4(t-1/2)}
\quad\text{(52)}\quad
```

has the same curvature and curvature derivative at $`1/2`$, and hence the same four second-order coefficients (50). Its log-curvature derivative is $`4`$, which satisfies
$`4\leq1/[s(1-s)]`$ on $`(0,1)`$. Theorem 5 gives exact common repair with the quadratic score. For a nonconstant forecast tuple the relevant mean comparisons are strict: the derivative ratio in each ordered comparison is strictly increasing, with at most an isolated zero derivative. Hence a point in the interior of the common interval strictly repairs both standards.

The polynomial and exponential cases have the same first-order projections and the same zero second-order margin at this context, yet opposite exact conclusions. The missing information is not supplied by declaring a zero linear-program value a pass.

## 9. Joint truth structure can restore repair

### 9.1 A polynomial score that fails on an isolated block

For the rest of this section set

```math
\psi(t)=\frac{t^2}{2}+4t^4,\qquad
r(s)=\psi''(s)=1+48s^2.
\quad\text{(53)}\quad
```

Against the unit quadratic score, the isolated diagonal block violates (35) at $`s=1/4`$:

```math
\frac{r'(1/4)}{r(1/4)}=6
>\frac1{(1/4)(3/4)}=\frac{16}{3}.
\quad\text{(54)}\quad
```

There is also an explicit interval of impossibility. Disturb the isolated block to $`(1/4+\varepsilon,1/4)`$, and put

```math
A_\varepsilon=\frac{(1/4+\varepsilon)^2+(1/4)^2}{2},
\qquad
u_\varepsilon=\frac14+\frac{\varepsilon}{2}
 +\frac{13\varepsilon^2}{24}.
```

For $`0<\varepsilon\leq1/100`$, $`0<u_\varepsilon<1`$, and

```math
u_\varepsilon^2-A_\varepsilon
=\frac{\varepsilon^2}{576}
 (169\varepsilon^2+312\varepsilon+12)>0.
\quad\text{(55)}\quad
```

Let $`L(q)=2D_\psi(1,q)`$ and
$`N_\varepsilon=D_\psi(1,1/4+\varepsilon)+D_\psi(1,1/4)`$.
Then

```math
L(u_\varepsilon)-N_\varepsilon
=\frac{\varepsilon^2}{13824}Q(\varepsilon),
\quad\text{(56)}\quad
```

with

```math
Q(\varepsilon)=3456-63360\varepsilon-246864\varepsilon^2
 +41184\varepsilon^3+128440\varepsilon^4
 +105456\varepsilon^5+28561\varepsilon^6.
```

Its value is positive on this interval, since
$`3456-63360/100-246864/10000>0`$.
The quadratic zero-truth constraint $`q^2\leq A_\varepsilon`$ forces $`q<u_\varepsilon`$; strict decrease of $`L`$ then contradicts $`L(q)\leq N_\varepsilon`$. Only these two actual truth comparisons are needed.

### 9.2 A coupled conjunction hull

Now keep the same first two coordinate potentials, but couple their truth values to two further propositions. Let $`C_{\wedge}`$ be the convex hull of

```math
(0,0,0,0),\quad(0,0,1,0),\quad
(0,0,0,1),\quad(1,1,1,1).
\quad\text{(57)}\quad
```

The first two coordinates both record the conjunction of the last two truth values. A relative-interior context has the form $`p=(s,s,z,w)`$, with the four positive barycentric weights

```math
1+s-z-w,\quad z-s,\quad w-s,\quad s.
\quad\text{(58)}\quad
```

We use duplicate first coordinates throughout this construction. In the equivalent complementary convention $`(x,y)`$, the affine transformation is $`(t_1,t_2)=(x,1-y)`$; the second transformed disturbance component is the negative of the original $`y`$-direction. Equation (29) has zero remainder for this affine transformation. The directions in the formulas below are the duplicate-coordinate directions.

Use

```math
G(x)=\frac12\sum_{i=1}^4x_i^2,\qquad
F(x)=\psi(x_1)+\psi(x_2)+50x_3^2+50x_4^2.
\quad\text{(59)}\quad
```

Write a disturbance direction as $`h=(h_1,h_2,h_z,h_w)`$ and define

```math
\mu=\frac{h_1+h_2}{2},\quad
e=\frac{(h_1-h_2)^2}{4},\quad
T_0=z+w,\quad A=T_0-2s.
```

Transversality is $`e>0`$. From (58),
$`0<s<1`$, $`0<A<1-s`$, and $`2s<T_0<1+s`$.
Set

```math
\begin{aligned}
\gamma&=\frac{96es^2}{T_0(100-r)},&
\beta&=\frac{48es-100\gamma}{r},\\
\theta&=\frac{9600s^2(T_0-2s)}
 {rT_0(100-r)},&
m_0&=1-\theta,\qquad r=1+48s^2.
\end{aligned}
\quad\text{(60)}\quad
```

The proposed repair is

```math
c_\varepsilon=
\bigl(q,q,z+\varepsilon h_z+\varepsilon^2\gamma,
             w+\varepsilon h_w+\varepsilon^2\gamma\bigr),
\quad
q=s+\varepsilon\mu+\varepsilon^2\beta.
\quad\text{(61)}\quad
```

We will prove $`m_0>0`$, membership in the actual hull, and strict gain under both scores. The whole truth relation (57), not merely its affine equality $`x_1=x_2`$, participates in the proof.

### 9.3 A finite positivity certificate

Define

```math
\begin{aligned}
\Pi(s)&=(1+s)r(s)(100-r(s))-9600s^2(1-s)\\
&=-2304s^5-2304s^4+14304s^3-4896s^2+99s+99.
\end{aligned}
\quad\text{(62)}\quad
```

The following exact Bernstein coefficients prove
$`\Pi(s)\geq132/5`$ on $`[0,1]`$.
On the interval $`j/8\leq s\leq(j+1)/8`$, put $`t=8s-j`$ and use the row in
$`\Pi(s)=\sum_{k=0}^5\binom5k b_k t^k(1-t)^{5-k}`$.

| $`j`$ | $`b_0`$ | $`b_1`$ | $`b_2`$ | $`b_3`$ | $`b_4`$ | $`b_5`$ |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 99 | 4059/40 | 963/10 | 13803/160 | 1185/16 | 7959/128 |
| 1 | 7959/128 | 3219/64 | 3099/80 | 30 | 132/5 | 30 |
| 2 | 30 | 168/5 | 222/5 | 5157/80 | 30591/320 | 17829/128 |
| 3 | 17829/128 | 29277/160 | 38277/160 | 12381/40 | 15801/40 | 993/2 |
| 4 | 993/2 | 23919/40 | 28617/40 | 135939/160 | 160149/160 | 149667/128 |
| 5 | 149667/128 | 428037/320 | 121839/80 | 17253/10 | 1944 | 2178 |
| 6 | 2178 | 2412 | 26613/10 | 46797/16 | 1024293/320 | 446385/128 |
| 7 | 446385/128 | 75477/20 | 651309/160 | 87513/20 | 187437/40 | 4998 |

Each row identity is verified by polynomial expansion. Every coefficient is at least $`132/5`$, and the Bernstein basis is nonnegative and sums to one. This supplies the advertised lower bound without a plot or numerical sampling.

To deduce $`m_0>0`$, the denominator $`rT_0(100-r)`$ is positive: $`1\leq r<49<100`$. Let $`D=r(100-r)-9600s^2`$. The difference between that denominator and the numerator of $`\theta`$ is
$`T_0D+19200s^3`$.
If $`D\geq0`$, it is positive. If $`D<0`$, write it as
$`\Pi(s)+(T_0-1-s)D`$; both terms are positive. Thus $`\theta<1`$.

### 9.4 Actual gain, feasibility and a usable scale

For a truth in (57), let $`a`$ be its repeated first coordinate and $`j`$ the sum of its last two coordinates. The only possibilities are $`(a,j)=(0,0),(0,1),(1,2)`$. Exact polynomial expansion of the actual Bregman losses gives the following coefficients of $`\varepsilon^2`$ in the gain from (61):

| Truth class $`(a,j)`$ | Quadratic gain coefficient | Nonlinear gain coefficient |
|---|---|---|
| $`(0,0)`$ | $`em_0`$ | $`rem_0`$ |
| $`(0,1)`$ | $`em_0+\gamma`$ | $`rem_0+100\gamma`$ |
| $`(1,2)`$ | $`em_0+\dfrac{96es(T_0-2s)}{rT_0}`$ | $`rem_0`$ |

For clarity, before substituting (60), these coefficients are

```math
\begin{aligned}
\Gamma_G(a,j)
 &=e-2(s-a)\beta+(j-T_0)\gamma,\\
\Gamma_F(a,j)
 &=re+(s-a)(96se-2r\beta)+100(j-T_0)\gamma.
\end{aligned}
\quad\text{(63)}\quad
```

Substitution and elementary cancellation give the table. All coefficients are strictly positive.
These are coefficients of real score differences: the identity

```math
D_\psi(v,t)=\frac{(v-t)^2}{2}+4v^4+12t^4-16vt^3
\quad\text{(64)}\quad
```

shows that every gain is exactly $`\varepsilon^2\Gamma+\varepsilon^3R(\varepsilon)`$, with a polynomial remainder. No assumed remainder sign is needed.

Membership is equally concrete. Substitute (61) into the four affine expressions (58). Each resulting weight is its strictly positive original value plus a linear and a quadratic term in $`\varepsilon`$; their sum remains one, and their convex combination of the four actual truths is $`c_\varepsilon`$. They remain positive for sufficiently small $`\varepsilon`$.

An explicit local scale can be extracted from the same formulas. Let $`M`$ be the sum of the absolute coefficients of all finitely many remainder polynomials, so $`|R(\varepsilon)|\leq M`$ for $`0\leq\varepsilon\leq1`$. Let $`b_0`$ be the smallest original weight in (58), and $`L`$ the sum of the absolute linear and quadratic coefficients in their changes. Let $`p_0=\min_i\{p_i,1-p_i\}>0`$, and $`H=1+\sum_i|h_i|`$. It suffices to take

```math
0<\varepsilon<
\min\left\{1,\frac{em_0}{2(M+1)},
\frac{b_0}{2(L+1)},\frac{p_0}{2H}\right\}.
\quad\text{(65)}\quad
```

The gains are then at least $`em_0\varepsilon^2/2`$, the barycentric weights stay positive, and the disturbed forecast stays in the open cube. Thus the coupled hull admits strict common repair at every interior context and every transverse direction, although the isolated repeated block fails (54).

### 9.5 Removing the free-coordinate explanation

The preceding four-coordinate example has free singleton directions in its tangent space. The phenomenon persists when every coordinate belongs to a constrained block.

Let $`C_{\mathrm c}\subset\mathbb R^6`$ be the convex hull of the six truth vectors

```math
\begin{aligned}
v_0&=(1,1,1,1,0,0),&
v_1&=(0,0,1,0,1,0),&
v_2&=(0,0,1,0,0,1),\\
v_3&=(0,0,0,1,1,0),&
v_4&=(0,0,0,1,0,1),&
v_5&=(0,0,0,0,1,1).
\end{aligned}
\quad\text{(66)}\quad
```

Its affine hull is $`x_1=x_2`$, $`\sum_{i=3}^6x_i=2`$, with tangent

```math
T=\{d:d_1=d_2,\ d_3+d_4+d_5+d_6=0\}.
\quad\text{(67)}\quad
```

For an explicit spanning verification, any $`d\in T`$ has coefficients

```math
\bigl(d_1,\ 0,\ d_3-d_1,\
d_5-d_1+d_3+d_4,\
-d_5-d_3,\
d_1-d_3-d_4\bigr)
\quad\text{(68)}\quad
```

whose sum is zero and whose combination of (66) is $`d`$. The two dependency blocks are $`\{1,2\}`$, of tangent rank one, and $`\{3,4,5,6\}`$, of tangent rank three. The duplicate-pair vector and the high-coordinate differences generate their elementary supports. No coordinate axis belongs to $`T`$.

Use

```math
G(x)=\frac12\sum_{i=1}^6x_i^2,\qquad
F(x)=\psi(x_1)+\psi(x_2)+50\sum_{i=3}^6x_i^2.
\quad\text{(69)}\quad
```

For $`p=(s,s,z,w,u,v)\in\mathrm{ri}C_{\mathrm c}`$, positive weights on (66) give
$`s>0`$, $`z>s`$, $`w>s`$, $`z+w<1+s`$, and all coordinates in $`(0,1)`$. Put

```math
\mu=\frac{h_1+h_2}{2},\quad
e=\frac{(h_1-h_2)^2}{4},\quad
k=\frac{h_3+h_4+h_5+h_6}{4},\quad E_H=2k^2.
```

The common Hessian projection is

```math
z_h=(\mu,\mu,h_3-k,h_4-k,h_5-k,h_6-k).
\quad\text{(70)}\quad
```

Indeed, its residual has opposite first-pair entries and equal high entries; both the Euclidean Hessian and $`\mathrm{diag}(r,r,100,100,100,100)`$ make it normal to (67).

Use $`\beta,\gamma`$ from (60), with $`T_0=z+w`$, and take

```math
c_\varepsilon=p+\varepsilon z_h+
\varepsilon^2(\beta,\beta,\gamma/2,\gamma/2,-\gamma/2,-\gamma/2).
\quad\text{(71)}\quad
```

Its actual gains have coefficients $`\Gamma_G(a,j)+E_H`$ and $`\Gamma_F(a,j)+100E_H`$, where $`\Gamma`$ is (63) and $`(a,j)`$ again runs through the three classes. If $`e>0`$, the previous positive table applies. If $`e=0`$, then $`\beta=\gamma=0`$; transversality means $`k\ne0`$, and the gains are exactly $`2k^2\varepsilon^2`$ and $`200k^2\varepsilon^2`$. Thus purely high-block disturbances are included, even with an arbitrary tangent component.

To prove actual hull membership, choose the strictly positive barycentric weights $`\alpha_i`$ of $`p`$ supplied by (1). Apply (68) to $`d=c_\varepsilon-p`$, which lies in $`T`$. Adding those coefficients to $`\alpha_i`$ preserves their sum, reconstructs $`c_\varepsilon`$, and keeps every weight positive for small $`\varepsilon`$. Polynomial remainders and a finite positive leading margin then prove:

**Theorem 8 — Mixed-rank coupled repair.** For every $`p\in\mathrm{ri}C_{\mathrm c}`$ and every $`h\notin T`$, (71) is a strict common repair under (69) for every sufficiently small positive $`\varepsilon`$, with the disturbed forecast still in the open cube.

The theorem does not contradict Theorem 4: there is a constrained rank-one block. It does show that repair on that block cannot in general be decided after discarding its joint truth relations with a higher-rank block.

### 9.6 The product hull has the opposite answer

Let $`C_{\mathrm p}`$ instead be the product of the duplicate segment and the hypersimplex
$`\Delta(2,4)=\{y\in[0,1]^4:\sum_i y_i=2\}`$.
Its twelve truths independently choose $`(a,a)`$, $`a\in\{0,1\}`$, and any high vector with exactly two ones. Keep the complete ambient score functions (69).

At

```math
p=(1/4,1/4,1/2,1/2,1/2,1/2),
\qquad h=(1,0,0,0,0,0),
\quad\text{(72)}\quad
```

no common weak repair exists for $`0<\varepsilon\leq1/100`$. To see this using actual product truths, take the two high truth vectors $`y^+=(1,1,0,0)`$ and $`y^-=(0,0,1,1)`$. Their average is the high block of $`p`$.

For any proposed repair $`(q,q,z,w,u,v)`$, define
$`S=(z-1/2)^2+(w-1/2)^2+(u-1/2)^2+(v-1/2)^2\geq0`$.
Average the two quadratic comparisons at truths $`(0,0,y^\pm)`$. They force

```math
q^2-A_\varepsilon+\frac S2\leq0.
```

Average the two nonlinear comparisons at $`(1,1,y^\pm)`$. They force

```math
L(q)-N_\varepsilon+50S\leq0.
```

Hence $`q^2\leq A_\varepsilon`$ and $`L(q)\leq N_\varepsilon`$, contradicting (55)–(56). This averaging is essential: the interior high-block point $`(1/2,1/2,1/2,1/2)`$ is not itself one of the listed Boolean truths. Four genuine product-state inequalities, not a fictitious extra truth, establish impossibility.

Both hulls have the same affine hull, tangent, dependency blocks and block projections. Their shared context (72) is in each relative interior. For $`C_{\mathrm c}`$, positive weights are
$`(1/4,1/8,1/8,1/8,1/8,1/4)`$.
For $`C_{\mathrm p}`$, give each of the six zero-flag truths weight $`1/8`$ and each of the six one-flag truths weight $`1/24`$.
The whole ambient score maps agree, so every derivative at $`p`$ agrees too. What differs is the admissible joint list of truth arguments.

### 9.7 Exact second-order values distinguish the hulls

The same example has compact rational primal and dual certificates. With (72), the common first direction is $`z_h=(1/2,1/2,0,0,0,0)`$. For a truth with repeated flag $`a`$, put

```math
A_G(v,w)=\frac14-(p-v)\cdot w,\qquad
A_F(v,w)=\frac52-6a-
\mathrm{diag}(4,4,100,100,100,100)[p-v,w].
\quad\text{(73)}\quad
```

Here the diagonal expression denotes its bilinear form. These are exactly the coefficients (43), obtained from the actual potentials (69), not separately chosen linear data.

For the coupled hull, the tangent correction

```math
w_{\mathrm c}=(12/41,12/41,3/328,3/328,-3/328,-3/328)
```

has every coefficient at least $`7/82`$. Substitution into the three truth classes verifies the lower bound. For every ambient $`w`$, the identity

```math
\frac{100}{123}A_G(v_5,w)
+\frac{11}{123}A_F(v_5,w)
+\frac{12}{123}A_F(v_0,w)=\frac7{82}
\quad\text{(74)}\quad
```

gives the matching dual bound. Thus $`\tau_{\mathrm c}=7/82`$.

For the product hull, $`w_{\mathrm p}=(15/26,15/26,0,0,0,0)`$ gives every coefficient at least $`-1/26`$. Let $`v_{a,+}=(a,a,1,1,0,0)`$, $`v_{a,-}=(a,a,0,0,1,1)`$. The dual identity is

```math
\frac6{13}A_G(v_{0,+},w)+\frac6{13}A_G(v_{0,-},w)
+\frac1{26}A_F(v_{1,+},w)+\frac1{26}A_F(v_{1,-},w)
=-\frac1{26}.
\quad\text{(75)}\quad
```

The coefficients in each identity are nonnegative and sum to one; the $`w`$-terms cancel. Therefore $`\tau_{\mathrm p}=-1/26`$. Theorem 7 consequently gives signed optimal excesses
$`-7\varepsilon^2/82+o(\varepsilon^2)`$ and
$`\varepsilon^2/26+o(\varepsilon^2)`$, respectively. The explicit interval proof in Section 9.6 does not depend on these asymptotics.

**Corollary — A joint-hull representation obstruction.** No decision rule given only the common context and disturbance, affine and tangent geometry, separate block projections, and the complete ambient score functions can correctly decide local common repair for every instance in a class containing both $`C_{\mathrm c}`$ and $`C_{\mathrm p}`$.

The inputs just listed are identical in the two instances, but their correct feasibility answers differ. A representation adequate for both must retain the relevant joint truth constraints or information that distinguishes them. This does not identify a unique minimal representation, prove that every joint moment is necessary, or establish a cognitive realization of either truth family.

## 10. An obstruction invisible to the full Taylor data

The joint-hull example changes the truth constraints while preserving the whole score functions. A different obstruction keeps the truth hull fixed and changes the generators by a smooth perturbation that is flat at the coherent context.

### 10.1 Two globally smooth positive-curvature potentials

Let $`s_0=1/2`$. Choose a smooth cutoff $`0\leq\chi\leq1`$, equal to one on an interval $`I`$ around $`s_0`$, with support contained in $`(1/4,3/4)`$. Define

```math
r_0(s)=1+\chi(s)\left(\frac{s}{1-s}-1\right),
```

with the expression extended by $`1`$ outside the support. It is positive and $`C^\infty`$ on the real line. On $`I`$ it is exactly $`s/(1-s)`$. Put

```math
h(s)=
\begin{cases}
0,&s\leq s_0,\\
\exp\bigl(-1/(s-s_0)^2\bigr),&s>s_0,
\end{cases}
\qquad
r_1(s)=r_0(s)e^{h(s)}.
\quad\text{(76)}\quad
```

The function $`h`$ and all its derivatives vanish at $`s_0`$, while it is strictly increasing to its right. Integrate $`r_0,r_1`$ twice to obtain potentials $`\psi_0,\psi_1`$, normalized by
$`\psi_i(s_0)=\psi_i'(s_0)=0`$.
Both are globally smooth with positive curvature, and every derivative of $`\psi_0`$ and $`\psi_1`$ agrees at $`s_0`$.

On the diagonal segment compare the same quadratic potential $`G(x,y)=(x^2+y^2)/2`$ with, separately,
$`F_i(x,y)=\psi_i(x)+\psi_i(y)`$.

### 10.2 Exact common repair for the unperturbed potential

For $`t_1,t_2\in I`$, let

```math
q=\sqrt{\frac{t_1^2+t_2^2}{2}}.
\quad\text{(77)}\quad
```

This lies between $`t_1,t_2`$, hence in $`I`$. For the quadratic score, the truth-zero loss is unchanged, while truth-one loss decreases because the root mean square is at least the arithmetic mean.

For $`B_0(t)=D_{\psi_0}(1,t)`$, one has $`B_0'(t)=-t`$ on $`I`$, so $`B_0(t)=C_0-t^2/2`$. The nonlinear truth-one loss is therefore also unchanged by (77). For $`A_0(t)=D_{\psi_0}(0,t)`$, the derivative of $`u\mapsto A_0(\sqrt u)`$ is $`r_0(\sqrt u)/2`$, which is increasing. Jensen's inequality shows that the truth-zero loss does not increase.

Thus (77) is a common weak repair. Its signed optimal worst excess is exactly zero. Any smaller coherent $`q`$ worsens the nonlinear truth-one loss; any larger one worsens the quadratic truth-zero loss. These comparisons also exclude candidates outside $`I`$, using global monotonicity of the endpoint loss.

### 10.3 No exact common repair after the flat perturbation

Take the ray $`t_1=s_0`$, $`t_2=s_0+\varepsilon`$, for small $`\varepsilon>0`$. Put

```math
u_0=t_1^2,\quad u_1=t_2^2,\quad
m=\frac{u_0+u_1}{2}.
```

The quadratic truth-zero constraint requires $`q^2\leq m`$. For
$`B_1(t)=D_{\psi_1}(1,t)`$, equation (76) gives

```math
B_1(t)=C_1-\frac12K(t^2),
\qquad K'(u)=e^{h(\sqrt u)}
\quad\text{(78)}\quad
```

on the relevant interval. The derivative $`K'`$ is strictly increasing for $`u>u_0`$, so $`K`$ is strictly convex there. The nonlinear truth-one constraint would require

```math
K(q^2)\geq\frac{K(u_0)+K(u_1)}2>K(m),
\quad\text{(79)}\quad
```

contradicting $`q^2\leq m`$. A candidate $`q\leq s_0`$ also fails, since the strictly decreasing $`B_1`$ then exceeds the average of its values at $`s_0`$ and $`s_0+\varepsilon`$. All remaining possible candidates lie in the local interval on which (78) holds. Thus there is no common weak repair.

### 10.4 Positive obstruction smaller than every power

Let $`R_1(\varepsilon)`$ be the signed minimax excess under $`G,F_1`$. Continuity on the compact coherent segment guarantees attainment. Since no weak repair exists,
$`R_1(\varepsilon)>0`$.
At the old root-mean-square candidate $`q=\sqrt m`$, every comparison except the nonlinear truth-one comparison remains nonpositive. For the nonlinear truth-zero comparison this follows again from Jensen: $`r_1`$ is increasing on the local interval.

The only positive excess is

```math
J_\varepsilon=
\frac{K(u_0)+K(u_1)}2-K(m).
```

Write $`L=u_1-u_0=\varepsilon+\varepsilon^2`$. On this interval,
$`1\leq K'(u)\leq e^{h(s_0+\varepsilon)}`$, so

```math
0<R_1(\varepsilon)\leq J_\varepsilon
\leq\frac L2\left(e^{h(s_0+\varepsilon)}-1\right)
\leq(\varepsilon+\varepsilon^2)e^{-1/\varepsilon^2}
\quad\text{(80)}\quad
```

for sufficiently small $`\varepsilon`$. In particular, $`R_1(\varepsilon)=o(\varepsilon^N)`$ for every fixed $`N`$, while it remains strictly positive. For the unperturbed pair, $`R_0(\varepsilon)=0`$.

The generators have the same full Taylor data at the coherent context, but exact repair differs. One qualification is essential: the uncentered losses $`D_{\psi_i}(v,t)`$ can differ in their constant truth terms $`\psi_i(v)`$. The losses actually relevant to the repair decision can be centered:

```math
\widetilde D_{\psi_i}(v,t)
=D_{\psi_i}(v,t)-D_{\psi_i}(v,s_0).
\quad\text{(81)}\quad
```

These centered losses have the same entire forecast jet at $`s_0`$, including their values, and centering does not alter any repair comparison.

**Theorem 9 — Smooth jet data do not decide exact local repair.** In the class of smooth positive-curvature scoring problems, even the complete jets of the generators, or of the centered truth losses, at a coherent context do not determine whether exact common repair exists nearby. Every tolerance bounded below by a positive polynomial power eventually absorbs the particular obstruction (80).

This does not assert that the optimized regret is itself differentiable to all orders. The point is its size bound and exact positivity. Nor does it identify a smooth jet with a function germ: distinct smooth germs can share a jet.

For real-analytic germs, the full Taylor series determines the local function, so this particular full-jet ambiguity is unavailable. A fixed finite jet remains insufficient without further restrictions. Replacing the flat $`h`$, near $`s_0`$, by $`(s-s_0)^{2m}`$ preserves any prescribed finite collection of derivatives when $`m`$ is large enough, while the strict-convexity argument on the positive ray still supplies failure. The resulting germs are analytic near $`s_0`$; the global cutoff extension is smooth, and no claim of analyticity on the whole truth neighborhood is being substituted. A known finite polynomial-degree bound is additional information and can make finitely many coefficients determine a polynomial.

## 11. Interpretation and unresolved scope

The results separate three levels of information. First-order curvature identifies which corrections can agree to sublinear accuracy. On higher-rank additive blocks, compatibility across every coherent context forces a strong exact relationship between standards. On rank-one blocks, the admissible relationship is wider and is governed by endpoint-mean comparison. Beyond those classifications, exact repair can depend on the joint truth constraints and on information invisible to finite, or even infinite smooth, Taylor data at one point.

These distinctions constrain applications to rational revision, recognition and restoration. A mechanism that observes only marginals or a local metric cannot be assumed to implement every shared improvement available under a richer truth model. A successful repair can also reveal information about relative scoring weights, as Section 2.4 demonstrates. Neither conclusion identifies which weights have objective authority, or establishes that an agent has cognitively adopted a particular representation. Mathematical feasibility, a proposed interpretation, empirical implementation and justified normativity remain distinct claims.

Several questions remain outside the proved scope:

- At a boundary coherent context, tangent-cone geometry replaces the relative-interior arguments. The positive-weight and tangent-ball proofs cannot simply be reused.
- The higher-rank theorem does not classify arbitrary coupled hulls with rank-one blocks. The polynomial example proves that isolated-block classification alone is insufficient.
- A zero second-order margin requires further information. The present counterexamples rule out a universal decision from that margin; they do not characterize every zero-margin analytic problem.
- Infinite families with only local Hessian agreement need additional uniformity hypotheses for a common tolerance or strict margin. The exact anchor theorem and rank-one interval theorem use stronger global structure.
- The representation obstructions do not determine a unique minimal sufficient description, nor do they prove that a proposed noetic field, differential model or cognitive process realizes these finite structures.

The exposition preserves both positive constructions and negative results. The fact that one representation is insufficient is not a replacement proof of a different philosophical or scientific conclusion.

## 12. References and verification scope

### 12.1 Primary literature

1. L. M. Bregman. “The relaxation method of finding the common point of convex sets and its application to the solution of problems in convex programming.” U.S.S.R. Computational Mathematics and Mathematical Physics 7(3), 200–217 (1967). [DOI and publication record][1].
2. R. T. Rockafellar. “The elementary vectors of a subspace of $`R^n`$.” In Combinatorial Mathematics and its Applications, edited by R. C. Bose and T. A. Dowling, University of North Carolina Press, 104–127 (1969). [Author-hosted text][2].
3. Graham Denham. “Toric and tropical compactifications of hyperplane complements.” Annales de la Faculté des Sciences de Toulouse, série 6, 23(2), 297–333 (2014), Proposition 2.12. [Author's preprint][3].
4. Zsolt Páles. Signed Remark 5 in “Report of Meeting: The Second Debrecen–Katowice Winter Seminar on Functional Equations and Inequalities.” Annales Mathematicae Silesianae 16 (2003), printed 97–99. [Primary report, theorem and proof][4].
5. Janusz Matkowski. “Generalized weighted quasi-arithmetic means and the Kolmogorov–Nagumo theorem.” Colloquium Mathematicum 133(1) (2013), Section 5, Remark 3, printed 45–46. [Primary article][5].
6. Jason Konek. “Degrees of incoherence, Dutch bookability & guidance value.” Philosophical Studies 180, 395–428 (2023; first published online 2022). [Publication record][6]; [accepted author manuscript][konek-manuscript].
7. Mika Meitz and Alexander Shapiro. “Minimax asymptotics.” arXiv:2504.11269v1 (2025), Proposition 2.3. [Primary preprint][7].
8. Frank Nielsen. “Curved representational Bregman divergences and their applications.” arXiv:2504.05654v5, Sections 2 and 4. [Primary preprint][8].

### 12.2 Public mathematical predecessors

The following citations identify the public mathematical source edition underlying this exposition. Their historical filenames authenticate the sources; the definitions, proofs and scientific organization of this chapter stand on their own.

- [Quadratic local repair and quantitative identification][quadratic] and [dependency-weight rigidity][dependency] support Sections 1–3.
- [Smooth categorical rigidity][categorical], [general higher-rank blocks][blocks], and [the fixed-anchor family theorem][anchor] support Section 4.
- [Local approximate equivalence][approximate], [common nudges and endpoint separation][nudges], [the context-dependent-standard counterexample][fixed-standard], and [faithful transport][transport] support Section 5.
- [The independent rank-one proof and attribution review][rank-one-review] supports the mean-comparison reconciliation in Section 6. The complete proof is reproduced above; this citation is not a claim to have received every earlier original manuscript cited within that review.
- [First-order minimax repair][first-order], [second-order repair and its dual][second-order], and [the critical-zero counterexample][critical-zero] support Sections 7–8.
- [The polynomial coupled construction][polynomial-construction], [the mixed-rank development][mixed-rank], [its independent correction review][mixed-review], and [the joint-hull representation corollary][joint-hull] support Section 9.
- [The smooth full-jet obstruction][full-jet] supports Section 10.

These references are public source editions, not substitutes for independent scholarly review of the present exposition. Historical statements about an original proof packet retain their original scope; they do not establish fresh receipt or fresh execution of an unavailable packet.

### 12.3 Inspectable formal dependencies

The following received Lean sources provide formal statements and proofs for the finite polynomial constructions and their exact algebraic controls:

| Mathematical role | Source and identifying result |
|---|---|
| Positive weights for every listed truth | [Finite barycentric bridge][formal-barycentric], `FiniteHullWeights.intrinsicInterior_positive_barycentric` |
| Curvature, actual divergence and finite positivity table | [Polynomial identities][formal-polynomial], `PolynomialAND.certificateP_lower` and scalarDiv_expansion |
| Positive correction coefficients | [Correction proof][formal-correction], `ANDCorrection.all_leading_positive` |
| Actual four-coordinate gains and hull weights | [Score identities][formal-score], `ANDScore.g_gain_identity`, f_gain_identity and hull_of_inequalities |
| Isolated quartic impossibility on a rational interval | [Isolated obstruction][formal-isolated], `IsolatedObstruction.no_isolated_common_repair` |
| Six-coordinate membership | [Mixed hull][formal-hull], `MixedHull.candidate_eventually_mem` |
| Genuine derivatives and nonlinear gains | [Mixed score][formal-mixed-score], `MixedScore.potentialF_hasFDerivAt`, gainG and gainF |
| Universal mixed-rank strict repair | [Mixed repair][formal-repair], `MixedRepair.universal_strict_Bregman_repair` |
| Tangent, Hessian normals and absence of free coordinates | [Mixed geometry][formal-geometry], `MixedGeometry.span_directions_eq`, common_hessian_normal and no_free_coordinate |
| Four actual product-truth impossibility | [Product obstruction][formal-product], ProductObstruction.no_product_four_tests |
| Rational optimal margins and actual gain binding | [Coupling certificates][formal-lp], `CouplingLPValues.coupled_primal`, coupled_dual_upper, product_primal, product_dual_upper, coefficientG_binding and coefficientF_binding |

The source bodies have been inspected in preparing this exposition. No new kernel execution or complete formalization of all the general smooth theorems is asserted here. The formal dependencies and independent review records retain their own evidential roles; incorporating a prose argument does not by itself justify removing them.

[1]: https://doi.org/10.1016/0041-5553(67)90040-7
[2]: https://sites.math.washington.edu/~rtr/papers/rtr020-ElemVectors.pdf
[3]: https://arxiv.org/html/1306.3519v1
[4]: https://journals.us.edu.pl/index.php/AMSIL/article/download/14111/10836/40243
[5]: https://www.impan.pl/shop/publication/transaction/download/product/87225
[6]: https://link.springer.com/article/10.1007/s11098-022-01860-z
[konek-manuscript]: https://research-information.bris.ac.uk/ws/portalfiles/portal/336592657/Staffel_Comments.pdf
[7]: https://arxiv.org/html/2504.11269v1
[8]: https://arxiv.org/html/2504.05654v5


[quadratic]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/a9eb8521054eb3769ff424037f438ae38f0f0c113d73624efc9d05dea3b35483.md
[dependency]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/55dc1c64cb207d0a4425ec989aab9c94a65490bda4191814fa4a055d5e148aab.md
[categorical]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be.md
[blocks]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/fbf8481b03ad278b916bebf337cf340f44597697764f7e9a6fffe219f2707805.md
[anchor]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/edb8d215fa5d1aa568c596d749385b42710030e9ff3215347cdaec5185f0e854.md
[approximate]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/c08f6d75254247a8c68f49f6b4e88bedc510790c38e9d7f8c493281eafc5c418.md
[nudges]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/1a5d94a8d7a2bca031de09dafcb3fc929797b94488d10836ddb696b0e6a1be0d.md
[fixed-standard]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/0113c7c7e1e78bd51645e77ee3646c856faac79f178e9b5760285c28aeeceac2.md
[transport]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/752593a77fa180409da3bf6aa55816508362669bb055233a79ba775cd55bdd5a.md
[first-order]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/a972fc4836f42db0ca2275134ba70388eb52b7e8e53937dac969995907f052ce.md
[second-order]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/9fea0e2238e657472dd44f65855fb07db1022f26f3f3484d83221ef40bcbb9a4.md
[critical-zero]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/9c6025d6b5bdedaf238a6294e5801470756cdbf213c1696f91007fd0844ae5af.md
[mixed-rank]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/6b108a747a7674bd09ee0c34995cf877185913c270a15102ba7c0b3e9391b543.md
[full-jet]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/7b8487cdf0e216631e0277a879cf8b869ea59c47f1c0fda2058341d1c191070f.md
[rank-one-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/2fcb5545ef8694c1ddb5f0c7af321fde0c5a4f5acd6fe79153864c876ee0d9bf.md
[polynomial-construction]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/a14075e3fedc4c137316f41aea04d48e361eeddbb68a6883d1957d54c15cf664/POLYNOMIAL_AND_KERNEL_TARGET.md
[mixed-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/9c5817df2c8f6f2d0ed3fbbb172b1e924349ab0ca9c0a2414e5dead1b481e643/MIXED_RANK_REVIEW.md
[joint-hull]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/research-v6/root_math/geometry_audit_annex/JOINT_HULL_OBSTRUCTION.md
[formal-barycentric]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/ac0ed23555915fcd324b9aa575cc5acde4d57cbcbe4edacd0ef6b64665f33ef5.lean
[formal-polynomial]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/3c1721046ecb48ff4b4d1d9bde2e483cfa6ed532b69009bbd02c27ed8d9a36a5.lean
[formal-correction]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/9b040710b99321214095e434c1096b3caa1e9135e1a2bde4bf7e09eee473be94.lean
[formal-score]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/684841d865cfddb7e9f8db226a7405c39c01ed53888f8e9535906f97465ff125.lean
[formal-isolated]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/46a16f9a1886a206ec371e328c8fd2e1f0a76aa060b03889aaae00efc4c1463e.lean
[formal-hull]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/0ffac3a36170239eff7abe256d1d6cad3efdced877c284f0e09fe94cc7e27e56.lean
[formal-mixed-score]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/a7bf5cbb8651eed6571b1f3cd7aff586a0640c9eeff4b99594e2fadace16690a.lean
[formal-repair]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/2a6e62d40b426e0760d2307494c7c4abb028c680c8e888a314314c79d9f10bac.lean
[formal-geometry]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/6aed37421110678ab4ce732ee00ba61dc97397ffadc5f16941169309d1ccc44e.lean
[formal-product]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/eb26c550b7ab1aaa3f74a29ffe945d8d00c84913b0cb8b588b3f88420b89bc13.lean
[formal-lp]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/bcbdbaca18e8c2f5ab3c25e38b19587b128e215719ae3d9fc7823d7823935ed2.lean
